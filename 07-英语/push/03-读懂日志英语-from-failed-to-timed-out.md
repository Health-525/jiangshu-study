# 读懂日志的英语：从 “failed” 到 “timed out”

同样是“出错”，日志里用的动词/形容词不一样，含义差很多。

这篇做一个高频速查：看到词就能大概判断**发生在谁那一侧**、**大概率怎么排查**。

---

## 1）最常见的 10 个错误表达

### **failed**（失败，最泛）
- 只告诉你“没成功”，原因要看上下文。

### **timed out**（超时）
- 常见原因：网络不通、对方太慢、队列堆积。
- 典型搭配：request timed out / connection timed out

### **denied**（被拒绝：权限/策略）
- 典型搭配：permission denied / access denied

### **refused**（对方拒绝连接）
- 典型搭配：connection refused
- 常见原因：端口没开、服务没起来、security group/防火墙。

### **unavailable**（不可用）
- 典型搭配：service unavailable (HTTP 503)

### **not found**（不存在）
- 典型搭配：404 not found / key not found

### **invalid**（无效/不合法）
- 典型搭配：invalid argument / invalid token

### **throttled / rate-limited**（被限流）
- 典型搭配：request was throttled / rate limit exceeded

### **corrupted**（损坏）
- 典型搭配：corrupted data / corrupted file

### **exceeded**（超过限制）
- 典型搭配：quota exceeded / limit exceeded

---

## 2）看到词就能做的“第一反应”
- timed out → 先看**延迟/队列/依赖服务**，再看网络
- denied → 先看**权限/IAM/ACL/鉴权**
- refused → 先看**端口/进程/防火墙/安全组**
- throttled → 先看**QPS/配额/限流策略**

---

## 3）例句（写工单很顺）
- The request **timed out** after 30s.
- The API returned **503 Service Unavailable**.
- Access was **denied** due to missing permissions.
- The connection was **refused** by the upstream service.
- We were **rate-limited** by the provider.

---

把你最近的一条报错贴出来（含关键一行日志即可），我帮你判断它更像是：权限/网络/依赖变慢/限流/参数不合法。
