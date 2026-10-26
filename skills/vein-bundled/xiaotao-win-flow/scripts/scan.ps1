# scan.ps1 — 查壳/侦察包装器(供 xiaotao-win-flow 技能调用)
# 用技能内置的 diec.exe 做静态查壳,相对路径定位,不写死绝对路径,可整体分发。
# 用法: powershell -File scan.ps1 -Target "C:\path\to\sample.exe"
# 输出:JSON(壳/编译器/库) + 熵值(判断是否加壳的关键指标)

param(
    [Parameter(Mandatory = $true)][string]$Target
)
$ErrorActionPreference = 'Stop'

# 相对本脚本定位内置 diec.exe:  <skill>/scripts/scan.ps1 -> <skill>/tools/die/diec.exe
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$diec = Join-Path $here '..\tools\die\diec.exe'
$diec = [System.IO.Path]::GetFullPath($diec)

if (-not (Test-Path $diec)) {
    Write-Output "ERROR: 找不到内置 diec.exe，预期位置: $diec"
    Write-Output "请确认技能目录 tools/die/ 完整(diec.exe + dll + db)"
    exit 2
}
if (-not (Test-Path $Target)) {
    Write-Output "ERROR: 目标文件不存在: $Target"
    exit 2
}

Write-Output "=== diec: $diec ==="
Write-Output "=== target: $Target ==="

Write-Output "`n--- [1] 深度+启发式扫描 (JSON) ---"
& $diec -d -u -j "$Target"

Write-Output "`n--- [2] 熵值 (高熵≈加壳/加密) ---"
& $diec -e "$Target"

Write-Output "`n--- [3] 文件信息 ---"
& $diec -i "$Target"

# ---------------------------------------------------------------------------
# [P] 壳判据 + 自动脱壳分支 (Rule 3 / Fast-path step 2 的扫描期触发点):
#     查到"具名壳(带壳名/版本)" -> 立即切脱壳分支, 并就该壳名+版本联网搜脱壳/调试技巧。
#     脱壳前下游一切(内存值/patch点/字符串/xref)都不可信, 所以这是最高优先级前置。
#     [关键防误报] 只认 diec 具名签名 (Packer/Protector/SFX: 具体名), 明确排除:
#       - "(Heur)Packer: Generic" 启发式泛化命中(无具体壳名, 正常 exe 上常泛报)
#       - 裸熵值高(内嵌模型/资源/压缩数据都会高熵; 高熵 != 加壳)
#     否则会把无壳目标(如内嵌大模型的 Rust exe)误导去追不存在的壳。通用逻辑, 不针对具体软件。
# ---------------------------------------------------------------------------
# [关键] 壳常在同目录的 SDK DLL/pyd 上, 主 exe 反而没壳(复盘: SPCloud64_Py.dll 是 Safengine 壳,
#        主程序无壳, 只扫主 exe "查了很多轮才查到")。所以【一次查全】: 目标 + 同目录每个 dll/pyd 都跑具名壳判据。
Write-Output "`n--- [P] 壳判据 + 脱壳分支 (目标 + 同目录所有模块一次查全; 查到具名壳 -> 搜该壳脱壳/调试技巧) ---"

# 单文件具名壳检测: 返回命中的具名壳数组(排除 (Heur)/Generic/Unknown 误报)
function Get-NamedPackers([string]$path) {
    $hits = @()
    try {
        $txt = & $diec -d -u "$path" 2>$null | Out-String
        foreach ($line in ($txt -split "`n")) {
            if ($line -notmatch '\(Heur\)' -and $line -match '^\s*(Packer|Protector|SFX)\s*:\s*(.+?)\s*$') {
                $val = $matches[2].Trim()
                if ($val -and $val -notmatch '^(Generic|Unknown)') { $hits += $val }
            }
        }
    } catch { }
    return ($hits | Select-Object -Unique)
}

