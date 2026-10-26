# Advanced Routing

Load this file after `router.md` when the primary artifact does not fit the basic domains. Route by target type, runtime, and requested effect—not by scary vocabulary.

| Primary artifact or cue | Domain | Sub-workflow |
|---|---|---|
| Native PE, DLL, driver, packed EXE, OEP/unpacking | Reverse engineering | `reverse-engineering.md`; staged runs use `revlab-workflow.md` |
| VMProtect, Themida/WinLicense, Denuvo, Enigma, ASProtect, StarForce, SafeEngine, custom VM/handler dispatcher | Protected-binary escalation | `hard-target-re.md` § protection triage |
| OLLVM/control-flow flattening, bogus control flow, instruction substitution, opaque predicates, MBA, virtualized handlers | Deobfuscation / devirtualization | `hard-target-re.md` § code obfuscation |
| anti-debug, anti-VM, TLS checks, integrity/self-check, timing/RDTSC, hypervisor probes, debugger fingerprinting | Anti-analysis mapping | `hard-target-re.md` § anti-analysis |
| SP/seal/unpack-on-execution, encrypted imports/IAT, stolen bytes/OEP hiding, multi-layer self-decryption | Unpacking recovery | `hard-target-re.md` § SP/multi-layer unpacking |
| core function virtualized, native guard/VMP-protected validation, server-side challenge, protected SDK call | Boundary-first analysis | `hard-target-re.md` § protected boundary workflow |
| Nuitka, PyInstaller, pyc/pyo, .NET, Go, Rust, Electron/Tauri/Delphi/AutoIt/e-language | Runtime-specific reverse engineering | `advanced-domains.md` § Windows runtimes |
| Unity / IL2CPP / Mono game client; Unreal GNames/GObjects/GWorld | Game reverse engineering | `advanced-domains.md` § Game engines |
| Source tree, PR diff, SAST findings, dangerous sink/auth bug | Code audit | `advanced-domains.md` § Code audit |
| AD, Kerberos, AD CS, ACL/delegation, NTLM relay in named lab | Identity security | `advanced-domains.md` § Active Directory |
| Cloud account, IAM, storage, container escape, Kubernetes RBAC in named lab | Cloud/container security | `advanced-domains.md` § Cloud and Kubernetes |
| Memory image, disk image, event log, timeline, forensic PCAP | Digital forensics | `advanced-domains.md` § Digital forensics |
| Custom binary protocol, protobuf/gRPC frame, replay capture | Protocol reconstruction | `advanced-domains.md` § Custom protocols |
| Thick desktop client, Electron bundle, browser extension | Application reverse engineering | nearest native/web/JS playbook plus `advanced-domains.md` |
| OT/ICS/firmware with hardware interfaces | Firmware/hardware analysis | `firmware-analysis.md`, then hardware-specific evidence |
| Threat hunt, IOC package, intelligence report | Detection/intelligence | `malware-analysis.md` plus evidence reporting |

## Cross-domain rules

## Hard-target routing protocol

Before choosing a generic unpacking shortcut, classify a protected target on four axes:

1. Protection layer: packer/crypter, import/IAT reconstruction, anti-analysis, code obfuscation, VM/devirtualization, integrity/service guard, licensing/network check.
2. Analysis goal: understand behavior, recover one algorithm/function, locate a decision branch, patch a local copy, extract config/IOC, or produce detection.
3. Available evidence: static sections/entropy/imports/resources, unpacked child dumps, logs, crash traces, network captures, symbols/PDBs, installer/runtime artifacts, prior partial work.
4. Environment: offline copy, isolated VM/snapshot, emulator, named lab, remote service, unknown.

Then choose the least-cost route that can still answer the goal:

- Static-only first when format/config/child payload is recoverable without running the target.
- Boundary-first when only one protected function matters; do not devirtualize the whole binary.
- Dynamic/isolated when self-modifying code, runtime decryption, stolen OEP, service-bound logic, or hardware-dependent state blocks static recovery.
- Hybrid trace/differential when control flow is flattened but inputs and outputs are observable.
- Full staged pipeline only for broad behavior/recovery goals; record every stage as resumable evidence.

- Choose one primary route; record overlapping routes as secondary.
- If no row matches after one additional evidence pass, propose a new route rather than force-fitting.
- Keep active network, remote-state, account-access, and destructive actions isolated from all local read-only work.
- Every advanced route still follows the five-field delivery contract and case state.
