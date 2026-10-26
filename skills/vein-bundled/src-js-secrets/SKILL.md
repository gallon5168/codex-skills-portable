---
name: src-js-secrets
description: JS文件深度分析与密钥提取技能。覆盖JS链接收集、端点提取、Secret发现(API keys/tokens/passwords)、变量名提取(潜在XSS参数)、DOM XSS扫描、Wordlist生成。基于JSFScan.sh方法论。触发词：JS分析、JavaScript侦察、密钥提取、API泄露、secret hunting、js recon、XSS参数、前端挖洞。
metadata:
  short-description: JS文件深度分析与密钥提取
  tools: JSFScan.sh,hakrawler,gospider,curl,linkfinder,secretfinder,nuclei
  categories: js-analysis,secret-hunting,xss,recon,src
version: "1.0"
author: CyberStrikeAI
---

# JS 文件深度分析与密钥提取

基于 JSFScan.sh 方法论，对目标网站的 JavaScript 文件进行全方位分析：收集→提取端点→发现密钥→变量分析→DOM XSS→报告。

## 工具路径

```bash
JSFSCAN_DIR="$SKILL_DIR/../../tmp/workspace/conversations/453646fc-df12-4e36-8985-88c2c55c2c6c/src_tools/JSFScan"
```

## 第一步：收集 JS 文件链接

```bash
# 方法1: 从存活URL爬取JS
cat alive.txt | while read url; do
  curl -sk "$url" 2>/dev/null | grep -oP '(?:src|href)=["'\'']([^"'\'' ]*\.js(?:[?#][^"'\'' ]*)?)["'\'' ]' | \
    sed -E 's/(?:src|href)=["'\'']//' | sed 's/["'\'' ].*//' | \
    awk -v base="$url" '{if($0~"^https?://")print$0; else if($0~"^//")print"https:"$0; else if($0~"^/")print base$0; else print base"/"$0}' >> js_links.txt
done

# 方法2: 用 hakrawler 直接爬取
cat alive.txt | hakrawler -js -depth 3 -plain | grep '\.js' | sort -u >> js_links.txt

# 方法3: 用 JSFScan.sh
bash $JSFSCAN_DIR/JSFScan.sh -l alive.txt
```

## 第二步：下载 JS 文件本地分析

```bash
mkdir -p js_files && cd js_files
cat ../js_links.txt | sort -u | while read jurl; do
  fname=$(echo "$jurl" | md5sum | cut -c1-8).js
  curl -skL --max-time 10 "$jurl" -o "$fname" 2>/dev/null
done
echo "下载完成: $(ls *.js 2>/dev/null | wc -l) 个文件"
```

## 第三步：端点提取

```bash
# 提取相对路径端点
cat js_files/*.js | grep -oP '["'\''`](/[\w\.\-/]+)["'\''`]' | \
  sed -E 's/["'\''`]//g' | sort -u > endpoints.txt

# 提取完整URL
cat js_files/*.js | grep -oP 'https?://[^\s"'\''`<>]+' | sort -u > full_urls.txt

