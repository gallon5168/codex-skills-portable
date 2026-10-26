# netcheck.ps1 — 联网可用性检测(供 xiaotao-win-flow 技能调用)
# 分流策略(按目标站分,不是一律走代理):
#   境外站(GitHub 查脱壳工具/仓库、Google) -> 走系统代理,代理优先(自动识别注册表设置)
#   国内 RE 论坛(看雪 bbs.kanxue.com / 吾爱破解 52pojie.cn 查脱壳教程) -> 直连,不走代理
#       且优先用 curl.exe:PowerShell 的 .NET TLS 栈对这两站常握手失败,curl.exe(schannel)直连正常;
#       走境外代理出口 IP 反而会被国内站 TLS 拒绝。
# 只读系统代理,不扫描端口。输出结构化文本供助手解析。

$ErrorActionPreference = 'SilentlyContinue'
$timeoutSec  = 8
$overseasUrl = 'https://github.com'
$domesticUrl = 'https://www.52pojie.cn'

function Test-Url([string]$url, [string]$proxy) {
    try {
        if ($proxy) {
            $r = Invoke-WebRequest -Uri $url -Method Head -TimeoutSec $timeoutSec -Proxy $proxy -UseBasicParsing
        } else {
            $r = Invoke-WebRequest -Uri $url -Method Head -TimeoutSec $timeoutSec -UseBasicParsing
        }
        return $r.StatusCode
    } catch { return 0 }
}

Write-Output "=== netcheck: overseas(GitHub) via proxy / domestic(CN RE forums) direct ==="

# ============ A) 境外:系统代理优先 ============
$reg = 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Internet Settings'
$enable = (Get-ItemProperty -Path $reg -Name ProxyEnable).ProxyEnable
$server = (Get-ItemProperty -Path $reg -Name ProxyServer).ProxyServer

if ($enable -eq 1 -and $server) {
    # ProxyServer 可能是 "host:port" 或 "http=host:port;https=host:port"
    $proxyHostPort = $server
    if ($server -match 'https=([^;]+)') { $proxyHostPort = $Matches[1] }
    elseif ($server -match 'http=([^;]+)') { $proxyHostPort = $Matches[1] }
    $proxyUrl = "http://$proxyHostPort"
    Write-Output "system-proxy: detected server=$server -> testing $overseasUrl via $proxyUrl"
    $code = Test-Url $overseasUrl $proxyUrl
    if ($code -ge 200 -and $code -lt 500) {
        Write-Output "OVERSEAS=PROXY_OK code=$code PROXY=$proxyUrl"
    } else {
        Write-Output "OVERSEAS=PROXY_DOWN code=$code"
        Write-Output "ACTION(overseas)=已识别系统代理 $proxyUrl 但连不通,请确认科学上网工具(VPN/Clash/v2ray)已开启后重试"
    }
} else {
    Write-Output "system-proxy: not configured (ProxyEnable=$enable)"
    $code = Test-Url $overseasUrl $null
    if ($code -ge 200 -and $code -lt 500) {
        Write-Output "OVERSEAS=DIRECT_OK code=$code"
        Write-Output "NOTE(overseas)=无代理直连可达,但查 github/google 外网资料若结果不全或超时,建议开启科学上网工具并设置系统代理"
    } else {
        Write-Output "OVERSEAS=NO_NETWORK code=$code"
        Write-Output "ACTION(overseas)=未检测到系统代理且直连不通,请开启科学上网工具并设置系统代理后重试"
    }
}

# ============ B) 国内 RE 论坛:直连(不走代理),优先 curl.exe ============
$curl = (Get-Command curl.exe -ErrorAction SilentlyContinue).Source
if ($curl) {
    $ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36'
    $code = & $curl -sS -A $ua --max-time $timeoutSec -o NUL -w '%{http_code}' $domesticUrl 2>$null
    if ($code -match '^[23]\d\d$') {
        Write-Output "DOMESTIC=DIRECT_OK code=$code (curl.exe 直连 $domesticUrl)"
        Write-Output "NOTE(domestic)=看雪/吾爱等国内站一律直连,不要走代理;用 curl.exe 而非 Invoke-WebRequest"
    } else {
        Write-Output "DOMESTIC=FAIL code=$code"
        Write-Output "ACTION(domestic)=国内站直连失败(勿走代理);确认本机能直连国内网络,或稍后重试"
    }
} else {
    Write-Output "DOMESTIC=NO_CURL"
    Write-Output "NOTE(domestic)=未找到 curl.exe;PowerShell 的 Invoke-WebRequest 对看雪/吾爱 TLS 握手常失败,请用 curl.exe 直连(勿走代理)"
}
