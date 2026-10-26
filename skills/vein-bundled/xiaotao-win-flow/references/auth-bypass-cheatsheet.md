# Auth-Bypass Technique Cheatsheet (defense-oriented)

> For xiaotao-win-flow when analyzing authorization/license checks. Goal: reconstruct red-team bypass techniques -> work backward to hardening, for developers hardening their own (or authorized) software -- not for cracking someone else's.
> Sources: Securitum "Breaking license validation in a desktop application," GuardingPearSoftware "Bypassing simple license checks," dev.to "Understanding Software Activation and Cracking Techniques," HackTricks reversing.

## Two forms of authorization checking (identify which first)

| Form | Characteristics | Weakness | Main battleground |
|---|---|---|---|
| **Local (offline)** | Client itself computes authorized/unauthorized -- local boolean or algorithmic key check | Logic lives on client -- findable and alterable | Binary layer (patch/hook) |
| **Online (networked)** | Sends key + machine fingerprint to server, which decides | Protocol capturable/modifiable; lax server validation allows replay/forgery | Network layer (capture/modify/forge) |
| **Hybrid** | Online result cached locally | Cache treated as permanent authorization | Either layer |

**Tell which**: Stage 1, capture traffic. Auth request exists -> online; none capturable -> local. Hybrid is most common: one network call, then relies on local cache.

---

## Gate-type checklist (after login, check every category -- don't fixate on the "authorization gate")

> Classic pitfall: treating only login/heartbeat/local-file as gates, when the real blocker -- looking like a crash-on-launch -- is the **version-update gate**. "Crashes/hangs/bounces to login" != necessarily the authorization gate. After login, check every gate category, match technique to the one actually hit.

| Gate type | Symptom/trigger | Locating signature | Matching technique |
|---|---|---|---|
| **Authorization gate** | "Not activated"/"expired" popup, feature greyed out | `/auth`, `/verify`, `/membership`; response has `isActive`/`vip` | Techniques 1-7 |
| **Version/forced-update gate** [WARN] often overlooked | **Looks like crash on launch**, exits immediately, "please update" popup; `current<minimum -> blocked` | `/version`, `/get_latest`, `/check_update`, `/app/config`; `minVersion`/`latestVersion`/`forceUpdate` | Technique 3 (forge `forceUpdate=false`/inflate local version) or edit local version constant |
| **Heartbeat/session gate** | Disconnects after a while, kicked to login | Periodic `/heartbeat`, `/keepalive`, `/session`; short-lived tokens | Technique 3 + replay; watch session monitoring |
| **Compute/feature gate (remote exec)** | UI shows unlocked but **running fails/no result** | Request goes to remote compute node (e.g. `:8443` GPU service) validating independently | **Client-side bypass likely dead end** -- SKILL Stage 3 "is client-side bypass possible" check |
| **Integrity/anti-debug gate** | Exits/changes behavior when debugged/patched | .text CRC self-check, `IsDebuggerPresent`, Frida detection | `hard-target-playbook.md` sec 2 |

**Per-endpoint validation**: many backends validate the token independently on **every** business endpoint. Forging only login/verify leaves other endpoints hitting the real server with a fake token -> all 401 -> bounced to login. -> SKILL Stage 3: enumerate every token-gated endpoint first, forge all at once with a wildcard.

---

## Techniques (mechanism -> locate via RE -> hardening)

### 1. Binary patching (patch/NOP a jump)
- **Mechanism**: find the conditional jump after the check (`je/jne/jz/jnz`), flip it, make unconditional, or NOP it to force the "authorized" branch. Classic, lowest-cost.
- **Locate** (Stage 3 IDA / Stage 4 x64dbg): search auth strings ("not authorized," "trial expired," "invalid license") -> xref to validation function -> its bool return + call site's `test eax,eax`/conditional jump -> breakpoint it, watch eax/flags.
- **Harden**: don't rely on one decision point (single `if(isLicensed)` is fragile) -- use distributed redundant checks. Feed the auth result into a computation (decrypt feature data with a license-derived key) so patching alone doesn't unlock it. Runtime integrity self-check: CRC/hash your own .text, exit if patched (protect the check itself too, via redundant copies).