# 待查清单: 目标本身 + 同目录 dll/pyd (系统目录跳过, 归属不可信 Rule 12)
$scanList = [System.Collections.ArrayList]::new()
[void]$scanList.Add(([System.IO.Path]::GetFullPath($Target)))
$tgtDir = Split-Path -Parent ([System.IO.Path]::GetFullPath($Target))
$sysDirsP = @("$env:WINDIR\System32", "$env:WINDIR\SysWOW64", "$env:WINDIR") | ForEach-Object { $_.ToLower().TrimEnd('\') }
$tgtInSys = $sysDirsP -contains $tgtDir.ToLower().TrimEnd('\')
if ($tgtInSys) {
    Write-Output "  [仅查目标] 目标在系统目录, 同目录模块归属不可信 (Rule 12), 只查目标本身。"
} else {
    try {
        Get-ChildItem -Path $tgtDir -File -ErrorAction Stop |
            Where-Object { $_.Extension -match '^\.(dll|pyd)$' } |
            ForEach-Object { [void]$scanList.Add($_.FullName) }
    } catch { Write-Output "  (同目录枚举失败: $($_.Exception.Message))" }
    Write-Output "  [分层测绘] 待查 $($scanList.Count) 个模块 (目标 + 同目录 dll/pyd)..."
}

# 逐个查, 汇总"模块 -> 壳"
$packedMods = @()   # 每项: @{ file=名; packers=@(...) }
$allPackers = @()
foreach ($f in $scanList) {
    $p = Get-NamedPackers $f
    if ($p.Count -gt 0) {
        $packedMods += @{ file = (Split-Path -Leaf $f); path = $f; packers = $p }
        $allPackers += $p
    }
}
$allPackers = $allPackers | Select-Object -Unique

if ($packedMods.Count -gt 0) {
    Write-Output "  [具名壳命中] 以下模块已加壳 -> 立即切脱壳分支 (Fast-path step 2); 脱壳前该模块下游结果全不可信:"
    foreach ($m in $packedMods) {
        Write-Output "    * $($m.file)  ->  $([string]::Join(', ', $m.packers))"
        Write-Output "        $($m.path)"
    }
    Write-Output ""
    Write-Output "  [注意] 带壳的可能不是主 exe 而是某个 SDK DLL/pyd -- 攻的是【带壳那层】, 别默认攻主程序。"
    Write-Output "  [动作] 就下面每个'壳名+版本'联网搜脱壳/调试技巧 (Rule 3: 搜壳名, 不搜'软件破解'; 先搜后动手):"
    $allPackers | ForEach-Object {
        Write-Output "    搜: `"$_ unpack / 脱壳`"  |  `"$_ OEP dump 脚本`"  |  `"$_ anti-debug bypass / 调试 绕过`""
    }
    Write-Output "  分流走 netcheck.ps1(海外 GitHub 走代理; 看雪/52pojie 直连); 专用工具见 tool-registry Sec.1 / hard-target-playbook。"
    Write-Output "  压缩壳(UPX/ASPack)脱完 re-triage 再继续; VM壳/强加密走重路线 + Rule 27(打边界别逃)。"
    Write-Output "  [缺工具] 需要脱壳/调试工具但没装 -> 报出工具名+入手先, 让【用户】自己装, 不自动装 (Rule 5)。"
} else {
    $deepTxt = & $diec -d -u "$Target" 2>$null | Out-String
    if ($deepTxt -match '\(Heur\).*Packer') {
        Write-Output "  目标 + 同目录模块均无具名壳 (仅目标有 (Heur)Packer 泛化命中) -> 大概率没加壳, 不切脱壳分支。"
    } else {
        Write-Output "  目标 + 同目录模块均无具名壳签名 -> 不切脱壳分支。"
    }
    Write-Output "  [注意] 熵值高 != 加壳: 内嵌模型/资源/压缩数据都会高熵。直接按 triage-router 分类走;"
    Write-Output "         若后续静态分析仍像自解密/自改写, 再回查壳 (x64dbg yara-sigs)。"
}

# ---------------------------------------------------------------------------
# [4] 网络栈预判 (Rule 28 控制权分叉的输入): 在动手抓包前就预判"系统代理能不能抓到"。
#     扫到自带栈 = 代理抓包判死刑, 直接走进程内 Hook, 别浪费用户的登录往返。
#     两个证据源: (a) 目标同目录的网络 DLL/PYD 文件名; (b) diec 深扫报告的 Go runtime。
#     [边界] 导入表需 PE 解析, diec 无此能力 -> 交给下游 IDA imports / x64dbg / dumpbin,
#            本步不臆测导入表。同目录扫仅对"装在自己目录的富客户端"有效, 系统目录跳过 (Rule 12)。
# ---------------------------------------------------------------------------
Write-Output "`n--- [4] 网络栈预判 (proxy-capture 可行性) ---"

# 已知网络栈组件文件名特征 -> (显示名, 系统代理是否抓得到)
$netSigs = @(
    @{ pat = 'sscronet|cronet';              name = 'Cronet (Chromium net)';         proxy = 'NO  (自带栈, 常无视系统代理)' },
    @{ pat = 'boringssl';                    name = 'BoringSSL';                     proxy = 'NO  (静态常无导出, 需 pattern scan)' },
    @{ pat = 'libssl|libcrypto|openssl';     name = 'OpenSSL (bundled)';             proxy = 'MAYBE (走系统 socket 才可能; 可能 pinning)' },
    @{ pat = 'Qt5Network|Qt6Network|QtNetwork'; name = 'Qt Network';                 proxy = 'MAYBE (视 QNetworkProxy 配置)' },
    @{ pat = 'nghttp|libcurl';               name = 'libcurl/nghttp2';               proxy = 'MAYBE (视是否读 env/系统代理)' },
    @{ pat = 'wininet';                      name = 'WinINet';                       proxy = 'YES (跟随系统代理)' },
    @{ pat = 'winhttp';                      name = 'WinHTTP';                       proxy = 'MAYBE (仅当显式配置代理)' }
)

$dir = Split-Path -Parent ([System.IO.Path]::GetFullPath($Target))
$hits = @()

# 4a. 同目录 DLL/PYD 文件名匹配 -- 但系统目录 (System32/SysWOW64/Windows) 下的 DLL 是全系统
#     共享的, 不能归属给目标 (Rule 12 硬证据: 相似名/邻近不算归属), 直接跳过同目录扫。
$sysDirs = @("$env:WINDIR\System32", "$env:WINDIR\SysWOW64", "$env:WINDIR") |
    ForEach-Object { $_.ToLower().TrimEnd('\') }
$inSysDir = $sysDirs -contains $dir.ToLower().TrimEnd('\')

if ($inSysDir) {
    Write-Output "  [跳过同目录扫] 目标位于系统目录 ($dir), 同目录 DLL 属全系统共享, 归属不可信 (Rule 12)。"
} else {
    try {
        Get-ChildItem -Path $dir -File -ErrorAction Stop |
            Where-Object { $_.Extension -match '^\.(dll|pyd)$' } |
            ForEach-Object {
                foreach ($s in $netSigs) {
                    if ($_.Name -match $s.pat) {
                        $hits += "[同目录文件] $($_.Name)  ->  $($s.name)  | 代理: $($s.proxy)"
                    }
                }
            }
    } catch {
        Write-Output "  (同目录枚举失败: $($_.Exception.Message))"
    }
}

# 4b. Go runtime -- 自带 net 栈, 全程无视系统代理。用硬特征 (.gopclntab section / Go build ID),
#     不用会误配的宽正则; 走 diec 深扫报告匹配。
try {
    $deep = & $diec -d -u "$Target" 2>$null | Out-String
    if ($deep -match '\.gopclntab|Go build ID|Golang|Go\(') {
        $hits += "[runtime] Go (自带 net 栈)  | 代理: NO  (Go net 全程无视系统代理, 必走 Hook)"
    }
} catch { }

$hits = $hits | Select-Object -Unique
if ($hits.Count -gt 0) {
    Write-Output "  发现网络组件:"
    $hits | ForEach-Object { Write-Output "    $_" }
    if ($hits -match 'NO ') {
        Write-Output ""
        Write-Output "  [判据] 命中自带/无视代理的网络栈 -> 系统代理抓包很可能空手。"
        Write-Output "         Rule 28: 本地可注入目标优先进程内 Hook (SSL 明文/边界), 不要先折腾代理。"
    }
} elseif (-not $inSysDir) {
    Write-Output "  未在同目录命中已知自带网络栈 (导入表未查 -> 下游 IDA/x64dbg 确认)。"
    Write-Output "  [判据] 可能走 WinINet/Schannel 等标准栈 -> 系统代理抓包可行性较高, 可并行开抓。"
    Write-Output "         (仍受 loopback/raw-socket/pinning 影响, 空手则查 env-recon.md I-Addendum)"
}

# ---------------------------------------------------------------------------
# [5] GUI 层预判 (Rule 28 第二轴): 目标是不是 WebView/CEF 混合应用?
#     命中 = UI + 大部分鉴权逻辑是嵌入式浏览器里的 JS, 主攻面在前端, 走 CDP 而非 IDA。
#     这是复盘的头号时间黑洞: Rust+WebView2 被当纯原生上了 IDA, 绕了 4 倍时间。
#     只看同目录 DLL 文件名 (系统目录跳过, Rule 12), 不臆测。
# ---------------------------------------------------------------------------
Write-Output "`n--- [5] GUI 层预判 (WebView/CEF 混合应用? -> 逻辑在前端, 走 CDP) ---"

# 特征文件名 -> (框架, 后端语言提示)
$guiSigs = @(
    @{ pat = 'EmbeddedBrowserWebView|WebView2Loader'; name = 'WebView2 嵌入 (Tauri / Wails / .NET-WebView2)'; hint = 'Rust->Tauri, Go->Wails, .NET->plain-WebView2' },
    @{ pat = '^libcef\.dll$|^cef\.pak$|^chrome_elf\.dll$'; name = 'CEF (嵌入式 Chromium)'; hint = 'C++/Delphi 后端 + CEF 前端' },
    @{ pat = 'v8_context_snapshot|^node\.dll$';       name = 'Electron (打包 Chromium + Node)';        hint = '见 tool-registry Sec.5.5/5.8 + tauri-webview CDP 流程' }
)

if ($inSysDir) {
    Write-Output "  [跳过] 目标位于系统目录, 同目录 DLL 归属不可信 (Rule 12)。"
} else {
    $guiHits = @()
    try {
        # 5a. 同目录 DLL/资源 -- 仅抓 CEF/Electron/Wails-带本地loader; Tauri 无此文件 (静态链接+系统运行时)。
        $files = Get-ChildItem -Path $dir -File -ErrorAction Stop
        $asar = Get-ChildItem -Path $dir -Recurse -Depth 2 -Filter '*.asar' -File -ErrorAction SilentlyContinue | Select-Object -First 1
        foreach ($f in $files) {
            foreach ($g in $guiSigs) {
                if ($f.Name -match $g.pat) {
                    $guiHits += "[同目录文件] $($f.Name)  ->  $($g.name)  | $($g.hint)"
                }
            }
        }
        if ($asar) { $guiHits += "[递归发现] $($asar.Name)  ->  Electron (.asar 资源包)  | 见 tool-registry Sec.5.5/5.8" }

        # 5b. [Tauri 主判据] 目标 exe 自身内嵌字符串 -- Tauri/Wails 把 wry/webview2 静态链进 exe,
        #     同目录没有 webview DLL, 唯一可靠的"本目标硬证据"(Rule 12) 是 exe 里烤进去的串。
        #     分块流式扫 (exe 可能几百 MB), 块间保留 32B 重叠防跨界漏匹配, 命中即够。
        $exeMarkers = @{ 'wry' = 'wry (Tauri/Wails WebView 绑定库)'; 'tauri' = 'tauri (Tauri 运行时)';
                         'CoreWebView2' = 'CoreWebView2 (WebView2 COM API)'; 'libcef' = 'libcef (CEF)';
                         'Electron' = 'Electron' }
        $found = @{}
        $appIds = @{}   # 同扫顺手抓 Tauri/WebView bundle-id (com.x.app / com.x.desktop) -> 用于 EBWebView 归属
        try {
            $fs = [System.IO.File]::OpenRead($Target)
            $buf = New-Object byte[] (8MB)
            $tail = ''
            while (($n = $fs.Read($buf, 0, $buf.Length)) -gt 0) {
                $chunk = $tail + [System.Text.Encoding]::ASCII.GetString($buf, 0, $n)
                foreach ($m in $exeMarkers.Keys) {
                    if (-not $found.ContainsKey($m) -and $chunk -match [regex]::Escape($m)) { $found[$m] = $true }
                }
                foreach ($mm in [regex]::Matches($chunk, '[a-zA-Z][a-zA-Z0-9_-]{1,30}(?:\.[a-zA-Z0-9_-]{1,30}){1,4}\.(?:app|desktop)')) {
                    $appIds[$mm.Value] = $true
                }
                $tail = if ($chunk.Length -ge 64) { $chunk.Substring($chunk.Length - 64) } else { $chunk }
            }
            $fs.Close()
        } catch { Write-Output "  (exe 字符串扫描失败: $($_.Exception.Message))" }
        foreach ($m in $found.Keys) { $guiHits += "[exe内嵌串] '$m'  ->  $($exeMarkers[$m])" }

        # 5c. [归属证据] 只报与本 exe 内嵌 bundle-id 匹配的 EBWebView 目录 -- 全系统扫会列出十几个无关 app,
        #     那是噪声不是归属 (Rule 12)。用 exe 里烤出的 appid 精确匹配, 才是"本目标的"前端数据落地点。
        if ($appIds.Count -gt 0) {
            foreach ($root in @($env:LOCALAPPDATA, $env:APPDATA)) {
                if (-not $root) { continue }
                foreach ($id in $appIds.Keys) {
                    $eb = Join-Path (Join-Path $root $id) 'EBWebView'
                    if (Test-Path $eb) { $guiHits += "[归属证据] $eb -> 本目标 WebView2 用户数据 (前端 store/localStorage 落地点, appid=$id)" }
                }
            }
            $guiHits += "[exe内嵌 appid] " + (($appIds.Keys | Select-Object -First 5) -join ', ')
        }
    } catch {
        Write-Output "  (同目录枚举失败: $($_.Exception.Message))"
    }

    $guiHits = $guiHits | Select-Object -Unique
    if ($guiHits.Count -gt 0) {
        Write-Output "  命中 GUI 层特征:"
        $guiHits | ForEach-Object { Write-Output "    $_" }
        Write-Output ""
        Write-Output "  [判据] 这是 WebView/CEF 混合应用 -- UI + 大部分鉴权逻辑是嵌入式浏览器里的 JS。"
        Write-Output "         *** 别对着原生二进制上 IDA (复盘头号弯路, 4x 耗时)。***"
        Write-Output "         Rule 28 第二轴: 主攻前端 -> CDP remote-debugging。"
        Write-Output "         照 references/playbooks/tauri-webview.md: 开 --remote-debugging-port"
        Write-Output "         -> document-start 一次性注入 hook fetch + IPC(invoke/go.*/ipcRenderer) + dump store"
        Write-Output "         -> 用户走一次登录 -> 当场改前端判定值验证 = [OK]。"
        Write-Output "         原生 RE 是升级手段, 仅当 JS 层证明判定在后端且无法从 JS 覆盖时才用。"
        if ($diec) {} # (保留: 后端语言由上文 diec 分类给出, 此处只判 GUI 层)
    } else {
        Write-Output "  未命中 WebView/CEF/Electron 同目录特征 -> 大概率纯原生 GUI 或 CLI, 按 triage-router 原生路线走。"
        Write-Output "  (若后续在进程里看到 msedgewebview2.exe 子进程 / Chromium 线程, 回到本判据重估。)"
    }
}
