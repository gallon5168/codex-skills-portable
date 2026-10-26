# Changelog / 更新日志

## v1.0.0 (2026-06-16)

### 首个公开版本

**核心技能族（7个技能）**
- `ai-security-dispatch` — 场景分类器和技能路由器
- `ai-security-redteam` — 总指挥（规划、执行、报告、自动化脚本）
- `ai-security-prompt` — 提示词注入专家（6大攻击类别 + 载荷库 + 检查清单）
- `ai-security-rag` — RAG管线专家（枚举 + ACL + 投毒 + 多平台API参考）
- `ai-security-agent-mcp` — Agent/MCP专家（工具权限 + SSRF + 攻击模式）
- `ai-security-infra-supplychain` — 基础设施专家（指纹识别 + 供应链 + 检查清单）
- `ai-redteam` — 红队入口别名

**自动化测试脚本（3个）**
- `auto-baseline.sh` — 全自动基线安全扫描（6阶段 + JSON报告）
- `prompt-test-runner.py` — 提示词注入自动测试（8类载荷 + 双次验证 + 泄露评分）
- `rag-enumerator.py` — RAG知识库自动枚举（detail:true + 引用分析）

**参考文档（7个）**
- methodology.md — 测试方法论（含原创攻击类别）
- attack-surfaces.md — 9大攻击面 + OWASP/MITRE映射
- test-cases.md — 13类测试用例 + 验证协议
- risk-taxonomy.md — 风险分类 + 严重度指南 + 修复映射
- tools.md — 2026最新工具参考（12+工具）
- platform-specific.md — 7大平台差异化测试指南
- skill-routing.md — 完整技能路由矩阵

**检查清单（7个）**
- 对话Web AI / RAG-Agent-MCP / 基础设施-供应链（总览级）
- 提示词注入 / RAG测试 / Agent-MCP测试 / 基础设施测试（专家级）

**模板（2个）**
- finding-report.md — 发现报告模板
- test-plan.md — 测试计划模板

**技术亮点**
- 原创攻击技术：语义框架注入（10变体）、递归自引用Quine攻击、detail:true推理泄露
- 对齐标准：OWASP LLM 2025 + OWASP ASI 2026 + MITRE ATLAS + NIST AI RMF
- 2026最新工具：Promptfoo/Garak/PyRIT/AgentAuditKit/AgentsID Scanner/AI-Infra-Guard等
- 多平台覆盖：FastGPT/Dify/Flowise/Coze/MaxKB/AnythingLLM/Langflow
- 中英双语检查清单
- 自包含无外部依赖
