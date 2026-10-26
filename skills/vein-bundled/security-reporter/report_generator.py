#!/usr/bin/env python3
"""
渗透测试HTML报告生成器
用法: python report_generator.py --input vulnerabilities.json --output report.html
"""

import json
import sys
import argparse
from datetime import datetime
from pathlib import Path

# CSS样式从外部文件加载
def load_css():
    css_path = Path(__file__).parent / "report_styles.css"
    if css_path.exists():
        return css_path.read_text(encoding='utf-8')
    return DEFAULT_CSS

DEFAULT_CSS = """
:root {
    --critical: #dc3545; --high: #fd7e14; --medium: #ffc107;
    --low: #28a745; --info: #17a2b8; --primary: #1a237e;
    --secondary: #455a64; --bg: #f5f7fa; --card: #ffffff;
    --border: #e0e0e0; --text: #333333;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
    font-family: "Microsoft YaHei","PingFang SC",-apple-system,sans-serif;
    background: var(--bg); color: var(--text); line-height: 1.8; font-size: 14px;
}
.cover-page {
    width: 100%; min-height: 100vh;
    background: linear-gradient(135deg,#0d1b3e 0%,#1a237e 40%,#283593 100%);
    color: #fff; display: flex; flex-direction: column;
    justify-content: center; align-items: center; text-align: center;
    padding: 60px; page-break-after: always; position: relative;
}
.cover-page .classification {
    position: absolute; top: 30px; right: 40px;
    border: 2px solid #ff5252; color: #ff5252;
    padding: 6px 20px; font-size: 16px; font-weight: bold;
    letter-spacing: 4px; border-radius: 4px;
}
.cover-page h1 { font-size: 42px; font-weight: 700; margin-bottom: 20px; letter-spacing: 4px; }
.cover-page .subtitle { font-size: 20px; color: #90caf9; margin-bottom: 60px; letter-spacing: 8px; }
.cover-page .meta { font-size: 15px; line-height: 2.5; color: #b0bec5; }
.cover-page .meta strong { color: #fff; margin-right: 8px; }
.cover-page .footer { position: absolute; bottom: 40px; font-size: 13px; color: #78909c; }
.content { max-width: 1100px; margin: 0 auto; padding: 40px 50px; }
.section {
    background: var(--card); border-radius: 8px; padding: 35px 40px;
    margin-bottom: 30px; box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    page-break-inside: avoid;
}
.section h2 {
    font-size: 24px; color: var(--primary); border-left: 4px solid var(--primary);
    padding-left: 15px; margin-bottom: 25px; font-weight: 700;
}
.section h3 { font-size: 18px; color: var(--secondary); margin: 25px 0 15px; padding-bottom: 8px; border-bottom: 1px solid var(--border); }
.stats-row { display: flex; gap: 20px; margin: 25px 0; flex-wrap: wrap; }
.stat-card { flex: 1; min-width: 160px; padding: 20px; border-radius: 8px; text-align: center; color: #fff; }
.stat-card.critical { background: var(--critical); }
.stat-card.high { background: var(--high); }
.stat-card.medium { background: var(--medium); color: #333; }
.stat-card.low { background: var(--low); }
.stat-card.info { background: var(--info); }
.stat-card.total { background: var(--secondary); }
.stat-card .number { font-size: 48px; font-weight: 700; line-height: 1; }
.stat-card .label { font-size: 13px; margin-top: 8px; opacity: 0.9; }
table { width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 13px; }
table thead { background: var(--primary); color: #fff; }
table th { padding: 12px 15px; text-align: left; font-weight: 600; white-space: nowrap; }
table td { padding: 12px 15px; border-bottom: 1px solid var(--border); }
table tbody tr:nth-child(even) { background: #fafbfc; }
.badge { display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; color: #fff; }
.badge-critical { background: var(--critical); }
.badge-high { background: var(--high); }
.badge-medium { background: var(--medium); color: #333; }
.badge-low { background: var(--low); }
.badge-info { background: var(--info); }
.code-block {
    background: #1e1e1e; color: #d4d4d4; border-radius: 6px; padding: 20px;
    margin: 15px 0; overflow-x: auto; font-family: "Consolas","Monaco",monospace;
    font-size: 13px; line-height: 1.6; white-space: pre-wrap; position: relative;
}
.code-block .lang-tag {
    position: absolute; top: 0; right: 0; background: #333; color: #aaa;
    padding: 3px 10px; font-size: 11px; border-radius: 0 6px 0 6px;
}
.alert { padding: 15px 20px; border-radius: 6px; margin: 15px 0; border-left: 4px solid; }
.alert-danger { background: #ffeaea; border-color: var(--critical); color: #721c24; }
.alert-warning { background: #fff3cd; border-color: var(--high); color: #856404; }
.alert-info { background: #e3f2fd; border-color: var(--info); color: #0c5460; }
.alert-success { background: #d4edda; border-color: var(--low); color: #155724; }
.vuln-card { border: 1px solid var(--border); border-radius: 8px; margin: 25px 0; overflow: hidden; }
.vuln-card .vuln-header { padding: 18px 25px; display: flex; justify-content: space-between; align-items: center; color: #fff; }
.vuln-card .vuln-header.critical { background: var(--critical); }
.vuln-card .vuln-header.high { background: var(--high); }
.vuln-card .vuln-header.medium { background: var(--medium); color: #333; }
.vuln-card .vuln-header.low { background: var(--low); }
.vuln-card .vuln-header .vuln-id { font-size: 18px; font-weight: 700; }
.vuln-card .vuln-header .cvss { font-size: 24px; font-weight: 700; }
.vuln-card .vuln-body { padding: 25px; }
.vuln-card .vuln-body .info-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 12px; margin-bottom: 20px; }
.vuln-card .vuln-body .info-item { display: flex; gap: 8px; }
.vuln-card .vuln-body .info-item .key { color: #666; font-weight: 600; min-width: 80px; }
.repro-step { display: flex; gap: 15px; margin: 15px 0; align-items: flex-start; }
.repro-step .step-num {
    background: var(--primary); color: #fff; width: 32px; height: 32px;
    border-radius: 50%; display: flex; align-items: center; justify-content: center;
    font-weight: 700; flex-shrink: 0; margin-top: 2px;
}
.repro-step .step-content .step-cmd {
    background: #f5f5f5; padding: 8px 14px; border-radius: 4px;
    font-family: monospace; font-size: 13px; margin: 6px 0; border-left: 3px solid var(--primary);
}
.timeline { position: relative; padding-left: 30px; margin: 20px 0; }
.timeline::before { content: ''; position: absolute; left: 8px; top: 0; bottom: 0; width: 3px; background: var(--border); }
.timeline-item { position: relative; margin-bottom: 20px; }
.timeline-item::before {
    content: ''; position: absolute; left: -26px; top: 5px; width: 14px; height: 14px;
    border-radius: 50%; background: var(--primary); border: 3px solid #fff; box-shadow: 0 0 0 2px var(--primary);
}
.timeline-item .time { font-size: 12px; color: #999; }
.toc { background: #f8f9fa; border-radius: 8px; padding: 25px 30px; margin: 20px 0; }
.toc ul { list-style: none; padding: 0; }
.toc ul li { padding: 5px 0; border-bottom: 1px dotted #ddd; }
.page-footer { padding: 10px 50px; border-top: 1px solid var(--border); font-size: 11px; color: #999; text-align: center; }
@media print {
    body { background: #fff; }
    .section { box-shadow: none; border: 1px solid #ddd; page-break-inside: avoid; }
    .cover-page { page-break-after: always; }
}
"""

