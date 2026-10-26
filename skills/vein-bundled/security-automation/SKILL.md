---
name: security-automation
description: 安全自动化深度专业技能：DevSecOps全流程集成、CI/CD安全管道、自动化扫描编排、安全左移实践、从代码提交到生产部署全链路安全自动化
version: 2.0.0
---

# 安全自动化深度技能

## 概述

安全自动化是将安全能力嵌入DevOps流程的核心实践。本技能系统化覆盖**代码提交→构建→测试→部署→运行**全生命周期安全自动化，涵盖SAST/DAST/SCA/容器扫描/合规检查/IaC安全等自动化能力。

## 一、DevSecOps全流程

### 1.1 安全左移模型
```
Plan阶段:  威胁建模 → 安全需求 → 安全设计评审
Code阶段:  IDE安全插件 → Pre-commit Hook → 代码审计
Build阶段: SAST → SCA → 依赖漏洞 → 许可证合规
Test阶段:  DAST → IAST → 渗透测试 → Fuzzing
Deploy阶段: 容器扫描 → IaC审计 → 配置合规
Run阶段:   RASP → WAF → 运行时监控 → 漏洞管理
```

### 1.2 安全管道架构
```yaml
# GitLab CI安全管道示例
stages:
  - security-scan

sast:
  stage: security-scan
  image: semgrep/semgrep
  script:
    - semgrep --config=auto --json -o sast-results.json .
  artifacts:
    reports:
      sast: sast-results.json

dependency-scan:
  stage: security-scan
  image: aquasec/trivy
  script:
    - trivy fs --format json -o deps-results.json .

container-scan:
  stage: security-scan
  image: aquasec/trivy
  script:
    - trivy image --format json -o container-results.json $CI_REGISTRY_IMAGE

secret-scan:
  stage: security-scan
  image: zricethezav/gitleaks
  script:
    - gitleaks detect --source . --report-format json --report-path secrets.json

iac-scan:
  stage: security-scan
  image: bridgecrew/checkov
  script:
    - checkov -d terraform/ -o json > iac-results.json
```

## 二、自动化扫描工具链

### 2.1 SAST（静态应用安全测试）

| 工具 | 语言 | 特点 |
|------|------|------|
| Semgrep | 多语言 | 规则灵活，自定义强 |
| CodeQL | 多语言 | GitHub集成，数据流分析 |
| SonarQube | 多语言 | 代码质量+安全 |
| Bandit | Python | Python专用 |
| Brakeman | Ruby | Rails专用 |
| Gosec | Go | Go专用 |
| ESLint Security | JS/TS | Node.js安全 |

### 2.2 DAST（动态应用安全测试）

| 工具 | 类型 | 特点 |
|------|------|------|
| OWASP ZAP | 开源 | CI/CD集成，API扫描 |
| Burp Suite CI | 商业 | 专业级，REST API |
| Nuclei | 开源 | 模板驱动，快速扫描 |
| Nikto | 开源 | Web服务器扫描 |

### 2.3 SCA（软件成分分析）

| 工具 | 范围 | 特点 |
|------|------|------|
| Trivy | 全面 | 依赖/容器/IaC/密钥 |
| Snyk | 依赖 | 修复建议，PR集成 |
| Dependabot | 依赖 | GitHub原生 |
| OWASP Dependency-Check | 依赖 | NVD数据库 |

### 2.4 容器与IaC安全

| 工具 | 目标 | 特点 |
|------|------|------|
| Trivy | 镜像/依赖 | 多用途扫描 |
| Hadolint | Dockerfile | Dockerfile Lint |
| Checkov | Terraform/K8s | IaC安全策略 |
| tfsec | Terraform | Terraform安全 |
| kube-hunter | K8s | K8s渗透测试 |
| OPA/Gatekeeper | K8s | 策略即代码 |

## 三、密钥泄露防护

### 3.1 Pre-commit Hook
```bash
# gitleaks pre-commit hook
#!/bin/sh
gitleaks protect --staged
if [ $? -ne 0 ]; then
  echo "检测到密钥泄露，提交被拒绝"
  exit 1
fi
```

### 3.2 CI扫描
```yaml
secret-scan:
  script:
    - gitleaks detect --source . --log-opts="--all"
    # 扫描所有Git历史
```

## 四、合规即代码

### 4.1 OPA策略示例
```rego
# K8s Pod安全策略
package kubernetes.admission

deny[msg] {
    input.request.kind.kind == "Pod"
    container := input.request.object.spec.containers[_]
    container.securityContext.privileged == true
    msg := sprintf("容器 %v 不允许使用特权模式", [container.name])
}

deny[msg] {
    input.request.kind.kind == "Pod"
    container := input.request.object.spec.containers[_]
    not container.securityContext.runAsNonRoot
    msg := sprintf("容器 %v 必须以非root运行", [container.name])
}
```

### 4.2 CIS Benchmark自动化
```bash
# Docker CIS Benchmark
docker-bench-security

# K8s CIS Benchmark
kube-bench

# AWS CIS Benchmark
prowler --checks cis
```

## 五、漏洞管理自动化

### 5.1 漏洞管理流程
```
1. 扫描发现 → 自动录入漏洞管理平台
2. 风险评估 → CVSS评分 + 资产权重 = 优先级
3. 分配修复 → 自动分配给责任人
4. 修复验证 → 自动复扫确认修复
5. SLA跟踪 → 超时自动告警
6. 定期报告 → 自动生成安全态势报告
```

### 5.2 漏洞平台集成
```bash
# DefectDojo（开源漏洞管理平台）
# API集成扫描结果
curl -X POST http://defectdojo/api/v2/import-scan/ \
  -H "Authorization: Token $TOKEN" \
  -F "scan_type=Trivy Scan" \
  -F "file=@trivy-results.json"
```

## 六、工具链

```bash
# CI/CD集成
GitLab CI / GitHub Actions / Jenkins  # CI平台
Tekton / Argo CD                      # K8s原生CI/CD

# 扫描编排
DefectDojo        # 漏洞管理平台
ThreadFix         # 漏洞聚合
Faraday           # 渗透测试管理

# 策略引擎
OPA/Gatekeeper    # K8s策略
Kyverno           # K8s策略
Conftest          # 通用策略测试

# 安全监控
Falco             # K8s运行时安全
Wazuh             # 主机安全
```

## 七、测试检查清单

- [ ] CI/CD管道安全扫描集成（SAST/DAST/SCA）
- [ ] Pre-commit Hook（密钥/敏感信息）
- [ ] 容器镜像自动扫描（Trivy/Grype）
- [ ] IaC安全策略（Checkov/OPA）
- [ ] 依赖漏洞自动更新（Dependabot/Renovate）
- [ ] 密钥泄露防护（Git历史/CI日志）
- [ ] 合规即代码（CIS Benchmark/自定义策略）
- [ ] 漏洞管理流程（发现→修复→验证→SLA）
- [ ] 安全指标与报告（漏洞趋势/修复率/SLA达标率）
- [ ] 供应链安全（SBOM/签名验证/来源审计）
