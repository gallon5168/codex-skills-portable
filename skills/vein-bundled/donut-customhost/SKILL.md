---
name: donut-customhost
description: Donut CustomHost — 红队 Shellcode 生成神器。将 .NET EXE/DLL/VBS/JS/XSL 转为位置无关 shellcode，内置 Custom CLR Host 绕过 ETW/AMSI/WLDP、Memory Tracking Evasion、架构感知 ETW Bypass、随机加密混淆。红队后渗透免杀中用于将C#工具(Rubeus/Seatbelt等)转为 shellcode 内存加载。触发词：donut、shellcode、donut-customhost、shellcode生成、exe2shellcode、.NET转shellcode。
version: 1.2.0
---

# Donut CustomHost — Shellcode 生成器

## 概述

Donut CustomHost 是基于 [TheWover/donut](https://github.com/TheWover/donut) v1.2 的增强分支，核心改进：

| 原始 Donut | CustomHost 增强 |
|-----------|----------------|
| 标准 CLR Host | ✅ Custom CLR Host（拦截程序集加载，避开 Fusion 加载器痕迹） |
| - | ✅ Memory Tracking Evasion（自定义内存管理器返回 S_OK，致盲 EDR） |
| 盲 RET Patch | ✅ 架构感知 ETW Bypass（Dynamic Tail Jump，非盲 RET Patch） |
| AMSI Patch | ✅ 移除 AMSI/WLDP Patch（Custom CLR Host 本身绕过了遥测） |
| 正常大小 | ✅ Shellcode 空间 100% 优化（修复对齐填充 bug） |

## 安装位置

| 组件 | 路径 |
|------|------|
| CLI 工具 | `/root/CyberStrikeAI-1.7.6/tools/donut-customhost/donut_cli` |
| Python 封装 | `/root/CyberStrikeAI-1.7.6/tools/donut-customhost/donut_wrapper.py` |
| 动态库 | `/root/CyberStrikeAI-1.7.6/tools/donut-customhost/lib/libdonut.so` |
| C 示例 | `/root/CyberStrikeAI-1.7.6/tools/donut-customhost/examples/main.c` |

## 在渗透测试中调用

```bash
# 方式1: CLI 直接生成
LD_LIBRARY_PATH=/root/CyberStrikeAI-1.7.6/tools/donut-customhost/lib \
  /root/CyberStrikeAI-1.7.6/tools/donut-customhost/donut_cli \
  -f 3 -e 3 -b Rubeus.exe

# 方式2: Python 封装（推荐）
python3 /root/CyberStrikeAI-1.7.6/tools/donut-customhost/donut_wrapper.py \
  Rubeus.exe -o rubeus.bin -b -a 3 -e 3

# 方式3: 我在 exec 中调用
exec(command="python3 /root/CyberStrikeAI-1.7.6/tools/donut-customhost/donut_wrapper.py /tmp/payload.exe -o /tmp/payload.bin -b")
```

## 参数速查

| 参数 | CLI | Python | 说明 |
|------|-----|--------|------|
| 输入文件 | 位置参数 | `input` | .NET exe/dll、VBS、JS、XSL |
| 输出 | - | `-o file` | 默认 loader.bin |
| 架构 | `-f 1/2/3` | `-a 1/2/3` | 1=x86 2=x64 3=双架构 |
| 熵 | `-e 1/2/3` | `-e 1/2/3` | 3=名称随机+加密(避开签名) |
| CustomHost 绕过 | `-b` | `-b` | ETW+AMSI+WLDP+Memory Tracking |
| 类名 | `-c` | `-c` | .NET 类名 |
| 方法 | `-m` | `-m` | 方法名(默认DllMain) |
| 参数 | `-p` | `-p` | 命令行参数 |

## 红队实战示例

```bash
# 1. 将 C# 横向工具 Rubeus 转 shellcode
python3 donut_wrapper.py Rubeus.exe -o rubeus.bin -b -e 3

# 2. 将 Seatbelt 转 shellcode
python3 donut_wrapper.py Seatbelt.exe -o seatbelt.bin -b \
  -p '-group=system -full' -c Seatbelt.Program -m Main

# 3. VBS 脚本转 shellcode
python3 donut_wrapper.py payload.vbs -o payload.bin

# 4. 高熵+ETW绕过（最隐蔽模式）
python3 donut_wrapper.py beacon.exe -o beacon.bin -b -e 3 -a 3
```

生成的 shellcode 可通过：
- Cobalt Strike `execute-assembly`（内存执行）
- 自定义 Loader（如 KhaosLdr / 本机 ai-av-evasion）
- 进程注入直接加载
