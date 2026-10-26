---
name: security_reporter
description: 安全报告编写助手 - 增强版。专业渗透测试报告生成器，支持HTML/Markdown格式，覆盖完整测试流程（规划→侦察→漏洞利用→横向移动→数据外泄→报告→修复验证），包含CVSS评分、PoC复现步骤、代码级修复方案、质控检查。当需要生成专业渗透测试报告/漏洞分析报告/安全评估报告时自动触发。
---

# 🔒 安全报告编写助手（增强版）

## 能力概述

本技能专注于生成**企业级专业渗透测试报告**，覆盖从测试规划到修复验证的完整生命周期。

### ⭐ 核心增强特性

| 特性 | 说明 |
|------|------|
| **HTML 专业报告** | 内嵌CSS样式系统，支持打印/浏览器阅读/PDF导出 |
| **完整漏洞复现** | 步骤化复现 × HTTP请求/响应原文 × PoC验证代码 |
| **代码级修复方案** | 修复前/修复后代码对比 × 改动说明 × 安全最佳实践 |
| **CVSS 3.1 自动评分** | 攻击向量/复杂度/权限/交互/范围/影响 全维度评分 |
| **修复验证方法** | 可操作的验证步骤 × 预期结果 × 回归测试建议 |
| **行业合规对齐** | 等保2.0/CISA/NIST/OWASP 合规对照表 |
| **10 行业模板** | 金融/医疗/政府/制造/教育/能源/交通 + 渗透测试/多漏洞/YouTrack |
| **质控检查清单** | 交付前8项必检指标 |

---

## 🎯 触发条件

以下关键词自动触发本技能：
- "生成渗透测试报告"
- "写一份安全报告"
- "漏洞报告"
- "渗透测试报告 HTML"
- "penteset report"
- "security assessment report"
- "漏洞分析报告"

---

## 📁 文件结构

```
security-reporter/
├── SKILL.md                              # ← 本文件
├── SKILL_ENHANCED.md                     # 增强版说明
├── templates/                            # 10+ 报告模板
│   ├── penetration_testing_report_html.md  # ⭐ HTML专业渗透报告（完整CSS+JS）
│   ├── penetration_testing_template.md     # Markdown渗透测试报告
│   ├── multi_vulnerability_template.md     # 多漏洞总分结构
│   ├── general_template.md                 # 通用漏洞报告
│   ├── financial_template.md               # 金融行业合规报告
│   ├── medical_template.md                 # 医疗行业合规报告
│   ├── government_template.md              # 政府行业合规报告
│   ├── manufacturing_template.md           # 制造业合规报告
│   ├── education_template.md               # 教育行业合规报告
│   ├── energy_template.md                  # 能源行业合规报告
│   ├── transportation_template.md          # 交通行业合规报告
│   └── youtrack_ticket_template.md         # YouTrack提报模板
├── snippets/                              # 可复用内容片段
│   ├── sql_injection.md
│   ├── xss.md
│   ├── csrf.md
│   ├── rce.md
│   ├── lfi.md / rfi.md
│   ├── brute_force.md
│   ├── weak_password.md
│   ├── information_disclosure.md
│   ├── access_control.md
│   ├── cvss_explanation.md
│   ├── remediation_steps.md
│   ├── verification_methods.md
│   ├── security_best_practices.md
│   └── incident_response.md
└── resources/                             # 资源文件
    └── vulnerabilities/                   # 漏洞知识库
        ├── sql_injection.md
        ├── xss.md
        └── ...
```

---

## 🚀 使用流程

### 流程一：HTML 专业报告（正式交付）

```
1. 选择模板：templates/penetration_testing_report_html.md
2. 收集漏洞数据（编号/CVSS/复现/PoC/修复）
3. 逐漏洞填充 vuln-card 模板
4. 替换报告级占位符（项目信息/统计/汇总）
5. 保存为 .html → 浏览器打开 → 打印为 PDF
6. 执行质控检查清单
```

### 流程二：Markdown 快速报告（内部沟通）

