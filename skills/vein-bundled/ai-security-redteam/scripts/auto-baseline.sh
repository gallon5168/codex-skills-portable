#!/bin/bash
# AI Security Auto-Baseline Scanner
# 自动化基线安全扫描 — 目标指纹识别 + 基础漏洞检测
#
# 用法: ./auto-baseline.sh <TARGET_URL> [SHARE_ID] [OUTPUT_DIR]
# 示例: ./auto-baseline.sh https://TARGET_HOST YOUR_SHARE_ID ./results
#
# 输出: JSON格式的扫描报告

set -euo pipefail

TARGET="${1:?用法: $0 <TARGET_URL> [SHARE_ID] [OUTPUT_DIR]}"
SHARE_ID="${2:-}"
OUTPUT_DIR="${3:-./ai-security-results}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
REPORT_DIR="$OUTPUT_DIR/$TIMESTAMP"

mkdir -p "$REPORT_DIR"

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() { echo -e "${BLUE}[*]${NC} $1"; }
ok() { echo -e "${GREEN}[+]${NC} $1"; }
warn() { echo -e "${YELLOW}[!]${NC} $1"; }
fail() { echo -e "${RED}[-]${NC} $1"; }

FINDINGS=0
finding() {
    FINDINGS=$((FINDINGS + 1))
    warn "发现 #$FINDINGS: $1 [$2]"
    echo "{\"id\":$FINDINGS,\"title\":\"$1\",\"severity\":\"$2\",\"detail\":\"$3\"}" >> "$REPORT_DIR/findings.jsonl"
}

# ========== Phase 1: 目标指纹 ==========
log "Phase 1: 目标指纹识别"

# HTTP头
log "  检查HTTP响应头..."
curl -sI "$TARGET/" -o "$REPORT_DIR/headers.txt" 2>/dev/null
HEADERS=$(cat "$REPORT_DIR/headers.txt")

# 安全头检查
for header in "Strict-Transport-Security" "Content-Security-Policy" "X-Frame-Options" "X-Content-Type-Options"; do
    if ! echo "$HEADERS" | grep -qi "$header"; then
        finding "缺少安全头: $header" "Low" "响应中未设置$header头"
    fi
done

# Server header
SERVER=$(echo "$HEADERS" | grep -i "^server:" | head -1 | cut -d: -f2- | xargs)
[ -n "$SERVER" ] && log "  Server: $SERVER"

# CORS检查
log "  检查CORS配置..."
CORS_RESP=$(curl -sI "$TARGET/" -H "Origin: https://evil.example.com" 2>/dev/null)
CORS_ORIGIN=$(echo "$CORS_RESP" | grep -i "access-control-allow-origin" | head -1)
if echo "$CORS_ORIGIN" | grep -qi "evil.example.com\|\*"; then
    finding "CORS配置过于宽松" "Medium" "允许任意来源: $CORS_ORIGIN"
fi

# ========== Phase 2: 平台识别 ==========
log "Phase 2: AI平台识别"

PLATFORM="unknown"

