# Tauri / WebView2 / CEF hybrid playbook -- logic lives in the renderer, drive it with CDP

> **Why this file exists** (post-mortem, ECutAuto / Tauri): the skill used to equate "Rust" with "native RE" and pushed a textbook Tauri app onto the IDA/x64dbg/socket route. It took ~4x longer and never landed `[OK]`. The truth for this whole target class: **the UI and most of the auth judgment run as JavaScript inside an embedded Chromium/WebKit renderer.** The backend (Rust/Go/C++) is often just a thin IPC + native-call shim. So the primary attack surface is the **web layer**, reached via CDP (Chrome DevTools Protocol) remote-debugging -- NOT the native binary. Go here the moment triage or `scan.ps1` flags a WebView/CEF DLL, before touching IDA.

---

## 0. Identify which hybrid it is (all route to CDP, enablement differs)

| Framework | Backend | Renderer engine | Same-dir / process tells |
|---|---|---|---|
| **Tauri** | Rust | system WebView2 (Win) / WebKit | `WebView2Loader.dll`, `EmbeddedBrowserWebView.dll`, user-data dir `%LOCALAPPDATA%\<appid>\EBWebView`, `__TAURI_INTERNALS__`/`__TAURI__` reachable in the page, Rust panic strings in the exe |
| **Wails** | Go | system WebView2 (Win) | `WebView2Loader.dll` + Go build marks (`.gopclntab`); `window.go.*` IPC bindings |
| **Electron** | Node | bundled Chromium | `.asar`, `node.dll`, `v8_context_snapshot.bin`, `resources/` (this is its own class -- see `triage-router` Electron row + `tool-registry Sec.5.5/5.8`, but the CDP flow below still applies) |
| **CEF (native + embedded Chromium)** | C++/Delphi/etc. | bundled Chromium | `libcef.dll`, `cef.pak`, `icudtl.dat`, `chrome_elf.dll` |
| **Plain WebView2 (.NET/C++)** | .NET/C++ | system WebView2 | `WebView2Loader.dll` + `Microsoft.Web.WebView2.*` |

**Key discriminator vs pure-native**: a `WebView2Loader.dll` / `EmbeddedBrowserWebView.dll` / `libcef.dll` sitting next to the exe means the front-end is a web page. Rust + WebView2 = almost certainly Tauri. Do not read this as "a native app that happens to show HTML" -- read it as "a web app with a native shell," and attack the web app.

---

## 1. The core move -- enable CDP remote-debugging, connect, own the renderer

CDP is a first-class, standard channel. It lets you read every DOM/JS value, inject code before the page's own scripts run, watch all `fetch`/IPC calls with plaintext args+returns, and rewrite state live. This is the default observe+rewrite channel for the whole class.

### 1.1 Enable the debug port (user sets env/flag + restarts -- Rules 8/9)

| Framework | How to open the port | Notes |
|---|---|---|
| **Tauri / Wails / plain WebView2** | set env `WEBVIEW2_ADDITIONAL_BROWSER_ARGUMENTS=--remote-debugging-port=9222` for the target process, then user relaunches | documented WebView2 passthrough; works without touching the binary. Some Tauri release builds disable devtools -- the remote-debugging port still attaches even when the right-click inspector is off. |
| **Electron** | relaunch with `--remote-debugging-port=9222` (renderer) and/or `--inspect=9223` (main/Node) | single-instance-lock may kick a second launch -- kill all instances first. asar integrity fuse does not block CDP. |
| **CEF** | relaunch with `--remote-debugging-port=9222` | CEF honors the switch natively; some apps strip switches -- if so, set via a config/ini the app reads, or fall back to Sec.4. |

Give the user the **exact** command/env-set line and the absolute target path; they set it and relaunch (Rule 8). Example (PowerShell): `$env:WEBVIEW2_ADDITIONAL_BROWSER_ARGUMENTS='--remote-debugging-port=9222'; & 'C:\path\target.exe'`.

### 1.2 Connect