SEVERITY_CLASS = {"critical": "critical", "high": "high", "medium": "medium", "low": "low", "info": "info"}
SEVERITY_LABEL = {"critical": "严重", "high": "高危", "medium": "中危", "low": "低危", "info": "信息"}

def escape_html(text):
    if not text:
        return ""
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def render_stat_cards(vulns):
    counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
    for v in vulns:
        sev = v.get("severity", "info").lower()
        if sev in counts:
            counts[sev] += 1
    total = sum(counts.values())
    cards = ""
    for sev, label in [("critical","严重"),("high","高危"),("medium","中危"),("low","低危"),("info","信息")]:
        cards += '<div class="stat-card %s"><div class="number">%d</div><div class="label">%s (%s)</div></div>\n' % (sev, counts[sev], label, sev.capitalize())
    cards += '<div class="stat-card total"><div class="number">%d</div><div class="label">总计</div></div>' % total
    return cards, counts, total

def render_cvss_table(cvss):
    if not cvss:
        return ""
    metrics = [
        ("AV", "攻击向量", {"N":"网络","A":"邻接","L":"本地","P":"物理"}),
        ("AC", "攻击复杂度", {"L":"低","H":"高"}),
        ("PR", "所需权限", {"N":"无","L":"低","H":"高"}),
        ("UI", "用户交互", {"N":"无","R":"需要"}),
        ("S", "影响范围", {"U":"不变","C":"改变"}),
        ("C", "机密性影响", {"N":"无","L":"低","H":"高"}),
        ("I", "完整性影响", {"N":"无","L":"低","H":"高"}),
        ("A", "可用性影响", {"N":"无","L":"低","H":"高"}),
    ]
    rows = ""
    for key, name, mapping in metrics:
        val = cvss.get(key, "N")
        desc = mapping.get(val, val)
        rows += '<tr><td>%s (%s)</td><td><strong>%s</strong></td><td>%s</td></tr>\n' % (name, key, val, desc)
    return '<table><thead><tr><th>指标</th><th>值</th><th>说明</th></tr></thead><tbody>%s</tbody></table>' % rows

