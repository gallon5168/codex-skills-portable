# AI Attack Surfaces (2026)

## A. Conversational Web Surface

- Chat completion API, share link init, chat history CRUD
- Feedback/rating, export (Markdown/PDF/HTML)
- Streaming events, intermediate traces, reasoning tokens
- Frontend-rendered Markdown, HTML, LaTeX, Mermaid, images, links, iframes
- Session IDs, app IDs, share IDs, outLink user IDs, tenant IDs

Risks: IDOR across histories, system/config leakage, weak rate limit, unsafe output rendering, external tracking, missing frame/CSP policy

## B. Prompt and Context Surface

- System prompt, developer prompt, user prompt
- Conversation history, memory, variables
- RAG quotes, tool results, error messages
- Hidden workflow node outputs

Risks: Direct/indirect injection, role confusion, system prompt leakage, cross-session poisoning, tool-result injection, context-window stuffing, semantic framing bypass, quine attack

## C. RAG Surface

- Dataset list/metadata, collection/source IDs, raw source previews
- Quote retrieval, export endpoints, chunking strategy
- Similarity threshold, re-ranking, query expansion
- ACL filtering, external website sync, API datasets, file libraries

Risks: Knowledge-base enumeration, protected source leakage, cross-tenant retrieval, ingestion poisoning, retrieval hijacking, stale sensitive content, embedding/vector leakage

## D. File, Image, and Audio Surface

- File/image upload, OCR, audio transcription
- Attachment rendering, object storage URLs
- File preview, dataset import

Risks: Indirect injection via document, unsafe file type handling, stored XSS through preview, public object storage, transcription injection

## E. Agent, Workflow, and Tool Surface

- Tool schemas/names/params, HTTP request nodes
- Database/file/Git/email/Slack/code execution nodes
- Conditional branches, variable update, loop, human approval nodes

Risks: Tool over-permission, parameter injection, SSRF via internal fetch, unauthorized writes, cross-tool correlation, tool-output injection, loop exhaustion, audit gaps

## F. MCP Surface

- Local stdio / remote HTTP+SSE / shared multi-user MCP
- Tool descriptions, JSON schemas, filesystem/git/database scopes
- Connected notes/secrets/tools

Risks: Tool schema extraction, secrets via file paths, git history secret recovery, remote MCP cross-user leakage, tool description poisoning, permission mismatch

## G. Multi-Agent / A2A Surface

- Agent identity/cards, capability discovery, task delegation
- Message queue, shared memory, result aggregation, registration

Risks: Rogue agent registration, impersonation, agent-card hijack, task injection, shared queue poisoning, cross-agent privilege escalation

## H. Supply Chain Surface

- Model/dataset repositories, LoRA/adapters, MCP servers/plugins
- Python/Node dependencies, serialized model formats, CI/CD jobs

Risks: Malicious artifacts, dataset poisoning, dependency confusion, namespace takeover, unsafe deserialization, backdoored MCP/plugin

## I. Infrastructure Surface

- Inference endpoints (OpenAI-compatible, vLLM, TGI, Ollama)
- Vector DB, object storage, Kubernetes, service mesh
- Notebooks, GPU nodes, model registry, logs/traces, admin panels

Risks: Public admin APIs, weak IAM, exposed vector DB, source maps/JS secrets, public buckets, container escape, inference abuse, cost exhaustion

## Standards Mapping

| Surface | OWASP LLM 2025 | OWASP ASI 2026 | MITRE ATLAS |
|---|---|---|---|
| A (Web) | LLM02 | ASI09 | — |
| B (Prompt) | LLM01, LLM07 | ASI01 | AML.T0051 |
| C (RAG) | LLM08, LLM06 | ASI06 | AML.T0049 |
| D (File) | LLM01 | ASI01 | AML.T0051 |
| E (Agent) | LLM09, LLM02 | ASI02, ASI05 | AML.T0040 |
| F (MCP) | — | ASI04 | — |
| G (Multi-Agent) | — | ASI07, ASI08 | — |
| H (Supply Chain) | LLM05 | ASI04 | AML.T0018 |
| I (Infra) | LLM05 | ASI10 | AML.T0035 |