# FastGPT
INIT_DATA=$(curl -s "$TARGET/api/common/system/getInitData" 2>/dev/null)
if echo "$INIT_DATA" | python3 -c "import json,sys;json.load(sys.stdin)" 2>/dev/null; then
    PLATFORM="FastGPT"
    ok "  检测到 FastGPT"
    echo "$INIT_DATA" > "$REPORT_DIR/init_data.json"

    SYS_TITLE=$(echo "$INIT_DATA" | python3 -c "import json,sys;d=json.load(sys.stdin);print(d.get('data',{}).get('systemTitle',''))" 2>/dev/null)
    [ -n "$SYS_TITLE" ] && log "  系统标题: $SYS_TITLE"

    # 检查配置泄露
    SENSITIVE_KEYS=$(echo "$INIT_DATA" | python3 -c "
import json,sys
d=json.load(sys.stdin).get('data',{})
keys=['apiBaseUrl','feConfigs','subPlans','systemVersion']
found=[k for k in keys if k in d and d[k]]
print(' '.join(found))
" 2>/dev/null)
    [ -n "$SENSITIVE_KEYS" ] && finding "API配置信息泄露" "Medium" "getInitData暴露: $SENSITIVE_KEYS"
fi

# Dify
DIFY_RESP=$(curl -s "$TARGET/v1/parameters" -H "Authorization: Bearer test" 2>/dev/null)
if echo "$DIFY_RESP" | grep -q "user_input_form\|opening_statement" 2>/dev/null; then
    PLATFORM="Dify"
    ok "  检测到 Dify"
fi

# Flowise
FLOWISE_RESP=$(curl -s "$TARGET/api/v1/chatflows" 2>/dev/null)
if echo "$FLOWISE_RESP" | grep -q "chatflows\|flowData" 2>/dev/null; then
    PLATFORM="Flowise"
    ok "  检测到 Flowise"
fi

# Ollama
OLLAMA_RESP=$(curl -s "$TARGET:11434/api/tags" 2>/dev/null)
if echo "$OLLAMA_RESP" | grep -q '"models"' 2>/dev/null; then
    finding "Ollama API暴露" "High" "无认证可访问模型列表"
fi

log "  平台: $PLATFORM"
echo "$PLATFORM" > "$REPORT_DIR/platform.txt"

# ========== Phase 3: Source Maps & JS ==========
log "Phase 3: 前端资产检查"

# Next.js source map
NEXTJS_CHECK=$(curl -s "$TARGET/" 2>/dev/null | grep -oE '_next/static/[^"]+' | head -1)
if [ -n "$NEXTJS_CHECK" ]; then
    BUILD_ID=$(echo "$NEXTJS_CHECK" | grep -oE '_next/static/[^/]+' | head -1 | sed 's|_next/static/||')
    log "  Next.js Build ID: $BUILD_ID"

    # Source maps
    SRCMAP=$(curl -s -o /dev/null -w '%{http_code}' "$TARGET/_next/static/chunks/main.js.map" 2>/dev/null)
    [ "$SRCMAP" = "200" ] && finding "Source Map暴露" "Medium" "可访问main.js.map"

    # Build manifest
    MANIFEST_CODE=$(curl -s -o /dev/null -w '%{http_code}' "$TARGET/_next/static/$BUILD_ID/_buildManifest.js" 2>/dev/null)
    [ "$MANIFEST_CODE" = "200" ] && log "  Build manifest可访问"
fi

# ========== Phase 4: API端点探测 ==========
log "Phase 4: API端点探测"

ENDPOINTS="/api/admin /api/debug /api/health /api/metrics /api/status /graphql /api/v1/models /v1/models"

for ep in $ENDPOINTS; do
    CODE=$(curl -s -o /dev/null -w '%{http_code}' "$TARGET$ep" 2>/dev/null)
    case "$CODE" in
        200) finding "管理/调试端点可访问: $ep" "Medium" "返回200" ;;
        500) log "  $ep → 500 (可能存在但缺少认证)" ;;
        *) ;;
    esac
done

