# MATLAB 基础用法（数学模型课常用）

## 1. MATLAB 的核心：矩阵
- MATLAB 默认处理的是**矩阵/向量**。
- `*` 是矩阵乘法；`.*` 是逐元素乘法。

```matlab
A = [1 2; 3 4];
x = [1; 2];

A*x        % 矩阵乘法
A.*A       % 逐元素
A^2        % 矩阵幂
A.^2       % 逐元素幂
```

## 2. 变量、向量、常用生成
```matlab
v1 = [1 2 3 4];
v2 = 1:5;          % 1 2 3 4 5
v3 = 0:0.1:1;      % 0 到 1，步长 0.1
z  = zeros(3,4);
o  = ones(2,2);
I  = eye(3);
```

## 3. 索引与切片
- MATLAB 下标从 **1** 开始。

```matlab
A = [10 20 30; 40 50 60];
A(1,2)     % 第1行第2列 -> 20
A(1,:)     % 第1行
A(:,3)     % 第3列
A(end,:)   % 最后一行

idx = [1 3];
v = [5 6 7 8];
v(idx)     % 取第1和第3个
```

## 4. 脚本与函数
### 4.1 脚本（.m 文件直接运行）
- 脚本中变量默认在工作区。

### 4.2 函数（推荐）
```matlab
function y = myfun(x)
    y = x.^2 + 1;
end
```

## 5. 常用控制结构
```matlab
if a > 0
    disp('positive')
elseif a == 0
    disp('zero')
else
    disp('negative')
end

for i = 1:5
    fprintf('%d\n', i);
end

while n > 0
    n = n - 1;
end
```

## 6. 常用数学/统计函数
```matlab
x = [1 2 3 4];
mean(x)
std(x)
sum(x)
max(x)
min(x)

% 常见函数
sin(pi/2)
log(10)
exp(1)
```

## 7. 绘图（建模作业高频）
```matlab
x = 0:0.01:2*pi;
y = sin(x);
plot(x,y,'LineWidth',1.5)
grid on
title('sin(x)')
xlabel('x')
ylabel('y')
```

多条曲线：
```matlab
plot(x, sin(x)); hold on;
plot(x, cos(x));
legend('sin','cos'); hold off;
```

## 8. 解方程与线性代数
### 8.1 线性方程组 Ax=b
```matlab
A = [2 1; 1 3];
b = [1; 2];
x = A\b;      % 推荐写法
```

### 8.2 多项式
```matlab
p = [1 -3 2];     % x^2 - 3x + 2
r = roots(p);
```

## 9. 优化（数学模型常见入口）
### 9.1 无约束最小化 fminsearch（简单好用）
```matlab
f = @(x) (x-3).^2 + 1;
x0 = 0;
xbest = fminsearch(f, x0);
```

### 9.2 线性规划 linprog（需要 Optimization Toolbox）
- 形式：min c^T x, s.t. A x <= b
```matlab
% 示例（仅示意）
% c = [1; 2];
% A = [1 1; -1 2];
% b = [2; 2];
% x = linprog(c, A, b);
```

## 10. 读写数据
```matlab
T = readtable('data.csv');
% writetable(T,'out.csv');

M = readmatrix('data.csv');
% writematrix(M,'out.csv');
```

## 11. 常用排错/习惯
- `whos` 看变量
- `size(A)`、`length(v)`
- `help funcname` / `doc funcname`
- 尽量用 `A\b` 代替 `inv(A)*b`
