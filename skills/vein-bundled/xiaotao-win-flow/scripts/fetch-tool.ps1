# fetch-tool.ps1 — 逆向工具【探活/入手先呈现】助手(供 xiaotao-win-flow 技能调用)
# 【本脚本只探活+打印"给用户执行的安装命令/下载链接",绝不代替用户下载或安装】
#   (用户决定:缺工具→停下,报出"工具名+入手先/命令",由用户自己装。与 bootstrap-tools.ps1 同策。)
# 作用:走系统代理(默认 7897)【探活】GitHub/PyPI 上 references/tool-registry.md 里登记的工具是否存在,
#       并【打印】该工具的安装命令 / release 下载链接,供用户自行执行。不含任何真正下载/安装动作。
# 安全:呼应主 SKILL.md 铁律5/铁律8——助手负责把"工具名+入手先/命令"呈现给用户,由【用户】自己装。
#
# 用法:
#   # 1) 探活:确认仓库/包存在(只读,安全)。先探活,避免报错名字的包。
#   powershell -File fetch-tool.ps1 -Probe -Repo "ergrelet/unlicense"
#   powershell -File fetch-tool.ps1 -Probe -Pip "pycryptodome"
#
#   # 2) 呈现安装命令(打印给用户执行,脚本不执行):
#   powershell -File fetch-tool.ps1 -Pip "pycryptodome"          # 打印 pip 安装命令
#   powershell -File fetch-tool.ps1 -Repo "can1357/NoVmp"        # 打印 git clone 命令
#
#   # 3) release 链接:很多逆向工具只发编译好的 exe/zip,用 -Release 列出下载链接给用户自己下
#   powershell -File fetch-tool.ps1 -Release "dnSpyEx/dnSpy"                  # 列最新 release 的资源清单(只读)
#   powershell -File fetch-tool.ps1 -Release "dnSpyEx/dnSpy" -Asset "win64"   # 列出匹配 win64 的下载链接(供用户自己下)
#
# 参数:
#   -Repo    "owner/name"  GitHub 仓库(打印 git clone 命令;若给 -Pip 则优先 pip)
#   -Pip     "pkg"         PyPI 包名(打印 pip install 命令)
#   -Uv      "pkg"         打印 uv tool install 命令(如 frida-tools)
#   -Winget  "id"          打印 winget 安装命令(如 upx)
#   -Release "owner/name"  列 GitHub Release 编译产物的下载链接(dnSpy/Scylla/de4dot-cex 等)
#   -Asset   "pattern"     -Release 时挑哪个资源(子串匹配,如 win64/zip);不给则列全部资源让用户选
#   -Dest    "路径"        建议的落地目录(默认 ./re-tools/<name>),仅用于提示,脚本不创建/不下载
#   -ProxyPort N           探活走的代理端口(默认 7897)
#   -NoProxy               探活不走代理(直连)
#   -Probe                 只探活,不打印安装命令

[CmdletBinding()]
param(
    [string]$Repo,
    [string]$Pip,
    [string]$Uv,
    [string]$Winget,
    [string]$Release,
    [string]$Asset,
    [string]$Dest,
    [int]$ProxyPort = 7897,
    [switch]$NoProxy,
    [switch]$Probe
)
$ErrorActionPreference = 'Stop'

if (-not ($Repo -or $Pip -or $Uv -or $Winget -or $Release)) {
    Write-Output "ERROR: 至少提供 -Repo / -Pip / -Uv / -Winget / -Release 之一。用法见脚本头部注释。"
    exit 2
}

# ---- 代理决策:优先用户指定端口,其次系统代理,-NoProxy 则直连 ----
$proxy = $null
if (-not $NoProxy) {
    $proxy = "http://127.0.0.1:$ProxyPort"
}
Write-Output "=== fetch-tool ==="
Write-Output "proxy   : $(if ($proxy) { $proxy } else { 'DIRECT (no proxy)' })"
Write-Output "mode    : $(if ($Probe) { 'PROBE (只探活)' } else { '呈现安装命令/下载链接给用户(脚本不下载/不安装)' })"

# ---- 探活:HEAD 请求确认目标存在(只读) ----
function Probe-Url([string]$url) {
    try {
        $p = @{ Uri = $url; Method = 'Head'; TimeoutSec = 15; UseBasicParsing = $true }
        if ($proxy) { $p['Proxy'] = $proxy }
        $r = Invoke-WebRequest @p
        return [int]$r.StatusCode
    } catch {
        if ($_.Exception.Response) { return [int]$_.Exception.Response.StatusCode }
        return 0
    }
}