### 2. Return-value forgery / function hooking
- **Mechanism**: without touching disk, Frida/debugger-hook the validation function at runtime, force `return true`; or hook the consumer of that result to unconditionally unlock.
- **Locate** (Stage 4 Frida, `frida-win/SKILL.md`): hook the target function, print args/return to confirm it's the real decision point; hook Win32 APIs (`strcmp`, `RegQueryValueEx`, `bcrypt`) to trace auth data flow.
- **Harden**: anti-hook/anti-debug (altered prologue detection, Frida detection via thread names/ports/memory sigs, `IsDebuggerPresent`/PEB/hardware-breakpoint checks -- raises the bar, doesn't fix root cause). Don't trust one function's return value -- feed it into subsequent encryption, not just an `if`. Move critical logic server-side -- can't hook what's not on the client.

### 3. Forging/replaying server responses (main attack surface for online checks)
- **Mechanism** (Securitum case study): capture an activation request -> find which fields the server actually validates vs ignores -> replay with tweaks to unvalidated fields, letting one license activate multiple devices; or stand up a fake local server replying "authorized."
- **Locate** (Stage 1 Reqable): capture the request, examine URL/params (key, machine serial, fingerprint) and which response field decides auth. Modify device-identifier params and replay to test server strictness (feeds the hardening assessment). Non-proxy-aware apps need a transparent proxy (Reqable/Burp invisible proxy).
- **Harden** (per Securitum): server must strictly validate every parameter. Decouple authorization from device identity -- generate a unique secret per license+device via challenge-response, not a repeated static value. Sign requests with HMAC-SHA256 + timestamp/nonce against replay. Session monitoring: revoke a token seen on multiple devices immediately. Sign responses too, verify client-side, to block forged responses.

### 4. Bypassing cert pinning / algorithm-level cracking of encrypted traffic (to reach techniques 2/3's content)
- **Mechanism**: SSL pinning or self-encrypted body blocks plaintext capture. (a) Bypass pinning: Frida-hook out the validation function or swap the cert chain so the proxy decrypts. (b) Can't bypass -> study ciphertext/algorithm instead (not a dead end): reverse the encryption/signing algorithm in IDA (Stage 3), ID crypto constants, per Iron Rule 3 search for a third-party library implementing it; decrypt captured ciphertext yourself; go further and forge requests/responses using the recovered algorithm (extends technique 3 -- key/algorithm in hand means valid ciphertext on demand).
- **Locate**: (a) `frida-win/SKILL.md` TLS/pinning bypass section; (b) reverse in `ida-re/`, confirm key dynamically with `x64dbg`.
- **Harden**: pinning/body encryption only raise the bar, not the real defense. Don't hardcode the key client-side (that's what enables (b)) -- issue server-side, one-time-use, or asymmetric. Real defense is item 3: strict server validation + request signing, so full algorithm recovery still can't forge a valid signature without the server's private key/secret.

### 5. Forging license file / registry / cached state
- **Mechanism**: auth state in a local file, registry key, or cached boolean (`premium_unlocked=true`, PlayerPrefs) -- edit it directly.
- **Locate**: monitor file/registry I/O with Frida/Procmon (`RegQueryValueEx`, `CreateFileW`); look for readable key names/endpoints (`/validate-license`, `premium_unlocked`) -- plaintext names are signposts.
- **Harden**: treat local cache as convenience not authority -- expire it, refresh before high-value ops. Sign/encrypt the cache; never store the final unlock decision in plaintext. Decide high-value features server-side.

### 6. Keygen / algorithm reverse engineering (offline checking)
- **Mechanism**: reverse the key-validation algorithm -> write a keygen producing valid keys.
- **Locate**: find the algorithm in IDA (Stage 3), ID crypto constants (`x64dbg`/`yara-sigs` scan, or diec's crypto detection).
- **Harden**: validate with asymmetric signatures (server private key signs, client public key verifies) -- client never holds the private key. Don't roll a reversible homegrown algorithm -- once you spot RSA/AES etc., per Iron Rule 3 search for correct third-party library usage (not a crack).

### 7. Bypassing time checks (trial periods)
- **Mechanism**: change system clock, clear first-run timestamp, or hook the time API to dodge expiration.
- **Harden**: server's authorization time is authoritative; sign and store first-run timestamp; detect clock rollback.

---

## Hardening priority (Stage 5 delivery)

Weakest to strongest, layer incrementally:

1. **(Weakest)** Single local boolean decision point -> retire it.
2. Obfuscate symbols/strings (remove signposts like `ValidateLicense`) -> raises locating cost, not a real fix.
3. Anti-debug/anti-hook/runtime integrity self-checks -> raises dynamic-bypass cost, not a real fix.
4. Multi-point redundant validation + feeding auth result into critical computations -> makes patching/hooking a single point ineffective.
5. **(Strongest)** Move critical logic and the authorization decision server-side + sign requests (HMAC/challenge-response) + session monitoring + short-lived auth -> client has no complete logic left to bypass.

> Core takeaway (GuardingPearSoftware): authorization is a "trust signal," not a "magic wall." A valuable feature can't rely on one yes from the client. The server holds the trustworthy result; the client only displays it.
