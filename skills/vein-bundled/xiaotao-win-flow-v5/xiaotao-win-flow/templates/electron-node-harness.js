/**
 * electron-node-harness.js — Electron-as-Node 离线 harness 模板
 *
 * 用途:主进程被反注入手段挡住时(asar integrity fuse 挡改包 / `--inspect` 崩溃 /
 * 单例锁踢掉重注入进程),把目标自己的 .jsc/JS 模块脱离真实 GUI,用
 * `ELECTRON_RUN_AS_NODE=1` 当纯 Node 加载进独立进程直接 require/调用——
 * 铁律23 通道优先级里"Electron-as-Node 离线调用"这一档的具体实现。
 *
 * 依赖(先问用户同意再装,铁律5):
 *   npm install --save-dev proxyquire nock
 * 装之前用 tool-registry.md §5.8 对应条目 `fetch-tool.ps1 -Probe` 确认可用。
 *
 * 用法:
 *   1. 改下面 "==== 改这里 ====" 区块的路径/常量。
 *   2. ELECTRON_RUN_AS_NODE=1 EE_BASE_DIR=... node electron-node-harness.js
 *   3. 需要测多个候选(密钥/响应格式/gate位置)时,用 CANDIDATES 数组一次跑完
 *      (铁律25:路线评分接近或有多个独立子假设时,批量并行测,不改一次脚本跑一次)。
 *
 * 本模板只处理"通用部分"(require('electron') 桩、HTTP 拦截),这两块优先用
 * proxyquire/nock 而不是手写——本次会话踩过的两个具体坑就是手写这两块导致的:
 *   - 手写 http.request 重定向:闭包忘记调用保存的原函数,导致自己重定向自己,
 *     表现为无限重试循环(看起来像目标在无限重连,其实是 harness 自己的 bug)。
 *   - 手写 EventEmitter 假 IncomingMessage/ClientRequest:axios 的 http adapter
 *     内部读取真实 socket/IncomingMessage 才有的属性,手搭的假对象缺这些属性,
 *     抛 `Cannot read properties of undefined (reading 'includes')`。
 * "目标专属部分"(ee-core 环境变量、path.join 补丁、jsencrypt 自动填充公钥)
 * 没有通用库可用,仍需按目标手写,已保留在下面对应区块。
 */

'use strict';

// ==================== 改这里:目标专属常量 ====================

const path = require('path');

const TARGET = {
  // 目标解包出的 app 目录(如 asar extract 后的目录 / resources/app)
  appDir: 'C:/path/to/target/_re/app_extracted',
  // ee-core 目标需要的环境变量(非 ee-core 目标可留空对象跳过这一段)
  eeEnv: {
    EE_BASE_DIR: 'C:/path/to/target/_re/app_extracted',
    EE_ELECTRON_DIR: 'C:/path/to/target/_re/app_extracted',
    EE_ENV: 'prod',
    EE_APP_USER_DATA: 'C:/Users/you/AppData/Roaming/目标AppName',
    EE_EXEC_DIR: 'C:/path/to/target/_re/app_extracted',
  },
  // 要 require 的目标模块(相对 appDir),例如 controller/user.jsc
  moduleToLoad: 'controller/user.jsc',
  // 目标真实域名(用于 nock 拦截时匹配 host)
  realHost: 'https://real-server.example.com',
};

// 一次跑完的候选集合(密钥/响应格式/gate位置等独立子假设),铁律25:
// 有多个互不依赖的候选时批量测,不要改一次脚本重跑一次。
const CANDIDATES = [
  // { name: 'K候选1', key: '...' },
  // { name: '响应格式plain', fmt: 'plain' },
];

// ==================== 通用部分:electron stub(用 proxyquire) ====================

// proxyquire 直接替代手写的 Module._load 拦截 + Proxy 桩。
// 用法示例(在实际 require 目标模块处按需调整):
//
//   const proxyquire = require('proxyquire');
//   const fakeElectron = {
//     app: { getPath: () => 'STUB', on: () => {}, whenReady: () => Promise.resolve() },
//     ipcMain: { on: () => {}, handle: () => {} },
//     BrowserWindow: function () { return { loadURL: () => {}, on: () => {} }; },
//     '@noCallThru': true, // 告诉 proxyquire 不要真的加载原始 electron 模块
//   };
//   const userController = proxyquire(
//     path.join(TARGET.appDir, TARGET.moduleToLoad),
//     { electron: fakeElectron }
//   );
//
// 若目标模块是多层 require electron(深层依赖也 require 了 electron),
// proxyquire 默认只替换直接 require 的那一层;深层用 `@global: true` 全局生效:
//   { electron: fakeElectron, '@global': true }