def render_vuln_card(vuln, index):
    sev = vuln.get("severity", "medium").lower()
    sev_class = SEVERITY_CLASS.get(sev, "medium")
    sev_label = SEVERITY_LABEL.get(sev, "中危")
    vuln_id = escape_html(vuln.get("id", "VULN-%03d" % index))
    title = escape_html(vuln.get("title", "未命名漏洞"))
    cvss_score = str(vuln.get("cvss_score", "N/A"))
    vuln_type = escape_html(vuln.get("type", ""))
    url = escape_html(vuln.get("url", ""))
    param = escape_html(vuln.get("parameter", ""))
    date = vuln.get("date", datetime.now().strftime("%Y-%m-%d"))
    description = escape_html(vuln.get("description", ""))
    impact = escape_html(vuln.get("impact", ""))
    cvss_vector = escape_html(vuln.get("cvss_vector", ""))
    cvss_detail = vuln.get("cvss_detail", {})
    cvss_html = render_cvss_table(cvss_detail)
    
    repro_steps = vuln.get("reproduction_steps", [])
    steps_html = ""
    prerequisites = vuln.get("prerequisites", [])
    if prerequisites:
        steps_html += "<p><strong>前置条件：</strong></p><ul>"
        for p in prerequisites:
            steps_html += "<li>%s</li>" % escape_html(p)
        steps_html += "</ul>\n"
    
    for i, step in enumerate(repro_steps, 1):
        step_title = escape_html(step.get("title", "步骤 %d" % i))
        step_desc = escape_html(step.get("description", ""))
        step_cmd = escape_html(step.get("command", ""))
        steps_html += '<div class="repro-step"><div class="step-num">%d</div><div class="step-content"><strong>%s</strong><p>%s</p>' % (i, step_title, step_desc)
        if step_cmd:
            steps_html += '<div class="step-cmd">%s</div>' % step_cmd
        steps_html += '</div></div>\n'
    
    http_req = vuln.get("http_request", "")
    http_resp = vuln.get("http_response", "")
    http_html = ""
    if http_req:
        http_html += '<h4>HTTP 请求原文</h4>\n<div class="code-block"><span class="lang-tag">HTTP</span>%s</div>\n' % escape_html(http_req)
    if http_resp:
        http_html += '<h4>HTTP 响应原文</h4>\n<div class="code-block"><span class="lang-tag">HTTP</span>%s</div>\n' % escape_html(http_resp)
    
    poc_code = vuln.get("poc", "")
    poc_lang = escape_html(vuln.get("poc_language", "bash"))
    poc_html = ""
    if poc_code:
        poc_html += '<h4>利用验证 (PoC)</h4>\n<div class="code-block"><span class="lang-tag">%s</span>%s</div>\n' % (poc_lang, escape_html(poc_code))
    
    temp_fix = escape_html(vuln.get("temporary_fix", ""))
    fix_description = escape_html(vuln.get("fix_description", ""))
    code_before = escape_html(vuln.get("code_before", ""))
    code_after = escape_html(vuln.get("code_after", ""))
    code_lang = escape_html(vuln.get("code_language", ""))
    fix_changes = vuln.get("fix_changes", [])
    hardening = vuln.get("hardening", [])
    
    fix_html = ""
    if temp_fix:
        fix_html += '<h4>临时缓解措施（立即执行）</h4>\n<div class="alert alert-warning">%s</div>\n' % temp_fix
    if fix_description:
        fix_html += '<h4>根本修复方案（推荐）</h4>\n<p>%s</p>\n' % fix_description
    if code_before:
        fix_html += '<h5>修复前（存在漏洞的代码）：</h5>\n<div class="code-block"><span class="lang-tag">%s</span>%s</div>\n' % (code_lang, code_before)
    if code_after:
        fix_html += '<h5>修复后（安全代码）：</h5>\n<div class="code-block"><span class="lang-tag">%s</span>%s</div>\n' % (code_lang, code_after)
    if fix_changes:
        fix_html += '<h5>关键改动说明：</h5>\n<ol>'
        for c in fix_changes:
            fix_html += '<li>%s</li>' % escape_html(c)
        fix_html += '</ol>\n'
    if hardening:
        fix_html += '<h4>配置加固建议</h4>\n<ul>'
        for h in hardening:
            fix_html += '<li>%s</li>' % escape_html(h)
        fix_html += '</ul>\n'
    
    verify_steps = vuln.get("verification_steps", [])
    verify_expected = escape_html(vuln.get("verification_expected", ""))
    verify_html = ""
    if verify_steps:
        verify_html += '<h3>修复验证方法</h3>\n<div class="alert alert-success"><strong>验证步骤：</strong><ol>'
        for v in verify_steps:
            verify_html += '<li>%s</li>' % escape_html(v)
        verify_html += '</ol></div>\n'
        if verify_expected:
            verify_html += '<p><strong>预期结果：</strong>%s</p>\n' % verify_expected
    
    refs = vuln.get("references", [])
    ref_html = ""
    if refs:
        ref_html += '<h3>参考资料</h3>\n<ul>'
        for r in refs:
            ref_html += '<li>%s</li>' % escape_html(r)
        ref_html += '</ul>\n'
    
    card = '''
    <div class="vuln-card">
        <div class="vuln-header %s">
            <div class="vuln-id">%s - %s</div>
            <div class="cvss">CVSS %s</div>
        </div>
        <div class="vuln-body">
            <div class="info-grid">
                <div class="info-item"><span class="key">漏洞类型：</span><span>%s</span></div>
                <div class="info-item"><span class="key">风险等级：</span><span class="badge badge-%s">%s</span></div>
                <div class="info-item"><span class="key">CVSS评分：</span><span>%s/10.0</span></div>
                <div class="info-item"><span class="key">影响URL：</span><span>%s</span></div>
                <div class="info-item"><span class="key">影响参数：</span><span>%s</span></div>
                <div class="info-item"><span class="key">发现日期：</span><span>%s</span></div>
            </div>
            <h3>漏洞描述</h3>
            <p>%s</p>
            <div class="alert alert-danger"><strong>危害分析：</strong>%s</div>
            <h3>CVSS 3.1 评分详情</h3>
            %s
            %s
            <h3>复现步骤</h3>
            %s
            %s
            %s
            <h3>修复方案</h3>
            %s
            %s
            %s
        </div>
    </div>\n''' % (
        sev_class, vuln_id, title, cvss_score,
        vuln_type, sev_class, sev_label, cvss_score, url, param, date,
        description, impact,
        cvss_html,
        ('<p><strong>CVSS向量：</strong><code>%s</code></p>' % cvss_vector) if cvss_vector else '',
        steps_html, http_html, poc_html,
        fix_html, verify_html, ref_html
    )
    return card

