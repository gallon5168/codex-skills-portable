# RAG平台API端点参考 / RAG Platform API Endpoints

## FastGPT

| 功能 | 端点 | 方法 |
|---|---|---|
| 数据集列表 | `/api/core/dataset/list` | GET |
| 集合列表 | `/api/core/dataset/collection/list?datasetId=ID` | GET |
| 数据详情 | `/api/core/dataset/data/detail?id=ID` | GET |
| 搜索测试 | `/api/core/dataset/searchTest` | POST |
| 对话（带引用） | `/api/v2/chat/completions` + `detail:true` | POST |
| 文件上传 | `/api/common/file/upload` | POST |
| 网站同步 | `/api/core/dataset/collection/create/link` | POST |
| 应用详情 | `/api/core/app/detail?appId=ID` | GET |
| 初始化数据 | `/api/common/system/getInitData` | GET |

## Dify

| 功能 | 端点 | 方法 |
|---|---|---|
| 对话 | `/v1/chat-messages` | POST |
| 知识库列表 | `/v1/datasets` | GET |
| 文档列表 | `/v1/datasets/{id}/documents` | GET |
| 应用信息 | `/v1/parameters` | GET |
| 消息反馈 | `/v1/messages/{id}/feedbacks` | POST |
| 文件上传 | `/v1/files/upload` | POST |
| 对话历史 | `/v1/messages` | GET |

## LangChain (LangServe / LangSmith)

| 功能 | 端点 | 方法 |
|---|---|---|
| 调用链 | `/invoke` | POST |
| 流式调用 | `/stream` | POST |
| 输入Schema | `/input_schema` | GET |
| 输出Schema | `/output_schema` | GET |
| 配置Schema | `/config_schema` | GET |
| Playground | `/playground` | GET |
| 运行追踪 | LangSmith API `/runs` | GET |

## Flowise

| 功能 | 端点 | 方法 |
|---|---|---|
| 对话 | `/api/v1/prediction/{id}` | POST |
| 聊天流列表 | `/api/v1/chatflows` | GET |
| 聊天流详情 | `/api/v1/chatflows/{id}` | GET |
| 凭据列表 | `/api/v1/credentials` | GET |
| 文档存储 | `/api/v1/document-store/loaders` | GET |
| 向量存储 | `/api/v1/vector/upsert/{id}` | POST |

## Coze / 扣子

| 功能 | 端点 | 方法 |
|---|---|---|
| 对话 | `/v3/chat` | POST |
| 消息列表 | `/v3/chat/message/list` | GET |
| Bot信息 | `/v3/bots/{bot_id}` | GET |
| 知识库 | `/v3/datasets` | GET |
| 文档列表 | `/v3/datasets/{id}/documents` | GET |
| 工作流 | `/v3/workflows/runs` | POST |

## 通用检查命令

```bash
# 快速探测目标平台类型
echo "=== FastGPT ===" && curl -s TARGET/api/common/system/getInitData | head -100
echo "=== Dify ===" && curl -s TARGET/v1/parameters -H "Authorization: Bearer API_KEY" | head -100
echo "=== Flowise ===" && curl -s TARGET/api/v1/chatflows | head -100
echo "=== LangServe ===" && curl -s TARGET/input_schema | head -100
```
