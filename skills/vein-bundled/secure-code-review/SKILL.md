---
name: secure-code-review
description: 安全代码审计深度专业技能：多语言漏洞模式识别（Java/Python/Go/Node.js/C#/PHP）、数据流追踪、认证授权审计、供应链安全、从代码缺陷到可利用漏洞完整分析链
version: 2.0.0
---

# 安全代码审计深度技能

## 概述

代码审计是发现漏洞根源的核心能力。本技能系统化覆盖**多语言漏洞模式→数据流追踪→认证授权缺陷→业务逻辑漏洞→供应链安全**完整审计链，聚焦于从代码中识别**可利用**的安全缺陷。

## 一、多语言漏洞模式

### 1.1 Java安全审计

**反序列化漏洞：**
```java
// 危险：未过滤的反序列化
ObjectInputStream ois = new ObjectInputStream(input);
Object obj = ois.readObject();  // 任意类反序列化

// 修复：使用白名单过滤
ObjectInputFilter filter = ObjectInputFilter.Config.createFilter("com.myapp.*;!*");
ois.setObjectInputFilter(filter);
```

**JNDI注入：**
```java
// 危险：用户可控的JNDI查询
Context ctx = new InitialContext();
Object obj = ctx.lookup(userInput);  // JNDI注入RCE

// 危险：@type反序列化（Fastjson）
JSON.parseObject(userInput);  // @type字段控制类加载
```

**SpEL/OGNL注入：**
```java
// 危险：表达式注入
SpelExpressionParser parser = new SpelExpressionParser();
Expression exp = parser.parseExpression(userInput);
exp.getValue();  // RCE

// 危险：OGNL（Struts2）
OgnlUtil.callMethod(userInput, context, root);
```

**SQL注入（Java特有）：**
```java
// 危险：字符串拼接
String sql = "SELECT * FROM users WHERE id = " + userId;
stmt.executeQuery(sql);

// 危险：MyBatis ${}
<select id="find">
  SELECT * FROM users WHERE name = '${name}'  // ${}不转义
</select>

// 修复：MyBatis #{}
<select id="find">
  SELECT * FROM users WHERE name = #{name}  // #{}参数化
</select>
```

**XXE（Java）：**
```java
// 危险：未禁用外部实体的解析器
DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
DocumentBuilder builder = factory.newDocumentBuilder();
Document doc = builder.parse(inputStream);

// 修复
factory.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
factory.setFeature("http://xml.org/sax/features/external-general-entities", false);
```

**SSRF（Java）：**
```java
// 危险：用户可控URL
URL url = new URL(userInput);
HttpURLConnection conn = (HttpURLConnection) url.openConnection();
// 可访问内网/云元数据 169.254.169.254
```

### 1.2 Python安全审计

```python
# 危险：命令注入
import os
os.system("ping " + user_input)
subprocess.call("cmd " + user_input, shell=True)

# 危险：反序列化
import pickle
data = pickle.loads(user_input)  # RCE

# 危险：SSTI
from jinja2 import Template
Template(user_input).render()  # {{config}}泄露
# {{''.__class__.__mro__[1].__subclasses__()}}

# 危险：SQL注入
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
cursor.execute("SELECT * FROM users WHERE id = %s" % user_id)

# 危险：路径遍历
open(os.path.join(base_dir, user_input))

# 危险：eval/exec
eval(user_input)
exec(user_input)

# 危险：YAML
import yaml
yaml.load(user_input)  # yaml.load()不安全
yaml.safe_load(user_input)  # 修复
```

### 1.3 Go安全审计

```go
// 危险：命令注入
cmd := exec.Command("sh", "-c", userInput)  // 用户可控命令

// 危险：SQL注入
db.Query("SELECT * FROM users WHERE id = " + id)
// 修复
db.Query("SELECT * FROM users WHERE id = ?", id)

// 危险：路径遍历
http.ServeFile(w, r, filepath.Join(base, r.URL.Query().Get("file")))
// 需要 filepath.Clean + 前缀检查

// 危险：SSRF
resp, err := http.Get(userInput)  // 用户可控URL

// 危险：不安全的随机数
import "math/rand"
token := rand.Int()  // 可预测
// 修复
import "crypto/rand"
```

### 1.4 Node.js安全审计

```javascript
// 危险：命令注入
const { exec } = require('child_process');
exec('cmd ' + userInput);  // 命令注入

// 危险：原型污染
const merge = (target, source) => {
    for (let key in source) {
        target[key] = source[key];  // __proto__污染
    }
};

// 危险：NoSQL注入
db.users.find({ username: req.body.username });
// { "$gt": "" } 绕过认证

// 危险：SSTI
const template = require('pug').compile(userInput);

// 危险：路径遍历
res.sendFile(path.join(__dirname, req.query.file));
// 修复：path.resolve + startsWith检查
```

### 1.5 PHP安全审计

```php
// 危险：文件包含
include($_GET['page']);  // LFI/RFI
include('php://filter/convert.base64-encode/resource=config');  // 利用流

// 危险：命令执行
system("ping " . $_GET['host']);
exec("cmd " . $_POST['input']);
// 分隔符：; | & || && ` $() \n

