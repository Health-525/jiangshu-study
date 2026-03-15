# Python 基础知识点（数据分析向）

## 1. 环境与包管理
- **解释器**：建议使用 Python 3.10+。
- **虚拟环境**：
  - 创建：`python -m venv .venv`
  - 激活：Windows：`.venv\Scripts\activate`；macOS/Linux：`source .venv/bin/activate`
- **安装依赖**：`pip install numpy pandas matplotlib seaborn jupyter`
- **导出依赖**：`pip freeze > requirements.txt`

## 2. 基本语法速记
### 2.1 变量与常见类型
- `int / float / str / bool / None`
- 容器：`list / tuple / dict / set`

```py
x = 10
name = "Alice"
arr = [1, 2, 3]
info = {"id": 1, "score": 95}
```

### 2.2 条件与循环
```py
if score >= 90:
    level = "A"
elif score >= 60:
    level = "B"
else:
    level = "C"

for i in range(5):
    print(i)

while n > 0:
    n -= 1
```

### 2.3 函数与返回值
```py
def mean(a):
    return sum(a) / len(a)
```

### 2.4 列表推导式（数据清洗常用）
```py
nums = [1, 2, 3, 4]
sq = [x*x for x in nums if x % 2 == 0]  # [4, 16]
```

## 3. 文件读写（数据分析常用）
### 3.1 文本
```py
with open("a.txt", "r", encoding="utf-8") as f:
    text = f.read()
```

### 3.2 CSV / Excel（pandas）
```py
import pandas as pd

df = pd.read_csv("data.csv")
df.to_csv("out.csv", index=False)

# Excel
# df = pd.read_excel("data.xlsx", sheet_name=0)
# df.to_excel("out.xlsx", index=False)
```

## 4. NumPy：数组与向量化
- `ndarray`：核心是**向量化计算**（比 for 循环更快更简洁）

```py
import numpy as np

a = np.array([1, 2, 3])
print(a.mean(), a.std())

b = np.arange(0, 10, 2)     # 0,2,4,6,8
c = a * 2 + 1               # 向量化

M = np.array([[1, 2], [3, 4]])
print(M.T)                  # 转置
print(M @ M)                # 矩阵乘法
```

## 5. Pandas：DataFrame 基础（最常用）
### 5.1 选取与过滤
```py
import pandas as pd

df = pd.DataFrame({"name": ["a", "b"], "score": [80, 95]})

# 列
scores = df["score"]

# 行过滤
high = df[df["score"] >= 90]

# loc/iloc
first_row = df.iloc[0]
name_score = df.loc[0, ["name", "score"]]
```

### 5.2 缺失值与类型
```py
# 缺失值
clean = df.dropna()
filled = df.fillna(0)

# 类型转换
# df["score"] = df["score"].astype(int)
```

### 5.3 分组聚合（groupby）
```py
# df.groupby("class")["score"].mean()
```

### 5.4 排序与去重
```py
# df.sort_values("score", ascending=False)
# df.drop_duplicates(subset=["name"]) 
```

## 6. 可视化（matplotlib/seaborn）
```py
import matplotlib.pyplot as plt

x = [1, 2, 3]
y = [2, 4, 3]
plt.plot(x, y)
plt.title("Demo")
plt.xlabel("x")
plt.ylabel("y")
plt.show()
```

## 7. 调试与常见坑
- `print()` 不够用时：用 `pdb`：`import pdb; pdb.set_trace()`
- 常见错误：
  - **可变默认参数**：`def f(x, arr=[]): ...`（尽量避免）
  - `==` vs `is`：比较值用 `==`，比较对象身份才用 `is`
  - pandas 里链式赋值：尽量用 `df.loc[mask, "col"] = val`

## 8. 推荐练习（数据分析入门）
- 读一个 CSV → 清洗缺失值 → groupby 聚合 → 画图输出。
