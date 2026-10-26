---
name: information-gathering
description: 信息收集深度渗透测试技能：被动/主动信息收集、子域名枚举、端口扫描、指纹识别、JS分析、云资产发现、GitHub泄露、完整攻击面映射
version: 2.0.0
---

# 信息收集深度测试技能

## 概述

信息收集是渗透测试第一阶段，通过被动+主动手段全面收集目标资产、技术栈、漏洞线索。现代信息收集覆盖OSINT（公开情报）、域名/子域名、DNS、端口/服务、Web指纹、API、云资源、泄露代码、员工信息等多维度。本技能系统化覆盖被动OSINT、主动扫描、JS信息提取、云资产发现、GitHub泄露等完整攻击面。

## 一、信息收集方法论

### 1.1 信息收集分层模型
```
Layer 1: OSINT被动收集（无流量触达目标）
Layer 2: DNS/域名层收集
Layer 3: 网络/端口/服务探测
Layer 4: Web层指纹识别
Layer 5: JS/API/敏感文件分析
Layer 6: 云资产/SaaS发现
Layer 7: 人员/组织信息
Layer 8: 历史数据/快照
```

### 1.2 信息收集类型
- **被动信息收集（Passive）**：不直接与目标交互，通过第三方数据源
- **主动信息收集（Active）**：直接向目标发送流量探测

## 二、被动信息收集（OSINT）

### 2.1 域名/Whois信息
```bash
# Whois查询
whois target.com
whois -h whois.iana.org target.com
whois target.com | grep -E "Registrant|Email|Phone|Name Server"

# 在线工具
- https://who.is
- https://whois.domaintools.com
- https://viewdns.info
- https://www.robtex.com
- https://bgp.he.net
- https://dnslytics.com

# 反查
- 同IP站点：https://viewdns.info/reverseip/
- 同注册人邮箱反查域名
- 历史Whois记录：DomainTools历史
```

### 2.2 搜索引擎Hack（Google Dorks）
```
# 基础语法
site:target.com                              限定站点
inurl:admin site:target.com                 URL中含admin
intitle:"login" site:target.com             标题含login
intext:"password" site:target.com           内容含password
filetype:pdf site:target.com                指定文件类型
cache:https://target.com                    Google缓存
link:https://target.com                     反向链接
related:https://target.com                  相关站点

# 敏感文件
site:target.com filetype:log
site:target.com filetype:sql
site:target.com filetype:conf
site:target.com filetype:bak
site:target.com filetype:env
site:target.com filetype:json inurl:api
site:target.com inurl:.git
site:target.com inurl:phpinfo.php
site:target.com "Index of /"                目录列表
site:target.com inurl:admin|login|dashboard

# 敏感信息
site:target.com "api_key"
site:target.com "aws_secret"
site:target.com "password"
site:s3.amazonaws.com "target"
site:blob.core.windows.net "target"
site:docs.google.com target.com
site:trello.com target
site:pastebin.com target
site:github.com target password
site:*.target.com -www

# Shodan/Censys/FOFA
# 设备/服务搜索
hostname:target.com
ssl.cert.subject.cn:target.com
http.html:target.com
org:"Target Company"
net:203.0.113.0/24
http.title:"Admin" target.com
product:Apache http.favicon.hash:-1337284695
```

### 2.3 GitHub/GitLab信息泄露
```bash
# GitHub搜索
"target.com" password
"target.com" secret
"target.com" api_key
"target.com" token
"target.com" AWS_SECRET_ACCESS_KEY
filename:.env target
filename:config.php target
filename:wp-config.php target
filename:.git-credentials target
path:.ssh/id_rsa target
repo:target/* password

# 工具
- GitRob/GitGot/GHunt/GitDorker
- truffleHog/git-secrets（查找硬编码密钥）
- GitHack（提取.git目录）
- shhgit 实时监控

# GitHub Dorks
filename:.npmrc _auth
filename:.dockercfg auth
extension:pem private
extension:ppk private
filename:id_rsa
filename:credentials aws
filename:s3cfg
filename:.htpasswd
filename:.git-credentials
filename:wp-config.php
filename:config.json password
```

