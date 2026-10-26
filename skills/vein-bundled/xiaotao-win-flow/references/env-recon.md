# Environment Three-Check (P0 admission filter) -- mandatory during recon, conclusions kill routes directly

> **Purpose**: during Stage 0/1 recon, before picking a bypass route, run three checks. Their conclusions feed Stage 2.5's route scoring as an **admission filter** -- insufficient-capability or structurally-blocked routes never enter the scoring table, instead of being found dead only after stepping into them.
> **Origin**: distilled from a real post-mortem (an EPL authorization analysis) as a P0 gap. The skill used to implicitly assume an ideal target (proxyable traffic, classic MSVC, memory-writable tools, a single auth gate) and only patched after hitting real diversity -- this reference moves the check upfront.

---

## I. Transport-layer protocol recon (don't default to HTTP or to proxying)

**Root cause**: both the proxy-capture route (Reqable) and the fake-server route assume traffic can be intercepted by the system proxy. Real software commonly uses custom binary TCP / raw sockets bypassing the proxy / TLS pinning / a framework's own network stack -- any one kills the proxy route, and early effort can sink into a route doomed from the start.

> **Stage-1 pre-judgment (moved upfront, Rule 28)**: the *cheap half* of this transport recon now runs at **Stage 1 scan time**, not after an empty capture. `scripts/scan.ps1` step [4] scans the target's own-directory network DLLs (`sscronet`=Cronet / `libssl`=OpenSSL / `Qt*Network` / BoringSSL) and the diec Go-runtime marks, and predicts proxy-capture viability in ~30s *before anyone walks a login*. A self-contained stack (Cronet / static BoringSSL / Go `net`) scores "system-proxy capture" **dead right there** -- feeding Rule 28's control-ownership fork toward in-process Hook instead of a wasted proxy round. This is the fix for the old "capture empty -> then diagnose why" detour: for a local injectable rich client you predict the miss statically, you don't discover it after the user's round-trip.
> **Fast-path note (what still comes after capture)**: the *deeper* transport recon here (live breakpoint on the network API layer, TLS-layer MITM verification) remains the **heavy-route / capture-came-back-empty** discipline. If you *did* run capture (process out of reach, or standard-stack target) and it came back empty, run this transport recon to explain why (loopback / raw socket / pinning / ignores-proxy) and recover per the I-Addendum table. What changed: the DLL/runtime pre-judgment no longer waits for an empty round -- only the runtime-confirmation half does.
>
> **Scope of the Stage-1 pre-judgment (honest limits)**: `scan.ps1` step [4] reads only **own-directory DLL filenames + Go marks**, NOT the PE import table (diec can't dump imports -- that's downstream IDA imports / x64dbg / dumpbin). It also **skips the same-dir scan entirely for targets in System32/Windows** (shared dirs -> attribution unreliable, Rule 12). So a static-BoringSSL-linked or raw-`ws2_32` target with no tell-tale sidecar DLL won't show here -- confirm the network API layer via the import-table/breakpoint step below when the pre-judgment is silent.

**Approach**: before capturing packets, determine transport type first:
1. **Check the import table + breakpoint to see which network API layer is used**:
   - `ws2_32.send`/`WSASend`/`recv` hit directly = raw socket, likely bypasses the proxy (common with custom binary protocols, e.g. an EMSG-style magic number).
   - `wininet`/`winhttp` = likely proxied (WinHTTP only if explicitly configured).
   - `schannel`/`SSPI` = TLS, possibly with its own cert validation/pinning.
2. **Determine protocol shape**: HTTP? TLS? Custom binary? Proxied or not?
3. **Loopback is its own category**: target sends to `127.0.0.1`/`localhost` (a local auth sub-engine) -> neither system proxy nor Reqable catches this; rule out the proxy route immediately, switch to a local technique.
4. **Thin clients, multiple network stacks**: one app can send part of its traffic via webview2/CEF and another via the main process (python-requests / a built-in HTTP lib) -- proxying is a separate question per stack; confirm each by originating process/UA.

**Feeds Stage 2.5**: non-proxied / pinned / custom-binary transport -> downscore or exclude "fake the server" outright.

### I-WebView: WebView/CEF app -> CDP is the default observe+rewrite channel (first-class, not a footnote)

