# 你以为的 bug 只是开始：缺陷分类英语速查

写工单、看告警、读复盘时，经常会看到一堆“看起来都像问题”的词：bug / issue / incident / outage…

它们不只是“同义词”，很多场景下用错词会让沟通成本暴涨。

---

## 1）最常见的 8 个词（按场景理解）

### **bug**
- 含义：代码层面的错误（实现不符合预期）
- 例：null pointer、边界条件没处理

### **defect**
- 含义：更正式的“缺陷”（测试/质量语境常用）
- 例：QA 报的 defect、缺陷单

### **issue**
- 含义：泛指“一个需要跟踪/解决的问题”（最通用）
- 例：GitHub issue、Jira issue

### **incident**
- 含义：线上事件（服务异常/告警触发/需要响应）
- 例：SRE 体系里 incident 是可被“值班响应”的单位

### **outage**
- 含义：不可用（服务完全或大面积挂掉）
- 对比：**degradation**（性能下降/部分受影响）

### **regression**
- 含义：回归问题（本来好的功能，被改坏了）
- 常见表达：regression test / regression bug

### **flaky**
- 含义：不稳定、偶现（测试/用例/接口偶尔失败）
- 常见表达：flaky test

### **edge case**
- 含义：边缘情况（极端输入/少见路径）
- 常见表达：handle edge cases

---

## 2）一句话对照（超实用）
- **issue**：任何需要追踪的问题（最通用）
- **bug/defect**：更偏“代码/质量缺陷”
- **incident/outage**：更偏“线上运行态问题”（要响应/要复盘）
- **regression/flaky/edge case**：更偏“问题的类型/特征”

---

## 3）工单/复盘里常用的句型
- We’ve opened an **issue** to track this.
- This is a **regression** introduced in v1.8.
- We had an **incident** affecting the login service.
- The service experienced an **outage** for 12 minutes.
- The test is **flaky**; we need to stabilize it.

---

## 结尾小互动
你最近遇到的是哪一种：**bug / issue / incident**？
把一句描述发我（中文也行），我帮你改成更地道的英文工单标题。