### 2.4 Wayback Machine（历史页面）
```bash
# Wayback Machine
https://web.archive.org/web/*/https://target.com
https://web.archive.org/cdx/search/cdx?url=*.target.com/*&output=text&fl=original&collapse=urlkey

# 工具
- waybackurls: waybackurls target.com
- gau: gau target.com (Get All URLs)
- Wayback Machine CDX API

# 提取历史URL中的敏感信息
echo target.com | waybackurls | grep -E "api|admin|config|password|\.env|key|token|secret|\.git"
```

### 2.5 子域名被动收集
```bash
# 第三方数据源
- VirusTotal: https://www.virustotal.com/gui/domain/target.com/relations
- SecurityTrails: https://securitytrails.com
- Censys: https://censys.io
- Shodan: https://www.shodan.io
- FOFA: https://fofa.info (title/body/cert/host)
- Quake/360/Hunter奇安信：https://quake.360.cn / https://hunter.qianxin.com
- DNSDumpster: https://dnsdumpster.com
- crt.sh（证书透明度日志）: https://crt.sh/?q=%25.target.com
- https://search.censys.io/certificates
- https://ui.ctsearch.entrust.com

# 证书透明度（CT Logs）
curl -s "https://crt.sh/?q=%.target.com&output=json" | jq '.[].name_value' | sed 's/\"//g' | sort -u
# 快速提取所有子域
curl -s "https://crt.sh/?q=%.target.com" | grep -oE '[a-zA-Z0-9._-]+\.target\.com' | sort -u

# 工具
- amass（最全面）
- subfinder
- assetfinder
- findomain
- sublist3r
- oneforall
```

### 2.6 ASN/IP段
```bash
# ASN查询
- https://bgp.he.net
- https://ipinfo.io
- whois -h whois.radb.net -- '-i origin AS12345'
- https://rdap.arin.net/registry/autnum/ASNUMBER

# IP段查询
- ASN lookup by company: https://bgpview.io
- CIDR汇总: whois查询net range
- https://ipinfo.io/countries/CN

# DNS区域传送（AXFR）
dig axfr target.com @ns1.target.com
dnsrecon -d target.com -t axfr
fierce --domain target.com
```

### 2.7 社交媒体/人员信息
```
# 邮箱收集
- Hunter.io
- theHarvester
- snov.io
- Email格式: firstname.lastname@target / first.last@target / flast@target

# LinkedIn员工信息
linkedin.com/company/target
# 用于后续钓鱼/密码喷洒

# Google邮箱格式
"@target.com" site:linkedin.com
```

## 三、主动信息收集

### 3.1 DNS枚举
```bash
# 常见记录类型
A / AAAA / CNAME / MX / NS / TXT / SOA / SRV / PTR / HINFO / CAA / DS / DNSKEY

# DNS查询
dig target.com A
dig target.com ANY
dig target.com MX
dig target.com NS
dig target.com TXT
dig target.com SRV
dig _autodiscover._tcp.target.com SRV
dig _sip._tcp.target.com SRV

# DNS暴力枚举
# 常见子域名字典
dnsrecon -d target.com -D subdomains.txt -t brt
fierce -dns target.com -wordlist subdomains.txt
gobuster dns -d target.com -w subdomains.txt -i
puredns bruteforce subdomains.txt target.com

# DNS记录类型中可能泄露信息
- TXT: SPF/DKIM/verification tokens
- SRV: _ldap._tcp（DC）、_sip、_autodiscover、_xmpp
- CNAME: 指向云服务（.elb.amazonaws.com/.blob.core.windows.net/.cloudfront.net）
```

