---
name: deepcode-integration
description: DeepCode(HKUDS)多Agent编程系统集成技能。当需要生成复杂代码(exploit/POC/Web工具/后端API)时，通过subprocess调用DeepCode CLI完成代码生成，再由本技能将结果集成到安全测试流程中。触发词：deepcode、深度代码、Paper2Code、Text2Web、Text2Backend、多Agent编程、复杂代码生成。
metadata:
  short-description: 集成HKUDS/DeepCode多Agent编程系统
  repo: https://github.com/HKUDS/DeepCode
  stars: 15898
  categories: code-generation,multi-agent,integration,exploit-dev
  requires: python3.10+, llm-api-key, deepcode-installed
version: "1.0"
author: CyberStrikeAI
---

# DeepCode 集成 — 多 Agent 编程系统

## DeepCode 是什么

港大出品(⭐15,898)，一个开源的 Multi-Agent 编码系统：
- 多个编码 Agent 并行协作，通过共享记忆和工具推进任务
- 内置安全沙箱，Agent 可以安全地执行代码验证结果
- 支持 Paper2Code / Text2Web / Text2Backend / AgenticChat
- 通过 MCP 协议连接外部工具（文件系统、Shell、数据库、Web）

## 安装 (在你的机器上)

```bash
# 1. 克隆仓库
git clone https://github.com/HKUDS/DeepCode.git
cd DeepCode

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置 API Key
cp deepcode_config.json.example deepcode_config.json
# 编辑 deepcode_config.json，填入你的 LLM API key:
# - OpenAI: "openai/your-key"
# - DeepSeek: "deepseek/your-key"  
# - OpenRouter: "openrouter/your-key"
# - Ollama本地: "ollama/"

# 4. 测试
python deepcode.py --help
```

## 配置示例 (deepcode_config.json)

```json
{
    "model_used": [
        {
            "model_id": 1,
            "provider": "deepseek",
            "model_name": "deepseek-chat",
            "api_key": "sk-your-deepseek-key",
            "temperature": 0.5,
            "top_p": 0.9
        }
    ],
    "models_config": {
        "deepseek": {
            "name": "DeepSeek",
            "base_url": "https://api.deepseek.com",
            "api_type": "openai",
            "api_key_name": "api_key",
            "default_model": "deepseek-chat",
            "supported_models": [
                "deepseek-chat",
                "deepseek-reasoner"
            ]
        }
    },
    "default_provider": "deepseek",
    "workspace_dir": "./workspace",
    "output_dir": "./output"
}
```

## 与 CyberStrikeAI 的集成模式

### 模式 1: 子进程调用（推荐）

```python
# CyberStrikeAI 调用 DeepCode 生成 exploit/POC/工具
import subprocess, json

def deepcode_generate(task_description: str, mode: str = "code") -> str:
    """
    mode: "code" = 纯代码 | "web" = Web应用 | "backend" = 后端API
    """
    result = subprocess.run(
        ['python', '/path/to/DeepCode/deepcode.py',
         '--task', task_description,
         '--mode', mode,
         '--output-dir', './deepcode_output/'],
        capture_output=True, text=True, timeout=600
    )
    return result.stdout

# 示例: 生成 CVE-2021-44228 利用 POC
poc_code = deepcode_generate(
    "Write a Python POC for Log4Shell (CVE-2021-44228) that: "
    "1. Starts a malicious LDAP server on port 1389 "
    "2. Serves a payload that executes reverse shell "
    "3. Sends the JNDI injection string to the target",
    mode="code"
)
print(poc_code)
```

### 模式 2: CyberStrikeAI 指定规格 → DeepCode 生成代码 → CyberStrikeAI 执行

```bash
# Step 1: CyberStrikeAI 分析目标，确定需要什么代码
# Step 2: CyberStrikeAI 写需求规格 → deepcode_spec.json
# Step 3: 调用 DeepCode 生成代码
python /path/to/DeepCode/deepcode.py \
    --spec deepcode_spec.json \
    --mode code \
    --output ./generated/

# Step 4: CyberStrikeAI 读取生成结果并执行
```

### 模式 3: 交互式协作

