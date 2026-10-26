---
name: "network-forensics"
description: "网络取证技术，包括Wireshark分析、tcpdump使用、攻击模式识别、PCAP分析和流量日志分析"
version: "1.0.0"
---

# Network Forensics (网络取证)

> 网络取证通过分析网络流量捕获攻击证据，包括恶意通信和数据外泄。

## Wireshark使用

### 常用过滤

```bash
# IP过滤
ip.addr == 192.168.1.100
ip.src == 192.168.1.0/24
ip.dst == 10.0.0.0/8

# 端口过滤
tcp.port == 80
udp.port == 53

# 协议过滤
tcp.flags.syn == 1
http.request.method == "POST"

# 组合过滤
(ip.addr == 192.168.1.100) && (tcp.port == 80)

# 搜索特定内容
tcp contains "password"
http contains "login"
```

### 流量分析

**统计功能：**
- Statistics -> Conversations（会话统计）
- Statistics -> Protocol Hierarchy（协议分级）
- Statistics -> Endpoints（端点列表）
- Statistics -> HTTP Requests（HTTP请求）

**跟踪流：**
- 右键 -> Follow -> TCP Stream
- 右键 -> Follow -> UDP Stream
- 右键 -> Follow -> SSL Stream

## tcpdump使用

### 基础命令

```bash
# 捕获流量
tcpdump -i eth0 -w capture.pcap

# 捕获特定主机
tcpdump -i eth0 host 192.168.1.100 -w capture.pcap

# 捕获特定端口
tcpdump -i eth0 port 80 -w capture.pcap

# 分析捕获文件
tcpdump -r capture.pcap -X
tcpdump -r capture.pcap -A
tcpdump -r capture.pcap -nn
```

### 高级过滤

```bash
# 捕获SYN包（端口扫描）
tcpdump -i eth0 'tcp[13] & 2 != 0'

# 捕获DNS查询
tcpdump -i eth0 port 53

# 捕获HTTP流量
tcpdump -i eth0 port 80

# 捕获恶意IP
tcpdump -i eth0 host <malicious_ip>

# 捕获特定标志位
tcpdump -i eth0 'tcp[tcpflags] == tcp-ack'
```

## 攻击模式识别

### C2通信检测

```
特征：
- 定期的心跳包
- 异常的时间间隔
- 隐蔽的协议（DNS、HTTPS）
- 非标准的端口

检测方法：
- 分析通信频率
- 检查协议异常
- 识别模式匹配
```

### 数据外泄检测

```
特征：
- 大规模数据外传
- 非工作时间传输
- 异常的目标地址
- 可疑的文件传输

检测方法：
- 监控带宽使用
- 分析流量大小
- 检查传输时间
```

### 横向移动检测

```
特征：
- 内部IP扫描
- SMB/WMI通信
- 凭据重用
- 异常登录模式

检测方法：
- 分析内部流量
- 检测扫描行为
- 监控认证日志
```

## PCAP分析示例

### 恶意软件通信分析

```bash
# 过滤可疑DNS
tcpdump -r malware.pcap port 53 -X | grep -A 20 "question"

# 分析C2通信
tcpdump -r malware.pcap -tttt | grep -E "C2|SERVER|payload"

# 提取传输的文件
foremost -i malware.pcap
```

### Webshell通信分析

```bash
# 过滤POST请求
tcpdump -r webshell.pcap -A | grep "POST"

# 分析命令执行
tcpdump -r webshell.pcap -A | grep -E "cmd|powershell|bash"

# 提取恶意请求
tcpdump -r webshell.pcap -w malicious_requests.pcap
```

## 工具对比

| 工具 | 特点 | 适用场景 |
|------|------|----------|
| Wireshark | GUI界面强大 | 深度分析 |
| tcpdump | 命令行高效 | 快速捕获 |
| tshark | 命令行Wireshark | 脚本化分析 |
| NetworkMiner | 自动PCAP分析 | 快速取证 |
| CapLoader | 大流量分析 | 恶意流量检测 |
| Moloch | 大规模流量 | 长期监控 |

## 取证最佳实践

### 证据收集

- [ ] 使用写保护设备
- [ ] 记录捕获时间
- [ ] 保存完整流量
- [ ] 计算哈希值
- [ ] 妥善保存证据

### 分析方法

1. **初步统计**：了解流量概况
2. **协议分析**：识别异常协议
3. **会话重建**：还原攻击链
4. **IOC提取**：发现恶意指标
5. **时间线分析**：还原攻击过程

## 参考资源

- [Wireshark文档](https://www.wireshark.org/docs/)
- [SANS Network Forensics](https://www.sans.org/security-training-incident-response/)
- [Mitre ATT&CK](https://attack.mitre.org/)
