# 依赖与降级

## 核心 Python

hack_scanner/requirements.txt 包含 requests、urllib3、beautifulsoup4、lxml、pyyaml、jinja2、dnspython、tldextract、cryptography、certifi、mcp、nltk。

安装：python -m pip install -r hack_scanner/requirements.txt

## 可选依赖

WAF/OSINT/TLS/元数据：wafw00f、shodan、sslyze、exifread、whois、rapidfuzz、zaproxy。浏览器：selenium、playwright、nest_asyncio、webdriver-manager；需要时运行 playwright install。报告、云与增强：pdfkit、weasyprint、boto3、bcrypt、gevent、aiohttp、mitmproxy、psutil、semgrep、checkov、sherlock-project 等。

## 外部 CLI

Nmap、Nuclei、Gobuster、Hydra、SQLMap、Nikto、Dirb、John、ffuf、feroxbuster、dirsearch、WPScan、Amass、Hakrawler、Hashcat、ExifTool、TruffleHog、Trivy、theHarvester、Sherlock。

缺少 CLI 时不要伪造成功：记录不可用，继续内置扫描，并在报告未覆盖项中说明。Windows 安装提示参考 hack_scanner/install_tools.bat，执行安装前先确认。

## 注意

config.json 默认 confirm_external_scan=true、限速开启、危险模式关闭。Python 3.13 上 checkov 可能因 rustworkx 无 wheel 安装失败，应视为可选依赖。MCP 启动失败时检查 mcp 包、工作目录和导入错误；CLI 仍可通过 hack_scanner.py 运行。
