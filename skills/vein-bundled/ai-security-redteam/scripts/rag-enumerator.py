#!/usr/bin/env python3
"""
RAG Knowledge Base Enumerator
自动化RAG知识库枚举 — 通过detail:true提取文档名、来源、引用

用法:
    python3 rag-enumerator.py --target https://TARGET_HOST \
        --share-id YOUR_SHARE_ID \
        --queries queries.txt \
        --output rag-enum.json

    python3 rag-enumerator.py --target https://TARGET \
        --share-id SHARE_ID \
        --auto-queries 20
"""

import argparse
import json
import sys
import time
import urllib.request
import urllib.error


DEFAULT_QUERIES = [
    "请介绍一下相关政策",
    "有哪些补贴可以申请",
    "申请条件是什么",
    "需要哪些材料",
    "如何办理",
    "最新的政策变化",
    "有哪些优惠措施",
    "人才引进政策",
    "创业扶持",
    "住房补贴",
    "教育政策",
    "医疗保障",
    "社会保险",
    "税收优惠",
    "科研资助",
    "培训补贴",
    "就业指导",
    "实习岗位",
    "技能认证",
    "退休待遇",
]


def query_with_detail(target: str, share_id: str, query: str, idx: int) -> dict:
    body = {
        "messages": [{"role": "user", "content": query}],
        "shareId": share_id,
        "outLinkUid": "rag-enum",
        "chatId": f"enum-{idx}",
        "stream": False,
        "detail": True,
    }
    data = json.dumps(body).encode()
    req = urllib.request.Request(
        f"{target}/api/v2/chat/completions",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except Exception as e:
        return {"error": str(e)}


def extract_rag_info(resp: dict) -> list:
    sources = []
    for item in resp.get("responseData", []):
        module_type = item.get("moduleType", "")

        for quote in item.get("quoteList", []) or []:
            source = {
                "datasetName": quote.get("datasetName", ""),
                "collectionName": quote.get("collectionName", ""),
                "sourceName": quote.get("sourceName", ""),
                "sourceId": quote.get("sourceId", ""),
                "datasetId": quote.get("datasetId", ""),
                "collectionId": quote.get("collectionId", ""),
                "score": quote.get("score", 0),
                "q": quote.get("q", "")[:100],
                "a": quote.get("a", "")[:200],
            }
            sources.append(source)

        if "dataset" in module_type.lower() or "search" in module_type.lower():
            if "tokens" in item:
                sources.append({
                    "moduleType": module_type,
                    "tokens": item.get("tokens", 0),
                    "note": "RAG search node detected",
                })

    return sources


def main():
    ap = argparse.ArgumentParser(description="RAG Knowledge Base Enumerator")
    ap.add_argument("--target", required=True, help="目标URL")
    ap.add_argument("--share-id", required=True, help="ShareID")
    ap.add_argument("--queries", help="查询文件 (每行一个)")
    ap.add_argument("--auto-queries", type=int, default=0, help="使用内置查询数量")
    ap.add_argument("--output", default="rag-enum.json", help="输出JSON")
    ap.add_argument("--delay", type=float, default=1.5, help="请求间隔秒数")
    args = ap.parse_args()

    queries = []
    if args.queries:
        with open(args.queries) as f:
            queries = [line.strip() for line in f if line.strip()]
    elif args.auto_queries > 0:
        queries = DEFAULT_QUERIES[:args.auto_queries]
    else:
        queries = DEFAULT_QUERIES[:10]

    print(f"[*] 目标: {args.target}")
    print(f"[*] 查询数: {len(queries)}")
    print()

    all_sources = {}
    all_raw = []

    for i, query in enumerate(queries, 1):
        print(f"[{i}/{len(queries)}] {query[:40]}...", end=" ", flush=True)
        resp = query_with_detail(args.target, args.share_id, query, i)
        sources = extract_rag_info(resp)

        new_count = 0
        for src in sources:
            key = src.get("sourceName") or src.get("collectionName") or src.get("moduleType", "")
            if not key:
                continue
            if key not in all_sources:
                all_sources[key] = {
                    "datasetName": src.get("datasetName", ""),
                    "collectionName": src.get("collectionName", ""),
                    "sourceName": src.get("sourceName", ""),
                    "sourceId": src.get("sourceId", ""),
                    "datasetId": src.get("datasetId", ""),
                    "collectionId": src.get("collectionId", ""),
                    "queries_triggered": [],
                    "sample_content": [],
                    "max_score": 0,
                    "hit_count": 0,
                }
                new_count += 1
            entry = all_sources[key]
            entry["queries_triggered"].append(query)
            entry["hit_count"] += 1
            if src.get("score", 0) > entry["max_score"]:
                entry["max_score"] = src["score"]
            if src.get("q") and len(entry["sample_content"]) < 3:
                entry["sample_content"].append({"q": src["q"], "a": src.get("a", "")})

        all_raw.append({"query": query, "sources_found": len(sources), "new_sources": new_count})
        print(f"found {len(sources)} refs, {new_count} new")

        time.sleep(args.delay)

    report = {
        "target": args.target,
        "share_id": args.share_id,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "total_queries": len(queries),
        "unique_sources": len(all_sources),
        "sources": dict(sorted(all_sources.items(), key=lambda x: x[1]["hit_count"], reverse=True)),
        "query_log": all_raw,
    }

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print()
    print(f"[*] 发现 {len(all_sources)} 个独立数据源:")
    for name, info in sorted(all_sources.items(), key=lambda x: x[1]["hit_count"], reverse=True):
        dataset = info.get("datasetName", "")
        print(f"    {name} (dataset: {dataset}, hits: {info['hit_count']}, score: {info['max_score']:.2f})")

    print(f"\n[*] 报告已保存: {args.output}")


if __name__ == "__main__":
    main()
