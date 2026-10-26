/**
 * mitm-observer.js — 被动抓包 + 加解密观察器(Windows / Node / Electron 场景)
 * ============================================================================
 * 用途:铁律19「三段式」的第①步「被动观察」。**只记录,不改任何流向/返回值**,
 *       让目标打真实服务端,一次性拿全:http(s) 请求/响应 + 各加密库 key/iv/mode + 明文/密文。
 *       拿到样本后:第②步离线用 Python/Node 验证能否解出已知密文,第③步才写伪造。
 *
 * 为什么"一次性全量 hook"(铁律20):授权类客户端的**请求加密**和**响应解密**
 *       完全可能用不同库(实测:请求 crypto-js、响应解密 Node 原生 crypto)。
 *       渐进式先猜一个库必踩坑,所以下面把常见几类**同时**挂上。
 *
 * 为什么输出到文件不用 stdout(铁律21 / 笔记问题8):
 *       Windows 下重定向或父进程退出后子进程 stdout 易产 0 字节/丢日志。
 *       这里直接在目标进程内用 Node 的 fs 追加写日志文件。
 *
 * ── ⚠ 运行环境:这是「目标自身 Node 上下文」里跑的 monkey-patch,不是 Frida GumJS 脚本 ──
 *  本文件用了 `require()` / `Buffer` / `fs` —— 这些是 **Node 全局**。
 *  **Frida 的 `-l` 把脚本跑在 GumJS 运行时里,GumJS 没有 `require`/`Buffer`/`fs`,直接 `-l` 本文件会立刻报错。**
 *  正确注入方式(任选,都要让代码在目标的 Node/Electron 主进程上下文里执行):
 *   A. **改 Electron 入口注入**(最直接):asar 解包后在 `main.js`/入口 `.js` 顶部 `require()` 本文件
 *      (或把内容贴进去),按铁律21 重打包(先判 integrity fuse);仅用于观察,拿完样本即还原。
 *   B. **调试端口注入**:目标以 `--inspect` 启动时,用 Node Inspector / DevTools 连上,在其
 *      Console 里 `require('C:/绝对路径/mitm-observer.js')` 让它在主进程上下文求值。
 *   C. **要用 Frida**:不能 `-l` 本文件;需另写 GumJS 脚本,用 `Interceptor` 在 native 层 hook,
 *      或通过 Frida 拿到目标的 V8/Node 上下文再注入本段(自行改造),不在本模板范围内。
 *
 * ── 适配须知(每个目标都要按需改)─────────────────────────────────────────
 *  - LOG_FILE 改成目标工作目录下的可写路径(建议放 <目标>-attempts 同目录)。
 *  - 目标若用打包/改名后的模块(webpack 后 crypto-js 可能被内联),按模块名 `require` 可能拿不到,
 *    需在 DevTools 里定位真实对象再 hook(或改用方式 C 的 native 兜底)。
 *  - 这是**模板**,不是即插即用成品;跑之前先确认注入通道可用、目标非模态状态(铁律17)。
 * ============================================================================
 */

'use strict';

// ==== 配置:按目标改 ====
const LOG_FILE = 'C:\\re-work\\mitm-observer.log'; // TODO: 改成目标工作目录下的可写绝对路径(单反斜杠转义即可)
const MAX_BODY = 4096; // 单条 body 最多记多少字节,防日志爆炸
// =========================

function _now() { return new Date().toISOString(); }

function _log(tag, obj) {
  let line;
  try {
    line = `[${_now()}] [${tag}] ` + (typeof obj === 'string' ? obj : JSON.stringify(obj)) + '\n';
  } catch (e) {
    line = `[${_now()}] [${tag}] <unserializable: ${e}>\n`;
  }
  try {
    // 在目标进程内用 Node fs 追加写,避免 stdout 丢日志(铁律21)
    require('fs').appendFileSync(LOG_FILE, line);
  } catch (e) {
    // 万一 fs 不可用(纯 renderer 无 node 集成),退回 console 但明确标注
    console.log('[MITM-NO-FS] ' + line);
  }
}