```
1. 选择模板：templates/penetration_testing_template.md 或 general_template.md
2. 使用 snippets/ 中的片段快速组装
3. 漏洞描述引用 snippets/ 标准描述（如 sql_injection.md）
4. 导出为 .md 或转换为 PDF
```

### 流程三：多漏洞综合分析

```
1. 选择模板：templates/multi_vulnerability_template.md
2. 按风险等级排序所有漏洞
3. 生成总分结构：总体概述 → 分漏洞详情 → 修复优先级
4. 风险趋势分析 + 修复路线图
```

---

## 📐 HTML 报告核心设计

### 封面页
- 渐变深蓝背景 + 公司Logo区
- 密级标识（绝密/机密/内部/公开）
- 项目元信息（客户/测试方/日期/版本）

### 执行摘要
- 5色风险统计卡片（严重🔴/高🟠/中🟡/低🟢/信息🔵）
- 关键发现高亮框
- 综合安全评级

### 漏洞详情卡片（vuln-card）
```
┌─────────────────────────────────────────┐
│ VULN-2024-001 | SQL注入 | CVSS 9.8     │ ← 等级颜色头部
├─────────────────────────────────────────┤
│ 📋 漏洞描述 + 危害分析                  │
│ 📊 CVSS 3.1 评分详情（8维表格）         │
│ 🔬 复现步骤（步骤号 + 命令框）          │
│ 📨 HTTP请求/响应原文（代码块）          │
│ 💥 PoC利用验证代码                     │
│ 🔧 修复方案（临时缓解 + 代码对比）      │
│ ✔️ 修复验证方法 + 预期结果              │
│ 📚 参考资料（CVE/OWASP/厂商公告）      │
└─────────────────────────────────────────┘
```

### CSS 样式系统
- `--critical/high/medium/low/info` 五色系统
- 响应式网格布局
- 打印友好 (@media print)
- 代码块深色主题
- 时间线样式（修复路线图）

---

## 📊 报告质量控制清单（交付前必检）

| # | 检查项 | 标准 |
|---|--------|------|
| 1 | 漏洞编号唯一 | VULN-YYYY-NNN 格式 |
| 2 | CVSS评分完整 | 含8维度评分 + 向量字符串 |
| 3 | 复现步骤可独立复现 | 第三人按步骤操作100%可重现 |
| 4 | HTTP证据原文 | 请求头+请求体+响应头+响应体完整 |
| 5 | PoC可执行 | 代码可直接运行验证漏洞存在 |
| 6 | 修复方案含代码对比 | 修复前/修复后代码 + 改动说明 |
| 7 | 修复验证可操作 | 具体命令或测试用例 + 预期结果 |
| 8 | 报告脱敏处理 | 密码/Token/内网IP/个人信息已替换 |
| 9 | 密级标识正确 | 封面+页眉/页脚一致 |
| 10 | 无错别字/语法错误 | 全文审校 |

---

## 🔗 与其他技能联动

| 上游技能 | 提供数据 → | 本技能处理 |
|----------|-----------|-----------|
| pentest-recon-osint | 资产/端口/服务列表 | → 测试范围章节 |
| pentest-web-app-attacker | Web漏洞发现 | → 漏洞详情卡片 |
| pentest-network-exploiter | 漏洞利用/PoC | → 复现步骤+PoC |
| pentest-priv-escalation | 提权路径 | → 攻击链分析 |
| pentest-lateral-movement | 横向移动路径 | → 内网影响范围 |
| pentest-data-exfil-tester | 数据外泄证明 | → 业务影响评估 |
| pentest-remediation-validator | 修复验证结果 | → 修复验证章节 |
| code-audit-comprehensive | 代码审计发现 | → 代码级修复方案 |
| dfyx-code-security-review | 代码审计发现 | → 修复前后代码对比 |
| threat-modeling-stride | 威胁模型 | → 风险优先级建议 |

---

## 📝 版本历史

- **v2.0** (当前): 新增HTML专业报告模板，完整CSS样式系统，代码级修复方案，质控清单
- **v1.0**: DFYX初始版本，10行业Markdown模板 + 片段库