# ========== Phase 5: Chat API测试 ==========
if [ -n "$SHARE_ID" ]; then
    log "Phase 5: Chat API安全测试"
    CHAT_URL="$TARGET/api/v2/chat/completions"

    # 5.1 基本对话
    log "  测试基本对话..."
    CHAT_RESP=$(curl -s "$CHAT_URL" \
        -X POST -H 'Content-Type: application/json' \
        -d "{\"messages\":[{\"role\":\"user\",\"content\":\"你好\"}],\"shareId\":\"$SHARE_ID\",\"outLinkUid\":\"baseline-test\",\"stream\":false}" 2>/dev/null)

    if echo "$CHAT_RESP" | python3 -c "import json,sys;d=json.load(sys.stdin);print(d.get('choices',[{}])[0].get('message',{}).get('content','')[:100])" 2>/dev/null; then
        ok "  对话API正常工作"
    fi

    # 5.2 detail:true泄露检查
    log "  测试detail:true信息泄露..."
    DETAIL_RESP=$(curl -s "$CHAT_URL" \
        -X POST -H 'Content-Type: application/json' \
        -d "{\"messages\":[{\"role\":\"user\",\"content\":\"你好\"}],\"shareId\":\"$SHARE_ID\",\"outLinkUid\":\"baseline-test\",\"stream\":false,\"detail\":true}" 2>/dev/null)
    echo "$DETAIL_RESP" > "$REPORT_DIR/detail_response.json"

    # 检查是否有responseData
    HAS_DETAIL=$(echo "$DETAIL_RESP" | python3 -c "
import json,sys
d=json.load(sys.stdin)
rd = d.get('responseData',[])
if rd:
    types = [item.get('moduleType','') for item in rd]
    print(' '.join(types))
" 2>/dev/null)
    [ -n "$HAS_DETAIL" ] && finding "detail:true暴露内部工作流" "Medium" "可见节点: $HAS_DETAIL"

    # 检查quoteList(RAG文档泄露)
    QUOTES=$(echo "$DETAIL_RESP" | python3 -c "
import json,sys
d=json.load(sys.stdin)
for item in d.get('responseData',[]):
    for q in item.get('quoteList',[]) or []:
        name = q.get('sourceName','') or q.get('collectionName','')
        if name: print(name)
" 2>/dev/null)
    [ -n "$QUOTES" ] && finding "RAG文档名称通过引用泄露" "Medium" "可见文档: $(echo $QUOTES | head -c 200)"

    # 5.3 SSE流式推理token检查
    log "  测试SSE流式推理泄露..."
    SSE_RESP=$(curl -s "$CHAT_URL" \
        -X POST -H 'Content-Type: application/json' \
        -d "{\"messages\":[{\"role\":\"user\",\"content\":\"你好\"}],\"shareId\":\"$SHARE_ID\",\"outLinkUid\":\"baseline-test\",\"stream\":true,\"detail\":true}" \
        --max-time 15 2>/dev/null)
    echo "$SSE_RESP" > "$REPORT_DIR/sse_response.txt"

    REASONING=$(echo "$SSE_RESP" | grep -o '"reasoning_content":"[^"]*"' | head -3)
    [ -n "$REASONING" ] && finding "SSE推理token泄露" "High" "reasoning_content可见: $(echo $REASONING | head -c 200)"

    FLOW_NODES=$(echo "$SSE_RESP" | grep -o '"flowNodeStatus"' | wc -l | xargs)
    [ "$FLOW_NODES" -gt 0 ] && finding "SSE工作流节点状态泄露" "Low" "flowNodeStatus事件: ${FLOW_NODES}个"

    # 5.4 速率限制检查
    log "  测试速率限制..."
    RATE_OK=0
    for i in $(seq 1 10); do
        CODE=$(curl -s -o /dev/null -w '%{http_code}' "$CHAT_URL" \
            -X POST -H 'Content-Type: application/json' \
            -d "{\"messages\":[{\"role\":\"user\",\"content\":\"测试$i\"}],\"shareId\":\"$SHARE_ID\",\"outLinkUid\":\"rate-test\",\"stream\":false}" 2>/dev/null)
        [ "$CODE" = "429" ] && RATE_OK=1 && break
    done
    [ "$RATE_OK" = "0" ] && finding "缺少速率限制" "Medium" "10次快速请求均未触发429"

    # 5.5 无效ShareID测试
    INVALID_SHARE=$(curl -s -o /dev/null -w '%{http_code}' "$CHAT_URL" \
        -X POST -H 'Content-Type: application/json' \
        -d '{"messages":[{"role":"user","content":"test"}],"shareId":"invalid_id_12345","outLinkUid":"test","stream":false}' 2>/dev/null)
    [ "$INVALID_SHARE" != "403" ] && [ "$INVALID_SHARE" != "401" ] && log "  无效shareId返回: $INVALID_SHARE"

    # 5.6 错误信息泄露检查
    log "  测试错误信息泄露..."
    ERR_RESP=$(curl -s "$CHAT_URL" \
        -X POST -H 'Content-Type: application/json' \
        -d '{"messages":"not_array","shareId":"'"$SHARE_ID"'","stream":false}' 2>/dev/null)

    if echo "$ERR_RESP" | grep -qiE "stack|trace|internal|error.*detail|module|function"; then
        finding "错误信息泄露内部细节" "Low" "$(echo $ERR_RESP | head -c 200)"
    fi

    # 5.7 HTTP方法测试
    log "  测试HTTP方法..."
    for method in PUT DELETE PATCH; do
        METHOD_CODE=$(curl -s -o /dev/null -w '%{http_code}' -X "$method" "$CHAT_URL" \
            -H 'Content-Type: application/json' -d '{}' 2>/dev/null)
        [ "$METHOD_CODE" != "403" ] && [ "$METHOD_CODE" != "405" ] && log "  $method → $METHOD_CODE (预期403/405)"
    done
fi

# ========== Phase 6: 向量数据库扫描 ==========
log "Phase 6: 向量数据库探测"

TARGET_HOST=$(echo "$TARGET" | sed 's|https\?://||' | cut -d/ -f1 | cut -d: -f1)

for port_name in "6333:Qdrant" "9091:Milvus" "8080:Weaviate"; do
    PORT=$(echo "$port_name" | cut -d: -f1)
    NAME=$(echo "$port_name" | cut -d: -f2)
    VDB_RESP=$(curl -s --connect-timeout 3 "http://$TARGET_HOST:$PORT/collections" 2>/dev/null)
    if [ -n "$VDB_RESP" ] && echo "$VDB_RESP" | grep -q "collections\|result" 2>/dev/null; then
        finding "$NAME向量数据库暴露" "High" "端口$PORT无认证可访问"
    fi
done

# ========== 汇总报告 ==========
echo ""
log "=========================================="
log "扫描完成"
log "=========================================="
log "目标: $TARGET"
log "平台: $PLATFORM"
log "发现数量: $FINDINGS"
log "报告目录: $REPORT_DIR"

# 生成JSON汇总
python3 -c "
import json, os
findings = []
fpath = '$REPORT_DIR/findings.jsonl'
if os.path.exists(fpath):
    with open(fpath) as f:
        for line in f:
            line = line.strip()
            if line:
                findings.append(json.loads(line))

report = {
    'target': '$TARGET',
    'platform': '$PLATFORM',
    'share_id': '$SHARE_ID',
    'timestamp': '$TIMESTAMP',
    'total_findings': len(findings),
    'by_severity': {},
    'findings': findings
}
for f in findings:
    sev = f['severity']
    report['by_severity'][sev] = report['by_severity'].get(sev, 0) + 1

with open('$REPORT_DIR/report.json', 'w') as f:
    json.dump(report, f, indent=2, ensure_ascii=False)
print(json.dumps(report['by_severity'], indent=2))
" 2>/dev/null

log "JSON报告: $REPORT_DIR/report.json"
echo ""
