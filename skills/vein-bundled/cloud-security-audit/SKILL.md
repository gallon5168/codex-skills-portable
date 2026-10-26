---
name: cloud-security-audit
description: 云安全深度审计专业技能：AWS/Azure/GCP/阿里云全平台覆盖、IAM滥用与提权、云原生攻击面、容器逃逸、元数据SSRF、存储桶劫持、从侦察到接管完整攻击链
version: 2.0.0
---

# 云安全深度审计技能

## 概述

云环境是现代化基础设施的核心，攻击面涵盖IaaS/PaaS/SaaS多层。本技能系统化覆盖**云资产枚举→身份滥用→权限提升→横向移动→数据窃取→持久化**完整攻击链，覆盖AWS/Azure/GCP/阿里云四大平台。

## 一、云资产枚举与攻击面映射

### 1.1 侦察阶段

**被动枚举：**
| 技术 | 工具 | 目标 |
|------|------|------|
| 子域名枚举 | Amass/Subfinder/CloudBrute | 发现云服务端点 |
| 证书透明度 | crt.sh/Censys | 发现云域名 |
| DNS枚举 | DNSRecon/DNSDumpster | CNAME到云服务 |
| 搜索引擎 | GoogleHacking/Shodan | 暴露的云资源 |
| GitHub泄露 | git-hound/truffleHog | AK/SK/Token |
| 云指纹识别 | CloudEnum/cloudbrute | 识别云服务商 |

**主动枚举：**
```bash
# AWS S3 Bucket枚举
aws s3 ls s3://bucket-name --no-sign-request
# Azure Storage枚举
az storage blob list --container-name container --account-name account
# GCP Bucket枚举
gsutil ls gs://bucket-name
```

### 1.2 云平台攻击面矩阵

| 攻击面 | AWS | Azure | GCP | 阿里云 |
|--------|-----|-------|-----|--------|
| 身份服务 | IAM | Azure AD | Cloud IAM | RAM |
| 对象存储 | S3 | Blob Storage | Cloud Storage | OSS |
| 计算 | EC2/Lambda | VM/Functions | GCE/Functions | ECS/FC |
| 数据库 | RDS/DynamoDB | SQL DB | Cloud SQL | RDS |
| 容器 | EKS/ECS | AKS | GKE | ACK |
| 消息队列 | SQS/SNS | Service Bus | Pub/Sub | MNS |
| Serverless | Lambda | Functions | Cloud Functions | FC |
| CDN | CloudFront | CDN | Cloud CDN | CDN |

## 二、IAM滥用与权限提升

### 2.1 AWS IAM攻击

**AK/SK泄露利用：**
```bash
# 枚举当前权限
aws sts get-caller-identity
aws iam list-attached-user-policies --user-name $(aws sts get-caller-identity --query Arn --output text | cut -d/ -f2)
aws iam simulate-principal-policy --policy-source-arn arn:aws:iam::123:user/user --action-names "*"

# 权限提升路径
# iam:CreateAccessKey → 接管其他用户
# iam:PutUserPolicy → 给自己加管理员权限
# sts:AssumeRole → 角色扮演提权
# lambda:CreateFunction + lambda:InvokeFunction → Lambda RCE
# ec2:RunInstances + iam:PassRole → 创建带角色的实例
```

**IAM Privilege Escalation 完整路径：**
```
1. iam:CreatePolicyVersion → 创建新策略版本覆盖原策略
2. iam:SetDefaultPolicyVersion → 切换到更宽松的旧版本
3. iam:CreateAccessKey → 为其他用户创建AK
4. iam:CreateLoginProfile → 为其他用户设置密码
5. iam:UpdateLoginProfile → 重置其他用户密码
6. iam:AttachUserPolicy/AttachGroupPolicy/AttachRolePolicy
7. iam:PutUserPolicy/PutGroupPolicy/PutRolePolicy
8. iam:AddUserToGroup → 加入高权限组
9. iam:UpdateAssumeRolePolicy → 修改角色信任策略
10. sts:AssumeRole → 扮演高权限角色
```

### 2.2 Azure AD攻击

**Service Principal滥用：**
```bash
# 枚举Service Principal
az ad sp list --all --query "[?appDisplayName=='target']"

# 凭据泄露利用
az login --service-principal -u APP_ID -p SECRET --tenant TENANT_ID

# 权限提升
# Application.ReadWrite.All → 修改应用权限
# RoleManagement.ReadWrite.Directory → 提升目录角色
# AppRoleAssignment.ReadWrite.All → 分配应用角色
```

### 2.3 GCP IAM攻击
```bash
# 枚举权限
gcloud projects get-iam-policy PROJECT_ID
gcloud iam service-accounts list --project=PROJECT_ID

# 服务账号Key利用
gcloud auth activate-service-account --key-file=key.json

# 权限提升
# iam.serviceAccounts.actAs → 模拟服务账号
# iam.serviceAccountKeys.create → 创建服务账号密钥
# iam.roles.update → 修改自定义角色
```

## 三、云存储安全

### 3.1 S3 Bucket攻击

