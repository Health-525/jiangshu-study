# 第01讲 · Python 与环境配置

## 课程内容概览

| 模块 | 内容 |
|------|------|
| 1 | IPython 与 Python 语言基础 |
| 2 | NumPy 基础与计算 |
| 3 | Pandas 数据处理 |
| 4 | Matplotlib 数据可视化 |
| 5 | Python 机器学习基础 |
| 6 | Python 数据读取和文件格式 |
| 7 | Python 数据分析案例 |

---

## 一、Python 简介

- 创始人：荷兰人 **Guido van Rossum**
- 起源：1989 年圣诞节，作为 ABC 语言的继承开发
- 命名来源：喜剧团体 **Monty Python**

### 特点

- 易学、易读、易维护
- 强大标准库
- 支持交互模式
- 可移植、可扩展、可嵌入
- 支持数据库操作与 GUI 编程

### 应用领域

- Web 开发
- 运维自动化脚本
- 科学计算
- 桌面应用
- 数据分析 / 机器学习

---

## 二、编程语言分类

| 类型 | 说明 | 示例 |
|------|------|------|
| 机器语言（第一代） | 二进制指令，CPU 直接识别 | 0101... |
| 汇编语言（第二代） | 用助记符代替二进制 | ADD、MOV |
| 高级语言（第三代） | 面向过程/对象，需编译器转换 | `var3 = var1 + var2` |

> Python 属于高级语言，2026年2月 TIOBE 排行榜排名第一。

---

## 三、Python 版本

- 主流版本：**Python 3.x**（Python 2 已停止维护）
- 建议使用最新稳定版

---

## 四、Anaconda 环境

$$
\text{Anaconda} = \text{Python} + \text{NumPy、SciPy 等常用库} + \text{IDE}
$$

| 组件 | 说明 |
|------|------|
| **Anaconda** | Python 环境管理软件 |
| **IPython** | 交互式 Python 命令行工具 |
| **Jupyter Notebook** | 网页端交互式开发环境 |
| **Spyder** | 类 MATLAB 风格 IDE |

### 下载地址

- 官网：`https://www.anaconda.com/download`
- 清华镜像（推荐国内）：`https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/`

---

## 五、三种使用方式对比

| 方式 | 特点 | 适用场景 |
|------|------|----------|
| Python 命令行 | 最基础 | 简单测试 |
| IPython 命令行 | 增强交互，支持补全、魔法命令 | 探索性调试 |
| Jupyter Notebook | 代码+文档+图表一体 | 数据分析、作业 |
| Spyder | 类 MATLAB，有变量查看器 | 科学计算 |

---

## 六、Jupyter Notebook 启动方式

1. 通过 Anaconda Navigator 启动
2. 通过开始菜单直接启动
3. 命令行输入 `jupyter notebook`