def render_vuln_table(vulns):
    rows = ""
    for i, v in enumerate(vulns):
        sev = v.get("severity", "medium").lower()
        sev_class = SEVERITY_CLASS.get(sev, "medium")
        sev_label = SEVERITY_LABEL.get(sev, "中危")
        rows += '<tr><td>%s</td><td>%s</td><td>%s</td><td><span class="badge badge-%s">%s</span></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>\n' % (
            escape_html(v.get("id", "VULN-%03d" % (i+1))),
            escape_html(v.get("title","")),
            escape_html(v.get("type","")),
            sev_class, sev_label,
            str(v.get("cvss_score","N/A")),
            escape_html(v.get("url","")),
            escape_html(v.get("priority","P1")),
            escape_html(v.get("status","未修复"))
        )
    return rows

def render_remediation_roadmap(vulns):
    groups = {"P0": [], "P1": [], "P2": [], "P3": []}
    for v in vulns:
        p = v.get("priority", "P1").upper()
        if p not in groups:
            p = "P1"
        groups[p].append(v)
    
    labels = {
        "P0": "P0 - 立即修复（24小时内）",
        "P1": "P1 - 本周修复（1周内）",
        "P2": "P2 - 本月修复（1月内）",
        "P3": "P3 - 下迭代修复",
    }
    
    html = ""
    for p in ["P0","P1","P2","P3"]:
        if groups[p]:
            items_html = ""
            for v in groups[p]:
                vid = escape_html(v.get("id", ""))
                title = escape_html(v.get("title", ""))
                items_html += "<li><strong>%s</strong> - %s</li>\n" % (vid, title)
            html += '<div class="timeline-item"><div class="time">%s</div><ul>%s</ul></div>\n' % (labels.get(p, p), items_html)
    return html

