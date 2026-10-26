#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
infogather_quake.py — Quake 360 测绘数据合并 & body搜索质检工具

功能:
  1. classify_results() → 对 Quake 原始记录分类(Lavel A/B)
  2. check_body_confidence() → 对 body 搜索产出做可信度判断
  3. quake_to_report() → 转 infogather_report.py 的 JSON 输入格式

用法:
  # 1) 分类 domain 搜索产出
  python infogather_quake.py classify diagnoses.json [output.json]

  # 2) 质检 body 搜索产出（判断搜索结果是否可信）
  python infogather_quake.py check data.json

  # 3) 转 infogather_report.py 需要的格式
  python infogather_quake.py to-report data.json report_data.json
"""

import json, sys
from collections import Counter


# ══════════════════════════════════════════════
# 功能 1: 分类 domain 搜索产出
# ══════════════════════════════════════════════

def classify_results(diagnoses: list) -> dict:
    """对诊断结果分类并生成结构化数据"""
    level_a = []   # domain搜 → 可信IP
    level_b = []   # 聚合有值 → 知有资产

    for d in diagnoses:
        label = d.get("label", d.get("query", "未知"))
        uniqueIP = d.get("uniqueIP", 0)
        dataIPs = d.get("dataIPs", 0)
        hasData = d.get("hasData", False)
        records = d.get("records", [])
        ips = list(dict.fromkeys([r["ip"] for r in records if r.get("ip")]))

        if hasData and dataIPs > 0:
            level_a.append({
                "label": label,
                "uniqueIP_agg": uniqueIP,
                "extractedIPs": len(ips),
                "ips": ips,
                "records": records,
                "ports": d.get("ports", ""),
                "services": d.get("services", "")
            })
        elif uniqueIP > 0:
            level_b.append({
                "label": label,
                "uniqueIP_agg": uniqueIP,
                "extractedIPs": 0,
                "ips": [],
                "records": [],
                "ports": d.get("ports", ""),
                "services": d.get("services", "")
            })

    return {"level_a": level_a, "level_b": level_b}


# ══════════════════════════════════════════════
# 功能 2: body 搜索质检（2026-07-17 新增）
# ══════════════════════════════════════════════

def check_body_confidence(records: list, target_name: str = "") -> dict:
    """
    对 body/模糊搜索的 Quake 原始记录做可信度判断

    判断标准：
      - IP <= 10 且 标题全部指向目标 → 可信 (confidence: high)
      - IP 11-50 或 标题部分匹配 → 部分可信 (medium)
      - IP > 50 或 标题无关 → 不可信 (low)

    输入: Quake search API 返回的 records（list of dict, 含 ip/port/service.http.title 等）
    输出: {"confidence": "high|medium|low", "summary": "...", ...}
    """
    if not records:
        return {"confidence": "none", "unique_ips": 0, "total": 0, "summary": "无数据"}

    # 统计
    all_ips = list(dict.fromkeys([r["ip"] for r in records if r.get("ip")]))
    titles = [((r.get("service") or {}).get("http") or {}).get("title", "") for r in records]
    non_empty_titles = [t.strip() for t in titles if t and t.strip()]

    # 唯一IP数
    unique_ip_count = len(all_ips)

    # 标题中命中目标关键词的比例
    if target_name:
        keywords = target_name.replace("（", "(").replace("）", ")").lower().split()
        matched = sum(1 for t in non_empty_titles if any(k in t.lower() for k in keywords))
        hit_ratio = matched / len(non_empty_titles) if non_empty_titles else 0
    else:
        hit_ratio = 1.0 if non_empty_titles else 0

    # 判定
    if unique_ip_count <= 10 and hit_ratio >= 0.5:
        confidence = "high"
    elif unique_ip_count <= 50 and hit_ratio >= 0.3:
        confidence = "medium"
    else:
        confidence = "low"

    return {
        "confidence": confidence,
        "unique_ips": unique_ip_count,
        "total_records": len(records),
        "target_name": target_name,
        "title_match_ratio": round(hit_ratio, 2),
        "all_ips": all_ips,
        "titles_sample": non_empty_titles[:10],
        "summary": {
            "high": "✅ 可信 — 目标专用系统/IP",
            "medium": "⚠️ 部分可信 — 需人工验证",
            "low": "❌ 不可信 — 误报率高",
            "none": "— 无数据",
        }.get(confidence, ""),
        "action": {
            "high": "直接列入资产表",
            "medium": "配合 domain搜索/备案反查 交叉验证",
            "low": "仅作参考，不以 IP 列入可信资产",
            "none": "换搜索词重试",
        }.get(confidence, ""),
    }


# ══════════════════════════════════════════════
# 功能 3: 转 infogather_report.py 的 JSON 格式
# ══════════════════════════════════════════════

def quake_to_report(records: list, target_name: str = "") -> dict:
    """
    将 Quake 原始记录（list of {ip, port, hostname, service.http.title}）
    转为 infogather_report.py 可消费的 JSON 格式

    去重规则: 相同 (IP, port, title) 只保留一条
    """
    seen = set()
    domains_map = {}
    ips_map = {}
    urls_list = []
    systems_map = {}

    for r in records:
        ip = r.get("ip", "")
        port = r.get("port", 0)
        title = ((r.get("service") or {}).get("http") or {}).get("title", "").strip()
        hostname = r.get("hostname", "")

        key = "%s:%s|%s" % (ip, port, title)
        if key in seen:
            continue
        seen.add(key)

        scheme = "https" if port in (443, 8443, 9443) else "http"
        url = "%s://%s:%s" % (scheme, ip, port)

        # 识别备注
        note = ""
        if "JumpServer" in title or "堡垒机" in title:
            note = "⚠️堡垒机"
        elif "LogViwer" in title or "日志" in title:
            note = "⚠️日志查看器"
        elif "接口文档" in title or "webapi" in title or "swagger" in title.lower():
            note = "⭐API文档"
        elif "后台" in title or "管理" in title:
            note = "管理后台"
        elif "登录" in title or "login" in title.lower():
            note = "登录页"
        elif not title:
            note = "(空标题)"
        elif "nginx" in title.lower():
            note = "默认页"

        urls_list.append({
            "url": url,
            "system": title or "(空标题)",
            "accessible": "公网可达",
            "ip": ip,
            "source": "Quake360 %s" % target_name,
            "note": note,
        })

        # IP去重
        if ip and ip not in ips_map:
            ips_map[ip] = {"ip": ip, "domain": hostname, "location": "", "isp": "", "type": "Quake发现", "source": "Quake360"}

        # 域名去重
        if hostname and hostname not in domains_map:
            domains_map[hostname] = {"domain": hostname, "unit": target_name, "ip": ip, "source": "Quake360", "note": ""}

        # 系统去重
        if title and title not in systems_map:
            systems_map[title] = {"system": title, "tech": "", "unit": target_name, "ports": str(port), "source": "Quake360"}
        elif title:
            existing = systems_map[title]["ports"]
            if str(port) not in existing:
                systems_map[title]["ports"] += "/%s" % port

    result = {
        "domains": list(domains_map.values()),
        "ips": list(ips_map.values()),
        "urls": urls_list,
        "systems": list(systems_map.values()),
        "social": [],
        "todos": [],
    }

    # 自动生成待办
    high_items = [u for u in urls_list if u["note"].startswith("⚠️") or u["note"].startswith("⭐")]
    if high_items:
        for item in high_items[:5]:
            result["todos"].append({
                "priority": "⭐⭐⭐",
                "action": "%s — %s (%s)" % (item["note"], item["system"], item["url"]),
            })
    if urls_list:
        result["todos"].append({
            "priority": "⭐⭐",
            "action": "测试 %s 个公网可达系统的弱口令/默认配置" % len(urls_list),
        })

    return result


# ══════════════════════════════════════════════
# 主入口
# ══════════════════════════════════════════════

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法:")
        print("  python infogather_quake.py classify diagnoses.json [output.json]")
        print("  python infogather_quake.py check data.json [target_name]")
        print("  python infogather_quake.py to-report data.json [output.json]")
        sys.exit(1)

    mode = sys.argv[1]
    input_path = sys.argv[2]

    with open(input_path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    if mode == "classify":
        classified = classify_results(raw)
        a = classified["level_a"]
        b = classified["level_b"]
        print("Level A (domain搜可信): %d 条" % len(a))
        print("Level B (聚合有值): %d 条" % len(b))
        output_path = sys.argv[3] if len(sys.argv) > 3 else None
        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(classified, f, ensure_ascii=False, indent=2)
            print("已导出:", output_path)

    elif mode == "check":
        target = sys.argv[3] if len(sys.argv) > 3 else ""
        result = check_body_confidence(raw, target)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif mode == "to-report":
        target = sys.argv[3] if len(sys.argv) > 3 else ""
        report_input = quake_to_report(raw, target)
        output_path = sys.argv[4] if len(sys.argv) > 4 else "report_input.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(report_input, f, ensure_ascii=False, indent=2)
        print("已转换: %s" % output_path)
        print("  domains: %d, ips: %d, urls: %d, systems: %d, todos: %d" % (
            len(report_input["domains"]), len(report_input["ips"]),
            len(report_input["urls"]), len(report_input["systems"]),
            len(report_input["todos"])))
