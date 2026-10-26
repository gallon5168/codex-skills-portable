# AI Security Skill Routing

This project is designed as a skill family. Use `ai-security-dispatch` first when the scenario is unclear.

## Skill Family

- `ai-security-dispatch`: scenario classifier and router.
- `ai-security-redteam`: full-scope AI target assessment, planning, and reporting.
- `ai-security-prompt`: prompt/context isolation and prompt injection.
- `ai-security-rag`: RAG, knowledge base, citations, vector stores, ingestion.
- `ai-security-agent-mcp`: agents, workflows, tools, MCP, multi-agent/A2A.
- `ai-security-infra-supplychain`: infrastructure, model deployment, supply chain.

## Scenario Matrix

| Scenario | Load first | Then load | Why |
|---|---|---|---|
| User says "AI security test this target" | `ai-security-dispatch` | `ai-security-redteam` | Need classification before specifics |
| Chat page only, no visible docs/tools | `ai-security-prompt` | `hunt-llm-ai`, `hunt-session` | Prompt/context and session isolation |
| Public share chatbot | `ai-security-prompt` | `hunt-idor`, `hunt-xss`, `hunt-cors` | Share IDs, rendered output, browser boundary |
| FastGPT/Dify/Flowise style app | `ai-security-redteam` | `ai-security-rag`, `ai-security-agent-mcp`, `hunt-idor` | These apps often mix RAG, workflows, share links |
| Citations/source references visible | `ai-security-rag` | `hunt-idor`, `hunt-source-leak` | Raw-source and quote boundaries |
| File upload into chat | `ai-security-rag` | `hunt-file-upload`, `ai-security-prompt`, `hunt-xss` | Upload may become RAG/indirect injection/rendering |
| Website sync/import URL | `ai-security-rag` | `hunt-ssrf`, `hunt-open-redirect` | Server-side URL fetch and ingestion |
| Tool call traces or workflow nodes | `ai-security-agent-mcp` | `hunt-business-logic`, `hunt-idor` | Tool side effects and authorization |
| HTTP request/fetch/browse tool | `ai-security-agent-mcp` | `hunt-ssrf` | Server-side request capability |
| Code execution node/notebook | `ai-security-agent-mcp` | `hunt-rce`, `ai-security-infra-supplychain` | Sandbox and runtime impact |
| MCP mentioned or configured | `ai-security-agent-mcp` | `hunt-source-leak`, `cloud-iam-deep` | Tool scope, secrets, remote MCP isolation |
| Multi-agent/A2A | `ai-security-agent-mcp` | `hunt-business-logic`, `supply-chain-attack-recon` | Identity, task integrity, rogue agents |
| Vector DB or embeddings | `ai-security-rag` | `ai-security-infra-supplychain` | App-layer retrieval plus deployment exposure |
| vLLM/Ollama/TGI/OpenAI-compatible endpoint | `ai-security-infra-supplychain` | `hunt-api-misconfig`, `hunt-rce` | Model hosting/API risk |
| Cloud creds or metadata path | `ai-security-infra-supplychain` | `cloud-iam-deep`, `hunt-ssrf` | Cloud blast radius |
| K8s/service mesh/GPU nodes | `ai-security-infra-supplychain` | `hunt-k8s`, `cloud-iam-deep` | Deployment compromise path |
| Model/dataset/plugin artifact review | `ai-security-infra-supplychain` | `supply-chain-attack-recon`, `hunt-cicd` | Supply-chain integrity |

## Avoiding Overlap

- Do not use `ai-security-prompt` to report RAG ACL bugs. Use it only to craft the injection and `ai-security-rag` to prove the data boundary.
- Do not use `ai-security-rag` to claim SSRF from website sync without OOB proof. Pair with `hunt-ssrf`.
- Do not use `ai-security-agent-mcp` to analyze cloud credentials after discovery. Pair with `cloud-iam-deep`.
- Do not use `ai-security-infra-supplychain` for ordinary chatbot jailbreak claims. Pair with `ai-security-prompt` only if there is no infrastructure angle.

## Recommended Load Sets

### Minimal Chatbot

```text
ai-security-dispatch
ai-security-prompt
hunt-llm-ai
hunt-session
hunt-api-misconfig
```

### Public RAG Chatbot

```text
ai-security-dispatch
ai-security-redteam
ai-security-prompt
ai-security-rag
hunt-idor
hunt-xss
hunt-file-upload
hunt-source-leak
```

### Agentic Workflow App

```text
ai-security-dispatch
ai-security-redteam
ai-security-prompt
ai-security-agent-mcp
hunt-idor
hunt-ssrf
hunt-business-logic
hunt-rce
```

### AI Platform / Admin Scope

```text
ai-security-dispatch
ai-security-redteam
ai-security-rag
ai-security-agent-mcp
ai-security-infra-supplychain
hunt-nextjs
hunt-source-leak
cloud-iam-deep
hunt-k8s
hunt-cicd
supply-chain-attack-recon
```

