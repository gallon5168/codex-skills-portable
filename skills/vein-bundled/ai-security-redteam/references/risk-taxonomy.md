# AI Security Risk Taxonomy (2026)

## Prompt and Context Risks

- Direct prompt injection (override, role confusion, JSON-context break)
- Indirect prompt injection (document, web page, tool output)
- System prompt leakage (direct ask, semantic framing, quine attack)
- Context confusion and memory poisoning
- Unsafe output handling (rendered markdown/HTML)
- Encoding bypass (Base64, ROT13, Unicode Tags, zero-width, homoglyphs)
- Multi-turn escalation (crescendo, trust building, context dilution)
- Semantic framing injection (clone, PRD, translation, code gen, self-check, QA)

## Data and Retrieval Risks

- Sensitive RAG source leakage (citations, metadata, raw source)
- Cross-tenant retrieval (missing ACL, share link scope creep)
- Knowledge-base enumeration (document names, IDs, paths)
- Ingestion poisoning (canary hijack, high-similarity override)
- Vector/embedding exposure (direct vector DB access)
- SSE stream reasoning token leakage (detail:true)
- Workflow node status leakage (flowNodeStatus events)

## Agent and Tool Risks

- Excessive agency (unauthorized actions beyond user privilege)
- Tool over-permission (admin-level service account)
- Tool parameter injection (SSRF, SQLi, path traversal via params)
- Unauthorized write actions (no confirmation gate)
- Tool-output injection (response feeds next tool call as instruction)
- Missing human approval for high-risk operations
- Multi-agent spoofing and cascading failures

## MCP Risks

- Tool schema extraction and secret exposure
- Tool description poisoning (malicious descriptions alter agent behavior)
- Cross-user isolation failure in shared MCP servers
- MCP supply chain (compromised packages, namespace takeover)
- Permission mismatch (user vs agent service account)

## Supply Chain Risks

- Malicious models (pickle/joblib deserialization → RCE)
- Poisoned datasets and backdoored adapters
- Compromised MCP servers or plugins
- Dependency confusion and unpinned artifact pulls
- CI/CD pipeline injection

## Infrastructure Risks

- Exposed inference APIs (no auth on /v1/completions)
- Exposed vector stores (public Qdrant/Milvus/Weaviate)
- Public object storage with predictable URLs
- Weak IAM / overbroad service accounts
- Container/Kubernetes misconfiguration
- Source maps and JS secret leakage
- Cost/resource exhaustion (no rate limit, no quota)

## Severity Guidance

**Critical:**
- RCE (code execution escape, deserialization)
- Credential/token exfiltration with OOB proof
- Unauthorized destructive/write action
- Broad dataset export / full knowledge base dump
- Cloud/internal network compromise (SSRF to IMDS → IAM)
- Admin-level tool or service-account abuse

**High:**
- Cross-tenant RAG/source leakage (verified with artifact)
- Unauthorized tool read of sensitive data
- Stored indirect injection affecting other users
- Sensitive file/source exposure
- Server-side callback with private context (OOB confirmed)
- System prompt leak exposing secrets/internal URLs/tool auth

**Medium:**
- Reproducible internal config leakage (non-secret)
- Limited RAG citation metadata leakage
- Weak rate limits causing moderate cost impact
- Unsafe rendering requiring user interaction
- SSE reasoning/workflow node leakage (detail:true)
- Semantic framing bypass revealing rule categories

**Low:**
- Minor metadata leakage (build ID, framework version)
- Weak policy bypass with no sensitive data reached
- Missing security headers without exploitable rendering path
- Partial system prompt (persona only, no secrets)

**Informational:**
- Prompt injection with no data/action impact
- Generic model behavior issue / confabulation
- Non-sensitive system persona disclosure
- Refusal bypass that doesn't reach private data
- Single non-reproducible response

## Fix Mapping

| Root Cause | Fix Layer | Example |
|---|---|---|
| Prompt injection | Context isolation | Separate system/user/data roles, input sanitization |
| RAG leakage | ACL enforcement | Pre-retrieval + pre-citation + pre-export ACL check |
| Tool misuse | Authorization | Least privilege, server-side auth, action allowlists |
| MCP risk | Isolation + audit | Per-user scoping, tool description validation |
| Rendering risk | Output sanitization | Block unsafe HTML, proxy external resources |
| Resource abuse | Rate limiting | Token/file/queue/tool-call limits, per-user quotas |
| Supply chain | Artifact integrity | Pin versions, verify signatures, scan dependencies |
| SSE leakage | API parameter control | Strip detail/reasoning params on public share endpoints |