function _hex(buf) {
  try {
    const b = Buffer.isBuffer(buf) ? buf : Buffer.from(buf);
    return b.slice(0, MAX_BODY).toString('hex');
  } catch (e) { return '<hex-fail>'; }
}

function _preview(x) {
  try {
    if (Buffer.isBuffer(x)) return { type: 'Buffer', len: x.length, hex: _hex(x) };
    if (typeof x === 'string') return { type: 'string', len: x.length, val: x.slice(0, MAX_BODY) };
    return { type: typeof x, val: String(x).slice(0, MAX_BODY) };
  } catch (e) { return '<preview-fail>'; }
}

_log('BOOT', `mitm-observer 启动,日志写入 ${LOG_FILE}`);

// ─────────────────────────────────────────────────────────────────────────
// 1) Node 原生 crypto:createCipheriv / createDecipheriv(捕获 algo/key/iv + 出入参)
// ─────────────────────────────────────────────────────────────────────────
try {
  const crypto = require('crypto');

  ['createCipheriv', 'createDecipheriv'].forEach(function (fn) {
    if (typeof crypto[fn] !== 'function') return;
    const orig = crypto[fn];
    crypto[fn] = function (algorithm, key, iv, ...rest) {
      _log('node-crypto', {
        fn: fn,
        algorithm: algorithm,
        key: _preview(key),
        iv: _preview(iv),
      });
      const cipher = orig.call(this, algorithm, key, iv, ...rest);
      // 记录 update/final 的出入参(明文<->密文样本)
      ['update', 'final'].forEach(function (m) {
        if (typeof cipher[m] !== 'function') return;
        const om = cipher[m];
        cipher[m] = function (...args) {
          if (args.length) _log('node-crypto', { fn: fn + '.' + m, in: _preview(args[0]) });
          const out = om.apply(this, args);
          if (out !== undefined) _log('node-crypto', { fn: fn + '.' + m, out: _preview(out) });
          return out;
        };
      });
      return cipher;
    };
  });

  // 兼容老 API createCipher/createDecipher(仅口令,无 iv)
  ['createCipher', 'createDecipher'].forEach(function (fn) {
    if (typeof crypto[fn] !== 'function') return;
    const orig = crypto[fn];
    crypto[fn] = function (algorithm, password, ...rest) {
      _log('node-crypto', { fn: fn, algorithm: algorithm, password: _preview(password) });
      return orig.call(this, algorithm, password, ...rest);
    };
  });

  // 公钥/私钥运算(RSA 等)
  ['publicEncrypt', 'privateDecrypt', 'privateEncrypt', 'publicDecrypt', 'sign', 'verify'].forEach(function (fn) {
    if (typeof crypto[fn] !== 'function') return;
    const orig = crypto[fn];
    crypto[fn] = function (...args) {
      _log('node-crypto', { fn: fn, arg0: _preview(args[0]), arg1: _preview(args[1]) });
      return orig.apply(this, args);
    };
  });

  _log('BOOT', 'Node 原生 crypto hook 已挂');
} catch (e) {
  _log('BOOT', 'Node crypto 未加载或不可 hook: ' + e);
}