### 3.2 子域名爆破
```bash
# 工具
subfinder -d target.com -silent | sort -u
amass enum -passive -d target.com
amass enum -brute -d target.com -w subdomains.txt
assetfinder target.com
findomain -t target.com
puredns resolve subdomains.txt -r resolvers.txt

# 综合使用
subfinder -d target.com -silent | httpx -status-code -title -tech-detect

# 子域名字典
- seclists: Discovery/DNS/
- bitquark-subdomains-top100000.txt
- sortedcombined-knock-dnsrecon-subdomains-top1m
- Assetnote词表
- 按行业/地区定制
```

### 3.3 端口扫描
```bash
# Nmap基础
nmap -sT -p- target.com          # TCP全端口
nmap -sS -p- target.com          # SYN半开放（需root）
nmap -sU -p 53,161,162 target.com # UDP常见端口
nmap -sV -sC -O target.com       # 服务版本+默认脚本+OS
nmap -p- --min-rate 1000 target.com -oA scan

# 端口范围快速扫描
nmap -p1-65535 --min-rate 2000 -T4 target.com

# 常见服务端口速查
21 FTP / 22 SSH / 23 Telnet / 25 SMTP / 53 DNS / 69 TFTP
80 HTTP / 88 Kerberos / 110 POP3 / 111 rpcbind / 135 MSRPC / 139/445 SMB
143 IMAP / 161/162 SNMP / 389 LDAP / 443 HTTPS / 445 SMB / 500 isakmp
512/513/514 rexec/rlogin/rsh / 5432 PostgreSQL / 6379 Redis
873 rsync / 1099 Java RMI / 1433 MSSQL / 1521 Oracle / 2049 NFS
2375/2376 Docker / 3306 MySQL / 3389 RDP / 5000 Flask/WSGI
5432 PostgreSQL / 5601 Kibana / 5900 VNC / 6379 Redis
7001 WebLogic / 8080 Tomcat/HTTP / 8081/8082 / 8443 HTTPS-alt
8888 / 9000 FastCGI/PHP-FPM / 9090 / 9200/9300 Elasticsearch
11211 Memcached / 27017 MongoDB / 27018 MongoDB (auth)
50070 Hadoop Namenode / 61616 ActiveMQ
```

### 3.4 服务探测与漏洞扫描
```bash
# Nmap脚本
nmap --script=default,vuln -sV target.com
nmap --script=http-enum target.com
nmap --script=dns-zone-transfer target.com
nmap --script=smb-enum-shares,smb-enum-users target.com
nmap --script=snmp-info,snmp-sysdescr target.com
nmap --script=http-title,http-headers target.com
nmap --script=ssl-enum-ciphers target.com
nmap --script=ssh-auth-methods target.com

# Nikto Web扫描
nikto -h https://target.com

# Nuclei模板扫描
nuclei -u https://target.com -t ~/nuclei-templates/ -severity critical,high,medium

# Masscan快速端口扫描
masscan -p1-65535 --rate=10000 target.com -oL masscan.txt
# 导入nmap详细扫描
nmap -sV -sC -p $(cat masscan.txt | awk '{print $4}' | cut -d'/' -f1 | tr '\n' ',') target.com
```

## 四、Web指纹识别

