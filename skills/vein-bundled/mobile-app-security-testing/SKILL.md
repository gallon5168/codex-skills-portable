---
name: mobile-app-security-testing
description: 移动应用安全深度测试专业技能：Android/iOS双平台覆盖、静态逆向与动态调试、Hook注入与脱壳、数据存储与传输安全、从逆向分析到漏洞利用完整攻击链
version: 2.0.0
---

# 移动应用安全深度测试技能

## 概述

移动应用是用户数据的入口，攻击面覆盖**客户端安全→数据存储→网络通信→后端API→系统交互**全栈。本技能系统化覆盖**APK/IPA逆向→脱壳调试→Hook注入→数据安全→API安全→系统漏洞**完整攻击链。

## 一、Android安全测试

### 1.1 静态分析
```bash
# APK解包
apktool d app.apk -o output
jadx-gui app.apk  # Java反编译

# AndroidManifest.xml审计
# 关键检查项：
# - android:debuggable="true"
# - android:allowBackup="true"
# - exported组件（Activity/Service/Receiver/Provider）
# - intent-filter（隐式Intent暴露）
# - 自定义权限定义
# - uses-permission过度申请

# 敏感信息检测
grep -r "api_key\|secret\|password\|token" . --include="*.java"
grep -r "http://" . --include="*.java"  # 明文HTTP

# Native库分析
# lib/arm64-v8a/*.so → Ghidra/IDA逆向
# JNI函数调用审计
```

### 1.2 动态分析与Hook
```bash
# Frida Hook（推荐）
frida -U -f com.target.app -l hook.js

# 常用Hook脚本
# SSL Pinning绕过
Java.perform(function() {
    var TrustManagerImpl = Java.use("com.android.org.conscrypt.TrustManagerImpl");
    TrustManagerImpl.verifyChain.implementation = function() {
        return arguments[0];
    };
});

# 加密函数Hook
Java.perform(function() {
    var Cipher = Java.use("javax.crypto.Cipher");
    Cipher.getInstance.overload("java.lang.String").implementation = function(algo) {
        console.log("[*] Cipher algo: " + algo);
        return this.getInstance(algo);
    };
});

# Objection（免root Hook）
objection -g com.target.app explore
android sslpinning disable
android keystore list

# Xposed/Magisk模块（持久化Hook）
```

### 1.3 数据存储安全
```bash
# SharedPreferences
cat /data/data/com.target/shared_prefs/*.xml

# SQLite数据库
sqlite3 /data/data/com.target/databases/*.db
.tables
SELECT * FROM users;

# 内部存储
ls -la /data/data/com.target/files/
ls -la /data/data/com.target/cache/

# 外部存储
ls -la /sdcard/Android/data/com.target/

# 备份提取
adb backup -f backup.ab com.target.app
abe unpack backup.ab backup.tar

# KeyStore分析
# 检查密钥是否可导出、是否硬件保护
```

### 1.4 网络通信安全
```
检查项：
1. SSL/TLS版本（TLS 1.2+）
2. 证书验证（SSL Pinning）
3. 明文传输（HTTP/明文字段）
4. 敏感数据泄露（URL参数/日志）
5. 中间人攻击（证书信任）
6. WebView混合内容
```

### 1.5 组件导出审计
```java
// 导出的Activity → 直接启动
adb shell am start -n com.target/.ExportedActivity -e key value

// 导出的Service → 直接调用
adb shell am startservice -n com.target/.ExportedService

// 导出的BroadcastReceiver → 发送广播
adb shell am broadcast -a com.target.RECEIVER -e data "malicious"

// ContentProvider → SQL注入/文件泄露
adb shell content query --uri content://com.target.provider/data
```

### 1.6 脱壳技术
```
加固壳识别：
- 腾讯乐固/360加固/梆梆加固/爱加密/网易易盾

脱壳方法：
1. Frida动态脱壳（dump内存中的dex）
2. Xposed模块（BlackDex/DexExtractor）
3. 模拟器脱壳（夜神/雷电+脱壳工具）
4. 静态脱壳（特定壳解密算法逆向）
```

## 二、iOS安全测试

### 2.1 静态分析
```bash
# IPA解包
unzip app.ipa -d output

# Mach-O分析
otool -l app_binary  # 加载命令
class-dump app_binary > classes.h  # OC类导出

# Info.plist审计
# URL Schemes / App Transport Security / 权限描述

# 加密检测
otool -l app_binary | grep -A4 LC_ENCRYPTION_INFO  # 是否加密
```

### 2.2 动态分析（越狱设备）
```bash
# Frida
frida -U -f com.target.app -l hook.js

# SSL Pinning绕过
# TrustKit / NSURLSession / AFNetworking Hook

# Cycript/ Substitute（运行时修改）
cycript -p PID
[UIApplication sharedApplication].keyWindow

# 数据存储
ls ~/Library/Application\ Support/
ls ~/Library/Preferences/
ls ~/Documents/

# Keychain提取
keychain_dump  # 越狱设备
# 检查kSecAttrAccessible属性
```

### 2.3 iOS特有攻击面
```
- URL Scheme劫持
- Universal Link欺骗
- 剪贴板数据泄露（UIPasteboard）
- 键盘缓存（autocorrection）
- 截屏保护（敏感界面）
- Jailbreak检测绕过
- FairPlay DRM绕过
```

## 三、通用攻击面

### 3.1 后端API安全
```
移动端API同样面临Web漏洞：
- 认证绕过（Token泄露/JWT攻击）
- IDOR（用户ID可预测）
- 参数篡改（价格/数量）
- 接口未授权访问
- 速率限制缺失
- GraphQL注入/过度查询
```

### 3.2 WebView安全
```
Android WebView:
- setJavaScriptEnabled(true) → XSS
- addJavascriptInterface → RCE（API<17）
- setAllowFileAccess → 本地文件读取
- file:///协议 → 本地文件遍历
- shouldOverrideUrlLoading → 协议劫持

iOS WKWebView:
- evaluateJavaScript → XSS
- WKURLSchemeHandler → 自定义协议
- messageHandlers → JS-Native桥接
```

## 四、工具链

```bash
# Android
jadx                    # 反编译
apktool                 # APK解包/重打包
Frida                   # 动态Hook
Objection               # 免root评估
drozer                  # 组件攻击
MobSF                   # 自动化分析
DexGuard/ProGuard       # 混淆分析

# iOS
class-dump              # OC类导出
Hopper/IDA              # 逆向分析
Frida                   # 动态Hook
Objection               # 越狱评估
iMazing                 # IPA管理
Libimobiledevice        # 设备通信

# 通用
Burp Suite              # HTTP代理/拦截
MobSF                   # 自动化移动安全
QARK                    # 快速审计
Needle                  # iOS渗透框架
```

## 五、测试检查清单

- [ ] APK/IPA静态分析（反编译/Manifest/权限）
- [ ] 敏感信息检测（硬编码密钥/Token/密码）
- [ ] 数据存储安全（明文/加密/KeyStore）
- [ ] 网络通信安全（TLS/Pinning/明文）
- [ ] 组件导出审计（Intent注入/数据泄露）
- [ ] SSL Pinning绕过与MITM
- [ ] Hook与动态调试
- [ ] WebView安全（XSS/文件访问/JS桥接）
- [ ] 后端API安全（认证/IDOR/注入）
- [ ] 加固与脱壳检测
