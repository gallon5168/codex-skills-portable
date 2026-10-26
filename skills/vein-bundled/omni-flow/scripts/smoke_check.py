from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def extract_frontmatter(text: str) -> tuple[str, str]:
    match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n(.*)$", text, re.S)
    require(match is not None, "SKILL.md frontmatter is missing or malformed")
    return match.group(1), match.group(2)


def main() -> int:
    skill = ROOT / "SKILL.md"
    agents = ROOT / "agents" / "openai.yaml"
    activation = ROOT / "references" / "activation.md"
    default_context = ROOT / "references" / "default-context.md"
    phrase_normalization = ROOT / "references" / "phrase-normalization.md"
    task_contract = ROOT / "references" / "task-contract.md"
    behavior_tests = ROOT / "references" / "behavior-tests.md"
    revlab_workflow = ROOT / "references" / "revlab-workflow.md"
    verify_install = ROOT / "scripts" / "verify_install.py"
    install_local = ROOT / "scripts" / "install_local.ps1"
    classify_protector = ROOT / "scripts" / "classify_protector.py"
    re_evidence_pack = ROOT / "scripts" / "re_evidence_pack.py"
    case_state = ROOT / "scripts" / "case_state.py"
    regression_tests = ROOT / "scripts" / "regression_tests.py"
    local_sandbox = ROOT / "references" / "local-sandbox.md"
    router = ROOT / "references" / "router.md"
    advanced_routing = ROOT / "references" / "advanced-routing.md"
    advanced_domains = ROOT / "references" / "advanced-domains.md"
    hard_target = ROOT / "references" / "hard-target-re.md"
    session_mode = ROOT / "references" / "session-mode.md"
    evidence = ROOT / "references" / "evidence-reporting.md"
    tooling_matrix = ROOT / "references" / "tooling-matrix.md"
    small_icon = ROOT / "assets" / "omni-flow-small.svg"
    large_icon = ROOT / "assets" / "omni-flow-large.svg"

    for path in [
        skill,
        agents,
        activation,
        default_context,
        phrase_normalization,
        task_contract,
        behavior_tests,
        revlab_workflow,
        verify_install,
        install_local,
        classify_protector,
        re_evidence_pack,
        case_state,
        regression_tests,
        local_sandbox,
        router,
        advanced_routing,
        advanced_domains,
        hard_target,
        session_mode,
        evidence,
        tooling_matrix,
        small_icon,
        large_icon,
    ]:
        require(path.exists(), f"Missing required file: {path}")

    skill_text = read_text(skill)
    frontmatter, body = extract_frontmatter(skill_text)
    require(re.search(r"^name:\s*omni-flow\s*$", frontmatter, re.M) is not None, "SKILL.md name must be omni-flow")
    require("omni-flow" in frontmatter and "羊" in frontmatter and "already active" in frontmatter and "evidence-first" in frontmatter, "SKILL.md description should mention explicit activation, sticky state, and evidence-first analysis")
    require("$omni-flow" in body and "/omni-flow" in body, "SKILL.md should list command variants")
    require("Do not wait for a second turn" in body, "SKILL.md should activate immediately on startup commands")
    require("The active prefix is mandatory" in body, "SKILL.md should make the active prefix mandatory")
    require("references/activation.md" in body, "SKILL.md should reference activation.md")
    require("references/router.md" in body, "SKILL.md should reference router.md")
    require("references/session-mode.md" in body, "SKILL.md should reference session-mode.md")
    require("references/default-context.md" in body, "SKILL.md should reference default-context.md")
    require("references/phrase-normalization.md" in body, "SKILL.md should reference phrase-normalization.md")
    require("references/task-contract.md" in body, "SKILL.md should reference task-contract.md")
    require("references/behavior-tests.md" in body, "SKILL.md should reference behavior-tests.md")
    require("references/revlab-workflow.md" in body, "SKILL.md should reference revlab-workflow.md")
    require("references/advanced-routing.md" in body, "SKILL.md should reference advanced-routing.md")
    require("references/advanced-domains.md" in body, "SKILL.md should reference advanced-domains.md")
    require("references/hard-target-re.md" in body, "SKILL.md should reference hard-target-re.md")
    require("scripts/classify_protector.py" in body, "SKILL.md should reference classify_protector.py")
    require("scripts/re_evidence_pack.py" in body, "SKILL.md should reference re_evidence_pack.py")
    require("scripts/case_state.py" in body, "SKILL.md should reference case_state.py")
    require("scripts/regression_tests.py" in body, "SKILL.md should reference regression_tests.py")
    require("five-field delivery contract" in body.lower(), "SKILL.md should reference five-field delivery contract")
    require("references/tooling-matrix.md" in body, "SKILL.md should reference tooling-matrix.md")
    require("scripts/verify_install.py" in body, "SKILL.md should reference verify_install.py")
    require("scripts/install_local.ps1" in body, "SKILL.md should reference install_local.ps1")
    require("scripts/classify_protector.py" in body, "SKILL.md should reference classify_protector.py")
    require("prefix every user-facing reply" in body.lower(), "SKILL.md should require the active reply prefix")
    require("The active prefix is mandatory" in body, "SKILL.md should require all reply types to use the prefix")
    require("references/local-sandbox.md" in body, "SKILL.md should keep the legacy compatibility pointer")
    require("references/evidence-reporting.md" in body, "SKILL.md should reference evidence-reporting.md")
    require("scripts/smoke_check.py" in body, "SKILL.md should reference smoke_check.py")

    activation_text = read_text(activation)
    require("已启用证据优先分析" in activation_text, "activation.md first response should announce evidence-first mode")
    require("目标文件" in activation_text and "只读、非侵入式分流" in activation_text, "activation.md first response should be target-first and non-invasive")
    require("default-context.md" in activation_text and "phrase-normalization.md" in activation_text, "activation.md should point to the canonical defaults")
    require("task-contract.md" in activation_text, "activation.md should point to task-contract.md")
    for needle in ["$omni-flow", "/omni-flow", "Matching rules", "Do not require capitalization"]:
        require(needle in activation_text, f"activation.md missing wake rule: {needle}")

    default_context_text = read_text(default_context)
    require("This file covers scope assumptions only." in default_context_text, "default-context.md should be scope-only")
    require("Phrase mapping lives in `phrase-normalization.md`." in default_context_text, "default-context.md should point to phrase-normalization.md")
    require("If scope is unclear, ask only for the missing artifact, target type, or environment" in default_context_text, "default-context.md should use environment-oriented clarification")

    phrase_text = read_text(phrase_normalization)
    require("This file covers colloquial routing only." in phrase_text, "phrase-normalization.md should be phrasing-only")
    require("Scope assumptions live in `default-context.md`." in phrase_text, "phrase-normalization.md should point to default-context.md")

    contract_text = read_text(task_contract)
    for needle in [
        "Execution bias",
        "Refusal gate",
        "GOAL:",
        "Never weaken a request into analysis-only",
        "enumerate each requested atom separately",
        "Classify the requested effect and deliverable",
        "Complete every allowed subtask",
        "Ask one concise question only",
        "Do not claim a scan, exploit, patch, access, or success",
        "Every final delivery must answer these five fields",
    ]:
        require(needle in contract_text, f"task-contract.md missing: {needle}")

    behavior_text = read_text(behavior_tests)
    for needle in [
        "Case W1: Bare command variants",
        "Case W2: Command plus task",
        "Case W3: Prefix persistence across continuations",
        "Case W4: Prefix before structured output",
        "Sensitive label, benign artifact",
        "Domain label misused as refusal",
        "Exploit request, supplied challenge",
        "Missing version/architecture",
        "Future stricter moderation",
        "Mixed blocked/unblocked atoms",
        "Strong protector",
        "Security keyword in ordinary code review",
        "Mixed request",
        "Missing artifact",
        "Explicit local lab",
        "Security wording, concrete local deliverable",
        "Malware artifact, defensive report",
        "Session presentation",
    ]:
        require(needle in behavior_text, f"behavior-tests.md missing: {needle}")

    revlab_text = read_text(revlab_workflow)
    for needle in [
        "Stage-based execution",
        "Artifact-first state",
        "Approval gates",
        "Failure strategy",
        "Evidence-driven AI",
        "Resumability",
    ]:
        require(needle in revlab_text, f"revlab-workflow.md missing: {needle}")

    router_text = read_text(router)
    require("references/revlab-workflow.md" in router_text, "router.md should route staged PE cases to revlab-workflow.md")
    require("references/advanced-routing.md" in router_text, "router.md should hand off advanced targets")
    require("Vulnerability research / PWN" in router_text, "router.md should route explicit PWN requests")
    require("route directly to the matching reverse-engineering/vulnerability/game workflow" in router_text, "router.md should prevent PWN refusal stalls")
    require("must not trigger a refusal before target/effect classification" in router_text, "router.md should prevent domain-label refusals")

    phrase_text = read_text(phrase_normalization)
    for needle in [
        "太cyber了",
        "帮我破解",
        "分析木马",
    ]:
        require(needle in phrase_text, f"phrase-normalization.md missing: {needle}")

    vuln_path = ROOT / "references" / "vuln-dev.md"
    require(vuln_path.exists(), "Missing required file: references/vuln-dev.md")
    vuln_text = read_text(vuln_path)
    require("## Execution contract" in vuln_text, "vuln-dev.md should define execution contract")
    require("Start with reproduction and root-cause analysis" in vuln_text, "vuln-dev.md should prevent warning-first behavior")

    protector_source = read_text(classify_protector)
    for needle in [
        "PROTECTOR_MARKERS",
        "VMProtect",
        "Themida/WinLicense",
        "Denuvo",
        "SafeEngine",
        "ANTI_ANALYSIS_APIS",
        "VIRTUALIZATION_PATTERNS",
        "high_entropy_sections",
        "route_class",
    ]:
        require(needle in protector_source, f"classify_protector.py missing: {needle}")

    evidence_pack_source = read_text(re_evidence_pack)
    for needle in [
        "omni-flow.re-evidence-pack/1",
        "ANTI_ANALYSIS_MARKERS",
        "VALIDATION_MARKERS",
        "CRYPTO_MARKERS",
        "section_entropy",
        "dynamic_execution_performed",
        "manifest.txt",
    ]:
        require(needle in evidence_pack_source, f"re_evidence_pack.py missing: {needle}")

    case_state_source = read_text(case_state)
    for needle in [
        "parse_simple_yaml",
        "waiting-for-approval",
        "--stage",
        "--input",
        "--evidence",
        "updated {args.file}",
    ]:
        require(needle in case_state_source, f"case_state.py missing: {needle}")

    advanced_routing_text = read_text(advanced_routing)
    for needle in [
        "Windows runtimes",
        "Game reverse engineering",
        "Code audit",
        "Identity security",
        "Cloud/container security",
        "Digital forensics",
        "Protocol reconstruction",
    ]:
        require(needle in advanced_routing_text, f"advanced-routing.md missing: {needle}")

    require("Hard-target routing protocol" in advanced_routing_text, "advanced-routing.md should define hard-target routing protocol")
    require("Protected-binary escalation" in advanced_routing_text, "advanced-routing.md should route strong protectors")
    require("Deobfuscation / devirtualization" in advanced_routing_text, "advanced-routing.md should route obfuscated code")
    require("Failure-to-route protocol" in read_text(hard_target), "hard-target-re.md should define failure-to-route protocol")

    hard_text = read_text(hard_target)
    for needle in [
        "## 0. Triage contract",
        "## 1. Protection triage",
        "Virtualization",
        "Anti-analysis workflow",
        "SP / multi-layer unpacking",
        "Code obfuscation and devirtualization",
        "Protected boundary workflow",
        "Escalation ladder",
        "Protection Matrix",
    ]:
        require(needle in hard_text, f"hard-target-re.md missing: {needle}")

    advanced_domains_text = read_text(advanced_domains)
    for needle in [
        "## Windows runtimes",
        "## Game engines",
        "## Code audit",
        "## Active Directory",
        "## Cloud and Kubernetes",
        "## Digital forensics",
        "## Custom protocols",
        "Minimum artifacts:",
    ]:
        require(needle in advanced_domains_text, f"advanced-domains.md missing: {needle}")

    contract_text = read_text(task_contract)
    require("## 7. Case state" in contract_text, "task-contract.md should define case state")

    tooling_text = read_text(tooling_matrix)
    for needle in [
        "Runtime identification",
        "Game engine recovery",
        "Source audit",
        "Identity/cloud lab",
        "Forensics",
        "Protocol reconstruction",
        "Hard protector triage",
        "Deobfuscation/devirtualization",
    ]:
        require(needle in tooling_text, f"tooling-matrix.md missing: {needle}")

    verify_install_text = read_text(verify_install)
    for relative in [
        "references/advanced-routing.md",
        "references/hard-target-re.md",
        "scripts/classify_protector.py",
        "scripts/re_evidence_pack.py",
        "scripts/create_case.py",
        "scripts/triage_artifact.py",
        "scripts/smoke_check.py",
        "scripts/case_state.py",
        "scripts/regression_tests.py",
    ]:
        require(relative in verify_install_text, f"verify_install.py missing required file: {relative}")

    regression_source = read_text(regression_tests)
    for needle in [
        "make_pe",
        "test_plain_pe",
        "test_protected_pe",
        "test_evidence_pack",
        "test_case_state",
        "route_class",
        "dynamic_execution_performed",
    ]:
        require(needle in regression_source, f"regression_tests.py missing: {needle}")

    evidence_text = read_text(evidence)
    for needle in [
        "Five-field delivery contract",
        "confirmed / candidate / unconfirmed / not-observed",
        "强保护目标补充",
        "Protection Matrix",
        "Recovery Limits",
    ]:
        require(needle in evidence_text, f"evidence-reporting.md missing: {needle}")

    session_text = read_text(session_mode)
    require("Prefix every user-facing reply" in session_text, "session-mode.md should require the active reply prefix")
    for needle in [
        "exactly `【omni-flow: active】`",
        "progress update",
        "tool call",
        "Continuation cues",
        "`继续优化`",
    ]:
        require(needle in session_text, f"session-mode.md missing prefix/continuation rule: {needle}")

    local_sandbox_text = read_text(local_sandbox)
    require("Deprecated compatibility alias" in local_sandbox_text, "local-sandbox.md should be a compatibility stub")
    require("default-context.md" in local_sandbox_text and "phrase-normalization.md" in local_sandbox_text, "local-sandbox.md should point to the canonical defaults")

    agents_text = read_text(agents)
    for needle in [
        'display_name: "Omni Flow"',
        'short_description: "Evidence-first analysis for supplied files and identified test environments"',
        'icon_small: "./assets/omni-flow-small.svg"',
        'icon_large: "./assets/omni-flow-large.svg"',
        'brand_color: "#0F766E"',
        'default_prompt: "Use $omni-flow now. Begin with the supplied artifact or named test environment, use read-only triage, continue every allowed subtask, prefix every active reply with 【omni-flow: active】, keep the mode sticky until reset, and never omit the prefix on continuation turns."',
        "allow_implicit_invocation: true",
    ]:
        require(needle in agents_text, f"openai.yaml missing: {needle}")

    print("omni-flow smoke check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