**Trigger**: same-dir `WebView2Loader.dll`/`EmbeddedBrowserWebView.dll`/`libcef.dll`, or the target is Tauri/Wails/Electron/CEF/plain-WebView2 (`scan.ps1` step [5], `triage-router` WebView row). **The UI and most auth logic run as JavaScript in an embedded Chromium/WebKit renderer** -- so the primary channel is not the system proxy and not native hooking, it's **CDP remote-debugging into the renderer**. This supersedes the transport-recon question for the front-end's traffic: you read the plaintext *inside* the page, before TLS.

- **Enable + connect**: `WEBVIEW2_ADDITIONAL_BROWSER_ARGUMENTS=--remote-debugging-port=9222` (WebView2) or `--remote-debugging-port=` launch switch (Electron/CEF), user relaunches (Rule 8) -> `http://127.0.0.1:9222/json` -> CDP client. Full flow: `playbooks/tauri-webview.md`.
- **Why it beats proxy/native here**: a Rust/Go `reqwest`/rustls stack is proxy-immune (scan step [4] scores it dead), and hooking rustls is fiddly -- but the **IPC boundary** (`invoke`/`window.go.*`/`ipcRenderer`) carries the same request in plaintext *above* the native TLS. CDP gets both the front-end `fetch` and the IPC boundary in one document-start injection.
- **The renderer-vs-native sub-fork**: for this class, Rule 28's "can I inject?" splits further into **"is the logic in the renderer or the native backend?"** Default answer for a hybrid app = renderer -> CDP first. Native RE is the escalation, only after the JS layer proves the verdict is computed backend-side and un-overridable from JS.

**Feeds Stage 2.5**: WebView/CEF target -> "CDP front-end (read/flip store + hook fetch/IPC)" enters the route table as the **top-ranked** candidate; native RE on the backend is scored as escalation-only.

### Three-layer TLS/MITM verification (standard order for "connection failed/certificate error")

On any TLS handshake failure, cert error, or "proxied or not" symptom, don't guess and change config blindly. Verify layer by layer, independent of the target, confirming each with one command before the next (echoes Rule 19's "test tool assumptions first" and Rule 14's "switch to the smallest repro when the loop gets heavy"):

1. **Did the transport layer reach the expected endpoint?** Use a capture tool's connection log, or `openssl s_client -connect <host>:<port>` (with/without `-proxy`) to confirm whether traffic went through the proxy, bypassed it, or never got sent. Don't assume a config change took effect because it "should have" -- confirm via the timestamp/source of an actual connection record against when the change was made.
2. **If it went through a MITM, was it actually decrypted?** Same command with `-proxy`, check the issuer: real CA (Let's Encrypt) = tunneled, not decrypted; MITM's own CA (Reqable/Charles/mitmproxy CA) = really decrypted. Different troubleshooting paths follow -- don't assume "a rule exists, so it must be decrypted."
3. **Does the MITM's certificate satisfy client validation?** Check the SAN is really the requested hostname (not what you'd expect) and the chain validates against the client's trust store. Test for real -- don't assume "MITM proxies mint certs from the requested hostname"; implementations differ (one real case copied the upstream SAN instead).

Each layer verifies in seconds with one `openssl s_client`-family command, no target launch or user action needed. Only after all three are confirmed should you check whether target behavior actually recovered -- otherwise you're changing config blindly forever.

### I-Addendum: forcing a non-proxied target through Reqable (don't abandon the proxy route)

**Scenario**: Stage 2 app-filtered capture yields no records, and env-recon confirmed it's not proxied. Not necessarily dead -- identify which kind of "doesn't go through" first:

| Reason it doesn't go through the proxy | Force-forwardable to Reqable? | Method |
|---|---|---|
| **App ignores system proxy** (WinHTTP unconfigured / own HTTP stack but still HTTP/HTTPS) | [OK] Yes | **Proxifier** (standard Windows per-app TCP forcing tool, commercial): rule forcing the target exe's outbound TCP to Reqable's proxy port; chain via Reqable's upstream proxy if needed. Equivalents: ProxyCap / SocksCap. |
| **HTTPS + cert pinning** | [WARN] Forwardable, not decryptable | Proxifier gets Reqable the connection, but pinning fails the handshake -> defeat pinning with Frida first (Stage 4B, `references/frida-win/`), then return to the proxy route. |
| **Raw socket custom binary** (`ws2_32.send`/`WSASend`) | [X] HTTP proxy can't handle it | Reqable is HTTP(S)-only, can't parse raw TCP -- forwarding just yields a byte stream. Use an in-process hook instead (Frida on `send`/`recv`/`WSASend`, Stage 4B). |
| **Loopback (127.0.0.1) sub-engine** | [X] Cannot be captured | Neither system proxy nor Reqable sees loopback traffic. Switch to a local technique (Stage 4). |

