# AI基础设施指纹识别参考 / AI Infrastructure Fingerprints

## 平台识别特征

### FastGPT
```
响应头: x-powered-by: Next.js
路径: /api/common/system/getInitData
路径: /api/v2/chat/completions
前端: _next/static/*, React + Chakra UI
特征JS: chatId, shareId, outLinkUid, appId
配置泄露: systemTitle, systemDescription, feConfigs
```

### Dify
```
路径: /v1/chat-messages, /v1/parameters
路径: /console/api/apps
前端: React + Tailwind
Cookie: remember_token, dify-session
特征: X-App-Code header
```

### Flowise
```
路径: /api/v1/prediction/{id}
路径: /api/v1/chatflows
前端: React + MUI
特征: chatflow_id参数
管理面板: /canvas
```

### Coze / 扣子
```
路径: /api/playground/chat (国内版)
路径: /v3/chat (API)
前端: React + Arco Design
特征: bot_id, conversation_id
域名: coze.cn (国内) / coze.com (海外)
```

### LangChain (LangServe)
```
路径: /invoke, /stream
路径: /input_schema, /output_schema, /config_schema
路径: /playground
特征: Pydantic schema格式
```

### MaxKB
```
路径: /api/application/chat
前端: Vue + Element Plus
特征: 开源知识库管理
域名: 通常自部署
```

### AnythingLLM
```
路径: /api/v1/workspace/{slug}/chat
路径: /api/v1/system/health
前端: React
管理面板: /settings
```

## 推理引擎识别

### vLLM
```bash
curl -s http://TARGET:8000/version
# {"version": "0.x.x"}
curl -s http://TARGET:8000/v1/models
# OpenAI兼容格式
```

### Ollama
```bash
curl -s http://TARGET:11434/api/tags
# {"models": [{"name": "llama3", ...}]}
```

### TGI (Text Generation Inference)
```bash
curl -s http://TARGET:8080/info
# {"model_id": "...", "model_sha": "...", ...}
```

### Triton
```bash
curl -s http://TARGET:8000/v2/health/ready
# 200 = ready
curl -s http://TARGET:8000/v2/models
# {"models": [...]}
```

## 向量数据库识别

| 数据库 | 默认端口 | 健康检查 |
|---|---|---|
| Qdrant | 6333 (HTTP), 6334 (gRPC) | `GET /collections` |
| Milvus | 9091 (HTTP), 19530 (gRPC) | `GET /api/v1/health` |
| Weaviate | 8080 | `GET /v1/.well-known/ready` |
| ChromaDB | 8000 | `GET /api/v1/heartbeat` |
| Pinecone | cloud only | requires API key |
| pgvector | 5432 | PostgreSQL连接 |

## 快速扫描脚本

```bash
#!/bin/bash
TARGET=$1
echo "=== 平台识别 ==="
curl -sI "$TARGET" | grep -iE 'server|x-powered|set-cookie'
echo "=== FastGPT ===" && curl -s "$TARGET/api/common/system/getInitData" | head -50
echo "=== Dify ===" && curl -s "$TARGET/v1/parameters" | head -50
echo "=== Flowise ===" && curl -s "$TARGET/api/v1/chatflows" | head -50
echo "=== 推理端点 ==="
for port in 8000 8080 11434; do
  curl -s "http://$TARGET:$port/v1/models" 2>/dev/null | head -20
  curl -s "http://$TARGET:$port/api/tags" 2>/dev/null | head -20
done
echo "=== 向量数据库 ==="
for port in 6333 9091 8080 8000; do
  curl -s "http://$TARGET:$port/collections" 2>/dev/null | head -20
done
```