- List targets: `curl http://127.0.0.1:9222/json` -> each page has a `webSocketDebuggerUrl`. `/json/version` shows the browser build.
- Drive it with any CDP client: `chrome-remote-interface` (npm), Python `pychrome` / raw `websocket-client`, or Playwright/Puppeteer `connectOverCDP('http://127.0.0.1:9222')`. **No Frida, no native injection needed.**
- If `/json` refuses / is empty: port not really open (env not inherited -> confirm the user launched from the same shell that set it), or the app spawns the webview in a child process (attach to the child's port).

### 1.3 Inject at document-start (the timing bug that cost the post-mortem a round)

Hooking `fetch`/IPC **after** the page loaded fails when the app has already cached a reference to the original function (exactly what happened before). Always inject **before** the page's scripts run:

- CDP: `Page.enable` -> `Page.addScriptToEvaluateOnNewDocument({source})` -> `Page.reload`. The script runs at document-start on every navigation, before app code, so your wrappers are in place first.

---

## 2. One injection, one user action -- capture everything (kills the "6 logins" waste)

Do **not** test probes one at a time and make the user re-login for each. Inject a **single** document-start script that installs all observers at once, then have the user walk one login/redeem flow -- it captures all of it. This is the concrete form of "batch read-only observation" (Rule 25).

Put these in one script:

1. **Hook `window.fetch` + `XMLHttpRequest`** -> log URL, method, request body, response text. Catches any auth call the front-end makes directly (plaintext, pre-TLS).
2. **Hook the IPC bridge** -> the plaintext boundary even when the backend does the networking:
   - Tauri v2: wrap `window.__TAURI_INTERNALS__.invoke`; v1: `window.__TAURI__.invoke` / `window.__TAURI__.tauri.invoke`. Log `(cmd, args)` and the resolved return.
   - Wails: wrap `window.go.<binding>.<Method>`.
   - Electron preload: `require('electron').ipcRenderer.invoke/send` (hook in the renderer/preload context).
3. **Dump front-end state** after load: framework store + web storage.
   - Vue 3: locate the app via `document.querySelector('#app').__vue_app__` or a component's `$data`; Pinia store on the app instance; Vuex on `$store`.
   - React: `___reactContainer$*` fiber walk, or Redux store if exposed.
   - Always: `localStorage`, `sessionStorage`, and IndexedDB keys (member flags/tokens/expiry commonly cached here).

Return it all over CDP `Runtime` bindings in one pass.

---

## 3. Bypass -- usually a live value flip, verified on the spot

Tauri/WebView auth is very often a **server data-gate + client-side local unlock** (server returns something like `memberExpireTs`, the JS decides what to show/enable). Classify with `auth-arch-classify.md` first, then:

- **Client-side boolean/expiry in the store or storage** -> flip it live with `Runtime.evaluate` (set `store.isVip = true` / rewrite the expiry / patch the response inside your fetch hook) and have the user watch the real feature run = `[OK]`. This is the fastest path and the most common outcome for this class.
- **Server data-gate, response forgeable** -> forge inside the fetch hook (return a crafted `memberExpireTs`), or move to a proxy/fake-server per `auth-bypass-cheatsheet.md 3` (build the field dictionary from a real response first, Rule 19).
- **The verdict is genuinely computed in the native backend** (a `#[tauri::command]` returns the boolean and JS merely consumes it, with no client-side override) -> now, and only now, is the backend in scope: hook the IPC boundary to force the return, or go native RE on that **one** command (Rule 27 boundary attack). Do not assume this before checking the JS -- the post-mortem's whole lesson is that the JS layer was skipped.

Recognition stays two-tier: `[Y]` = UI unlocked only, `[OK]` = the real feature actually produced a result (Rules 6/19). Only `[OK]` earns a hardening write-up.

---

## 4. Capturing plaintext when the request is made in native code (reqwest/rustls et al.)

`scan.ps1` flags self-contained stacks (Cronet/Go-net/rustls) as proxy-dead. For a WebView hybrid, decide by **where the HTTP call originates**:

- **Front-end `fetch`/`axios`** -> the CDP fetch hook (Sec.2.1) already has the plaintext. Done.
- **Backend makes the call** (JS `invoke('login', creds)` -> Rust `reqwest`) -> the **IPC boundary hook (Sec.2.2) still sees the plaintext** args in and result out, regardless of the native TLS. This is the elegant first choice -- you rarely need to touch rustls at all.
- **If you must get it below the IPC boundary**, in priority order:
  1. **SSLKEYLOGFILE + Wireshark** -- works for the **Chromium/WebView2 renderer's own TLS** (Edge/Chromium honors `SSLKEYLOGFILE`). For **rustls/reqwest it usually does nothing**: rustls only writes keylog if the app opted in (`KeyLogFile`), which reqwest does not by default -- **verify, don't assume** (Rule 4). Same caveat for statically-linked BoringSSL/OpenSSL unless the app enabled keylog.
  2. **Memory-marker scan** -- run the flow with a unique marker string (e.g. a distinctive card/license code) as the needle, scan process memory for it, read the surrounding plaintext request/response. The post-mortem's fallback that worked -- but it's the *harder* path; try the IPC hook first.
  3. **Hook the native crypto/network fn** -- Frida on rustls/reqwest send/recv or the SSL write boundary (`frida-win/references/windows-hooking-recipes.md`, the SSL `_ex` clause). Last resort for this class.

---

## 5. Fast route summary (drop-in for the SKILL Fast path)

1. `scan.ps1` flags WebView2/CEF/Electron -> **this class**. Don't open IDA.
2. Give the user the env/flag line to open the CDP port + relaunch (Rule 8).
3. Connect CDP, `addScriptToEvaluateOnNewDocument` one script hooking fetch + IPC + store-dump, reload.
4. User walks **one** login/redeem flow -> you have every request, IPC call, and store value.
5. Flip the client-side gate (or forge the response) live -> user watches the real feature run = `[OK]`.
6. Only then, hardening from `[OK]` points (Rule 6).

Native RE (IDA/x64dbg on the Rust/Go/C++ backend) is the **escalation**, entered only if step 5 proves the verdict is truly computed native-side and un-overridable from JS -- not the default.

---

## Tie-in

| Main flow | This file |
|---|---|
| triage-router Rust row / WebView2-CEF hybrid row | routes here |
| `scan.ps1` step [5] flags a UI/web layer | come here at Stage 1, before native routing |
| env-recon Sec.I "CDP is the default channel" | CDP enablement + connect detail here |
| Fast path control-ownership fork (Rule 28), WebView sub-fork | "renderer vs native layer" resolved here |
| reqwest/rustls plaintext | Sec.4 (IPC-boundary hook first, marker/keylog fallback) |