**Key steps (Proxifier -> Reqable chain)**: (1) confirm Reqable's proxy port from its own UI (default differs by version -- don't hardcode); (2) in Proxifier, Proxy Server = `127.0.0.1:<port>` (HTTP) + a Rule matching only the target exe; (3) user installs Reqable's root cert (Rules 8/9), restart target, run the flow, confirm new records appear.
**[WARN] Unverified**: Reqable may have a built-in "force proxy/TUN" feature, but its docs were WAF-blocked so the exact name/port couldn't be confirmed. Check the Reqable UI on the spot first; prefer it over installing Proxifier if present. Don't assert menu names from memory.

**Feeds Stage 2.5**: "ignores system proxy" is recoverable (Proxifier) -> not downscored; pinning (defeat first) / raw socket / loopback get downscored or redirected to a hook.

---

## II. Tool/environment capability self-check (insufficient-capability techniques get removed, not scored)

**Root cause**: any technique needing memory/register writes, injection, or attaching depends on the tool/environment actually having that capability. One real case lost significant time to "MCP write permission disabled by default" (plugin was read-only, fix needed a debugger restart).

**Checklist before drafting a plan**:
- **Debugger capability**: memory write / register modify / scripting? MCP read-only? Does enabling write need a restart?
- **Can it attach**: admin privileges / PPL (protected process) / a service?
- **Anti-debug plugin present**: ScyllaHide / TitanHide already installed? (One real case had ScyllaHide installed locally but unchecked upfront.)
- **MCP installed**: `mcp__reqable__*` / `mcp__ida__*` / `mcp__x64dbg__*` present in the tool list (Rule 1).
- **CLI deps**: does e.g. `frida --version` actually succeed? A Python-binding error may be a DLL/interpreter conflict, not "not installed."

**Feeds Stage 2.5**: technique needs an unavailable, short-term-unfixable capability -> removed outright, doesn't enter scoring.

---

## III. Anti-analysis prerequisites (unpack / defeat anti-debug first if a packer exists, or nothing downstream is trustworthy)

**Root cause**: "not packed, no strong anti-debug" is luck, not guaranteed. Real commercial software commonly runs VMProtect/Themida, UPX/custom packers, integrity/checksum self-checks, TLS-callback anti-debug, timing checks/`IsDebuggerPresent`/hardware breakpoint detection. Analyzing while packed makes every result untrustworthy.

**Anti-analysis gate at process start**:
1. **Packer check**: `scripts/scan.ps1` (diec) + `references/x64dbg/yara-sigs/`. If packed -> L1/L2/L3 tiers in section one of `hard-target-playbook.md`, fetch an unpacker from `tool-registry.md Sec.1`.
2. **Self-checks/CFG**: integrity/checksum self-verification (crashes/refuses launch on a changed byte)? Electron asar integrity fuse enabled?
3. **Anti-debug**: `IsDebuggerPresent`/`NtQueryInformationProcess`/TLS callbacks/timing/hardware breakpoint detection -- if hit, bypass per section two of `hard-target-playbook.md` plus `references/frida-win/references/anti-debug-db/` (ScyllaHide/TitanHide or API hooking).
4. **Anti-VM/anti-injection**: anti-VM -> prefer a physical machine; anti-injection (module-name/cmdline blacklists) -> ASCII-neutral names in the analysis script (see `playbooks/nuitka.md Sec.5.2`).

**Feeds Stage 2.5**: until unpacked/anti-debug defeated, tag conclusions "environment not clean, pending re-verification"; these are prerequisites, not optional -- no high score until done.

---

## Tie-in with the main process

| Main process | Role of this reference |
|---|---|
| Stage 0 trust boundary diagram | Raw data for the three-check (process tree/ports/network stack) collected here |
| Stage 1, after packer check | The "anti-analysis" gate runs here |
| Stage 2, before capturing packets | Transport-layer recon first, don't default to HTTP/proxy |
| Stage 2, no capture records | I-Addendum sorts the 4 reasons; recoverable -> Proxifier forward, pinning -> Frida first, raw/loopback -> hook |
| Stage 2.5 route scoring | Three-check conclusions = the admission filter |