// 危险：反序列化
unserialize($_GET['data']);  // POP链RCE

// 危险：SQL注入
$query = "SELECT * FROM users WHERE id = " . $_GET['id'];

// 危险：preg_replace /e修饰符
preg_replace('/pattern/e', 'code', $input);

// 危险：类型混淆
if ($user == "admin") { }  // == 宽松比较
if ($user === "admin") { }  // === 严格比较（修复）
```

### 1.6 C#安全审计

```csharp
// 危险：反序列化
BinaryFormatter bf = new BinaryFormatter();
object obj = bf.Deserialize(stream);  // RCE

// 危险：ViewState未加密
// EnableViewStateMac=false

// 危险：LDAP注入
DirectorySearcher searcher = new DirectorySearcher();
searcher.Filter = "(&(cn=" + userInput + "))";

// 危险：XPath注入
XmlDocument doc = new XmlDocument();
XmlNode node = doc.SelectSingleNode("//user[@name='" + userInput + "']");
```

## 二、数据流追踪方法

### 2.1 Source-Sink分析
```
Source（输入源）:
- HTTP参数（GET/POST/Header/Cookie）
- 文件上传内容
- 数据库查询结果（二次注入）
- 外部API响应
- 环境变量/配置

Sink（危险操作）:
- SQL查询
- 命令执行
- 文件操作
- 反序列化
- 表达式解析
- LDAP/XPath查询
- HTTP请求（SSRF）

追踪路径:
Source → [Transform] → [Sanitize?] → Sink
```

### 2.2 关键审计路径
```
1. 认证流程：Login → Token验证 → 会话管理 → 权限检查
2. 授权流程：请求 → 权限校验 → 数据访问 → 响应过滤
3. 文件操作：上传路径 → 存储路径 → 访问路径 → 下载路径
4. API链路：请求解析 → 参数验证 → 业务逻辑 → 数据操作
```

## 三、认证与授权审计

### 3.1 认证缺陷检查
```
- 弱密码策略（长度/复杂度/历史）
- 暴力破解防护（速率限制/锁定）
- 会话管理（Session固定/劫持/超时）
- Token安全（JWT签名/过期/存储）
- MFA实现（绕过/降级/恢复码）
- OAuth实现（redirect_uri/State/Scope）
- 密码存储（明文/弱Hash/盐）
```

### 3.2 授权缺陷检查
```
- 水平越权（IDOR：用户A访问用户B数据）
- 垂直越权（普通用户访问管理员功能）
- 功能级越权（API接口无权限校验）
- 数据级越权（查询条件无所有者过滤）
- 文件级越权（路径遍历/未授权下载）
- API越权（BOLA/BFLA/Mass Assignment）
```

## 四、业务逻辑审计

```
- 支付逻辑（价格篡改/数量负数/0元支付）
- 优惠券/积分（重复使用/超额/竞态条件）
- 验证码（绕过/复用/OCR/竞态）
- 密码重置（Token预测/邮件注入/逻辑缺陷）
- 注册流程（用户名冲突/邮箱验证绕过）
- 投票/限制（Cookie/IP/竞态绕过）
```

## 五、供应链安全审计

```
- 依赖漏洞（CVE检测：npm audit/pip audit/mvn dependency）
- 恶意包（typosquatting/dependency confusion）
- 构建安全（CI/CD管道注入/密钥泄露）
- 镜像安全（Docker Hub恶意镜像/基础镜像漏洞）
- 第三方SDK（数据外传/后门/过度权限）
- 开源合规（许可证冲突/代码抄袭）
```

## 六、工具链

```bash
# 静态分析
Semgrep               # 多语言SAST
SonarQube             # 代码质量+安全
CodeQL                # GitHub高级SAST
Fortify               # 企业级SAST

# 依赖分析
trivy                 # 依赖漏洞扫描
snyk                  # 依赖安全
npm audit / pip audit # 包管理审计
OWASP Dependency-Check # 依赖CVE检测

# 密钥检测
truffleHog            # Git历史密钥
git-secrets           # 提交前检测
gitleaks              # 仓库扫描

# 代码审计辅助
VS Code + 审计插件
JADX（Java反编译）
dnSpy（.NET反编译）
Ghidra（Native逆向）
```

## 七、测试检查清单

- [ ] Source-Sink数据流追踪
- [ ] 输入验证（类型/长度/范围/格式）
- [ ] 输出编码（HTML/JS/URL/CSS上下文）
- [ ] 认证安全（密码策略/MFA/会话/Token）
- [ ] 授权安全（水平/垂直/功能级/数据级）
- [ ] 加密安全（算法/密钥/随机数/协议）
- [ ] 错误处理（信息泄露/日志敏感数据）
- [ ] 依赖安全（CVE/恶意包/版本过时）
- [ ] 业务逻辑（支付/优惠券/验证码/竞态）
- [ ] 日志与审计（操作日志/异常告警）