// ==================== 通用部分:HTTP 拦截(用 nock) ====================

// nock 直接替代手写的 http/https.request 全局重定向 + 手搭 http.createServer。
// 用法示例:
//
//   const nock = require('nock');
//   const scope = nock(TARGET.realHost)
//     .post('/v2/login')
//     .reply(200, (uri, requestBody) => {
//       // requestBody 是目标发出的真实加密载荷,在这里按候选构造伪造响应
//       return JSON.stringify({ code: 200, msg: '操作成功', data: { /* ... */ } });
//     });
//
// 批量测多个候选格式时,可对每个候选单独起一个 nock scope 循环跑:
//
//   for (const c of CANDIDATES) {
//     nock.cleanAll(); // 清掉上一个候选的拦截,避免干扰
//     nock(TARGET.realHost).post('/v2/login').reply(200, buildForgedBody(c));
//     const result = await callLoginViaHarness(); // 调用目标的 login()
//     console.log(`[${c.name}] =>`, result);
//   }
//
// nock 默认拦截所有未显式放行的请求(nock.disableNetConnect() 可强制),
// 天然兼容 axios 内部对 http.ClientRequest/IncomingMessage 的读取方式,
// 不会出现手写 mock 缺属性导致的 axios adapter 报错。

// ==================== 目标专属:ee-core 环境变量(无 ee-core 可删) ====================

function seedEeCoreEnv() {
  for (const [k, v] of Object.entries(TARGET.eeEnv)) {
    if (v) process.env[k] = v;
  }
}

// ==================== 目标专属:path.join 补丁(绕 undefined 参数) ====================

function patchPathJoinForUndefinedArgs() {
  const origJoin = path.join.bind(path);
  path.join = function (...args) {
    const patched = args.map((a) => {
      if (a === undefined || a === null) {
        console.warn('[harness] path.join got undefined/null arg, substituting STUB. stack:', new Error().stack.split('\n')[2]);
        return 'STUB';
      }
      return a;
    });
    return origJoin(...patched);
  };
}

// ==================== 目标专属:jsencrypt 自动填充公钥(绕"请先设置RSA公钥"guard) ====================

function autoSeedJsEncrypt(fakeKeyPair) {
  let JSEncrypt;
  try {
    JSEncrypt = require(path.join(TARGET.appDir, 'node_modules/jsencrypt')).JSEncrypt;
  } catch (e) {
    console.warn('[harness] jsencrypt not found under target node_modules, skip auto-seed:', e.message);
    return;
  }
  const origSetPublicKey = JSEncrypt.prototype.setPublicKey;
  const origEncrypt = JSEncrypt.prototype.encrypt;
  JSEncrypt.prototype.encrypt = function (text) {
    if (!this.key || !this.key.n) {
      origSetPublicKey.call(this, fakeKeyPair.publicKey);
    }
    return origEncrypt.call(this, text);
  };
}

// ==================== 主流程 ====================

async function main() {
  seedEeCoreEnv();
  patchPathJoinForUndefinedArgs();

  // const fakeKeyPair = require('./fake_rsa.json');
  // autoSeedJsEncrypt(fakeKeyPair);

  // const proxyquire = require('proxyquire');
  // const fakeElectron = { /* 见上方示例 */ '@noCallThru': true };
  // const userController = proxyquire(
  //   path.join(TARGET.appDir, TARGET.moduleToLoad),
  //   { electron: fakeElectron }
  // );

  // const nock = require('nock');
  // 逐个候选批量测(铁律25):
  // for (const c of CANDIDATES) {
  //   nock.cleanAll();
  //   nock(TARGET.realHost).post('/v2/login').reply(200, /* 按候选构造 */);
  //   const result = await userController.login(JSON.stringify({ /* ... */ }));
  //   console.log(`[${c.name}] =>`, result);
  // }

  console.log('[harness] 骨架就位,按上方示例填充 moduleToLoad / CANDIDATES / 请求体后运行。');
}

main().catch((e) => {
  console.error('[harness] fatal:', e);
  process.exit(1);
});