**Bucket枚举与劫持：**
```bash
# 未授权访问检测
aws s3 ls s3://target-bucket --no-sign-request

# Bucket策略分析
aws s3api get-bucket-policy --bucket target-bucket

# ACL分析
aws s3api get-bucket-acl --bucket target-bucket

# 常见误配置
# - s3:GetObject 公开 → 数据泄露
# - s3:PutObject 公开 → 数据篡改/钓鱼
# - s3:ListBucket 公开 → 文件枚举
# - s3:PutBucketPolicy → 策略篡改
# - Bucket未删除 → Dangling DNS劫持
```

**Bucket命名接管（Dangling DNS）：**
```
1. 域名CNAME指向已删除的S3 Bucket
2. 创建同名Bucket接管
3. 实现钓鱼/内容注入
```

### 3.2 Azure Blob Storage
```bash
# 公开访问检测
curl https://account.blob.core.windows.net/container?restype=container&comp=list

# SAS Token泄露利用
az storage blob list --container-name container --sas-token "sv=...&sig=..."
```

## 四、元数据服务攻击（SSRF→凭据窃取）

### 4.1 云元数据端点

| 云平台 | 元数据地址 | 凭据路径 |
|--------|----------|---------|
| AWS | http://169.254.169.254 | /latest/meta-data/iam/security-credentials/ROLE |
| Azure | http://169.254.169.254 | /metadata/identity/oauth2/token?api-version=2018-02-01&resource=RESOURCE |
| GCP | http://metadata.google.internal | /computeMetadata/v1/instance/service-accounts/default/token |
| 阿里云 | http://100.100.100.200 | /latest/meta-data/ram/security-credentials/ROLE |

### 4.2 SSRF利用链
```
1. 发现SSRF漏洞
2. 请求元数据端点获取临时凭据
3. 使用临时凭据调用云API
4. 提升权限/横向移动/数据窃取
```

### 4.3 IMDSv2绕过（AWS）
```bash
# IMDSv2需要PUT请求获取Token
# 如果SSRF支持PUT方法：
curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600"
# 然后用Token访问
curl "http://169.254.169.254/latest/meta-data/" -H "X-aws-ec2-metadata-token: TOKEN"
```

## 五、容器与K8s攻击

### 5.1 容器逃逸路径
```
1. 特权容器 → 直接访问宿主机设备
2. 内核漏洞（CVE-2022-0847/CVE-2024-1086）→ 内核级逃逸
3. 挂载宿主机文件系统 → 读写宿主机
4. Docker Socket挂载 → 创建特权容器
5. CAP_SYS_ADMIN → mount逃逸
6. PID namespace共享 → nsenter逃逸
```

### 5.2 Kubernetes攻击
```bash
# Service Account Token泄露
cat /var/run/secrets/kubernetes.io/serviceaccount/token

# API Server未授权访问
curl -k https://k8s-api:6443/api/v1/pods -H "Authorization: Bearer TOKEN"

# RBAC审计
kubectl get clusterrolebindings -o json
kubectl auth can-i --list

# K8s横向移动
# 1. 窃取ServiceAccount Token
# 2. 创建特权Pod挂载宿主机
# 3. 通过API Server创建恶意工作负载
# 4. 利用NetworkPolicy缺陷横向移动
```

## 六、Serverless与Lambda攻击

### 6.1 Lambda安全
```
攻击面：
- 环境变量泄露（包含AK/SK）
- 过度权限的IAM角色
- 依赖包漏洞（供应链攻击）
- 事件源注入（S3/SQS/API Gateway触发器）
- 临时凭据窃取（/tmp目录残留）
- Lambda层投毒
```

## 七、工具链

```bash
# 云安全审计
prowler                    # AWS/Azure/GCP安全审计
ScoutSuite                 # 多云安全审计
CloudSploit                # AWS配置审计
pacu                       # AWS攻击框架

# 枚举工具
CloudBrute                 # 云资产枚举
cloud_enum                 # 多云枚举
cartography                # 资产图谱

# 利用工具
aws-consoler               # AK转Console登录
leonid                     # Azure AD攻击
gcp-iam-collector          # GCP IAM分析

# K8s安全
kube-hunter                # K8s渗透测试
kubeaudit                  # K8s审计
peirates                   # K8s渗透工具集
kdigger                    # K8s环境探测
```

## 八、测试检查清单

- [ ] 云资产完整枚举（所有服务、所有区域）
- [ ] IAM策略审计（过度权限、未使用权限）
- [ ] AK/SK泄露检测（GitHub/日志/配置文件）
- [ ] 对象存储权限审计（公开访问、Bucket策略）
- [ ] 元数据服务防护（IMDSv2、网络隔离）
- [ ] 网络安全审计（安全组、NACL、VPC对等连接）
- [ ] 日志与监控（CloudTrail/ActionTrail完整性）
- [ ] 加密与密钥管理（KMS、数据加密）
- [ ] 容器与K8s安全（镜像扫描、RBAC、网络策略）
- [ ] Serverless安全（Lambda权限、事件注入）

## 九、修复建议

- **最小权限原则**：IAM策略仅授予必要权限
- **启用MFA**：所有管理员和敏感操作强制MFA
- **私有化存储**：对象存储禁止公开访问
- **IMDSv2**：强制使用IMDSv2并要求Token
- **日志完整性**：启用CloudTrail/Activity Log全区域审计
- **密钥轮转**：定期轮转AK/SK，使用IAM角色替代
- **网络隔离**：VPC私有子网、安全组最小开放
- **合规框架**：遵循CIS Benchmark for Cloud
