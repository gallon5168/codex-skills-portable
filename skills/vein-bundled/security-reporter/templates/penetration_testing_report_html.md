# HTML 渗透测试报告生成技能

## 技能描述
专业渗透测试报告 HTML 生成器。基于安全测试全流程，自动生成包含漏洞复现步骤、验证方法、修复方案的标准化 HTML 报告，满足企业级交付要求。

## 报告核心结构

### 1. 封面区
- 项目名称、客户单位
- 测试单位、测试人员
- 报告日期、密级标识
- 文档编号、版本号

### 2. 执行摘要
- 整体安全评估结论（高中低风险统计）
- 关键发现 Top 5
- 风险分布饼图（HTML+CSS）
- 修复优先级建议

### 3. 测试概述
- 测试范围（IP/域名/应用列表）
- 测试方法（黑盒/白盒/灰盒）
- 测试时间线
- 参与人员与角色
- 测试依据（OWASP/PTES/NIST等）

### 4. 漏洞详情（核心）
每个漏洞必须包含：
- **基本信息**: 漏洞编号、名称、类型、等级、CVSS评分
- **漏洞描述**: 原理说明、危害分析
- **影响范围**: 受影响URL/IP、参数、版本
- **复现步骤**: 逐步截图+请求/响应原文
- **利用验证**: POC代码、利用截图
- **修复方案**: 
  - 临时缓解措施
  - 根本修复方案（含代码示例）
  - 配置加固建议
- **修复验证**: 如何验证修复已生效
- **参考资料**: CVE编号、OWASP参考、厂商公告

### 5. 风险汇总表
- 漏洞清单（编号/名称/等级/状态/修复优先级）
- 风险等级分布统计
- 修复时间线建议

### 6. 修复建议路线图
- P0（立即修复）：24h内
- P1（本周修复）：1周内
- P2（本月修复）：1月内
- P3（下版本修复）：下一迭代

### 7. 附录
- 测试工具清单
- 测试用例索引
- 术语表
- 合规对照表（等保/CISA/NIST）

---