### 4.1 技术栈识别
```bash
# Wappalyzer/Whatruns/WhatWeb
whatweb https://target.com
whatweb -v https://target.com

# httpx（快速批量）
httpx -l domains.txt -status-code -title -tech-detect -server -ip -cname -cdn

# 指纹识别维度
- Server头: Apache/Nginx/IIS/Tomcat/Node.js
- X-Powered-By: PHP/ASP.NET/Express
- Cookie特征: PHPSESSID/JSESSIONID/ASP.NET_SessionId/laravel_session/connect.sid
- 静态资源路径: /static/、/assets/、wp-content/
- 常见路径: /admin、/phpmyadmin、/console、/actuator、/swagger
- Favicon hash: python3 favihash.py -u https://target.com/favicon.ico

# 常见CMS指纹
WordPress: /wp-content/、/wp-includes/、/wp-json/、wp-login.php
Joomla: /administrator/、/components/、/media/
Drupal: /sites/、/modules/、/CHANGELOG.txt
DedeCMS: /uploads/、/plus/、/data/
ThinkPHP: /thinkphp/、/?s=/
Laravel: /storage/、/vendor/、XSRF-TOKEN
Spring Boot: /actuator、/swagger-ui、/api-docs
Shiro: rememberMe=deleteMe Cookie
Django: csrftoken Cookie、/admin/
Flask: /console/debugger
Nexus/Artifactory/Jenkins: 固定路径
```

### 4.2 目录/文件扫描
```bash
# 目录扫描
ffuf -u https://target.com/FUZZ -w wordlist.txt -t 50 -mc 200,301,302,403
gobuster dir -u https://target.com -w wordlist.txt -x php,asp,aspx,jsp,html,json
dirsearch -u https://target.com -e php,asp,aspx,jsp,html,js,json,bak,zip
feroxbuster -u https://target.com -w wordlist.txt
dirb https://target.com wordlist.txt

# 常见敏感路径
# 备份/源码
.bak .swp .old .zip .tar.gz .sql .git .svn .hg
backup/ backup.zip www.zip web.zip source.zip site.zip
.htaccess .htpasswd web.config .user.ini
www.rar dump.sql db.sql backup.sql

# 配置/调试
phpinfo.php info.php test.php debug.php console
.env .env.bak .env.local .env.prod
config.php config.inc.php settings.py
server-status server-info
robots.txt sitemap.xml crossdomain.xml
.htaccess httpd.conf nginx.conf

# 管理后台
admin/ administrator/ manager/ backend/ wp-admin/
phpmyadmin/ adminer/ pma/ myadmin/
jmx-console/ web-console/
actuator/ swagger-ui.html api-docs
console/ dashboard/ cpanel/

# API
api/ v1/ v2/ graphql swagger openapi.json

# 文件上传
upload/ uploads/ files/ attachments/ media/

# 错误状态码
403 → 目录存在但无权限（403bypass）
401 → 需要认证
301/302 → 重定向（跟随观察）
500 → 服务器错误（可能泄露信息）

# 403绕过
/secret → /secret/ → /secret/. → /secret%2f → /secret/.git/HEAD
/secret → /SECRET → /./secret/./ → /*/secret → /secret.json
HTTP方法切换：GET→POST→PUT→OPTIONS
添加Header: X-Forwarded-For: 127.0.0.1, X-Original-URL, X-Rewrite-URL
Referer: https://target.com/admin
```

### 4.3 SSL/TLS信息
```bash
# 证书信息
openssl s_client -connect target.com:443 </dev/null | openssl x509 -text -noout
sslscan target.com
testssl.sh target.com

# 证书透明日志中获取子域名（crt.sh前文）
# 证书中的SAN（Subject Alternative Name）列出所有域名
```

### 4.4 JavaScript分析
```bash
# 提取JS文件
echo "target.com" | waybackurls | grep "\.js" | sort -u > js.txt
cat js.txt | xargs -I {} curl -s {} | grep -Eo '"https?://[^"]*"'
# 使用LinkFinder/SecretFinder
python3 LinkFinder.py -i https://target.com/js/app.js -o cli
python3 SecretFinder.py -i https://target.com/js/app.js -o cli

# JS中提取的内容
- API端点
- API Key/Token/Secret
- 内部IP/域名
- 注释中的凭据
- 路由信息（React/Vue/Angular）
- Firebase/Supabase配置
- AWS Cognito/Amplify配置
- S3 Bucket名

# 工具
- LinkFinder: https://github.com/GerbenJavado/LinkFinder
- SecretFinder: https://github.com/m4ll0k/SecretFinder
- JSFinder/FetchSourceMap
- getJS: getJS --url https://target.com
- Packer-Fuzzer（JS混淆API接口发现）
- Burp JS Miner插件
```

