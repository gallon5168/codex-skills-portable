---
name: src-recon-collection
description: SRC漏洞挖掘全流程自动化技能——覆盖子域名收集、端口扫描、指纹识别、JS分析、目录爆破、漏洞扫描、弱口令爆破的完整攻击面映射。集成Komo、JSFScan、Reconator、Secbuild等13个GitHub顶级工具的精华方法论。触发词：SRC挖洞、众测、打点、信息收集、资产收集、子域名、recon、bug bounty、渗透测试。
metadata:
  short-description: SRC全流程信息收集与漏洞扫描
  tools: subfinder,httpx,naabu,nuclei,gau,ffuf,dirsearch,katana,waybackurls,afrog,vulmap
  categories: recon,vulnerability-scanning,automation,src,bug-bounty
version: "1.0"
author: CyberStrikeAI
---

# SRC 综合信息收集与漏洞扫描

SRC 漏洞挖掘全流程自动化技能。覆盖从子域名收集、端口扫描、指纹识别、JS分析、目录爆破到漏洞扫描的完整攻击面映射。

## 工具目录

```
$SKILL_DIR/../../tmp/workspace/conversations/453646fc-df12-4e36-8985-88c2c55c2c6c/src_tools/
├── Komo/           # 综合扫描引擎
├── JSFScan/        # JS深度分析
├── FrameVul/       # 框架nday POC索引
├── Secbuild/       # 100+工具一键安装
├── Reconator/      # Docker自动化侦察
├── Discord-Recon/  # Discord远程侦察
├── Beginner-BB/    # 初学者自动化脚本
├── bugradar/       # 外部自动化
├── talosplus/      # Go智能自动化
├── LangSrcCurise/  # 资产监控
├── recon-checklist/# 侦察清单
└── thinkphp-POC/   # ThinkPHP RCE POC
```

## 阶段一：子域名收集

```bash
# 被动枚举
subfinder -d TARGET.com -all -silent | tee subs_subfinder.txt
curl -s "https://crt.sh/?q=%25.TARGET.com&output=json" | jq -r '.[].name_value' | sed 's/\*\.//g' | sort -u > subs_crtsh.txt
amass enum -passive -d TARGET.com -o subs_amass.txt

# 合并去重
cat subs_*.txt | sort -u > all_subs.txt

# 存活验证 + 指纹
cat all_subs.txt | httpx -silent -status-code -title -tech-detect -o alive.txt

# 筛选高价值
cat alive.txt | grep -E '\[200\]|\[403\]|\[401\]' > interesting.txt
```

## 阶段二：端口扫描

```bash
# 快速端口扫描
cat all_subs.txt | naabu -silent -top-ports 1000 -o ports.txt

# Web服务发现
cat all_subs.txt | httpx -silent -ports 80,443,8080,8443,8000,9090,3000,5000,7001 -o web_services.txt
```

## 阶段三：URL 与 JS 收集

```bash
# 历史URL
echo "TARGET.com" | gau --subs | tee urls_gau.txt
cat all_subs.txt | waybackurls | tee urls_wayback.txt

# 合并+去重+过滤
cat urls_*.txt | sort -u | uro > all_urls.txt

# 参数URL(注入点)
cat all_urls.txt | grep -E '\?.*=' | sort -u > params.txt

# JS文件收集
cat alive.txt | awk '{print $1}' | while read url; do
  curl -sk "$url" | grep -oP '(?:src|href)="([^"]*\.js)"' | sed "s|^|${url%/*}/|" >> js_files.txt
done
```

## 阶段四：目录爆破

```bash
cat alive.txt | awk '{print $1}' | while read u; do
  ffuf -u "$u/FUZZ" -w /usr/share/wordlists/dirb/common.txt -mc 200,301,302,403 -of csv -o "ffuf_$(echo $u | md5sum | cut -c1-8).csv"
done
```

## 阶段五：漏洞扫描

```bash
# Nuclei 官方模板
nuclei -l alive.txt -severity critical,high,medium -o nuclei_results.txt

# WordPress模板 (76,781个)
nuclei -l alive.txt -t nuclei-wordfence-cve/nuclei-templates/ -severity critical,high -o wp_results.txt

# POC批量验证
afrog -T alive.txt -o afrog_results.html
```

## 阶段六：弱口令

```bash
# Web弱口令
cat alive.txt | while read url; do
  title=$(echo "$url" | httpx -title -silent | awk -F'[' '{print $2}')
  case "$title" in
    *tomcat*)   hydra -L users.txt -P pass.txt "$url" http-get ;;
    *jenkins*)  hydra -L users.txt -P pass.txt "$url" http-post-form ;;
    *login*|*Login*|*后台*) hydra -L users.txt -P pass.txt "$url" http-post-form "/login:username=^USER^&password=^PASS^:F=error" ;;
  esac
done
```

## 阶段七：Komo 全自动扫描

```bash
# 一键安装依赖
python3 Komo/Komo.py install

# 全流程扫描
python3 Komo/Komo.py -d TARGET.com

# Komo扫描链:
# 子域→邮箱→存活→指纹→DNS反查→端口→爬虫→POC→弱口令
```

## 阶段八：JSFScan JS 分析

```bash
# 全量分析
bash JSFScan/JSFScan.sh -l alive.txt --all -r

# 分步执行:
# -l 收集JS链接  -e 提取端点  -s 查找密钥
# -m 本地下载    -w 提取字典  -d DOM XSS  -r HTML报告
```

## 阶段九：Secbuild 环境一键搭建

```bash
sudo bash Secbuild/secbuild.sh --profile recon   # 侦察工具
sudo bash Secbuild/secbuild.sh --profile web     # Web工具
sudo bash Secbuild/secbuild.sh --profile full    # 全部100+工具
```

## 进程检查清单

订阅以下侦察清单作为检查点（参考 recon-checklist/README.md）:

```
被动:  crt.sh | SecurityTrails | Shodan | GitHub Dork | Wayback Machine
主动:  子域爆破 | 端口扫描 | HTTP指纹 | JS分析 | 目录爆破 | 参数发现
      子域接管 | CORS检查 | SSL分析
漏洞:  Nuclei | afrog | vulmap | OA专项 | 弱口令
```

## 常见 OA/框架指纹速查

| 产品 | 特征 | POC来源 |
|------|------|---------|
| 泛微OA | `/wui/index.html` `/e-cology/` | FrameVul README |
| 用友NC | `/uapws/` `/yyoa/` | supplier repo |
| 通达OA | `/ispirit/login.php` | MYExploit |
| 万户OA | `/defaultroot/` | vulnerability-list |
| 致远OA | `/seeyon/` | FrameVul README |
| ThinkPHP | `/index.php?s=` + 报错特征 | thinkphp-POC/repo |
| 海康摄像头 | `/ISAPI/` + 默认路由 | CameraHack |
| 1Panel | `/api/v1/` | peiqi.wgpsec.org |

## 输出规范

所有扫描结果统一输出到 `results/TARGET_TIMESTAMP/`:
```
results/example.com_20260101/
├── 01_subdomains.txt
├── 02_alive.txt
├── 03_ports.txt
├── 04_urls.txt
├── 05_params.txt
├── 06_js_files.txt
├── 07_dirs.txt
├── 08_nuclei_results.txt
├── 09_weak_passwords.txt
└── report.html
```