def generate_report(project_info, vulns, output_path):
    stat_cards, counts, total = render_stat_cards(vulns)
    vuln_cards = "\n".join([render_vuln_card(v, i+1) for i, v in enumerate(vulns)])
    vuln_table = render_vuln_table(vulns)
    roadmap = render_remediation_roadmap(vulns)
    css = load_css()
    
    classification = escape_html(project_info.get("classification", "内部"))
    client = escape_html(project_info.get("client", ""))
    tester = escape_html(project_info.get("tester", ""))
    project_name = escape_html(project_info.get("project_name", "安全测试项目"))
    doc_id = escape_html(project_info.get("doc_id", ""))
    version = escape_html(project_info.get("version", "1.0"))
    report_date = project_info.get("date", datetime.now().strftime("%Y年%m月%d日"))
    
    overview = escape_html(project_info.get("overview", ""))
    key_critical = escape_html(project_info.get("key_critical_finding", "无"))
    key_high = escape_html(project_info.get("key_high_finding", "无"))
    overall_rating = escape_html(project_info.get("overall_rating", "中"))
    overall_conclusion = escape_html(project_info.get("overall_conclusion", ""))
    
    test_type = escape_html(project_info.get("test_type", "黑盒测试"))
    test_standards_items = "\n".join(["<li>%s</li>" % escape_html(s) for s in project_info.get("test_standards", ["OWASP Top 10 (2021)", "OWASP WSTG", "PTES"])])
    
    timeline_html = ""
    for t in project_info.get("timeline", []):
        timeline_html += '<div class="timeline-item"><div class="time">%s</div><p>%s</p></div>\n' % (escape_html(t.get("date","")), escape_html(t.get("event","")))
    
    team_html = ""
    for m in project_info.get("team", []):
        team_html += "<tr><td>%s</td><td>%s</td><td>%s</td></tr>\n" % (escape_html(m.get('name','')), escape_html(m.get('role','')), escape_html(m.get('duty','')))
    
    scope_html = ""
    for s in project_info.get("scope", []):
        scope_html += "<tr><td>%s</td><td>%s</td><td>%s</td></tr>\n" % (escape_html(s.get('category','')), escape_html(s.get('target','')), escape_html(s.get('note','')))
    
    tools_html = ""
    for t in project_info.get("tools", []):
        tools_html += "<tr><td>%s</td><td>%s</td><td>%s</td></tr>\n" % (escape_html(t.get('name','')), escape_html(t.get('version','')), escape_html(t.get('purpose','')))
    
    compliance_html = ""
    for c in project_info.get("compliance", []):
        compliance_html += "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>\n" % (escape_html(c.get('vuln_id','')), escape_html(c.get('cwe','')), escape_html(c.get('owasp','')), escape_html(c.get('grade_protection','')))
    
    long_term_html = ""
    for l in project_info.get("long_term_improvements", []):
        long_term_html += "<li>%s</li>\n" % escape_html(l)
    
    def pct(n):
        return round(n/total*100, 1) if total > 0 else 0
    
    html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>%s - 渗透测试报告</title>
    <style>%s</style>
