# REVLab-Inspired Workflow - 可验证逆向流水线

This reference distills reusable workflow patterns observed in the local REVLab project. It is a design reference, not an instruction to copy its implementation or to bypass higher-priority policy.

## What is worth adopting

- Stage-based execution: separate intake, identification, unpacking, disassembly, decompilation, dynamic observation, network evidence, and reporting.
- Artifact-first state: every stage publishes named outputs, hashes, timestamps, tool versions, and an evidence summary. Downstream stages consume the verified artifact selected by the previous stage.
- Explicit status: use pending, running, completed, failed, skipped, waiting-for-approval, and retry-waiting. Never turn a missing tool or unobserved runtime fact into a confident conclusion.
- Approval gates: pause before execution, memory dumping, active network tests, or any other consequential side effect. Record the decision and reason in the case log.
- Failure strategy: choose abort, skip, or bounded retry per stage. Preserve the partial run and state exactly where it stopped.
- Portable run layout: keep one run directory with a manifest, input copy, static evidence, dynamic evidence, captures, derived artifacts, and reports.
- Evidence-driven AI: give the model a bounded evidence package; require conclusions to cite evidence and mark confirmed, candidate, unconfirmed, or not observed. Store AI output as a report artifact, never as a replacement for raw evidence.
- Resumability: allow a completed stage to be reused, a failed stage to be retried, and a single node to be rerun without silently changing earlier outputs.

## Recommended case state

case:
  id: case-YYYYMMDD-HHMMSS
  input:
    path: /absolute/path/to/copy
    sha256: observed-value
    size: observed-value
  environment:
    mode: offline | local-lab | named-staging | unknown
    network: disabled | captured | enabled-with-approval
    sandbox: none | vm-snapshot | local-isolated
  stages:
    - id: identify
      status: completed
      outputs: [pe.json, hashes.json]
      evidence: [pe-header, section-table]
    - id: dynamic
      status: waiting-for-approval
      requires: [named-environment, approval]
  claims:
    - text: "..."
      state: confirmed | candidate | unconfirmed | not-observed
      evidence: [artifact-id]

## Stage contract

Each stage should declare:

1. Inputs and required previous outputs.
2. Read-only versus side-effecting behavior.
3. Expected output files and a machine-readable summary.
4. Evidence IDs and hashes.
5. Failure behavior and retry limit.
6. Whether an approval gate is required.

Use this order for a PE case unless the artifact or user goal calls for a narrower route:

1. Intake and immutable copy.
2. File type, architecture, signature, hashes, and metadata.
3. Section/import/export/resource/TLS and entropy analysis.
4. Packer or protector detection; record confidence and signals.
5. Optional unpacking on a copy; verify the resulting file before downstream analysis.
6. Disassembly and cross-reference extraction.
7. Optional decompilation when the tool is available.
8. Dynamic observation only in a named isolated environment and after approval.
9. Network capture only when explicitly part of the identified environment; store the capture and parser summary.
10. Aggregate report with evidence links, limitations, and next actions.

## AI handoff contract

Give an AI analysis node only the minimum relevant evidence package. Require JSON or a clearly structured result with:

- summary
- findings, each with severity, state, evidence IDs, and confidence
- unknowns and missing inputs
- recommended next diagnostic step
- no claim of execution, access, or exploitation unless an observed artifact proves it

If the AI provider is unavailable, retain a deterministic evidence summary and mark the AI stage as waiting or skipped; do not fail the entire case.

## Why this improves omni-flow

This pattern makes the skill more capable without making it more trigger-happy: it gives the model a concrete way to progress from static inspection to deeper analysis, preserve partial results, ask only for a blocking fact, and keep raw evidence separate from interpretation.
