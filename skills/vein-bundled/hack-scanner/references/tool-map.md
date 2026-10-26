# Hack Scanner MCP 工具地图

MCP server 位于 hack_scanner/mcp_server.py，使用 stdio，启动命令为 python mcp_server.py。工具返回 JSON 字符串；缺少可选依赖时通常返回 ok: false 与错误信息。

## 核心

- url_scan(url, depth="standard", output_dir=".")：URL 黑盒扫描，生成 report.html/report.json。
- file_analyze(path)：文件或目录 SAST、密钥和配置分析。

## Web/API 检测

waf_detect、sql_exploit、web_fuzz、crlf_detect、jwt_analyze、graphql_security、http_param_pollution、oob_blind_scan、subdomain_takeover_check、deepsec_scan、waf_bypass。

## Swarm、证据与报告

swarm_classify、swarm_orchestrate、swarm_prompt_builder、swarm_report、swarm_bounty_estimate、findings_dedup、evidence_collector、quality_gate、roi_calculator、recon_parser、payload_engine、vuln_patterns_check。

## 侦察、网络与资产

osint_recon_tool、ssl_deep_scan_tool、network_scan_tool、dns_recon_tool、domain_typosquat、cert_monitor、domain_util、deep_crawler、zero_discovery_scan、cloud_bucket_enhanced。

## 文件、代码与依赖

file_meta_tool、webshell_detect、git_secret_scan、cve_lookup_tool、semgrep_scan_tool、trufflehog_scan_tool、checkov_scan_tool、trivy_scan_tool、exiftool_extract_tool。

## 外部 wrapper

zap_scan_tool、nuclei_scan_tool、gobuster_tool、hydra_scan_tool、google_dork_tool、nikto_scan_tool、dirb_scan_tool、john_crack_tool、ffuf_scan_tool、feroxbuster_scan_tool、dirsearch_scan_tool、wpscan_scan_tool、amass_enum_tool、hakrawler_crawl_tool、hashcat_crack_tool、theharvester_recon_tool、sherlock_enum_tool。调用前检查 CLI 是否在 PATH 或 config.json 的 tools 路径中。

## 认证与运行控制

auth_session_check、sso_probe、login_sequence_recorder、continuous_scan_manager、cert_factory、mitm_proxy_start、waf_rules_export、scan_profiles、playbook_execute、swarm_train_classifier。

## 常见工作流

URL/API：url_scan → 针对技术栈调用 waf_detect、graphql_security、jwt_analyze、ssl_deep_scan_tool → findings_dedup/quality_gate → swarm_report 或 export_reports。

源码/目录：file_analyze → deepsec_scan、git_secret_scan、semgrep_scan_tool/trivy_scan_tool → 去重、分级和报告。

仅处理已有结果：直接使用 recon_parser、findings_dedup、quality_gate、swarm_report，并标记未重新验证。