</head>
<body>
<div class="cover-page">
    <div class="classification">%s</div>
    <div class="logo-area">&#x1f6e1;&#xfe0f;</div>
    <h1>%s</h1>
    <div class="subtitle">渗透测试报告</div>
    <div class="meta">
        <p><strong>客户单位：</strong>%s</p>
        <p><strong>测试单位：</strong>%s</p>
        <p><strong>报告日期：</strong>%s</p>
        <p><strong>文档编号：</strong>%s</p>
        <p><strong>版本号：</strong>%s</p>
    </div>
    <div class="footer">本文档为保密文件，未经授权不得外传</div>
</div>

<div class="content">
<div class="section toc">
    <h3 style="margin-top:0;border:none;">&#x1f4d1; 目录</h3>
    <ul>
        <li>1. 执行摘要</li>
        <li>2. 测试概述</li>
        <li>3. 漏洞详情（共 %d 个）</li>
        <li>4. 风险汇总</li>
        <li>5. 修复建议路线图</li>
        <li>6. 附录</li>
    </ul>
</div>

<div class="section" id="executive-summary">
    <h2>1. 执行摘要</h2>
    <p>%s</p>
    <div class="stats-row">%s</div>
    <h3>关键发现</h3>
    <div class="alert alert-danger"><strong>&#x1f534; 高危发现：</strong>%s</div>
    <div class="alert alert-warning"><strong>&#x1f7e0; 值得关注：</strong>%s</div>
    <h3>整体评估</h3>
    <p><strong>综合安全评级：</strong>%s</p>
    <p>%s</p>
</div>

<div class="section" id="test-overview">
    <h2>2. 测试概述</h2>
    <h3>2.1 测试范围</h3>
    <table><thead><tr><th>类别</th><th>目标</th><th>说明</th></tr></thead><tbody>%s</tbody></table>
    <h3>2.2 测试方法</h3>
    <p><strong>测试类型：</strong>%s</p>
    <p><strong>测试依据：</strong></p><ul>%s</ul>
    <h3>2.3 测试时间线</h3>
    <div class="timeline">%s</div>
    <h3>2.4 参与人员</h3>
    <table><thead><tr><th>姓名</th><th>角色</th><th>职责</th></tr></thead><tbody>%s</tbody></table>
</div>

<div class="section" id="vuln-details">
    <h2>3. 漏洞详情</h2>
    %s
</div>