### 4.5 Source Map文件
```bash
# Source Map泄露前端源码
find .js .js.map file with sourceMappingURL
# 下载.js.map文件还原完整源码
# 使用source-map-restore/unwebpack-sourcemap还原
curl https://target.com/js/app.js.map -o app.js.map
unwebpack-sourcemap app.js.map
```

## 五、云资产发现

### 5.1 S3 Bucket
```bash
# Bucket命名规律
target-prod / target-dev / target-static / target-assets
target-images / target-upload / target-backup
target-media / target-cdn / target-data

# 工具
- S3Scanner
- bucket-stream
- grayhatwarfare.com (公共Bucket搜索)
- aws s3 ls s3://target-prod --no-sign-request

# S3权限检查
aws s3api get-bucket-acl --bucket target-prod
aws s3 ls s3://target-prod
# 常见错误: AccessDenied/NoSuchBucket/AllAccessDisabled/Region错误
```

### 5.2 Azure Blob
```
xxx.blob.core.windows.net
xxx.file.core.windows.net
xxx.queue.core.windows.net
xxx.table.core.windows.net
```

### 5.3 Google Cloud Storage
```
xxx.storage.googleapis.com
storage.googleapis.com/xxx
```

### 5.4 Kubernetes/Docker API
```
- 2375 Docker API无认证
- 6443 Kubernetes API
- 8080 Kubernetes API未授权
- 10250 kubelet API
- Harbor/Registry 5000端口
```

## 六、指纹与威胁情报

### 6.1 历史数据
```
- Wayback Machine
- Search Engine Cache
- Shodan历史快照
- Censys历史证书
- DNS历史记录（SecurityTrails/DNSDB）
```

### 6.2 邮箱/账号枚举
```bash
# 邮件枚举工具
theHarvester -d target.com -b all
h8mail -t target.com

# 检查账号泄露
- Have I Been Pwned: https://haveibeenpwned.com
- Dehashed (付费)
- Snusbase
- Leakcheck
```

## 七、WAF/CDN识别

```bash
# WAF识别
wafw00f https://target.com
whatweb https://target.com | grep -i waf

# 常见WAF特征
Cloudflare: Server: cloudflare / __cfduid / cf-ray
Akamai: X-Akamai-* / Akamai-Ghost
CloudFront: X-Cache / Server: CloudFront / via:cloudfront
Incapsula/Imperva: X-Iinfo / visid_incap_
F5 BIG-IP: BigIPServer / TS*Cookie
ModSecurity: 403 Forbidden特定页面
阿里云/Azure Front Door/AWS WAF: 特征Header
安全狗/D盾/云锁: 拦截页特征
长亭雷池/SafeLine: 特征拦截页

# CDN绕过真实IP查找
- 历史DNS记录（CDN上线前的解析）
- 邮件头Received字段
- 全球PING对比（多地解析结果不同则是CDN）
- SSL证书Censys/FOFA搜索证书
- 子域名（非加速子域可能是真实IP）
- Censys/Shodan搜索证书匹配IP
- 泄露的配置文件/JS中的IP
- DNS域传送
- 外部RSS/API接口（未走CDN）
- F5/LTM/AX-Cookie解码真实IP
```

## 八、自动化编排工具

