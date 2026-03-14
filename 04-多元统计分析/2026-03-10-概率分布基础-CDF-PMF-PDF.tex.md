# 概率分布基础：CDF / PMF / PDF（复习笔记）

## 来源信息
- 文件：`4a127c3fafb1fe09a5e2805b420466c2.pdf`
- 可见元信息片段：`201910006533@njtech.edu.cn`；日期字符串：`2026-03-10`
- 说明：我当前读取到的内容主要是**概率论基础（离散/连续随机变量、分布函数与密度函数）**，属于多元统计分析的前置基础。

## 3–5 句摘要
- 本节给出了随机变量的**累积分布函数（CDF）**定义：$F(x)=P(X\le x)$。
- 对离散随机变量，介绍了**概率质量函数（PMF）**：$P(X=x_i)=p_i$，并要求 $p_i\ge 0$、$\sum p_i=1$。
- 用“掷公平六面骰子”的例子展示了 CDF 的**分段阶梯**表达。
- 对连续随机变量，给出 **CDF 与 PDF 的关系**：$F(x)=\int_{-\infty}^x f(t)\,dt$，并要求 $f(x)\ge 0$、$\int f=1$。
- 这些概念是后续学习**联合分布/边缘分布/条件分布**（多元统计核心）必备工具。

## 关键概念与定义

### 1) 离散随机变量（Discrete RV）与 PMF
- 若随机变量 $X$ 取值集合 $\{x_1,\dots,x_n\}$，则

$$
P(X=x_i)=p_i,\quad i=1,\dots,n
$$

- 概率约束：

$$
p_i\ge 0,\qquad \sum_{i=1}^n p_i = 1
$$

- PMF（概率质量函数）：$p_X(x)=P(X=x)$。

### 2) 累积分布函数 CDF（Cumulative Distribution Function）
- 定义：

$$
F_X(x)=P(X\le x)
$$
- 常用性质（复习必背）：
  - 单调不减；
  - $\lim_{x\to-\infty}F(x)=0$，$\lim_{x\to+\infty}F(x)=1$；
  - 一般为右连续。

### 3) 连续随机变量（Continuous RV）与 PDF
- 若存在非负可积函数 $f(x)$，使得对任意 $x$：

$$
F_X(x)=\int_{-\infty}^{x} f(t)\,dt
$$

- 则 $f$ 为 PDF（概率密度函数），并满足：

$$
f(x)\ge 0,\qquad \int_{-\infty}^{+\infty} f(x)\,dx = 1
$$

- 若 $F$ 可导，则：

$$
f(x)=F'(x)
$$

## 重要公式（高频）
- 区间概率（由 CDF 表示）：

$$
P(a<X\le b)=F(b)-F(a)
$$

- 离散 CDF（由 PMF 求）：

$$
F_X(x)=\sum_{x_i\le x} p_i
$$

## 例题：公平六面骰子 CDF（分段）
设 $Y\in\{1,2,3,4,5,6\}$，且 $P(Y=i)=1/6$。则

$$
F_Y(y)=P(Y\le y)=
\begin{cases}
0, & y<1\\
1/6, & 1\le y<2\\
2/6, & 2\le y<3\\
3/6, & 3\le y<4\\
4/6, & 4\le y<5\\
5/6, & 5\le y<6\\
1, & y\ge 6
\end{cases}
$$

## 易错点 / 考点
- **PMF vs PDF**：连续型的 $f(x_0)$ 不是点概率，连续型有 $P(X=x_0)=0$，概率要靠积分。
- **端点包含**：连续分布中 $P(a<X\le b)=P(a\le X\le b)$ 常相同；离散分布端点会影响结果。
- **合法性判断题**：
  - CDF：单调不减、极限 0/1、右连续；
  - PDF：非负、积分为 1。
- **离散分布的 CDF**：在取值点处有“跳跃”，跳跃高度就是该点的概率质量。

## 术语中英对照
- 随机变量 — Random variable
- 概率质量函数 — Probability mass function (PMF)
- 概率密度函数 — Probability density function (PDF)
- 累积分布函数 — Cumulative distribution function (CDF)
- 离散分布 — Discrete distribution
- 连续分布 — Continuous distribution

## 本节自测题（含答案要点）
1. **离散 CDF**：$X$ 取 $\{1,2,3\}$，概率 $\{0.2,0.5,0.3\}$。写 $F(x)$，并算 $P(1<X\le3)$。
   - 要点：分段阶梯；$P=0.8$。
2. **判断 PDF**：$g(x)=2x$（$0\le x\le1$ 其余 0）是否为 PDF？
   - 要点：非负；$\int_0^1 2x\,dx=1$。
3. **由 CDF 求 PDF**：$F(x)=1-e^{-x}$（$x\ge0$）求 $f(x)$ 与 $P(1<X\le2)$。
   - 要点：$f(x)=e^{-x}$，概率 $e^{-1}-e^{-2}$。
4. **CDF 合法性**：函数从 0.5 跳到 0.3 是否可能是 CDF？
   - 要点：不可能（违反单调不减）。
5. **归一化常数**：$P(Y=k)=c/k^2$（$k\ge1$）求 $c$。
   - 要点：$\sum 1/k^2=\pi^2/6$，$c=6/\pi^2$。
