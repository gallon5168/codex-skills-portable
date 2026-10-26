# 本機 Codex Skills 整理報告

> 產生時間：2026-10-27T02:46:14+08:00

## 摘要

- 實體 `SKILL.md` 定義：**2,180**
- 去重後 Skill 名稱：**1,682**
- 唯一內容雜湊：**1,907**
- 完全相同內容的重複群組：**220**
- 同名但內容不同的群組：**218**
- 命中 prompt 覆寫／越權指令特徵：**205 個名稱**（209 份定義）

## 掃描範圍與去重方式

- **Vein 套件庫**：`%USERPROFILE%\.codex\skills\.vein-bundled` — 2,079 份
- **Codex 系統**：`%USERPROFILE%\.codex\skills\.system` — 5 份
- **Codex Home**：`%USERPROFILE%\AppData\Local\OpenAI\Codex-Second\home\skills` — 53 份
- **外掛快取**：`%USERPROFILE%\AppData\Local\OpenAI\Codex-Second\home\plugins\cache` — 43 份

`.agents\skills` 與 `.codex\skills` 根目錄下的 `niuzi-*` 多數是指向 `.vein-bundled` 的 Junction；本報告以實際來源目錄計數，避免把同一檔案重複算兩次。專案工作區中的備份、舊輸出、虛擬環境與 `node_modules` 未納入「目前安裝」統計。

## 類別統計（以去重名稱計）

| 類別 | 數量 |
|---|---:|
| 系統／Skill 管理 | 9 |
| 文件／試算表／簡報／PDF | 97 |
| 商務範本／專案管理 | 5 |
| 網站／前端／UI／UX／設計 | 23 |
| AI／LLM／代理工作流 | 84 |
| 軟體開發／測試／架構 | 38 |
| DevOps／雲端／容器 | 64 |
| 資料／資料庫／分析 | 27 |
| 資安—Web／API | 220 |
| 資安—逆向／惡意程式／漏洞利用 | 230 |
| 資安—Windows／AD／身分 | 56 |
| 資安—網路／無線／協定 | 150 |
| 資安—雲端／供應鏈 | 43 |
| 資安—鑑識／事件應變／威脅情報 | 102 |
| 資安—治理／稽核／合規 | 47 |
| 資安—行動裝置／硬體／IoT | 22 |
| 資安—通用攻防／CTF | 341 |
| 寫作／內容／研究 | 8 |
| 生產力／協作／自動化 | 4 |
| 其他 | 112 |

## 資料品質與維護重點

- Frontmatter 完整：**2,170** 份；缺少或不完整：**10** 份。
- `prompt_override_flag` 只標示明確字串特徵（例如要求忽略安全／上層指令），不是內容風險的最終判定；可在 CSV 篩選 `TRUE` 後人工複核。
- `same_name_content_variants > 1` 代表同名 Skill 有多個不同內容版本，更新時最容易產生載入歧義。
- Junction 是目前安裝結構的一部分，不應把它當成一般重複資料夾直接刪除。

### 同名、多內容版本（前 50 組）

| Skill 名稱 | 定義數 | 內容版本數 | 來源 |
|---|---:|---:|---|
| code-audit | 5 | 3 | Codex Home, Vein 套件庫 |
| ida-reverse | 4 | 3 | Codex Home, Vein 套件庫 |
| reverse-engineering | 4 | 3 | Codex Home, Vein 套件庫 |
| src-hunter | 4 | 3 | Codex Home, Vein 套件庫 |
| anti-reversing-techniques | 3 | 3 | Vein 套件庫 |
| clickjacking | 3 | 3 | Vein 套件庫 |
| crlf-injection | 3 | 3 | Vein 套件庫 |
| api-security | 4 | 2 | Codex Home, Vein 套件庫 |
| apk-reverse | 4 | 2 | Codex Home, Vein 套件庫 |
| attack-chain | 4 | 2 | Codex Home, Vein 套件庫 |
| binary-diff | 4 | 2 | Codex Home, Vein 套件庫 |
| browser-automation | 4 | 2 | Codex Home, Vein 套件庫 |
| browser-extension-reverse | 4 | 2 | Codex Home, Vein 套件庫 |
| cloud-k8s | 4 | 2 | Codex Home, Vein 套件庫 |
| database-security | 4 | 2 | Codex Home, Vein 套件庫 |
| diagram-generator | 4 | 2 | Codex Home, Vein 套件庫 |
| digital-forensics | 4 | 2 | Codex Home, Vein 套件庫 |
| docs-generator | 4 | 2 | Codex Home, Vein 套件庫 |
| dotnet-reverse | 4 | 2 | Codex Home, Vein 套件庫 |
| edr-bypass-re | 4 | 2 | Codex Home, Vein 套件庫 |
| email-security | 4 | 2 | Codex Home, Vein 套件庫 |
| firmware-pentest | 4 | 2 | Codex Home, Vein 套件庫 |
| ghidra-reverse | 4 | 2 | Codex Home, Vein 套件庫 |
| go-rust-reverse | 4 | 2 | Codex Home, Vein 套件庫 |
| hardware-security | 4 | 2 | Codex Home, Vein 套件庫 |
| identity-federation | 4 | 2 | Codex Home, Vein 套件庫 |
| js-reverse | 4 | 2 | Codex Home, Vein 套件庫 |
| llm-security | 4 | 2 | Codex Home, Vein 套件庫 |
| macos-reverse | 4 | 2 | Codex Home, Vein 套件庫 |
| malware-analysis | 4 | 2 | Codex Home, Vein 套件庫 |
| mobile-reverse | 4 | 2 | Codex Home, Vein 套件庫 |
| ot-ics | 4 | 2 | Codex Home, Vein 套件庫 |
| patch-diff-exploit | 4 | 2 | Codex Home, Vein 套件庫 |
| pentest-tools | 4 | 2 | Codex Home, Vein 套件庫 |
| protocol-reverse | 4 | 2 | Codex Home, Vein 套件庫 |
| pwn-chain | 4 | 2 | Codex Home, Vein 套件庫 |
| radare2 | 4 | 2 | Codex Home, Vein 套件庫 |
| radio-sdr | 4 | 2 | Codex Home, Vein 套件庫 |
| supply-chain-security | 4 | 2 | Codex Home, Vein 套件庫 |
| thick-client | 4 | 2 | Codex Home, Vein 套件庫 |
| threat-hunting | 4 | 2 | Codex Home, Vein 套件庫 |
| wifi-wireless | 4 | 2 | Codex Home, Vein 套件庫 |
| windows-ad | 4 | 2 | Codex Home, Vein 套件庫 |
| openai-docs | 3 | 2 | Codex Home, Codex 系統, Vein 套件庫 |
| reverse-skill-router | 3 | 2 | Codex Home, Vein 套件庫 |
| analyzing-android-malware-with-apktool | 2 | 2 | Vein 套件庫 |
| analyzing-apt-group-with-mitre-navigator | 2 | 2 | Vein 套件庫 |
| analyzing-cobalt-strike-beacon-configuration | 2 | 2 | Vein 套件庫 |
| analyzing-cobaltstrike-malleable-c2-profiles | 2 | 2 | Vein 套件庫 |
| analyzing-golang-malware-with-ghidra | 2 | 2 | Vein 套件庫 |

## 完整 Skill 索引（名稱去重）

每個名稱只列一次；`定義/版本` 分別表示實體定義數與不同內容數。完整路徑、SHA-256 與時間在 CSV／JSON。

### 系統／Skill 管理（9）

| Skill | 說明 | 定義/版本 | 旗標 |
|---|---|---:|---|
| `openai-docs` | Use for Codex models/pricing, scheduled tasks, skills, settings, setup, troubleshooting, customization, automations, and self-knowledge—including 'you,' 'your,' 'this ap… | 3/2 |  |
| `plugin-creator` | Create and scaffold plugin directories for Codex with a required `.codex-plugin/plugin.json`, optional plugin folders/files, valid manifest defaults, and personal-market… | 1/1 |  |
| `plugin-management` | Discover and suggest relevant plugins, inspect app permissions and dependencies, and manage plugin connections or removal. Use when the user asks about plugins or when a… | 1/1 |  |
| `review-agent` | Perform a read-only, defect-first review of a specified code change and return every actionable finding. Use when another agent delegates review of uncommitted changes,… | 3/1 |  |
| `skill-creator` | Create or update a Codex skill with appropriately scoped instructions and any needed supporting resources. | 3/1 |  |
| `skill-creator-pro` | Create and evolve production-ready skills with reusable scripts, references, and validation. Use for new skill creation, skill upgrades, and enforcing consistent metadat… | 1/1 |  |
| `skill-installer` | Install Codex skills into $CODEX_HOME/skills from a curated list or a GitHub repo path. Use when a user asks to list installable skills, install a curated skill, or inst… | 3/1 |  |
| `template-creator` | Create or update a reusable personal Codex artifact-template skill. Use when the user invokes $template-creator or asks in natural language to create a reusable template… | 1/1 |  |
| `write-a-skill` | Create new agent skills with proper structure, progressive disclosure, and bundled resources. Use when user wants to create, write, or build a new skill. | 1/1 |  |

### 文件／試算表／簡報／PDF（97）

| Skill | 說明 | 定義/版本 | 旗標 |
|---|---|---:|---|
| `ai-engineering-discipline` | This skill should be used when tasks require strict AI engineering discipline, evidence-based conclusions, modular planning, strong-opponent modeling, open-source toolin… | 1/1 |  |
| `ai-security-agent-mcp` | Agent/工作流/工具/MCP服务器/多Agent安全测试专家。覆盖工具枚举、Schema提取、权限映射、HTTP/Fetch SSRF、文件/数据库/Git/代码工具、工具输出注入、MCP传输安全、工具投毒、共享MCP租户隔离、多Agent身份/委托/任务完整性。含MCP攻击模式参考和最新安全工具（AgentAuditKit/Age… | 1/1 |  |
| `analyzing-macro-malware-in-office-documents` | Analyzes malicious VBA macros embedded in Microsoft Office documents (Word, Excel, PowerPoint) to identify download cradles, payload execution, persistence mechanisms, a… | 1/1 |  |
| `analyzing-malicious-pdf-with-peepdf` | Perform static analysis of malicious PDF documents using peepdf, pdfid, and pdf-parser to extract embedded JavaScript, shellcode, and suspicious objects. | 1/1 |  |
| `analyzing-pdf-malware-with-pdfid` | Analyzes malicious PDF files using PDFiD, pdf-parser, and peepdf to identify embedded JavaScript, shellcode, exploits, and suspicious objects without opening the documen… | 1/1 |  |
| `api-recon-and-docs` | API reconnaissance and documentation review playbook. Use when discovering endpoints, schemas, versions, OpenAPI specs, hidden docs, and surface area for API testing. | 2/2 |  |
| `archive-&-document-password` | Credential Breach Chain Phase 6/压缩包与文档密码. 触发词: 压缩包与文档密码。 | 1/1 | 覆寫特徵 |
| `artifact-template-analytics-dashboard` | Create a spreadsheet using the Analytics Dashboard template and its retained reference file. Use when the user selects or names Analytics Dashboard. Monitor acquisition,… | 1/1 |  |
| `artifact-template-design-report` | Create a document using the Design Report template and its retained reference file. Use when the user selects or names Design Report. Produce design reports with an exec… | 1/1 |  |
| `artifact-template-experiment-analysis` | Create a document using the Experiment Analysis template and its retained reference file. Use when the user selects or names Experiment Analysis. Analyze experiments wit… | 1/1 |  |
| `artifact-template-financial-budget` | Create a spreadsheet using the Financial Budget template and its retained reference file. Use when the user selects or names Financial Budget. Model actuals, budget and… | 1/1 |  |
| `artifact-template-investment-committee-memo` | Create a document using the Investment Committee Memo template and its retained reference file. Use when the user selects or names Investment Committee Memo. Prepare inv… | 1/1 |  |
| `artifact-template-legal-memorandum` | Create a document using the Legal Memorandum template and its retained reference file. Use when the user selects or names Legal Memorandum. Draft legal memoranda with th… | 1/1 |  |
| `artifact-template-minimal-letterhead` | Create a document using the Minimal Letterhead template and its retained reference file. Use when the user selects or names Minimal Letterhead. Write professional busine… | 1/1 |  |
| `artifact-template-operating-calendar` | Create a spreadsheet using the Operating Calendar template and its retained reference file. Use when the user selects or names Operating Calendar. Plan annual and monthl… | 1/1 |  |
| `artifact-template-project-tracker` | Create a spreadsheet using the Project Tracker template and its retained reference file. Use when the user selects or names Project Tracker. Manage workstreams, tasks, o… | 1/1 |  |
| `artifact-template-sales-pipeline` | Create a spreadsheet using the Sales Pipeline template and its retained reference file. Use when the user selects or names Sales Pipeline. Track opportunities, stages, o… | 1/1 |  |
| `artifact-template-simple-dark-mode` | Create a presentation using the Simple Dark Mode template and its retained reference file. Use when the user selects or names Simple Dark Mode. Create clean dark-mode pr… | 1/1 |  |
| `artifact-template-simple-light-mode` | Create a presentation using the Simple Light Mode template and its retained reference file. Use when the user selects or names Simple Light Mode. Create clean light-mode… | 1/1 |  |
| `artifact-template-strategy-memorandum` | Create a document using the Strategy Memorandum template and its retained reference file. Use when the user selects or names Strategy Memorandum. Present strategic conte… | 1/1 |  |
| `artifact-template-system-design` | Create a document using the System Design template and its retained reference file. Use when the user selects or names System Design. Document system architecture, requi… | 1/1 |  |
| `artifact-template-three-statement-forecast` | Create a spreadsheet using the Three-Statement Forecast template and its retained reference file. Use when the user selects or names Three-Statement Forecast. Build an i… | 1/1 |  |
| `building-incident-response-playbook` | Designs and documents structured incident response playbooks that define step-by-step procedures for specific incident types aligned with NIST SP 800-61r3 and SANS PICER… | 2/1 |  |
| `building-incident-timeline-with-timesketch` | Build collaborative forensic incident timelines using Timesketch to ingest, normalize, and analyze multi-source event data for attack chain reconstruction and investigat… | 1/1 |  |
| `building-threat-actor-profile-from-osint` | Build comprehensive threat actor profiles using open-source intelligence (OSINT) techniques to document adversary motivations, capabilities, infrastructure, and TTPs for… | 2/2 |  |
| `building-vulnerability-exception-tracking-system` | Build a vulnerability exception and risk acceptance tracking system with approval workflows, compensating controls documentation, and expiration management. | 1/1 |  |
| `c2-operation` | C2 框架操作手册 — 基于 Rshell C2 架构提炼的通用 C2 操作知识。涵盖认证鉴权、客户端管理、命令执行、文件操作、凭据抓取、浏览器密码提取、内存执行、SOCKS5代理、Web Delivery、植入端生成、交互式终端等完整后渗透操作链。当需要操作C2框架、管理植入端、执行后渗透任务时使用。 | 1/1 |  |
| `cavecrew` | Caveman 子 Agent 委派决策指南。告诉主线程何时启动 cavecrew-investigator (定位代码)、 cavecrew-builder (1-2 文件编辑) 或 cavecrew-reviewer (diff 审查)， 替代内联工作或使用普通 Explore。子 Agent 输出为 caveman 压缩格式， 注… | 1/1 |  |
| `caveman-compress` | 将自然语言文件（CLAUDE.md, README, 记忆文件等）批处理压缩为 caveman 格式， 节省输入 token。保留所有技术实质、代码、URL 和结构。压缩版覆写原文件， 可读备份保存为 FILE.original.md。 触发词："/caveman-compress <文件路径>"、"压缩记忆文件"、"compress… | 1/1 |  |
| `code-review` | Review the changes since a fixed point (commit, branch, tag, or merge-base) along two axes — Standards (does the code follow this repo's documented coding standards?) an… | 1/1 |  |
| `competition-stego-media` | Internal downstream skill for ctf-sandbox-orchestrator. CTF-sandbox workflow for image, audio, video, document, and container steganography. Use when the user asks to in… | 2/1 |  |
| `conducting-post-incident-lessons-learned` | Facilitate structured post-incident reviews to identify root causes, document what worked and failed, and produce actionable recommendations to improve future incident r… | 1/1 |  |
| `csm-endpoint-security-less-lolbins` | 文件less恶意软件与LOLBins检测 — 端点安全模块 \| Endpoint Security \| 难度★★★★★ \| PTES框架 | 1/1 |  |
| `csm-exploitation` | 文件包含利用 — 漏洞利用模块 \| Exploitation \| 难度★★★ \| PTES框架 | 1/1 |  |
| `csm-reporting-word-pdf` | Word/PDF安全报告模板 — 报告撰写模块 \| Reporting \| 难度★★★ \| PTES框架 | 1/1 |  |
| `csv-formula-injection` | CSV/spreadsheet formula injection (DDE, Excel/LibreOffice, Google Sheets IMPORT*). Use when exports, imports, or user fields feed spreadsheets or reporting tools. | 2/2 |  |
| `ctf-forensics` | Provides digital forensics and signal analysis techniques for CTF challenges. Use when analyzing disk images, memory dumps, event logs, network captures, cryptocurrency… | 1/1 |  |
| `ctf-writeup` | Generates a single standardized submission-style CTF writeup for competition handoff and organizer review. Use after solving a CTF challenge to document the solution ste… | 1/1 |  |
| `detecting-shadow-api-endpoints` | Discover and inventory shadow API endpoints that operate outside documented specifications using traffic analysis, code scanning, and API discovery platforms. | 1/1 |  |
| `disk-forensics` | 磁盘取证技术，包括Autopsy使用、文件系统分析、文件恢复和注册表分析 | 1/1 |  |
| `docs-generator` | Creates task-oriented technical documentation with progressive disclosure. Use when writing READMEs, API docs, architecture docs, or markdown documentation. Also use thi… | 4/2 |  |
| `docs-pipeline-automation` | Build repeatable data-to-Docs pipelines from Sheets and Drive sources. Use for automated status reports, template-based document assembly, and scheduled publishing workf… | 1/1 |  |
| `documentation-lookup` | Use up-to-date library and framework docs via Context7 MCP instead of training data. Activates for setup questions, API references, code examples, or when the user names… | 1/1 |  |
| `documents` | Create, edit, redline, and comment on `.docx`, Word, and Google Docs-targeted document artifacts inside the container, with a strict render-and-verify workflow. Use `ren… | 1/1 |  |
| `elf-file-analysis` | Reverse Engineering Chain Phase 2/ELF文件分析. 触发词: ELF文件分析。 | 1/1 | 覆寫特徵 |
| `evidence-first` | Use when 处理任何需要交付结论或产出物的非琐碎任务（调研、分析、排查问题、写方案、写文档、编码），尤其当任务带时间压力（"快点、直接给答案"）、信息来源可能互相矛盾、被要求汇报数字或事实、或产出要给他人做决策依据时。也用于用户想把这套工作方式移植到其他模型（取 portable 文件）。 | 1/1 |  |
| `excel-live-control` | Control an open or active Microsoft Excel workbook through the ChatGPT add-in or connected session. Use when the user tags the Microsoft Excel app in Codex or follows up… | 1/1 |  |
| `exploitdb-search` | Exploit-DB本地化搜索工具操作技能。47090条漏洞索引离线搜索，覆盖webapps/remote/local/dos/hardware全平台。支持关键词搜索、CVE搜索、EDB-ID精确查找，按需下载exploit文件。触发词：exploit-db、searchsploit、漏洞搜索、POC搜索、EXP搜索、CVE查询、漏洞利… | 1/1 |  |
| `file-agent` | 负责文件类漏洞检测：路径穿越/LFI/RFI/LFI→RCE、任意文件上传、文件包含、 任意文件下载、Zip Slip、SVG/CSV 注入、PHP Wrapper 利用、PEARCMD RCE、 编辑器路径利用、敏感文件泄露与文件解析链风险。 | 1/1 |  |
| `file-inclusion-lfi/rfi` | Web Attack Chain Phase 18/文件包含LFI-RFI. 触发词: 文件包含LFI-RFI。 | 1/1 | 覆寫特徵 |
| `file-upload-attack` | Web Attack Chain Phase 17/文件上传攻击. 触发词: 文件上传攻击。 | 1/1 | 覆寫特徵 |
| `file-upload-testing` | 文件上传漏洞深度测试专业技能：14种WAF绕过策略、分语言免杀WebShell、解析漏洞全场景、从黑名单绕过到RCE完整攻击链 | 1/1 |  |
| `frontend-slides` | Create stunning, animation-rich HTML presentations from scratch or by converting PowerPoint files. Use when the user wants to build a presentation, convert a PPT/PPTX to… | 1/1 |  |
| `google-docs` | Create and edit native Google Docs through connected tools. | 1/1 |  |
| `google-sheets` | Analyze and edit connected Google Sheets with range precision. Use when the user wants to create Google Sheets, find a spreadsheet, inspect tabs or ranges, search rows,… | 1/1 |  |
| `google-slides` | Route Google Slides authoring requests and derive a design system from a native template or reference deck. Use this skill when the user provides an existing native Goog… | 1/1 |  |
| `graphql-and-hidden-parameters` | GraphQL and hidden parameter testing playbook. Use when exploring introspection, batching, undocumented fields, hidden parameters, schema abuse, and GraphQL authorizatio… | 2/2 |  |
| `grill-with-docs` | Grilling session that challenges your plan against the existing domain model, sharpens terminology, and updates documentation (CONTEXT.md, ADRs) inline as decisions crys… | 1/1 |  |
| `handoff` | Compact the current conversation into a handoff document for another agent to pick up. | 2/2 |  |
| `ida-reverse` | IDA Pro 逆向分析辅助技能。当用户提到逆向、反编译、分析二进制/PE/ELF/APK/DLL/SO、破解、找密码、漏洞分析、病毒分析、firmware 固件分析，或需要分析 exe/dll/so/elf/macho/sys 等文件时，务必使用此技能。 Ensure to use this skill when the user w… | 4/3 |  |
| `implementing-deception-based-detection-with-canarytoken` | Deploy and monitor Canary Tokens via the Thinkst Canary API for deception-based breach detection using web bug tokens, DNS tokens, document tokens, and AWS key tokens. | 2/2 |  |
| `implementing-honeytokens-for-breach-detection` | Deploys canary tokens and honeytokens (fake AWS credentials, DNS canaries, document beacons, database records) that trigger alerts when accessed by attackers. Uses the C… | 1/1 |  |
| `implementing-ticketing-system-for-incidents` | Implements an integrated incident ticketing system connecting SIEM alerts to ServiceNow, Jira, or TheHive for structured incident tracking, SLA management, escalation wo… | 1/1 |  |
| `java-auth-audit` | Java Web 源码鉴权机制审计工具。从源码中识别所有鉴权实现，检测鉴权绕过漏洞和越权访问缺陷。适用于：(1) 识别鉴权框架和实现方式，(2) 发现鉴权绕过漏洞，(3) 检测越权访问缺陷，(4) 审计权限校验逻辑。支持 Shiro、Spring Security、JWT、Filter/Interceptor、自定义鉴权等。**支持反编… | 1/1 |  |
| `java-file-read-audit` | Java Web 源码任意文件读取漏洞审计工具。从源码中识别所有文件读取操作并检测路径遍历漏洞。适用于：(1) 识别文件读取框架和实现方式，(2) 发现任意文件读取漏洞，(3) 检测路径遍历漏洞，(4) 审计文件路径参数校验逻辑。支持 BufferedReader、Scanner、Files.lines/readAllLines/rea… | 1/1 |  |
| `java-file-upload-audit` | Java Web 源码文件上传漏洞审计工具。用于从源码中识别所有文件上传入口并检查上传路径、文件名处理与校验逻辑漏洞。适用于：(1) 识别 Servlet/Commons FileUpload 与 Spring Boot MultipartFile 上传实现，(2) 发现任意文件上传、路径穿越与可执行文件上传漏洞，(3) 检查文件名/目… | 1/1 |  |
| `java-route-tracer` | Java Web 源码路由多层级调用链追踪工具。根据用户指定的路由路径，追踪从 Controller/Action 到 DAO 层的完整调用链，输出每一层的文件位置、方法签名和可传入参数。适用于多种漏洞类型的参数流向追踪：(1) SQL注入 - 追踪参数到SQL拼接点，(2) 命令注入 - 追踪参数到Runtime.exec()，(3)… | 1/1 |  |
| `java-sql-audit` | Java Web 源码 SQL 注入漏洞审计工具。从源码中定位所有 SQL 执行入口并检测注入漏洞。适用于：(1) 识别 SQL 执行框架和实现方式，(2) 发现 SQL 注入漏洞，(3) 检查参数化查询使用情况，(4) 检测动态 SQL 拼接漏洞。支持 JDBC、MyBatis、Hibernate 三种主流框架。**支持反编译 .cl… | 1/1 |  |
| `java-vuln-scanner` | Java 组件版本漏洞检测工具。扫描 pom.xml、build.gradle 或 jar 文件中的第三方依赖，匹配已知漏洞规则（CVE）并生成漏洞检测报告。适用于：(1) Java 项目依赖安全审计，(2) 识别 Log4j、Fastjson、Shiro、Spring 等高危组件漏洞，(3) jar 包反编译后的依赖提取。支持按目录层… | 1/1 |  |
| `java-xxe-audit` | Java Web 源码 XXE (XML External Entity) 漏洞审计工具。从源码中识别所有 XML 解析操作并检测外部实体注入漏洞。适用于：(1) 识别 XML 解析器类型和实现方式，(2) 发现 XXE 注入漏洞，(3) 检查外部实体防护配置情况，(4) 审计 XML 输入来源与回显逻辑。支持 XMLReader、SA… | 1/1 |  |
| `pdf` | Read, create, inspect, render, and verify PDF files where visual layout matters, including fillable AcroForms. Use Poppler rendering plus Python tools such as reportlab,… | 1/1 |  |
| `pe-file-analysis` | Reverse Engineering Chain Phase 3/PE文件分析. 触发词: PE文件分析。 | 1/1 | 覆寫特徵 |
| `pentest-agent-os` | 渗透测试Agent操作系统。把渗透抽象成状态空间搜索:不预设固定路径,以项目黑板 Fact 图 (upsert_project_fact)+漏洞记录沉淀认知,路径从已验证事实上涌现。覆盖全杀伤链攻击手法 (联网情报/Web/认证/服务端/源码/社工/后渗透/二进制/内网域/云/区块链/AI/无线/硬件)+0day+ 组合拳+代理自举。核… | 1/1 |  |
| `performing-api-inventory-and-discovery` | Performs API inventory and discovery to identify all API endpoints in an organization's environment including documented, undocumented, shadow, zombie, and deprecated AP… | 2/2 |  |
| `performing-plc-firmware-security-analysis` | This skill covers analyzing Programmable Logic Controller (PLC) firmware for security vulnerabilities including hardcoded credentials, insecure update mechanisms, backdo… | 1/1 |  |
| `php-audit-pipeline` | PHP Web 全链路白盒代码安全审计流水线（多文件版编排）。作为总编排参考，按 Sink 类型调用各子审计 skill（`php-route-mapper/php-auth-audit/php-route-tracer/php-*-audit`），并复用统一输出与分级标准。 | 1/1 |  |
| `php-file-read-audit` | PHP Web 源码任意文件读取/路径穿越审计工具。识别文件读取 Sink，追踪路径来源与校验逻辑，输出可利用性分级、PoC 与修复建议（禁止省略）。 | 1/1 |  |
| `php-file-upload-audit` | PHP Web 源码文件上传审计工具。识别上传入口与保存路径、文件名处理与校验逻辑，检测任意文件上传/路径穿越/可执行上传风险，输出可利用性分级、PoC 与修复建议（禁止省略）。 | 1/1 |  |
| `php-file-write-audit` | PHP Web 源码任意文件写入审计工具。识别用户可控数据进入写入 Sink 的链路，追踪任意落点写入/路径穿越到 write，并评估写入后的可执行性（禁止省略）。 | 1/1 |  |
| `php-filesystem-audit` | PHP 文件系统操作审计工具。聚焦 mkdir/chmod/chown/unlink/rmdir/link/symlink/readlink/touch/权限与 TOCTOU 等操作的安全风险，为路径校验绕过与写入链利用提供“可利用性增强证据”（不替代 FILE/UPLOAD/WRITE 等 sink 子审计）。 | 1/1 |  |
| `php-nosql-audit` | PHP Web 源码 NoSQL 注入审计工具。识别用户输入进入 MongoDB/DocumentDB 查询构造，分析是否存在 operator 注入（$gt/$ne/$where 等），输出分级、PoC 与修复建议（禁止省略）。 | 1/1 |  |
| `Presentations` | Read, create or edit Spaces presentations, PowerPoint files, or Google Slides decks. Use for presentation, slide deck, PowerPoint, PPT, PPTX, or Google Slides requests. | 1/1 |  |
| `profiling-threat-actor-groups` | Develops comprehensive threat actor profiles for APT groups, criminal organizations, and hacktivist collectives by aggregating TTP documentation, historical campaign dat… | 1/1 |  |
| `protocol-reverse-engineering` | Comprehensive techniques for capturing, analyzing, and documenting network protocols for security research, interoperability, and debugging. | 1/1 |  |
| `reverse-flow` | Comprehensive reverse engineering workflow for binaries, firmware, mobile apps, scripts, document samples, protocol captures, memory dumps, and unknown artifacts. Covers… | 1/1 |  |
| `reverse-skill-router` | Routes reverse engineering, exploitation, penetration testing, malware, mobile, firmware, browser automation, documentation, and security tasks to the appropriate specia… | 3/2 |  |
| `security-bluebook-builder` | Build a minimal but real security policy for sensitive apps. The output is a single, coherent Blue Book document using MUST/SHOULD/CAN language, with explicit assumption… | 1/1 |  |
| `specialized-attack-playbooks` | 专题实战利用:GoEdge私钥导出,灰产CDN取证,ARP MITM,CDN→S3 STS链,宝塔+UniApp,AI IDE API反代,OCS+MinIO;含references/scripts支持文件索引。Use when applying specialized playbooks for GoEdge, CDN, ARP MI… | 1/1 |  |
| `Spreadsheets` | Use skill when user requests to create, modify, analyze, visualize, or work with spreadsheet files (`.xlsx`, `.xls`, `.csv`, `.tsv`) or Google Sheets with formulas, form… | 1/1 |  |
| `src-js-secrets` | JS文件深度分析与密钥提取技能。覆盖JS链接收集、端点提取、Secret发现(API keys/tokens/passwords)、变量名提取(潜在XSS参数)、DOM XSS扫描、Wordlist生成。基于JSFScan.sh方法论。触发词：JS分析、JavaScript侦察、密钥提取、API泄露、secret hunting、js… | 1/1 |  |
| `testing-api-for-mass-assignment-vulnerability` | Tests APIs for mass assignment (auto-binding) vulnerabilities where clients can modify object properties they should not have access to by including additional parameter… | 2/1 |  |
| `triaging-security-alerts-in-splunk` | Triages security alerts in Splunk Enterprise Security by classifying severity, investigating notable events, correlating related telemetry, and making escalation or clos… | 1/1 |  |
| `vuln-analysis-expert` | WooYun漏洞分析专家系统。基于88,636个真实漏洞案例提炼的元思考方法论、测试流程、利用技巧、绕过方法。覆盖SQL注入、XSS、命令执行、逻辑漏洞、文件上传、未授权访问等主要漏洞类型。当用户进行漏洞挖掘、渗透测试、安全审计、代码审计时触发。 | 1/1 |  |
| `writable-files-&-config` | Linux PrivEsc Chain Phase 8/可写文件与配置. 触发词: 可写文件与配置。 | 1/1 | 覆寫特徵 |
| `write-page` | Create or edit requested Page/Space content, or use for prose you have already decided to save as a standalone Markdown file, only if the user did not explicitly request… | 1/1 |  |
| `xslt-injection` | XSLT injection testing: processor fingerprinting, XXE and document() SSRF, EXSLT write primitives, PHP/Java/.NET extension RCE surfaces. Use when user-controlled XSLT/st… | 2/2 |  |
| `xxe-injection-testing` | XXE XML外部实体注入深度测试技能：全解析器攻击面、文件读取/SSRF/RCE/DoS利用链、编码绕过、OOB外带、Java/.NET/PHP特定利用 | 1/1 |  |

### 商務範本／專案管理（5）

| Skill | 說明 | 定義/版本 | 旗標 |
|---|---|---:|---|
| `artifact-template-business-review` | Create a presentation using the Business Review template and its retained reference file. Use when the user selects or names Business Review. Review business performance… | 1/1 |  |
| `artifact-template-market-trends-report` | Create a presentation using the Market Trends Report template and its retained reference file. Use when the user selects or names Market Trends Report. Communicate marke… | 1/1 |  |
| `artifact-template-operating-review` | Create a presentation using the Operating Review template and its retained reference file. Use when the user selects or names Operating Review. Run weekly operating revi… | 1/1 |  |
| `artifact-template-project-kickoff` | Create a presentation using the Project Kickoff template and its retained reference file. Use when the user selects or names Project Kickoff. Align teams on project goal… | 1/1 |  |
| `artifact-template-team-alignment` | Create a presentation using the Team Alignment template and its retained reference file. Use when the user selects or names Team Alignment. Facilitate team offsites and… | 1/1 |  |

### 網站／前端／UI／UX／設計（23）

| Skill | 說明 | 定義/版本 | 旗標 |
|---|---|---:|---|
| `attack-tree-construction` | Build comprehensive attack trees to visualize threat paths. Use when mapping attack scenarios, identifying defense gaps, or communicating security risks to stakeholders. | 1/1 |  |
| `competition-bundle-sourcemap-recovery` | Internal downstream skill for ctf-sandbox-orchestrator. CTF-sandbox workflow for source maps, build manifests, chunk registries, emitted bundles, obfuscated loader flow,… | 2/1 |  |
| `competition-web-runtime` | Internal downstream skill for ctf-sandbox-orchestrator. CTF-sandbox workflow for CTF web, API, SSR, frontend, queue-backed app, and routing challenges. Use when the user… | 2/1 |  |
| `css` | CSS3 styling language including Flexbox, Grid, animations, and responsive design | 1/1 |  |
| `ctf-web` | Provides web exploitation techniques for CTF challenges. Use when the target is primarily an HTTP application, API, browser client, template engine, identity flow, or sm… | 1/1 |  |
| `diagram-generator` | generate, refine, validate, and render diagrams from natural language, notes, code snippets, schemas, tables, or existing diagram source. use for flowcharts, swimlanes,… | 4/2 |  |
| `exploiting-excessive-data-exposure-in-api` | Tests APIs for excessive data exposure where endpoints return more data than the client application needs, relying on the frontend to filter sensitive fields. The tester… | 2/2 |  |
| `exploiting-http-request-smuggling` | Detecting and exploiting HTTP request smuggling vulnerabilities caused by Content-Length and Transfer-Encoding parsing discrepancies between front-end and back-end serve… | 2/1 |  |
| `frontend-mobile-security-xss-scan` | You are a frontend security specialist focusing on Cross-Site Scripting (XSS) vulnerability detection and prevention. Analyze React, Vue, Angular, and vanilla JavaScript… | 1/1 |  |
| `frontend-patterns` | Frontend development patterns for React, Next.js, state management, performance optimization, and UI best practices. | 1/1 |  |
| `frontend-security-coder` | Expert in secure frontend coding practices specializing in XSS prevention, output sanitization, and client-side security patterns. | 1/1 |  |
| `imagegen` | Generate or edit raster images when the task benefits from AI-created bitmap visuals such as photos, illustrations, textures, sprites, mockups, or transparent-background… | 3/1 |  |
| `implementing-microsegmentation-with-guardicore` | Implementing microsegmentation using Akamai Guardicore Segmentation to map application dependencies, create granular network policies, visualize east-west traffic flows,… | 1/1 |  |
| `performing-http-parameter-pollution-attack` | Execute HTTP Parameter Pollution attacks to bypass input validation, WAF rules, and security controls by injecting duplicate parameters that are processed differently by… | 2/2 |  |
| `sites` | Use Sites when the user wants a website built for them (including a landing page, portfolio, dashboard, portal, tracker, hub, game, event registration, or tool), request… | 1/1 |  |
| `sites-remix` | Remix a Site built with the Sites plugin into a new Site. Use when the user has identified the source Site and asks to remix it. | 1/1 |  |
| `ui-ux-pro-max` | UI/UX design intelligence for web, mobile, and desktop. This skill should be used when designing, building, reviewing, or fixing interfaces, including pages, components,… | 1/1 |  |
| `visualize` | Create visualizations and interactive tools directly in conversation. Proactively use to show how something works; explore 'what happens when', 'what changes', or 'help… | 1/1 |  |
| `web-frontend-designer` | Scaffold frontend architecture, components, routing, and UI dependencies from project config and wireframes. | 1/1 |  |
| `web-frontend-tester` | Run frontend functional, accessibility, visual, and performance test planning with structured reports. | 1/1 |  |
| `web-security-auditor` | Aggregate SAST, SCA, DAST, secrets, API, frontend, and backend security checks into one report. | 1/1 |  |
| `web-ux-architect` | Generate sitemap and wireframe specifications from project-config.json and produce UX planning artifacts. | 1/1 |  |
| `xss-&-front-end-attacks` | Web Attack Chain Phase 13/XSS与前端攻击. 触发词: XSS与前端攻击。 | 1/1 | 覆寫特徵 |

### AI／LLM／代理工作流（84）

| Skill | 說明 | 定義/版本 | 旗標 |
|---|---|---:|---|
| `agentic-mcp-server-builder` | Scaffold MCP server projects and baseline tool contract checks. Use for defining tool schemas, generating starter server layouts, and validating MCP-ready structure. | 1/1 |  |
| `agentic-workflow-automation` | Generate reusable multi-step agent workflow blueprints. Use for trigger/action orchestration, deterministic workflow definitions, and automation handoff artifacts. | 1/1 |  |
| `ai-engineering` | AI 工程技能套件 — 来自 Matt Pocock Skills for Real Engineers。涵盖 TDD 测试驱动开发、结构化诊断调试、代码架构优化、需求对齐访谈、原型构建、Issue 分诊、会话交接等核心工程能力。当需要系统化软件开发方法论、调试复杂Bug、改进代码架构、或创建新技能时使用。 | 1/1 |  |
| `ai-engineering-tdd` | Test-driven development. Use when the user wants to build features or fix bugs test-first, mentions "red-green-refactor", or wants integration tests. | 1/1 |  |
| `ai-engineering-triage` | Move issues and external PRs through a state machine of triage roles — categorise, verify, grill if needed, and write agent-ready briefs. | 1/1 |  |
| `ai-infogather` | AI 驱动的企业信息收集作战手册 — 基于国家电投黄河水电（SPIC）真实红队实战沉淀。13种作战模式覆盖 ICP 备案反查、工商信息、招标公告、GitHub 泄露、DNS 暴力枚举、子公司攻击面扩张、Quake/Fofa 网络测绘、OneForAll/Subfinder 异步子域名扫描。专为中国政企/能源/金融等行业渗透测试前期信息收… | 1/1 |  |
| `analyzing-cloud-storage-access-patterns` | Detect abnormal access patterns in AWS S3, GCS, and Azure Blob Storage by analyzing CloudTrail Data Events, GCS audit logs, and Azure Storage Analytics. Identifies after… | 1/1 |  |
| `article-writing` | Write articles, guides, blog posts, tutorials, newsletter issues, and other long-form content in a distinctive voice derived from supplied examples or brand guidance. Us… | 1/1 |  |
| `binary-diff` | 跨版本符号迁移与二进制差分。当你有旧版本的符号/逆向结果，需要快速迁移到新版本时使用。 适用场景：内核缺 PDB 用旧版符号推导、程序更新后批量迁移函数名、应用更新后快速定位新偏移。 核心方法：用 LLM 做结构化差异比对，程序化输入输出，成本极低（200 函数 ~1 元）。 触发关键词：符号迁移、bindiff、跨版本、PDB 缺失、… | 4/2 |  |
| `case-review` | Reviews a reverse-skill case package for scope readiness, Evidence to Finding to Path traceability, work item coverage, timeline references, and optional artifact hash i… | 3/1 |  |
| `caveman` | Ultra-compressed communication mode. Cuts token usage ~75% by dropping filler, articles, and pleasantries while keeping full technical accuracy. Use when user says "cave… | 1/1 |  |
| `claude-api` | Anthropic Claude API patterns for Python and TypeScript. Covers Messages API, streaming, tool use, vision, extended thinking, batches, prompt caching, and Claude Agent S… | 1/1 |  |
| `codebase-design` | Shared vocabulary for designing deep modules. Use when the user wants to design or improve a module's interface, find deepening opportunities, decide where a seam goes,… | 1/1 |  |
| `competition-ad-certificate-abuse` | Internal downstream skill for ctf-sandbox-orchestrator. CTF-sandbox workflow for AD CS, certificate templates, enrollment rights, EKUs, SAN controls, PKINIT, certificate… | 2/1 |  |
| `competition-agent-cloud` | Internal downstream skill for ctf-sandbox-orchestrator. CTF-sandbox workflow for AI-agent, prompt-injection, MCP or toolchain, cloud, container, CI/CD, and supply-chain… | 2/1 |  |
| `competition-browser-persistence` | Internal downstream skill for ctf-sandbox-orchestrator. CTF-sandbox workflow for browser cookies, localStorage, sessionStorage, IndexedDB, Cache Storage, service workers… | 2/1 |  |
| `competition-crypto-mobile` | Internal downstream skill for ctf-sandbox-orchestrator. CTF-sandbox workflow for crypto, encoding, steganography, APK, IPA, and mobile trust-boundary challenges. Use whe… | 2/1 |  |
| `competition-prompt-injection` | Internal downstream skill for ctf-sandbox-orchestrator. CTF-sandbox workflow for prompt-injection, retrieval poisoning, memory contamination, planner drift, MCP or tool-… | 2/1 |  |
| `competition-relay-coercion-chain` | Internal downstream skill for ctf-sandbox-orchestrator. CTF-sandbox workflow for forced-auth coercion, relay chains, target selection, NTLM or related acceptance paths,… | 2/1 |  |
| `computer-use` | Control Windows apps from ChatGPT | 1/1 |  |
| `conducting-mobile-application-penetration-test` | Perform a mobile application penetration test on Android and iOS apps to identify insecure data storage, certificate pinning bypass, API vulnerabilities, binary protecti… | 1/1 |  |
| `create-pet` | Create, repair, validate, preview, upload, or activate an animated v2 pet in ChatGPT Work mode from a character idea, brand cue, or reference image. Use for new ChatGPT… | 1/1 |  |
| `csm-ai-agent-vuln-scanning` | AI代理漏洞扫描 — 漏洞扫描模块 \| Vulnerability Scanning \| 难度★★★★ \| PTES框架 | 1/1 |  |
| `csm-code-audit-ai-agent` | AI Agent代码审计 — 代码审计模块 \| Code Audit \| 难度★★★★ \| PTES框架 | 1/1 |  |
| `ctf-sandbox-orchestrator` | Default entrypoint and master ctf-sandbox-orchestrator workflow for CTF, exploit, reverse engineering, DFIR, pwnable, crypto, stego, mobile, AI-agent, cloud, container,… | 2/1 |  |
| `cti-expert` | CTI Expert — cyber threat intelligence and OSINT analysis toolkit. Activates on: OSINT, CTI, threat intelligence, digital footprint, social media investigation, username… | 1/1 |  |
| `deploying-cloudflare-access-for-zero-trust` | Deploying Cloudflare Access with Cloudflare Tunnel to provide zero trust access to self-hosted and private applications, configuring identity-aware access policies, devi… | 1/1 |  |
| `deploying-edr-agent-with-crowdstrike` | Deploys and configures CrowdStrike Falcon EDR agents across enterprise endpoints to enable real-time threat detection, behavioral analysis, and automated response. Use w… | 1/1 |  |
| `detecting-anomalies-in-industrial-control-systems` | This skill covers deploying anomaly detection systems for industrial control environments using machine learning models trained on OT network baselines, physics-based pr… | 1/1 |  |
| `detecting-anomalous-authentication-patterns` | Detects anomalous authentication patterns using UEBA analytics, statistical baselines, and machine learning models to identify impossible travel, credential stuffing, br… | 1/1 |  |
| `detecting-azure-storage-account-misconfigurations` | Audit Azure Blob and ADLS storage accounts for public access exposure, weak or long-lived SAS tokens, missing encryption at rest, disabled HTTPS-only traffic, and outdat… | 1/1 |  |
| `detecting-dnp3-protocol-anomalies` | Detect anomalies in DNP3 (Distributed Network Protocol 3) communications used in SCADA systems by monitoring for unauthorized control commands, firmware update attempts,… | 1/1 |  |
| `detecting-misconfigured-azure-storage` | Detecting misconfigured Azure Storage accounts including publicly accessible blob containers, missing encryption settings, overly permissive SAS tokens, disabled logging… | 1/1 |  |
| `detecting-modbus-protocol-anomalies` | This skill covers detecting anomalies in Modbus/TCP and Modbus RTU communications in industrial control systems. It addresses function code monitoring, register range va… | 1/1 |  |
| `diagnose` | Disciplined diagnosis loop for hard bugs and performance regressions. Reproduce → minimise → hypothesise → instrument → fix → regression-test. Use when user says "diagno… | 1/1 |  |
| `diagnosing-bugs` | Diagnosis loop for hard bugs and performance regressions. Use when the user says "diagnose"/"debug this", or reports something broken/throwing/failing/slow. | 1/1 |  |
| `dmux-workflows` | Multi-agent orchestration using dmux (tmux pane manager for AI agents). Patterns for parallel agent workflows across Claude Code, Codex, OpenCode, and other harnesses. U… | 1/1 |  |
| `domain-modeling` | Build and sharpen a project's domain model. Use when the user wants to pin down domain terminology or a ubiquitous language, record an architectural decision, or when an… | 1/1 |  |
| `emblemai-crypto-wallet` | Crypto wallet management across 7 blockchains via EmblemAI Agent Hustle API. Balance checks, token swaps, portfolio analysis, and transaction execution for Solana, Ether… | 1/1 |  |
| `exa-search` | Neural search via Exa MCP for web, code, and company research. Use when the user needs web search, code examples, company intel, people lookup, or AI-powered deep resear… | 1/1 |  |
| `fal-ai-media` | Unified media generation via fal.ai MCP — image, video, and audio. Covers text-to-image (Nano Banana), text/image-to-video (Seedance, Kling, Veo 3), text-to-speech (CSM-… | 1/1 |  |
| `file-access-vuln` | Entry P1 category router for file access and upload workflows. Use when testing download endpoints, file paths, local file inclusion, upload flows, preview pipelines, ar… | 2/2 |  |
| `git-guardrails-claude-code` | Set up Claude Code hooks to block dangerous git commands (push, reset --hard, clean, branch -D, etc.) before they execute. Use when user wants to prevent destructive git… | 2/1 |  |
| `google-drive` | Use connected Google Drive as the single entrypoint for Drive, Docs, Sheets, and Slides work. Use when the user wants to find, fetch, organize, share, export, copy, or d… | 1/1 |  |
| `google-drive-comments` | Write, reply to, and resolve Google Drive comments on Docs, Sheets, Slides, and Drive files with evidence-backed location context. Use when the user asks to leave commen… | 1/1 |  |
| `gpt-image-2-style-library` | Choose GPT-Image2 / gpt-image-2 visual styles and industrial prompt templates from the awesome-gpt-image-2 style library. Use when an agent needs to create, rewrite, cla… | 2/1 |  |
| `grill-me` | Interview the user relentlessly about a plan or design until reaching shared understanding, resolving each branch of the decision tree. Use when user wants to stress-tes… | 1/1 |  |
| `hunting-for-data-exfiltration-indicators` | Hunt for data exfiltration through network traffic analysis, detecting unusual data flows, DNS tunneling, cloud storage uploads, and encrypted channel abuse. | 1/1 |  |
| `implement` | Implement a piece of work based on a spec or set of tickets. | 1/1 |  |
| `implementing-aws-macie-for-data-classification` | Implement Amazon Macie to automatically discover, classify, and protect sensitive data in S3 buckets using machine learning and pattern matching for PII, financial data,… | 1/1 |  |
| `implementing-cloud-dlp-for-data-protection` | Implementing Cloud Data Loss Prevention (DLP) using Amazon Macie, Azure Information Protection, and Google Cloud DLP API to discover, classify, and protect sensitive dat… | 1/1 |  |
| `implementing-dragos-platform-for-ot-monitoring` | Deploy and configure the Dragos Platform for OT network monitoring, leveraging its 600+ industrial protocol parsers, intelligence-driven threat detection analytics, and… | 1/1 |  |
| `implementing-endpoint-dlp-controls` | Implements endpoint Data Loss Prevention (DLP) controls to detect and prevent sensitive data exfiltration through email, USB, cloud storage, and printing. Use when deplo… | 1/1 |  |
| `implementing-fuzz-testing-in-cicd-with-aflplusplus` | Integrate AFL++ coverage-guided fuzz testing into CI/CD pipelines to discover memory corruption, input handling, and logic vulnerabilities in C/C++ and compiled applicat… | 1/1 |  |
| `implementing-gdpr-data-protection-controls` | The General Data Protection Regulation (EU) 2016/679 (GDPR) is the EU's comprehensive data protection law governing the collection, processing, storage, and transfer of… | 1/1 |  |
| `implementing-immutable-backup-with-restic` | Implements immutable backup strategy using restic with S3-compatible storage and object lock for ransomware-resistant data protection. Automates backup creation, integri… | 1/1 |  |
| `implementing-ot-network-traffic-analysis-with-nozomi` | Deploy Nozomi Networks Guardian sensors for passive OT network traffic analysis to achieve comprehensive asset visibility, real-time threat detection, and vulnerability… | 1/1 |  |
| `implementing-siem-use-cases-for-detection` | Implements SIEM detection use cases by designing correlation rules, threshold alerts, and behavioral analytics mapped to MITRE ATT&CK techniques across Splunk, Elastic,… | 1/1 |  |
| `improve-codebase-architecture` | Scan a codebase for deepening opportunities, present them as a visual HTML report, then grill through whichever one you pick. | 2/2 |  |
| `maintain-space` | Reconcile new evidence into existing ChatGPT Pages or a Space when the user requests upkeep. For a direct text correction, use write-page. Do not use for ordinary chat d… | 1/1 |  |
| `manage-schedules` | Review a ChatGPT Space page and its schedules, recommend useful recurring work, and create, update, or remove scheduled automations. | 1/1 |  |
| `organize-space` | Organize existing ChatGPT Pages and Space structure when the user requests changes to that structure. Do not use for ordinary chat drafts or advice; a selected Page alon… | 1/1 |  |
| `performing-cloud-storage-forensic-acquisition` | Perform forensic acquisition and analysis of cloud storage services including Google Drive, OneDrive, Dropbox, and Box by collecting both API-based remote data and local… | 1/1 |  |
| `performing-cve-prioritization-with-kev-catalog` | Leverage the CISA Known Exploited Vulnerabilities catalog alongside EPSS and CVSS to prioritize CVE remediation based on real-world exploitation evidence. | 1/1 |  |
| `performing-dynamic-analysis-with-any-run` | Performs interactive dynamic malware analysis using the ANY.RUN cloud sandbox to observe real-time execution behavior, interact with malware prompts, and capture process… | 1/1 |  |
| `performing-ics-asset-discovery-with-claroty` | Perform comprehensive ICS/OT asset discovery using Claroty xDome platform, leveraging passive monitoring, Claroty Edge active queries, and integration ecosystem to gain… | 1/1 |  |
| `performing-thick-client-application-penetration-test` | Conduct a thick client application penetration test to identify insecure local storage, hardcoded credentials, DLL hijacking, memory manipulation, and insecure API commu… | 1/1 |  |
| `performing-threat-modeling-with-owasp-threat-dragon` | Use OWASP Threat Dragon to create data flow diagrams, identify threats using STRIDE and LINDDUN methodologies, and generate threat model reports for secure design review. | 1/1 |  |
| `pets` | List, inspect, select, download, or delete animated pets in ChatGPT Work mode. Use for an explicit pet in ChatGPT or established ChatGPT Pets context. Exclude real-world… | 1/1 |  |
| `prompt-injection-testing` | 大模型红队安全测试技能 - 自动化生成极高隐蔽性越狱测试提示词（图灵+空间拓扑+Anti-Refusal强力版），覆盖围栏对抗与底层对齐两大攻击面 | 1/1 |  |
| `prototype` | Build a throwaway prototype to answer a design question. Use when the user wants to sanity-check whether a state model or logic feels right, or explore what a UI should… | 2/2 |  |
| `recovering-deleted-files-with-photorec` | Recover deleted files from disk images and storage media using PhotoRec's file signature-based carving engine regardless of file system damage. | 1/1 |  |
| `research` | Investigate a question against high-trust primary sources and capture the findings as a Markdown file in the repo. Use when the user wants a topic researched, docs or AP… | 1/1 |  |
| `resolving-merge-conflicts` | Use when you need to resolve an in-progress git merge/rebase conflict. | 1/1 |  |
| `rev-unicorn-debug` | Debug and emulate specific code fragments or functions using the Unicorn engine. Activate when the user wants to emulate a function with Unicorn, trace binary execution… | 3/1 |  |
| `tdd` | Test-driven development with red-green-refactor loop. Use when user wants to build features or fix bugs using TDD, mentions "red-green-refactor", wants integration tests… | 1/1 |  |
| `teach` | Teach the user a new skill or concept, within this workspace. | 1/1 |  |
| `to-spec` | Turn the current conversation into a spec and publish it to the project issue tracker — no interview, just synthesis of what you've already discussed. | 1/1 |  |
| `to-tickets` | Break a plan, spec, or the current conversation into a set of tracer-bullet tickets, each declaring its blocking edges, published to the configured tracker — edges as te… | 1/1 |  |
| `triage` | Triage issues through a state machine driven by triage roles. Use when user wants to create an issue, triage issues, review incoming bugs or feature requests, prepare is… | 1/1 |  |
| `update-pet` | Inspect, validate, preview, repair, or update a custom pet in ChatGPT Work mode, including its name, description, or sprite sheet. Use for a pet in ChatGPT or establishe… | 1/1 |  |
| `upload-insecure-files` | Insecure file upload playbook. Use when testing upload validation, storage paths, processing pipelines, preview behavior, overwrite risks, and upload-to-RCE chains. | 2/2 |  |
| `writing-great-skills` | Reference for writing and editing skills well — the vocabulary and principles that make a skill predictable. | 1/1 |  |
| `zoom-out` | Tell the agent to zoom out and give broader context or a higher-level perspective. Use when you're unfamiliar with a section of code or need to understand how it fits in… | 1/1 |  |

### 軟體開發／測試／架構（38）

| Skill | 說明 | 定義/版本 | 旗標 |
|---|---|---:|---|
| `auditing-gcp-iam-permissions` | Auditing Google Cloud Platform IAM permissions to identify overly permissive bindings, primitive role usage, service account key proliferation, and cross-project access… | 1/1 |  |
| `caveman-core` | Caveman 输出压缩核心技能。将 AI 回复压缩至精简模式，token 实测节省 65%。 支持 6 级强度：lite (简洁) / full (默认, 压缩) / ultra (极限) / wenyan-lite / wenyan-full / wenyan-ultra (文言文)。 适用场景：任何需要减少 AI 输出 token… | 1/1 |  |
| `caveman-review` | 极致压缩的代码审查评论。每条发现一行：位置、问题、修复。 触发词："review this PR"、"代码审查"、"/review"、"审查这个PR"。 | 1/1 |  |
| `coding-standards` | Universal coding standards, best practices, and patterns for TypeScript, JavaScript, React, and Node.js development. | 1/1 |  |
| `configuring-certificate-authority-with-openssl` | A Certificate Authority (CA) is the trust anchor in a PKI hierarchy, responsible for issuing, signing, and revoking digital certificates. This skill covers building a tw… | 1/1 |  |
| `configuring-microsegmentation-for-zero-trust` | Configuring Microsegmentation For Zero Trust | 1/1 |  |
| `configuring-multi-factor-authentication-with-duo` | Deploy Cisco Duo multi-factor authentication across enterprise applications, VPN, RDP, and SSH access points. This skill covers Duo integration methods, adaptive authent… | 1/1 |  |
| `covert-channel-&-encoding` | Exfiltration Chain Phase 6/隐蔽信道与编码. 触发词: 隐蔽信道与编码。 | 1/1 | 覆寫特徵 |
| `cpp` | C++ programming with modern C++ features, STL, templates, and OOP | 1/1 |  |
| `csm-c-code-audit` | C代码审计 — 代码审计模块 \| Code Audit \| 难度★★★★ \| PTES框架 | 1/1 |  |
| `csm-code-audit-rust` | Rust代码审计 — 代码审计模块 \| Code Audit \| 难度★★★ \| PTES框架 | 1/1 |  |
| `csm-covering-tracks` | 进程注入与代码注入 — 痕迹清除模块 \| Covering Tracks \| 难度★★★★ \| PTES框架 | 1/1 |  |
| `csm-cpp-code-audit` | C++代码审计 — 代码审计模块 \| Code Audit \| 难度★★★★ \| PTES框架 | 1/1 |  |
| `csm-go-code-audit` | Go代码审计 — 代码审计模块 \| Code Audit \| 难度★★★ \| PTES框架 | 1/1 |  |
| `csm-java-code-audit` | Java代码审计 — 代码审计模块 \| Code Audit \| 难度★★★★ \| PTES框架 | 1/1 |  |
| `csm-javascript-code-audit` | JavaScript代码审计 — 代码审计模块 \| Code Audit \| 难度★★★ \| PTES框架 | 1/1 |  |
| `csm-php-code-audit` | PHP代码审计 — 代码审计模块 \| Code Audit \| 难度★★★ \| PTES框架 | 1/1 |  |
| `csm-python-code-audit` | Python代码审计 — 代码审计模块 \| Code Audit \| 难度★★★ \| PTES框架 | 1/1 |  |
| `csm-zero-trust-architecture` | 零信任架构设计与实施 — 零信任架构模块 \| Zero Trust Architecture \| 难度★★★★ \| PTES框架 | 1/1 |  |
| `csm-zero-trust-architecture-sdp` | 微隔离与软件定义边界(SDP) — 零信任架构模块 \| Zero Trust Architecture \| 难度★★★★ \| PTES框架 | 1/1 |  |
| `csm-zero-trust-architecture-ztna-iam` | ZTNA解决方案与IAM集成 — 零信任架构模块 \| Zero Trust Architecture \| 难度★★★★ \| PTES框架 | 1/1 |  |
| `deploying-tailscale-for-zero-trust-vpn` | Deploy and configure Tailscale as a WireGuard-based zero trust mesh VPN with identity-aware access controls, ACLs, and exit nodes for secure peer-to-peer connectivity. | 1/1 |  |
| `everything-claude-code-conventions` | Development conventions and patterns for everything-claude-code. JavaScript project with conventional commits. | 1/1 |  |
| `golang` | Go programming language including goroutines, channels, and concurrency patterns | 1/1 |  |
| `hunting-for-startup-folder-persistence` | Detect T1547.001 startup folder persistence by monitoring Windows startup directories for suspicious file creation, analyzing autoruns entries, and using Python watchdog… | 1/1 |  |
| `implementing-identity-verification-for-zero-trust` | Implementing Identity Verification For Zero Trust | 1/1 |  |
| `implementing-just-in-time-access-provisioning` | Implement Just-In-Time (JIT) access provisioning to eliminate standing privileges by granting temporary, time-bound access only when needed. This skill covers JIT archit… | 1/1 |  |
| `implementing-patch-management-workflow` | Patch management is the systematic process of identifying, testing, deploying, and verifying software updates to remediate vulnerabilities across an organization's IT in… | 1/1 |  |
| `implementing-syslog-centralization-with-rsyslog` | Configure rsyslog for centralized log collection with TLS encryption, custom templates, and log rotation. Generates server and client configuration files with GnuTLS str… | 1/1 |  |
| `java` | Java programming language including OOP, collections, multithreading, and Spring framework | 1/1 |  |
| `javascript` | JavaScript programming for web, including ES6+ features, DOM, async programming | 1/1 |  |
| `performing-soc-2-type-ii-audit-preparation` | SOC 2 Type II audit preparation involves designing, implementing, and demonstrating the operational effectiveness of controls aligned to the AICPA Trust Services Criteri… | 1/1 |  |
| `prototype-pollution` | Prototype pollution testing for JavaScript stacks. Use when user input is merged into objects (query parsers, JSON bodies, deep assign), when configuring libraries via u… | 2/2 |  |
| `string-obfuscation` | String obfuscation techniques including XOR, AES, RC4 encryption, base64 encoding, and function hashing to evade static analysis | 1/1 |  |
| `testing-qa` | — | 1/1 |  |
| `testing-standards` | Methodology Chain Phase 3/测试标准方法论. 触发词: 测试标准方法论。 | 1/1 | 覆寫特徵 |
| `web-backend-builder` | Scaffold backend API, data models, ORM setup, and endpoint inventory with OpenAPI output. | 1/1 |  |
| `xpath-injection-testing` | XPath注入深度测试技能：认证绕过、盲注数据提取、XPath 1.0/2.0差异、XSLT RCE、编码绕过、XML数据库攻击 | 1/1 |  |

### DevOps／雲端／容器（64）

| Skill | 說明 | 定義/版本 | 旗標 |
|---|---|---:|---|
| `analyzing-azure-activity-logs-for-threats` | Queries Azure Monitor activity logs and sign-in logs via azure-monitor-query to detect suspicious administrative operations, impossible travel, privilege escalation, and… | 1/1 |  |
| `analyzing-ethereum-smart-contract-vulnerabilities` | Perform static and symbolic analysis of Solidity smart contracts using Slither and Mythril to detect reentrancy, integer overflow, access control, and other vulnerabilit… | 1/1 |  |
| `analyzing-linux-elf-malware` | Analyzes malicious Linux ELF (Executable and Linkable Format) binaries including botnets, cryptominers, ransomware, and rootkits targeting Linux servers, containers, and… | 2/1 |  |
| `authbypass-authentication-flaws` | Authentication bypass testing playbook. Use when assessing login flows, password reset logic, account recovery, MFA bypass, token predictability, brute-force resistance,… | 2/2 |  |
| `building-devsecops-pipeline-with-gitlab-ci` | Design and implement a comprehensive DevSecOps pipeline in GitLab CI/CD integrating SAST, DAST, container scanning, dependency scanning, and secret detection. | 1/1 |  |
| `building-identity-federation-with-saml-azure-ad` | Establish SAML 2.0 identity federation between on-premises Active Directory and Azure AD (Microsoft Entra ID) for seamless cross-domain authentication and SSO to cloud a… | 1/1 |  |
| `competition-container-runtime` | Internal downstream skill for ctf-sandbox-orchestrator. CTF-sandbox workflow for live container runtime analysis, mounted secrets, sidecars, namespaces, init containers,… | 2/1 |  |
| `competition-k8s-control-plane` | Internal downstream skill for ctf-sandbox-orchestrator. CTF-sandbox workflow for Kubernetes API analysis, service-account trust, RBAC edges, admission and controller beh… | 2/1 |  |
| `competition-linux-credential-pivot` | Internal downstream skill for ctf-sandbox-orchestrator. CTF-sandbox workflow for Linux credential artifacts, service tokens, SSH material, cloud and container secrets, s… | 2/1 |  |
| `competition-runtime-routing` | Internal downstream skill for ctf-sandbox-orchestrator. CTF-sandbox workflow for reverse proxies, Host headers, forwarded headers, vhost routing, websocket upgrades, pat… | 2/1 |  |
| `competition-supply-chain` | Internal downstream skill for ctf-sandbox-orchestrator. CTF-sandbox workflow for CI/CD, registry, dependency drift, artifact provenance, image build, release pipeline, a… | 2/1 |  |
| `configuring-aws-verified-access-for-ztna` | Configure AWS Verified Access to provide VPN-less zero trust network access to internal applications using identity and device posture verification with Cedar policy lan… | 1/1 |  |
| `container-escape-techniques` | Container escape playbook. Use when operating inside a Docker container, LXC, or Kubernetes pod and need to escape to the host via privileged mode, capabilities, Docker… | 1/1 |  |
| `csm-devsecops-ci-cd` | CI/CD管道安全审计 — 安全开发运维模块 \| DevSecOps \| 难度★★★★ \| PTES框架 | 1/1 |  |
| `deploying-osquery-for-endpoint-monitoring` | Deploys and configures osquery for real-time endpoint monitoring using SQL-based queries to inspect running processes, open ports, installed software, and system configu… | 1/1 |  |
| `detecting-aws-cloudtrail-anomalies` | Detect unusual API call patterns in AWS CloudTrail logs using boto3, statistical baselining, and behavioral analysis to identify credential compromise, privilege escalat… | 1/1 |  |
| `detecting-aws-credential-exposure-with-trufflehog` | Detecting exposed AWS credentials in source code repositories, CI/CD pipelines, and configuration files using TruffleHog, git-secrets, and AWS-native detection mechanism… | 1/1 |  |
| `detecting-aws-iam-privilege-escalation` | Detect AWS IAM privilege escalation paths using boto3 and Cloudsplaining policy analysis to identify overly permissive policies, dangerous permission combinations, and l… | 2/2 |  |
| `detecting-azure-service-principal-abuse` | Detect and investigate Azure service principal abuse including privilege escalation, credential compromise, admin consent bypass, and unauthorized enumeration in Microso… | 1/1 |  |
| `detecting-compromised-cloud-credentials` | Detecting compromised cloud credentials across AWS, Azure, and GCP by analyzing anomalous API activity, impossible travel patterns, unauthorized resource provisioning, a… | 1/1 |  |
| `detecting-container-drift-at-runtime` | Detect unauthorized modifications to running containers by monitoring for binary execution drift, file system changes, and configuration deviations from the original con… | 1/1 |  |
| `detecting-s3-data-exfiltration-attempts` | Detecting data exfiltration attempts from AWS S3 buckets by analyzing CloudTrail S3 data events, VPC Flow Logs, GuardDuty findings, Amazon Macie alerts, and S3 access pa… | 1/1 |  |
| `docker-&-container-escape` | Linux PrivEsc Chain Phase 2/Docker与容器逃逸. 触发词: Docker与容器逃逸。 | 1/1 | 覆寫特徵 |
| `e2e-testing` | Playwright E2E testing patterns, Page Object Model, configuration, CI/CD integration, artifact management, and flaky test strategies. | 1/1 |  |
| `fakesign-driver-signing` | FakeSign 驱动免签名工具 — 自签证书绕过 Windows 驱动签名强制(DSE)、Cloudflare Workers 时间戳服务器 Docker一键部署。覆盖 RFC-3161 时间戳伪造、SignTool Hook、WDAC 绕过、EV 证书内核签名、测试证书套件。红队渗透中用于加载未签名内核驱动/rootkit、绕过杀软… | 1/1 |  |
| `hardening-docker-daemon-configuration` | Harden the Docker daemon by configuring daemon.json with user namespace remapping, TLS authentication, rootless mode, and CIS benchmark controls. | 2/2 |  |
| `hunting-for-living-off-the-cloud-techniques` | Hunt for adversary abuse of legitimate cloud services for C2, data staging, and exfiltration including abuse of Azure, AWS, GCP services, and SaaS platforms. | 1/1 |  |
| `hunting-for-webshell-activity` | Hunt for web shell deployments on internet-facing servers by analyzing file creation in web directories, suspicious process spawning from web servers, and anomalous HTTP… | 2/1 |  |
| `implementing-aws-config-rules-for-compliance` | Implementing AWS Config rules for continuous compliance monitoring of AWS resources, deploying managed and custom rules aligned to CIS and PCI DSS frameworks, configurin… | 1/1 |  |
| `implementing-azure-ad-privileged-identity-management` | Configure Microsoft Entra Privileged Identity Management to enforce just-in-time role activation, approval workflows, and access reviews for Azure AD privileged roles. | 1/1 |  |
| `implementing-canary-tokens-for-network-intrusion` | Deploys DNS, HTTP, and AWS API key canary tokens across network infrastructure to detect unauthorized access and lateral movement. Integrates with webhook alerting (Slac… | 1/1 |  |
| `implementing-code-signing-for-artifacts` | This skill covers implementing code signing for build artifacts to ensure integrity and authenticity throughout the software supply chain. It addresses signing binaries,… | 1/1 |  |
| `implementing-conditional-access-policies-azure-ad` | Configure Microsoft Entra ID (Azure AD) Conditional Access policies for zero trust access control. Covers signal-based policy design, device compliance requirements, ris… | 1/1 |  |
| `implementing-container-network-policies-with-calico` | Enforce Kubernetes network segmentation using Calico CNI network policies and global network policies to control pod-to-pod traffic, restrict egress, and implement zero-… | 1/1 |  |
| `implementing-delinea-secret-server-for-pam` | Implements Delinea Secret Server for privileged access management (PAM) including secret vault configuration, role-based access policies, automated password rotation, se… | 1/1 |  |
| `implementing-envelope-encryption-with-aws-kms` | Envelope encryption is a strategy where data is encrypted with a data encryption key (DEK), and the DEK itself is encrypted with a master key (KEK) managed by AWS KMS. T… | 1/1 |  |
| `implementing-hashicorp-vault-dynamic-secrets` | Implements HashiCorp Vault dynamic secrets engines for database credentials, AWS IAM keys, and PKI certificates with automatic generation, lease management, and credenti… | 1/1 |  |
| `implementing-image-provenance-verification-with-cosign` | Sign and verify container image provenance using Sigstore Cosign with keyless OIDC-based signing, attestations, and Kubernetes admission enforcement. | 1/1 |  |
| `implementing-kubernetes-network-policy-with-calico` | Implement Kubernetes network segmentation using Calico NetworkPolicy and GlobalNetworkPolicy for zero-trust pod-to-pod communication. | 1/1 |  |
| `implementing-network-policies-for-kubernetes` | Kubernetes NetworkPolicies provide pod-level network segmentation by defining ingress and egress rules that control traffic flow between pods, namespaces, and external e… | 1/1 |  |
| `implementing-opa-gatekeeper-for-policy-enforcement` | Enforce Kubernetes admission policies using OPA Gatekeeper with ConstraintTemplates, Rego rules, and the Gatekeeper policy library. | 1/1 |  |
| `implementing-patch-management-for-ot-systems` | This skill covers implementing a structured patch management program for OT/ICS environments where traditional IT patching approaches can cause process disruption or saf… | 1/1 |  |
| `implementing-policy-as-code-with-open-policy-agent` | This skill covers implementing Open Policy Agent (OPA) and Gatekeeper for policy-as-code enforcement in Kubernetes and CI/CD pipelines. It addresses writing Rego policie… | 1/1 |  |
| `implementing-privileged-identity-management-with-azure` | Configure Azure AD Privileged Identity Management (PIM) using Microsoft Graph API to manage eligible role assignments, just-in-time activation, access reviews, and role… | 1/1 |  |
| `implementing-rbac-for-kubernetes-cluster` | Configure Kubernetes Role-Based Access Control (RBAC) to enforce least-privilege access to cluster resources. This skill covers Role/ClusterRole design, RoleBinding conf… | 1/1 |  |
| `implementing-secret-scanning-with-gitleaks` | This skill covers implementing Gitleaks for detecting and preventing hardcoded secrets in git repositories. It addresses configuring pre-commit hooks, CI/CD pipeline int… | 1/1 |  |
| `implementing-secrets-management-with-vault` | This skill covers deploying HashiCorp Vault for centralized secrets management across cloud environments, including dynamic secret generation for databases and cloud pro… | 1/1 |  |
| `implementing-secrets-scanning-in-ci-cd` | Integrate gitleaks and trufflehog into CI/CD pipelines to detect leaked secrets before deployment | 1/1 |  |
| `implementing-semgrep-for-custom-sast-rules` | Write custom Semgrep SAST rules in YAML to detect application-specific vulnerabilities, enforce coding standards, and integrate into CI/CD pipelines. | 1/1 |  |
| `implementing-soar-playbook-for-phishing` | Automate phishing incident response using Splunk SOAR REST API to create containers, add artifacts, and trigger playbooks | 1/1 |  |
| `implementing-zero-trust-in-cloud` | This skill guides organizations through implementing zero trust architecture in cloud environments following NIST SP 800-207 and Google BeyondCorp principles. It covers… | 1/1 |  |
| `implementing-zero-trust-with-beyondcorp` | Deploy Google BeyondCorp Enterprise zero trust access controls using Identity-Aware Proxy (IAP), context-aware access policies, device trust validation, and Access Conte… | 1/1 |  |
| `performing-aws-privilege-escalation-assessment` | Performing authorized privilege escalation assessments in AWS environments to identify IAM misconfigurations that allow users or roles to elevate their permissions using… | 2/1 |  |
| `performing-indicator-lifecycle-management` | Indicator lifecycle management tracks IOCs from initial discovery through validation, enrichment, deployment, monitoring, and eventual retirement. This skill covers impl… | 1/1 |  |
| `performing-red-team-with-covenant` | Conduct red team operations using the Covenant C2 framework for authorized adversary simulation, including listener setup, grunt deployment, task execution, and lateral… | 2/2 |  |
| `performing-sca-dependency-scanning-with-snyk` | This skill covers implementing Software Composition Analysis (SCA) using Snyk to detect vulnerable open-source dependencies in CI/CD pipelines. It addresses scanning pac… | 2/1 |  |
| `phishing-kb` | Offensive phishing operations knowledge base for red team engagements. Use when the user asks about phishing infrastructure, page design, anti-detection, credential harv… | 1/1 |  |
| `sandbox-escape-techniques` | Sandbox escape playbook. Use when breaking out of Python sandbox, Lua sandbox, seccomp filter, chroot jail, container/Docker, browser sandbox, or namespace isolation to… | 1/1 |  |
| `scanning-container-images-with-grype` | Scan container images for known vulnerabilities using Anchore Grype with SBOM-based matching and configurable severity thresholds. | 2/2 |  |
| `securing-aws-iam-permissions` | This skill guides practitioners through hardening AWS Identity and Access Management configurations to enforce least privilege access across cloud accounts. It covers IA… | 2/1 |  |
| `securing-aws-lambda-execution-roles` | Securing AWS Lambda execution roles by implementing least-privilege IAM policies, applying permission boundaries, restricting resource-based policies, using IAM Access A… | 2/1 |  |
| `securing-container-registry-images` | Securing container registry images by implementing vulnerability scanning with Trivy and Grype, enforcing image signing with Cosign and Sigstore, configuring registry ac… | 2/1 |  |
| `testing-for-business-logic-vulnerabilities` | Identifying flaws in application business logic that allow price manipulation, workflow bypass, and privilege escalation beyond what technical vulnerability scanners can… | 1/1 |  |
| `web-deploy-launcher` | Prepare deployment configs, final checks, and pre-launch readiness artifacts for production release. | 1/1 |  |

### 資料／資料庫／分析（27）

| Skill | 說明 | 定義/版本 | 旗標 |
|---|---|---:|---|
| `ai-redteam` | Web+AI 安全测试知识库。融合 WooYun 88,636 案例 + 先知 L1-L4 方法论 + GAARM 173 风险 + OWASP Top 10 (LLM/ASI/WSTG)。 TRIGGER when 任务是实战安全测试：渗透测试、漏洞挖掘/利用、红队攻防、安全审计 (SAST/DAST)、 CTF、AI/LLM 安全测… | 1/1 |  |
| `backend-patterns` | Backend architecture patterns, API design, database optimization, and server-side best practices for Node.js, Express, and Next.js API routes. | 1/1 |  |
| `competition-android-hooking` | Internal downstream skill for ctf-sandbox-orchestrator. CTF-sandbox workflow for Android APK hooking, Frida tracing, request-signing recovery, SSL pinning bypass, JNI bo… | 2/1 |  |
| `database-brute-force` | Credential Breach Chain Phase 10/数据库口令爆破. 触发词: 数据库口令爆破。 | 1/1 | 覆寫特徵 |
| `deploying-ransomware-canary-files` | Deploys and monitors ransomware canary files across critical directories using Python's watchdog library for real-time filesystem event detection. Places strategically n… | 1/1 |  |
| `detecting-beaconing-patterns-with-zeek` | Performs statistical analysis of Zeek conn.log connection intervals to detect C2 beaconing patterns. Uses the ZAT library to load Zeek logs into Pandas DataFrames, calcu… | 1/1 |  |
| `detecting-insider-data-exfiltration-via-dlp` | Detects insider data exfiltration by analyzing DLP policy violations, file access patterns, upload volume anomalies, and off-hours activity in endpoint and cloud logs. U… | 1/1 |  |
| `detecting-insider-threat-with-ueba` | Implement User and Entity Behavior Analytics using Elasticsearch/OpenSearch to build behavioral baselines, calculate anomaly scores, perform peer group analysis, and det… | 1/1 |  |
| `detecting-shadow-it-cloud-usage` | Detect unauthorized SaaS and cloud service usage (shadow IT) by analyzing proxy logs, DNS query logs, and netflow data using Python pandas for traffic pattern analysis a… | 1/1 |  |
| `ida-re` | Drive IDA Pro through the IDA Pro MCP like a senior reverse engineer: don't just narrate decompiler output, transform the database. Use this whenever the user is reverse… | 2/1 |  |
| `implementing-network-traffic-baselining` | Build network traffic baselines from NetFlow/IPFIX data using Python pandas for statistical analysis, z-score anomaly detection, and hourly/daily traffic pattern profili… | 1/1 |  |
| `implementing-pam-for-database-access` | Deploy privileged access management for database systems including Oracle, SQL Server, PostgreSQL, and MySQL. Covers session proxy configuration, credential vaulting, qu… | 1/1 |  |
| `implementing-privileged-session-monitoring` | Monitor and audit privileged user sessions including SSH, RDP, and database access. Tracks session metadata, records commands, detects anomalous activity, and enforces s… | 1/1 |  |
| `investigating-insider-threat-indicators` | Investigates insider threat indicators including data exfiltration attempts, unauthorized access patterns, policy violations, and pre-departure behaviors using SIEM anal… | 1/1 |  |
| `ntlm-relay-coercion` | NTLM relay and authentication coercion playbook. Use when capturing and relaying NTLM authentication to escalate privileges via SMB, LDAP, HTTP, or MSSQL relay targets,… | 1/1 |  |
| `performing-ot-vulnerability-assessment-with-claroty` | This skill covers performing vulnerability assessments in OT environments using the Claroty xDome platform for comprehensive asset discovery, risk scoring, vulnerability… | 1/1 |  |
| `performing-privileged-account-discovery` | Discover and inventory all privileged accounts across enterprise infrastructure including domain admins, local admins, service accounts, database admins, cloud IAM roles… | 1/1 |  |
| `performing-service-account-credential-rotation` | Automate credential rotation for service accounts across Active Directory, cloud platforms, and application databases to eliminate stale secrets and reduce compromise ri… | 1/1 |  |
| `performing-sqlite-database-forensics` | Perform forensic analysis of SQLite databases to recover deleted records from freelists and WAL files, decode encoded timestamps, and extract evidence from browser histo… | 1/1 |  |
| `performing-user-behavior-analytics` | Performs User and Entity Behavior Analytics (UEBA) to detect anomalous user activities including impossible travel, unusual access patterns, privilege abuse, and insider… | 1/1 |  |
| `performing-vulnerability-scanning-with-nessus` | Performs authenticated and unauthenticated vulnerability scanning using Tenable Nessus to identify known vulnerabilities, misconfigurations, default credentials, and mis… | 1/1 |  |
| `php-codeigniter-audit` | CodeIgniter 框架特效安全审计工具。针对 CodeIgniter 的 CSRF、XSS 输出过滤、数据库查询构造、路由与验证器配置、会话 Cookie 安全等机制进行白盒静态审计，并映射到通用漏洞类型体系（CSRF/AUTH/XSS/SQL/CFG/SESS 等）。 | 1/1 |  |
| `php-sql-audit` | PHP Web 源码 SQL 注入漏洞审计工具。从源码中识别所有 SQL 执行点并分析注入风险，输出可利用性分级、PoC 与修复建议（禁止省略）。 | 1/1 |  |
| `php-thinkphp-audit` | ThinkPHP 框架特效安全审计工具。针对 ThinkPHP 常见的鉴权/CSRF/模板转义/ORM 写入（Mass Assignment）/调试与配置暴露等机制进行白盒静态审计，并映射到通用漏洞类型体系（AUTH/CSRF/TPL/XSS/LOGIC/CFG/SESS/SQL 等）。 | 1/1 |  |
| `php-wordpress-audit` | WordPress 框架特效安全审计工具。针对 WordPress 常见 nonce/capability/check_admin_referer、AJAX action、escape/sanitize、重定向、安全上传与远程请求等机制进行白盒静态审计，并映射到通用漏洞类型体系（AUTH/CSRF/XSS/SQL/CFG/SSRF 等）。 | 1/1 |  |
| `rev-idapython` | IDAPython and IDALib script reference for reverse engineering. Activate when the user needs to write IDAPython scripts in IDA, use IDALib for headless analysis, operate… | 3/1 |  |
| `web-database-validator` | Validate database schema, migrations, indexes, and query behavior with structured pass/fail reporting. | 1/1 |  |

### 資安—Web／API（220）

| Skill | 說明 | 定義/版本 | 旗標 |
|---|---|---:|---|
| `ai-security-rag` | RAG管线安全测试专家。覆盖知识库枚举、数据集/集合/来源ID泄露、引用/原文授权、跨租户检索ACL、文档上传投毒、检索劫持、网站同步SSRF、嵌入/向量存储暴露、引用元数据泄露、通过摄入内容的间接注入。含多平台RAG API参考（FastGPT/Dify/Flowise/Coze/LangChain）和自动枚举脚本。 | 1/1 |  |
| `ai-security-redteam` | AI安全红队主技能。全范围授权评估AI目标：聊天机器人/RAG/Agent/MCP/多Agent/向量/供应链/基础设施。自包含操作手册含攻击载荷、工具命令、证据规则、2026最新工具集成。对齐OWASP LLM 2025 + OWASP ASI 2026 + MITRE ATLAS + NIST AI RMF。含自动化测试脚本。信益安… | 1/1 | 覆寫特徵 |
| `analyzing-api-gateway-access-logs` | Parses API Gateway access logs (AWS API Gateway, Kong, Nginx) to detect BOLA/IDOR attacks, rate limit bypass, credential scanning, and injection attempts. Uses pandas fo… | 1/1 |  |
| `analyzing-office365-audit-logs-for-compromise` | Parse Office 365 Unified Audit Logs via Microsoft Graph API to detect email forwarding rule creation, inbox delegation, suspicious OAuth app grants, and other indicators… | 1/1 |  |
| `analyzing-web-server-logs-for-intrusion` | Parse Apache and Nginx access logs to detect SQL injection attempts, local file inclusion, directory traversal, web scanner fingerprints, and brute-force patterns. Uses… | 1/1 |  |
| `api-agent` | 负责 API 安全类漏洞检测：未授权访问/BOLA/BFLA/批量赋值/GraphQL 深度测试/ API 参数篡改/隐藏参数发现/WebSocket 安全/API 版本枚举/ 过度数据暴露 | 1/1 |  |
| `api-attacks` | Web Attack Chain Phase 1/API攻击. 触发词: API攻击。 | 1/1 | 覆寫特徵 |
| `api-auth-and-jwt-abuse` | API authentication and JWT abuse playbook. Use when testing bearer tokens, API keys, claim trust, header spoofing, rate limits, and API auth boundary weaknesses. | 2/2 |  |
| `api-authorization-and-bola` | API authorization and BOLA testing playbook. Use when APIs expose object identifiers, nested resources, hidden writable fields, or weak function-level authorization. | 2/2 |  |
| `api-design` | REST API design patterns including resource naming, status codes, pagination, filtering, error responses, versioning, and rate limiting for production APIs. | 1/1 |  |
| `api-fuzzing-bug-bounty` | Provide comprehensive techniques for testing REST, SOAP, and GraphQL APIs during bug bounty hunting and penetration testing engagements. Covers vulnerability discovery,… | 1/1 |  |
| `api-sec` | Entry P1 category router for API security. Use when choosing between API recon, authorization, token abuse, and hidden-parameter workflows before any deeper API topic sk… | 2/2 |  |
| `api-security` | Use for authorized security assessment of REST, GraphQL, WebSocket, or SOAP APIs, including discovery, authentication, authorization, rate-limit, and CI/CD testing. | 4/2 |  |
| `api-security-best-practices` | Implement secure API design patterns including authentication, authorization, input validation, rate limiting, and protection against common API vulnerabilities | 1/1 |  |
| `api-security-testing` | API security testing workflow for REST and GraphQL APIs covering authentication, authorization, rate limiting, input validation, and security best practices. | 1/1 |  |
| `auth-&-session-attacks` | Web Attack Chain Phase 24/认证与会话攻击. 触发词: 认证与会话攻击。 | 1/1 | 覆寫特徵 |
| `auth-agent` | 负责认证与会话类漏洞检测：认证绕过/暴力破解/会话管理/JWT/OAuth/SAML/ 密码重置绕过/验证码绕过/不安全随机数/用户枚举/OIDC/CSRF。 受控密码测试为条件执行：根据用户授权、测试账号情况、验证码类型和登录保护强度自主决策。 | 1/1 |  |
| `auth-sec` | Entry P1 category router for authentication and authorization. Use when testing login flows, sessions, object authorization, JWT, OAuth, CORS, CSRF, and enterprise SSO w… | 2/2 |  |
| `aws-penetration-testing` | Provide comprehensive techniques for penetration testing AWS cloud environments. Covers IAM enumeration, privilege escalation, SSRF to metadata endpoint, S3 bucket explo… | 1/1 |  |
| `backend-security-coder` | Expert in secure backend coding practices specializing in input validation, authentication, and API security. Use PROACTIVELY for backend security implementations or sec… | 1/1 |  |
| `Burp Suite/Web Security Skill` | Web application security testing with Burp Suite integration | 1/1 |  |
| `burp-suite-testing` | Execute comprehensive web application security testing using Burp Suite's integrated toolset, including HTTP traffic interception and modification, request analysis and… | 1/1 |  |
| `burpsuite-project-parser` | Searches and explores Burp Suite project files (.burp) from the command line. Use when searching response headers or bodies with regex patterns, extracting security audi… | 1/1 |  |
| `business-logic-flaws` | Web Attack Chain Phase 25/逻辑漏洞. 触发词: 逻辑漏洞。 | 1/1 | 覆寫特徵 |
| `cache-poisoning-&-host-header` | Web Attack Chain Phase 23/缓存投毒与Host头注入. 触发词: 缓存投毒与Host头注入。 | 1/1 | 覆寫特徵 |
| `capability-primitive-search` | 能力原语+状态空间搜索:read/write/exec/ssrf等原语凑RCE等式A-F,低危映射,正反向搜索,跨域兑现。Use when no single RCE, chaining low-severity vulns, or deriving novel attack chains. | 1/1 |  |
| `cc-skill-security-review` | This skill ensures all code follows security best practices and identifies potential vulnerabilities. Use when implementing authentication or authorization, handling use… | 1/1 |  |
| `cloud-k8s` | Use for authorized cloud, container, and Kubernetes security assessment including metadata SSRF, IAM misconfig, container escape paths, and cluster RBAC review. | 4/2 |  |
| `cloud-metadata-&-ssrf` | Cloud Attack Chain Phase 6/云元数据与SSRF. 触发词: 云元数据与SSRF。 | 1/1 | 覆寫特徵 |
| `cloud-security-audit` | 云安全深度审计专业技能：AWS/Azure/GCP/阿里云全平台覆盖、IAM滥用与提权、云原生攻击面、容器逃逸、元数据SSRF、存储桶劫持、从侦察到接管完整攻击链 | 1/1 |  |
| `command-injection` | Web Attack Chain Phase 15/命令注入. 触发词: 命令注入。 | 1/1 | 覆寫特徵 |
| `command-injection-testing` | OS命令注入深度测试技能：全平台命令连接符/分隔符、空格/关键字/通配符绕过、WAF绕过、无回显外带、沙箱逃逸 | 1/1 |  |
| `competition-cloud-metadata-path` | Internal downstream skill for ctf-sandbox-orchestrator. CTF-sandbox workflow for cloud metadata services, instance identity, workload identity, link-local credential pat… | 2/1 |  |
| `competition-dpapi-credential-chain` | Internal downstream skill for ctf-sandbox-orchestrator. CTF-sandbox workflow for DPAPI masterkeys, vault blobs, browser credential stores, protected secrets, domain back… | 2/1 |  |
| `competition-file-parser-chain` | Internal downstream skill for ctf-sandbox-orchestrator. CTF-sandbox workflow for file uploads, imports, previews, archive extraction, format conversion, parser invocatio… | 2/1 |  |
| `competition-graphql-rpc-drift` | Internal downstream skill for ctf-sandbox-orchestrator. CTF-sandbox workflow for GraphQL schemas, persisted queries, RPC manifests, generated clients, OpenAPI drift, hid… | 2/1 |  |
| `competition-identity-windows` | Internal downstream skill for ctf-sandbox-orchestrator. CTF-sandbox workflow for Active Directory, Kerberos, LDAP, OAuth, enterprise messaging, Windows host forensics, c… | 2/1 |  |
| `competition-jwt-claim-confusion` | Internal downstream skill for ctf-sandbox-orchestrator. CTF-sandbox workflow for JWT, JWS, and JWE validation paths, header parsing, key selection, claim acceptance, aud… | 2/1 |  |
| `competition-lsass-ticket-material` | Internal downstream skill for ctf-sandbox-orchestrator. CTF-sandbox workflow for LSASS-resident secrets, Windows logon sessions, Kerberos ticket caches, DPAPI-backed mat… | 2/1 |  |
| `competition-mailbox-abuse` | Internal downstream skill for ctf-sandbox-orchestrator. CTF-sandbox workflow for enterprise mail abuse, OAuth consent, inbox or forwarding rules, transport rules, shared… | 2/1 |  |
| `competition-oauth-oidc-chain` | Internal downstream skill for ctf-sandbox-orchestrator. CTF-sandbox workflow for OAuth, OIDC, redirect flows, state or nonce handling, PKCE, token exchange, refresh logi… | 2/1 |  |
| `competition-pcap-protocol` | Internal downstream skill for ctf-sandbox-orchestrator. CTF-sandbox workflow for packet capture analysis, session reconstruction, application-protocol decoding, stream r… | 2/1 |  |
| `competition-ssrf-metadata-pivot` | Internal downstream skill for ctf-sandbox-orchestrator. CTF-sandbox workflow for SSRF reachability, internal route probing, metadata-service access, credential pivoting,… | 2/1 |  |
| `competition-websocket-runtime` | Internal downstream skill for ctf-sandbox-orchestrator. CTF-sandbox workflow for WebSocket and SSE handshakes, auth material, subscription state, realtime message schema… | 2/1 |  |
| `conducting-api-security-testing` | Conducts security testing of REST, GraphQL, and gRPC APIs to identify vulnerabilities in authentication, authorization, rate limiting, input validation, and business log… | 1/1 |  |
| `conducting-cloud-penetration-testing` | This skill outlines methodologies for performing authorized penetration testing against AWS, Azure, and GCP cloud environments. It covers understanding the shared respon… | 2/1 |  |
| `conducting-mobile-app-penetration-test` | Conducts penetration testing of iOS and Android mobile applications following the OWASP Mobile Application Security Testing Guide (MASTG) to identify vulnerabilities in… | 1/1 |  |
| `configuring-oauth2-authorization-flow` | Configure secure OAuth 2.0 authorization flows including Authorization Code with PKCE, Client Credentials, and Device Authorization Grant. This skill covers flow selecti… | 1/1 |  |
| `cors-cross-origin-misconfiguration` | CORS misconfiguration testing playbook. Use when analyzing cross-origin trust, credentialed browser reads, origin reflection, preflight policy bugs, and browser-based ac… | 2/2 |  |
| `cors-misconfig` | Web Attack Chain Phase 2/CORS错误配置. 触发词: CORS错误配置。 | 1/1 | 覆寫特徵 |
| `csm-api-security-api` | API认证与授权安全 — API安全模块 \| API Security \| 难度★★★★ \| PTES框架 | 1/1 |  |
| `csm-api-security-graphql-api` | GraphQL与微服务API安全 — API安全模块 \| API Security \| 难度★★★★ \| PTES框架 | 1/1 |  |
| `csm-api-security-owasp-api` | OWASP API安全测试 — API安全模块 \| API Security \| 难度★★★★ \| PTES框架 | 1/1 |  |
| `csm-cloud-security-waf` | 云网络与WAF安全 — 云安全模块 \| Cloud Security \| 难度★★★★ \| PTES框架 | 1/1 |  |
| `csm-exploitation-ssrf` | SSRF服务端请求伪造 — 漏洞利用模块 \| Exploitation \| 难度★★★ \| PTES框架 | 1/1 |  |
| `csm-exploitation-web` | Web漏洞利用 — 漏洞利用模块 \| Exploitation \| 难度★★★ \| PTES框架 | 1/1 |  |
| `csm-web-vulnerability-scanning` | Web漏洞扫描 — 漏洞扫描模块 \| Vulnerability Scanning \| 难度★★★ \| PTES框架 | 1/1 |  |
| `csm-xss-cross-site-scripting` | XSS跨站脚本 — 漏洞利用模块 \| Exploitation \| 难度★★★ \| PTES框架 | 1/1 |  |
| `csp-bypass-advanced` | Advanced Content Security Policy bypass techniques. Use when XSS or data exfiltration is blocked by CSP and you need to find policy weaknesses, trusted endpoint abuse, n… | 1/1 |  |
| `csrf` | Web Attack Chain Phase 4/CSRF. 触发词: CSRF。 | 1/1 | 覆寫特徵 |
| `csrf-cross-site-request-forgery` | CSRF testing playbook. Use when reviewing state-changing web flows, anti-CSRF defenses, SameSite behavior, JSON CSRF, login CSRF, and OAuth state handling. | 2/2 |  |
| `csrf-testing` | CSRF跨站请求伪造深度测试技能：GET/POST/JSON/Flash/SOAP全类型、Token绕过矩阵、SameSite Lax/Strict/None绕过、CORS+CSRF组合攻击、登录CSRF/注销CSRF | 1/1 |  |
| `cyber-owasp-review` | Map application security findings to OWASP Top 10 categories and generate remediation checklists. Use for normalized AppSec review outputs and category-level prioritizat… | 1/1 |  |
| `dangling-markup-injection` | Dangling markup injection playbook. Use when HTML injection is possible but JavaScript execution is blocked (CSP, sanitizer strips event handlers, WAF blocks script tags… | 1/1 |  |
| `deserialization-testing` | 反序列化漏洞深度测试技能：Java/PHP/Python/.NET全语言、常见Gadget库、CommonsCollections/Fastjson/Shiro/Log4j等历史高危链、ysoserial/PhpGC工具使用、WAF绕过 | 1/1 |  |
| `detecting-api-enumeration-attacks` | Detect and prevent API enumeration attacks including BOLA and IDOR exploitation by monitoring sequential identifier access patterns and authorization failures. | 1/1 |  |
| `detecting-broken-object-property-level-authorization` | Detect and test for OWASP API3:2023 Broken Object Property Level Authorization vulnerabilities including excessive data exposure and mass assignment attacks. | 1/1 |  |
| `detecting-oauth-token-theft` | Detect OAuth access token theft and misuse by analyzing sign-in logs for impossible travel, new device patterns, token replay from unusual IPs, and anomalous scope reque… | 1/1 |  |
| `detecting-sql-injection-via-waf-logs` | Analyze WAF (ModSecurity/AWS WAF/Cloudflare) logs to detect SQL injection attack campaigns. Parses ModSecurity audit logs and JSON WAF event logs to identify SQLi patter… | 1/1 |  |
| `detecting-suspicious-oauth-application-consent` | Detect risky OAuth application consent grants in Azure AD / Microsoft Entra ID using Microsoft Graph API, audit logs, and permission analysis to identify illicit consent… | 1/1 |  |
| `directory-discovery` | Web Attack Chain Phase 22/目录与内容发现. 触发词: 目录与内容发现。 | 2/2 | 覆寫特徵 |
| `dns-rebinding-attacks` | DNS rebinding attack playbook. Use when testing applications that trust DNS resolution for origin checks, interact with internal services from browser context, or when S… | 1/1 |  |
| `exploiting-api-injection-vulnerabilities` | Tests APIs for injection vulnerabilities including SQL injection, NoSQL injection, OS command injection, LDAP injection, and Server-Side Request Forgery (SSRF) through A… | 2/2 |  |
| `exploiting-broken-function-level-authorization` | Tests APIs for Broken Function Level Authorization (BFLA) vulnerabilities where regular users can invoke administrative functions or access privileged API endpoints by d… | 2/1 |  |
| `exploiting-idor-vulnerabilities` | Identifying and exploiting Insecure Direct Object Reference vulnerabilities to access unauthorized resources by manipulating object identifiers in API requests and URLs. | 2/1 |  |
| `exploiting-insecure-data-storage-in-mobile` | Identifies and exploits insecure local data storage vulnerabilities in Android and iOS mobile applications including unencrypted databases, world-readable files, insecur… | 2/2 |  |
| `exploiting-jwt-algorithm-confusion-attack` | Exploits JWT algorithm confusion vulnerabilities where the server's token verification library accepts the algorithm specified in the JWT header rather than enforcing a… | 2/2 |  |
| `exploiting-nosql-injection-vulnerabilities` | Detect and exploit NoSQL injection vulnerabilities in MongoDB, CouchDB, and other NoSQL databases to demonstrate authentication bypass, data extraction, and unauthorized… | 2/1 |  |
| `exploiting-oauth-misconfiguration` | Identifying and exploiting OAuth 2.0 and OpenID Connect misconfigurations including redirect URI manipulation, token leakage, and authorization code theft during securit… | 2/1 |  |
| `exploiting-prototype-pollution-in-javascript` | Detect and exploit JavaScript prototype pollution vulnerabilities on both client-side and server-side applications to achieve XSS, RCE, and authentication bypass through… | 2/2 |  |
| `exploiting-server-side-request-forgery` | Identifying and exploiting SSRF vulnerabilities to access internal services, cloud metadata, and restricted network resources during authorized penetration tests. | 2/1 |  |
| `exploiting-sql-injection-vulnerabilities` | Identifies and exploits SQL injection vulnerabilities in web applications during authorized penetration tests using manual techniques and automated tools like sqlmap. Th… | 2/1 |  |
| `exploiting-sql-injection-with-sqlmap` | Detecting and exploiting SQL injection vulnerabilities using sqlmap to extract database contents during authorized penetration tests. | 2/1 |  |
| `exploiting-websocket-vulnerabilities` | Testing WebSocket implementations for authentication bypass, cross-site hijacking, injection attacks, and insecure message handling during authorized security assessment… | 2/1 |  |
| `fastjson-exploitation` | Fastjson反序列化漏洞深度利用专业技能：版本探测、AutoType全版本绕过、JNDI/BCEL/TemplatesImpl/c3p0利用链、不出网利用、WAF绕过、从探测到RCE完整攻击链 | 1/1 |  |
| `firmware-pentest` | 固件 / IoT 渗透链。从拿到一坨 .bin / .img 开始，闭环走完逆向 → 提取 → 模拟 → 利用。 方法论遵循 OWASP FSTM 九阶段；工具链以 binwalk v3、unblob、EMBA、Firmadyne、AFL++ 为主。 适用场景：路由器/摄像头/智能家居固件审计、固件升级包逆向、IoT CVE 复现、嵌入… | 4/2 |  |
| `ghost-bits-cast-attack` | Java "Ghost Bits" / Cast Attack playbook (Black Hat Asia 2026). Use when attacking Java services where 16-bit char is silently narrowed to 8-bit byte to bypass WAF/IDS f… | 1/1 |  |
| `google-workspace-automation` | Design Gmail, Drive, Sheets, and Calendar automations with scope-aware plans. Use for repeatable daily task automation with explicit OAuth scopes and audit-ready outputs. | 1/1 |  |
| `graphql-attacks` | Web Attack Chain Phase 5/GraphQL攻击. 触发词: GraphQL攻击。 | 1/1 | 覆寫特徵 |
| `hack` | Entry P0 primary router for HackSkills. Use when the task involves web application testing, API security assessment, recon, vulnerability triage, exploit path planning,… | 2/2 |  |
| `http-host-header-attacks` | HTTP Host header injection and routing abuse playbook. Use when the application trusts the Host header for generating URLs, routing requests, or access control — enablin… | 1/1 |  |
| `http-parameter-pollution` | HTTP Parameter Pollution (HPP): duplicate query/body keys parsed differently by servers, proxies, WAFs, and app frameworks. Use when filters and application layers disag… | 2/2 |  |
| `identity-federation` | Use for authorized assessment of federated identity systems including SAML, OIDC, OAuth2 flows, SSO misconfiguration, and token confusion issues. | 4/2 |  |
| `idor-broken-object-authorization` | IDOR and broken object authorization testing playbook. Use when requests expose object identifiers, tenant boundaries, writable fields, or missing object-level authoriza… | 2/2 |  |
| `idor-testing` | IDOR不安全直接对象引用深度测试技能：水平越权/垂直越权/BOLA/BFLA、参数篡改、对象ID枚举、GraphQL IDOR、批量分配 | 1/1 |  |
| `implementing-api-abuse-detection-with-rate-limiting` | Implement API abuse detection using token bucket, sliding window, and adaptive rate limiting algorithms to prevent DDoS, brute force, and credential stuffing attacks. | 1/1 |  |
| `implementing-api-gateway-security-controls` | Implements security controls at the API gateway layer including authentication enforcement, rate limiting, request validation, IP allowlisting, TLS termination, and thre… | 1/1 |  |
| `implementing-api-key-security-controls` | Implements secure API key generation, storage, rotation, and revocation controls to protect API authentication credentials from leakage, brute force, and abuse. The engi… | 1/1 |  |
| `implementing-api-rate-limiting-and-throttling` | Implements API rate limiting and throttling controls using token bucket, sliding window, and fixed window algorithms to protect against brute force attacks, credential s… | 1/1 |  |
| `implementing-api-schema-validation-security` | Implement API schema validation using OpenAPI specifications and JSON Schema to enforce input/output contracts and prevent injection, data exposure, and mass assignment… | 1/1 |  |
| `implementing-api-security-posture-management` | Implement API Security Posture Management to continuously discover, classify, and score APIs based on risk while enforcing security policies across the API lifecycle. | 1/1 |  |
| `implementing-api-security-testing-with-42crunch` | Implement comprehensive API security testing using the 42Crunch platform to perform static audit and dynamic conformance scanning of OpenAPI specifications. | 1/1 |  |
| `implementing-api-threat-protection-with-apigee` | Implement API threat protection using Google Apigee policies including JSON/XML threat protection, OAuth 2.0, SpikeArrest, and Advanced API Security for OWASP Top 10 def… | 1/1 |  |
| `implementing-cloud-waf-rules` | This skill covers deploying and tuning Web Application Firewall rules on AWS WAF, Azure WAF, and Cloudflare to protect cloud-hosted applications against OWASP Top 10 att… | 1/1 |  |
| `implementing-ddos-mitigation-with-cloudflare` | Configure Cloudflare DDoS protection with managed rulesets, rate limiting, WAF rules, Bot Management, and origin protection to mitigate volumetric, protocol, and applica… | 1/1 |  |
| `implementing-google-workspace-admin-security` | Implements comprehensive Google Workspace security hardening including admin console configuration, phishing-resistant MFA enforcement, DLP policies, email authenticatio… | 1/1 |  |
| `implementing-jwt-signing-and-verification` | JSON Web Tokens (JWT) defined in RFC 7519 are compact, URL-safe tokens used for authentication and authorization in web applications. This skill covers implementing secu… | 1/1 |  |
| `implementing-security-chaos-engineering` | Implements security chaos engineering experiments that deliberately disable or degrade security controls to verify detection and response capabilities. Tests WAF bypass,… | 1/1 |  |
| `implementing-web-application-logging-with-modsecurity` | Configure ModSecurity WAF with OWASP Core Rule Set (CRS) for web application logging, tune rules to reduce false positives, analyze audit logs for attack detection, and… | 1/1 |  |
| `implementing-zero-trust-for-saas-applications` | Implementing zero trust access controls for SaaS applications using CASB, SSPM, conditional access policies, OAuth app governance, and session controls to enforce identi… | 1/1 |  |
| `initial-access-phishing` | 初始访问/钓鱼/社工:凭据喷洒,AiTM,设备码,OAuth同意钓鱼,载荷,vishing。Use when needing initial access, phishing, AiTM, device code, or social engineering. | 1/1 |  |
| `injection-agent` | 负责所有注入类漏洞检测：SQLi/NoSQL/XSS(存储/反射/DOM)/SSRF/XXE/SSTI/RCE/反序列化/CRLF/XSLT/EL/JNDI | 1/1 |  |
| `injection-checking` | Entry P1 category router for injection testing. Use when routing between XSS, SQLi, SSRF, XXE, SSTI, command injection, and NoSQL injection workflows based on how attack… | 2/2 |  |
| `integrating-dast-with-owasp-zap-in-pipeline` | This skill covers integrating OWASP ZAP (Zed Attack Proxy) for Dynamic Application Security Testing in CI/CD pipelines. It addresses configuring baseline, full, and API… | 1/1 |  |
| `intercepting-mobile-traffic-with-burpsuite` | Intercepts and analyzes HTTP/HTTPS traffic from mobile applications using Burp Suite proxy to identify insecure API communications, authentication flaws, data leakage, a… | 2/1 |  |
| `java-route-mapper` | Java Web 源码路由与参数映射分析工具。从源码中提取**所有** HTTP 路由和参数，生成完整 Burp Suite 请求模板，并自动保存为 MD 文档。适用于：(1) 无 API 文档的项目完整接口梳理，(2) 生成所有接口的 Burp 测试请求，(3) 源码端点完整分析。支持 Spring MVC、Servlet、JAX-R… | 1/1 |  |
| `js-reverse-automation` | 通过 chrome-devtools-mcp 连接真实浏览器，跟踪 sign/enc/token 的生成链路，识别运行时入口函数与依赖，然后生成 JSRPC 注入代码、Flask 代理代码以及带校验输出的 Burp autoDecoder 对接文档,本skills只生成对应的代码，不会对未授权目标进行测试。 | 1/1 |  |
| `js-source-&-api-extraction` | Recon Chain Phase 3/JS源码分析与API提取. 触发词: JS源码分析与API提取。 | 1/1 | 覆寫特徵 |
| `jwt-attack` | Web Attack Chain Phase 6/JWT攻击. 触发词: JWT攻击。 | 1/1 | 覆寫特徵 |
| `jwt-oauth-token-attacks` | JWT and OAuth token attack playbook. Use when validating token trust, signing algorithms, key handling, claim abuse, bearer flows, and OAuth account-binding weaknesses. | 2/2 |  |
| `laravel-security-audit` | Security auditor for Laravel applications. Analyzes code for vulnerabilities, misconfigurations, and insecure practices using OWASP standards and Laravel security best p… | 1/1 |  |
| `log4shell-exploitation` | Log4Shell（CVE-2021-44228）深度利用专业技能：JNDI Lookup全链路利用、JDK各版本绕过技术、不出网利用、WAF绕过、从探测到RCE完整攻击链、影响面最广的Java漏洞专项 | 1/1 |  |
| `misc-agent` | 负责外围攻击面与协议边界安全检测：信息泄露/开放重定向/CORS/CSP/安全头/目录索引/子域名接管/401-403绕过/Web缓存欺骗/Clickjacking/Host头攻击 | 1/1 |  |
| `nosql-injection` | NoSQL injection playbook. Use when MongoDB-style operators, JSON query objects, flexible search filters, or backend query DSLs may allow data or logic abuse. | 2/2 | 覆寫特徵 |
| `oauth-&-sso-attacks` | Web Attack Chain Phase 8/OAuth与SSO攻击. 触发词: OAuth与SSO攻击。 | 1/1 | 覆寫特徵 |
| `oauth-oidc-misconfiguration` | OAuth and OIDC misconfiguration testing playbook. Use when reviewing redirect URI handling, state and nonce validation, PKCE, token audience, callback binding, and ident… | 2/2 |  |
| `oauth-phishing` | Social Engineering Chain Phase 1/OAuth钓鱼. 触发词: OAuth钓鱼。 | 1/1 | 覆寫特徵 |
| `path-traversal-lfi` | Path traversal and LFI playbook. Use when file paths, download endpoints, include operations, archive extraction, or wrapper behavior may expose filesystem control. | 1/1 |  |
| `pentest-ai-driven` | AI 主导的 Web 渗透测试技能。AI 是指挥官，脚本是武器库。AI 自主决策测试路径、召唤工具、解读结果、追踪攻击链。 覆盖中高危/严重漏洞的广谱挖掘，重点强化接口与参数发现能力。 内置自进化机制：每次测试结束后 AI 自动回溯「为什么漏了」，写入本地记忆数据库，下次启动时自动加载。 触发词：渗透测试、SRC漏洞挖掘、挖洞、接口测试… | 1/1 |  |
| `pentest-api-attacker` | Test APIs against OWASP API Security Top 10 including discovery, auth abuse, and protocol-specific checks. | 1/1 |  |
| `pentest-blackboard` | CyberStrikeAI 项目黑板：跨会话 Fact 图（SQLite）+ upsert_project_fact/record_vulnerability 边渗透边记录节奏、关系边 links、confidence、与多代理协调落库。Use when managing project facts, blackboard index,… | 1/1 |  |
| `pentest-injection-engine` | Systematically test authorized targets for SQL, XSS, SSTI, XXE, command, and request-smuggling injection classes. | 1/1 |  |
| `pentest-mobile-auditor` | Assess mobile applications with static and dynamic analysis aligned to OWASP MASTG and MASVS. | 1/1 |  |
| `pentest-tools` | 主动渗透测试工具链。覆盖信息收集、端口扫描、漏洞扫描、Web 渗透、SQL 注入、目录爆破、密码破解等场景。 通过 MCP server（pentestMCP / mcp-security-hub）将 20+ 安全工具暴露给 AI agent。 触发关键词：渗透测试、端口扫描、Nmap、漏洞扫描、Nuclei、SQL 注入、SQLMap… | 4/2 |  |
| `pentest-web-app-attacker` | Assess web applications against OWASP WSTG and OWASP Top 10 with reproducible evidence capture. | 1/1 |  |
| `performing-agentless-vulnerability-scanning` | Configure and execute agentless vulnerability scanning using network protocols, cloud snapshot analysis, and API-based discovery to assess systems without installing end… | 1/1 |  |
| `performing-api-fuzzing-with-restler` | Uses Microsoft RESTler to perform stateful REST API fuzzing by automatically generating and executing test sequences that exercise API endpoints, discover producer-consu… | 2/1 |  |
| `performing-api-rate-limiting-bypass` | Tests API rate limiting implementations for bypass vulnerabilities by manipulating request headers, IP addresses, HTTP methods, API versions, and encoding schemes to cir… | 1/1 |  |
| `performing-api-security-testing-with-postman` | Uses Postman to perform structured API security testing by building collections that test for OWASP API Security Top 10 vulnerabilities including authentication bypass,… | 1/1 |  |
| `performing-blind-ssrf-exploitation` | Detect and exploit blind Server-Side Request Forgery vulnerabilities using out-of-band techniques, DNS interactions, and timing analysis to access internal services and… | 2/1 |  |
| `performing-csrf-attack-simulation` | Testing web applications for Cross-Site Request Forgery vulnerabilities by crafting forged requests that exploit authenticated user sessions during authorized security a… | 2/2 |  |
| `performing-directory-traversal-testing` | Testing web applications for path traversal vulnerabilities that allow reading or writing arbitrary files on the server by manipulating file path parameters. | 2/1 |  |
| `performing-graphql-depth-limit-attack` | Execute and test GraphQL depth limit attacks using deeply nested recursive queries to identify denial-of-service vulnerabilities in GraphQL APIs. | 2/2 |  |
| `performing-graphql-introspection-attack` | Performs GraphQL introspection attacks to extract the full API schema including types, queries, mutations, subscriptions, and field definitions from GraphQL endpoints. T… | 2/2 |  |
| `performing-graphql-security-assessment` | Assessing GraphQL API endpoints for introspection leaks, injection attacks, authorization flaws, and denial-of-service vulnerabilities during authorized security tests. | 2/1 |  |
| `performing-ios-app-security-assessment` | Performs comprehensive iOS application security assessments using Frida for dynamic instrumentation, Objection for runtime exploration, SSL pinning bypass for traffic in… | 1/1 |  |
| `performing-jwt-none-algorithm-attack` | Execute and test the JWT none algorithm attack to bypass signature verification by manipulating the alg header field in JSON Web Tokens. | 2/2 |  |
| `performing-oauth-scope-minimization-review` | Performs OAuth 2.0 scope minimization review to identify over-permissioned third-party application integrations, excessive API scopes, unused token grants, and risky OAu… | 1/1 |  |
| `performing-second-order-sql-injection` | Detect and exploit second-order SQL injection vulnerabilities where malicious input is stored in a database and later executed in an unsafe SQL query during a different… | 1/1 |  |
| `performing-soap-web-service-security-testing` | Perform security testing of SOAP web services by analyzing WSDL definitions and testing for XML injection, XXE, WS-Security bypass, and SOAPAction spoofing. | 2/2 |  |
| `performing-ssrf-vulnerability-exploitation` | Test for Server-Side Request Forgery vulnerabilities by probing cloud metadata endpoints, internal network services, and protocol handlers through user-controllable URL… | 2/2 |  |
| `performing-web-application-firewall-bypass` | Bypass Web Application Firewall protections using encoding techniques, HTTP method manipulation, parameter pollution, and payload obfuscation to deliver SQL injection, X… | 2/1 |  |
| `performing-web-application-penetration-test` | Performs systematic security testing of web applications following the OWASP Web Security Testing Guide (WSTG) methodology to identify vulnerabilities in authentication,… | 2/1 |  |
| `performing-web-application-vulnerability-triage` | Triage web application vulnerability findings from DAST/SAST scanners using OWASP risk rating methodology to separate true positives from false positives and prioritize… | 1/1 |  |
| `performing-web-cache-deception-attack` | Execute web cache deception attacks by exploiting path normalization discrepancies between CDN caching layers and origin servers to cache and retrieve sensitive authenti… | 2/2 |  |
| `performing-web-cache-poisoning-attack` | Exploiting web cache mechanisms to serve malicious content to other users by poisoning cached responses through unkeyed headers and parameters during authorized security… | 2/2 |  |
| `php-config-audit` | PHP Web 配置安全审计工具。识别 CORS/错误暴露/调试开关/安全头/危险运行时开关等，输出分级、可利用性分析、PoC 与修复建议（禁止省略）。 | 1/1 |  |
| `php-csrf-audit` | PHP Web 源码 CSRF 审计工具。识别状态变更接口是否受 CSRF 保护，追踪 token 生成、校验与绕过条件，输出可利用性分级、PoC 与修复建议（禁止省略）。 | 1/1 |  |
| `php-laravel-audit` | Laravel 框架特效安全审计工具。针对 Laravel 常见鉴权/CSRF/Session/模型填充/Blade 渲染等框架特性进行白盒静态审计，并将风险映射到你现有通用漏洞类型体系（AUTH/CSRF/LOGIC/XSS/CFG 等）。 | 1/1 |  |
| `php-session-cookie-audit` | PHP Web 源码会话与 Cookie 安全审计工具。识别 session 固定、Cookie flags 不安全、JWT 验证缺陷与记住登录风险，输出分级、PoC 与修复建议（禁止省略）。 | 1/1 |  |
| `php-ssrf-audit` | PHP Web 源码 SSRF 审计工具。识别用户可控 URL/地址进入网络请求 Sink，追踪内网/协议/端口限制与回显，输出可利用性分级、PoC 与修复建议（禁止省略）。 | 1/1 |  |
| `php-symfony-audit` | Symfony 框架特效安全审计工具。针对 Symfony 常见 security.yaml、CSRF、Twig/Twig raw、表达式与访问控制等框架机制做白盒静态审计，并将风险映射到通用漏洞类型体系（AUTH/CSRF/CFG/XSS/TPL/LOGIC 等）。 | 1/1 |  |
| `php-xss-audit` | PHP Web 源码 XSS 审计工具。识别用户输入进入输出上下文（HTML/属性/JS/URL/模板），分析转义与防护策略，输出可利用性分级、PoC 与修复建议（禁止省略）。 | 1/1 |  |
| `php-xxe-audit` | PHP Web 源码 XXE 审计工具。识别 XML 解析点与实体处理配置，追踪 XML 输入来源与回显，输出可利用性分级、PoC 与修复建议（禁止省略）。 | 1/1 |  |
| `php-yii-audit` | Yii 框架特效安全审计工具。针对 Yii（通常指 Yii2）访问控制（AccessControl/RBAC）、CSRF、输入过滤规则、输出编码策略、URL/重定向安全等进行白盒静态审计，并映射到通用漏洞类型体系（AUTH/CSRF/XSS/CFG/LOGIC 等）。 | 1/1 |  |
| `protocol-reverse` | Use for authorized reverse engineering of custom binary protocols, Protobuf/gRPC, WebSocket frames, and PCAP-driven protocol recovery. | 4/2 |  |
| `proxy-tool-bootstrap` | 自找代理+工具自举:SOCKS5/HTTP/Tor换路序列,工具Python自举,字典自生成,OOB基础设施。Use when blocked by 403/429/WAF/timeout, missing tools, or needing OOB confirmation. | 1/1 |  |
| `request-smuggling` | HTTP request smuggling and desynchronization testing. Use when front proxies, CDNs, or load balancers disagree with the origin on message framing (Content-Length vs Tran… | 2/2 |  |
| `securing-api-gateway-with-aws-waf` | Securing API Gateway endpoints with AWS WAF by configuring managed rule groups for OWASP Top 10 protection, creating custom rate limiting rules, implementing bot control… | 1/1 |  |
| `securing-historian-server-in-ot-environment` | This skill covers hardening and securing process historian servers (OSIsoft PI, Honeywell PHD, GE Proficy, AVEVA Historian) in OT environments. It addresses network plac… | 1/1 |  |
| `shiro-exploitation` | Apache Shiro反序列化漏洞深度利用专业技能：rememberMe Cookie CBC/GCM双模式利用、Key爆破字典、Gadget链选择、WAF绕过、从探测到RCE完整攻击链 | 1/1 |  |
| `skill` | SRC 漏洞挖掘 + 白盒 0day 审计全流程技能。覆盖国内大厂、中小企业、 政府/教育/医疗等目标类型。包含：JS 逆向接口发现、越权/注入/逻辑漏洞测试、 WAF 绕过、白盒代码审计（Linux Kernel/Chromium/Laravel/Spring/Django）、以及中文 SRC 报告生成。 当用户提到以下任意关键词时必… | 1/1 |  |
| `source-leak-&-version-control` | Web Attack Chain Phase 20/源码泄露与版本控制. 触发词: 源码泄露与版本控制。 | 1/1 | 覆寫特徵 |
| `spring-exploitation` | Spring Framework漏洞深度利用专业技能：Spring4Shell/SpEL注入/Spring Cloud Function/Spring Gateway/Spring Boot Actuator全系列漏洞利用、从指纹识别到RCE完整攻击链、WAF绕过与不出网利用 | 1/1 |  |
| `sql-injection` | Web Attack Chain Phase 9/SQL注入. 触发词: SQL注入。 | 1/1 | 覆寫特徵 |
| `sql-injection-testing` | Execute comprehensive SQL injection vulnerability assessments on web applications to identify database security flaws, demonstrate exploitation techniques, and validate… | 1/1 |  |
| `sqli-sql-injection` | SQL injection playbook. Use when input reaches SQL queries, authentication logic, sorting, filtering, reporting, or DB-specific blind and out-of-band execution paths. | 2/2 |  |
| `sqlmap-database-pentesting` | Provide systematic methodologies for automated SQL injection detection and exploitation using SQLMap. | 1/1 |  |
| `src-hunter` | 实战 SRC / 众测 / Bug bounty 漏洞挖掘工作流 skill。包含：5 阶段方法论（intake → recon → enum → hunt → report）、19 个攻击类 playbook（SQLi/XSS/RCE/SSRF/IDOR/CSRF/Path Traversal/File Upload/SSTI/XXE… | 4/3 |  |
| `ssrf` | Web Attack Chain Phase 10/SSRF. 触发词: SSRF。 | 1/1 | 覆寫特徵 |
| `ssrf-server-side-request-forgery` | SSRF playbook. Use when the server fetches URLs, resolves hostnames, imports remote content, or can be driven toward internal networks, cloud metadata, or secondary prot… | 2/2 |  |
| `ssrf-testing` | SSRF服务器端请求伪造深度测试技能：内网渗透全协议攻击面、云元数据、Gopher/Dict全协议利用、WAF绕过、Redis/FastCGI/Memcached RCE利用链 | 1/1 |  |
| `ssti` | Web Attack Chain Phase 19/模板注入SSTI. 触发词: 模板注入SSTI。 | 1/1 | 覆寫特徵 |
| `targeted-web-exploitation` | Exploit Chain Phase 3/Web漏洞定向利用. 触发词: Web漏洞定向利用。 | 1/1 | 覆寫特徵 |
| `testing-api-authentication-weaknesses` | Tests API authentication mechanisms for weaknesses including broken token validation, missing authentication on endpoints, weak password policies, credential stuffing su… | 2/1 |  |
| `testing-api-for-broken-object-level-authorization` | Tests REST and GraphQL APIs for Broken Object Level Authorization (BOLA/IDOR) vulnerabilities where an authenticated user can access or modify resources belonging to oth… | 2/1 |  |
| `testing-api-security-with-owasp-top-10` | Systematically assessing REST and GraphQL API endpoints against the OWASP API Security Top 10 risks using automated and manual testing techniques. | 2/1 |  |
| `testing-cors-misconfiguration` | Identifying and exploiting Cross-Origin Resource Sharing misconfigurations that allow unauthorized cross-domain data access and credential theft during security assessme… | 2/1 |  |
| `testing-for-host-header-injection` | Test web applications for HTTP Host header injection vulnerabilities to identify password reset poisoning, web cache poisoning, SSRF, and virtual host routing manipulati… | 1/1 |  |
| `testing-for-json-web-token-vulnerabilities` | Test JWT implementations for critical vulnerabilities including algorithm confusion, none algorithm bypass, kid parameter injection, and weak secret exploitation to achi… | 1/1 |  |
| `testing-for-xml-injection-vulnerabilities` | Test web applications for XML injection vulnerabilities including XXE, XPath injection, and XML entity attacks to identify data exposure and server-side request forgery… | 1/1 |  |
| `testing-for-xss-vulnerabilities` | Tests web applications for Cross-Site Scripting (XSS) vulnerabilities by injecting JavaScript payloads into reflected, stored, and DOM-based contexts to demonstrate clie… | 1/1 |  |
| `testing-for-xss-vulnerabilities-with-burpsuite` | Identifying and validating cross-site scripting vulnerabilities using Burp Suite's scanner, intruder, and repeater tools during authorized security assessments. | 1/1 |  |
| `testing-for-xxe-injection-vulnerabilities` | Discovering and exploiting XML External Entity injection vulnerabilities to read server files, perform SSRF, and exfiltrate data during authorized penetration tests. | 1/1 |  |
| `testing-jwt-token-security` | Assessing JSON Web Token implementations for cryptographic weaknesses, algorithm confusion attacks, and authorization bypass vulnerabilities during security engagements. | 2/1 |  |
| `testing-mobile-api-authentication` | Tests authentication and authorization mechanisms in mobile application APIs to identify broken authentication, insecure token management, session fixation, privilege es… | 1/1 |  |
| `testing-oauth2-implementation-flaws` | Tests OAuth 2.0 and OpenID Connect implementations for security flaws including authorization code interception, redirect URI manipulation, CSRF in OAuth flows, token le… | 2/1 |  |
| `testing-websocket-api-security` | Tests WebSocket API implementations for security vulnerabilities including missing authentication on WebSocket upgrade, Cross-Site WebSocket Hijacking (CSWSH), injection… | 2/1 |  |
| `threat-modeling` | Threat model, security audit, find vulnerabilities, check security of my app, risk assessment, penetration test prep, analyze attack surface, what could an attacker expl… | 1/1 |  |
| `top-web-vulnerabilities` | Provide a comprehensive, structured reference for the 100 most critical web application vulnerabilities organized by category. This skill enables systematic vulnerabilit… | 1/1 |  |
| `vulnerability-scanner` | Advanced vulnerability analysis principles. OWASP 2025, Supply Chain Security, attack surface mapping, risk prioritization. | 1/1 |  |
| `waf-&-cdn-detection` | Recon Chain Phase 4/WAF与CDN识别. 触发词: WAF与CDN识别。 | 1/1 | 覆寫特徵 |
| `waf-bypass-techniques` | WAF bypass methodology and generic evasion techniques. Use when a web application firewall blocks injection payloads (SQLi, XSS, RCE) and you need to craft bypasses usin… | 1/1 |  |
| `Web Attack Chain` | Web攻击类 automated penetration testing chain. 触发词: Web攻击类。 | 1/1 | 覆寫特徵 |
| `web-api-tester` | Test API endpoints for correctness, edge cases, auth handling, and OpenAPI contract compliance. | 1/1 |  |
| `web-attack-methods` | Web全栈攻击:SQLi/命令注入/SSTI/XSS/SSRF/NoSQL,认证JWT/OAuth/SAML,LFI/上传,Tomcat/WS/STOMP/XFF/PATH_INFO/CDN502/网宿JS挑战绕过。Use when testing Web injection, auth bypass, server-side, WAF… | 1/1 |  |
| `web-cache-deception` | Web cache deception and poisoning playbook. Use when CDN, reverse proxy, or application caching may serve sensitive authenticated content to other users due to path conf… | 2/2 |  |
| `web-security-testing` | Web application security testing workflow for OWASP Top 10 vulnerabilities including injection, XSS, authentication flaws, and access control issues. | 1/1 |  |
| `web-vulnerability-labs` | Lab & Training Chain Phase 3/Web漏洞靶场. 触发词: Web漏洞靶场。 | 1/1 | 覆寫特徵 |
| `web-vulnerability-scanners` | Web Attack Chain Phase 12/Web扫描器. 触发词: Web扫描器。 | 1/1 | 覆寫特徵 |
| `websocket-attacks` | Web Attack Chain Phase 11/WebSocket攻击. 触发词: WebSocket攻击。 | 1/1 | 覆寫特徵 |
| `websocket-security` | WebSocket handshake, CSWSH, tooling (wsrepl, ws-harness, Burp), and common flaws. Use when apps use real-time channels, chat, notifications, or WS-backed APIs. | 2/2 |  |
| `wordpress-penetration-testing` | Assess WordPress installations for common vulnerabilities and WordPress 7.0 attack surfaces. | 1/1 | 覆寫特徵 |
| `xss-cross-site-scripting` | XSS playbook. Use when user-controlled content reaches HTML, attributes, JavaScript, DOM sinks, uploads, or multi-context rendering paths. | 2/2 |  |
| `xss-html-injection` | Execute comprehensive client-side injection vulnerability assessments on web applications to identify XSS and HTML injection flaws, demonstrate exploitation techniques f… | 1/1 |  |
| `xss-testing` | XSS跨站脚本攻击深度测试技能：覆盖反射/存储/DOM/mXSS/vXSS全类型、CSP绕过、WAF绕过、现代浏览器防护对抗、高级利用链 | 1/1 |  |
| `xxe` | Web Attack Chain Phase 14/XXE. 触发词: XXE。 | 1/1 | 覆寫特徵 |
| `xxe-testing` | XXE XML外部实体注入测试的专业技能和方法论 | 1/1 |  |
| `xxe-xml-external-entity` | XXE playbook. Use when XML, SVG, OOXML, SOAP, or parser-driven imports may resolve external entities, files, or internal network resources. | 2/2 |  |
| `子域名接管` | Web Attack Chain Phase 16/子域名接管. 触发词: 子域名接管。 | 1/1 | 覆寫特徵 |

### 資安—逆向／惡意程式／漏洞利用（230）

| Skill | 說明 | 定義/版本 | 旗標 |
|---|---|---:|---|
| `.net-&-java-reverse-engineering` | Reverse Engineering Chain Phase 1/.NET-Java逆向. 触发词: .NET-Java逆向。 | 1/1 | 覆寫特徵 |
| `ai-av-evasion-optimized` | 使用AI生成免杀Loader和处理Shellcode，结合IPv4混淆、XOR加密、Module Stomping等免杀技术绕过主流杀软检测 | 1/1 |  |
| `amsi-bypass` | AMSI (Antimalware Scan Interface) bypass techniques for PowerShell, .NET, and script-based attacks | 1/1 |  |
| `analyzing-android-malware-with-apktool` | Perform static analysis of Android APK malware samples using apktool for decompilation, jadx for Java source recovery, and androguard for permission analysis, manifest i… | 2/2 |  |
| `analyzing-bootkit-and-rootkit-samples` | Analyzes bootkit and advanced rootkit malware that infects the Master Boot Record (MBR), Volume Boot Record (VBR), or UEFI firmware to gain persistence below the operati… | 1/1 |  |
| `analyzing-command-and-control-communication` | Analyzes malware command-and-control (C2) communication protocols to understand beacon patterns, command structures, data encoding, and infrastructure. Covers HTTP, HTTP… | 2/1 |  |
| `analyzing-email-headers-for-phishing-investigation` | Parse and analyze email headers to trace the origin of phishing emails, verify sender authenticity, and identify spoofing through SPF, DKIM, and DMARC validation. | 1/1 |  |
| `analyzing-golang-malware-with-ghidra` | Reverse engineer Go-compiled malware using Ghidra with specialized scripts for function recovery, string extraction, and type reconstruction in stripped Go binaries. | 2/2 |  |
| `analyzing-heap-spray-exploitation` | Detect and analyze heap spray attacks in memory dumps using Volatility3 plugins to identify NOP sled patterns, shellcode landing zones, and suspicious large allocations… | 1/1 |  |
| `analyzing-indicators-of-compromise` | Analyzes indicators of compromise (IOCs) including IP addresses, domains, file hashes, URLs, and email artifacts to determine maliciousness confidence, campaign attribut… | 1/1 |  |
| `analyzing-ios-app-security-with-objection` | Performs runtime mobile security exploration of iOS applications using Objection, a Frida-powered toolkit that enables security testers to interact with app internals wi… | 1/1 |  |
| `analyzing-linux-kernel-rootkits` | Detect kernel-level rootkits in Linux memory dumps using Volatility3 linux plugins (check_syscall, lsmod, hidden_modules), rkhunter system scanning, and /proc vs /sys di… | 1/1 |  |
| `analyzing-lnk-file-and-jump-list-artifacts` | Analyze Windows LNK shortcut files and Jump List artifacts to establish evidence of file access, program execution, and user activity using LECmd, JLECmd, and manual bin… | 1/1 |  |
| `analyzing-malware-behavior-with-cuckoo-sandbox` | Executes malware samples in Cuckoo Sandbox to observe runtime behavior including process creation, file system modifications, registry changes, network communications, a… | 2/1 |  |
| `analyzing-malware-family-relationships-with-malpedia` | Use the Malpedia platform and API to research malware family relationships, track variant evolution, link families to threat actors, and integrate YARA rules for detecti… | 2/2 |  |
| `analyzing-malware-persistence-with-autoruns` | Use Sysinternals Autoruns to systematically identify and analyze malware persistence mechanisms across registry keys, scheduled tasks, services, drivers, and startup loc… | 2/2 |  |
| `analyzing-malware-sandbox-evasion-techniques` | Detect sandbox evasion techniques in malware samples by analyzing timing checks, VM artifact queries, user interaction detection, and sleep inflation patterns from Cucko… | 2/2 |  |
| `analyzing-memory-dumps-with-volatility` | Analyzes RAM memory dumps from compromised systems using the Volatility framework to identify malicious processes, injected code, network connections, loaded modules, an… | 2/1 |  |
| `analyzing-network-covert-channels-in-malware` | Detect and analyze covert communication channels used by malware including DNS tunneling, ICMP exfiltration, steganographic HTTP, and protocol abuse for C2 and data exfi… | 1/1 |  |
| `analyzing-network-traffic-of-malware` | Analyzes network traffic generated by malware during sandbox execution or live incident response to identify C2 protocols, data exfiltration channels, payload downloads,… | 1/1 |  |
| `analyzing-packed-malware-with-upx-unpacker` | Identifies and unpacks UPX-packed and other packed malware samples to expose the original executable code for static analysis. Covers both standard UPX unpacking and han… | 2/1 |  |
| `analyzing-supply-chain-malware-artifacts` | Investigate supply chain attack artifacts including trojanized software updates, compromised build pipelines, and sideloaded dependencies to identify intrusion vectors a… | 1/1 |  |
| `analyzing-threat-landscape-with-misp` | Analyze the threat landscape using MISP (Malware Information Sharing Platform) by querying event statistics, attribute distributions, threat actor galaxy clusters, and t… | 1/1 |  |
| `anti-debugging-techniques` | Anti-debugging detection and bypass playbook. Use when reversing protected binaries that detect debuggers via ptrace, PEB flags, timing checks, or signal/exception handl… | 1/1 |  |
| `anti-reversing-techniques` | AUTHORIZED USE ONLY: This skill contains dual-use security techniques. Before proceeding with any bypass or analysis: > 1. | 3/3 |  |
| `apk-reverse` | 在 CLI 环境下做 Android APK 逆向时使用。适用于 APK 解包、Java 反编译、smali 修改、重打包、Frida 动态 Hook，以及按需切换到 so/native 分析。优先使用本机已安装的 jadx、apktool、frida、adb、ida-reverse、radare2。 | 4/2 |  |
| `attack-chain` | Use for authorized multi-stage attack-path planning and orchestration when a task spans reconnaissance, initial access, privilege escalation, lateral movement, or impact… | 4/2 |  |
| `binary-&-pwn-labs` | Lab & Training Chain Phase 4/二进制与PWN靶场. 触发词: 二进制与PWN靶场。 | 1/1 | 覆寫特徵 |
| `binary-mobile-reversing` | APK/EXE/二进制:UniApp/DCloud/Flutter逆向,证书固定绕过,导出组件,内存破坏exploit链,IoT固件。Use when reversing APK/EXE, UniApp/Flutter, native .so, or memory-corruption exploits. | 1/1 |  |
| `binary-ninja-reverse` | Use for authorized binary analysis in Binary Ninja, including HLIL/MLIL/LLIL inspection, strings/imports/exports, cross-references, types, patch review, Python API autom… | 1/1 |  |
| `binary-protection-bypass` | Binary protection bypass playbook. Use when identifying and bypassing ASLR, PIE, NX/DEP, stack canary, RELRO, FORTIFY_SOURCE, CET, and MTE protections in ELF binaries to… | 1/1 |  |
| `browser-automation` | 统一自动化入口。覆盖浏览器自动化（Playwright）和 Windows 桌面应用自动化（OpenReverse）。 浏览器场景：打开网页、点击、填表、爬取、截图、自动化登录、渗透页面交互。 桌面场景：操作 IDA/x64dbg 等 GUI 工具、Windows UI Automation、视觉驱动交互、桌面应用网络抓包。 触发关键词… | 4/2 |  |
| `browser-extension-reverse` | Use for authorized reverse engineering of browser extensions (Chrome/Firefox) including manifest analysis, background workers, and extension-based credential or traffic… | 4/2 |  |
| `building-automated-malware-submission-pipeline` | Builds an automated malware submission and analysis pipeline that collects suspicious files from endpoints and email gateways, submits them to sandbox environments and m… | 1/1 |  |
| `building-malware-incident-communication-template` | Build structured communication templates for malware incidents including stakeholder notifications, executive briefings, technical advisories, and regulatory disclosures… | 1/1 |  |
| `building-threat-feed-aggregation-with-misp` | Deploy MISP (Malware Information Sharing Platform) to aggregate, correlate, and distribute threat intelligence feeds from multiple sources for centralized IOC management… | 1/1 |  |
| `code-audit` | Use for authorized source-code security review and SAST workflows including Semgrep, CodeQL patterns, dangerous API hunting, and fix verification. | 5/3 |  |
| `code-obfuscation-deobfuscation` | Code obfuscation analysis and deobfuscation playbook. Use when reversing binaries protected by junk code, opaque predicates, self-modifying code, control flow flattening… | 1/1 |  |
| `collecting-threat-intelligence-with-misp` | MISP (Malware Information Sharing Platform) is an open-source threat intelligence platform for gathering, sharing, storing, and correlating Indicators of Compromise (IOC… | 1/1 |  |
| `competition-custom-protocol-replay` | Internal downstream skill for ctf-sandbox-orchestrator. CTF-sandbox workflow for custom binary or text protocol recovery, handshake reconstruction, framing, sequence con… | 2/1 |  |
| `competition-firmware-layout` | Internal downstream skill for ctf-sandbox-orchestrator. CTF-sandbox workflow for firmware images, partition tables, boot chains, update packages, extracted filesystems,… | 2/1 |  |
| `competition-forensic-timeline` | Internal downstream skill for ctf-sandbox-orchestrator. CTF-sandbox workflow for DFIR chronology, cross-artifact correlation, persistence chains, and incident timeline r… | 2/1 |  |
| `competition-ios-runtime` | Internal downstream skill for ctf-sandbox-orchestrator. CTF-sandbox workflow for IPA runtime analysis, Frida hooks, Objective-C or Swift method tracing, Keychain inspect… | 2/1 |  |
| `competition-kerberos-delegation` | Internal downstream skill for ctf-sandbox-orchestrator. CTF-sandbox workflow for Kerberos delegation, SPN trust edges, S4U abuse, RBCD, constrained or unconstrained dele… | 2/1 |  |
| `competition-kernel-container-escape` | Internal downstream skill for ctf-sandbox-orchestrator. CTF-sandbox workflow for kernel attack surface, namespace and cgroup boundaries, container isolation assumptions,… | 2/1 |  |
| `competition-malware-config` | Internal downstream skill for ctf-sandbox-orchestrator. CTF-sandbox workflow for malware configuration recovery, staged payload boundaries, beacon parameter extraction,… | 2/1 |  |
| `competition-queue-worker-drift` | Internal downstream skill for ctf-sandbox-orchestrator. CTF-sandbox workflow for queues, async workers, cron jobs, delayed tasks, retry behavior, worker-only config drif… | 2/1 |  |
| `competition-race-condition-state-drift` | Internal downstream skill for ctf-sandbox-orchestrator. CTF-sandbox workflow for race windows, ordering bugs, idempotency failures, lock gaps, concurrent worker drift, a… | 2/1 |  |
| `competition-request-normalization-smuggling` | Internal downstream skill for ctf-sandbox-orchestrator. CTF-sandbox workflow for parser differentials, HTTP normalization gaps, ambiguous headers, path decoding drift, t… | 2/1 |  |
| `competition-reverse-pwn` | Internal downstream skill for ctf-sandbox-orchestrator. CTF-sandbox workflow for reverse engineering, malware, DFIR, firmware, pwnable, and native exploit challenges. Us… | 2/1 |  |
| `competition-template-render-path` | Internal downstream skill for ctf-sandbox-orchestrator. CTF-sandbox workflow for SSR, template rendering, route loaders, hydration payloads, server-client render boundar… | 2/1 |  |
| `competition-windows-pivot` | Internal downstream skill for ctf-sandbox-orchestrator. CTF-sandbox workflow for Kerberos, WinRM, SMB, RDP, Windows credential material, replayable tickets, delegation e… | 2/1 |  |
| `competition-zip-archive` | Internal downstream skill for ctf-sandbox-orchestrator. CTF-sandbox workflow for ZIP and PKZIP archive challenges, legacy ZipCrypto identification, known-plaintext recov… | 2/1 |  |
| `conducting-malware-incident-response` | Responds to malware infections across enterprise endpoints by identifying the malware family, determining infection vectors, assessing spread, and executing eradication… | 1/1 |  |
| `conducting-man-in-the-middle-attack-simulation` | Simulates man-in-the-middle attacks using Ettercap, mitmproxy, and Bettercap in authorized environments to intercept, analyze, and modify network traffic for testing enc… | 2/1 |  |
| `conducting-memory-forensics-with-volatility` | Performs memory forensics analysis using Volatility 3 to extract evidence of malware execution, process injection, network connections, and credential theft from RAM dum… | 1/1 |  |
| `configuring-windows-defender-advanced-settings` | Configures Microsoft Defender for Endpoint (MDE) advanced protection settings including attack surface reduction rules, controlled folder access, network protection, and… | 1/1 |  |
| `cryptographic-algorithm-identification` | Reverse Engineering Chain Phase 7/密码算法识别. 触发词: 密码算法识别。 | 1/1 | 覆寫特徵 |
| `csm-iot-security` | 固件逆向与分析 — 物联网安全模块 \| IoT Security \| 难度★★★★★ \| PTES框架 | 1/1 |  |
| `csm-persistence-bootkit` | Bootkit与固件持久化 — 持久化模块 \| Persistence \| 难度★★★★★ \| PTES框架 | 1/1 |  |
| `csm-reverse-engineering` | 静态逆向分析 — 逆向工程模块 \| Reverse Engineering \| 难度★★★★ \| PTES框架 | 1/1 |  |
| `ctf-malware` | Provides malware analysis and network traffic techniques for CTF challenges. Use when analyzing obfuscated scripts, malicious packages, custom crypto protocols, C2 traff… | 1/1 |  |
| `ctf-misc` | Provides miscellaneous CTF challenge techniques for problems that do not cleanly fit the main categories. Use for encoding puzzles, pyjails, bash jails, RF/SDR, DNS oddi… | 1/1 |  |
| `ctf-osint` | Provides open source intelligence techniques for CTF challenges. Use when gathering information from public sources, social media, geolocation, DNS records, username enu… | 1/1 |  |
| `ctf-pwn` | Provides binary exploitation techniques for CTF challenges. Use when you already have a vulnerable native target or service and need to turn memory corruption or low-lev… | 1/1 |  |
| `ctf-reverse` | Provides reverse engineering techniques for CTF challenges. Use when the main job is to understand how a compiled, obfuscated, packed, or virtualized target works before… | 1/1 |  |
| `ctf-sandbox` | Thin PRIMARY for CTF / AWD / 靶场 multi-type orchestration. Hands off to the sidecar CTF-Sandbox-Orchestrator. Use when the user says CTF, AWD, 靶场, or 比赛题 and no more spec… | 3/1 |  |
| `database-security` | Use for authorized database security assessment covering PostgreSQL/MySQL/MSSQL/Mongo/Redis exposure, authz, UDF/command paths, and misconfiguration review. | 4/2 |  |
| `decompile` | Decompile a function to C-like pseudocode using angr | 2/2 |  |
| `deobfuscating-javascript-malware` | Deobfuscates malicious JavaScript code used in web-based attacks, phishing pages, and dropper scripts by reversing encoding layers, eval chains, string manipulation, and… | 2/1 |  |
| `deobfuscating-powershell-obfuscated-malware` | Systematically deobfuscate multi-layer PowerShell malware using AST analysis, dynamic tracing, and tools like PSDecode and PowerDecode to reveal hidden payloads and C2 i… | 2/2 |  |
| `detecting-fileless-attacks-on-endpoints` | Detects fileless malware and in-memory attacks that execute entirely in RAM without writing persistent files to disk, evading traditional antivirus. Use when building de… | 2/1 |  |
| `detecting-fileless-malware-techniques` | Detects and analyzes fileless malware that operates entirely in memory using PowerShell, WMI, .NET reflection, registry-resident payloads, and living-off-the-land binari… | 2/1 |  |
| `detecting-mimikatz-execution-patterns` | Detect Mimikatz execution through command-line patterns, LSASS access signatures, binary indicators, and in-memory detection of known modules. | 2/1 |  |
| `detecting-mobile-malware-behavior` | Detects and analyzes malicious behavior in mobile applications through behavioral analysis, permission abuse detection, network traffic monitoring, and dynamic instrumen… | 1/1 |  |
| `detecting-process-injection-techniques` | Detects and analyzes process injection techniques used by malware including classic DLL injection, process hollowing, APC injection, thread hijacking, and reflective loa… | 2/1 |  |
| `detecting-rootkit-activity` | Detects rootkit presence on compromised systems by identifying hidden processes, hooked system calls, modified kernel structures, hidden files, and covert network connec… | 1/1 |  |
| `digital-forensics` | Use for authorized digital forensics including memory dumps, disk timelines, PCAP investigation, artifact triage, and IR evidence preservation. | 4/2 |  |
| `donut-customhost` | Donut CustomHost — 红队 Shellcode 生成神器。将 .NET EXE/DLL/VBS/JS/XSL 转为位置无关 shellcode，内置 Custom CLR Host 绕过 ETW/AMSI/WLDP、Memory Tracking Evasion、架构感知 ETW Bypass、随机加密混淆。红队后渗透免… | 1/1 |  |
| `dotnet-reverse` | .NET / C# 二进制逆向。当目标是 .NET assembly（PE 头含 CLR、.exe/.dll 托管程序）、C# 编译产物（含 NativeAOT）、红队 Sharp* 工具（Rubeus / SharpHound / SharpHound 等）、.NET 混淆程序（ConfuserEx / SmartAssembly /… | 4/2 |  |
| `dsl-vm-reverse` | Reverse JavaScript-based custom DSL/VM interpreters, non-standard WASM-like runtimes, and risk-control engines. Use when analyzing IIFE or switch-based opcode dispatcher… | 3/1 |  |
| `dynamic-debugging` | Reverse Engineering Chain Phase 5/动态调试. 触发词: 动态调试。 | 1/1 | 覆寫特徵 |
| `edr-bypass-re` | 逆向防御方实现 → 红队针对性绕过。把 EDR / Defender / AV 的 hook 表、ETW provider、AMSI 实现先逆向出来， 再写针对性的 unhook / 间接 syscall / ETW patch / call stack spoof。对照 MITRE ATT&CK T1562 防御规避。 触发关键词：E… | 4/2 |  |
| `email-security` | Use for authorized email security review including phishing analysis, header authentication (SPF/DKIM/DMARC), BEC patterns, and mailbox token abuse research. | 4/2 |  |
| `eradicating-malware-from-infected-systems` | Systematically remove malware, backdoors, and attacker persistence mechanisms from infected systems while ensuring complete eradication and preventing re-infection. | 1/1 |  |
| `exploitarium-0day-arsenal` | Exploitarium 批量 0Day 武器库 — 23 个未公开漏洞 POC，覆盖 Web RCE/容器逃逸/本地提权/供应链/网络中间件/浏览器/远程桌面。 包含 10 个已分配 CVE：CVE-2026-58050~CVE-2026-58058。 厂商覆盖：Floci, PHP, FFmpeg, c-ares, libssh2,… | 1/1 |  |
| `exploiting-bgp-hijacking-vulnerabilities` | Analyzes and simulates BGP hijacking scenarios in authorized lab environments to assess route origin validation, RPKI deployment, and BGP monitoring defenses against pre… | 2/1 |  |
| `extracting-iocs-from-malware-samples` | Extracts indicators of compromise (IOCs) from malware samples including file hashes, network indicators (IPs, domains, URLs), host artifacts (file paths, registry keys,… | 2/1 |  |
| `extracting-memory-artifacts-with-rekall` | Uses Rekall memory forensics framework to analyze memory dumps for process hollowing, injected code via VAD anomalies, hidden processes, and rootkit detection. Applies p… | 2/2 |  |
| `find-oep` | Smart trace-based OEP finder for packed/protected PE executables. Traces through packer stubs using intelligent stepping, anti-debug evasion, and heuristic OEP detection… | 2/2 |  |
| `firmware-analysis` | Reverse Engineering Chain Phase 6/固件分析. 触发词: 固件分析。 | 1/1 | 覆寫特徵 |
| `frida-hook-&-injection` | Mobile Attack Chain Phase 3/Frida Hook与注入. 触发词: Frida Hook与注入。 | 1/1 | 覆寫特徵 |
| `frida-win` | Cheatsheet for dynamic instrumentation and security analysis of Windows binaries with Frida and the frida-tools CLI (frida REPL, frida-trace, frida-ps). Use it for runti… | 2/1 |  |
| `game-hacking` | 游戏辅助开发全链路助手——覆盖内存读写、协议分析、反编译、Hook 技术、驱动级隐藏、自动化脚本。 支持 C/C++、Python、x86/x64 汇编、DirectX/OpenGL。适用于 PC 端游、Android/iOS 手游、主机游戏。 当用户提到以下任何关键词时必须触发：游戏外挂、游戏辅助、内存修改、CE教程、游戏Hook、… | 1/1 |  |
| `ghidra-reverse` | Use for free/open reverse engineering with Ghidra (headless or GUI), including decompile, cross-refs, and optional Ghidra MCP workflows when IDA is unavailable. | 4/2 |  |
| `go-rust-reverse` | Use for reverse engineering stripped Go and Rust binaries including runtime recognition, pclntab/moduel data recovery, panic strings, and idiomatic decompilation recover… | 4/2 |  |
| `hardware-security` | Use for authorized hardware and embedded interface security research including UART/JTAG discovery, debug pad triage, secure boot overview, and offline firmware extracti… | 4/2 |  |
| `http2-specific-attacks` | HTTP/2 protocol-specific attack playbook. Use when the target supports HTTP/2 and you need to exploit binary framing, HPACK compression, h2c upgrade smuggling, pseudo-he… | 1/1 |  |
| `hunting-advanced-persistent-threats` | Proactively hunts for Advanced Persistent Threat (APT) activity within enterprise environments using hypothesis-driven searches across endpoint telemetry, network logs,… | 1/1 |  |
| `hunting-for-data-staging-before-exfiltration` | Detect data staging activity before exfiltration by monitoring for archive creation with 7-Zip/RAR, unusual temp folder access, large file consolidation, and staging dir… | 1/1 |  |
| `hunting-for-unusual-service-installations` | Detect suspicious Windows service installations (MITRE ATT&CK T1543.003) by parsing System event logs for Event ID 7045, analyzing service binary paths, and identifying… | 1/1 |  |
| `IDA-Skill` | IDA Pro 逆向分析。通过 IDAPython 脚本获取反汇编、反编译、字符串、导入表、交叉引用等信息。 | 1/1 |  |
| `implementing-alert-fatigue-reduction` | Implements strategies to reduce SOC alert fatigue by tuning detection rules, consolidating duplicate alerts, implementing risk-based alerting, and measuring alert qualit… | 1/1 |  |
| `implementing-application-whitelisting-with-applocker` | Implements application whitelisting using Windows AppLocker to restrict unauthorized software execution on endpoints, reducing attack surface from malware, unauthorized… | 1/1 |  |
| `implementing-bgp-security-with-rpki` | Implement BGP route origin validation using RPKI with Route Origin Authorizations, RPKI-to-Router protocol, and ROV policies on Cisco and Juniper routers to prevent rout… | 1/1 |  |
| `implementing-cloud-workload-protection` | Implements cloud workload protection using boto3 and google-cloud APIs for runtime security monitoring, process anomaly detection, and file integrity checking on EC2/GCE… | 1/1 |  |
| `implementing-continuous-security-validation-with-bas` | Deploy Breach and Attack Simulation tools to continuously validate security control effectiveness by safely emulating real-world attack techniques across the kill chain. | 1/1 |  |
| `implementing-dmarc-dkim-spf-email-security` | SPF, DKIM, and DMARC form the three pillars of email authentication. Together they prevent domain spoofing, validate message integrity, and define policies for handling… | 1/1 |  |
| `implementing-email-sandboxing-with-proofpoint` | Email sandboxing detonates suspicious attachments and URLs in isolated environments to detect zero-day malware and evasive phishing payloads. Proofpoint Targeted Attack… | 1/1 |  |
| `implementing-email-security-with-dmarc-dkim-spf` | Audit and validate email authentication configurations by checking SPF, DKIM, and DMARC DNS records for a domain. Uses dnspython to query TXT records, validates SPF synt… | 1/1 |  |
| `implementing-gcp-binary-authorization` | Implement GCP Binary Authorization to enforce deploy-time security controls that ensure only trusted, attested container images are deployed to Google Kubernetes Engine… | 1/1 |  |
| `implementing-google-workspace-phishing-protection` | Configure Google Workspace advanced phishing and malware protection settings including pre-delivery scanning, attachment protection, spoofing detection, and Enhanced Saf… | 1/1 |  |
| `implementing-iec-62443-security-zones` | This skill covers designing and implementing security zones and conduits for industrial automation and control systems (IACS) per IEC 62443-3-2. It addresses zone partit… | 1/1 |  |
| `implementing-log-integrity-with-blockchain` | Build an append-only log integrity chain using SHA-256 hash chaining for tamper detection. Each log entry is hashed with the previous entry's hash to create a blockchain… | 1/1 |  |
| `implementing-memory-protection-with-dep-aslr` | Implements memory protection mechanisms including DEP (Data Execution Prevention), ASLR (Address Space Layout Randomization), CFG (Control Flow Guard), and other exploit… | 1/1 |  |
| `implementing-mtls-for-zero-trust-services` | Configures mutual TLS (mTLS) authentication between microservices using Python cryptography library for certificate generation and ssl module for TLS verification. Valid… | 1/1 |  |
| `implementing-network-segmentation-for-ot` | This skill covers implementing network segmentation in Operational Technology environments using VLANs, industrial firewalls, data diodes, and software-defined networkin… | 1/1 |  |
| `implementing-proofpoint-email-security-gateway` | Deploy and configure Proofpoint Email Protection as a secure email gateway to detect and block phishing, malware, BEC, and spam before messages reach user inboxes. | 1/1 |  |
| `implementing-security-information-sharing-with-stix2` | Create, validate, and share STIX 2.1 threat intelligence objects using the stix2 Python library. Covers indicators, malware, campaigns, relationships, bundles, and TAXII… | 1/1 |  |
| `implementing-usb-device-control-policy` | Implements USB device control policies to restrict unauthorized removable media access on endpoints, preventing data exfiltration and malware introduction via USB device… | 1/1 |  |
| `ios-pentesting-tricks` | iOS pentesting playbook. Use when testing iOS applications for keychain extraction, URL scheme hijacking, Universal Links exploitation, runtime manipulation, binary prot… | 1/1 |  |
| `js-reverse` | 在使用 js-reverse-mcp 做前端 JavaScript 逆向时使用，适用于签名链路定位、页面观察取证、运行时采样、本地补环境复现与证据化输出。优先适配当前环境里的 js-reverse_* 工具，需要更强的浏览器/CDP/Hook 面时联动 jshookmcp。 | 4/2 |  |
| `jsr-reverse` | Use when a Web JS reverse task has unclear phase selection, mixed source-chain and shell blockers, runtime divergence, validation-only work, or RS/瑞数 clues such as 412,… | 1/1 |  |
| `kernel-exploitation` | Linux kernel exploitation playbook. Use when exploiting kernel vulnerabilities (UAF, OOB, race condition, type confusion) for privilege escalation via commit_creds, modp… | 2/2 | 覆寫特徵 |
| `khaosldr-evasion` | KhaosLdr — Windows 高级 Shellcode 加载器与 EDR 规避框架。集成直接系统调用（Direct Syscalls）、硬件断点（HWBP）绕过、IPv4 混淆 Shellcode 解码、EVS XOR 字符串混淆、多层沙箱/VM 检测逃逸、PPID 父进程欺骗、Syscall 级休眠混淆、RC4 载荷加密、多模… | 1/1 |  |
| `linux-suid-sudo-exploitation` | Linux SUID/GUID binary exploitation and sudo misconfiguration techniques including GTFOBins usage and privilege escalation | 1/1 |  |
| `llm-security` | Use for authorized security assessment of LLM applications and AI agents, including prompt injection, tool abuse, RAG exposure, memory poisoning, and model supply-chain… | 4/2 | 覆寫特徵 |
| `macos-reverse` | Use for authorized macOS and Mach-O reverse engineering including codesign, Objective-C/Swift recovery, endpoint security surfaces, and Apple platform malware analysis. | 4/2 |  |
| `malware-analysis` | Use when analyzing suspected malware through static, dynamic, and behavioral techniques, including IOC extraction, YARA or Sigma rules, sandboxing, and anti-analysis beh… | 4/2 |  |
| `malware-analyst` | Expert malware analyst specializing in defensive malware research, threat intelligence, and incident response. Masters sandbox analysis, behavioral analysis, and malware… | 1/1 |  |
| `malware-sample-analysis` | Reverse Engineering Chain Phase 8/恶意样本分析. 触发词: 恶意样本分析。 | 1/1 | 覆寫特徵 |
| `malware-triage` | — | 1/1 |  |
| `memory-forensics` | Comprehensive techniques for acquiring, analyzing, and extracting artifacts from memory dumps for incident response and malware analysis. | 1/1 |  |
| `memory-forensics-volatility` | Memory forensics playbook using Volatility 2/3. Use when analyzing memory dumps for malware analysis, credential extraction, process investigation, code injection detect… | 1/1 |  |
| `ml-model-eval-benchmark` | Compare model candidates using weighted metrics and deterministic ranking outputs. Use for benchmark leaderboards and model promotion decisions. | 1/1 |  |
| `mobile-app-security-testing` | 移动应用安全深度测试专业技能：Android/iOS双平台覆盖、静态逆向与动态调试、Hook注入与脱壳、数据存储与传输安全、从逆向分析到漏洞利用完整攻击链 | 1/1 |  |
| `mobile-reverse` | Use for authorized Android or iOS application reverse engineering and security testing, including APK or IPA analysis, runtime instrumentation, SSL pinning, and platform… | 4/2 |  |
| `mobile-security-coder` | Expert in secure mobile coding practices specializing in input validation, WebView security, and mobile-specific security patterns. | 1/1 |  |
| `obfuscation-deobfuscation` | Reverse Engineering Chain Phase 9/混淆还原. 触发词: 混淆还原。 | 1/1 | 覆寫特徵 |
| `ot-ics` | Use for authorized OT/ICS security assessment covering Purdue model zoning, PLC/SCADA exposure, industrial protocol discovery, and safe passive-first evaluation. | 4/2 |  |
| `p3-shellcode-loader` | P³ (Process Parameter Poisoning) — 高级 Windows Shellcode 注入技术 PE Loader。利用 PEB 中 Process Parameters 结构作为 Shellcode 暂存区，通过修改进程命令行伪装进程启动参数，规避 VirtualAllocEx/WriteProcessMem… | 1/1 |  |
| `packing-&-unpacking` | Reverse Engineering Chain Phase 4/加壳与脱壳. 触发词: 加壳与脱壳。 | 1/1 | 覆寫特徵 |
| `patch-diff-exploit` | N-day 补丁差分到利用。从厂商发布的补丁里反推漏洞点、写 PoC、做成可用的攻击模块。 适用场景：已知 CVE 编号但只有补丁没有 PoC、SRC/红队需要打击未及时更新的资产、N-day 武器化、Patch Tuesday 跟进。 核心方法：拿 before/after 二进制 → 对齐符号 → 二进制 diff → 看新增的安全… | 4/2 |  |
| `pentest-remediation-validator` | Retest remediated findings, detect regressions, and generate remediation status and certification artifacts. | 1/1 |  |
| `pentest-verification` | 验证铁律:搜索≠漏洞,confirmed Fact须证据,tentative表线索,禁止空泛推测,负结果也落库, 想象力拉满+单步验证零容忍。Use when writing project facts, validating findings, or avoiding hallucination. | 1/1 |  |
| `performing-access-recertification-with-saviynt` | Configure and execute access recertification campaigns in Saviynt Enterprise Identity Cloud to validate user entitlements, revoke excessive access, and maintain complian… | 1/1 |  |
| `performing-adversary-in-the-middle-phishing-detection` | Detect and respond to Adversary-in-the-Middle (AiTM) phishing attacks that use reverse proxy kits like EvilProxy, Evilginx, and Tycoon 2FA to bypass MFA and steal sessio… | 1/1 |  |
| `performing-arp-spoofing-attack-simulation` | Simulates ARP spoofing attacks in authorized lab or pentest environments using arpspoof, Ettercap, and Scapy to demonstrate man-in-the-middle risks, test network detecti… | 2/2 |  |
| `performing-automated-malware-analysis-with-cape` | Deploy and operate CAPEv2 sandbox for automated malware analysis with behavioral monitoring, payload extraction, configuration parsing, and anti-evasion capabilities. | 1/1 |  |
| `performing-binary-exploitation-analysis` | Analyze binary exploitation techniques including buffer overflows and ROP chains using pwntools Python library. Covers checksec analysis, gadget discovery with ROPgadget… | 2/2 |  |
| `performing-cloud-penetration-testing-with-pacu` | Performing authorized AWS penetration testing using Pacu, the open-source AWS exploitation framework, to enumerate IAM configurations, discover privilege escalation path… | 2/1 |  |
| `performing-dynamic-analysis-of-android-app` | Performs runtime dynamic analysis of Android applications using Frida, Objection, and Android Debug Bridge to observe application behavior during execution, intercept fu… | 1/1 |  |
| `performing-endpoint-vulnerability-remediation` | Performs vulnerability remediation on endpoints by prioritizing CVEs based on risk scoring, deploying patches, applying configuration changes, and validating fixes. Use… | 1/1 |  |
| `performing-entitlement-review-with-sailpoint-iiq` | Performs entitlement review and access certification campaigns using SailPoint IdentityIQ including manager certifications, targeted entitlement reviews, role-based acce… | 1/1 |  |
| `performing-firmware-extraction-with-binwalk` | Performs firmware image extraction and analysis using binwalk to identify embedded filesystems, compressed archives, bootloaders, kernel images, and cryptographic materi… | 1/1 |  |
| `performing-firmware-malware-analysis` | Analyzes firmware images for embedded malware, backdoors, and unauthorized modifications targeting routers, IoT devices, UEFI/BIOS, and embedded systems. Covers firmware… | 2/1 |  |
| `performing-fuzzing-with-aflplusplus` | Perform coverage-guided fuzzing of compiled binaries using AFL++ (American Fuzzy Lop Plus Plus) to discover memory corruption, crashes, and security vulnerabilities. The… | 2/2 |  |
| `performing-log-source-onboarding-in-siem` | Perform structured log source onboarding into SIEM platforms by configuring collectors, parsers, normalization, and validation for complete security visibility. | 1/1 |  |
| `performing-malware-hash-enrichment-with-virustotal` | Enrich malware file hashes using the VirusTotal API to retrieve detection rates, behavioral analysis, YARA matches, and contextual threat intelligence for incident triag… | 1/1 |  |
| `performing-malware-ioc-extraction` | Malware IOC extraction is the process of analyzing malicious software to identify actionable indicators of compromise including file hashes, network indicators (C2 domai… | 1/1 |  |
| `performing-malware-persistence-investigation` | Systematically investigate all persistence mechanisms on Windows and Linux systems to identify how malware survives reboots and maintains access. | 1/1 |  |
| `performing-malware-triage-with-yara` | Performs rapid malware triage and classification using YARA rules to match file patterns, strings, byte sequences, and structural characteristics against known malware f… | 1/1 |  |
| `performing-memory-forensics-with-volatility3-plugins` | Analyze memory dumps using Volatility3 plugins to detect injected code, rootkits, credential theft, and malware artifacts in Windows, Linux, and macOS memory images. | 2/2 |  |
| `performing-mobile-app-certificate-pinning-bypass` | Bypasses SSL/TLS certificate pinning implementations in Android and iOS applications to enable traffic interception during authorized security assessments. Covers OkHttp… | 2/1 |  |
| `performing-post-quantum-cryptography-migration` | Assesses organizational readiness for post-quantum cryptography migration per NIST FIPS 203/204/205 standards. Performs cryptographic inventory scanning to identify quan… | 1/1 |  |
| `performing-privacy-impact-assessment` | Automates the Privacy Impact Assessment (PIA) workflow including data flow mapping, privacy risk scoring matrices, GDPR Article 35 DPIA and CCPA/CPRA alignment checks, d… | 1/1 |  |
| `performing-privileged-account-access-review` | Conduct systematic reviews of privileged accounts to validate access rights, identify excessive permissions, and enforce least privilege across PAM infrastructure. | 1/1 |  |
| `performing-purple-team-atomic-testing` | Executes Atomic Red Team tests mapped to MITRE ATT&CK techniques, performs coverage gap analysis across the ATT&CK matrix, and runs detection validation loops to measure… | 1/1 |  |
| `performing-purple-team-exercise` | Performs purple team exercises by coordinating red team adversary emulation with blue team detection validation using MITRE ATT&CK-mapped attack scenarios, real-time det… | 2/1 |  |
| `performing-soc-tabletop-exercise` | Performs tabletop exercises for SOC teams simulating security incidents through discussion-based scenarios to test incident response procedures, communication workflows,… | 1/1 |  |
| `performing-ssl-stripping-attack` | Simulates SSL stripping attacks using sslstrip, Bettercap, and mitmproxy in authorized environments to test HSTS enforcement, certificate validation, and HTTPS upgrade m… | 2/2 |  |
| `performing-static-malware-analysis-with-pe-studio` | Performs static analysis of Windows PE (Portable Executable) malware samples using PEStudio to examine file headers, imports, strings, resources, and indicators without… | 1/1 |  |
| `performing-threat-emulation-with-atomic-red-team` | Executes Atomic Red Team tests for MITRE ATT&CK technique validation using the atomic-operator Python framework. Loads test definitions from YAML atomics, runs attack si… | 2/2 |  |
| `performing-threat-hunting-with-elastic-siem` | Performs proactive threat hunting in Elastic Security SIEM using KQL/EQL queries, detection rules, and Timeline investigation to identify threats that evade automated de… | 2/1 |  |
| `performing-threat-hunting-with-yara-rules` | Use YARA pattern-matching rules to hunt for malware, suspicious files, and indicators of compromise across filesystems and memory dumps. Covers rule authoring, yara-pyth… | 2/2 |  |
| `performing-vlan-hopping-attack` | Simulates VLAN hopping attacks using switch spoofing and double tagging techniques in authorized environments to test VLAN segmentation effectiveness and validate switch… | 2/2 |  |
| `performing-yara-rule-development-for-detection` | Develop precise YARA rules for malware detection by identifying unique byte patterns, strings, and behavioral indicators in executable files while minimizing false posit… | 1/1 |  |
| `processing-stix-taxii-feeds` | Processes STIX 2.1 threat intelligence bundles delivered via TAXII 2.1 servers, normalizing objects into platform-native schemas and routing them to appropriate consumin… | 1/1 |  |
| `pwn-chain` | 从逆向走到可用利用 (Working Exploit) 的全链路工程化方法。 适用场景：拿到了二进制 + 漏洞点 + 目标环境，需要写出一个能稳定打通的 exploit（不是只能本地复现一下、远程一打就崩的脚本）。 覆盖三大方向：栈溢出 / 堆利用 / 内核 pwn。强调"CTF 本地通 → 真实远程稳定打通"的工程差距：libc 版本… | 4/2 |  |
| `radare2` | Use this skill whenever the user wants to analyze binaries with radare2/r2 from the command line, including reverse engineering, disassembly, function analysis, strings/… | 4/2 |  |
| `radio-sdr` | Use for authorized RF/SDR security research including signal identification, replay feasibility study in shielded labs, and wireless protocol analysis outside classic Wi… | 4/2 |  |
| `reasonix-code-agent` | Reasonix — DeepSeek 原生 AI 编程代理。支持交互式编码、项目搜索/编辑、子代理委派(4并发)、HTTP+SSE/ACP协议、MCP工具集成、多模型切换(deeseek-flash/deepseek-pro/deepseek-reasoner)。effort=max 模式确保最强推理+全量代码搜索。用于渗透测试代码生… | 1/1 |  |
| `recovering-from-ransomware-attack` | Executes structured recovery from a ransomware incident following NIST and CISA frameworks, including environment isolation, forensic evidence preservation, clean infras… | 1/1 |  |
| `rev-dex-dumper` | Dump DEX files from a running Android app for unpacking/deobfuscation. Activate when the user wants to unpack an Android APK, dump DEX from memory, extract decrypted DEX… | 3/1 |  |
| `rev-frida` | Generate Frida hook scripts using modern Frida API. Activate when the user wants to write Frida scripts, hook functions at runtime, trace calls or arguments or return va… | 3/1 |  |
| `rev-ios-dump` | Dump decrypted iOS app binaries (砸壳) from jailbroken devices using frida-ios-dump. Activate when the user wants to decrypt an iOS app, dump an IPA from a device, or extr… | 3/1 |  |
| `rev-u3d-dump` | Dump Unity IL2CPP symbols from iOS/Android builds. Extract method names, addresses, and type info from IL2CPP binaries and global-metadata.dat, then generate IDA/Ghidra… | 3/1 |  |
| `Reverse Engineering Chain` | 逆向分析类 automated penetration testing chain. 触发词: 逆向分析类。 | 1/1 | 覆寫特徵 |
| `reverse-engineer` | Expert reverse engineer specializing in binary analysis, disassembly, decompilation, and software analysis. Masters IDA Pro, Ghidra, radare2, x64dbg, and modern RE toolc… | 1/1 |  |
| `reverse-engineering` | Provides reverse engineering techniques. Use when the main job is to understand how a compiled, obfuscated, packed, or virtualized target works before exploiting or solv… | 4/3 |  |
| `reverse-engineering-android-malware-with-jadx` | Reverse engineers malicious Android APK files using JADX decompiler to analyze Java/Kotlin source code, identify malicious functionality including data theft, C2 communi… | 2/1 |  |
| `reverse-engineering-dotnet-malware-with-dnspy` | Reverse engineers .NET malware using dnSpy decompiler and debugger to analyze C#/VB.NET source code, identify obfuscation techniques, extract configurations, and underst… | 2/1 |  |
| `reverse-engineering-ios-app-with-frida` | Reverse engineers iOS applications using Frida dynamic instrumentation to understand internal logic, extract encryption keys, bypass security controls, and discover hidd… | 2/1 |  |
| `reverse-engineering-malware-with-ghidra` | Reverse engineers malware binaries using NSA's Ghidra disassembler and decompiler to understand internal logic, cryptographic routines, C2 protocols, and evasion techniq… | 2/1 |  |
| `reverse-engineering-ransomware-encryption-routine` | Reverse engineer ransomware encryption routines to identify cryptographic algorithms, key generation flaws, and potential decryption opportunities using static and dynam… | 2/2 |  |
| `reverse-engineering-rust-malware` | Reverse engineer Rust-compiled malware using IDA Pro and Ghidra with techniques for handling non-null-terminated strings, crate dependency extraction, and Rust-specific… | 2/2 |  |
| `reverse-shell-techniques` | Reverse shell techniques playbook. Use when establishing remote shells including language one-liners, encrypted shells (OpenSSL/socat/ncat), web shells, PTY upgrades, fi… | 1/1 |  |
| `roothawk-lpe` | RootHawk Linux本地提权工具操作技能——集成9个内核级CVE漏洞利用模块，覆盖PwnKit/DirtyPipe/Polkit及6个2026年最新CVE。支持单CVE执行和全量自动攻击(-any模式)。触发词：Linux提权、ROOT提权、本地提权、内核漏洞提权、LPE、DirtyPipe、PwnKit、sudo提权、kern… | 1/1 |  |
| `runtime-hook-&-injection` | Reverse Engineering Chain Phase 10/运行时Hook与注入. 触发词: 运行时Hook与注入。 | 1/1 | 覆寫特徵 |
| `saml-sso-assertion-attacks` | SAML SSO assertion attack playbook. Use when testing signature validation, assertion wrapping, audience restrictions, ACS handling, XML trust boundaries, and enterprise… | 2/2 |  |
| `securing-helm-chart-deployments` | Secure Helm chart deployments by validating chart integrity, scanning templates for misconfigurations, and enforcing security contexts in Kubernetes releases. | 1/1 |  |
| `securing-serverless-functions` | This skill covers security hardening for serverless compute platforms including AWS Lambda, Azure Functions, and Google Cloud Functions. It addresses least privilege IAM… | 2/1 |  |
| `security-audit` | Security guidance and vulnerability review for codebases, APIs, services, CLI tools, libraries, and daemons. Use for security questions, focused reviews, vulnerability r… | 2/2 |  |
| `security-compliance-compliance-check` | You are a compliance expert specializing in regulatory requirements for software systems including GDPR, HIPAA, SOC2, PCI-DSS, and other industry standards. Perform comp… | 1/1 |  |
| `shellcode-analyzer` | Load, unpack, and analyze shellcode in x64dbg. Use this skill when the user wants to analyze shellcode, load a shellcode blob into a debugger, unpack encoded/encrypted s… | 2/2 |  |
| `shellcode-crafting` | Exploit Chain Phase 2/Shellcode编写. 触发词: Shellcode编写。 | 1/1 | 覆寫特徵 |
| `shellcode-encryption-&-encoding` | Evasion Chain Phase 2/Shellcode加密与编码. 触发词: Shellcode加密与编码。 | 1/1 | 覆寫特徵 |
| `stack-overflow-and-rop` | Stack overflow and ROP playbook. Use when exploiting buffer overflows to hijack control flow via return address overwrite, ROP chains, ret2libc, ret2csu, ret2dlresolve,… | 1/1 |  |
| `state-diff` | Compare two state snapshots to identify register and memory changes between two points in time | 2/2 |  |
| `state-snapshot` | Capture a full debuggee state snapshot (all committed memory regions + processor state) to disk for offline analysis | 2/2 |  |
| `static-analysis` | Reverse Engineering Chain Phase 11/静态分析. 触发词: 静态分析。 | 1/1 | 覆寫特徵 |
| `supply-chain-security` | Use for software supply-chain security assessment covering SBOM, SCA, CI/CD pipelines, container images, build integrity, dependency provenance, and vulnerability reacha… | 4/2 |  |
| `symbolic-execution-tools` | Symbolic execution and constraint solving playbook. Use when solving CTF reversing challenges, recovering keys, bypassing checks, or automating binary analysis with angr… | 1/1 |  |
| `testing-ransomware-recovery-procedures` | Test and validate ransomware recovery procedures including backup restore operations, RTO/RPO target verification, recovery sequencing, and clean restore validation to e… | 1/1 |  |
| `thick-client` | Use for authorized security testing of desktop thick clients including local storage, update channels, IPC, traffic, and client-side trust boundaries. | 4/2 |  |
| `threat-hunting` | Use for blue-team threat hunting, detection engineering with Sigma/YARA, SIEM query design, and incident detection validation. | 4/2 |  |
| `threat-intelligence` | Use for authorized OSINT and cyber threat intelligence that enriches IOCs, campaigns, impersonation, scams, or threat actors from public sources. Includes bounded X/Twit… | 3/1 |  |
| `tracealyzer` | Trace execution (into or over calls) for N steps or until a condition, then analyze the recorded instruction log | 2/2 |  |
| `type-juggling` | PHP type juggling and weak comparison (`==`) bypass. Use when authentication, HMAC/signature checks, or token validation uses loose equality, numeric coercion, or hash c… | 2/2 |  |
| `validating-backup-integrity-for-recovery` | Validate backup integrity through cryptographic hash verification, automated restore testing, corruption detection, and recoverability checks to ensure backups are relia… | 1/1 |  |
| `vm-and-bytecode-reverse` | Custom VM and bytecode reverse engineering playbook. Use when CTF challenges or protected software implement custom virtual machines with proprietary bytecode, dispatche… | 1/1 |  |
| `vuln-hunter` | Hunt for vulnerabilities in a running debuggee by analyzing imports/exports, triaging attack surface, and iteratively testing for bugs with PoC generation. | 2/2 |  |
| `wifi-wireless` | Use for authorized wireless security assessment including Wi-Fi capture, WPA handshake analysis, rogue AP detection research, and lab-only deauth testing. | 4/2 |  |
| `win-offensive-dev` | Windows 攻击性安全开发完整知识库 — 涵盖 shellcode 加载、进程注入、API 哈希/IAT 隐藏、syscall 存根、NTDLL unhooking、sleep 混淆、反射加载、BOF、ETW/AMSI 绕过、持久化机制、C2 植入物、Token 操纵、横向移动、UAC 绕过等。当用户讨论 shellcode、注入、… | 1/1 |  |
| `windows-ad` | Use for authorized Active Directory and Windows identity attacks including Kerberos, AD CS, BloodHound paths, NTLM relay, and domain privilege escalation research. | 4/2 |  |
| `windows-av-evasion` | AV/EDR evasion playbook for Windows. Use when bypassing AMSI, ETW, .NET assembly detection, shellcode execution, process injection, API hooking, and signature-based dete… | 1/1 |  |
| `windows-shell-reliability` | Reliable command execution on Windows: paths, encoding, and common binary pitfalls. | 1/1 |  |
| `xiaojianbang-auto-reverse` | Android Native 用户明确许可样本/研究环境下的反检测分析与稳定绕过工程（中文工作语言，宿主机 Windows/Linux/macOS）。分析 .so 的反调试、反 Frida(anti-Frida)、Root、模拟器、完整性/CRC、JNI/constructor/dlopen/匿名 RX 检测链并做 patch 绕过；按… | 1/1 |  |
| `xiaotao-win-flow` | Windows reverse-engineering pipeline. Identifies target type (native/Nuitka/Go/Rust/.NET/Python-bytecode/Java/Electron/Tauri-WebView/Delphi/AutoIt/e-language/packed), ro… | 2/2 |  |
| `yara-sigs` | Scan a state snapshot's memory dumps with YARA signatures to detect packers, crypto constants, malware, and more | 2/2 |  |

### 資安—Windows／AD／身分（56）

| Skill | 說明 | 定義/版本 | 旗標 |
|---|---|---:|---|
| `active-directory-acl-abuse` | Active Directory ACL abuse playbook. Use when exploiting misconfigured AD permissions including GenericAll, WriteDACL, DCSync rights, shadow credentials, LAPS reading, G… | 1/1 |  |
| `active-directory-attack` | 内网域攻击:BloodHound,Kerberoast,ADCS ESC1/ESC8,NTLM Relay,Coerce,DACL,DCSync,Zerologon/NoPac/PrintNightmare,mitm6,LLMNR,Linux内网。Use when attacking Active Directory, ADCS, NT… | 1/1 |  |
| `active-directory-attacks` | Provide comprehensive techniques for attacking Microsoft Active Directory environments. Covers reconnaissance, credential harvesting, Kerberos attacks, lateral movement,… | 1/1 |  |
| `active-directory-certificate-services` | AD Certificate Services attack playbook. Use when targeting misconfigured AD CS for privilege escalation via ESC1-ESC13 template abuse, NTLM relay to enrollment, CA offi… | 1/1 |  |
| `active-directory-kerberos-attacks` | Kerberos attack playbook for Active Directory. Use when targeting AD authentication via AS-REP roasting, Kerberoasting, golden/silver/diamond tickets, delegation abuse,… | 1/1 |  |
| `analyzing-active-directory-acl-abuse` | Detect dangerous ACL misconfigurations in Active Directory using ldap3 to identify GenericAll, WriteDACL, and WriteOwner abuse paths | 1/1 |  |
| `analyzing-windows-event-logs-in-splunk` | Analyzes Windows Security, System, and Sysmon event logs in Splunk to detect authentication attacks, privilege escalation, persistence mechanisms, and lateral movement u… | 1/1 |  |
| `auditing-azure-active-directory-configuration` | Auditing Microsoft Entra ID (Azure Active Directory) configuration to identify risky authentication policies, overly permissive role assignments, stale accounts, conditi… | 1/1 |  |
| `cloud-key-&-credential-attacks` | Cloud Attack Chain Phase 8/云密钥与凭证攻击. 触发词: 云密钥与凭证攻击。 | 1/1 | 覆寫特徵 |
| `conducting-domain-persistence-with-dcsync` | Perform DCSync attacks to replicate Active Directory credentials and establish domain persistence by extracting KRBTGT, Domain Admin, and service account hashes for Gold… | 2/2 |  |
| `conducting-internal-reconnaissance-with-bloodhound-ce` | Conduct internal Active Directory reconnaissance using BloodHound Community Edition to map attack paths, identify privilege escalation chains, and discover misconfigurat… | 1/1 |  |
| `conducting-pass-the-ticket-attack` | Pass-the-Ticket (PtT) is a lateral movement technique that uses stolen Kerberos tickets (TGT or TGS) to authenticate to services without knowing the user's password. By… | 2/2 |  |
| `configuring-active-directory-tiered-model` | Implement Microsoft's Enhanced Security Admin Environment (ESAE) tiered administration model for Active Directory. Covers Tier 0/1/2 separation, privileged access workst… | 1/1 |  |
| `configuring-ldap-security-hardening` | Harden LDAP directory services against common attacks including credential harvesting, LDAP injection, anonymous binding, and channel binding bypass. Covers LDAPS enforc… | 1/1 |  |
| `credential-spraying` | Credential Breach Chain Phase 5/凭证喷洒. 触发词: 凭证喷洒。 | 1/1 | 覆寫特徵 |
| `detecting-azure-lateral-movement` | Detect lateral movement in Azure AD/Entra ID environments using Microsoft Graph API audit logs, Azure Sentinel KQL hunting queries, and sign-in anomaly correlation to id… | 2/2 |  |
| `detecting-credential-dumping-techniques` | Detect LSASS credential dumping, SAM database extraction, and NTDS.dit theft using Sysmon Event ID 10, Windows Security logs, and SIEM correlation rules | 2/2 |  |
| `detecting-credential-dumping-with-edr` | Detect OS credential dumping techniques including LSASS access, SAM extraction, and DCSync using EDR telemetry and Sysmon logs. | 1/1 |  |
| `detecting-dcsync-attack-in-active-directory` | Detect DCSync attacks where adversaries abuse Active Directory replication privileges to extract password hashes by monitoring for non-domain-controller accounts request… | 2/1 |  |
| `detecting-golden-ticket-attacks` | Detect Kerberos golden ticket attacks by analyzing Windows Security event logs for anomalous TGT usage patterns. Parses Event IDs 4624, 4672, and 4768 from EVTX files to… | 1/1 |  |
| `detecting-golden-ticket-attacks-in-kerberos-logs` | Detect Golden Ticket attacks in Active Directory by analyzing Kerberos TGT anomalies including mismatched encryption types, impossible ticket lifetimes, non-existent acc… | 2/1 |  |
| `detecting-golden-ticket-forgery` | Detect Kerberos Golden Ticket forgery by analyzing Windows Event ID 4769 for RC4 encryption downgrades (0x17), abnormal ticket lifetimes, and krbtgt account anomalies in… | 2/2 |  |
| `detecting-kerberoasting-attacks` | Detect Kerberoasting attacks by monitoring for anomalous Kerberos TGS requests targeting service accounts with SPNs for offline password cracking. | 2/1 |  |
| `detecting-lateral-movement-with-zeek` | Detect lateral movement in network traffic using Zeek (formerly Bro) log analysis. Parses conn.log, smb_mapping.log, smb_files.log, dce_rpc.log, kerberos.log, and ntlm.l… | 1/1 |  |
| `detecting-pass-the-hash-attacks` | Detect Pass-the-Hash attacks by analyzing NTLM authentication patterns, identifying Type 3 logons with NTLM where Kerberos is expected, and correlating with credential d… | 2/1 |  |
| `detecting-pass-the-ticket-attacks` | Detect Kerberos Pass-the-Ticket (PtT) attacks by analyzing Windows Event IDs 4768, 4769, and 4771 for anomalous ticket usage patterns in Splunk and Elastic SIEM | 2/2 |  |
| `detecting-ransomware-precursors-in-network` | Detects early-stage ransomware indicators in network traffic before encryption begins, including initial access broker activity, command-and-control beaconing, credentia… | 1/1 |  |
| `detecting-t1003-credential-dumping-with-edr` | Detect OS credential dumping techniques targeting LSASS memory, SAM database, NTDS.dit, and cached credentials using EDR telemetry, Sysmon process access monitoring, and… | 1/1 |  |
| `executing-active-directory-attack-simulation` | Executes authorized attack simulations against Active Directory environments to identify misconfigurations, weak credentials, dangerous privilege paths, and exploitable… | 2/1 |  |
| `exploiting-active-directory-certificate-services-esc1` | Exploit misconfigured Active Directory Certificate Services (AD CS) ESC1 vulnerability to request certificates as high-privileged users and escalate domain privileges du… | 2/2 |  |
| `exploiting-active-directory-with-bloodhound` | BloodHound is a graph-based Active Directory reconnaissance tool that uses graph theory to reveal hidden and unintended relationships within AD environments. Red teams u… | 2/2 |  |
| `exploiting-constrained-delegation-abuse` | Exploit Kerberos Constrained Delegation misconfigurations in Active Directory to impersonate privileged users via S4U2self and S4U2proxy extensions for lateral movement… | 2/2 |  |
| `exploiting-kerberoasting-with-impacket` | Perform Kerberoasting attacks using Impacket's GetUserSPNs to extract and crack Kerberos TGS tickets for Active Directory service accounts. | 2/2 |  |
| `exploiting-nopac-cve-2021-42278-42287` | Exploit the noPac vulnerability chain (CVE-2021-42278 sAMAccountName spoofing and CVE-2021-42287 KDC PAC confusion) to escalate from standard domain user to Domain Admin… | 2/2 |  |
| `exploiting-zerologon-vulnerability-cve-2020-1472` | Exploit the Zerologon vulnerability (CVE-2020-1472) in the Netlogon Remote Protocol to achieve domain controller compromise by resetting the machine account password to… | 2/2 |  |
| `extracting-credentials-from-memory-dump` | Extract cached credentials, password hashes, Kerberos tickets, and authentication tokens from memory dumps using Volatility and Mimikatz for forensic investigation. | 2/1 |  |
| `hunting-for-ntlm-relay-attacks` | Detect NTLM relay attacks by analyzing Windows Event 4624 logon type 3 with NTLMSSP authentication, identifying IP-to-hostname mismatches, Responder traffic signatures,… | 1/1 |  |
| `implementing-passwordless-auth-with-microsoft-entra` | Implements passwordless authentication using Microsoft Entra ID with FIDO2 security keys, Windows Hello for Business, Microsoft Authenticator passkeys, and certificate-b… | 1/1 |  |
| `ldap-injection-testing` | LDAP注入深度测试技能：认证绕过、信息枚举、盲注、RCE（Log4Shell类JNDI）、LDAP过滤器注入、Active Directory攻击 | 1/1 |  |
| `ldap-query-&-enumeration` | Domain Infiltration Chain Phase 6/LDAP查询与枚举. 触发词: LDAP查询与枚举。 | 1/1 | 覆寫特徵 |
| `network-penetration-testing` | 网络渗透测试深度专业技能：内外网渗透全流程、AD域渗透与攻击链、隧道代理与横向移动、协议攻击与利用、从信息收集到域控接管完整攻击链 | 1/1 |  |
| `ntlm-relay-attacks` | Domain Infiltration Chain Phase 7/NTLM中继攻击. 触发词: NTLM中继攻击。 | 1/1 | 覆寫特徵 |
| `pass-the-hash/ticket` | Domain Infiltration Chain Phase 10/哈希传递与票据传递. 触发词: 哈希传递与票据传递。 | 1/1 | 覆寫特徵 |
| `pentest-active-directory` | Assess Active Directory identity attack paths including roasting, relay, and delegation abuse. | 1/1 |  |
| `pentest-priv-escalation` | Assess Linux and Windows privilege escalation vectors from existing authorized footholds. | 1/1 |  |
| `performing-active-directory-bloodhound-analysis` | Use BloodHound and SharpHound to enumerate Active Directory relationships and identify attack paths from compromised users to Domain Admin. | 1/1 |  |
| `performing-active-directory-compromise-investigation` | Investigate Active Directory compromise by analyzing authentication logs, replication metadata, Group Policy changes, and Kerberos ticket anomalies to identify attacker… | 1/1 |  |
| `performing-active-directory-forest-trust-attack` | Enumerate and audit Active Directory forest trust relationships using impacket for SID filtering analysis, trust key extraction, cross-forest SID history abuse detection… | 1/1 |  |
| `performing-active-directory-penetration-test` | Conduct a focused Active Directory penetration test to enumerate domain objects, discover attack paths with BloodHound, exploit Kerberos weaknesses, escalate privileges… | 2/2 |  |
| `performing-active-directory-vulnerability-assessment` | Assess Active Directory security posture using PingCastle, BloodHound, and Purple Knight to identify misconfigurations, privilege escalation paths, and attack vectors. | 1/1 |  |
| `performing-kerberoasting-attack` | Kerberoasting is a post-exploitation technique that targets service accounts in Active Directory by requesting Kerberos TGS (Ticket Granting Service) tickets for account… | 2/2 |  |
| `performing-lateral-movement-detection` | Detects lateral movement techniques including Pass-the-Hash, PsExec, WMI execution, RDP pivoting, and SMB-based spreading using SIEM correlation of Windows event logs, n… | 2/1 |  |
| `performing-service-account-audit` | Audit service accounts across enterprise infrastructure to identify orphaned, over-privileged, and non-compliant accounts. This skill covers discovery of service account… | 1/1 |  |
| `php-ldap-audit` | PHP Web 源码 LDAP 注入审计工具。识别用户可控数据进入 LDAP filter/DN 构造并被 ldap_search/ldap_read 执行，输出可利用性分级、PoC 与修复建议（禁止省略）。 | 1/1 |  |
| `windows-lateral-movement` | Windows lateral movement playbook. Use when pivoting between Windows hosts via PsExec, WMI, WinRM, DCOM, RDP, pass-the-hash, overpass-the-hash, or pass-the-ticket techni… | 1/1 |  |
| `windows-service-exploitation` | Windows service vulnerabilities including unquoted service paths, weak permissions, DLL hijacking, and service configuration errors | 1/1 |  |

### 資安—網路／無線／協定（150）

| Skill | 說明 | 定義/版本 | 旗標 |
|---|---|---:|---|
| `401-403-bypass-techniques` | 401/403 bypass playbook. Use when encountering access-denied responses on admin panels, API endpoints, or restricted paths. Covers path manipulation, HTTP method tamperi… | 1/1 |  |
| `analyzing-cobalt-strike-malleable-profiles` | Parses Cobalt Strike malleable C2 profiles using pyMalleableC2 to extract beacon configuration, HTTP communication patterns, and sleep/jitter settings. Combines with JAR… | 1/1 |  |
| `analyzing-cobaltstrike-malleable-c2-profiles` | Parse and analyze Cobalt Strike Malleable C2 profiles using dissect.cobaltstrike and pyMalleableC2 to extract C2 indicators, detect evasion techniques, and generate netw… | 2/2 |  |
| `analyzing-dns-logs-for-exfiltration` | Analyzes DNS query logs to detect data exfiltration via DNS tunneling, DGA domain communication, and covert C2 channels using entropy analysis, query volume anomalies, a… | 1/1 |  |
| `analyzing-malicious-url-with-urlscan` | URLScan.io is a free service for scanning and analyzing suspicious URLs. It captures screenshots, DOM content, HTTP transactions, JavaScript behavior, and network connec… | 1/1 |  |
| `analyzing-memory-forensics-with-lime-and-volatility` | Performs Linux memory acquisition using LiME (Linux Memory Extractor) kernel module and analysis with Volatility 3 framework. Extracts process lists, network connections… | 2/2 |  |
| `analyzing-network-flow-data-with-netflow` | Parse NetFlow v9 and IPFIX records to detect volumetric anomalies, port scanning, data exfiltration, and C2 beaconing patterns. Uses the Python netflow library to decode… | 1/1 |  |
| `analyzing-network-packets-with-scapy` | Craft, send, sniff, and dissect network packets using Scapy for protocol analysis, network reconnaissance, and traffic anomaly detection in authorized security testing | 1/1 |  |
| `analyzing-network-traffic-for-incidents` | Analyzes network traffic captures and flow data to identify adversary activity during security incidents, including command-and-control communications, lateral movement,… | 1/1 |  |
| `analyzing-network-traffic-with-wireshark` | Captures and analyzes network packet data using Wireshark and tshark to identify malicious traffic patterns, diagnose protocol issues, extract artifacts, and support inc… | 1/1 |  |
| `analyzing-ransomware-network-indicators` | Identify ransomware network indicators including C2 beaconing patterns, TOR exit node connections, data exfiltration flows, and encryption key exchange via Zeek conn.log… | 2/2 |  |
| `analyzing-typosquatting-domains-with-dnstwist` | Detect typosquatting, homograph phishing, and brand impersonation domains using dnstwist to generate domain permutations and identify registered lookalike domains target… | 2/2 |  |
| `analyzing-windows-shellbag-artifacts` | Analyze Windows Shellbag registry artifacts to reconstruct folder browsing activity, detect access to removable media and network shares, and establish user interaction… | 1/1 |  |
| `arp/dns-spoofing` | Network Control Chain Phase 1/ARP-DNS欺骗. 触发词: ARP-DNS欺骗。 | 1/1 | 覆寫特徵 |
| `attack-surface-recon` | 侦察/攻击面测绘:被动whois/amass/crt.sh/FOFA/Shodan,主动subfinder/httpx/naabu/katana/nuclei,DNS地域/CDN/Nginx catch-all/宝塔/UniApp指纹。开局第一动作,认知写入项目黑板。Use when starting recon, asset mapp… | 1/1 |  |
| `bluetooth-&-nfc-attacks` | Network Control Chain Phase 10/蓝牙与NFC攻击. 触发词: 蓝牙与NFC攻击。 | 1/1 | 覆寫特徵 |
| `building-adversary-infrastructure-tracking-system` | Build an automated system to track adversary infrastructure using passive DNS, certificate transparency, WHOIS data, and IP enrichment to map and monitor threat actor co… | 2/2 |  |
| `collecting-indicators-of-compromise` | Systematically collects, categorizes, and distributes indicators of compromise (IOCs) during and after security incidents to enable detection, blocking, and threat intel… | 2/1 |  |
| `collecting-volatile-evidence-from-compromised-host` | Collect volatile forensic evidence from a compromised system following order of volatility, preserving memory, network connections, processes, and system state before th… | 1/1 |  |
| `conducting-external-reconnaissance-with-osint` | Conducts external reconnaissance using Open Source Intelligence (OSINT) techniques to map an organization's external attack surface without directly interacting with tar… | 1/1 |  |
| `conducting-internal-network-penetration-test` | Execute an internal network penetration test simulating an insider threat or post-breach attacker to identify lateral movement paths, privilege escalation vectors, and s… | 1/1 |  |
| `conducting-network-penetration-test` | Conducts comprehensive network penetration tests against authorized target environments by performing host discovery, port scanning, service enumeration, vulnerability i… | 2/1 |  |
| `conducting-spearphishing-simulation-campaign` | Spearphishing simulation is a targeted social engineering attack vector used by red teams to gain initial access. Unlike broad phishing campaigns, spearphishing uses OSI… | 2/2 |  |
| `conducting-wireless-network-penetration-test` | Conducts authorized wireless network penetration tests to assess the security of WiFi infrastructure by testing for weak encryption protocols, captive portal bypasses, e… | 1/1 |  |
| `configuring-network-segmentation-with-vlans` | Designs and implements VLAN-based network segmentation on managed switches to isolate network zones, enforce access control between segments, and reduce the attack surfa… | 1/1 |  |
| `configuring-pfsense-firewall-rules` | Configures pfSense firewall rules, NAT policies, VPN tunnels, and traffic shaping to enforce network segmentation, control traffic flow, and protect internal network zon… | 1/1 |  |
| `configuring-snort-ids-for-intrusion-detection` | Installs, configures, and tunes Snort 3 intrusion detection system to monitor network traffic for malicious activity using custom and community rulesets, preprocessors,… | 1/1 |  |
| `configuring-suricata-for-network-monitoring` | Deploys and configures Suricata IDS/IPS with Emerging Threats rulesets, EVE JSON logging, and custom rules for real-time network traffic inspection, threat detection, an… | 1/1 |  |
| `configuring-tls-1-3-for-secure-communications` | TLS 1.3 (RFC 8446) is the latest version of the Transport Layer Security protocol, providing significant improvements over TLS 1.2 in both security and performance. It r… | 1/1 |  |
| `configuring-zscaler-private-access-for-ztna` | Configuring Zscaler Private Access (ZPA) to replace traditional VPN with zero trust network access by deploying App Connectors, defining application segments, configurin… | 1/1 |  |
| `containing-active-breach` | Executes containment strategies to stop active adversary operations and prevent lateral movement during a confirmed security breach. Implements short-term and long-term… | 1/1 |  |
| `correlating-security-events-in-qradar` | Correlates security events in IBM QRadar SIEM using AQL (Ariel Query Language), custom rules, building blocks, and offense management to detect multi-stage attacks acros… | 1/1 |  |
| `csm-dns-enumeration` | DNS枚举 — 信息搜集模块 \| Reconnaissance \| 难度★★ \| PTES框架 | 1/1 |  |
| `csm-iot-security-ble-zigbee-z-wave` | BLE/Zigbee/Z-Wave无线安全测试 — 物联网安全模块 \| IoT Security \| 难度★★★★ \| PTES框架 | 1/1 |  |
| `csm-wireless-security-wi-fi` | Wi-Fi安全审计 — 无线安全模块 \| Wireless Security \| 难度★★★ \| PTES框架 | 1/1 |  |
| `ctf-ai-ml` | Provides AI and machine learning techniques for CTF challenges. Use when attacking ML models, crafting adversarial examples, performing model extraction, prompt injectio… | 1/1 | 覆寫特徵 |
| `defi-attack-patterns` | DeFi attack pattern playbook. Use when analyzing flash loan attacks, price oracle manipulation, MEV sandwich attacks, governance exploits, bridge vulnerabilities, and to… | 1/1 |  |
| `deploying-palo-alto-prisma-access-zero-trust` | Deploying Palo Alto Networks Prisma Access for SASE-based zero trust network access using GlobalProtect agents, ZTNA Connectors, security policy enforcement, and integra… | 1/1 |  |
| `detecting-arp-poisoning-in-network-traffic` | Detect and prevent ARP spoofing attacks using ARPWatch, Dynamic ARP Inspection, Wireshark analysis, and custom monitoring scripts to protect against man-in-the-middle in… | 1/1 |  |
| `detecting-attacks-on-historian-servers` | Detect cyber attacks targeting OT historian servers (OSIsoft PI, Ignition, Wonderware) that sit at the IT/OT boundary and serve as pivot points for lateral movement betw… | 1/1 |  |
| `detecting-attacks-on-scada-systems` | This skill covers detecting cyber attacks targeting Supervisory Control and Data Acquisition (SCADA) systems including man-in-the-middle attacks on industrial protocols,… | 1/1 |  |
| `detecting-cloud-cryptomining-activity` | Detecting unauthorized cryptocurrency mining activity in cloud environments by analyzing compute usage anomalies, network traffic to mining pools, GuardDuty findings, an… | 1/1 |  |
| `detecting-cryptomining-in-cloud` | This skill teaches security teams how to detect and respond to unauthorized cryptocurrency mining operations in cloud environments. It covers identifying cryptomining in… | 1/1 |  |
| `detecting-dns-exfiltration-with-dns-query-analysis` | Detect data exfiltration through DNS tunneling by analyzing query entropy, subdomain length, query volume, TXT record abuse, and response payload sizes using passive DNS… | 1/1 |  |
| `detecting-exfiltration-over-dns-with-zeek` | Detect DNS-based data exfiltration by analyzing Zeek dns.log for high-entropy subdomains and anomalous query patterns | 1/1 |  |
| `detecting-lateral-movement-in-network` | Identifies lateral movement techniques in enterprise networks by analyzing authentication logs, network flows, SMB traffic, and RDP sessions using Zeek, Velociraptor, an… | 2/1 |  |
| `detecting-lateral-movement-with-splunk` | Detect adversary lateral movement across networks using Splunk SPL queries against Windows authentication logs, SMB traffic, and remote service abuse. | 2/1 |  |
| `detecting-modbus-command-injection-attacks` | Detect command injection attacks against Modbus TCP/RTU protocol in ICS environments by monitoring for unauthorized write operations, anomalous function codes, malformed… | 1/1 |  |
| `detecting-network-anomalies-with-zeek` | Deploys and configures Zeek (formerly Bro) network security monitor to passively analyze network traffic, generate structured logs, detect anomalous behavior, and create… | 1/1 |  |
| `detecting-network-scanning-with-ids-signatures` | Detect network reconnaissance and port scanning using Suricata and Snort IDS signatures, threshold-based detection rules, and traffic anomaly analysis to identify Nmap,… | 1/1 |  |
| `detecting-port-scanning-with-fail2ban` | Configures Fail2ban with custom filters and actions to detect port scanning activity, SSH brute force attempts, and network reconnaissance, automatically banning offendi… | 1/1 |  |
| `detecting-spearphishing-with-email-gateway` | Spearphishing targets specific individuals using personalized, researched content that bypasses generic spam filters. Email security gateways (SEGs) like Microsoft Defen… | 1/1 |  |
| `device-&-protocol-exploitation` | Exploit Chain Phase 12/设备与协议利用. 触发词: 设备与协议利用。 | 1/1 | 覆寫特徵 |
| `dhcp-attacks` | Network Control Chain Phase 2/DHCP攻击. 触发词: DHCP攻击。 | 1/1 | 覆寫特徵 |
| `dns-tunneling` | Exfiltration Chain Phase 2/DNS隧道渗出. 触发词: DNS隧道渗出。 | 1/1 | 覆寫特徵 |
| `exploiting-ipv6-vulnerabilities` | Identifies and exploits IPv6-specific vulnerabilities including SLAAC spoofing, Router Advertisement flooding, and IPv6 tunneling during authorized assessments to test d… | 2/1 |  |
| `exploiting-race-condition-vulnerabilities` | Detect and exploit race condition vulnerabilities in web applications using Turbo Intruder's single-packet attack technique to bypass rate limits, duplicate transactions… | 2/2 |  |
| `exploiting-smb-vulnerabilities-with-metasploit` | Identifies and exploits SMB protocol vulnerabilities using Metasploit Framework during authorized penetration tests to demonstrate risks from unpatched Windows systems,… | 2/1 |  |
| `hack-scanner` | Run the bundled Hack Scanner for URL, domain, API, network, and source-code security analysis, using its MCP server or Python CLI and producing structured vulnerability… | 1/1 |  |
| `http/https-tunneling` | Exfiltration Chain Phase 3/HTTP-HTTPS隧道. 触发词: HTTP-HTTPS隧道。 | 1/1 | 覆寫特徵 |
| `hunting-for-beaconing-with-frequency-analysis` | Identify command-and-control beaconing patterns in network traffic by applying statistical frequency analysis, jitter calculation, and coefficient of variation scoring t… | 2/1 |  |
| `hunting-for-cobalt-strike-beacons` | Detect Cobalt Strike beacon network activity using default TLS certificate signatures (serial 8BB00EE), JA3/JA3S/JARM fingerprints, HTTP C2 profile pattern matching, bea… | 2/2 |  |
| `hunting-for-command-and-control-beaconing` | Detect C2 beaconing patterns in network traffic using frequency analysis, jitter detection, and domain reputation to identify compromised endpoints communicating with ad… | 2/1 |  |
| `hunting-for-dns-based-persistence` | Hunt for DNS-based persistence mechanisms including DNS hijacking, dangling CNAME records, wildcard DNS abuse, and unauthorized zone modifications using passive DNS data… | 1/1 |  |
| `hunting-for-dns-tunneling-with-zeek` | Detect DNS tunneling and data exfiltration by analyzing Zeek dns.log for high-entropy subdomain queries, excessive query volume, long query lengths, and unusual DNS reco… | 1/1 |  |
| `hunting-for-spearphishing-indicators` | Hunt for spearphishing campaign indicators across email logs, endpoint telemetry, and network data to detect targeted email attacks. | 1/1 |  |
| `hunting-for-unusual-network-connections` | Hunt for unusual network connections by analyzing outbound traffic patterns, rare destinations, non-standard ports, and anomalous connection frequencies from endpoints. | 1/1 |  |
| `icmp-tunneling` | Exfiltration Chain Phase 4/ICMP隧道. 触发词: ICMP隧道。 | 1/1 | 覆寫特徵 |
| `implementing-beyondcorp-zero-trust-access-model` | Implementing Google's BeyondCorp zero trust access model to eliminate implicit trust from the network perimeter, enforce identity-aware access controls using IAP, Access… | 1/1 |  |
| `implementing-cisa-zero-trust-maturity-model` | Implement the CISA Zero Trust Maturity Model v2.0 across the five pillars of identity, devices, networks, applications, and data to achieve progressive organizational ze… | 1/1 |  |
| `implementing-conduit-security-for-ot-remote-access` | Implement secure conduit architecture for OT remote access following IEC 62443 zones and conduits model, deploying jump servers, MFA-enabled gateways, session recording,… | 1/1 |  |
| `implementing-gcp-vpc-firewall-rules` | Implementing and auditing GCP VPC firewall rules to enforce network segmentation, restrict ingress and egress traffic, apply hierarchical firewall policies across the or… | 1/1 |  |
| `implementing-honeypot-for-ransomware-detection` | Deploys canary files, honeypot shares, and decoy systems to detect ransomware activity at the earliest possible stage. Configures canary tokens embedded in strategic fil… | 2/1 |  |
| `implementing-ics-firewall-with-tofino` | Deploy and configure Tofino industrial firewalls from Belden/Hirschmann to protect SCADA systems and PLCs using deep packet inspection for OT protocols including Modbus,… | 1/1 |  |
| `implementing-mimecast-targeted-attack-protection` | Deploy Mimecast Targeted Threat Protection including URL Protect, Attachment Protect, Impersonation Protect, and Internal Email Protect to defend against advanced phishi… | 1/1 |  |
| `implementing-network-access-control` | Implements 802.1X port-based network access control using RADIUS authentication, PacketFence NAC, and switch configurations to enforce identity-based access policies, po… | 1/1 |  |
| `implementing-network-access-control-with-cisco-ise` | Deploy Cisco Identity Services Engine for 802.1X wired and wireless authentication, MAC Authentication Bypass, posture assessment, and dynamic VLAN assignment for networ… | 1/1 |  |
| `implementing-network-deception-with-honeypots` | Deploy and manage network honeypots using OpenCanary, T-Pot, or Cowrie to detect unauthorized access, lateral movement, and attacker reconnaissance. | 1/1 |  |
| `implementing-network-intrusion-prevention-with-suricata` | Deploy and configure Suricata as a network intrusion prevention system with custom rules, Emerging Threats rulesets, and inline traffic inspection for real-time threat b… | 1/1 |  |
| `implementing-network-segmentation-with-firewall-zones` | Design and implement network segmentation using firewall security zones, VLANs, ACLs, and microsegmentation policies to restrict lateral movement and enforce least-privi… | 1/1 |  |
| `implementing-network-traffic-analysis-with-arkime` | Deploy and query Arkime (formerly Moloch) for full packet capture network traffic analysis. Uses the Arkime API v3 to search sessions, download PCAPs, analyze connection… | 1/1 |  |
| `implementing-next-generation-firewall-with-palo-alto` | Configure and deploy Palo Alto Networks next-generation firewalls with App-ID, User-ID, zone-based policies, SSL decryption, and threat prevention profiles for enterpris… | 1/1 |  |
| `implementing-osquery-for-endpoint-monitoring` | Deploy osquery scheduled queries for continuous endpoint monitoring covering process inventory, network connections, file integrity, and persistence mechanisms. Generate… | 1/1 |  |
| `implementing-purdue-model-network-segmentation` | Implement network segmentation based on the Purdue Enterprise Reference Architecture (PERA) model to separate industrial control system networks into hierarchical securi… | 1/1 |  |
| `implementing-scim-provisioning-with-okta` | Implement automated user provisioning and deprovisioning using SCIM 2.0 protocol with Okta as the identity provider. | 1/1 |  |
| `implementing-siem-correlation-rules-for-apt` | Write multi-event correlation rules that detect APT lateral movement by chaining Windows authentication events, process execution telemetry, and network connection logs… | 1/1 |  |
| `implementing-taxii-server-with-opentaxii` | Deploy and configure an OpenTAXII server to share and consume STIX-formatted cyber threat intelligence using the TAXII 2.1 protocol for automated indicator exchange betw… | 1/1 |  |
| `implementing-vulnerability-management-with-greenbone` | Deploy and operate Greenbone/OpenVAS vulnerability management using the python-gvm library to create scan targets, execute vulnerability scans, and parse scan reports vi… | 1/1 |  |
| `implementing-zero-trust-dns-with-nextdns` | Implement NextDNS as a zero trust DNS filtering layer with encrypted resolution, threat intelligence blocking, privacy protection, and organizational policy enforcement… | 1/1 |  |
| `implementing-zero-trust-network-access` | Implementing Zero Trust Network Access (ZTNA) in cloud environments by configuring identity-aware proxies, micro-segmentation, continuous verification with conditional a… | 1/1 |  |
| `implementing-zero-trust-network-access-with-zscaler` | Implementing Zero Trust Network Access With Zscaler | 1/1 |  |
| `k8s-security-policies` | Comprehensive guide for implementing NetworkPolicy, PodSecurityPolicy, RBAC, and Pod Security Standards in Kubernetes. | 1/1 |  |
| `linux-lateral-movement` | Linux lateral movement playbook. Use after gaining initial access to pivot across Linux hosts via SSH hijacking, credential harvesting, internal pivoting, D-Bus exploita… | 1/1 |  |
| `mobile-network-layer-attack` | Mobile Attack Chain Phase 7/移动网络层攻击. 触发词: 移动网络层攻击。 | 1/1 | 覆寫特徵 |
| `mobile-traffic-analysis-&-capture` | Mobile Attack Chain Phase 5/移动流量分析与抓包. 触发词: 移动流量分析与抓包。 | 1/1 | 覆寫特徵 |
| `Network Control Chain` | 网络中间人类 automated penetration testing chain. 触发词: 网络中间人类。 | 1/1 | 覆寫特徵 |
| `network-analysis` | — | 1/1 |  |
| `network-forensics` | 网络取证技术，包括Wireshark分析、tcpdump使用、攻击模式识别、PCAP分析和流量日志分析 | 1/1 |  |
| `network-protocol-attacks` | Network protocol attack playbook. Use when exploiting layer 2/3 protocols including ARP spoofing, LLMNR/NBT-NS/mDNS poisoning, WPAD abuse, DHCPv6 attacks, VLAN hopping,… | 1/1 |  |
| `packet-capture-&-protocol-analysis` | Network Control Chain Phase 7/抓包与协议分析. 触发词: 抓包与协议分析。 | 1/1 | 覆寫特徵 |
| `pentest-commands` | Provide a comprehensive command reference for penetration testing tools including network scanning, exploitation, password cracking, and web application testing. Enable… | 1/1 |  |
| `pentest-network-exploiter` | Run controlled exploitation against confirmed vulnerabilities while enforcing scope and authorization gates. | 1/1 |  |
| `pentest-network-scanner` | Actively enumerate in-scope hosts and services, then produce normalized network mapping artifacts. | 1/1 |  |
| `pentest-wireless-attacker` | Evaluate authorized wireless networks for handshake, PMKID, rogue AP, and enterprise auth weaknesses. | 1/1 |  |
| `performing-bandwidth-throttling-attack-simulation` | Simulates bandwidth throttling and network degradation attacks using tc, iperf3, and Scapy in authorized environments to test quality-of-service controls, application re… | 1/1 |  |
| `performing-bluetooth-security-assessment` | Assess Bluetooth Low Energy device security by scanning, enumerating GATT services, and detecting vulnerabilities | 1/1 |  |
| `performing-cloud-native-forensics-with-falco` | Uses Falco YAML rules for runtime threat detection in containers and Kubernetes, monitoring syscalls for shell spawns, file tampering, network anomalies, and privilege e… | 1/1 |  |
| `performing-cryptographic-audit-of-application` | A cryptographic audit systematically reviews an application's use of cryptographic primitives, protocols, and key management to identify vulnerabilities such as weak alg… | 1/1 |  |
| `performing-deception-technology-deployment` | Deploys deception technology including honeypots, honeytokens, and decoy systems to detect attackers who have bypassed perimeter defenses, providing high-fidelity alerts… | 1/1 |  |
| `performing-dns-enumeration-and-zone-transfer` | Enumerates DNS records, attempts zone transfers, brute-forces subdomains, and maps DNS infrastructure during authorized reconnaissance to identify attack surface, miscon… | 2/1 |  |
| `performing-dns-tunneling-detection` | Detects DNS tunneling by computing Shannon entropy of DNS query names, analyzing query length distributions, inspecting TXT record payloads, and identifying high subdoma… | 1/1 |  |
| `performing-external-network-penetration-test` | Conduct a comprehensive external network penetration test to identify vulnerabilities in internet-facing infrastructure using PTES methodology, reconnaissance, scanning,… | 1/1 |  |
| `performing-iot-security-assessment` | Performs comprehensive security assessments of IoT devices and their ecosystems by testing hardware interfaces, firmware, network communications, cloud APIs, and compani… | 1/1 |  |
| `performing-kubernetes-etcd-security-assessment` | Assess the security posture of Kubernetes etcd clusters by evaluating encryption at rest, TLS configuration, access controls, backup encryption, and network isolation. | 1/1 |  |
| `performing-kubernetes-penetration-testing` | Kubernetes penetration testing systematically evaluates cluster security by simulating attacker techniques against the API server, kubelet, etcd, pods, RBAC, network pol… | 2/2 |  |
| `performing-lateral-movement-with-wmiexec` | Perform lateral movement across Windows networks using WMI-based remote execution techniques including Impacket wmiexec.py, CrackMapExec, and native WMI commands for ste… | 2/2 |  |
| `performing-memory-forensics-with-volatility3` | Analyze volatile memory dumps using Volatility 3 to extract running processes, network connections, loaded modules, and evidence of malicious activity. | 2/1 |  |
| `performing-network-forensics-with-wireshark` | Capture and analyze network traffic using Wireshark and tshark to reconstruct network events, extract artifacts, and identify malicious communications. | 2/1 |  |
| `performing-network-packet-capture-analysis` | Perform forensic analysis of network packet captures (PCAP/PCAPNG) using Wireshark, tshark, and tcpdump to reconstruct network communications, extract transferred files,… | 1/1 |  |
| `performing-network-traffic-analysis-with-tshark` | Automate network traffic analysis using tshark and pyshark for protocol statistics, suspicious flow detection, DNS anomaly identification, and IOC extraction from PCAP f… | 1/1 |  |
| `performing-network-traffic-analysis-with-zeek` | Deploy Zeek network security monitor to capture, parse, and analyze network traffic metadata for threat detection, anomaly identification, and forensic investigation. | 1/1 |  |
| `performing-ot-network-security-assessment` | This skill covers conducting comprehensive security assessments of Operational Technology (OT) networks including SCADA systems, DCS architectures, and industrial contro… | 1/1 |  |
| `performing-ot-vulnerability-scanning-safely` | Perform vulnerability scanning in OT/ICS environments safely using passive monitoring, native protocol queries, and carefully controlled active scanning with Tenable OT… | 1/1 |  |
| `performing-packet-injection-attack` | Crafts and injects custom network packets using Scapy, hping3, and Nemesis during authorized security assessments to test firewall rules, IDS detection, protocol handlin… | 2/1 |  |
| `performing-power-grid-cybersecurity-assessment` | This skill covers conducting cybersecurity assessments of electric power grid infrastructure including generation facilities, transmission substations, distribution syst… | 1/1 |  |
| `performing-s7comm-protocol-security-analysis` | Perform security analysis of Siemens S7comm and S7CommPlus protocols used by SIMATIC S7 PLCs to identify vulnerabilities including replay attacks, integrity bypass, unau… | 1/1 |  |
| `performing-ssl-tls-inspection-configuration` | Configure SSL/TLS inspection on network security devices to decrypt, inspect, and re-encrypt HTTPS traffic for threat detection while managing certificates, exemptions,… | 2/2 |  |
| `performing-ssl-tls-security-assessment` | Assess SSL/TLS server configurations using the sslyze Python library to evaluate cipher suites, certificate chains, protocol versions, HSTS headers, and known vulnerabil… | 2/2 |  |
| `performing-wifi-password-cracking-with-aircrack` | Captures WPA/WPA2 handshakes and performs offline password cracking using aircrack-ng, hashcat, and dictionary attacks during authorized wireless security assessments to… | 2/1 |  |
| `performing-wireless-network-penetration-test` | Execute a wireless network penetration test to assess WiFi security by capturing handshakes, cracking WPA2/WPA3 keys, detecting rogue access points, and testing wireless… | 1/1 |  |
| `performing-wireless-security-assessment-with-kismet` | Conduct wireless network security assessments using Kismet to detect rogue access points, hidden SSIDs, weak encryption, and unauthorized clients through passive RF moni… | 1/1 |  |
| `protocol-exploitation` | Network Control Chain Phase 5/协议漏洞利用. 触发词: 协议漏洞利用。 | 1/1 | 覆寫特徵 |
| `race-condition` | Race condition and TOCTOU testing for web apps. Use when testing one-time operations, concurrent HTTP abuse, rate-limit bypass, Turbo Intruder gates, HTTP/2 single-packe… | 2/2 |  |
| `redteam-opsec` | OPSEC隐蔽作战纪律:IP黑名单绕过,速率时序,流量混淆,最小足迹,反取证,渐进暴露。Use when maintaining stealth, bypassing IP bans, or planning covert red-team ops. | 1/1 |  |
| `scanning-infrastructure-with-nessus` | Tenable Nessus is the industry-leading vulnerability scanner used to identify security weaknesses across network infrastructure including servers, workstations, network… | 2/2 |  |
| `scanning-network-with-nmap-advanced` | Performs advanced network reconnaissance using Nmap's scripting engine, timing controls, evasion techniques, and output parsing to discover hosts, enumerate services, de… | 2/1 |  |
| `securing-kubernetes-on-cloud` | This skill covers hardening managed Kubernetes clusters on EKS, AKS, and GKE by implementing Pod Security Standards, network policies, workload identity, RBAC scoping, i… | 2/1 |  |
| `slow-dos-&-flooding` | Network Control Chain Phase 6/慢速DoS与泛洪. 触发词: 慢速DoS与泛洪。 | 1/1 | 覆寫特徵 |
| `smtp-penetration-testing` | Conduct comprehensive security assessments of SMTP (Simple Mail Transfer Protocol) servers to identify vulnerabilities including open relays, user enumeration, weak auth… | 1/1 |  |
| `ssh-penetration-testing` | Conduct comprehensive SSH security assessments including enumeration, credential attacks, vulnerability exploitation, tunneling techniques, and post-exploitation activit… | 1/1 |  |
| `tls/ssh-auditing` | Network Control Chain Phase 3/TLS-SSH审计. 触发词: TLS-SSH审计。 | 1/1 | 覆寫特徵 |
| `traffic-analysis-pcap` | Traffic analysis and PCAP forensics playbook. Use when analyzing network captures including Wireshark filters, protocol analysis (HTTP/DNS/FTP/SMTP/USB/WiFi), data extra… | 1/1 |  |
| `traffic-replay-&-editing` | Network Control Chain Phase 9/流量重放与编辑. 触发词: 流量重放与编辑。 | 1/1 | 覆寫特徵 |
| `tunneling-and-pivoting` | Tunneling and pivoting playbook. Use when establishing network tunnels through compromised hosts including SSH tunneling, Chisel, Ligolo-ng, socat, DNS/ICMP/HTTP tunneli… | 1/1 |  |
| `unlimited-attack-scope` | 不设限原则:搜索/验证/串联/记录一切,全领域适用,被拦换路,不达不休。Use when reminding scope is unlimited across Web/APK/cloud/AI/wireless/social eng. | 1/1 |  |
| `vlan-hopping-&-l2` | Network Control Chain Phase 4/VLAN跳跃与二层攻击. 触发词: VLAN跳跃与二层攻击。 | 1/1 | 覆寫特徵 |
| `wi-fi-phishing-/-evil-twin` | Social Engineering Chain Phase 6/Wi-Fi钓鱼. 触发词: Wi-Fi钓鱼。 | 1/1 | 覆寫特徵 |
| `wireless-attacks` | Network Control Chain Phase 8/无线攻击. 触发词: 无线攻击。 | 1/1 | 覆寫特徵 |
| `wireless-brute-force` | Credential Breach Chain Phase 11/无线爆破. 触发词: 无线爆破。 | 1/1 | 覆寫特徵 |
| `wireless-hardware-attack` | 无线/硬件:WiFi PMKID/WPS/Evil Twin,BLE,Zigbee,NFC,SDR,UART/JTAG/SPI,侧信道,故障注入。Use when attacking WiFi, BLE, RFID, SDR, or hardware interfaces. | 1/1 |  |

### 資安—雲端／供應鏈（43）

| Skill | 說明 | 定義/版本 | 旗標 |
|---|---|---:|---|
| `ai-ml-security` | AI/ML security playbook. Use when assessing model supply chain attacks (pickle RCE, poisoned weights), adversarial examples, model poisoning, model stealing, data privac… | 1/1 |  |
| `auditing-aws-s3-bucket-permissions` | Systematically audit AWS S3 bucket permissions to identify publicly accessible buckets, overly permissive ACLs, misconfigured bucket policies, and missing encryption set… | 1/1 |  |
| `auditing-cloud-with-cis-benchmarks` | This skill details how to conduct cloud security audits using Center for Internet Security benchmarks for AWS, Azure, and GCP. It covers interpreting CIS Foundations Ben… | 1/1 |  |
| `aws-attacks` | Cloud Attack Chain Phase 1/AWS攻击. 触发词: AWS攻击。 | 1/1 | 覆寫特徵 |
| `aws-security-audit` | Comprehensive AWS security posture assessment using AWS CLI and security best practices | 1/1 |  |
| `azure-attacks` | Cloud Attack Chain Phase 2/Azure攻击. 触发词: Azure攻击。 | 1/1 | 覆寫特徵 |
| `building-cloud-security-posture-management` | This skill guides security architects through designing and implementing a cloud security posture management program that continuously monitors infrastructure configurat… | 1/1 |  |
| `building-cloud-siem-with-sentinel` | This skill covers deploying Microsoft Sentinel as a cloud-native SIEM and SOAR platform for centralized security operations. It details configuring data connectors for m… | 1/1 |  |
| `Cloud Attack Chain` | 云平台攻击类 automated penetration testing chain. 触发词: 云平台攻击类。 | 1/1 | 覆寫特徵 |
| `cloud-config-audit` | Cloud Attack Chain Phase 9/云配置审计. 触发词: 云配置审计。 | 1/1 | 覆寫特徵 |
| `cloud-security-labs` | Lab & Training Chain Phase 5/云安全靶场. 触发词: 云安全靶场。 | 1/1 | 覆寫特徵 |
| `cloud-storage-bucket-attack` | Cloud Attack Chain Phase 7/云存储桶攻击. 触发词: 云存储桶攻击。 | 1/1 | 覆寫特徵 |
| `conducting-cloud-incident-response` | Responds to security incidents in cloud environments (AWS, Azure, GCP) by performing identity-based containment, cloud-native log analysis, resource isolation, and foren… | 1/1 |  |
| `container-&-k8s-attacks` | Cloud Attack Chain Phase 10/容器与K8s攻击. 触发词: 容器与K8s攻击。 | 1/1 | 覆寫特徵 |
| `csm-cloud-security` | 云存储安全配置审计 — 云安全模块 \| Cloud Security \| 难度★★★ \| PTES框架 | 1/1 |  |
| `csm-cloud-security-aws` | AWS安全评估 — 云安全模块 \| Cloud Security \| 难度★★★★ \| PTES框架 | 1/1 |  |
| `csm-cloud-security-azure` | Azure安全评估 — 云安全模块 \| Cloud Security \| 难度★★★★ \| PTES框架 | 1/1 |  |
| `csm-cloud-security-gcp` | GCP安全评估 — 云安全模块 \| Cloud Security \| 难度★★★★ \| PTES框架 | 1/1 |  |
| `csm-cloud-security-iam` | 云IAM权限与访问控制审计 — 云安全模块 \| Cloud Security \| 难度★★★ \| PTES框架 | 1/1 |  |
| `csm-supply-chain-security` | 软件依赖与开源合规审计 — 供应链安全模块 \| Supply Chain Security \| 难度★★★ \| PTES框架 | 1/1 |  |
| `csm-supply-chain-security-sbom` | SBOM生成与验证 — 供应链安全模块 \| Supply Chain Security \| 难度★★★ \| PTES框架 | 1/1 |  |
| `detecting-container-escape-attempts` | Container escape is a critical attack technique where an adversary breaks out of container isolation to access the host system or other containers. Detection involves mo… | 1/1 |  |
| `detecting-container-escape-with-falco-rules` | Detect container escape attempts in real-time using Falco runtime security rules that monitor syscalls, file access, and privilege escalation. | 1/1 |  |
| `detecting-supply-chain-attacks-in-ci-cd` | Scans GitHub Actions workflows and CI/CD pipeline configurations for supply chain attack vectors including unpinned actions, script injection via expressions, dependency… | 2/2 |  |
| `detecting-typosquatting-packages-in-npm-pypi` | Detects typosquatting attacks in npm and PyPI package registries by analyzing package name similarity using Levenshtein distance and other string metrics, examining publ… | 1/1 |  |
| `gcp-attacks` | Cloud Attack Chain Phase 3/GCP攻击. 触发词: GCP攻击。 | 1/1 | 覆寫特徵 |
| `hunting-for-supply-chain-compromise` | Hunt for supply chain compromise indicators including trojanized software updates, compromised dependencies, unauthorized code modifications, and tampered build artifact… | 1/1 |  |
| `iam-&-privilege-escalation` | Cloud Attack Chain Phase 4/IAM与特权提升. 触发词: IAM与特权提升。 | 1/1 | 覆寫特徵 |
| `implementing-aws-security-hub` | This skill covers deploying AWS Security Hub as a centralized cloud security posture management platform that aggregates findings from GuardDuty, Inspector, Macie, and t… | 1/1 |  |
| `implementing-aws-security-hub-compliance` | Implementing AWS Security Hub to aggregate security findings across AWS accounts, enable compliance standards like CIS AWS Foundations and PCI DSS, configure automated r… | 1/1 |  |
| `implementing-azure-defender-for-cloud` | Implementing Microsoft Defender for Cloud to enable cloud security posture management, workload protection across VMs, containers, databases, and storage, configure secu… | 1/1 |  |
| `implementing-cloud-security-posture-management` | Implementing Cloud Security Posture Management (CSPM) to continuously monitor multi-cloud environments for misconfigurations, compliance violations, and security risks u… | 1/1 |  |
| `implementing-cloud-vulnerability-posture-management` | Implement Cloud Security Posture Management using AWS Security Hub, Azure Defender for Cloud, and open-source tools like Prowler and ScoutSuite for multi-cloud vulnerabi… | 1/1 |  |
| `implementing-nerc-cip-compliance-controls` | This skill covers implementing North American Electric Reliability Corporation Critical Infrastructure Protection (NERC CIP) compliance controls for Bulk Electric System… | 1/1 |  |
| `implementing-supply-chain-security-with-in-toto` | Implement software supply chain integrity verification for container builds using the in-toto framework to create cryptographically signed attestations across CI/CD pipe… | 1/1 |  |
| `performing-cloud-penetration-testing` | Performs authorized penetration testing of cloud environments across AWS, Azure, and GCP to identify IAM misconfigurations, exposed storage buckets, overly permissive se… | 1/1 |  |
| `performing-container-escape-detection` | Detects container escape attempts by analyzing namespace configurations, privileged container checks, dangerous capability assignments, and host path mounts using the ku… | 1/1 |  |
| `performing-gcp-penetration-testing-with-gcpbucketbrute` | Perform GCP security testing using GCPBucketBrute for storage bucket enumeration, gcloud IAM privilege escalation path analysis, and service account permission auditing | 2/2 |  |
| `performing-supply-chain-attack-simulation` | Simulate and detect software supply chain attacks including typosquatting detection via Levenshtein distance, dependency confusion testing against private registries, pa… | 2/2 |  |
| `remediating-s3-bucket-misconfiguration` | This skill provides step-by-step procedures for identifying and remediating Amazon S3 bucket misconfigurations that expose sensitive data to unauthorized access. It cove… | 1/1 |  |
| `securing-github-actions-workflows` | This skill covers hardening GitHub Actions workflows against supply chain attacks, credential theft, and privilege escalation. It addresses pinning actions to SHA digest… | 2/1 |  |
| `security-scanning-security-dependencies` | You are a security expert specializing in dependency vulnerability analysis, SBOM generation, and supply chain security. Scan project dependencies across multiple ecosys… | 1/1 |  |
| `serverless-attacks` | Cloud Attack Chain Phase 5/Serverless攻击. 触发词: Serverless攻击。 | 1/1 | 覆寫特徵 |

### 資安—鑑識／事件應變／威脅情報（102）

| Skill | 說明 | 定義/版本 | 旗標 |
|---|---|---:|---|
| `acquiring-disk-image-with-dd-and-dcfldd` | Create forensically sound bit-for-bit disk images using dd and dcfldd while preserving evidence integrity through hash verification. | 1/1 |  |
| `analyzing-browser-forensics-with-hindsight` | Analyze Chromium-based browser artifacts using Hindsight to extract browsing history, downloads, cookies, cached content, autofill data, saved passwords, and browser ext… | 1/1 |  |
| `analyzing-cobalt-strike-beacon-configuration` | Extract and analyze Cobalt Strike beacon configuration from PE files and memory dumps to identify C2 infrastructure, malleable profiles, and operator tradecraft. | 2/2 |  |
| `analyzing-disk-image-with-autopsy` | Perform comprehensive forensic analysis of disk images using Autopsy to recover files, examine artifacts, and build investigation timelines. | 2/1 |  |
| `analyzing-docker-container-forensics` | Investigate compromised Docker containers by analyzing images, layers, volumes, logs, and runtime artifacts to identify malicious activity and evidence. | 1/1 |  |
| `analyzing-kubernetes-audit-logs` | Parses Kubernetes API server audit logs (JSON lines) to detect exec-into-pod, secret access, RBAC modifications, privileged pod creation, and anonymous API access. Build… | 1/1 |  |
| `analyzing-mft-for-deleted-file-recovery` | Analyze the NTFS Master File Table ($MFT) to recover metadata and content of deleted files by examining MFT record entries, $LogFile, $UsnJrnl, and MFT slack space using… | 1/1 |  |
| `analyzing-outlook-pst-for-email-forensics` | Analyze Microsoft Outlook PST and OST files for email forensic evidence including message content, headers, attachments, deleted items, and metadata using libpff, pst-ut… | 1/1 |  |
| `analyzing-powershell-empire-artifacts` | Detect PowerShell Empire framework artifacts in Windows event logs by identifying Base64 encoded launcher patterns, default user agents, staging URL structures, stager I… | 2/2 |  |
| `analyzing-prefetch-files-for-execution-history` | Parse Windows Prefetch files to determine program execution history including run counts, timestamps, and referenced files for forensic investigation. | 1/1 |  |
| `analyzing-ransomware-leak-site-intelligence` | Monitor and analyze ransomware group data leak sites (DLS) to track victim postings, extract threat intelligence on group tactics, and assess sector-specific ransomware… | 2/2 |  |
| `analyzing-ransomware-payment-wallets` | Traces ransomware cryptocurrency payment flows using blockchain analysis tools such as Chainalysis Reactor, WalletExplorer, and blockchain.com APIs. Identifies wallet cl… | 1/1 |  |
| `analyzing-security-logs-with-splunk` | Leverages Splunk Enterprise Security and SPL (Search Processing Language) to investigate security incidents through log correlation, timeline reconstruction, and anomaly… | 1/1 |  |
| `analyzing-slack-space-and-file-system-artifacts` | Examine file system slack space, MFT entries, USN journal, and alternate data streams to recover hidden data and reconstruct file activity on NTFS volumes. | 1/1 |  |
| `analyzing-threat-intelligence-feeds` | Analyzes structured and unstructured threat intelligence feeds to extract actionable indicators, adversary tactics, and campaign context. Use when ingesting commercial o… | 1/1 |  |
| `analyzing-usb-device-connection-history` | Investigate USB device connection history from Windows registry, event logs, and setupapi logs to track removable media usage and potential data exfiltration. | 1/1 |  |
| `analyzing-windows-amcache-artifacts` | Parse and analyze Windows Amcache.hve registry hive to extract program execution evidence, file metadata, SHA-1 hashes, and device connection history for digital forensi… | 1/1 |  |
| `analyzing-windows-lnk-files-for-artifacts` | Parse Windows LNK shortcut files to extract target paths, timestamps, volume information, and machine identifiers for forensic timeline reconstruction. | 1/1 |  |
| `analyzing-windows-prefetch-with-python` | Parse Windows Prefetch files using the windowsprefetch Python library to reconstruct application execution history, detect renamed or masquerading binaries, and identify… | 1/1 |  |
| `automating-ioc-enrichment` | Automates the enrichment of raw indicators of compromise with multi-source threat intelligence context using SOAR platforms, Python pipelines, or TIP playbooks to reduce… | 1/1 |  |
| `building-attack-pattern-library-from-cti-reports` | Extract and catalog attack patterns from cyber threat intelligence reports into a structured STIX-based library mapped to MITRE ATT&CK for detection engineering and thre… | 2/2 |  |
| `building-detection-rule-with-splunk-spl` | Build effective detection rules using Splunk Search Processing Language (SPL) correlation searches to identify security threats in SOC environments. | 1/1 |  |
| `building-detection-rules-with-sigma` | Builds vendor-agnostic detection rules using the Sigma rule format for threat detection across SIEM platforms including Splunk, Elastic, and Microsoft Sentinel. Use when… | 2/1 |  |
| `building-incident-response-dashboard` | Builds real-time incident response dashboards in Splunk, Elastic, or Grafana to provide SOC analysts and leadership with situational awareness during active incidents, t… | 2/1 |  |
| `building-ioc-defanging-and-sharing-pipeline` | Build an automated pipeline to defang indicators of compromise (URLs, IPs, domains, emails) for safe sharing and distribute them in STIX format through TAXII feeds and t… | 1/1 |  |
| `building-ioc-enrichment-pipeline-with-opencti` | OpenCTI is an open-source platform for managing cyber threat intelligence knowledge, built on STIX 2.1 as its native data model. This skill covers building an automated… | 1/1 |  |
| `building-soc-playbook-for-ransomware` | Builds a structured SOC incident response playbook for ransomware attacks covering detection, containment, eradication, and recovery phases with specific SIEM queries, i… | 1/1 |  |
| `building-threat-hunt-hypothesis-framework` | Build a systematic threat hunt hypothesis framework that transforms threat intelligence, attack patterns, and environmental data into testable hunting hypotheses. | 2/1 |  |
| `building-threat-intelligence-enrichment-in-splunk` | Build automated threat intelligence enrichment pipelines in Splunk Enterprise Security using lookup tables, modular inputs, and the Threat Intelligence Framework. | 2/2 |  |
| `building-threat-intelligence-feed-integration` | Builds automated threat intelligence feed integration pipelines connecting STIX/TAXII feeds, open-source threat intel, and commercial TI platforms into SIEM and security… | 2/2 |  |
| `building-threat-intelligence-platform` | Building a Threat Intelligence Platform (TIP) involves deploying and integrating multiple CTI tools into a unified system for collecting, analyzing, enriching, and disse… | 2/2 |  |
| `building-vulnerability-aging-and-sla-tracking` | Implement a vulnerability aging dashboard and SLA tracking system to measure remediation performance against severity-based timelines and drive accountability. | 1/1 |  |
| `configuring-windows-event-logging-for-detection` | Configures Windows Event Logging with advanced audit policies to generate high-fidelity security events for threat detection and forensic investigation. Use when enablin… | 1/1 |  |
| `correlating-threat-campaigns` | Correlates disparate security incidents, IOCs, and adversary behaviors across time and organizations to identify unified threat campaigns, attribute them to common threa… | 1/1 |  |
| `csm-anti-forensics-covering-tracks` | 痕迹清除与反取证 — 痕迹清除模块 \| Covering Tracks \| 难度★★★ \| PTES框架 | 1/1 |  |
| `csm-digital-forensics` | 磁盘镜像与证据获取 — 数字取证模块 \| Digital Forensics \| 难度★★★ \| PTES框架 | 1/1 |  |
| `csm-digital-forensics-linux` | Linux数字取证分析 — 数字取证模块 \| Digital Forensics \| 难度★★★★ \| PTES框架 | 1/1 |  |
| `csm-digital-forensics-volatility` | 内存取证分析(Volatility) — 数字取证模块 \| Digital Forensics \| 难度★★★★ \| PTES框架 | 1/1 |  |
| `csm-incident-response` | 事件分类与优先级评估 — 应急响应模块 \| Incident Response \| 难度★★★ \| PTES框架 | 1/1 |  |
| `csm-incident-response-ai` | AI安全应急响应 — 应急响应模块 \| Incident Response \| 难度★★★★ \| PTES框架 | 1/1 |  |
| `csm-threat-hunting` | 威胁狩猎方法论与假设驱动 — 威胁狩猎模块 \| Threat Hunting \| 难度★★★★ \| PTES框架 | 1/1 |  |
| `csm-threat-hunting-att-ck` | 基于ATT&CK的威胁狩猎 — 威胁狩猎模块 \| Threat Hunting \| 难度★★★★★ \| PTES框架 | 1/1 |  |
| `csm-threat-hunting-sigma` | 基于Sigma规则的检测工程 — 威胁狩猎模块 \| Threat Hunting \| 难度★★★★ \| PTES框架 | 1/1 |  |
| `csm-threat-intelligence` | 威胁情报驱动安全运营 — 威胁情报模块 \| Threat Intelligence \| 难度★★★★ \| PTES框架 | 1/1 |  |
| `csm-threat-intelligence-apt` | APT组织分析与归因 — 威胁情报模块 \| Threat Intelligence \| 难度★★★★★ \| PTES框架 | 1/1 |  |
| `csm-threat-intelligence-misp` | MISP平台部署与威胁情报共享 — 威胁情报模块 \| Threat Intelligence \| 难度★★★★ \| PTES框架 | 1/1 |  |
| `csm-threat-intelligence-taxii-stix` | 威胁情报馈入与TAXII/STIX管理 — 威胁情报模块 \| Threat Intelligence \| 难度★★★ \| PTES框架 | 1/1 |  |
| `csm-windows-digital-forensics` | Windows数字取证分析 — 数字取证模块 \| Digital Forensics \| 难度★★★★ \| PTES框架 | 1/1 |  |
| `cyber-ir-playbook` | Build incident response timelines and report packs from event logs. Use for detection-to-recovery reporting, phase tracking, and stakeholder-ready incident summaries. | 1/1 |  |
| `detecting-aws-guardduty-findings-automation` | Automate AWS GuardDuty threat detection findings processing using EventBridge and Lambda to enable real-time incident response, automatic quarantine of compromised resou… | 1/1 |  |
| `detecting-email-account-compromise` | Detect compromised O365 and Google Workspace email accounts by analyzing inbox rule creation, suspicious sign-in locations, mail forwarding rules, and unusual API access… | 1/1 |  |
| `detecting-evasion-techniques-in-endpoint-logs` | Detects defense evasion techniques used by adversaries in endpoint logs including log tampering, timestomping, process injection, and security tool disabling. Use when i… | 2/1 |  |
| `detecting-living-off-the-land-with-lolbas` | Detect Living Off the Land Binaries (LOLBins/LOLBAS) abuse including certutil, regsvr32, mshta, and rundll32 via process telemetry, Sigma rules, and parent-child process… | 1/1 |  |
| `detecting-rdp-brute-force-attacks` | Detect RDP brute force attacks by analyzing Windows Security Event Logs for failed authentication patterns (Event ID 4625), successful logons after failures (Event ID 46… | 1/1 |  |
| `evaluating-threat-intelligence-platforms` | Evaluates and selects Threat Intelligence Platform (TIP) products based on organizational requirements including feed integration capability, STIX/TAXII support, workflo… | 1/1 |  |
| `executing-diamond-model-analysis` | Applies the Diamond Model of Intrusion Analysis to structure adversary activity into its four core vertices (adversary, capability, infrastructure, victim) and identifie… | 1/1 |  |
| `executing-red-team-engagement-planning` | Red team engagement planning is the foundational phase that defines scope, objectives, rules of engagement (ROE), threat model selection, and operational timelines befor… | 2/2 |  |
| `extracting-browser-history-artifacts` | Extract and analyze browser history, cookies, cache, downloads, and bookmarks from Chrome, Firefox, and Edge for forensic evidence of user web activity. | 2/1 |  |
| `extracting-windows-event-logs-artifacts` | Extract, parse, and analyze Windows Event Logs (EVTX) using Chainsaw, Hayabusa, and EvtxECmd to detect lateral movement, persistence, and privilege escalation. | 1/1 |  |
| `generating-threat-intelligence-reports` | Generates structured cyber threat intelligence reports at strategic, operational, and tactical levels tailored to specific audiences including executives, security opera… | 1/1 |  |
| `hunting-credential-stuffing-attacks` | Detects credential stuffing attacks by analyzing authentication logs for login velocity anomalies, ASN diversity, password spray patterns, and geographic distribution of… | 1/1 |  |
| `hunting-for-anomalous-powershell-execution` | Hunt for malicious PowerShell activity by analyzing Script Block Logging (Event 4104), Module Logging (Event 4103), and process creation events. The analyst parses Windo… | 1/1 |  |
| `hunting-for-defense-evasion-via-timestomping` | Detect NTFS timestamp manipulation (MITRE T1070.006) by comparing $STANDARD_INFORMATION vs $FILE_NAME timestamps in the MFT. Uses analyzeMFT and Python to identify files… | 1/1 |  |
| `hunting-for-shadow-copy-deletion` | Hunt for Volume Shadow Copy deletion activity that indicates ransomware preparation or anti-forensics by monitoring vssadmin, wmic, and PowerShell shadow copy commands. | 1/1 |  |
| `hunting-for-t1098-account-manipulation` | Hunt for MITRE ATT&CK T1098 account manipulation including shadow admin creation, SID history injection, group membership changes, and credential modifications using Win… | 1/1 |  |
| `hunting-living-off-the-land-binaries` | Detects abuse of Living Off The Land Binaries (LOLBAS) such as certutil, wmic, mshta, regsvr32, and rundll32 in Windows event logs and Sysmon telemetry. Builds detection… | 1/1 |  |
| `implementing-cloud-trail-log-analysis` | Implementing AWS CloudTrail log analysis for security monitoring, threat detection, and forensic investigation using Athena, CloudWatch Logs Insights, and SIEM integrati… | 1/1 |  |
| `implementing-ot-incident-response-playbook` | Develop and implement OT-specific incident response playbooks aligned with SANS PICERL framework, IEC 62443, and NIST SP 800-82 that address unique ICS challenges includ… | 1/1 |  |
| `implementing-siem-use-case-tuning` | Tune SIEM detection rules to reduce false positives by analyzing alert volumes, creating whitelists, adjusting thresholds, and measuring detection efficacy metrics in Sp… | 1/1 |  |
| `implementing-soar-automation-with-phantom` | Implements Security Orchestration, Automation, and Response (SOAR) workflows using Splunk SOAR (formerly Phantom) to automate alert triage, IOC enrichment, containment a… | 1/1 |  |
| `implementing-soar-playbook-with-palo-alto-xsoar` | Implement automated incident response playbooks in Cortex XSOAR to orchestrate security workflows across SOC tools and reduce manual response time. | 1/1 |  |
| `implementing-stix-taxii-feed-integration` | STIX (Structured Threat Information eXpression) and TAXII (Trusted Automated eXchange of Intelligence Information) are OASIS open standards for representing and transpor… | 1/1 |  |
| `implementing-threat-intelligence-lifecycle-management` | Implement a structured threat intelligence lifecycle encompassing planning, collection, processing, analysis, dissemination, and feedback stages to produce actionable in… | 1/1 |  |
| `implementing-threat-intelligence-platform` | Build a MISP-backed threat intelligence platform that ingests IOCs from multiple feeds, correlates events with galaxy clusters, and enriches indicators via VirusTotal an… | 1/1 |  |
| `implementing-velociraptor-for-ir-collection` | Deploy and configure Velociraptor for scalable endpoint forensic artifact collection during incident response using VQL queries, hunts, and pre-built artifact packs acro… | 1/1 |  |
| `implementing-vulnerability-sla-breach-alerting` | Build automated alerting for vulnerability remediation SLA breaches with severity-based timelines, escalation workflows, and compliance reporting dashboards. | 1/1 |  |
| `incident-response` | 安全事件响应深度专业技能：APT追踪与溯源、恶意样本分析、内存取证、日志关联分析、攻击链重建、从告警到溯源完整响应链 | 1/1 |  |
| `investigating-phishing-email-incident` | Investigates phishing email incidents from initial user report through header analysis, URL/attachment detonation, impacted user identification, and containment actions… | 1/1 |  |
| `linux-security-bypass` | Linux security mechanism bypass playbook. Use when facing restricted bash/rbash, read-only or noexec filesystems, AppArmor, SELinux, seccomp filters, or audit logging th… | 1/1 |  |
| `managing-intelligence-lifecycle` | Manages the end-to-end cyber threat intelligence lifecycle from planning and direction through collection, processing, analysis, dissemination, and feedback to ensure in… | 1/1 |  |
| `mapping-mitre-attack-techniques` | Maps observed adversary behaviors, security alerts, and detection rules to MITRE ATT&CK techniques and sub-techniques to quantify detection coverage and guide control pr… | 1/1 |  |
| `performing-cloud-forensics-investigation` | Conduct forensic investigations in cloud environments by collecting and analyzing logs, snapshots, and metadata from AWS, Azure, and GCP services. | 2/1 |  |
| `performing-cloud-forensics-with-aws-cloudtrail` | Perform forensic investigation of AWS environments using CloudTrail logs to reconstruct attacker activity, identify compromised credentials, and analyze API call pattern… | 2/1 |  |
| `performing-cloud-incident-containment-procedures` | Execute cloud-native incident containment across AWS, Azure, and GCP by isolating compromised resources, revoking credentials, preserving forensic evidence, and applying… | 1/1 |  |
| `performing-disk-forensics-investigation` | Conducts disk forensics investigations using forensic imaging, file system analysis, artifact recovery, and timeline reconstruction to support incident response cases. U… | 2/1 |  |
| `performing-endpoint-forensics-investigation` | Performs digital forensics investigation on compromised endpoints including memory acquisition, disk imaging, artifact analysis, and timeline reconstruction. Use when in… | 2/1 |  |
| `performing-false-positive-reduction-in-siem` | Perform systematic SIEM false positive reduction through rule tuning, threshold adjustment, correlation refinement, and threat intelligence enrichment to combat alert fa… | 1/1 |  |
| `performing-file-carving-with-foremost` | Recover files from disk images and unallocated space using Foremost's header-footer signature carving to extract evidence regardless of file system state. | 2/1 |  |
| `performing-insider-threat-investigation` | Investigates insider threat incidents involving employees, contractors, or trusted partners who misuse authorized access to steal data, sabotage systems, or violate secu… | 1/1 |  |
| `performing-ioc-enrichment-automation` | Automates Indicator of Compromise (IOC) enrichment by orchestrating lookups across VirusTotal, AbuseIPDB, Shodan, MISP, and other intelligence sources to provide context… | 1/1 |  |
| `performing-ip-reputation-analysis-with-shodan` | Analyze IP address reputation using the Shodan API to identify open ports, running services, known vulnerabilities, and hosting context for threat intelligence enrichmen… | 2/2 |  |
| `performing-linux-log-forensics-investigation` | Perform forensic investigation of Linux system logs including syslog, auth.log, systemd journal, kern.log, and application logs to reconstruct user activity, detect unau… | 1/1 |  |
| `performing-log-analysis-for-forensic-investigation` | Collect, parse, and correlate system, application, and security logs to reconstruct events and establish timelines during forensic investigations. | 1/1 |  |
| `performing-mobile-device-forensics-with-cellebrite` | Acquire and analyze mobile device data using Cellebrite UFED and open-source tools to extract communications, location data, and application artifacts. | 2/1 |  |
| `performing-ransomware-incident-response` | Execute a structured ransomware incident response including containment, decryption assessment, recovery from backups, and eradication of ransomware persistence mechanis… | 1/1 |  |
| `performing-ransomware-response` | Executes a structured ransomware incident response from initial detection through containment, forensic analysis, decryption assessment, recovery, and post-incident hard… | 1/1 |  |
| `performing-ransomware-tabletop-exercise` | Plans and facilitates tabletop exercises simulating ransomware incidents to test organizational readiness, decision-making, and communication procedures. Designs realist… | 1/1 |  |
| `performing-threat-intelligence-sharing-with-misp` | Use PyMISP to create, enrich, and share threat intelligence events on a MISP platform, including IOC management, feed integration, STIX export, and community sharing wor… | 1/1 |  |
| `performing-timeline-reconstruction-with-plaso` | Build comprehensive forensic super-timelines using Plaso (log2timeline) to correlate events across file systems, logs, and artifacts into a unified chronological view. | 1/1 |  |
| `performing-windows-artifact-analysis-with-eric-zimmerman-tools` | Perform comprehensive Windows forensic artifact analysis using Eric Zimmerman's open-source EZ Tools suite including KAPE, MFTECmd, PECmd, LECmd, JLECmd, and Timeline Ex… | 1/1 |  |
| `prioritizing-vulnerabilities-with-cvss-scoring` | The Common Vulnerability Scoring System (CVSS) is the industry standard framework maintained by FIRST (Forum of Incident Response and Security Teams) for assessing vulne… | 1/1 |  |
| `seo-forensic-incident-response` | Investigate sudden drops in organic traffic or rankings and run a structured forensic SEO incident response with triage, root-cause analysis and recovery plan. | 1/1 |  |

### 資安—治理／稽核／合規（47）

| Skill | 說明 | 定義/版本 | 旗標 |
|---|---|---:|---|
| `auditing-terraform-infrastructure-for-security` | Auditing Terraform infrastructure-as-code for security misconfigurations using Checkov, tfsec, Terrascan, and OPA/Rego policies to detect overly permissive IAM policies,… | 1/1 |  |
| `aws-compliance-checker` | Automated compliance checking against CIS, PCI-DSS, HIPAA, and SOC 2 benchmarks | 1/1 |  |
| `building-identity-governance-lifecycle-process` | Builds comprehensive identity governance and lifecycle management processes including joiner-mover-leaver automation, role mining, access request workflows, periodic rec… | 1/1 |  |
| `bypassing-authentication-with-forced-browsing` | Discovering and accessing unprotected pages, APIs, and administrative interfaces by enumerating URLs and bypassing authentication controls during authorized security ass… | 2/1 |  |
| `configuring-host-based-intrusion-detection` | Configures host-based intrusion detection systems (HIDS) to monitor endpoint file integrity, system calls, and configuration changes for security violations. Use when de… | 1/1 |  |
| `csm-data-security-privacy-gdpr` | GDPR/个保法合规评估 — 数据安全与隐私保护模块 \| Data Security & Privacy \| 难度★★★★ \| PTES框架 | 1/1 |  |
| `csm-devsecops` | 软件供应链安全 — 安全开发运维模块 \| DevSecOps \| 难度★★★★ \| PTES框架 | 1/1 |  |
| `csm-devsecops-dast` | DAST动态应用安全测试 — 安全开发运维模块 \| DevSecOps \| 难度★★★★ \| PTES框架 | 1/1 |  |
| `csm-devsecops-iac` | IaC安全扫描 — 安全开发运维模块 \| DevSecOps \| 难度★★★ \| PTES框架 | 1/1 |  |
| `csm-devsecops-sast` | SAST静态应用安全测试 — 安全开发运维模块 \| DevSecOps \| 难度★★★★ \| PTES框架 | 1/1 |  |
| `csm-endpoint-security` | 端点加固与合规基线 — 端点安全模块 \| Endpoint Security \| 难度★★★★ \| PTES框架 | 1/1 |  |
| `csm-ics-ot-security-iec-62443` | 工控安全合规审计（IEC 62443） — 工控安全模块 \| ICS/OT Security \| 难度★★★★ \| PTES框架 | 1/1 |  |
| `csm-risk-management-security-metrics` | 风险管理与安全度量 — 安全治理与合规模块 \| Governance & Compliance \| 难度★★★★ \| PTES框架 | 1/1 |  |
| `csm-security-audit` | 等级保护合规审计 — 安全审计模块 \| Security Audit \| 难度★★★★ \| PTES框架 | 1/1 |  |
| `csm-security-audit-ai-agent` | AI Agent安全审计 — 安全审计模块 \| Security Audit \| 难度★★★★ \| PTES框架 | 1/1 |  |
| `csm-security-framework-compliance-audit` | 安全框架与合规审计 — 安全治理与合规模块 \| Governance & Compliance \| 难度★★★ \| PTES框架 | 1/1 |  |
| `csm-security-policy-awareness-program` | 安全策略体系与安全意识 — 安全治理与合规模块 \| Governance & Compliance \| 难度★★★ \| PTES框架 | 1/1 |  |
| `hardening-linux-endpoint-with-cis-benchmark` | Hardens Linux endpoints using CIS Benchmark recommendations for Ubuntu, RHEL, and CentOS to reduce attack surface, enforce security baselines, and meet compliance requir… | 2/1 |  |
| `hardening-windows-endpoint-with-cis-benchmark` | Hardens Windows endpoints using CIS (Center for Internet Security) Benchmark recommendations to reduce attack surface, enforce security baselines, and meet compliance re… | 2/1 |  |
| `implementing-aes-encryption-for-data-at-rest` | AES (Advanced Encryption Standard) is a symmetric block cipher standardized by NIST (FIPS 197) used to protect classified and sensitive data. This skill covers implement… | 1/1 |  |
| `implementing-device-posture-assessment-in-zero-trust` | Implementing device posture assessment as a zero trust access control by integrating endpoint health signals from CrowdStrike ZTA, Microsoft Intune, and Jamf into condit… | 1/1 |  |
| `implementing-devsecops-security-scanning` | Integrate security scanning into CI/CD pipelines using tools like Semgrep, Trivy, and Gitleaks. Covers SAST, SCA, container scanning, and secret detection with structure… | 1/1 |  |
| `implementing-disk-encryption-with-bitlocker` | Implements full disk encryption using Microsoft BitLocker on Windows endpoints to protect data at rest from unauthorized access in case of device loss or theft. Use when… | 1/1 |  |
| `implementing-gcp-organization-policy-constraints` | Implement GCP Organization Policy constraints to enforce security guardrails across the entire resource hierarchy, restricting risky configurations and ensuring complian… | 1/1 |  |
| `implementing-identity-governance-with-sailpoint` | Deploy SailPoint IdentityNow or IdentityIQ for identity governance and administration. Covers identity lifecycle management, access request workflows, certification camp… | 1/1 |  |
| `implementing-infrastructure-as-code-security-scanning` | This skill covers implementing automated security scanning for Infrastructure as Code (IaC) templates using tools like Checkov, tfsec, and KICS. It addresses detecting m… | 1/1 |  |
| `implementing-pci-dss-compliance-controls` | PCI DSS 4.0.1 establishes 12 requirements across 6 control objectives for organizations that store, process, or transmit cardholder data. With PCI DSS 3.2.1 retiring Apr… | 1/1 |  |
| `implementing-privileged-access-workstation` | Design and implement Privileged Access Workstations (PAWs) with device hardening, just-in-time access, and integration with CyberArk or BeyondTrust for secure administra… | 1/1 |  |
| `implementing-runtime-application-self-protection` | Deploy Runtime Application Self-Protection (RASP) agents to detect and block attacks from within application runtime, covering OpenRASP integration, attack pattern detec… | 1/1 |  |
| `implementing-threat-modeling-with-mitre-attack` | Implements threat modeling using the MITRE ATT&CK framework to map adversary TTPs against organizational assets, assess detection coverage gaps, and prioritize defensive… | 1/1 |  |
| `linux-shell-scripting` | Provide production-ready shell script templates for common Linux system administration tasks including backups, monitoring, user management, log analysis, and automation… | 1/1 |  |
| `performing-container-security-scanning-with-trivy` | Scan container images, filesystems, and Kubernetes manifests for vulnerabilities, misconfigurations, exposed secrets, and license compliance issues using Aqua Security T… | 2/2 |  |
| `performing-content-security-policy-bypass` | Analyze and bypass Content Security Policy implementations to achieve cross-site scripting by exploiting misconfigurations, JSONP endpoints, unsafe directives, and polic… | 2/1 |  |
| `performing-gcp-security-assessment-with-forseti` | Performing comprehensive security assessments of Google Cloud Platform environments using Forseti Security, Security Command Center, and gcloud CLI to audit IAM policies… | 1/1 |  |
| `performing-hash-cracking-with-hashcat` | Hash cracking is an essential skill for penetration testers and security auditors to evaluate password strength. Hashcat is the world's fastest password recovery tool, s… | 2/2 |  |
| `performing-kubernetes-cis-benchmark-with-kube-bench` | Audit Kubernetes cluster security posture against CIS benchmarks using kube-bench with automated checks for control plane, worker nodes, and RBAC. | 2/2 |  |
| `performing-nist-csf-maturity-assessment` | The NIST Cybersecurity Framework (CSF) 2.0, released in February 2024, provides a comprehensive taxonomy for managing cybersecurity risk through six core Functions - Gov… | 2/2 |  |
| `performing-oil-gas-cybersecurity-assessment` | This skill covers conducting cybersecurity assessments specific to oil and gas facilities including upstream (exploration/production), midstream (pipeline/transport), an… | 1/1 |  |
| `performing-scada-hmi-security-assessment` | Perform security assessments of SCADA Human-Machine Interface (HMI) systems to identify vulnerabilities in web-based HMIs, thin-client configurations, authentication mec… | 1/1 |  |
| `privilege-escalation-methods` | Provide comprehensive techniques for escalating privileges from a low-privileged user to root/administrator access on compromised Linux and Windows systems. Essential fo… | 1/1 |  |
| `securing-remote-access-to-ot-environment` | This skill covers implementing secure remote access to OT/ICS environments for operators, engineers, and vendors while preventing unauthorized access that could compromi… | 1/1 |  |
| `security-auditor` | Expert security auditor specializing in DevSecOps, comprehensive cybersecurity, and compliance frameworks. | 2/2 |  |
| `security-automation` | 安全自动化深度专业技能：DevSecOps全流程集成、CI/CD安全管道、自动化扫描编排、安全左移实践、从代码提交到生产部署全链路安全自动化 | 1/1 |  |
| `security-framework-compliance` | 安全框架与合规审计 — 安全治理与合规模块 \| Governance & Compliance \| 难度★★★ | 1/1 |  |
| `security-policy-awareness` | 安全策略体系与安全意识 — 安全治理与合规模块 \| Governance & Compliance \| 难度★★★ | 1/1 |  |
| `security-scanning-security-hardening` | Coordinate multi-layer security scanning and hardening across application, infrastructure, and compliance controls. | 1/1 |  |
| `triaging-security-incident` | Performs initial triage of security incidents to determine severity, scope, and required response actions using the NIST SP 800-61r3 and SANS PICERL frameworks. Classifi… | 1/1 |  |

### 資安—行動裝置／硬體／IoT（22）

| Skill | 說明 | 定義/版本 | 旗標 |
|---|---|---:|---|
| `android-apk-builder` | Build lightweight Android APKs from scratch or from a simple native Android project, especially when Gradle or a full Android Studio setup is unavailable. Use for reques… | 1/1 |  |
| `android-pentesting-tricks` | Android pentesting playbook. Use when testing Android applications for SSL pinning bypass, exported component abuse, WebView vulnerabilities, intent redirection, root de… | 1/1 |  |
| `apk-static-analysis` | Mobile Attack Chain Phase 1/APK静态分析. 触发词: APK静态分析。 | 1/1 | 覆寫特徵 |
| `app-dynamic-debugging` | Mobile Attack Chain Phase 2/App动态调试. 触发词: App动态调试。 | 1/1 | 覆寫特徵 |
| `badusb-duckyscript` | BadUSB / USB Rubber Ducky 键盘宏脚本（DuckyScript 兼容）完整语法参考与 Payload 生成。覆盖基础语法、全按键分类、延时控制、STRING 文本注入、REPEAT 循环、LOCALE 键盘布局切换、KEYCODE 原始键码、LED 灯光控制。适用于物理社工攻击模拟、HID 注入测试、自动化按键操… | 1/1 |  |
| `configuring-hsm-for-key-storage` | Hardware Security Modules (HSMs) are tamper-resistant physical devices that safeguard cryptographic keys and perform cryptographic operations in a hardened environment.… | 1/1 |  |
| `csm-android-security-testing` | Android安全测试 — 移动安全模块 \| Mobile Security \| 难度★★★ \| PTES框架 | 1/1 |  |
| `csm-ios-security-testing` | iOS安全测试 — 移动安全模块 \| Mobile Security \| 难度★★★★★ \| PTES框架 | 1/1 |  |
| `detecting-stuxnet-style-attacks` | This skill covers detecting sophisticated cyber-physical attacks that follow the Stuxnet attack pattern of modifying PLC logic while spoofing sensor readings to hide the… | 1/1 |  |
| `exploiting-deeplink-vulnerabilities` | Tests and exploits deep link (URL scheme and App Link) vulnerabilities in Android and iOS mobile applications to identify unauthorized access, data injection, intent hij… | 2/1 |  |
| `extracting-config-from-agent-tesla-rat` | Extract embedded configuration from Agent Tesla RAT samples including SMTP/FTP/Telegram exfiltration credentials, keylogger settings, and C2 endpoints using .NET decompi… | 2/2 |  |
| `implementing-mobile-application-management` | Implements Mobile Application Management (MAM) policies to protect enterprise data on managed and unmanaged mobile devices through app-level controls including data loss… | 1/1 |  |
| `Mobile Attack Chain` | 移动端攻击类 automated penetration testing chain. 触发词: 移动端攻击类。 | 1/1 | 覆寫特徵 |
| `mobile-data-storage-leak` | Mobile Attack Chain Phase 4/移动数据存储泄露. 触发词: 移动数据存储泄露。 | 1/1 | 覆寫特徵 |
| `mobile-pentesting-frameworks` | Mobile Attack Chain Phase 6/移动渗透框架. 触发词: 移动渗透框架。 | 1/1 | 覆寫特徵 |
| `mobile-ssl-pinning-bypass` | Mobile SSL pinning bypass playbook. Use when intercepting HTTPS traffic from mobile applications that implement certificate pinning, public key pinning, or SPKI hash pin… | 1/1 |  |
| `performing-android-app-static-analysis-with-mobsf` | Performs automated static analysis of Android applications using Mobile Security Framework (MobSF) to identify hardcoded secrets, insecure permissions, vulnerable compon… | 2/1 |  |
| `performing-brand-monitoring-for-impersonation` | Monitor for brand impersonation attacks across domains, social media, mobile apps, and dark web channels to detect phishing campaigns, fake sites, and unauthorized brand… | 2/2 |  |
| `performing-hardware-security-module-integration` | Integrate Hardware Security Modules (HSMs) using PKCS#11 interface for cryptographic key management, signing operations, and secure key storage with python-pkcs11, AWS C… | 1/1 |  |
| `performing-steganography-detection` | Detect and extract hidden data embedded in images, audio, and other media files using steganalysis tools to uncover covert communication channels. | 2/1 |  |
| `testing-android-intents-for-vulnerabilities` | Tests Android inter-process communication (IPC) through intents for vulnerabilities including intent injection, unauthorized component access, broadcast sniffing, pendin… | 2/1 |  |
| `usb-drop-/-rubber-ducky` | Social Engineering Chain Phase 4/USB掉落攻击. 触发词: USB掉落攻击。 | 1/1 | 覆寫特徵 |

### 資安—通用攻防／CTF（341）

| Skill | 說明 | 定義/版本 | 旗標 |
|---|---|---:|---|
| `active-directory-labs` | Lab & Training Chain Phase 1/AD域靶场. 触发词: AD域靶场。 | 1/1 | 覆寫特徵 |
| `ad-reconnaissance` | Domain Infiltration Chain Phase 1/AD侦察. 触发词: AD侦察。 | 1/1 | 覆寫特徵 |
| `ai-llm-app-attack` | AI/LLM应用攻击:提示注入,Agent工具滥用RCE,RAG投毒,MCP供应链,torch.load pickle RCE。Use when testing LLM apps, agents, RAG, MCP plugins, or AI model file risks. | 1/1 |  |
| `ai-security-dispatch` | AI安全场景分类器和技能路由器。评估任何AI目标时首先调用此技能。自动识别目标类型（聊天机器人/RAG/Agent/MCP/多Agent/基础设施），加载正确的技能组合，生成评估计划。支持FastGPT/Dify/Flowise/Coze/MaxKB/AnythingLLM/Langflow等平台。 | 1/1 |  |
| `ai-security-infra-supplychain` | AI基础设施与供应链安全测试专家。覆盖推理端点暴露(vLLM/Ollama/TGI/OpenAI兼容)、向量数据库安全(Qdrant/Milvus/Weaviate/Pinecone/ChromaDB)、对象存储、Source Maps、云IAM、K8s/服务网格、模型注册表、CI/CD管线、序列化模型风险(pickle/joblib)… | 1/1 |  |
| `ai-security-prompt` | 提示词注入与上下文安全测试专家。覆盖6大攻击类别（指令覆盖、语义框架注入、对话历史操纵、编码隐写、多轮升级、格式语言绕过）、间接注入载体、系统提示词提取、推理泄露、越狱检测。自包含载荷库。含中英双语检查清单和自动化脚本支持。 | 1/1 | 覆寫特徵 |
| `analyzing-certificate-transparency-for-phishing` | Monitor Certificate Transparency logs using crt.sh and Certstream to detect phishing domains, lookalike certificates, and unauthorized certificate issuance targeting you… | 1/1 |  |
| `analyzing-cyber-kill-chain` | Analyzes intrusion activity against the Lockheed Martin Cyber Kill Chain framework to identify which phases an adversary has completed, where defenses succeeded or faile… | 1/1 |  |
| `analyzing-linux-audit-logs-for-intrusion` | Parse and analyze Linux auditd logs to detect intrusion indicators including unauthorized file access, privilege escalation, syscall anomalies, and suspicious process ex… | 1/1 |  |
| `analyzing-phishing-email-headers` | Email headers contain critical metadata that reveals the true origin, routing path, and authentication status of emails. Analyzing these headers is a foundational skill… | 1/1 |  |
| `analyzing-powershell-script-block-logging` | Parse Windows PowerShell Script Block Logs (Event ID 4104) from EVTX files to detect obfuscated commands, encoded payloads, and living-off-the-land techniques. Uses pyth… | 2/2 |  |
| `analyzing-threat-actor-ttps-with-mitre-attack` | MITRE ATT&CK is a globally-accessible knowledge base of adversary tactics, techniques, and procedures (TTPs) based on real-world observations. This skill covers systemat… | 2/2 |  |
| `analyzing-threat-actor-ttps-with-mitre-navigator` | Map advanced persistent threat (APT) group tactics, techniques, and procedures (TTPs) to the MITRE ATT&CK framework using the ATT&CK Navigator and attackcti Python libra… | 2/2 |  |
| `analyzing-tls-certificate-transparency-logs` | Queries Certificate Transparency logs via crt.sh and pycrtsh to detect phishing domains, unauthorized certificate issuance, and shadow IT. Monitors newly issued certific… | 1/1 |  |
| `arbitrary-write-to-rce` | Arbitrary write to RCE playbook. Use when you have an arbitrary write primitive (from heap exploitation, format string, or OOB write) and need to convert it into code ex… | 1/1 |  |
| `asset-screenshot-&-archive` | Recon Chain Phase 17/资产截图与留存. 触发词: 资产截图与留存。 | 1/1 | 覆寫特徵 |
| `auditing-kubernetes-cluster-rbac` | Auditing Kubernetes cluster RBAC configurations to identify overly permissive roles, wildcard permissions, dangerous ClusterRoleBindings, service account abuse, and priv… | 1/1 |  |
| `auditing-kubernetes-rbac-permissions` | Kubernetes Role-Based Access Control (RBAC) auditing systematically reviews roles, cluster roles, bindings, and service account permissions to identify overly permissive… | 1/1 |  |
| `av-evasion` | Anti-Virus (AV) Evasion comprehensive techniques including static, dynamic, behavioral, and memory-based evasion methods | 1/1 |  |
| `aws-iam-best-practices` | IAM policy review, hardening, and least privilege implementation | 1/1 |  |
| `aws-secrets-rotation` | Automate AWS secrets rotation for RDS, API keys, and credentials | 1/1 |  |
| `azure-security-keyvault-keys-dotnet` | Azure Key Vault Keys SDK for .NET. Client library for managing cryptographic keys in Azure Key Vault and Managed HSM. Use for key creation, rotation, encryption, decrypt… | 1/1 |  |
| `azure-security-keyvault-keys-java` | Azure Key Vault Keys Java SDK for cryptographic key management. Use when creating, managing, or using RSA/EC keys, performing encrypt/decrypt/sign/verify operations, or… | 1/1 |  |
| `azure-security-keyvault-secrets-java` | Azure Key Vault Secrets Java SDK for secret management. Use when storing, retrieving, or managing passwords, API keys, connection strings, or other sensitive configurati… | 1/1 |  |
| `backdoors-&-webshells` | Exploit Chain Phase 5/后门与Webshell. 触发词: 后门与Webshell。 | 1/1 | 覆寫特徵 |
| `blockchain-contract-attack` | 区块链/智能合约:Etherscan,slither/mythril,重入/访问控制/预言机/闪电贷,跨链桥,RPC暴露。Use when auditing smart contracts, DeFi, or blockchain attack surfaces. | 1/1 |  |
| `browser-exploitation-v8` | Browser and V8 exploitation playbook. Use when exploiting JavaScript engine vulnerabilities including JIT type confusion, incorrect bounds elimination, and V8 sandbox by… | 1/1 |  |
| `bug-bounty-&-src` | Methodology Chain Phase 6/漏洞赏金与SRC. 触发词: 漏洞赏金与SRC。 | 1/1 | 覆寫特徵 |
| `building-c2-infrastructure-with-sliver-framework` | Build and configure a resilient command-and-control infrastructure using BishopFox's Sliver C2 framework with redirectors, HTTPS listeners, and multi-operator support fo… | 2/2 |  |
| `building-patch-tuesday-response-process` | Establish a structured operational process to triage, test, and deploy Microsoft Patch Tuesday security updates within risk-based remediation SLAs. | 1/1 |  |
| `building-phishing-reporting-button-workflow` | Implement a phishing report button in email clients with automated triage workflow that analyzes user-reported suspicious emails and provides feedback to reporters. | 1/1 |  |
| `building-red-team-c2-infrastructure-with-havoc` | Deploy and configure the Havoc C2 framework with teamserver, HTTPS listeners, redirectors, and Demon agents for authorized red team operations. | 2/2 |  |
| `building-soc-escalation-matrix` | Build a structured SOC escalation matrix defining severity tiers, response SLAs, escalation paths, and notification procedures for security incidents. | 1/1 |  |
| `building-soc-metrics-and-kpi-tracking` | Builds SOC performance metrics and KPI tracking dashboards measuring Mean Time to Detect (MTTD), Mean Time to Respond (MTTR), alert quality ratios, analyst productivity,… | 1/1 |  |
| `building-vulnerability-dashboard-with-defectdojo` | Deploy DefectDojo as a centralized vulnerability management dashboard with scanner integrations, deduplication, metrics tracking, and Jira ticketing workflows. | 2/2 |  |
| `building-vulnerability-scanning-workflow` | Builds a structured vulnerability scanning workflow using tools like Nessus, Qualys, and OpenVAS to discover, prioritize, and track remediation of security vulnerabiliti… | 1/1 |  |
| `business-agent` | 负责业务逻辑漏洞检测：业务流程绕过、状态机缺陷、竞态滥用、价格篡改、 优惠券滥用、库存与数量操纵，以及订单、支付、订阅等场景中的业务规则滥用 | 1/1 |  |
| `business-logic-testing` | 业务逻辑漏洞深度测试技能：支付/验证码/密码重置/竞态条件/水平垂直越权/邀请/优惠/短信轰炸/0元购/整数溢出/订单流程绕过 | 1/1 |  |
| `business-logic-vuln` | Entry P1 category router for business logic testing. Use when workflow abuse, race conditions, pricing flaws, or multi-step state attacks matter more than parser-level i… | 2/2 |  |
| `business-logic-vulnerabilities` | Business logic vulnerability playbook. Use when reasoning about workflows, race conditions, price manipulation, coupon abuse, state machines, and multi-step authorizatio… | 2/2 |  |
| `c2-lateral-movement` | C2驱动的内网横向移动标准作业流程。从端口探测→进程定位→searchall64全盘配置采集→pass.txt密码本提取→fs.exe资产扫描→密码喷洒→横向移动的完整攻击链。覆盖Shiro反序列化、Nacos配置收割、SOCKS5隧道避坑技巧。触发词：横向移动、内网渗透、密码喷洒、fs扫描、searchall64、Nacos利用、Sh… | 1/1 |  |
| `classical-cipher-analysis` | Classical cipher analysis playbook. Use when encountering substitution ciphers, Vigenere, transposition, XOR, or encoded text in CTF challenges that requires frequency a… | 1/1 |  |
| `clickjacking` | Clickjacking playbook. Use when testing whether target pages can be framed, whether X-Frame-Options or CSP frame-ancestors are properly configured, and whether UI redres… | 3/3 | 覆寫特徵 |
| `client-side-attacks` | Exploit Chain Phase 6/客户端攻击. 触发词: 客户端攻击。 | 1/1 | 覆寫特徵 |
| `cloud-asset-discovery` | Recon Chain Phase 5/云资产发现. 触发词: 云资产发现。 | 1/1 | 覆寫特徵 |
| `cloud-attack-methods` | 云攻击:元数据API,S3/K8s,AWS/Azure/GCP身份提权,MinIO矩阵,阿里云FC,ChengZi SDK解密。Use when attacking cloud metadata, IAM, K8s, MinIO, Aliyun FC, or cloud post-ex. | 1/1 |  |
| `cloud-penetration-testing` | Conduct comprehensive security assessments of cloud infrastructure across Microsoft Azure, Amazon Web Services (AWS), and Google Cloud Platform (GCP). | 1/1 |  |
| `cms-fingerprinting` | Recon Chain Phase 1/CMS指纹识别. 触发词: CMS指纹识别。 | 1/1 | 覆寫特徵 |
| `collecting-open-source-intelligence` | Collects and synthesizes open-source intelligence (OSINT) about threat actors, malicious infrastructure, and attack campaigns using publicly available data sources, pass… | 2/1 |  |
| `component-vuln-intel` | 联网情报收集:识别组件后必做CVE/搜索引擎/中文社区/GitHub PoC/资产引擎/即时情报/依赖扩展+受阻换路。Use when a framework/component/version is identified and must search before exploit. | 1/1 |  |
| `conducting-cloud-infrastructure-penetration-test` | Perform a cloud infrastructure penetration test across AWS, Azure, and GCP to identify IAM misconfigurations, exposed storage buckets, insecure serverless functions, and… | 1/1 |  |
| `conducting-full-scope-red-team-engagement` | Plan and execute a comprehensive red team engagement covering reconnaissance through post-exploitation using MITRE ATT&CK-aligned TTPs to evaluate an organization's dete… | 1/1 |  |
| `conducting-phishing-incident-response` | Responds to phishing incidents by analyzing reported emails, extracting indicators, assessing credential compromise, quarantining malicious messages across the organizat… | 1/1 |  |
| `conducting-social-engineering-penetration-test` | Design and execute a social engineering penetration test including phishing, vishing, smishing, and physical pretexting campaigns to measure human security resilience an… | 2/2 |  |
| `conducting-social-engineering-pretext-call` | Plan and execute authorized vishing (voice phishing) pretext calls to assess employee susceptibility to social engineering and evaluate security awareness controls. | 2/2 |  |
| `container-security-testing` | 容器安全深度测试专业技能：Docker/K8s攻击面全覆盖、镜像漏洞利用、容器逃逸技术链、运行时攻击、供应链安全、从镜像审计到宿主机接管完整攻击链 | 1/1 |  |
| `containing-active-security-breach` | Rapidly contain an active security breach by isolating compromised systems, blocking attacker communications, and preserving evidence while minimizing business disruptio… | 1/1 |  |
| `Credential Breach Chain` | Password & Hash Cracking automated penetration testing chain. 触发词: 口令哈希破解。 | 1/1 | 覆寫特徵 |
| `credential-theft` | Domain Infiltration Chain Phase 9/凭据窃取. 触发词: 凭据窃取。 | 1/1 | 覆寫特徵 |
| `csm-active-reconnaissance` | 主动信息搜集 — 信息搜集模块 \| Reconnaissance \| 难度★★★ \| PTES框架 | 1/1 |  |
| `csm-blockchain-web3-security` | 智能合约安全审计 — 区块链/Web3安全模块 \| Blockchain/Web3 Security \| 难度★★★★★ \| PTES框架 | 1/1 |  |
| `csm-blockchain-web3-security-defi` | DeFi协议安全评估 — 区块链/Web3安全模块 \| Blockchain/Web3 Security \| 难度★★★★★ \| PTES框架 | 1/1 |  |
| `csm-blockchain-web3-security-mev` | MEV与跨链桥安全 — 区块链/Web3安全模块 \| Blockchain/Web3 Security \| 难度★★★★★ \| PTES框架 | 1/1 |  |
| `csm-blockchain-web3-security-web3` | Web3前端与钱包安全 — 区块链/Web3安全模块 \| Blockchain/Web3 Security \| 难度★★★★ \| PTES框架 | 1/1 |  |
| `csm-command-injection-exploitation` | 命令注入 — 漏洞利用模块 \| Exploitation \| 难度★★★ \| PTES框架 | 1/1 |  |
| `csm-container-security` | 容器镜像安全与漏洞扫描 — 容器安全模块 \| Container Security \| 难度★★★ \| PTES框架 | 1/1 |  |
| `csm-container-security-falco` | 容器运行时安全(Falco) — 容器安全模块 \| Container Security \| 难度★★★★ \| PTES框架 | 1/1 |  |
| `csm-container-security-kubernetes-rbac` | Kubernetes RBAC与安全策略 — 容器安全模块 \| Container Security \| 难度★★★★ \| PTES框架 | 1/1 |  |
| `csm-cyberspace-search-engine` | 网络空间搜索引擎 — 信息搜集模块 \| Reconnaissance \| 难度★★★ \| PTES框架 | 1/1 |  |
| `csm-data-masking-anonymization` | 数据脱敏与匿名化 — 数据安全与隐私保护模块 \| Data Security & Privacy \| 难度★★★ \| PTES框架 | 1/1 |  |
| `csm-data-security-privacy` | 数据分类与分级保护 — 数据安全与隐私保护模块 \| Data Security & Privacy \| 难度★★★ \| PTES框架 | 1/1 |  |
| `csm-data-security-privacy-dlp` | DLP数据防泄漏策略 — 数据安全与隐私保护模块 \| Data Security & Privacy \| 难度★★★★ \| PTES框架 | 1/1 |  |
| `csm-data-security-privacy-pia` | 隐私影响评估（PIA） — 数据安全与隐私保护模块 \| Data Security & Privacy \| 难度★★★★ \| PTES框架 | 1/1 |  |
| `csm-database-security-assessment` | 数据库安全评估 — 漏洞扫描模块 \| Vulnerability Scanning \| 难度★★★ \| PTES框架 | 1/1 |  |
| `csm-endpoint-security-edr` | EDR部署与检测规则 — 端点安全模块 \| Endpoint Security \| 难度★★★★ \| PTES框架 | 1/1 |  |
| `csm-endpoint-security-mdm` | 移动设备安全与MDM — 端点安全模块 \| Endpoint Security \| 难度★★★★ \| PTES框架 | 1/1 |  |
| `csm-exploitation-ai` | AI代理漏洞利用 — 漏洞利用模块 \| Exploitation \| 难度★★★★ \| PTES框架 | 1/1 |  |
| `csm-exploitation-metasploit` | Metasploit框架利用 — 漏洞利用模块 \| Exploitation \| 难度★★★ \| PTES框架 | 1/1 |  |
| `csm-exploitation-sql` | SQL注入利用 — 漏洞利用模块 \| Exploitation \| 难度★★★ \| PTES框架 | 1/1 |  |
| `csm-html-security-report` | HTML安全报告模板 — 报告撰写模块 \| Reporting \| 难度★★★ \| PTES框架 | 1/1 |  |
| `csm-ics-ot-security` | 工控网络协议安全 — 工控安全模块 \| ICS/OT Security \| 难度★★★★ \| PTES框架 | 1/1 |  |
| `csm-ics-ot-security-plc-rtu` | PLC与RTU安全测试 — 工控安全模块 \| ICS/OT Security \| 难度★★★★★ \| PTES框架 | 1/1 |  |
| `csm-ics-ot-security-scada` | SCADA系统安全评估 — 工控安全模块 \| ICS/OT Security \| 难度★★★★ \| PTES框架 | 1/1 |  |
| `csm-linux-privilege-escalation` | Linux提权 — 权限提升模块 \| Privilege Escalation \| 难度★★★ \| PTES框架 | 1/1 |  |
| `csm-linux-security-hardening` | Linux安全加固与基线检查 — 操作系统安全模块 \| OS Security \| 难度★★★ \| PTES框架 | 1/1 |  |
| `csm-llm-security` | 大模型红队测试 — 大模型安全模块 \| LLM Security \| 难度★★★★★ \| PTES框架 | 1/1 | 覆寫特徵 |
| `csm-llm-security-ai` | AI供应链安全 — 大模型安全模块 \| LLM Security \| 难度★★★ \| PTES框架 | 1/1 |  |
| `csm-llm-security-ai-agent` | AI Agent权限与访问控制 — 大模型安全模块 \| LLM Security \| 难度★★★★ \| PTES框架 | 1/1 |  |
| `csm-llm-security-llm` | LLM提示注入与安全防护 — 大模型安全模块 \| LLM Security \| 难度★★★★ \| PTES框架 | 1/1 | 覆寫特徵 |
| `csm-os-security` | 国产操作系统安全加固 — 操作系统安全模块 \| OS Security \| 难度★★★ \| PTES框架 | 1/1 |  |
| `csm-os-security-linux` | Linux攻击与权限维持技术 — 操作系统安全模块 \| OS Security \| 难度★★★★ \| PTES框架 | 1/1 |  |
| `csm-os-security-macos` | macOS安全评估与加固 — 操作系统安全模块 \| OS Security \| 难度★★★★ \| PTES框架 | 1/1 |  |
| `csm-passive-recon-osint` | 被动信息搜集/OSINT — 信息搜集模块 \| Reconnaissance \| 难度★★ \| PTES框架 | 1/1 |  |
| `csm-post-exploitation` | 信息收集与数据窃取 — 后渗透模块 \| Post-Exploitation \| 难度★★★ \| PTES框架 | 1/1 |  |
| `csm-post-exploitation-shell` | 远程控制与交互式Shell — 后渗透模块 \| Post-Exploitation \| 难度★★★★ \| PTES框架 | 1/1 |  |
| `csm-privilege-escalation` | 内核漏洞与服务配置错误提权 — 权限提升模块 \| Privilege Escalation \| 难度★★★★ \| PTES框架 | 1/1 |  |
| `csm-reporting` | 渗透测试报告编写 — 报告撰写模块 \| Reporting \| 难度★★★ \| PTES框架 | 1/1 |  |
| `csm-reporting-cvss` | 漏洞评级与CVSS评分 — 报告撰写模块 \| Reporting \| 难度★★★ \| PTES框架 | 1/1 |  |
| `csm-social-engineering` | 钓鱼邮件模拟 — 社会工程学模块 \| Social Engineering \| 难度★★★ \| PTES框架 | 1/1 |  |
| `csm-social-engineering-info` | 社会工程学信息 — 信息搜集模块 \| Reconnaissance \| 难度★★★★ \| PTES框架 | 1/1 |  |
| `csm-social-engineering-vishing` | 电话诈骗与Vishing测试 — 社会工程学模块 \| Social Engineering \| 难度★★★★ \| PTES框架 | 1/1 |  |
| `csm-subdomain-discovery` | 子域名探测 — 信息搜集模块 \| Reconnaissance \| 难度★★★ \| PTES框架 | 1/1 |  |
| `csm-tech-stack-fingerprinting` | 目标技术栈识别 — 信息搜集模块 \| Reconnaissance \| 难度★★★ \| PTES框架 | 1/1 |  |
| `csm-vulnerability-management` | 漏洞优先级与风险评估 — 漏洞管理模块 \| Vulnerability Management \| 难度★★★★ \| PTES框架 | 1/1 |  |
| `csm-vulnerability-management-cve` | 漏洞情报与CVE查询 — 漏洞管理模块 \| Vulnerability Management \| 难度★★★ \| PTES框架 | 1/1 |  |
| `csm-vulnerability-management-poc` | 漏洞验证与PoC测试 — 漏洞管理模块 \| Vulnerability Management \| 难度★★★★ \| PTES框架 | 1/1 |  |
| `csm-vulnerability-scanning` | 网络漏洞扫描 — 漏洞扫描模块 \| Vulnerability Scanning \| 难度★★★ \| PTES框架 | 1/1 |  |
| `csm-windows-attack-lateral-movement` | Windows攻击与横向移动技术 — 操作系统安全模块 \| OS Security \| 难度★★★★ \| PTES框架 | 1/1 |  |
| `csm-windows-privilege-escalation` | Windows提权 — 权限提升模块 \| Privilege Escalation \| 难度★★★ \| PTES框架 | 1/1 |  |
| `csm-windows-security-hardening` | Windows安全加固与基线检查 — 操作系统安全模块 \| OS Security \| 难度★★★ \| PTES框架 | 1/1 |  |
| `ct-log-enumeration` | Recon Chain Phase 16/证书透明日志测绘. 触发词: 证书透明日志测绘。 | 1/1 | 覆寫特徵 |
| `ctf-crypto` | Provides cryptography attack techniques for CTF challenges. Use when attacking encryption, hashing, signatures, ZKP, PRNG, or mathematical crypto problems involving RSA,… | 1/1 |  |
| `ctf-platforms` | Lab & Training Chain Phase 2/CTF平台. 触发词: CTF平台。 | 1/1 | 覆寫特徵 |
| `cve-/-nvd-official` | Intelligence Chain Phase 2/CVE-NVD官方库. 触发词: CVE-NVD官方库。 | 1/1 | 覆寫特徵 |
| `cvss-scoring` | Methodology Chain Phase 5/漏洞评级CVSS. 触发词: 漏洞评级CVSS。 | 1/1 | 覆寫特徵 |
| `cyber-kev-triage` | Prioritize vulnerability remediation using KEV-style exploitation context plus asset criticality. Use for CVE triage, patch order decisions, and remediation reporting. | 1/1 |  |
| `deepcode-integration` | DeepCode(HKUDS)多Agent编程系统集成技能。当需要生成复杂代码(exploit/POC/Web工具/后端API)时，通过subprocess调用DeepCode CLI完成代码生成，再由本技能将结果集成到安全测试流程中。触发词：deepcode、深度代码、Paper2Code、Text2Web、Text2Backend、… | 1/1 |  |
| `dependency-confusion` | Supply-chain testing via package-manager dependency confusion: when internal package names resolve to attacker-controlled public registries, leading to malicious install… | 2/2 |  |
| `deserialization-insecure` | Insecure deserialization playbook. Use when Java, PHP, or Python applications deserialize untrusted data via ObjectInputStream, unserialize, pickle, or similar mechanism… | 2/2 |  |
| `detecting-business-email-compromise` | Business Email Compromise (BEC) is a sophisticated fraud scheme where attackers impersonate executives, vendors, or trusted partners to trick employees into transferring… | 1/1 |  |
| `detecting-business-email-compromise-with-ai` | Deploy AI and NLP-powered detection systems to identify business email compromise attacks by analyzing writing style, behavioral patterns, and contextual anomalies that… | 1/1 |  |
| `detecting-cloud-threats-with-guardduty` | This skill teaches security teams how to deploy and operationalize Amazon GuardDuty for continuous threat detection across AWS accounts and workloads. It covers enabling… | 1/1 |  |
| `detecting-dll-sideloading-attacks` | Detect DLL side-loading attacks where adversaries place malicious DLLs alongside legitimate applications to hijack execution flow for defense evasion. | 2/1 |  |
| `detecting-email-forwarding-rules-attack` | Detect malicious email forwarding rules created by adversaries to maintain persistent access to email communications for intelligence collection and BEC attacks. | 1/1 |  |
| `detecting-living-off-the-land-attacks` | Detect abuse of legitimate Windows binaries (LOLBins) used for living off the land attacks. Monitors process creation, command-line arguments, and parent-child relations… | 1/1 |  |
| `detecting-malicious-scheduled-tasks-with-sysmon` | Detect malicious scheduled task creation and modification using Sysmon Event IDs 1 (Process Create for schtasks.exe), 11 (File Create for task XML), and Windows Security… | 1/1 |  |
| `detecting-privilege-escalation-attempts` | Detect privilege escalation attempts including token manipulation, UAC bypass, unquoted service paths, kernel exploits, and sudo/doas abuse across Windows and Linux. | 1/1 |  |
| `detecting-privilege-escalation-in-kubernetes-pods` | Detect and prevent privilege escalation in Kubernetes pods by monitoring security contexts, capabilities, and syscall patterns with Falco and OPA policies. | 1/1 |  |
| `detecting-qr-code-phishing-with-email-security` | Detect and prevent QR code phishing (quishing) attacks that bypass traditional email security by embedding malicious URLs in QR code images within emails. | 1/1 |  |
| `detecting-service-account-abuse` | Detect abuse of service accounts through anomalous interactive logons, privilege escalation, lateral movement, and unauthorized access patterns. | 1/1 |  |
| `detecting-suspicious-powershell-execution` | Detect suspicious PowerShell execution patterns including encoded commands, download cradles, AMSI bypass attempts, and constrained language mode evasion. | 1/1 |  |
| `detecting-t1548-abuse-elevation-control-mechanism` | Detect abuse of elevation control mechanisms including UAC bypass, sudo exploitation, and setuid/setgid manipulation by monitoring registry modifications, process elevat… | 1/1 |  |
| `dfyx_code_security_review` | 高级白盒安全审计专家。基于深度数据流分析和业务逻辑理解的专家级代码安全审计工具。 | 1/1 |  |
| `dll-hijacking-&-sideloading` | Evasion Chain Phase 1/DLL劫持与侧载. 触发词: DLL劫持与侧载。 | 1/1 | 覆寫特徵 |
| `Domain Infiltration Chain` | AD攻击类 automated penetration testing chain. 触发词: AD攻击类。 | 1/1 | 覆寫特徵 |
| `email-&-exchange-attacks` | Domain Infiltration Chain Phase 13/邮件与Exchange攻击. 触发词: 邮件与Exchange攻击。 | 1/1 | 覆寫特徵 |
| `email-header-injection` | Email header injection and spoofing playbook. Use when testing contact forms, email APIs, password reset flows, or any feature that constructs SMTP messages with user-co… | 1/1 |  |
| `employee-&-supply-chain-intel` | Recon Chain Phase 8/员工与供应链情报. 触发词: 员工与供应链情报。 | 1/1 | 覆寫特徵 |
| `ethical-hacking-methodology` | Master the complete penetration testing lifecycle from reconnaissance through reporting. This skill covers the five stages of ethical hacking methodology, essential tool… | 1/1 |  |
| `Evasion Chain` | 免杀规避类 automated penetration testing chain. 触发词: 免杀规避类。 | 1/1 | 覆寫特徵 |
| `executing-phishing-simulation-campaign` | Executes authorized phishing simulation campaigns to assess an organization's susceptibility to email-based social engineering attacks. The tester designs realistic phis… | 2/1 |  |
| `executing-red-team-exercise` | Executes comprehensive red team exercises that simulate real-world adversary operations against an organization's people, processes, and technology. The red team operate… | 2/2 |  |
| `Exfiltration Chain` | 数据渗出类 automated penetration testing chain. 触发词: 数据渗出类。 | 1/1 | 覆寫特徵 |
| `Exploit Chain` | Exploitation automated penetration testing chain. 触发词: 漏洞利用。 | 1/1 | 覆寫特徵 |
| `exploit-code-repositories` | Intelligence Chain Phase 4/漏洞利用代码库. 触发词: 漏洞利用代码库。 | 1/1 | 覆寫特徵 |
| `exploit-development` | Exploit Chain Phase 9/漏洞利用开发. 触发词: 漏洞利用开发。 | 1/1 | 覆寫特徵 |
| `exploit-frameworks` | Exploit Chain Phase 10/漏洞利用框架. 触发词: 漏洞利用框架。 | 1/1 | 覆寫特徵 |
| `exploiting-broken-link-hijacking` | Discover and exploit broken link hijacking vulnerabilities by identifying references to expired domains, decommissioned cloud resources, and dead external services that… | 2/2 |  |
| `exploiting-insecure-deserialization` | Identifying and exploiting insecure deserialization vulnerabilities in Java, PHP, Python, and .NET applications to achieve remote code execution during authorized penetr… | 2/1 |  |
| `exploiting-mass-assignment-in-rest-apis` | Discover and exploit mass assignment vulnerabilities in REST APIs to escalate privileges, modify restricted fields, and bypass authorization controls by injecting unexpe… | 2/2 |  |
| `exploiting-ms17-010-eternalblue-vulnerability` | MS17-010 (EternalBlue) is a critical vulnerability in Microsoft's SMBv1 implementation that allows remote code execution. Originally discovered by the NSA and leaked by… | 2/2 |  |
| `exploiting-template-injection-vulnerabilities` | Detecting and exploiting Server-Side Template Injection (SSTI) vulnerabilities across Jinja2, Twig, Freemarker, and other template engines to achieve remote code executi… | 2/1 |  |
| `exploiting-type-juggling-vulnerabilities` | Exploit PHP type juggling vulnerabilities caused by loose comparison operators to bypass authentication, circumvent hash verification, and manipulate application logic t… | 2/2 |  |
| `exploiting-vulnerabilities-with-metasploit-framework` | The Metasploit Framework is the world's most widely used penetration testing platform, maintained by Rapid7. It contains over 2,300 exploits, 1,200 auxiliary modules, an… | 2/2 |  |
| `expression-language-injection` | Expression Language injection playbook. Use when Java EL, SpEL, OGNL, or MVEL expressions may evaluate attacker-controlled input in Spring, Struts2, Confluence, or simil… | 2/2 |  |
| `file-uploads` | Careful about security and performance. Never trusts file extensions. Knows that large uploads need special handling. Prefers presigned URLs over server proxying. | 1/1 |  |
| `format-string-exploitation` | Format string exploitation playbook. Use when printf-family functions receive user-controlled format strings, enabling arbitrary stack reads (%p/%s), arbitrary memory wr… | 2/2 | 覆寫特徵 |
| `Framework Chain` | 综合框架类 automated penetration testing chain. 触发词: 综合框架类。 | 1/1 | 覆寫特徵 |
| `ftp/smb/mail-brute-force` | Credential Breach Chain Phase 1/FTP-SMB-邮件爆破. 触发词: FTP-SMB-邮件爆破。 | 1/1 | 覆寫特徵 |
| `fuck-cdn-bypass` | FUCK-CDN：绕过CDN查询网站真实源站IP。输入目标域名，按优先级自动穷尽所有OSINT方法，构建证据链输出最终判定。支持 Shodan/FOFA/Censys 等 API Key 注入，自动适配 Windows/Linux。 | 1/1 |  |
| `gha-security-review` | Find exploitable vulnerabilities in GitHub Actions workflows. Every finding MUST include a concrete exploitation scenario — if you can't build the attack, don't report i… | 1/1 |  |
| `github-&-code-leak-search` | Recon Chain Phase 2/GitHub与代码泄露搜索. 触发词: GitHub与代码泄露搜索。 | 1/1 | 覆寫特徵 |
| `gpp-&-group-policy-attacks` | Domain Infiltration Chain Phase 4/GPP与组策略攻击. 触发词: GPP与组策略攻击。 | 1/1 | 覆寫特徵 |
| `gpu-&-distributed-cracking` | Credential Breach Chain Phase 2/GPU加速与分布式破解. 触发词: GPU加速与分布式破解。 | 1/1 | 覆寫特徵 |
| `hardening-docker-containers-for-production` | Hardening Docker containers for production involves applying security best practices aligned with CIS Docker Benchmark v1.8.0 to minimize attack surface, prevent privile… | 2/2 |  |
| `hash-attack-techniques` | Hash attack playbook. Use when exploiting length extension, MD5/SHA1 collisions, HMAC timing leaks, birthday attacks, or hash-based proof of work in CTF and authorized t… | 1/1 |  |
| `hash-id-&-conversion` | Credential Breach Chain Phase 7/哈希识别与格式转换. 触发词: 哈希识别与格式转换。 | 1/1 | 覆寫特徵 |
| `heap-exploitation` | Heap exploitation playbook. Use when targeting ptmalloc2/glibc heap vulnerabilities including UAF, double free, overflow, off-by-one/null, and leveraging tcache/fastbin/… | 1/1 |  |
| `html-injection-testing` | Identify and exploit HTML injection vulnerabilities that allow attackers to inject malicious HTML content into web applications. This vulnerability enables attackers to… | 1/1 |  |
| `hunting-for-dcsync-attacks` | Detect DCSync attacks by analyzing Windows Event ID 4662 for unauthorized DS-Replication-Get-Changes requests from non-domain-controller accounts. | 2/1 |  |
| `implementing-anti-phishing-training-program` | Security awareness training is the human layer of phishing defense. An effective anti-phishing training program combines regular simulations, interactive learning module… | 1/1 |  |
| `implementing-aqua-security-for-container-scanning` | Deploy Aqua Security's Trivy scanner to detect vulnerabilities, misconfigurations, secrets, and license issues in container images across CI/CD pipelines and registries. | 1/1 |  |
| `implementing-attack-path-analysis-with-xm-cyber` | Deploy XM Cyber's continuous exposure management platform to map attack paths, identify choke points, and prioritize the 2% of exposures that threaten critical assets. | 1/1 |  |
| `implementing-aws-iam-permission-boundaries` | Configure IAM permission boundaries in AWS to delegate role creation to developers while enforcing maximum privilege limits set by the security team. | 1/1 |  |
| `implementing-container-image-minimal-base-with-distroless` | Reduce container attack surface by building application images on Google distroless base images that contain only the application runtime with no shell, package manager,… | 1/1 |  |
| `implementing-digital-signatures-with-ed25519` | Ed25519 is a high-performance digital signature algorithm using the Edwards curve Curve25519. It provides 128-bit security with 64-byte signatures and 32-byte keys, offe… | 1/1 |  |
| `implementing-epss-score-for-vulnerability-prioritization` | Integrate FIRST's Exploit Prediction Scoring System (EPSS) API to prioritize vulnerability remediation based on real-world exploitation probability within 30 days. | 1/1 |  |
| `implementing-github-advanced-security-for-code-scanning` | Configure GitHub Advanced Security with CodeQL to perform automated static analysis and vulnerability detection across repositories at enterprise scale. | 1/1 |  |
| `implementing-iso-27001-information-security-management` | ISO/IEC 27001:2022 is the international standard for establishing, implementing, maintaining, and continually improving an Information Security Management System (ISMS).… | 1/1 |  |
| `implementing-kubernetes-pod-security-standards` | Pod Security Standards (PSS) define three levels of security policies -- Privileged, Baseline, and Restricted -- enforced by the Pod Security Admission (PSA) controller… | 1/1 |  |
| `implementing-mitre-attack-coverage-mapping` | Implement MITRE ATT&CK coverage mapping to identify detection gaps, prioritize rule development, and measure SOC detection maturity against adversary techniques. | 1/1 |  |
| `implementing-passwordless-authentication-with-fido2` | Deploy FIDO2/WebAuthn passwordless authentication using security keys and platform authenticators. Covers WebAuthn API integration, FIDO2 server configuration, passkey e… | 1/1 |  |
| `implementing-pod-security-admission-controller` | Implement Kubernetes Pod Security Admission to enforce baseline and restricted security profiles at namespace level using built-in admission controller. | 1/1 |  |
| `implementing-privileged-access-management-with-cyberark` | Deploy CyberArk Privileged Access Management to discover, vault, rotate, and monitor privileged credentials across enterprise infrastructure. This skill covers vault arc… | 1/1 |  |
| `implementing-ransomware-backup-strategy` | Designs and implements a ransomware-resilient backup strategy following the 3-2-1-1-0 methodology (3 copies, 2 media types, 1 offsite, 1 immutable/air-gapped, 0 errors o… | 1/1 |  |
| `implementing-rapid7-insightvm-for-scanning` | Deploy and configure Rapid7 InsightVM Security Console and Scan Engines for authenticated and unauthenticated vulnerability scanning across enterprise environments. | 1/1 |  |
| `implementing-runtime-security-with-tetragon` | Implement eBPF-based runtime security observability and enforcement in Kubernetes clusters using Cilium Tetragon for kernel-level threat detection and policy enforcement. | 1/1 |  |
| `implementing-security-monitoring-with-datadog` | Implement security monitoring using Datadog's Cloud SIEM, log analysis, and threat detection capabilities to identify and respond to security events across cloud infrast… | 1/1 |  |
| `implementing-vulnerability-remediation-sla` | Vulnerability remediation SLAs define mandatory timeframes for patching or mitigating identified vulnerabilities based on severity, asset criticality, and exploit availa… | 1/1 |  |
| `implementing-zero-trust-with-hashicorp-boundary` | Implement HashiCorp Boundary for identity-aware zero trust infrastructure access management with dynamic credential brokering, session recording, and Vault integration. | 1/1 |  |
| `information-gathering` | 信息收集深度渗透测试技能：被动/主动信息收集、子域名枚举、端口扫描、指纹识别、JS分析、云资产发现、GitHub泄露、完整攻击面映射 | 1/1 |  |
| `insecure-source-code-management` | Source control and artifact exposure (.git, .svn, .hg, backups, .env). Use when recon finds VCS paths, 403 on hidden dirs, or backup/config leaks during authorized testi… | 2/2 |  |
| `integrating-sast-into-github-actions-pipeline` | This skill covers integrating Static Application Security Testing (SAST) tools—CodeQL and Semgrep—into GitHub Actions CI/CD pipelines. It addresses configuring automated… | 1/1 |  |
| `Intelligence Chain` | 漏洞数据库类 automated penetration testing chain. 触发词: 漏洞数据库类。 | 1/1 | 覆寫特徵 |
| `investigating-ransomware-attack-artifacts` | Identify, collect, and analyze ransomware attack artifacts to determine the variant, initial access vector, encryption scope, and recovery options. | 1/1 |  |
| `java-audit-pipeline` | Java Web 全链路自动化安全审计流水线。使用 agent team 编排多个审计 skill，自动完成路由提取→鉴权审计→组件漏洞→交叉筛选→调用链追踪→漏洞深度检测→质量校验的完整流程。适用于：(1) 一键启动 Java 项目全量安全审计，(2) 自动识别无鉴权高危路由并精准检测漏洞，(3) 基于调用链的精准漏洞审计（减少误报）… | 1/1 |  |
| `jndi-injection` | JNDI injection playbook. Use when Java applications perform JNDI lookups with attacker-controlled names, especially via Log4j2, Spring, or any code path reaching Initial… | 2/2 |  |
| `kubernetes-pentesting` | Kubernetes penetration testing playbook. Use when targeting Kubernetes clusters via API server, RBAC enumeration, service account abuse, etcd access, Kubelet API, pod es… | 1/1 |  |
| `Lab & Training Chain` | 靶场漏洞环境类 automated penetration testing chain. 触发词: 靶场漏洞环境类。 | 1/1 | 覆寫特徵 |
| `lattice-crypto-attacks` | Lattice-based cryptanalysis playbook. Use when attacking RSA via Coppersmith small roots, recovering DSA/ECDSA nonces from bias, solving knapsack problems, or applying L… | 1/1 |  |
| `Linux PrivEsc Chain` | Linux提权类 automated penetration testing chain. 触发词: Linux提权类。 | 1/1 | 覆寫特徵 |
| `linux-privilege-escalation` | Execute systematic privilege escalation assessments on Linux systems to identify and exploit misconfigurations, vulnerable services, and security weaknesses that allow e… | 1/1 |  |
| `linux-service-exploitation` | Linux service vulnerabilities including cron job exploitation, systemd service abuse, and init.d script manipulation | 1/1 |  |
| `living-off-the-land` | Evasion Chain Phase 4/白名单LivingOffTheLand. 触发词: 白名单LivingOffTheLand。 | 1/1 | 覆寫特徵 |
| `llm-prompt-injection` | LLM prompt injection playbook. Use when testing AI/LLM applications for direct injection, indirect injection via RAG/browsing, tool abuse, data exfiltration, MCP securit… | 1/1 | 覆寫特徵 |
| `macos-process-injection` | macOS process injection playbook. Use when you need to inject code into running or launching macOS processes via dylib hijacking, DYLD environment variables, XPC exploit… | 1/1 |  |
| `macos-security-bypass` | macOS security bypass playbook. Use when targeting macOS endpoints and need to bypass TCC, Gatekeeper, SIP, sandbox, code signing, or entitlement-based protections durin… | 1/1 |  |
| `managing-cloud-identity-with-okta` | This skill covers implementing Okta as a centralized identity provider for cloud environments, configuring SSO integration with AWS, Azure, and GCP, deploying phishing-… | 1/1 |  |
| `memory-shell-injection` | Exploit Chain Phase 4/内存马注入. 触发词: 内存马注入。 | 1/1 | 覆寫特徵 |
| `Methodology Chain` | 方法论框架类 automated penetration testing chain. 触发词: 方法论框架类。 | 1/1 | 覆寫特徵 |
| `mitm-phishing-/-evilginx` | Social Engineering Chain Phase 7/中间人钓鱼. 触发词: 中间人钓鱼。 | 1/1 | 覆寫特徵 |
| `monitoring-darkweb-sources` | Monitors dark web forums, marketplaces, paste sites, and ransomware leak sites for mentions of organizational assets, leaked credentials, threatened attacks, and threat… | 1/1 |  |
| `multi-purpose-attack-frameworks` | Framework Chain Phase 3/多功能攻击框架. 触发词: 多功能攻击框架。 | 1/1 | 覆寫特徵 |
| `odoo-security-rules` | Expert in Odoo access control: ir.model.access.csv, record rules (ir.rule), groups, and multi-company security patterns. | 1/1 |  |
| `offline-hash-cracking` | Credential Breach Chain Phase 13/离线哈希破解. 触发词: 离线哈希破解。 | 1/1 | 覆寫特徵 |
| `online-brute-force` | Credential Breach Chain Phase 8/在线口令爆破. 触发词: 在线口令爆破。 | 1/1 | 覆寫特徵 |
| `open-redirect` | Open redirect playbook. Use when URL parameters, form actions, or JavaScript sinks control navigation targets and may redirect users to attacker-controlled destinations. | 2/2 |  |
| `parameter-&-endpoint-discovery` | Recon Chain Phase 7/参数与端点发现. 触发词: 参数与端点发现。 | 1/1 | 覆寫特徵 |
| `passive-recon-&-osint` | Recon Chain Phase 15/被动侦察OSINT. 触发词: 被动侦察OSINT。 | 1/1 | 覆寫特徵 |
| `payload-gen-&-obfuscation` | Evasion Chain Phase 6/载荷生成与混淆. 触发词: 载荷生成与混淆。 | 1/1 | 覆寫特徵 |
| `pentest-auth-bypass` | Test authentication and session management controls for bypass and account takeover scenarios. | 1/1 |  |
| `pentest-c2-operator` | Set up authorized C2 simulation workflows and measure defensive detection outcomes. | 1/1 |  |
| `pentest-checklist` | Provide a comprehensive checklist for planning, executing, and following up on penetration tests. Ensure thorough preparation, proper scoping, and effective remediation… | 1/1 |  |
| `pentest-cloud-auditor` | Assess AWS, Azure, and GCP controls for IAM escalation and cloud service exposure. | 1/1 |  |
| `pentest-container-k8s` | Test Docker and Kubernetes security controls for RBAC abuse, breakout, and secret exposure. | 1/1 |  |
| `pentest-data-exfil-tester` | Test egress and DLP controls using synthetic canary data across authorized exfiltration channels. | 1/1 |  |
| `pentest-engagement-planner` | Define legal scope, rules of engagement, and authorization artifacts for downstream pentest execution. | 1/1 |  |
| `pentest-lateral-movement` | Assess lateral movement and pivot paths across authorized internal trust boundaries. | 1/1 |  |
| `pentest-output-standards` | 输出规范:中文分析,思维链,漏洞报告模板,负结果,黑板状态总览,改动台账,死锁突破。 Use when reporting findings, maintaining change ledger, or formatting pentest output. | 1/1 |  |
| `pentest-recon-osint` | Perform passive reconnaissance and leak intelligence collection with no direct contact to target systems. | 1/1 |  |
| `pentest-redteam-ops` | Coordinate autonomous pentest skills with dependency enforcement, deconfliction, and emergency stop controls. | 1/1 |  |
| `pentest-report-generator` | Aggregate findings and generate multi-format pentest reports with remediation roadmap and risk scoring. | 1/1 |  |
| `pentest-social-engineer` | Design phishing and social engineering simulations with explicit authorization and measurable outcomes. | 1/1 |  |
| `pentest-tool` | Autonomous penetration testing framework. Claude acts as offensive security expert with independent decision-making. Provides methodology and principles, not command scr… | 1/1 |  |
| `pentest-vuln-analyzer` | Correlate scanner results with CVE and exploit intelligence and prioritize by CVSS and exploitability. | 1/1 |  |
| `pentesting-distributions` | Framework Chain Phase 4/渗透测试发行版. 触发词: 渗透测试发行版。 | 1/1 | 覆寫特徵 |
| `pentesting-workflow` | Methodology Chain Phase 4/渗透测试流程. 触发词: 渗透测试流程。 | 1/1 | 覆寫特徵 |
| `performing-alert-triage-with-elastic-siem` | Perform systematic alert triage in Elastic Security SIEM to rapidly classify, prioritize, and investigate security alerts for SOC operations. | 1/1 |  |
| `performing-asset-criticality-scoring-for-vulns` | Develop and apply a multi-factor asset criticality scoring model to weight vulnerability prioritization based on business impact, data sensitivity, and operational impor… | 1/1 |  |
| `performing-authenticated-scan-with-openvas` | Configure and execute authenticated vulnerability scans using OpenVAS/Greenbone Vulnerability Management with SSH and SMB credentials for comprehensive host-level assess… | 1/1 |  |
| `performing-authenticated-vulnerability-scan` | Authenticated (credentialed) vulnerability scanning uses valid system credentials to log into target hosts and perform deep inspection of installed software, patches, co… | 1/1 |  |
| `performing-aws-account-enumeration-with-scout-suite` | Perform comprehensive security posture assessment of AWS accounts using ScoutSuite to enumerate resources, identify misconfigurations, and generate actionable security r… | 1/1 |  |
| `performing-clickjacking-attack-test` | Testing web applications for clickjacking vulnerabilities by assessing frame embedding controls and crafting proof-of-concept overlay attacks during authorized security… | 2/2 |  |
| `performing-cloud-asset-inventory-with-cartography` | Perform comprehensive cloud asset inventory and relationship mapping using Cartography to build a Neo4j security graph of infrastructure assets, IAM permissions, and att… | 1/1 |  |
| `performing-container-image-hardening` | This skill covers hardening container images by minimizing attack surface, removing unnecessary packages, implementing multi-stage builds, configuring non-root users, an… | 1/1 |  |
| `performing-credential-access-with-lazagne` | Extract stored credentials from compromised endpoints using the LaZagne post-exploitation tool to recover passwords from browsers, databases, system vaults, and applicat… | 1/1 |  |
| `performing-docker-bench-security-assessment` | Docker Bench for Security is an open-source script that checks dozens of common best practices around deploying Docker containers in production. Based on the CIS Docker… | 2/2 |  |
| `performing-initial-access-with-evilginx3` | Perform authorized initial access using EvilGinx3 adversary-in-the-middle phishing framework to capture session tokens and bypass multi-factor authentication during red… | 2/2 |  |
| `performing-open-source-intelligence-gathering` | Open Source Intelligence (OSINT) gathering is the first active phase of a red team engagement, where operators collect publicly available information about the target or… | 2/2 |  |
| `performing-osint-with-spiderfoot` | Automate OSINT collection using SpiderFoot REST API and CLI for target profiling, module-based reconnaissance, and structured result analysis across 200+ data sources | 2/2 |  |
| `performing-paste-site-monitoring-for-credentials` | Monitor paste sites like Pastebin and GitHub Gists for leaked credentials, API keys, and sensitive data dumps using automated scraping and keyword matching to detect bre… | 2/2 |  |
| `performing-phishing-simulation-with-gophish` | GoPhish is an open-source phishing simulation framework used by security teams to conduct authorized phishing awareness campaigns. It provides campaign management, email… | 1/1 |  |
| `performing-physical-intrusion-assessment` | Conduct authorized physical penetration testing using tailgating, badge cloning, lock bypassing, and rogue device deployment to evaluate facility security controls. | 1/1 |  |
| `performing-privilege-escalation-assessment` | Performs privilege escalation assessments on compromised Linux and Windows systems to identify paths from low-privilege access to root or SYSTEM-level control. The teste… | 2/1 |  |
| `performing-privilege-escalation-on-linux` | Linux privilege escalation involves elevating from a low-privilege user account to root access on a compromised system. Red teams exploit misconfigurations, vulnerable s… | 2/2 |  |
| `performing-red-team-phishing-with-gophish` | Automate GoPhish phishing simulation campaigns using the Python gophish library. Creates email templates with tracking pixels, configures SMTP sending profiles, builds t… | 2/2 |  |
| `performing-security-headers-audit` | Auditing HTTP security headers including CSP, HSTS, X-Frame-Options, and cookie attributes to identify missing or misconfigured browser-level protections. | 2/1 |  |
| `performing-serverless-function-security-review` | Performing security reviews of serverless functions across AWS Lambda, Azure Functions, and GCP Cloud Functions to identify overly permissive execution roles, insecure e… | 1/1 |  |
| `performing-subdomain-enumeration-with-subfinder` | Enumerate subdomains of target domains using ProjectDiscovery's Subfinder passive reconnaissance tool to map the attack surface during security assessments. | 2/1 |  |
| `performing-threat-landscape-assessment-for-sector` | Conduct a sector-specific threat landscape assessment by analyzing threat actor targeting patterns, common attack vectors, and industry-specific vulnerabilities to infor… | 1/1 |  |
| `phishing-email-attacks` | Social Engineering Chain Phase 10/钓鱼邮件攻击. 触发词: 钓鱼邮件攻击。 | 1/1 | 覆寫特徵 |
| `phishing-page-cloning` | Social Engineering Chain Phase 11/钓鱼页面克隆. 触发词: 钓鱼页面克隆。 | 1/1 | 覆寫特徵 |
| `php` | PHP programming language basics, syntax, and security best practices | 1/1 |  |
| `php-auth-audit` | PHP Web 源码鉴权机制审计工具。从源码中识别所有认证/鉴权实现并分析风险，输出路由-鉴权映射与漏洞分析（含 PoC 与修复建议）。 | 1/1 |  |
| `php-exploit-chain-audit` | PHP 利用链/POP(回弹)链聚合器。把已产出的各类漏洞报告按“前置条件满足”串成可利用链路叙事（不新增证据点字典）。 | 1/1 |  |
| `php-logic-audit` | PHP Web 业务逻辑漏洞审计工具。识别认证/授权以外的逻辑缺陷：Mass Assignment、流程绕过、竞态条件、状态机缺陷、支付/权限时序漏洞等，输出证据链、分级、PoC 与修复建议（禁止省略）。 | 1/1 |  |
| `php-route-tracer` | PHP Web 路由到 Sink 的多层数据流追踪工具。根据用户指定路由，追踪从 handler 到最终敏感操作点，输出层级证据、参数变量追踪、可控性分析（不做漏洞结论）。 | 1/1 |  |
| `php-vuln-scanner` | PHP 组件版本漏洞检测工具。扫描 composer.json / composer.lock 或 jar/包元信息，匹配已知漏洞规则并输出报告（包含可能的触发点分析框架）。 | 1/1 |  |
| `poc-agent` | 基于指纹识别结果（tech_stack），优先匹配本地 POC；在用户明确授权时补充联网搜索 POC，并通过 http_test.py 验证已知漏洞。 工作流程：读取指纹识别结果 → 提取关键字搜索本地与联网 POC → 整理待验证清单 → 解析 POC 定义 → 构造 http_test.py 命令 → 评估匹配器 → 回填 find… | 1/1 |  |
| `port-&-service-scan` | Recon Chain Phase 14/端口与服务扫描. 触发词: 端口与服务扫描。 | 1/1 | 覆寫特徵 |
| `post-exploitation` | 后渗透/提权+凭据破解+密码学:反弹shell,Linux/Windows提权,横向,隧道,免杀,C2持久化,hashcat/Padding Oracle/hash长度扩展。Use when post-exploitation, privilege escalation, lateral movement, or cracking cr… | 1/1 |  |
| `process-injection-&-memory-execution` | Evasion Chain Phase 7/进程注入与内存执行. 触发词: 进程注入与内存执行。 | 1/1 | 覆寫特徵 |
| `prototype-pollution-advanced` | Advanced prototype pollution playbook — server-side RCE, client-side gadgets, filter bypasses, and detection techniques. Companion to ../prototype-pollution/ for basics.… | 1/1 |  |
| `qr-code-phishing` | Social Engineering Chain Phase 2/QR二维码钓鱼. 触发词: QR二维码钓鱼。 | 1/1 | 覆寫特徵 |
| `Recon Chain` | Recon & Intel automated penetration testing chain. 触发词: 侦察信息收集。 | 1/1 | 覆寫特徵 |
| `recon-and-methodology` | Reconnaissance and methodology playbook. Use when mapping assets, discovering endpoints, fingerprinting technology, and building a structured testing plan for a new targ… | 2/2 |  |
| `recon-for-sec` | Entry P1 category router for reconnaissance and methodology. Use when mapping scope, discovering assets, fingerprinting technology, building endpoint inventory, and choo… | 2/2 |  |
| `red-vs-blue-platforms` | Lab & Training Chain Phase 6/攻防演练平台. 触发词: 攻防演练平台。 | 1/1 | 覆寫特徵 |
| `rev-struct` | Reconstruct data structures by analyzing memory access patterns across functions | 3/1 |  |
| `rop-chain-construction` | Exploit Chain Phase 1/ROP链构造. 触发词: ROP链构造。 | 1/1 | 覆寫特徵 |
| `rsa-attack-techniques` | RSA attack playbook for CTF and real-world cryptanalysis. Use when given RSA parameters (n, e, c) and need to recover plaintext by exploiting weak keys, small exponents,… | 1/1 |  |
| `sandbox-&-edr-evasion` | Evasion Chain Phase 3/沙箱与EDR规避. 触发词: 沙箱与EDR规避。 | 1/1 | 覆寫特徵 |
| `scanning-containers-with-trivy-in-cicd` | This skill covers integrating Aqua Security's Trivy scanner into CI/CD pipelines for comprehensive container image vulnerability detection. It addresses scanning Docker… | 2/1 |  |
| `scanning-docker-images-with-trivy` | Trivy is a comprehensive open-source vulnerability scanner by Aqua Security that detects vulnerabilities in OS packages, language-specific dependencies, misconfiguration… | 2/2 |  |
| `scanning-kubernetes-manifests-with-kubesec` | Perform security risk analysis on Kubernetes resource manifests using Kubesec to identify misconfigurations, privilege escalation risks, and deviations from security bes… | 2/2 |  |
| `scrapling-official` | Scrape web pages using Scrapling with anti-bot bypass (like Cloudflare Turnstile), stealth headless browsing, spiders framework, adaptive scraping, and JavaScript render… | 1/1 |  |
| `secure-code-review` | 安全代码审计深度专业技能：多语言漏洞模式识别（Java/Python/Go/Node.js/C#/PHP）、数据流追踪、认证授权审计、供应链安全、从代码缺陷到可利用漏洞完整分析链 | 1/1 |  |
| `securing-azure-with-microsoft-defender` | This skill instructs security practitioners on deploying Microsoft Defender for Cloud as a cloud-native application protection platform for Azure, multi-cloud, and hybri… | 1/1 |  |
| `securing-container-registry-with-harbor` | Harbor is an open-source container registry that provides security features including vulnerability scanning (integrated Trivy), image signing (Notary/Cosign), RBAC, con… | 2/2 |  |
| `security-awareness-training` | 安全意识培训深度专业技能：社会工程学攻防实战、钓鱼演练设计与评估、安全编码最佳实践、红蓝对抗培训、从意识提升到技能转化的完整培训体系 | 1/1 |  |
| `security-requirement-extraction` | Derive security requirements from threat models and business context. Use when translating threats into actionable requirements, creating security user stories, or build… | 1/1 |  |
| `security-scanning-security-sast` | 'Static Application Security Testing (SAST) for code vulnerability | 1/1 |  |
| `security_reporter` | 安全报告编写助手是一款专注于网络安全领域的智能报告生成工具，当用户提出需要针对给出的漏洞信息给出分析报告时，需要基于漏洞编号、名称或安全扫描工具报告，自动生成符合行业标准的漏洞分析报告，包含漏洞背景、漏洞描述、漏洞原理、漏洞利用条件和修复要求等核心内容，帮助安全从业者快速生成标准化、专业的安全报告。 | 1/1 |  |
| `service-version-fingerprint` | Recon Chain Phase 12/服务版本指纹. 触发词: 服务版本指纹。 | 1/1 | 覆寫特徵 |
| `signature-&-pattern-bypass` | Evasion Chain Phase 5/签名与特征绕过. 触发词: 签名与特征绕过。 | 1/1 | 覆寫特徵 |
| `smart-contract-vulnerabilities` | Smart contract vulnerability playbook. Use when auditing Solidity/EVM contracts for reentrancy, integer overflow, access control, delegatecall, flash loan, signature rep… | 1/1 |  |
| `smb-attacks` | Domain Infiltration Chain Phase 8/SMB攻击. 触发词: SMB攻击。 | 1/1 | 覆寫特徵 |
| `smishing-/-sms-phishing` | Social Engineering Chain Phase 3/Smishing短信钓鱼. 触发词: Smishing短信钓鱼。 | 1/1 | 覆寫特徵 |
| `Social Engineering Chain` | 社工钓鱼类 automated penetration testing chain. 触发词: 社工钓鱼类。 | 1/1 | 覆寫特徵 |
| `social-engineering-methodology` | Social Engineering Chain Phase 9/社工方法论. 触发词: 社工方法论。 | 1/1 | 覆寫特徵 |
| `solidity-security` | Master smart contract security best practices, vulnerability prevention, and secure Solidity development patterns. | 1/1 |  |
| `solve-challenge` | Solves CTF challenges by performing first-pass triage, identifying the dominant category, and routing execution to the right specialized ctf-* skill. Use when the user g… | 1/1 |  |
| `spear-phishing` | Social Engineering Chain Phase 12/鱼叉式钓鱼. 触发词: 鱼叉式钓鱼。 | 1/1 | 覆寫特徵 |
| `special-format-cracking` | Credential Breach Chain Phase 12/特定格式破解. 触发词: 特定格式破解。 | 1/1 | 覆寫特徵 |
| `src-framework-poc` | 框架/中间件/OA系统nday漏洞POC索引与利用技能。覆盖泛微OA、用友NC、通达OA、万户OA、致远OA、ThinkPHP、海康大华摄像头、1Panel、宝塔、钉钉、百卓、亿邮等主流产品的已知漏洞POC速查。基于FrameVul索引和多个POC仓库。触发词：OA漏洞、框架漏洞、nday利用、泛微、用友、通达、POC速查、漏洞验证、已… | 1/1 |  |
| `src-recon-collection` | SRC漏洞挖掘全流程自动化技能——覆盖子域名收集、端口扫描、指纹识别、JS分析、目录爆破、漏洞扫描、弱口令爆破的完整攻击面映射。集成Komo、JSFScan、Reconator、Secbuild等13个GitHub顶级工具的精华方法论。触发词：SRC挖洞、众测、打点、信息收集、资产收集、子域名、recon、bug bounty、渗透测试。 | 1/1 |  |
| `ssh/rdp-brute-force` | Credential Breach Chain Phase 3/SSH-RDP远程爆破. 触发词: SSH-RDP远程爆破。 | 1/1 | 覆寫特徵 |
| `ssti-server-side-template-injection` | SSTI playbook. Use when template expressions, server-side rendering, preview features, or templating engines may evaluate attacker-controlled content. | 2/2 |  |
| `stack-&-heap-exploitation` | Exploit Chain Phase 7/栈与堆溢出利用. 触发词: 栈与堆溢出利用。 | 1/1 | 覆寫特徵 |
| `subdomain-enumeration` | Recon Chain Phase 10/子域枚举. 触发词: 子域枚举。 | 1/1 | 覆寫特徵 |
| `subdomain-takeover` | Subdomain takeover detection and exploitation playbook. Use when targets have dangling CNAME/NS/MX records pointing to deprovisioned cloud resources, expired third-party… | 1/1 |  |
| `subdomain-takeover-detect` | Recon Chain Phase 9/子域名接管检测. 触发词: 子域名接管检测。 | 1/1 | 覆寫特徵 |
| `symmetric-cipher-attacks` | Symmetric cipher attack playbook. Use when exploiting block cipher mode weaknesses (CBC padding oracle, ECB cut-and-paste, bit flipping), stream cipher key reuse, or mee… | 1/1 |  |
| `syscall-techniques` | Direct system call techniques to bypass userland API hooks set by EDR solutions | 1/1 |  |
| `tech-stack-fingerprinting` | Recon Chain Phase 11/技术栈与指纹识别. 触发词: 技术栈与指纹识别。 | 1/1 | 覆寫特徵 |
| `testing-for-broken-access-control` | Systematically testing web applications for broken access control vulnerabilities including privilege escalation, missing function-level checks, and insecure direct obje… | 1/1 |  |
| `testing-for-email-header-injection` | Test web application email functionality for SMTP header injection vulnerabilities that allow attackers to inject additional email headers, modify recipients, and abuse… | 1/1 |  |
| `testing-for-open-redirect-vulnerabilities` | Identify and test open redirect vulnerabilities in web applications by analyzing URL redirection parameters, bypass techniques, and exploitation chains for phishing and… | 1/1 |  |
| `testing-for-sensitive-data-exposure` | Identifying sensitive data exposure vulnerabilities including API key leakage, PII in responses, insecure storage, and unprotected data transmission during security asse… | 1/1 |  |
| `threat-intelligence-&-alerts` | Intelligence Chain Phase 5/漏洞情报与预警. 触发词: 漏洞情报与预警。 | 1/1 | 覆寫特徵 |
| `tracking-threat-actor-infrastructure` | Threat actor infrastructure tracking involves monitoring and mapping adversary-controlled assets including command-and-control (C2) servers, phishing domains, exploit ki… | 1/1 |  |
| `triaging-security-incident-with-ir-playbook` | Classify and prioritize security incidents using structured IR playbooks to determine severity, assign response teams, and initiate appropriate response procedures. | 1/1 |  |
| `triaging-vulnerabilities-with-ssvc-framework` | Triage and prioritize vulnerabilities using CISA's Stakeholder-Specific Vulnerability Categorization (SSVC) decision tree framework to produce actionable remediation pri… | 1/1 |  |
| `vendor-security-advisories` | Intelligence Chain Phase 3/厂商安全公告. 触发词: 厂商安全公告。 | 1/1 | 覆寫特徵 |
| `vishing-/-voice-phishing` | Social Engineering Chain Phase 5/Vishing电话钓鱼. 触发词: Vishing电话钓鱼。 | 1/1 | 覆寫特徵 |
| `voidshell-linux-av-bypass` | VoidShell — Linux ELF 免杀打包工具。多层加密 + 内存执行 + 反沙箱，将 fscan/frp/C2 Beacon/RootHawk 等 Linux 工具打包为免杀版本，VT（VirusTotal）0 检测。VoidShell-fe 专攻 fork_exec 型程序免杀。触发词：voidshell、linux免杀、… | 1/1 |  |
| `vuln-analysis-agent` | Vibe Pentest 漏洞综合分析 Agent。固定负责 Phase 5.5 攻击链分析与 Phase 5.6 漏洞证据复查：读取已启用的渗透 Agent 的 findings，输出 attack_chains.json | 1/1 |  |
| `vuln-reproduction-&-poc` | Exploit Chain Phase 11/漏洞复现与POC验证. 触发词: 漏洞复现与POC验证。 | 1/1 | 覆寫特徵 |
| `vulnerability-aggregators` | Intelligence Chain Phase 6/漏洞聚合平台. 触发词: 漏洞聚合平台。 | 1/1 | 覆寫特徵 |
| `vulnerability-assessment` | 漏洞评估深度专业技能：漏洞全生命周期管理、CVSS评分与风险评估、漏洞验证与PoC开发、修复验证与回归测试、从发现到闭环完整漏洞管理流程 | 1/1 |  |
| `vulnerability-management` | Framework Chain Phase 5/漏洞管理平台. 触发词: 漏洞管理平台。 | 1/1 | 覆寫特徵 |
| `vulnerability-reproduction` | Lab & Training Chain Phase 7/真实漏洞复现环境. 触发词: 真实漏洞复现环境。 | 1/1 | 覆寫特徵 |
| `watering-hole-attacks` | Social Engineering Chain Phase 8/水坑攻击. 触发词: 水坑攻击。 | 1/1 | 覆寫特徵 |
| `web-login-brute-force` | Credential Breach Chain Phase 4/Web登录爆破. 触发词: Web登录爆破。 | 1/1 | 覆寫特徵 |
| `whaling-/-executive-phishing` | Social Engineering Chain Phase 13/鲸钓-高管钓鱼. 触发词: 鲸钓-高管钓鱼。 | 1/1 | 覆寫特徵 |
| `windows-privilege-escalation` | Provide systematic methodologies for discovering and exploiting privilege escalation vulnerabilities on Windows systems during penetration testing engagements. | 1/1 |  |
| `windows-token-privileges` | Windows token manipulation, impersonation, and privilege escalation techniques including the complete Potato family (Juicy Potato, PrintSpoofer, Rogue Potato) | 1/1 |  |
| `wordlist-&-rule-generation` | Credential Breach Chain Phase 9/字典与规则生成. 触发词: 字典与规则生成。 | 1/1 | 覆寫特徵 |
| `zero-day-&-wild-exploitation` | Intelligence Chain Phase 1/0day与在野利用. 触发词: 0day与在野利用。 | 1/1 | 覆寫特徵 |
| `内容与目录发现` | Recon Chain Phase 6/内容与目录发现. 触发词: 内容与目录发现。 | 1/1 | 覆寫特徵 |
| `线下哈希破解` | Credential Breach Chain Phase 14/线下哈希破解. 触发词: 线下哈希破解。 | 1/1 | 覆寫特徵 |

### 寫作／內容／研究（8）

| Skill | 說明 | 定義/版本 | 旗標 |
|---|---|---:|---|
| `brand-voice` | Build a source-derived writing style profile from real posts, essays, launch notes, docs, or site copy, then reuse that profile across content, outreach, and social work… | 1/1 |  |
| `collaboration-&-reporting` | Framework Chain Phase 2/协作与报告平台. 触发词: 协作与报告平台。 | 1/1 | 覆寫特徵 |
| `content-engine` | Create platform-native content systems for X, LinkedIn, TikTok, YouTube, newsletters, and repurposed multi-platform campaigns. Use when the user wants social posts, thre… | 1/1 |  |
| `crlf-injection` | CRLF injection playbook. Use when user input reaches HTTP response headers, Location redirects, Set-Cookie values, or log files where carriage-return/line-feed character… | 3/3 | 覆寫特徵 |
| `crosspost` | Multi-platform content distribution across X, LinkedIn, Threads, and Bluesky. Adapts content per platform using content-engine patterns. Never posts identical content cr… | 1/1 |  |
| `csm-reporting-markdown` | Markdown安全报告模板 — 报告撰写模块 \| Reporting \| 难度★★ \| PTES框架 | 1/1 |  |
| `deep-research` | Multi-source deep research using firecrawl and exa MCPs. Searches the web, synthesizes findings, and delivers cited reports with source attribution. Use when the user wa… | 1/1 |  |
| `report-template-&-writing` | Methodology Chain Phase 2/报告模板与撰写. 触发词: 报告模板与撰写。 | 1/1 | 覆寫特徵 |

### 生產力／協作／自動化（4）

| Skill | 說明 | 定義/版本 | 旗標 |
|---|---|---:|---|
| `dl-transformer-finetune` | Build transformer fine-tuning run plans with task settings, hyperparameters, and model-card outputs. Use for repeatable Hugging Face or PyTorch finetuning workflows. | 1/1 |  |
| `hunting-for-scheduled-task-persistence` | Hunt for adversary persistence via Windows Scheduled Tasks by analyzing task creation events, suspicious task actions, and unusual scheduling patterns. | 2/1 |  |
| `hunting-for-suspicious-scheduled-tasks` | Hunt for adversary persistence and execution via Windows scheduled tasks by analyzing task creation events, suspicious task properties, and unusual execution patterns th… | 1/1 |  |
| `implementing-file-integrity-monitoring-with-aide` | Configure AIDE (Advanced Intrusion Detection Environment) for file integrity monitoring including baseline creation, scheduled integrity checks, change detection, and al… | 1/1 |  |

### 其他（112）

| Skill | 說明 | 定義/版本 | 旗標 |
|---|---|---:|---|
| `analyzing-apt-group-with-mitre-navigator` | Analyze advanced persistent threat (APT) group techniques using MITRE ATT&CK Navigator to create layered heatmaps of adversary TTPs for detection gap analysis and threat… | 2/2 |  |
| `analyzing-campaign-attribution-evidence` | Campaign attribution analysis involves systematically evaluating evidence to determine which threat actor or group is responsible for a cyber operation. This skill cover… | 1/1 |  |
| `analyzing-linux-system-artifacts` | Examine Linux system artifacts including auth logs, cron jobs, shell history, and system configuration to uncover evidence of compromise or unauthorized activity. | 1/1 |  |
| `analyzing-persistence-mechanisms-in-linux` | Detect and analyze Linux persistence mechanisms including crontab entries, systemd service units, LD_PRELOAD hijacking, bashrc modifications, and authorized_keys backdoo… | 1/1 |  |
| `analyzing-ransomware-encryption-mechanisms` | Analyzes encryption algorithms, key management, and file encryption routines used by ransomware families to assess decryption feasibility, identify implementation weakne… | 2/1 |  |
| `analyzing-windows-registry-for-artifacts` | Extract and analyze Windows Registry hives to uncover user activity, installed software, autostart entries, and evidence of system compromise. | 1/1 |  |
| `as-rep-roasting` | Domain Infiltration Chain Phase 2/AS-REP Roast. 触发词: AS-REP Roast。 | 1/1 | 覆寫特徵 |
| `bloodhound-domain-analysis` | Domain Infiltration Chain Phase 3/BloodHound域分析. 触发词: BloodHound域分析。 | 1/1 | 覆寫特徵 |
| `build-release` | — | 1/1 |  |
| `building-role-mining-for-rbac-optimization` | Apply bottom-up and top-down role mining techniques to discover optimal RBAC roles from existing user-permission assignments, reducing role explosion and enforcing least… | 1/1 |  |
| `bun-runtime` | Bun as runtime, package manager, bundler, and test runner. When to choose Bun vs Node, migration notes, and Vercel support. | 1/1 |  |
| `c` | C programming language for system programming, memory management, and low-level operations | 1/1 |  |
| `c2-channel-establishment` | Exfiltration Chain Phase 1/C2通道建立. 触发词: C2通道建立。 | 1/1 | 覆寫特徵 |
| `c2-frameworks` | Framework Chain Phase 1/C2框架. 触发词: C2框架。 | 1/1 | 覆寫特徵 |
| `capabilities-&-permissions` | Linux PrivEsc Chain Phase 1/Capabilities与特殊权限. 触发词: Capabilities与特殊权限。 | 1/1 | 覆寫特徵 |
| `caveman-commit` | 极致压缩的 commit message 生成器。去除提交信息噪声，保留意图和逻辑。 遵循 Conventional Commits 格式。主题 ≤50 字符，body 仅写非显而易见的"为什么"。 触发词："写 commit"、"commit message"、"生成提交信息"、"/commit"。 自动在暂存变更时触发。 | 1/1 |  |
| `cmdi-command-injection` | Command injection playbook. Use when user input may reach shell commands, process execution, converters, import pipelines, or blind out-of-band command sinks. | 1/1 |  |
| `configuring-identity-aware-proxy-with-google-iap` | Configuring Google Cloud Identity-Aware Proxy (IAP) to enforce per-request identity verification for Compute Engine, App Engine, Cloud Run, and GKE services using access… | 1/1 |  |
| `cron-job-hijacking` | Linux PrivEsc Chain Phase 9/定时任务劫持. 触发词: 定时任务劫持。 | 1/1 | 覆寫特徵 |
| `crypto-bd-agent` | Production-tested patterns for building AI agents that autonomously discover, > evaluate, and acquire token listings for cryptocurrency exchanges. | 1/1 |  |
| `csm-covering-tracks-amsi-edr` | AMSI绕过与EDR规避 — 痕迹清除模块 \| Covering Tracks \| 难度★★★★★ \| PTES框架 | 1/1 |  |
| `csm-cryptography-pki` | 加密算法与密钥管理 — 密码学与PKI模块 \| Cryptography & PKI \| 难度★★★★ \| PTES框架 | 1/1 |  |
| `csm-cryptography-pki-pki` | PKI架构与证书安全管理 — 密码学与PKI模块 \| Cryptography & PKI \| 难度★★★★ \| PTES框架 | 1/1 |  |
| `csm-cryptography-pki-tls-ssl` | TLS/SSL安全配置与审计 — 密码学与PKI模块 \| Cryptography & PKI \| 难度★★★ \| PTES框架 | 1/1 |  |
| `csm-identity-access-management-ad` | AD域安全与攻击路径分析 — 身份与访问管理模块 \| Identity & Access Management \| 难度★★★★★ \| PTES框架 | 1/1 |  |
| `csm-identity-access-management-iam` | 企业IAM策略与架构 — 身份与访问管理模块 \| Identity & Access Management \| 难度★★★ \| PTES框架 | 1/1 |  |
| `csm-identity-access-management-pam` | PAM特权账号管理 — 身份与访问管理模块 \| Identity & Access Management \| 难度★★★★ \| PTES框架 | 1/1 |  |
| `csm-lateral-movement` | 横向移动 — 横向移动模块 \| Lateral Movement \| 难度★★★ \| PTES框架 | 1/1 |  |
| `csm-lateral-movement-psexec-wmi` | PsExec与WMI远程执行 — 横向移动模块 \| Lateral Movement \| 难度★★★ \| PTES框架 | 1/1 |  |
| `csm-persistence` | 持久化 — 持久化模块 \| Persistence \| 难度★★★ \| PTES框架 | 1/1 |  |
| `csm-persistence-office` | Office应用程序持久化 — 持久化模块 \| Persistence \| 难度★★★★ \| PTES框架 | 1/1 |  |
| `csm-ransomware-defense` | 勒索软件攻击链分析与检测 — 勒索软件防御模块 \| Ransomware Defense \| 难度★★★★ \| PTES框架 | 1/1 |  |
| `csm-red-blue-team` | 红队评估方法论 — 红蓝对抗模块 \| Red/Blue Team \| 难度★★★★★ \| PTES框架 | 1/1 |  |
| `csm-red-blue-team-bas` | BAS攻击模拟平台 — 红蓝对抗模块 \| Red/Blue Team \| 难度★★★★ \| PTES框架 | 1/1 |  |
| `csm-soc-operations-siem` | SIEM告警规则与关联分析 — SOC运营模块 \| SOC Operations \| 难度★★★★ \| PTES框架 | 1/1 |  |
| `csm-soc-operations-soar` | 安全自动化与编排(SOAR) — SOC运营模块 \| SOC Operations \| 难度★★★★ \| PTES框架 | 1/1 |  |
| `csm-soc-operations-soc` | SOC事件分级与响应流程 — SOC运营模块 \| SOC Operations \| 难度★★★ \| PTES框架 | 1/1 |  |
| `cyberstrike-eino-demo` | 满配示例技能包：SKILL.md + scripts/、references/、assets/ 等可选目录；验证 Eino skill 与 HTTP 包内路径（仅授权安全测试与教学）。 | 1/1 |  |
| `deploy-infra` | — | 1/1 |  |
| `deploying-software-defined-perimeter` | Deploying Software Defined Perimeter | 1/1 |  |
| `detecting-insider-threat-behaviors` | Detect insider threat behavioral indicators including unusual data access, off-hours activity, mass file downloads, privilege abuse, and resignation-correlated data thef… | 1/1 |  |
| `detecting-process-hollowing-technique` | Detect process hollowing (T1055.012) by analyzing memory-mapped sections, hollowed process indicators, and parent-child process anomalies in EDR telemetry. | 2/1 |  |
| `detecting-t1055-process-injection-with-sysmon` | Detect process injection techniques (T1055) including classic DLL injection, process hollowing, and APC injection by analyzing Sysmon events for cross-process memory ope… | 1/1 |  |
| `detecting-wmi-persistence` | Detect WMI event subscription persistence by analyzing Sysmon Event IDs 19, 20, and 21 for malicious EventFilter, EventConsumer, and FilterToConsumerBinding creation. | 2/1 |  |
| `domain-persistence` | Domain Infiltration Chain Phase 11/域持久化. 触发词: 域持久化。 | 1/1 | 覆寫特徵 |
| `eval-harness` | Formal evaluation framework for Claude Code sessions implementing eval-driven development (EDD) principles | 1/1 |  |
| `field-journal` | — | 1/1 |  |
| `golden-&-silver-tickets` | Domain Infiltration Chain Phase 14/黄金白银票据. 触发词: 黄金白银票据。 | 1/1 | 覆寫特徵 |
| `html` | HTML5 markup language for web page structure and semantic elements | 1/1 |  |
| `hunting-for-domain-fronting-c2-traffic` | Detect domain fronting C2 traffic by analyzing SNI vs HTTP Host header mismatches in proxy logs and TLS certificate discrepancies using pyOpenSSL for certificate inspect… | 1/1 |  |
| `hunting-for-lateral-movement-via-wmi` | Detect WMI-based lateral movement by analyzing Windows Event ID 4688 process creation and Sysmon Event ID 1 for WmiPrvSE.exe child process patterns, remote process execu… | 2/2 |  |
| `hunting-for-living-off-the-land-binaries` | Proactively hunt for adversary abuse of legitimate system binaries (LOLBins) to execute malicious payloads while evading detection. | 1/1 |  |
| `hunting-for-lolbins-execution-in-endpoint-logs` | Hunt for adversary abuse of Living Off the Land Binaries (LOLBins) by analyzing endpoint process creation logs for suspicious execution patterns of legitimate Windows sy… | 1/1 |  |
| `hunting-for-persistence-mechanisms-in-windows` | Systematically hunt for adversary persistence mechanisms across Windows endpoints including registry, services, startup folders, and WMI subscriptions. | 2/1 |  |
| `hunting-for-persistence-via-wmi-subscriptions` | Hunt for adversary persistence through Windows Management Instrumentation event subscriptions by monitoring WMI consumer, filter, and binding creation events that execut… | 2/1 |  |
| `hunting-for-process-injection-techniques` | Detect process injection techniques (T1055) including CreateRemoteThread, process hollowing, and DLL injection via Sysmon Event IDs 8 and 10 and EDR process telemetry | 2/2 |  |
| `hunting-for-registry-persistence-mechanisms` | Hunt for registry-based persistence mechanisms including Run keys, Winlogon modifications, IFEO injection, and COM hijacking in Windows environments. | 2/1 |  |
| `hunting-for-registry-run-key-persistence` | Detect MITRE ATT&CK T1547.001 registry Run key persistence by analyzing Sysmon Event ID 13 logs and registry queries to identify malicious auto-start entries. | 2/2 |  |
| `hunting-for-webshells-in-web-servers` | Detect webshells planted on web servers by scanning for high-entropy files, suspicious PHP/JSP/ASP patterns (eval, base64_decode, system, passthru), recently modified fi… | 1/1 |  |
| `implementing-diamond-model-analysis` | The Diamond Model of Intrusion Analysis provides a structured framework for analyzing cyber intrusions by examining four core features: Adversary, Capability, Infrastruc… | 1/1 |  |
| `implementing-end-to-end-encryption-for-messaging` | End-to-end encryption (E2EE) ensures that only the communicating parties can read messages, with no intermediary (including the server) able to decrypt them. This skill… | 1/1 |  |
| `implementing-endpoint-detection-with-wazuh` | Deploy and configure Wazuh SIEM/XDR for endpoint detection including agent management, custom decoder and rule XML creation, alert querying via the Wazuh REST API, and a… | 1/1 |  |
| `implementing-google-workspace-sso-configuration` | Configure SAML 2.0 single sign-on for Google Workspace with a third-party identity provider, enabling centralized authentication and enforcing organization-wide access p… | 1/1 |  |
| `implementing-log-forwarding-with-fluentd` | Configure Fluentd and Fluent Bit for centralized log aggregation, routing, filtering, and enrichment across distributed infrastructure | 1/1 |  |
| `implementing-rbac-hardening-for-kubernetes` | Harden Kubernetes Role-Based Access Control by implementing least-privilege policies, auditing role bindings, eliminating cluster-admin sprawl, and integrating external… | 1/1 |  |
| `implementing-rsa-key-pair-management` | RSA (Rivest-Shamir-Adleman) is the most widely deployed asymmetric cryptographic algorithm, used for digital signatures, key exchange, and encryption. This skill covers… | 1/1 |  |
| `implementing-saml-sso-with-okta` | Implement SAML 2.0 Single Sign-On (SSO) using Okta as the Identity Provider (IdP). This skill covers end-to-end configuration of SAML authentication flows, attribute map… | 1/1 |  |
| `implementing-zero-knowledge-proof-for-authentication` | Zero-Knowledge Proofs (ZKPs) allow a prover to demonstrate knowledge of a secret (such as a password or private key) without revealing the secret itself. This skill impl… | 1/1 |  |
| `implementing-zero-standing-privilege-with-cyberark` | Deploy CyberArk Secure Cloud Access to eliminate standing privileges in hybrid and multi-cloud environments using just-in-time access with time, entitlement, and approva… | 1/1 |  |
| `jailbreak-engineering` | — | 1/1 |  |
| `kerberoasting` | Domain Infiltration Chain Phase 5/Kerberoasting. 触发词: Kerberoasting。 | 1/1 | 覆寫特徵 |
| `lateral-movement` | Domain Infiltration Chain Phase 12/横向移动. 触发词: 横向移动。 | 1/1 | 覆寫特徵 |
| `ml-experiment-tracker` | Plan reproducible ML experiment runs with explicit parameters, metrics, and artifacts. Use before model training to standardize tracking-ready experiment definitions. | 1/1 |  |
| `nfs-&-shared-dir` | Linux PrivEsc Chain Phase 3/NFS与共享目录. 触发词: NFS与共享目录。 | 1/1 | 覆寫特徵 |
| `omni-flow` | Use when the user explicitly says `omni-flow` or `羊`, or when this mode is already active in the conversation. It provides evidence-first analysis for a supplied artifac… | 1/1 |  |
| `path-&-env-hijack` | Linux PrivEsc Chain Phase 4/PATH与环境变量劫持. 触发词: PATH与环境变量劫持。 | 1/1 | 覆寫特徵 |
| `perf-optimize` | — | 1/1 |  |
| `performing-access-review-and-certification` | Conduct systematic access reviews and certifications to ensure users have appropriate access rights aligned with their roles. This skill covers review campaign design, r… | 1/1 |  |
| `performing-dark-web-monitoring-for-threats` | Dark web monitoring involves systematically scanning Tor hidden services, underground forums, paste sites, and dark web marketplaces to identify threats targeting an org… | 2/2 |  |
| `performing-dmarc-policy-enforcement-rollout` | Execute a phased DMARC rollout from p=none monitoring through p=quarantine to p=reject enforcement, ensuring all legitimate email sources are authenticated before blocki… | 1/1 |  |
| `performing-ssl-certificate-lifecycle-management` | SSL/TLS certificate lifecycle management encompasses the full process of requesting, issuing, deploying, monitoring, renewing, and revoking X.509 certificates. Poor cert… | 1/1 |  |
| `performing-web-application-scanning-with-nikto` | Nikto is an open-source web server and web application scanner that tests against over 7,000 potentially dangerous files/programs, checks for outdated versions of over 1… | 1/1 |  |
| `php-archive-extract-audit` | PHP Web 归档解压（Zip Slip/路径穿越）审计工具。识别解压条目名如何与目标目录拼接、是否存在 base dir 约束缺失，输出可利用性分级、可观测 PoC 与修复建议（禁止省略）。 | 1/1 |  |
| `php-cmd-audit` | PHP Web 源码命令注入审计工具。识别命令执行 Sink（exec/system/shell_exec 等），追踪用户输入进入命令拼接，输出可利用性分级、PoC 与修复建议（禁止省略）。 | 1/1 |  |
| `php-crlf-audit` | PHP Web 源码 CRLF/响应分割审计工具。识别用户输入进入 HTTP 响应头，分析换行/控制字符过滤与编码，输出分级、PoC 与修复建议（禁止省略）。 | 1/1 |  |
| `php-crypto-audit` | PHP Web 源码加密与密钥安全审计工具。识别弱哈希/弱加密/硬编码密钥/签名校验缺陷，输出分级、PoC 与修复建议（禁止省略）。 | 1/1 |  |
| `php-deser-audit` | PHP Web 源码反序列化/对象注入审计工具。识别 unserialize 注入点与可控数据来源，追踪魔术方法链，输出可利用性分级、PoC 与修复建议（禁止省略）。 | 1/1 |  |
| `php-expr-audit` | PHP Web 源码表达式注入（非模板）审计工具。识别用户可控表达式字符串进入表达式引擎求值/编译并最终导致敏感语义执行，输出可利用性分级、PoC 与修复建议（禁止省略）。 | 1/1 |  |
| `php-logging-audit` | PHP Web 安全日志与监控审计工具。识别安全事件缺失、敏感信息写入日志、日志注入/伪造风险，以及日志与告警链路缺陷，并输出可利用性分级、可观测 PoC 与修复建议（禁止省略）。 | 1/1 |  |
| `php-open-redirect-audit` | PHP Web 源码开放重定向审计工具。识别用户可控重定向目的地进入 header Location/跳转函数，分析校验与 allowlist，输出分级、PoC 与修复建议（禁止省略）。 | 1/1 |  |
| `php-route-mapper` | PHP Web 源码路由与参数映射分析工具。从源码中提取所有入口路由与参数结构，输出完整请求模板与参数清单（禁止省略）。 | 1/1 |  |
| `php-tpl-audit` | PHP Web 源码模板注入/SSTI 审计工具。识别模板引擎渲染点与模板名/表达式可控性，追踪到 eval/执行链，输出可利用性分级、PoC 与修复建议（禁止省略）。 | 1/1 |  |
| `posix-shell-pro` | Expert in strict POSIX sh scripting for maximum portability across Unix-like systems. Specializes in shell scripts that run on any POSIX-compliant shell (dash, ash, sh,… | 1/1 |  |
| `powershell-windows` | PowerShell Windows patterns. Critical pitfalls, operator syntax, error handling. | 1/1 |  |
| `privesc-enumeration` | Linux PrivEsc Chain Phase 10/提权枚举. 触发词: 提权枚举。 | 1/1 | 覆寫特徵 |
| `problem-solving` | 按需用于问题澄清、陌生领域学习、复杂问题解决、方案决策和自我认识；根据任务选择一个最小必要方法，不适用于简单且目标明确的执行请求。 | 1/1 |  |
| `process-injection` | Process injection techniques including remote thread injection, APC injection, process hollowing, and reflective DLL injection | 1/1 |  |
| `red-team-operations` | Methodology Chain Phase 7/红队运营. 触发词: 红队运营。 | 1/1 | 覆寫特徵 |
| `refactor-arch` | — | 1/1 |  |
| `rev-symbol` | Restore function symbols by analyzing code patterns, strings, constants, and cross-references | 3/1 |  |
| `sandbox-detection` | Sandbox detection techniques to identify automated analysis environments like Cuckoo Sandbox, VMRay, and Joe Sandbox | 1/1 |  |
| `shellcheck-configuration` | Master ShellCheck static analysis configuration and usage for shell script quality. Use when setting up linting infrastructure, fixing code issues, or ensuring script po… | 1/1 |  |
| `source-code-hunting` | 源码狩猎:.git泄露,危险函数grep,JS RC4解混淆,semgrep/CodeQL,trufflehog,patch diff,供应链/CI。Use when hunting source leaks, secrets, JS deobfuscation, or supply-chain issues. | 1/1 |  |
| `steganography-techniques` | Steganography detection and extraction playbook. Use when analyzing images (LSB, PNG chunks, JPEG DCT, EXIF), audio (spectrogram, DTMF), files (polyglots, appended data,… | 1/1 |  |
| `stego-exfiltration` | Exfiltration Chain Phase 5/隐写术渗出. 触发词: 隐写术渗出。 | 1/1 | 覆寫特徵 |
| `sudo-abuse` | Linux PrivEsc Chain Phase 6/sudo滥用. 触发词: sudo滥用。 | 1/1 | 覆寫特徵 |
| `suid-&-privileged-binaries` | Linux PrivEsc Chain Phase 5/SUID与特权二进制. 触发词: SUID与特权二进制。 | 1/1 | 覆寫特徵 |
| `threat-modeling-&-tactics` | Methodology Chain Phase 1/威胁建模与战术. 触发词: 威胁建模与战术。 | 1/1 | 覆寫特徵 |
| `unauthorized-access-common-services` | Unauthorized access playbook for common exposed services. Use when Redis, Rsync, PHP-FPM, AJP/Ghostcat, Hadoop YARN, H2 Console, or similar management interfaces are exp… | 1/1 |  |
| `web-auth-integrator` | Integrate authentication and authorization flows with provider-specific setup and RBAC safeguards. | 1/1 |  |
| `web-stack-planner` | Collect project brief and stack choices, then output canonical project-config.json for downstream web-builder skills. | 1/1 |  |
| `zero-day-discovery` | 0day自主发现引擎:变体分析/补丁间隙/差分/Fuzzing/污点推理/N-day武器化/猎人思维。Use when public vulns not found and need to discover 0day or weaponize N-day. | 1/1 |  |