<div class="section" id="risk-summary">
    <h2>4. 风险汇总</h2>
    <h3>4.1 漏洞清单</h3>
    <table><thead><tr><th>编号</th><th>漏洞名称</th><th>类型</th><th>风险等级</th><th>CVSS</th><th>影响URL</th><th>修复优先级</th><th>状态</th></tr></thead><tbody>%s</tbody></table>
    <h3>4.2 风险分布统计</h3>
    <table><thead><tr><th>风险等级</th><th>数量</th><th>占比</th><th>修复时限</th></tr></thead>
    <tbody>
        <tr><td><span class="badge badge-critical">严重</span></td><td>%d</td><td>%.1f%%</td><td>24小时</td></tr>
        <tr><td><span class="badge badge-high">高危</span></td><td>%d</td><td>%.1f%%</td><td>1周</td></tr>
        <tr><td><span class="badge badge-medium">中危</span></td><td>%d</td><td>%.1f%%</td><td>1个月</td></tr>
        <tr><td><span class="badge badge-low">低危</span></td><td>%d</td><td>%.1f%%</td><td>3个月</td></tr>
    </tbody></table>
</div>

<div class="section" id="remediation-roadmap">
    <h2>5. 修复建议路线图</h2>
    <div class="timeline">%s</div>
    <h3>安全加固建议</h3>
    <div class="alert alert-info"><strong>&#x1f4a1; 长期安全改进建议：</strong><ul>%s</ul></div>
</div>

<div class="section" id="appendix">
    <h2>6. 附录</h2>
    <h3>6.1 测试工具清单</h3>
    <table><thead><tr><th>工具名称</th><th>版本</th><th>用途</th></tr></thead><tbody>%s</tbody></table>
    <h3>6.2 术语表</h3>
    <table><thead><tr><th>术语</th><th>说明</th></tr></thead>
    <tbody>
        <tr><td>CVE</td><td>通用漏洞披露</td></tr>
        <tr><td>CVSS</td><td>通用漏洞评分系统</td></tr>
        <tr><td>OWASP</td><td>开源Web应用安全项目</td></tr>
        <tr><td>POC</td><td>概念验证</td></tr>
        <tr><td>WAF</td><td>Web应用防火墙</td></tr>
        <tr><td>PTES</td><td>渗透测试执行标准</td></tr>
    </tbody></table>
    <h3>6.3 合规对照</h3>
    <table><thead><tr><th>漏洞编号</th><th>CWE</th><th>OWASP Top 10</th><th>等保2.0要求</th></tr></thead><tbody>%s</tbody></table>
</div>

</div>

<div class="page-footer">
    %s | 渗透测试报告 | 密级:%s
</div>
</body>
</html>""" % (
        project_name, css,
        classification, project_name, client, tester, report_date, doc_id, version,
        total,
        overview, stat_cards, key_critical, key_high, overall_rating, overall_conclusion,
        scope_html, test_type, test_standards_items, timeline_html, team_html,
        vuln_cards,
        vuln_table,
        counts["critical"], pct(counts["critical"]),
        counts["high"], pct(counts["high"]),
        counts["medium"], pct(counts["medium"]),
        counts["low"], pct(counts["low"]),
        roadmap, long_term_html,
        tools_html, compliance_html,
        client, classification
    )
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return html

def main():
    parser = argparse.ArgumentParser(description="渗透测试HTML报告生成器")
    parser.add_argument("--input", "-i", required=True, help="JSON输入文件路径")
    parser.add_argument("--output", "-o", default="penetration_test_report.html", help="输出HTML文件路径")
    args = parser.parse_args()
    
    with open(args.input, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    project_info = data.get("project", {})
    vulns = data.get("vulnerabilities", [])
    
    if not vulns:
        print("WARNING: 未找到漏洞数据，将生成空报告")
    
    generate_report(project_info, vulns, args.output)
    print("报告已生成: %s" % args.output)
    print("漏洞数量: %d" % len(vulns))
    print("请在浏览器中打开查看，或使用 Ctrl+P 打印为 PDF")

if __name__ == "__main__":
    main()
