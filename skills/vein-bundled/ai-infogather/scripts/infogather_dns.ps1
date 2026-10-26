<#
.SYNOPSIS
    infogather_dns.ps1 — 批量 DNS 解析工具
.DESCRIPTION
    从文件或参数读取域名列表，批量解析 A/MX/NS/CNAME 记录，输出 CSV。
.PARAMETER InputFile
    域名列表文件，每行一个域名。
.PARAMETER Domains
    逗号分隔的域名列表（与 InputFile 二选一）。
.PARAMETER OutputFile
    输出 CSV 路径（默认桌面）。
.PARAMETER RecordType
    解析记录类型：A / MX / NS / ALL（默认 ALL）。
.EXAMPLE
    .\infogather_dns.ps1 -InputFile domains.txt -OutputFile result.csv
.EXAMPLE
    .\infogather_dns.ps1 -Domains "www.example.com,mail.example.com" -RecordType MX
#>

param(
    [string]$InputFile,
    [string]$Domains,
    [string]$OutputFile,
    [ValidateSet("A","MX","NS","CNAME","ALL")]
    [string]$RecordType = "ALL"
)

# ── 获取域名列表 ──
$domainList = @()
if ($InputFile -and (Test-Path $InputFile)) {
    $domainList = Get-Content $InputFile | Where-Object { $_.Trim() -ne "" }
}
elseif ($Domains) {
    $domainList = $Domains -split "," | ForEach-Object { $_.Trim() }
}
else {
    Write-Host "[-] 请提供 -InputFile 或 -Domains" -ForegroundColor Red
    exit 1
}

# ── 默认输出到桌面 ──
if (-not $OutputFile) {
    $desktop = [Environment]::GetFolderPath("Desktop")
    $timestamp = Get-Date -Format "yyyyMMdd_HHmm"
    $OutputFile = Join-Path $desktop "infogather_dns_$timestamp.csv"
}

# ── 解析函数 ──
function Resolve-DnsRecord {
    param($Domain, $Type)
    $result = @()
    try {
        $records = [System.Net.Dns]::GetHostEntry($Domain)
        if ($Type -eq "A" -or $Type -eq "ALL") {
            foreach ($ip in $records.AddressList) {
                if ($ip.AddressFamily -eq "InterNetwork") {
                    $result += [PSCustomObject]@{
                        域名     = $Domain
                        记录类型 = "A"
                        值       = $ip.IPAddressToString
                    }
                }
            }
        }
    }
    catch { $result += [PSCustomObject]@{ 域名=$Domain; 记录类型="A"; 值="解析失败" } }

    # MX
    if ($Type -eq "MX" -or $Type -eq "ALL") {
        try {
            $mxRecords = Resolve-DnsName -Name $Domain -Type MX -ErrorAction Stop
            foreach ($mx in $mxRecords) {
                $result += [PSCustomObject]@{
                    域名     = $Domain
                    记录类型 = "MX"
                    值       = "$($mx.NameExchange) [优先级 $($mx.Preference)]"
                }
            }
        }
        catch { if ($Type -eq "MX") { $result += [PSCustomObject]@{ 域名=$Domain; 记录类型="MX"; 值="解析失败" } } }
    }

    # NS
    if ($Type -eq "NS" -or $Type -eq "ALL") {
        try {
            $nsRecords = Resolve-DnsName -Name $Domain -Type NS -ErrorAction Stop
            foreach ($ns in $nsRecords) {
                $result += [PSCustomObject]@{
                    域名     = $Domain
                    记录类型 = "NS"
                    值       = $ns.NameHost
                }
            }
        }
        catch { if ($Type -eq "NS") { $result += [PSCustomObject]@{ 域名=$Domain; 记录类型="NS"; 值="解析失败" } } }
    }

    # CNAME
    if ($Type -eq "CNAME" -or $Type -eq "ALL") {
        try {
            $cnameRecords = Resolve-DnsName -Name $Domain -Type CNAME -ErrorAction Stop
            foreach ($cn in $cnameRecords) {
                $result += [PSCustomObject]@{
                    域名     = $Domain
                    记录类型 = "CNAME"
                    值       = $cn.NameHost
                }
            }
        }
        catch {}
    }

    return $result
}

# ── 执行解析 ──
$allResults = @()
foreach ($domain in $domainList) {
    Write-Host "[*] 解析: $domain" -ForegroundColor Cyan
    $allResults += Resolve-DnsRecord -Domain $domain -Type $RecordType
    Start-Sleep -Milliseconds 200  # 避免频率限制
}

# ── 输出 ──
$allResults | Export-Csv -Path $OutputFile -NoTypeInformation -Encoding utf8
Write-Host "[+] 完成！共解析 $($domainList.Count) 个域名，$($allResults.Count) 条记录" -ForegroundColor Green
Write-Host "[+] 输出: $OutputFile" -ForegroundColor Green

# 控制台摘要
$allResults | Format-Table -AutoSize | Out-Host
