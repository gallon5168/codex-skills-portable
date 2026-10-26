# bootstrap-tools.ps1 — 环境体检(供 xiaotao-win-flow 阶段0 调用)
# 【本脚本只做体检,绝不自动安装】(用户决定:缺工具→停下,报出"工具名+入手先",由用户自己装)
# 目标:跑一遍,列出"稳定的非GUI核心工具"里缺了哪些,并给出每个缺失项的【推荐安装命令/入手先】,
#       然后【停止】。助手据此把工具名与来源告诉用户,由用户手动安装(铁律5/铁律8 同等对待)。
# 设计原则:
#   1) 不提前预装到仓库(怕版本过时);运行时只检查缺什么、报出来。
#   2) 版本敏感的工具(capa/angr)建议用 uv 起独立 py3.11 环境隔离——脚本给出建议命令,由用户执行。
#   3) 建议命令里:国内包走清华 PyPI 镜像;uv 下 Python 解释器建议走系统代理(默认 7897)。
#   4) 本脚本不带任何真正安装动作;无 -Execute 之类开关。呈现→停止,安装权在用户。
#   5) GUI 工具(x64dbg/IDA/dnSpy/Scylla/ScyllaHide/Reqable)同样由用户手动装/手动开(铁律8)。
#
# 用法:
#   powershell -File bootstrap-tools.ps1            # 体检 + 报出缺失项的推荐安装命令/入手先,然后停止
#   powershell -File bootstrap-tools.ps1 -CheckOnly # 只输出体检表,不给安装建议
#
# 参数:
#   -CheckOnly    只输出体检表,不组装安装建议
#   -ProxyPort N  建议命令里 uv 下载 Python 解释器走的代理端口(默认 7897)
#   -NoProxy      建议命令里 uv 下载不走代理(直连)
#   -PyMirror URL 清华 PyPI 镜像(默认 https://pypi.tuna.tsinghua.edu.cn/simple)

[CmdletBinding()]
param(
    [switch]$CheckOnly,
    [int]$ProxyPort = 7897,
    [switch]$NoProxy,
    [string]$PyMirror = 'https://pypi.tuna.tsinghua.edu.cn/simple'
)
$ErrorActionPreference = 'Continue'
$proxy = if ($NoProxy) { $null } else { "http://127.0.0.1:$ProxyPort" }

function Have([string]$cmd) {
    $old = $ErrorActionPreference; $ErrorActionPreference = 'SilentlyContinue'
    $g = Get-Command $cmd -ErrorAction SilentlyContinue
    $ErrorActionPreference = $old
    return [bool]$g
}
function PyMod([string]$mod) {
    # 在系统 python 里检查模块是否可导入
    if (-not (Have 'python')) { return $false }
    python -c "import $mod" 2>$null; return ($LASTEXITCODE -eq 0)
}

Write-Output "=== xiaotao-win-flow 环境自举体检 ==="
Write-Output "proxy(uv下Python用): $(if($proxy){$proxy}else{'DIRECT'})   PyPI镜像: $PyMirror"
Write-Output "mode: $(if($CheckOnly){'CHECK-ONLY(只体检)'}else{'体检+报出缺失项入手先(不安装)'})"
Write-Output ""

# ---- 体检:核心非GUI工具 ----
$rows = @()
$rows += [pscustomobject]@{ Name='python'; Have=(Have 'python'); Note='解释器(diec分诊/脚本)' }
$rows += [pscustomobject]@{ Name='git';    Have=(Have 'git');    Note='clone 源码类工具' }
$rows += [pscustomobject]@{ Name='uv';     Have=(Have 'uv');     Note='隔离装版本敏感工具的关键' }
$rows += [pscustomobject]@{ Name='frida';  Have=(Have 'frida');  Note='动态插桩CLI(阶段4B)' }
$rows += [pscustomobject]@{ Name='7z';     Have=(Have '7z');     Note='NSIS/安装器解包(§0.5)' }
$rows += [pscustomobject]@{ Name='upx';    Have=(Have 'upx');    Note='L1压缩壳一键脱' }
$rows += [pscustomobject]@{ Name='pyinstxtractor-ng'; Have=(Have 'pyinstxtractor-ng'); Note='PyInstaller解包' }
$rows += [pscustomobject]@{ Name='capa';   Have=(Have 'capa');   Note='加密/能力识别(uv隔离)' }
$rows += [pscustomobject]@{ Name='angr(mod)'; Have=(PyMod 'angr'); Note='符号执行keygen(uv隔离)' }

$rows | ForEach-Object {
    Write-Output ("  [{0}] {1,-20} {2}" -f $(if($_.Have){'OK '}else{'MISS'}), $_.Name, $_.Note)
}
Write-Output ""

# ---- frida 绑定/CLI 版本错配检查(常见坑:hook 报协议不匹配) ----
if ((Have 'python') -and (Have 'frida')) {
    $bind = (python -c "import frida;print(frida.__version__)" 2>$null)
    $cli  = (frida --version 2>$null)
    if ($bind -and $cli -and ($bind.Trim() -ne $cli.Trim())) {
        Write-Output "⚠️ frida 版本错配:python绑定=$bind  CLI=$cli  → hook 可能报错,建议对齐(见下)"
        $script:fridaMismatch = @($bind.Trim(), $cli.Trim())
    }
}
Write-Output ""

if ($CheckOnly) { exit 0 }

# ---- 组装安装命令(只装缺的) ----
$cmds = @()

if (-not (Have 'uv')) {
    # 用户没装 uv:优先 winget,退而用 pip 清华镜像装(pip 一定在,因为 python 在)
    $cmds += "winget install --id astral-sh.uv -e   # 或: python -m pip install -i $PyMirror uv"
}
if (-not (Have '7z'))  { $cmds += "winget install --id 7zip.7zip -e" }
if (-not (Have 'upx')) { $cmds += "winget install --id UPX.UPX -e" }