// ─────────────────────────────────────────────────────────────────────────
// 2) crypto-js:AES/DES/TripleDES 的 encrypt/decrypt(捕获 key/iv/cfg + 出入参)
//    注:webpack 打包后可能拿不到裸模块名,需在 DevTools 里定位真实对象后改这里的获取方式。
// ─────────────────────────────────────────────────────────────────────────
try {
  const CryptoJS = require('crypto-js');
  ['AES', 'DES', 'TripleDES', 'RC4', 'Rabbit'].forEach(function (algoName) {
    const algo = CryptoJS[algoName];
    if (!algo) return;
    ['encrypt', 'decrypt'].forEach(function (op) {
      if (typeof algo[op] !== 'function') return;
      const orig = algo[op];
      algo[op] = function (message, key, cfg) {
        let keyStr, ivStr;
        try { keyStr = key && key.toString ? key.toString() : String(key); } catch (e) { keyStr = '<key?>'; }
        try { ivStr = cfg && cfg.iv ? cfg.iv.toString() : undefined; } catch (e) { ivStr = '<iv?>'; }
        _log('crypto-js', {
          algo: algoName, op: op,
          key: keyStr, iv: ivStr,
          mode: cfg && cfg.mode ? String(cfg.mode) : undefined,
          in: _preview(message && message.toString ? message.toString() : message),
        });
        const out = orig.call(this, message, key, cfg);
        try { _log('crypto-js', { algo: algoName, op: op, out: out && out.toString ? out.toString() : String(out) }); } catch (e) {}
        return out;
      };
    });
  });
  _log('BOOT', 'crypto-js hook 已挂');
} catch (e) {
  _log('BOOT', 'crypto-js 未加载(可能被打包内联,需 DevTools 定位): ' + e);
}

// ─────────────────────────────────────────────────────────────────────────
// 3) RSA 库:jsencrypt / node-forge(捕获 setKey / encrypt / decrypt)
// ─────────────────────────────────────────────────────────────────────────
try {
  const JSEncrypt = require('jsencrypt').JSEncrypt || require('jsencrypt');
  if (JSEncrypt && JSEncrypt.prototype) {
    ['setPublicKey', 'setPrivateKey', 'setKey', 'encrypt', 'decrypt'].forEach(function (m) {
      if (typeof JSEncrypt.prototype[m] !== 'function') return;
      const orig = JSEncrypt.prototype[m];
      JSEncrypt.prototype[m] = function (arg) {
        _log('jsencrypt', { fn: m, in: _preview(arg) });
        const out = orig.apply(this, arguments);
        if (m === 'encrypt' || m === 'decrypt') _log('jsencrypt', { fn: m, out: _preview(out) });
        return out;
      };
    });
    _log('BOOT', 'jsencrypt hook 已挂');
  }
} catch (e) {
  _log('BOOT', 'jsencrypt 未加载: ' + e);
}

// ─────────────────────────────────────────────────────────────────────────
// 4) http / https:被动记录 request 出参 + response 入参(不改!铁律19 第①步)
// ─────────────────────────────────────────────────────────────────────────
['http', 'https'].forEach(function (modName) {
  try {
    const mod = require(modName);
    const origRequest = mod.request;
    mod.request = function (options, cb) {
      let meta;
      try {
        meta = (typeof options === 'string')
          ? { url: options }
          : { method: options.method, host: options.host || options.hostname, port: options.port, path: options.path, headers: options.headers };
      } catch (e) { meta = { parseErr: String(e) }; }
      _log(modName + '-req', meta);

      const req = origRequest.apply(this, arguments);

      // 记请求体
      const origWrite = req.write;
      req.write = function (chunk) {
        _log(modName + '-req-body', _preview(chunk));
        return origWrite.apply(this, arguments);
      };

      // 记响应体
      req.on('response', function (res) {
        const chunks = [];
        res.on('data', function (c) { try { chunks.push(Buffer.from(c)); } catch (e) {} });
        res.on('end', function () {
          let body;
          try { body = Buffer.concat(chunks); } catch (e) { body = null; }
          _log(modName + '-res', {
            statusCode: res.statusCode,
            headers: res.headers,
            body: body ? _preview(body) : '<no-body>',
          });
        });
      });
      return req;
    };
    _log('BOOT', modName + '.request hook 已挂');
  } catch (e) {
    _log('BOOT', modName + ' 未加载: ' + e);
  }
});

_log('BOOT', '全部 hook 挂载完成 —— 现在由用户手动走一遍完整授权/登录流程(铁律9),事后读日志建字段字典 + 离线验证');