# ---- 解析 GitHub 最新 release 的资源 URL(走网页端点,绕开 api.github.com 的 60/小时匿名限流) ----
# 方法:①请求 /releases/latest 拿重定向后的真实 URL,尾段即 tag;②抓 /releases/expanded_assets/<tag> 里的下载链接。
function Resolve-ReleaseAssets([string]$ownerRepo) {
    $common = @{ TimeoutSec = 30; UseBasicParsing = $true }
    if ($proxy) { $common['Proxy'] = $proxy }
    # ① 拿 tag:latest 会 302 到 /releases/tag/<tag>
    $latest = "https://github.com/$ownerRepo/releases/latest"
    try {
        $r = Invoke-WebRequest @common -Uri $latest -MaximumRedirection 5
        $eff = $r.BaseResponse.ResponseUri.AbsoluteUri
    } catch {
        # 某些 PowerShell 版本把最终 URL 放在异常里;兜底再取一次
        $eff = $latest
    }
    $tag = ($eff -split '/tag/')[-1]
    if (-not $tag -or $tag -eq $eff) {
        Write-Output "!!! 无法解析 $ownerRepo 的 release tag(可能无 release,或需 git clone/自行编译)。eff=$eff"
        return @{ tag = $null; assets = @() }
    }
    # ② 抓资源清单
    $ea = "https://github.com/$ownerRepo/releases/expanded_assets/$tag"
    $assets = @()
    try {
        $h = (Invoke-WebRequest @common -Uri $ea).Content
        # 抓 /owner/repo/releases/download/<tag>/<file> 形式的相对链接
        [regex]::Matches($h, 'href="(/[^"]+/releases/download/[^"]+)"') | ForEach-Object {
            $assets += "https://github.com$($_.Groups[1].Value)"
        }
        $assets = $assets | Select-Object -Unique
    } catch {
        Write-Output "!!! 抓 expanded_assets 失败:$($_.Exception.Message)"
    }
    return @{ tag = $tag; assets = $assets }
}

if ($Probe) {
    if ($Repo) {
        $u = "https://github.com/$Repo"
        Write-Output "probe github: $u -> $(Probe-Url $u)"
    }
    if ($Pip) {
        $u = "https://pypi.org/pypi/$Pip/json"
        Write-Output "probe pypi  : $u -> $(Probe-Url $u)"
    }
    if ($Uv)  { Write-Output "probe uv    : (uv 装的通常也是 PyPI 包)  https://pypi.org/pypi/$Uv/json -> $(Probe-Url "https://pypi.org/pypi/$Uv/json")" }
    if ($Winget) { Write-Output "probe winget: winget 包需本地 'winget search $Winget' 确认,脚本不联网探 winget 源" }
    if ($Release) {
        $u = "https://github.com/$Release/releases/latest"
        Write-Output "probe release: $u -> $(Probe-Url $u)  (200/302=有 release)"
    }
    exit 0
}

# ---- -Release:列/下载 GitHub release 编译产物 ----
if ($Release) {
    Write-Output "`n--- 解析 $Release 最新 release ---"
    $rel = Resolve-ReleaseAssets $Release
    if (-not $rel.tag) {
        Write-Output "RESULT=NO_RELEASE — 该仓库无可解析的 release 二进制,改用 -Repo(git clone 后自行编译)。"
        exit 1
    }
    Write-Output "tag     : $($rel.tag)"
    if ($rel.assets.Count -eq 0) {
        Write-Output "该 release **无二进制资源**(常见于只发源码 zip 的仓库,如 Scylla)。改 -Repo git clone 自行编译。"
        exit 1
    }
    Write-Output "资源清单:"
    $rel.assets | ForEach-Object { Write-Output "  $_" }

    # 挑资源
    $picked = $rel.assets
    if ($Asset) { $picked = $rel.assets | Where-Object { $_ -like "*$Asset*" } }
    if ($Asset -and $picked.Count -eq 0) {
        Write-Output "`n!!! -Asset '$Asset' 没匹配到任何资源,请从上面清单挑子串重试。"
        exit 2
    }
    if (-not $Asset) {
        Write-Output "`n[提示] 未指定 -Asset:上面是全部资源。加 -Asset `"关键字`"(如 win64/zip)选一个,列出其下载链接供用户自己下。"
        exit 0
    }

    if (-not $Dest) { $Dest = Join-Path (Get-Location) "re-tools\$(($Release -split '/')[-1])" }
    Write-Output "`n--- 下载链接(-Asset '$Asset' 命中 $($picked.Count) 个)——【由用户自己下载】,建议落地目录 $Dest ---"
    $picked | ForEach-Object { Write-Output "  $_" }
    Write-Output "`n[停止] 本脚本不代下载。助手把上面的链接给用户,由用户自己下载到建议目录(zip 自行解压,注意校验来源)。"
    exit 0
}

# ---- 组装将执行的命令 ----
$commands = @()

if ($Winget) {
    $commands += "winget install --id $Winget -e"
}
if ($Uv) {
    # uv 走代理靠环境变量
    if ($proxy) { $commands += "`$env:HTTPS_PROXY='$proxy'; `$env:HTTP_PROXY='$proxy'; uv tool install $Uv" }
    else        { $commands += "uv tool install $Uv" }
}
if ($Pip) {
    $proxyArg = if ($proxy) { " --proxy $proxy" } else { "" }
    $commands += "python -m pip install --upgrade$proxyArg $Pip"
}
if ($Repo -and -not $Pip) {
    $name = ($Repo -split '/')[-1]
    if (-not $Dest) { $Dest = Join-Path (Get-Location) "re-tools\$name" }
    $proxyCfg = if ($proxy) { "-c http.proxy=$proxy -c https.proxy=$proxy " } else { "" }
    $commands += "git $proxyCfg clone --depth 1 https://github.com/$Repo `"$Dest`""
}

Write-Output "`n--- 安装命令(【给用户执行】,本脚本不代跑)---"
$commands | ForEach-Object { Write-Output "  $_" }
Write-Output "`n[停止] 助手把上面的工具名+命令告诉用户,由【用户】自己执行安装后再继续(铁律5/铁律8)。"
if ($Repo -and -not $Pip) { Write-Output "[提示] git clone 只是第一步:很多工具还需用户自行编译/装依赖。" }
exit 0