| 工具 | 用途 |
|------|------|
| amass | 子域名枚举（最全面）|
| subfinder/findomain/assetfinder | 快速子域发现 |
| httpx/catphish | HTTP探测+指纹 |
| naabu/masscan | 快速端口扫描 |
| nmap | 端口+服务+脚本 |
| nuclei | 漏洞模板扫描 |
| gau/waybackurls | 历史URL收集 |
| ffuf/gobuster/feroxbuster | 目录fuzz |
| dnsx | DNS解析验证 |
| alterx | 子域名字典排列 |
| mapcidr | CIDR处理 |
| gitdorks/trufflehog | Git密钥泄露 |
| whatweb/wappalyzer | Web指纹 |
| theHarvester | 邮箱/人员 |
| wafw00f | WAF识别 |
| CloudFail/CloudUnflare | CDN真实IP |
| autorecon | 自动化侦察 |
| finalrecon | OSINT框架 |
| reconftw | 一键信息收集 |
| osmedeus | 自动化渗透编排 |
| SpiderFoot | OSINT自动化 |

### 8.1 一键Recon流程
```bash
# 子域名枚举 + 验证 + 端口 + 路径 + 漏洞扫描 典型流程
# 1. 子域名发现
subfinder -d target.com -silent | anew subs.txt
amass enum -passive -d target.com | anew subs.txt
# 2. DNS验证
cat subs.txt | dnsx -silent -a -resp | anew resolved.txt
# 3. HTTP探测
cat resolved.txt | awk '{print $1}' | httpx -silent -title -tech-detect -status-code -cdn | anew alive.txt
# 4. 端口扫描
cat resolved.txt | naabu -silent -p - | anew ports.txt
# 5. 目录扫描
cat alive.txt | grep "200" | awk '{print $1}' | xargs -I {} ffuf -u {}/FUZZ -w wordlist.txt -t 50
# 6. Nuclei漏洞扫描
cat alive.txt | nuclei -severity critical,high -t ~/nuclei-templates/
# 7. Wayback历史
cat alive.txt | gau | anew urls.txt
cat urls.txt | gf xss | anew xss.txt
cat urls.txt | gf sqli | anew sqli.txt
```

## 九、信息收集测试清单

- [ ] Whois/注册人信息/历史Whois
- [ ] 子域名枚举（被动+主动爆破）
- [ ] 证书透明度日志
- [ ] DNS记录（A/AAAA/CNAME/MX/TXT/NS/SRV）
- [ ] DNS区域传送（AXFR）
- [ ] ASN/IP段归属
- [ ] Shodan/Censys/FOFA设备搜索
- [ ] Google Dorks敏感文件/页面
- [ ] GitHub/GitLab代码泄露
- [ ] Wayback Machine历史URL
- [ ] 端口扫描（TCP/UDP全端口）
- [ ] 服务版本识别
- [ ] Web指纹（CMS/框架/语言/WAF/CDN）
- [ ] 目录/敏感文件扫描
- [ ] JS文件分析（API/密钥/路由）
- [ ] Source Map源码还原
- [ ] SSL/TLS证书信息
- [ ] 云存储Bucket（S3/Blob/GCS）
- [ ] 邮件/员工信息收集
- [ ] 历史数据泄露查询
- [ ] 真实IP（绕过CDN）
- [ ] 错误页面/调试信息
- [ ] 401/403认证页面
- [ ] 邮箱账号泄露检查
- [ ] 移动应用API（反编译APK/IPA）
- [ ] GitHub/GitLab Dorks全面搜索
- [ ] Swagger/API文档
- [ ] 后台管理入口
- [ ] 默认凭证/默认页面
- [ ] Sitemap/robots.txt

## 十、注意事项

- **被动优先**：先OSINT被动收集，后主动扫描
- **速率控制**：端口扫描/目录fuzz控制速率，避免触发WAF封禁
- **授权范围**：确认授权测试的IP/域名范围，避免越界
- **法律合规**：Whois/Shodan等公开数据合法，但主动扫描需授权
- **数据保护**：收集的信息保密，不泄露用户数据
- **记录留痕**：所有发现记录在案，便于后续验证和报告
- **CDN注意**：确认目标是否使用CDN，扫描CDN IP无意义
- **WAF调整**：如遇WAF，降低扫描速率或调整策略
- **合规要求**：遵守《网络安全法》，仅在授权范围内测试