# frida 对齐(错配时):把系统 python 的绑定升到 CLI 同版本,走清华镜像
if ($script:fridaMismatch) {
    $cli = $script:fridaMismatch[1]
    $cmds += "python -m pip install -i $PyMirror frida==$cli frida-tools"
}

# capa:版本敏感 → uv tool install,指定 py3.11(不污染系统 py3.8),走清华镜像
# ★发布名是 flare-capa(Mandiant/FLARE),提供的 CLI 才叫 capa;PyPI 上的裸 `capa` 是无关空包。
if (-not (Have 'capa')) {
    $cmds += "uv tool install --python 3.11 --index-url $PyMirror flare-capa"
}
# angr:库(无CLI)→ uv 建独立 venv,scripts 用它跑;走清华镜像
# (PS 5.1 不支持 &&,拆两条;用法: .venv-angr\Scripts\python.exe your_angr_script.py)
if (-not (PyMod 'angr')) {
    $cmds += "uv venv --python 3.11 .venv-angr"
    $cmds += "uv pip install --python .venv-angr --index-url $PyMirror angr"
}

if ($cmds.Count -eq 0) {
    Write-Output "所有核心非GUI工具已就位,无需安装。"
} else {
    Write-Output "--- 缺失项 + 推荐入手先(【由用户自己安装】,本脚本不代装)---"
    $cmds | ForEach-Object { Write-Output "  $_" }
    Write-Output ""
    Write-Output "[提示] 以上命令是【给用户执行】的建议,不是脚本要跑的动作。"
    Write-Output "[提示] 执行时:uv 下 Python 解释器可走系统代理 $proxy;PyPI 包走清华镜像 $PyMirror(镜像域名需绕开代理直连)。"
    Write-Output "[停止] 助手须把上面的工具名+入手先告诉用户,由用户手动安装后再继续(铁律5/铁律8)。"
    Write-Output ""
}

# ---- 装后自检:解析每个工具的【绝对路径】并实测运行 ----
# 关键:winget/uv 装的工具常不在当前会话 PATH(7z 可能在非标准盘、capa 在 ~\.local\bin、upx 是 winget 别名),
# Get-Command 会假阴性。这里按已知落点解析真实路径并跑一下,给 skill/用户可直接调用的绝对路径(呼应铁律8/12)。
Write-Output "--- 已装工具的绝对路径解析(只读,给 skill/用户可直接调用的路径)---"
$skillDir = Split-Path -Parent $PSScriptRoot
function Find-First($cands) { foreach ($p in $cands) { if ($p -and (Test-Path $p)) { return $p } } return $null }
# 7z:注册表 InstallLocation 优先(可能在任意盘)
$7zReg = @("HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*","HKLM:\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*","HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*") |
    ForEach-Object { Get-ItemProperty $_ -ErrorAction SilentlyContinue } | Where-Object { $_.DisplayName -match '7-Zip' } | Select-Object -First 1 -Expand InstallLocation
$paths = [ordered]@{
    '7z'    = Find-First @( ($(if($7zReg){Join-Path $7zReg '7z.exe'})), "$env:ProgramFiles\7-Zip\7z.exe", "${env:ProgramFiles(x86)}\7-Zip\7z.exe" )
    'upx'   = Find-First @( (Get-ChildItem "$env:LOCALAPPDATA\Microsoft\WinGet\Packages" -Recurse -Filter 'upx.exe' -ErrorAction SilentlyContinue | Select-Object -First 1 -Expand FullName) )
    'capa'  = Find-First @( "$env:USERPROFILE\.local\bin\capa.exe" )
    'frida' = 'python -c "import frida"'
    'angr'  = Find-First @( "$skillDir\.venv-angr\Scripts\python.exe" )
}
$allok = $true
foreach ($k in $paths.Keys) {
    $p = $paths[$k]
    if (-not $p) { Write-Output ("  [未定位] {0}" -f $k); $allok=$false; continue }
    $ver = '?'
    try {
        switch ($k) {
            '7z'    { $ver = ((& $p) 2>&1 | Where-Object { $_ -match '7-Zip' } | Select-Object -First 1) }
            'upx'   { $ver = ((& $p --version) 2>&1 | Select-Object -First 1) }
            'capa'  { $ver = ((& $p --version) 2>&1 | Select-Object -First 1) }
            'frida' { $ver = (python -c "import frida;print('frida',frida.__version__)" 2>&1) }
            'angr'  { $ver = (& $p -c "import angr;print('ANGRVER',angr.__version__)" 2>&1 | Select-String 'ANGRVER' | Select-Object -First 1) }
        }
        Write-Output ("  [OK] {0,-6} {1}" -f $k, $p)
        Write-Output ("        -> {0}" -f ($ver -replace '\s+',' ').Trim())
    } catch { Write-Output ("  [跑不起来] {0}  {1}  ({2})" -f $k,$p,$_.Exception.Message); $allok=$false }
}
Write-Output ""

if ($allok) {
    Write-Output "RESULT=OK — 上面是【已装工具】实测运行的绝对路径,skill 里直接用这些路径调用(别依赖裸命令名,PATH 未必刷新)。"
} else {
    Write-Output "RESULT=INCOMPLETE — 部分工具未定位:或【未安装】(见上面缺失项,由用户自己装),或已装但不在已知落点(手动确认路径)。"
}
Write-Output "[可选] 让裸命令名生效:capa 需把 %USERPROFILE%\.local\bin 加入 PATH(uv tool update-shell);upx/7z 同理加各自目录。"
exit 0
