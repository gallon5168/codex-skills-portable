---
name: "disk-forensics"
description: "磁盘取证技术，包括Autopsy使用、文件系统分析、文件恢复和注册表分析"
version: "1.0.0"
---

# Disk Forensics (磁盘取证)

> 磁盘取证是数字取证的基础技术，通过分析磁盘镜像获取证据。

## 概述

磁盘取证允许安全分析师从存储设备中恢复数据、分析文件系统和识别恶意软件。

## Autopsy使用

### 基本流程

1. **创建新案例**
2. **添加数据源**
3. **选择分析模块**
4. **浏览文件系统**
5. **标记重要文件**
6. **生成报告**

### 常用模块

| 模块 | 功能 |
|------|------|
| Keyword Search | 关键词搜索 |
| File Type Sorting | 文件类型分类 |
| EXIF Metadata | EXIF元数据分析 |
| Email Parser | 邮件解析 |
| Registry Parser | 注册表分析 |
| Web Search | 网络搜索 |
| Hash Lookup | 哈希比对 |

## FTK Imager使用

### 功能

- 磁盘镜像获取
- 只读访问
- 内存获取
- 哈希计算
- 取证报告

### 常用命令

```bash
# 获取磁盘镜像
ftkimager /dev/sda output --e01

# 内存获取
ftkimager --memdump memory.raw

# 验证镜像
ftkimager --verify image.E01
```

## 文件恢复

### foremost使用

```bash
# 恢复所有类型文件
foremost -i disk.dd -o recovered/

# 恢复特定类型
foremost -i disk.dd -o recovered/ -t jpg,gif,png

# 恢复Office文档
foremost -i disk.dd -o recovered/ -t doc,xls,ppt
```

### extundelete使用

```bash
# 恢复删除的文件
extundelete /dev/sda1 --restore-all

# 恢复特定文件
extundelete /dev/sda1 --restore-file deleted_file.txt

# 恢复目录
extundelete /dev/sda1 --restore-directory deleted_dir
```

## 注册表分析

### 注册表 hives

| Hive | 内容 |
|------|------|
| HKLM\SYSTEM | 系统配置 |
| HKLM\SAM | 用户账户 |
| HKLM\SECURITY | 安全策略 |
| HKLM\SOFTWARE | 软件配置 |
| HKCU | 用户配置 |

### 常用分析点

```bash
# 用户登录历史
HKCU\Software\Microsoft\Windows\Run

# 系统启动项
HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run

# 网络配置
HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters

# USB设备历史
HKLM\SYSTEM\CurrentControlSet\Enum\USBSTOR
```

## PE文件分析

### pecheck使用

```bash
# 分析PE文件
pecheck suspicious.exe

# 检查节
pecheck -s suspicious.exe

# 检查导入表
pecheck -i suspicious.exe
```

### 字符串分析

```bash
# 提取所有字符串
strings suspicious.exe

# 提取ASCII字符串
strings -a suspicious.exe

# 提取Unicode字符串
strings -u suspicious.exe

# 提取特定长度字符串
strings -n 10 suspicious.exe
```

## 取证最佳实践

### 证据收集

- [ ] 使用写保护设备
- [ ] 保持证据完整性
- [ ] 记录所有操作
- [ ] 验证哈希值
- [ ] 妥善保存证据

### 分析方法

1. **初步评估**：了解证据概况
2. **文件恢复**：恢复删除数据
3. **时间线分析**：重建事件
4. **IOC提取**：发现恶意指标
5. **报告生成**：记录发现

## 参考资源

- [Autopsy官方文档](https://www.sleuthkit.org/autopsy/docs.php)
- [The Sleuth Kit](https://www.sleuthkit.org/)
- [SANS Digital Forensics](https://www.sans.org/security-training-incident-response/)