# 提取 API 路径
cat endpoints.txt | grep -iE '(api|v[0-9]+|graphql|rest|ws|auth|login|admin|upload|download|export)' > api_endpoints.txt
```

## 第四步：密钥发现（核心）

```bash
# 通用正则模式匹配
cat js_files/*.js | grep -oP '(?i)(api[_-]?key|api[_-]?secret|access[_-]?token|auth[_-]?token|bearer|jwt|secret[_-]?key|private[_-]?key|client[_-]?secret|app[_-]?secret|session[_-]?token|csrf[_-]?token|nonce|signature|password|credential)["'\''\s:=]+([a-zA-Z0-9._\-+/=]{8,})' | sort -u > secrets_pattern.txt

# AWS 密钥
cat js_files/*.js | grep -oP 'AKIA[0-9A-Z]{16}' > secrets_aws.txt

# GCP 密钥  
cat js_files/*.js | grep -oP 'AIza[0-9A-Za-z\-_]{35}' > secrets_gcp.txt

# GitHub Token
cat js_files/*.js | grep -oP 'gh[pousr]_[A-Za-z0-9_]{36,}' > secrets_github.txt

# 通用 Token
cat js_files/*.js | grep -oP '(?:token|key|secret|password|credential)["'\''\s:=]+["'\'']?([a-zA-Z0-9._\-]{20,})["'\'']?' | \
  grep -viE '(function|string|object|undefined|null|true|false|window|document|console)' > secrets_tokens.txt

# Stripe/Slack/Heroku/Mailgun 等
cat js_files/*.js | grep -oP '(?:sk_live_|pk_live_|xox[bpras]\-[0-9a-zA-Z\-]+|rk_live_[0-9a-zA-Z]+|key\-[0-9a-zA-Z]+|MG_[0-9a-zA-Z]{20,})' > secrets_saas.txt
```

## 第五步：变量提取（XSS 参数发现）

```bash
# 提取 JS 变量名 → 可能对应 URL 参数
cat js_files/*.js | grep -oP '(?:var|let|const)\s+([a-zA-Z_$][a-zA-Z0-9_$]*)' | \
  awk '{print $NF}' | sort -u > js_variables.txt

# 提取 URL 参数引用
cat js_files/*.js | grep -oP '[?&]([a-zA-Z_][a-zA-Z0-9_]*)\s*=' | \
  sed 's/[?&]//' | sed 's/=//' | sort -u > js_params.txt

# 提取 location.search / URLSearchParams 引用
cat js_files/*.js | grep -oP '(?:location\.search|URLSearchParams|getParameter|getQueryString|\.query)\s*[\(\[][^\)\]]*' > xss_candidates.txt
```

## 第六步：DOM XSS 扫描

```bash
# 危险 sink 检测
for pattern in 'innerHTML' 'outerHTML' 'document\.write' 'eval\s*\(' 'setTimeout\s*\(' 'setInterval\s*\(' 'location\.href\s*=' 'location\.replace' 'location\.assign'; do
  echo "=== $pattern ===" >> dom_xss.txt
  grep -rn "$pattern" js_files/ >> dom_xss.txt
done

# jQuery 危险用法
grep -rn '\$(.*\.html\s*\(' js_files/ >> dom_xss.txt
grep -rn '\$(.*\.append\s*\(' js_files/ >> dom_xss.txt
grep -rn '\$(.*\.prepend\s*\(' js_files/ >> dom_xss.txt
```

## 第七步：Wordlist 生成

```bash
# 从JS中提取单词制作字典
cat js_files/*.js | grep -oP '[a-zA-Z][a-zA-Z0-9_]{2,20}' | \
  sort -u | awk 'length($0) >= 4' > js_wordlist.txt

# 高频路径词
cat endpoints.txt | grep -oP '/[a-zA-Z0-9_\-]+' | sort | uniq -c | sort -rn | head -200 > path_wordlist.txt
```

## 第八步：JSFScan.sh 一键全流程

```bash
bash $JSFSCAN_DIR/JSFScan.sh -l alive.txt --all -r
# 自动执行: 收集→端点提取→密钥发现→变量提取→DOM XSS→HTML报告
```

## 第九步：Nuclei JS 模板扫描

```bash
# 使用 Nuclei JS 相关模板
nuclei -l alive.txt -t ~/nuclei-templates/exposures/ -o js_exposure_results.txt
nuclei -l alive.txt -t ~/nuclei-templates/token-spray/ -o js_token_results.txt
```

## 常见密钥泄露模式速查

| 服务 | 正则模式 |
|------|---------|
| AWS Access Key | `AKIA[0-9A-Z]{16}` |
| AWS Secret Key | `[0-9a-zA-Z/+]{40}` |
| GCP API Key | `AIza[0-9A-Za-z\-_]{35}` |
| GitHub Token | `gh[pousr]_[A-Za-z0-9_]{36,}` |
| Slack Token | `xox[bpras]\-[0-9a-zA-Z\-]+` |
| Stripe Live Key | `sk_live_[0-9a-zA-Z]+` |
| Stripe Publishable | `pk_live_[0-9a-zA-Z]+` |
| Heroku API Key | `[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}` |
| Mailgun Key | `key-[0-9a-zA-Z]+` |
| JWT Token | `eyJ[A-Za-z0-9\-_]+\.eyJ[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_]+` |
| 阿里云 AccessKey | `LTAI[0-9A-Za-z]{16,20}` |
| 腾讯云 SecretId | `AKID[0-9A-Za-z]{32}` |
| 百度云 AK | `ak-[0-9a-z]{32}` |

## 输出目录

```
results/js_analysis/
├── js_links.txt        # 所有JS链接
├── js_files/           # 本地下载的JS文件
├── endpoints.txt       # 提取的端点
├── api_endpoints.txt   # API端点
├── secrets_all.txt     # 所有发现的密钥
├── secrets_aws.txt     # AWS密钥
├── secrets_github.txt  # GitHub Token
├── secrets_tokens.txt  # 通用Token
├── js_variables.txt    # JS变量名
├── js_params.txt       # URL参数名
├── dom_xss.txt         # DOM XSS候选点
├── js_wordlist.txt     # 提取的单词字典
└── jsfscan_report.html # JSFScan HTML报告
```
