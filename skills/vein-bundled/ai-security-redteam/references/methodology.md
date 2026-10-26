# AI Security Methodology (2026)

Original research and operational methodology. Aligned with OWASP LLM 2025 + OWASP ASI 2026 + MITRE ATLAS + NIST AI RMF. 信益安信息安全研究院出品。

## 1. Target Reconstruction

Build an assumption register from incomplete information:

| Known Fact | Source | Confidence | Validation Method |
|---|---|---|---|
| Frontend framework | JS/headers | High | Source map check |
| Backend platform | API responses | Medium | Init endpoint |
| RAG pipeline | Citations in output | Medium | detail:true |
| Tool capabilities | Model responses | Low | Verify with action |

Typical inputs: scope doc, DNS/TLS, frontend JS, API routes, OpenAPI, share links, job postings, repos, error messages, model responses, CORS/CSP headers.

## 2. AI Stack Model (Top→Bottom)

```
1. User Interface: web, iframe, mobile, widget, extension
2. API Gateway: auth, rate limit, tenant routing, logging
3. Orchestration: FastGPT / Dify / Flowise / LangChain / LlamaIndex / custom
4. Context Builder: system prompt + developer prompt + user input + memory + RAG + tool outputs
5. Model/Inference: provider API / vLLM / TGI / Ollama / self-hosted
6. RAG Pipeline: embedding model → vector DB → re-ranker → chunk → metadata → ACL
7. Tools: HTTP / database / file / Git / Slack / email / code execution / cloud APIs
8. Storage: chat history / uploads / knowledge base / raw source / object store
9. Infrastructure: cloud IAM / K8s / service mesh / queues / CI/CD / model registry
```

## 3. Trust Boundary Model

| Trust Level | Content Type | Treatment |
|---|---|---|
| Trusted policy | System/developer instructions | Authoritative |
| Semi-trusted state | Variables, workflow outputs, server metadata | Verify before acting |
| User input | Chat text, form fields, uploads | Never trust as instruction |
| External data | Web pages, emails, tickets, PRs, docs | Untrusted data |
| Tool output | API responses, search results | Data, not instruction |
| RAG content | Retrieved documents, citations | Data, not instruction |

**Core vulnerability pattern:** untrusted data treated as trusted instruction, OR model acts with privileges broader than the user.

## 4. Test Cycle

For each attack surface:
1. Enumerate capability
2. Establish safe baseline
3. Inject canary or benign instruction
4. Observe model + server behavior
5. Check downstream sink: retrieval, tool, file, API, rendering, log, callback
6. Repeat in clean session (run-twice rule)
7. Reduce to minimal proof
8. Write root cause and fix at correct layer

## 5. Impact Classification

**Valid impact:**
- Low-privilege user reads protected RAG source
- Public share link exposes raw citations
- Model calls tool the current user shouldn't control
- Uploaded document changes other users' answers
- Rendered answer executes script or makes external request with sensitive context
- Workflow fetches internal URLs or cloud metadata
- Model service leaks API keys, config, internal endpoints
- Vector store reveals sensitive text or cross-tenant data

**NOT impact:**
- Model says it's admin but no privileged action happens
- Model invents a fake system prompt (confabulation)
- Model gives generic unsafe advice without target-specific data
- Single non-reproducible response
- Refusal bypass that doesn't reach private data or action

## 6. Novel Attack Classes Discovered

### Semantic Framing Injection
Disguise extraction as legitimate business tasks (PRD, translation, cloning, code generation, self-check). Bypasses RAG input rewriting because rewriting modules cannot distinguish "business discussion about rules" from "extraction attack."

### Recursive Self-Reference (Quine Attack)
Ask model to describe "how to answer when asked about rules" → outputs actual rules as "example responses."

### detail:true / SSE Reasoning Leak
API parameters expose chain-of-thought that references internal rules verbatim, even when direct extraction is blocked.

## 7. Reporting Discipline

Every finding includes:
- Role and account used
- Exact feature and endpoint
- Trust boundary crossed
- Minimal request/response or UI steps
- Canary/test data proof
- Business impact
- Correct fix layer (prompt policy / RAG ACL / API auth / tool permission / rendering / infra)
- Regression test suggestion