```python
# CyberStrikeAI 在渗透测试中实时调用 DeepCode
def exploit_dev_pipeline(target_info: dict) -> dict:
    """
    完整 exploit 开发流水线:
    1. 根据目标指纹搜索已知 CVE (通过 searchsploit)
    2. 调用 DeepCode 生成定制 POC
    3. 调用 DeepCode 生成免杀 shellcode
    4. CyberStrikeAI 整合执行
    """
    results = {}
    
    # Phase 1: CVE 搜索
    cve_list = search_exploit_db(target_info['fingerprint'])
    
    # Phase 2: 代码生成
    for cve in cve_list[:3]:
        spec = f"""
        Write a Python exploit for {cve['id']} ({cve['description']}).
        Target: {target_info['os']} {target_info['version']}
        Requirements:
        - Must use only Python standard library
        - Must have error handling
        - Must output success/failure status
        - Must NOT require external dependencies
        """
        code = deepcode_generate(spec)
        results[cve['id']] = code
    
    return results
```

## 实战场景

### 场景 1: 生成定制 ROP 链

```
CyberStrikeAI: "目标是 Ubuntu 22.04, libc 2.35, NX+ASLR 开启, 无 PIE"
DeepCode:      "需要找 pop rdi;ret gadget + system + /bin/sh 字符串偏移"
               → 生成 Python ROP 链构建代码
               → 生成最终 exploit.py
```

### 场景 2: WAF 绕过 Payload 定制

```
CyberStrikeAI: "目标 WAF 规则: 过滤 SELECT/UNION/'/1=1, 但允许 /\*\*/ 注释"
DeepCode:      → 生成多编码层 SQL 注入 payload
               → 生成 Python 自动化发包脚本 (带 WAF 探测)
```

### 场景 3: 免杀 Loader 生成

```
CyberStrikeAI: "需绕过 Windows Defender + CrowdStrike, C2 是 HTTPS 443"
DeepCode:      → 生成 C 语言 shellcode loader
               → 含 XOR 加密 + 分段加载 + 回调执行
               → 生成编译脚本和部署说明
```

### 场景 4: 内网横向移动工具

```
CyberStrikeAI: "需要 Python 实现的 SMB 横向移动, 用已获取的 hash 批量执行命令"
DeepCode:      → 生成 impacket 风格的 SMB 执行代码
               → 带多线程、日志、结果汇总
```

## DeepCode 的 Agent 架构

```
┌────────────────────────────────────────────────────┐
│                   DeepCode Core                     │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐            │
│  │ Agent 1 │  │ Agent 2 │  │ Agent 3 │  ...       │
│  │ Coder   │  │Tester   │  │Planner  │            │
│  └────┬────┘  └────┬────┘  └────┬────┘            │
│       │            │            │                  │
│       └────────────┼────────────┘                  │
│                    ▼                               │
│          ┌─────────────────┐                       │
│          │  Shared Memory   │                       │
│          │  + Tool Manager  │                       │
│          └────────┬────────┘                       │
│                   │                                │
│         ┌─────────┼─────────┐                      │
│         ▼         ▼         ▼                      │
│    ┌──────┐  ┌──────┐  ┌──────┐                   │
│    │ MCP  │  │ MCP  │  │ MCP  │                   │
│    │ File │  │Shell │  │ Web  │  ...              │
│    └──────┘  └──────┘  └──────┘                   │
└────────────────────────────────────────────────────┘
        ▲                    ▲
        │   CyberStrikeAI    │
        │   通过 subprocess   │
        │   调用 DeepCode     │
        └────────────────────┘
```

## 支持的 LLM 供应商

DeepCode 通过 litellm 支持 100+ 供应商:

```
OpenAI     → gpt-4o, gpt-4.1
DeepSeek   → deepseek-chat, deepseek-reasoner  ← 推荐(便宜+强编码)
Anthropic  → claude-3.5-sonnet, claude-opus
OpenRouter → 统一网关(按需路由)
Ollama     → 本地部署(llama3, codestral, qwen) ← 免费
通义千问   → qwen-max  ← 国产
GLM        → glm-4     ← 国产
Moonshot   → moonshot-v1
```

## 常见问题

```bash
# Q: DeepCode 需要多少内存?
# A: 自身占用 < 500MB, 但推荐 16GB+ (代码生成可能产生大量中间文件)

# Q: 生成速度?
# A: DeepSeek-chat: 500行代码约30-60秒; 复杂项目 3-10 分钟

# Q: 安全沙箱?
# A: DeepCode 内置 subprocess 沙箱, 生成的代码在执行前会审查

# Q: 和 GitHub Copilot 的区别?
# A: Copilot 是行级补全, DeepCode 是多Agent项目级生成
```