## HTML 报告模板

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{报告标题}} - 渗透测试报告</title>
    <style>
        :root {
            --critical: #dc3545;
            --high: #fd7e14;
            --medium: #ffc107;
            --low: #28a745;
            --info: #17a2b8;
            --primary: #1a237e;
            --secondary: #455a64;
            --bg: #f5f7fa;
            --card: #ffffff;
            --border: #e0e0e0;
            --text: #333333;
        }
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: "Microsoft YaHei", "PingFang SC", -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.8;
            font-size: 14px;
        }
        
        /* ========== COVER PAGE ========== */
        .cover-page {
            width: 100%;
            min-height: 100vh;
            background: linear-gradient(135deg, #0d1b3e 0%, #1a237e 40%, #283593 100%);
            color: #ffffff;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            padding: 60px;
            page-break-after: always;
        }
        
        .cover-page .classification {
            position: absolute;
            top: 30px;
            right: 40px;
            border: 2px solid #ff5252;
            color: #ff5252;
            padding: 6px 20px;
            font-size: 16px;
            font-weight: bold;
            letter-spacing: 4px;
            border-radius: 4px;
        }
        
        .cover-page .logo-area {
            margin-bottom: 60px;
            font-size: 48px;
            opacity: 0.9;
        }
        
        .cover-page h1 {
            font-size: 42px;
            font-weight: 700;
            margin-bottom: 20px;
            letter-spacing: 4px;
            text-shadow: 0 2px 10px rgba(0,0,0,0.3);
        }
        
        .cover-page .subtitle {
            font-size: 20px;
            color: #90caf9;
            margin-bottom: 60px;
            letter-spacing: 8px;
        }
        
        .cover-page .meta {
            font-size: 15px;
            line-height: 2.5;
            color: #b0bec5;
        }
        
        .cover-page .meta strong {
            color: #ffffff;
            margin-right: 8px;
        }
        
        .cover-page .footer {
            position: absolute;
            bottom: 40px;
            font-size: 13px;
            color: #78909c;
        }
        
        /* ========== MAIN CONTENT ========== */
        .content {
            max-width: 1100px;
            margin: 0 auto;
            padding: 40px 50px;
        }
        
        /* Section styling */
        .section {
            background: var(--card);
            border-radius: 8px;
            padding: 35px 40px;
            margin-bottom: 30px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.06);
            page-break-inside: avoid;
        }
        
        .section h2 {
            font-size: 24px;
            color: var(--primary);
            border-left: 4px solid var(--primary);
            padding-left: 15px;
            margin-bottom: 25px;
            font-weight: 700;
        }
        
        .section h3 {
            font-size: 18px;
            color: var(--secondary);
            margin: 25px 0 15px 0;
            padding-bottom: 8px;
            border-bottom: 1px solid var(--border);
        }
        
        .section h4 {
            font-size: 15px;
            color: #555;
            margin: 20px 0 10px 0;
        }
        
        /* ========== STATS CARDS ========== */
        .stats-row {
            display: flex;
            gap: 20px;
            margin: 25px 0;
            flex-wrap: wrap;
        }
        
        .stat-card {
            flex: 1;
            min-width: 160px;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            color: #fff;
        }
        
        .stat-card.critical { background: var(--critical); }
        .stat-card.high { background: var(--high); }
        .stat-card.medium { background: var(--medium); color: #333; }
        .stat-card.low { background: var(--low); }
        .stat-card.info { background: var(--info); }
        .stat-card.total { background: var(--secondary); }
        
        .stat-card .number {
            font-size: 48px;
            font-weight: 700;
            line-height: 1;
        }
        
        .stat-card .label {
            font-size: 13px;
            margin-top: 8px;
            opacity: 0.9;
        }
        
        /* ========== TABLES ========== */
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 13px;
        }
        
        table thead {
            background: var(--primary);
            color: #fff;
        }
        
        table th {
            padding: 12px 15px;
            text-align: left;
            font-weight: 600;
            white-space: nowrap;
        }
        
        table td {
            padding: 12px 15px;
            border-bottom: 1px solid var(--border);
        }
        
        table tbody tr:hover {
            background: #f0f4ff;
        }
        
        table tbody tr:nth-child(even) {
            background: #fafbfc;
        }
        
        /* Severity badges */
        .badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            color: #fff;
        }
        .badge-critical { background: var(--critical); }
        .badge-high { background: var(--high); }
        .badge-medium { background: var(--medium); color: #333; }
        .badge-low { background: var(--low); }
        .badge-info { background: var(--info); }
        
        /* ========== CODE BLOCKS ========== */
        .code-block {
            background: #1e1e1e;
            color: #d4d4d4;
            border-radius: 6px;
            padding: 20px;
            margin: 15px 0;
            overflow-x: auto;
            font-family: "Consolas", "Monaco", "Courier New", monospace;
            font-size: 13px;
            line-height: 1.6;
            position: relative;
        }
        
        .code-block .lang-tag {
            position: absolute;
            top: 0;
            right: 0;
            background: #333;
            color: #aaa;
            padding: 3px 10px;
            font-size: 11px;
            border-radius: 0 6px 0 6px;
        }
        
        /* ========== ALERT BOXES ========== */
        .alert {
            padding: 15px 20px;
            border-radius: 6px;
            margin: 15px 0;
            border-left: 4px solid;
        }
        
        .alert-danger {
            background: #ffeaea;
            border-color: var(--critical);
            color: #721c24;
        }
        
        .alert-warning {
            background: #fff3cd;
            border-color: var(--high);
            color: #856404;
        }
        
        .alert-info {
            background: #e3f2fd;
            border-color: var(--info);
            color: #0c5460;
        }
        
        .alert-success {
            background: #d4edda;
            border-color: var(--low);
            color: #155724;
        }
        
        /* ========== VULNERABILITY CARD ========== */
        .vuln-card {
            border: 1px solid var(--border);
            border-radius: 8px;
            margin: 25px 0;
            overflow: hidden;
        }
        
        .vuln-card .vuln-header {
            padding: 18px 25px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            color: #fff;
        }
        
        .vuln-card .vuln-header.critical { background: var(--critical); }
        .vuln-card .vuln-header.high { background: var(--high); }
        .vuln-card .vuln-header.medium { background: var(--medium); color: #333; }
        .vuln-card .vuln-header.low { background: var(--low); }
        
        .vuln-card .vuln-header .vuln-id {
            font-size: 18px;
            font-weight: 700;
        }
        
        .vuln-card .vuln-header .cvss {
            font-size: 24px;
            font-weight: 700;
        }
        
        .vuln-card .vuln-body {
            padding: 25px;
        }
        
        .vuln-card .vuln-body .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 12px;
            margin-bottom: 20px;
        }
        
        .vuln-card .vuln-body .info-item {
            display: flex;
            gap: 8px;
        }
        
        .vuln-card .vuln-body .info-item .key {
            color: #666;
            font-weight: 600;
            min-width: 80px;
        }
        
        /* ========== STEP-BY-STEP REPRODUCTION ========== */
        .repro-step {
            display: flex;
            gap: 15px;
            margin: 15px 0;
            align-items: flex-start;
        }
        
        .repro-step .step-num {
            background: var(--primary);
            color: #fff;
            width: 32px;
            height: 32px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            flex-shrink: 0;
            margin-top: 2px;
        }
        
        .repro-step .step-content {
            flex: 1;
        }
        
        .repro-step .step-content .step-cmd {
            background: #f5f5f5;
            padding: 8px 14px;
            border-radius: 4px;
            font-family: monospace;
            font-size: 13px;
            margin: 6px 0;
            border-left: 3px solid var(--primary);
        }
        
        /* ========== TIMELINE ========== */
        .timeline {
            position: relative;
            padding-left: 30px;
            margin: 20px 0;
        }
        
        .timeline::before {
            content: '';
            position: absolute;
            left: 8px;
            top: 0;
            bottom: 0;
            width: 3px;
            background: var(--border);
        }
        
        .timeline-item {
            position: relative;
            margin-bottom: 20px;
        }
        
        .timeline-item::before {
            content: '';
            position: absolute;
            left: -26px;
            top: 5px;
            width: 14px;
            height: 14px;
            border-radius: 50%;
            background: var(--primary);
            border: 3px solid #fff;
            box-shadow: 0 0 0 2px var(--primary);
        }
        
        .timeline-item .time {
            font-size: 12px;
            color: #999;
        }
        
        /* ========== PRINT ========== */
        @media print {
            body { background: #fff; }
            .section { box-shadow: none; border: 1px solid #ddd; page-break-inside: avoid; }
            .cover-page { page-break-after: always; }
        }
        
        /* ========== TOC ========== */
        .toc {
            background: #f8f9fa;
            border-radius: 8px;
            padding: 25px 30px;
            margin: 20px 0;
        }
        
        .toc h3 {
            margin-top: 0;
            border: none;
        }
        
        .toc ul {
            list-style: none;
            padding: 0;
        }
        
        .toc ul li {
            padding: 5px 0;
            border-bottom: 1px dotted #ddd;
        }
        
        .toc ul li a {
            color: var(--primary);
            text-decoration: none;
        }
        
        .toc ul li a:hover {
            text-decoration: underline;
        }
        
        /* Page header/footer */
        .page-header {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            padding: 10px 50px;
            background: #fff;
            border-bottom: 1px solid var(--border);
            font-size: 11px;
            color: #999;
            display: flex;
            justify-content: space-between;
        }
        
        .page-footer {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            padding: 10px 50px;
            background: #fff;
            border-top: 1px solid var(--border);
            font-size: 11px;
            color: #999;
            text-align: center;
        }
        
        @media print {
            .page-header, .page-footer { display: block; }
        }
    </style>
</head>
<body>

<!-- ==================== COVER PAGE ==================== -->
<div class="cover-page">
    <div class="classification">{{密级}}</div>
    <div class="logo-area">🛡️</div>
    <h1>{{项目名称}}</h1>
    <div class="subtitle">渗透测试报告</div>
    <div class="meta">
        <p><strong>客户单位：</strong>{{客户单位}}</p>
        <p><strong>测试单位：</strong>{{测试单位}}</p>
        <p><strong>报告日期：</strong>{{报告日期}}</p>
        <p><strong>文档编号：</strong>{{文档编号}}</p>
        <p><strong>版本号：</strong>{{版本号}}</p>
    </div>
    <div class="footer">本文档为保密文件，未经授权不得外传</div>
</div>

<!-- ==================== MAIN CONTENT ==================== -->
<div class="content">

<!-- ===== TOC ===== -->
<div class="section toc">
    <h3>📑 目录</h3>
    <ul>
        <li><a href="#executive-summary">1. 执行摘要</a></li>
        <li><a href="#test-overview">2. 测试概述</a></li>
        <li><a href="#vuln-details">3. 漏洞详情</a></li>
        <li><a href="#risk-summary">4. 风险汇总</a></li>
        <li><a href="#remediation-roadmap">5. 修复建议路线图</a></li>
        <li><a href="#appendix">6. 附录</a></li>
    </ul>
</div>

<!-- ===== 1. EXECUTIVE SUMMARY ===== -->
<div class="section" id="executive-summary">
    <h2>1. 执行摘要</h2>
    
    <p>{{执行摘要概述}}</p>
    
    <div class="stats-row">
        <div class="stat-card critical">
            <div class="number">{{严重数量}}</div>
            <div class="label">严重 (Critical)</div>
        </div>
        <div class="stat-card high">
            <div class="number">{{高危数量}}</div>
            <div class="label">高危 (High)</div>
        </div>
        <div class="stat-card medium">
            <div class="number">{{中危数量}}</div>
            <div class="label">中危 (Medium)</div>
        </div>
        <div class="stat-card low">
            <div class="number">{{低危数量}}</div>
            <div class="label">低危 (Low)</div>
        </div>
        <div class="stat-card total">
            <div class="number">{{总计数量}}</div>
            <div class="label">总计</div>
        </div>
    </div>
    
    <h3>关键发现</h3>
    <div class="alert alert-danger">
        <strong>🔴 高危发现：</strong>{{关键高危发现描述}}
    </div>
    <div class="alert alert-warning">
        <strong>🟠 值得关注：</strong>{{关键中危发现描述}}
    </div>
    
    <h3>整体评估</h3>
    <p><strong>综合安全评级：</strong><span class="badge badge-{{综合评级颜色}}">{{综合评级}}</span></p>
    <p>{{整体评估结论}}</p>
</div>

<!-- ===== 2. TEST OVERVIEW ===== -->
<div class="section" id="test-overview">
    <h2>2. 测试概述</h2>
    
    <h3>2.1 测试范围</h3>
    <table>
        <thead>
            <tr><th>类别</th><th>目标</th><th>说明</th></tr>
        </thead>
        <tbody>
            {{测试范围表格行}}
        </tbody>
    </table>
    
    <h3>2.2 测试方法</h3>
    <p><strong>测试类型：</strong>{{测试类型（黑盒/白盒/灰盒）}}</p>
    <p><strong>测试依据：</strong></p>
    <ul>
        <li>OWASP Top 10 (2021)</li>
        <li>OWASP Web Security Testing Guide (WSTG)</li>
        <li>PTES (Penetration Testing Execution Standard)</li>
        <li>CWE Top 25 Most Dangerous Software Weaknesses</li>
        <li>{{其他测试标准}}</li>
    </ul>
    
    <h3>2.3 测试时间线</h3>
    <div class="timeline">
        {{测试时间线条目}}
    </div>
    
    <h3>2.4 参与人员</h3>
    <table>
        <thead>
            <tr><th>姓名</th><th>角色</th><th>职责</th></tr>
        </thead>
        <tbody>
            {{参与人员表格行}}
        </tbody>
    </table>
</div>

<!-- ===== 3. VULNERABILITY DETAILS ===== -->
<div class="section" id="vuln-details">
    <h2>3. 漏洞详情</h2>
    
    <!-- 
    ============================================
    每个漏洞使用以下 vuln-card 模板
    复制此模板为每个发现的漏洞填写
    ============================================
    -->
    
    <!-- VULN-001 示例 -->
    <div class="vuln-card">
        <div class="vuln-header {{漏洞等级CSS类}}">
            <div class="vuln-id">{{漏洞编号}} - {{漏洞名称}}</div>
            <div class="cvss">CVSS {{CVSS评分}}</div>
        </div>
        <div class="vuln-body">
            
            <!-- 基本信息 -->
            <div class="info-grid">
                <div class="info-item"><span class="key">漏洞类型：</span><span>{{漏洞类型}}</span></div>
                <div class="info-item"><span class="key">风险等级：</span><span class="badge badge-{{等级CSS类}}">{{风险等级}}</span></div>
                <div class="info-item"><span class="key">CVSS评分：</span><span>{{CVSS评分}}/10.0</span></div>
                <div class="info-item"><span class="key">影响URL：</span><span>{{影响URL}}</span></div>
                <div class="info-item"><span class="key">影响参数：</span><span>{{影响参数}}</span></div>
                <div class="info-item"><span class="key">发现日期：</span><span>{{发现日期}}</span></div>
            </div>
            
            <!-- 漏洞描述 -->
            <h3>📋 漏洞描述</h3>
            <p>{{漏洞详细描述}}</p>
            
            <div class="alert alert-danger">
                <strong>⚠️ 危害分析：</strong>{{漏洞危害分析}}
            </div>
            
            <!-- CVSS 向量 -->
            <h3>📊 CVSS 3.1 评分详情</h3>
            <table>
                <thead>
                    <tr><th>指标</th><th>值</th><th>说明</th></tr>
                </thead>
                <tbody>
                    <tr><td>攻击向量 (AV)</td><td>{{AV}}</td><td>{{AV说明}}</td></tr>
                    <tr><td>攻击复杂度 (AC)</td><td>{{AC}}</td><td>{{AC说明}}</td></tr>
                    <tr><td>所需权限 (PR)</td><td>{{PR}}</td><td>{{PR说明}}</td></tr>
                    <tr><td>用户交互 (UI)</td><td>{{UI}}</td><td>{{UI说明}}</td></tr>
                    <tr><td>影响范围 (S)</td><td>{{S}}</td><td>{{S说明}}</td></tr>
                    <tr><td>机密性影响 (C)</td><td>{{C}}</td><td>{{C说明}}</td></tr>
                    <tr><td>完整性影响 (I)</td><td>{{I}}</td><td>{{I说明}}</td></tr>
                    <tr><td>可用性影响 (A)</td><td>{{A}}</td><td>{{A说明}}</td></tr>
                </tbody>
            </table>
            <p><strong>CVSS向量：</strong><code>{{CVSS向量字符串}}</code></p>
            
            <!-- 复现步骤 -->
            <h3>🔬 复现步骤</h3>
            <p><strong>前置条件：</strong></p>
            <ul>
                {{前置条件列表}}
            </ul>
            
            <div class="repro-step">
                <div class="step-num">1</div>
                <div class="step-content">
                    <strong>{{步骤1标题}}</strong>
                    <p>{{步骤1描述}}</p>
                    <div class="step-cmd">{{步骤1命令或URL}}</div>
                </div>
            </div>
            
            <div class="repro-step">
                <div class="step-num">2</div>
                <div class="step-content">
                    <strong>{{步骤2标题}}</strong>
                    <p>{{步骤2描述}}</p>
                    <div class="step-cmd">{{步骤2命令或URL}}</div>
                </div>
            </div>
            
            <div class="repro-step">
                <div class="step-num">3</div>
                <div class="step-content">
                    <strong>{{步骤3标题}}</strong>
                    <p>{{步骤3描述}}</p>
                    <div class="step-cmd">{{步骤3命令或URL}}</div>
                </div>
            </div>
            
            <!-- 请求/响应证据 -->
            <h4>📨 HTTP 请求原文</h4>
            <div class="code-block">
                <span class="lang-tag">HTTP</span>
{{HTTP请求原文}}
            </div>
            
            <h4>📩 HTTP 响应原文</h4>
            <div class="code-block">
                <span class="lang-tag">HTTP</span>
{{HTTP响应原文}}
            </div>
            
            <!-- POC -->
            <h4>💥 利用验证 (PoC)</h4>
            <div class="code-block">
                <span class="lang-tag">{{PoC语言}}</span>
{{PoC代码}}
            </div>
            
            <!-- 修复方案 -->
            <h3>🔧 修复方案</h3>
            
            <h4>🩹 临时缓解措施（立即执行）</h4>
            <div class="alert alert-warning">
                {{临时缓解措施}}
            </div>
            
            <h4>✅ 根本修复方案（推荐）</h4>
            <p>{{修复方案说明}}</p>
            
            <h5>修复前（存在漏洞的代码）：</h5>
            <div class="code-block">
                <span class="lang-tag">{{代码语言}}</span>
{{修复前代码}}
            </div>
            
            <h5>修复后（安全代码）：</h5>
            <div class="code-block">
                <span class="lang-tag">{{代码语言}}</span>
{{修复后代码}}
            </div>
            
            <h5>关键改动说明：</h5>
            <ol>
                {{关键改动说明列表}}
            </ol>
            
            <h4>🛡️ 配置加固建议</h4>
            <ul>
                {{配置加固建议列表}}
            </ul>
            
            <!-- 修复验证 -->
            <h3>✔️ 修复验证方法</h3>
            <div class="alert alert-success">
                <strong>验证步骤：</strong>
                <ol>
                    {{修复验证步骤列表}}
                </ol>
            </div>
            <p><strong>预期结果：</strong>{{修复验证预期结果}}</p>
            
            <!-- 参考资料 -->
            <h3>📚 参考资料</h3>
            <ul>
                {{参考资料列表}}
            </ul>
        </div>
    </div>
    
    <!-- ===== 更多漏洞卡片在此重复 ===== -->
    {{更多漏洞卡片}}
    
</div>

<!-- ===== 4. RISK SUMMARY ===== -->
<div class="section" id="risk-summary">
    <h2>4. 风险汇总</h2>
    
    <h3>4.1 漏洞清单</h3>
    <table>
        <thead>
            <tr>
                <th>编号</th>
                <th>漏洞名称</th>
                <th>类型</th>
                <th>风险等级</th>
                <th>CVSS</th>
                <th>影响URL</th>
                <th>修复优先级</th>
                <th>状态</th>
            </tr>
        </thead>
        <tbody>
            {{漏洞清单表格行}}
        </tbody>
    </table>
    
    <h3>4.2 风险分布统计</h3>
    <table>
        <thead>
            <tr><th>风险等级</th><th>数量</th><th>占比</th><th>修复时限</th></tr>
        </thead>
        <tbody>
            <tr><td><span class="badge badge-critical">严重</span></td><td>{{严重计数}}</td><td>{{严重占比}}%</td><td>24小时</td></tr>
            <tr><td><span class="badge badge-high">高危</span></td><td>{{高危计数}}</td><td>{{高危占比}}%</td><td>1周</td></tr>
            <tr><td><span class="badge badge-medium">中危</span></td><td>{{中危计数}}</td><td>{{中危占比}}%</td><td>1个月</td></tr>
            <tr><td><span class="badge badge-low">低危</span></td><td>{{低危计数}}</td><td>{{低危占比}}%</td><td>3个月</td></tr>
        </tbody>
    </table>
</div>

<!-- ===== 5. REMEDIATION ROADMAP ===== -->
<div class="section" id="remediation-roadmap">
    <h2>5. 修复建议路线图</h2>
    
    <div class="timeline">
        <div class="timeline-item">
            <div class="time">🔴 P0 - 立即修复（24小时内）</div>
            <ul>
                {{P0修复项目列表}}
            </ul>
        </div>
        
        <div class="timeline-item">
            <div class="time">🟠 P1 - 本周修复（1周内）</div>
            <ul>
                {{P1修复项目列表}}
            </ul>
        </div>
        
        <div class="timeline-item">
            <div class="time">🟡 P2 - 本月修复（1月内）</div>
            <ul>
                {{P2修复项目列表}}
            </ul>
        </div>
        
        <div class="timeline-item">
            <div class="time">🟢 P3 - 下迭代修复</div>
            <ul>
                {{P3修复项目列表}}
            </ul>
        </div>
    </div>
    
    <h3>安全加固建议</h3>
    <div class="alert alert-info">
        <strong>💡 长期安全改进建议：</strong>
        <ul>
            {{长期改进建议列表}}
        </ul>
    </div>
</div>

<!-- ===== 6. APPENDIX ===== -->
<div class="section" id="appendix">
    <h2>6. 附录</h2>
    
    <h3>6.1 测试工具清单</h3>
    <table>
        <thead>
            <tr><th>工具名称</th><th>版本</th><th>用途</th></tr>
        </thead>
        <tbody>
            {{测试工具清单表格行}}
        </tbody>
    </table>
    
    <h3>6.2 术语表</h3>
    <table>
        <thead>
            <tr><th>术语</th><th>说明</th></tr>
        </thead>
        <tbody>
            <tr><td>CVE</td><td>Common Vulnerabilities and Exposures，通用漏洞披露</td></tr>
            <tr><td>CVSS</td><td>Common Vulnerability Scoring System，通用漏洞评分系统</td></tr>
            <tr><td>OWASP</td><td>Open Web Application Security Project，开源Web应用安全项目</td></tr>
            <tr><td>POC</td><td>Proof of Concept，概念验证</td></tr>
            <tr><td>WAF</td><td>Web Application Firewall，Web应用防火墙</td></tr>
        </tbody>
    </table>
    
    <h3>6.3 合规对照</h3>
    <table>
        <thead>
            <tr><th>漏洞编号</th><th>CWE</th><th>OWASP Top 10</th><th>等保2.0要求</th></tr>
        </thead>
        <tbody>
            {{合规对照表格行}}
        </tbody>
    </table>
</div>

</div><!-- /.content -->

<!-- Page Footer -->
<div class="page-footer">
    {{客户单位}} | 渗透测试报告 | 密级:{{密级}} | 页码: <span class="page-num"></span>
</div>

</body>
</html>
```

---

## 使用流程

### 步骤1：收集漏洞数据
从渗透测试过程中收集每个漏洞的完整信息：
- 漏洞基本信息（类型、等级、URL、参数）
- 复现步骤（含截图和请求/响应原文）
- POC代码
- 修复建议（含代码对比）

### 步骤2：选择报告模板
- 单个漏洞 → `penetration_testing_template.md` (简洁Markdown)
- 多个漏洞 → `multi_vulnerability_template.md` (总分结构)
- 正式交付 → `penetration_testing_template_html.md` (完整HTML)
- 按行业 → 选择对应行业模板（金融/医疗/政府等）

### 步骤3：填充报告内容
用实际测试数据替换所有 `{{占位符}}`

### 步骤4：生成最终报告
将HTML代码保存为 `.html` 文件，浏览器打开即可查看/打印

---

## 报告质量控制清单

在交付报告前，确保：
- [ ] 每个漏洞都有唯一编号（格式: VULN-YYYY-XXX）
- [ ] 每个漏洞都有CVSS 3.1评分和向量字符串
- [ ] 复现步骤可独立复现（任何人按步骤操作都能重现）
- [ ] 所有HTTP请求/响应都有原文佐证
- [ ] 修复方案包含代码对比（修复前/修复后）
- [ ] 修复验证方法可操作、可验证
- [ ] 漏洞等级评定有理有据（基于CVSS + 业务影响）
- [ ] 报告无拼写/语法错误
- [ ] 敏感信息已脱敏处理
- [ ] 密级标识正确
