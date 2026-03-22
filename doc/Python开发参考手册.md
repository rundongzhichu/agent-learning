# Python 开发与高级特性完全指南

## 目录
1. [Python 基础核心](#python-基础核心)
2. [数据结构深度应用](#数据结构深度应用)
3. [函数式编程与装饰器](#函数式编程与装饰器)
4. [面向对象高级特性](#面向对象高级特性)
5. [异步编程与并发](#异步编程与并发)
6. [元编程与魔法方法](#元编程与魔法方法)
7. [性能优化与最佳实践](#性能优化与最佳实践)

---

## 第一部分：Python 基础核心

### 一、Python 设计哲学

#### 1.1 The Zen of Python（Python 之禅）

```python
import this

# 输出 Python 的 19 条设计原则
"""
Beautiful is better than ugly.        # 优美胜于丑陋
Explicit is better than implicit.     # 明了胜于晦涩
Simple is better than complex.        # 简洁胜于复杂
Complex is better than complicated.   # 复杂胜于繁琐
Flat is better than nested.           # 扁平胜于嵌套
Sparse is better than dense.          # 稀疏胜于密集
Readability counts.                   # 可读性很重要
...
"""
```

**实际应用指导**：
```python
# ❌ 糟糕的设计（隐式、复杂）
def calc(a, b): return a if a > b else b

# ✅ 好的设计（显式、清晰）
def get_maximum(value1, value2):
    """返回两个值中的较大者"""
    if value1 > value2:
        return value1
    else:
        return value2
```

---

#### 1.2 Python 版本选择（2026 年视角）

```
✅ 推荐版本：Python 3.11+
理由：
- 性能提升 10-60%（CPython 3.11 优化）
- 更好的错误提示（显示表达式值）
- 新增 typing.Self 等类型提示
- 完整的 async/await 支持
- 活跃的社区支持

❌ 避免使用：
- Python 2.x（已停止维护）
- Python 3.6 及以下（缺少新特性）
```

---

### 二、核心语法精要

#### 2.1 变量与作用域

##### LEGB 规则（作用域查找顺序）

```python
# Local（局部） → Enclosed（嵌套） → Global（全局） → Built-in（内置）

x = "global"

def outer():
    x = "enclosed"
    
    def inner():
        x = "local"
        print(x)  # local
    
    inner()
    print(x)  # enclosed

outer()
print(x)  # global
```

##### nonlocal 和 global 关键字

```python
# global - 修改全局变量
count = 0

def increment():
    global count
    count += 1

# nonlocal - 修改嵌套作用域的变量
def make_counter():
    count = 0
    
    def counter():
        nonlocal count
        count += 1
        return count
    
    return counter

c = make_counter()
print(c())  # 1
print(c())  # 2
```

---

#### 2.2 数据类型概览

```python
# 数值类型
int_num = 42              # 整数（无限精度）
float_num = 3.14159       # 浮点数
complex_num = 3 + 4j      # 复数

# 布尔类型
is_valid = True
is_invalid = False

# 序列类型
text = "hello"            # 字符串
numbers = [1, 2, 3]       # 列表（可变）
dimensions = (10, 20)     # 元组（不可变）
range_obj = range(1, 10)  # 范围

# 集合类型
unique_items = {1, 2, 3}          # 集合（无序、唯一）
frozen_set = frozenset([1, 2])    # 冻结集合（不可变）

# 映射类型
person = {"name": "Alice", "age": 30}  # 字典

# 特殊类型
none_value = None         # 空值
not_implemented = NotImplemented  # 未实现
```

---

#### 2.3 类型注解（Type Hints）

Python 3.5+ 的类型系统是**渐进式**的，运行时不强制检查。

##### 基础类型注解

```python
from typing import List, Dict, Tuple, Optional, Union

# 变量注解
name: str = "Alice"
age: int = 30
height: float = 1.75
is_student: bool = False

# 容器类型
names: List[str] = ["Alice", "Bob"]
scores: Dict[str, int] = {"math": 95, "english": 88}
coordinates: Tuple[int, int] = (10, 20)

# 可选类型（可以是 None）
middle_name: Optional[str] = None

# 联合类型（可以是多种类型之一）
user_id: Union[int, str] = 12345  # 或 "user_123"

# Python 3.10+ 简化语法
user_id_new: int | str = 12345
optional_name: str | None = None
```

##### 函数类型注解

```python
from typing import Callable, Any

def greet(name: str, greeting: str = "Hello") -> str:
    """生成问候语"""
    return f"{greeting}, {name}!"

# 可调用对象类型
def apply_operation(
    x: int, 
    operation: Callable[[int], int]
) -> int:
    return operation(x)

# 任意参数
def process_items(*args: str, **kwargs: Any) -> None:
    pass
```

##### 泛型与 TypeVar

```python
from typing import TypeVar, Generic

T = TypeVar('T')  # 定义类型变量

def first_element(items: list[T]) -> T:
    """返回列表的第一个元素"""
    return items[0]

class Stack(Generic[T]):
    """泛型栈类"""
    
    def __init__(self) -> None:
        self.items: list[T] = []
    
    def push(self, item: T) -> None:
        self.items.append(item)
    
    def pop(self) -> T:
        return self.items.pop()

# 使用
int_stack = Stack[int]()
int_stack.push(1)
int_stack.push(2)
top: int = int_stack.pop()
```

##### Python 3.11+ 新特性

```python
from typing import Self, Literal, TypedDict

# Self 类型（引用当前类）
class MyClass:
    def set_value(self, value: int) -> Self:
        self.value = value
        return self  # 支持链式调用
    
    def clone(self) -> Self:
        return type(self)()

# 字面量类型（限制为特定值）
def set_status(status: Literal["active", "inactive"]) -> None:
    pass

set_status("active")  # ✅
set_status("pending")  # ❌ 类型检查器会报错

# TypedDict（强类型字典）
class PersonInfo(TypedDict):
    name: str
    age: int
    email: str | None

person: PersonInfo = {
    "name": "Alice",
    "age": 30,
    "email": "alice@example.com"
}
```

---

### 三、控制流高级用法

#### 3.1 条件表达式的优雅写法

```python
# ❌ 冗长的 if-else
if condition:
    result = "yes"
else:
    result = "no"

# ✅ 三元运算符
result = "yes" if condition else "no"

# ✅ walrus 运算符（:=）Python 3.8+
# 在表达式中赋值
if (n := len(data)) > 10:
    print(f"数据过多：{n} 条")

# 读取文件时的优雅用法
with open("file.txt") as f:
    while (line := f.readline()):
        process(line)
```

#### 3.2 match-case 结构化模式匹配（Python 3.10+）

```python
# 替代冗长的 if-elif-else
def handle_command(command: str) -> str:
    match command.split():
        case ["quit"]:
            return "退出系统"
        
        case ["load", filename]:
            return f"加载文件：{filename}"
        
        case ["save", filename] if filename.endswith(".txt"):
            return f"保存文本文件：{filename}"
        
        case ["move", x, y]:
            return f"移动到位置 ({x}, {y})"
        
        case _:
            return "未知命令"

# 数据类模式匹配
from dataclasses import dataclass

@dataclass
class Point:
    x: int
    y: int

def analyze_point(point: Point) -> str:
    match point:
        case Point(x=0, y=0):
            return "原点"
        case Point(x=0):
            return "在 Y 轴上"
        case Point(y=0):
            return "在 X 轴上"
        case Point(x=x, y=y) if x == y:
            return "在对角线上"
        case _:
            return "普通位置"
```

---

#### 3.3 循环的高级技巧

```python
# enumerate - 同时获取索引和值
fruits = ["apple", "banana", "cherry"]
for i, fruit in enumerate(fruits, start=1):
    print(f"{i}. {fruit}")

# zip - 并行遍历多个序列
names = ["Alice", "Bob", "Charlie"]
ages = [25, 30, 35]
for name, age in zip(names, ages):
    print(f"{name} is {age} years old")

# reversed - 反向遍历
for i in reversed(range(len(fruits))):
    print(fruits[i])

# sorted - 排序遍历
for num in sorted([3, 1, 4, 1, 5], reverse=True):
    print(num)

# break-else 结构
# else 块只在循环正常完成（未 break）时执行
def find_prime(numbers):
    for n in numbers:
        if n < 2:
            continue
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                break
        else:
            print(f"{n} 是质数")
```

---

## 第二部分：数据结构深度应用

### 一、列表（List）的深度用法

#### 1.1 列表推导式的艺术

```python
# 基础用法
squares = [x**2 for x in range(10)]

# 带条件过滤
even_squares = [x**2 for x in range(10) if x % 2 == 0]

# 嵌套循环
matrix = [[i*j for j in range(1, 4)] for i in range(1, 4)]
# [[1, 2, 3], [2, 4, 6], [3, 6, 9]]

# 扁平化嵌套列表
nested = [[1, 2], [3, 4], [5, 6]]
flattened = [item for sublist in nested for item in sublist]

# 实际案例：提取特定字段
users = [
    {"name": "Alice", "age": 25, "active": True},
    {"name": "Bob", "age": 30, "active": False},
    {"name": "Charlie", "age": 35, "active": True}
]

active_names = [user["name"] for user in users if user["active"]]
```

#### 1.2 列表切片的高级用法

```python
nums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# 完整切片：[start:end:step]
print(nums[::2])    # [0, 2, 4, 6, 8] 隔一个取一个
print(nums[1::2])   # [1, 3, 5, 7, 9] 隔一个取一个
print(nums[::-1])   # [9, 8, ..., 0] 反转列表

# 切片赋值（原地修改）
nums[0:3] = [10, 20, 30]  # 替换前三个元素
nums[::2] = [0] * 5       # 替换所有偶数位置

# 删除切片
del nums[2:5]

# 浅拷贝 vs 深拷贝
shallow_copy = nums[:]           # 浅拷贝
deep_copy = [x[:] for x in matrix]  # 二维列表深拷贝

import copy
deep_copy_full = copy.deepcopy(matrix)
```

---

### 二、字典（Dict）的高效操作

#### 2.1 字典推导式

```python
# 基础用法
squares = {x: x**2 for x in range(5)}

# 键值对交换
original = {"a": 1, "b": 2, "c": 3}
swapped = {v: k for k, v in original.items()}

# 过滤字典
scores = {"Alice": 85, "Bob": 60, "Charlie": 90}
passed = {name: score for name, score in scores.items() if score >= 70}

# 合并字典（Python 3.9+）
dict1 = {"a": 1, "b": 2}
dict2 = {"c": 3, "d": 4}
merged = dict1 | dict2  # {'a': 1, 'b': 2, 'c': 3, 'd': 4}

# 更新字典
dict1 |= dict2  # 原地更新
```

#### 2.2 字典的高效访问

```python
# get 方法（安全访问）
value = my_dict.get("key", default_value)

# setdefault（存在则返回，不存在则设置）
my_dict.setdefault("new_key", []).append("value")

# defaultdict（自动初始化）
from collections import defaultdict

word_count = defaultdict(int)
for word in words:
    word_count[word] += 1

grouped = defaultdict(list)
for item in items:
    grouped[item.category].append(item)

# ChainMap（合并多个字典视图）
from collections import ChainMap

defaults = {"theme": "dark", "lang": "en"}
user_prefs = {"theme": "light"}
combined = ChainMap(user_prefs, defaults)
print(combined["theme"])  # "light"（用户优先）
print(combined["lang"])   # "en"（回退到默认）
```

#### 2.3 OrderedDict 与 FrozenDict

```python
from collections import OrderedDict
from types import MappingProxyType

# OrderedDict - 保持插入顺序
ordered = OrderedDict()
ordered["first"] = 1
ordered["second"] = 2
ordered["third"] = 3

# 移动键到末尾/开头
ordered.move_to_end("first")           # 移到末尾
ordered.move_to_end("first", last=False)  # 移到开头

# FrozenDict（不可变字典）
frozen = MappingProxyType({"a": 1, "b": 2})
# frozen["c"] = 3  # ❌ TypeError
```

---

### 三、集合（Set）的数学运算

```python
A = {1, 2, 3, 4, 5}
B = {4, 5, 6, 7, 8}

# 并集
union = A | B  # 或 A.union(B)

# 交集
intersection = A & B  # 或 A.intersection(B)

# 差集
difference = A - B  # 或 A.difference(B)  # {1, 2, 3}

# 对称差集（只在一个集合中）
symmetric_diff = A ^ B  # 或 A.symmetric_difference(B)

# 子集/超集判断
is_subset = A <= B  # A.issubset(B)
is_superset = A >= B  # A.issuperset(B)
is_disjoint = A.isdisjoint(B)  # 是否无交集

# 实际应用：去重并保持顺序
def unique_preserve_order(items):
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result
```

---

### 四、collections 模块的高级数据结构

#### 4.1 Counter - 计数器

```python
from collections import Counter

# 统计频率
words = ["apple", "banana", "apple", "orange", "banana", "apple"]
counter = Counter(words)
print(counter.most_common(2))  # [('apple', 3), ('banana', 2)]

# 数学运算
c1 = Counter(a=3, b=1)
c2 = Counter(a=1, b=2, c=1)
print(c1 + c2)   # Counter({'a': 4, 'b': 3, 'c': 1})
print(c1 - c2)   # Counter({'a': 2})

# 元素展开
elements = Counter(a=2, b=3)
list(elements.elements())  # ['a', 'a', 'b', 'b', 'b']
```

#### 4.2 deque - 双端队列

```python
from collections import deque

# O(1) 时间复杂度的两端操作
queue = deque([1, 2, 3])
queue.append(4)        # 右端添加
queue.appendleft(0)    # 左端添加
queue.pop()            # 右端弹出
queue.popleft()        # 左端弹出

# 固定长度队列（自动丢弃旧元素）
recent = deque(maxlen=5)
for i in range(10):
    recent.append(i)
# deque([5, 6, 7, 8, 9], maxlen=5)

# 旋转
queue.rotate(1)   # 向右旋转
queue.rotate(-1)  # 向左旋转
```

#### 4.3 namedtuple - 轻量级类

```python
from collections import namedtuple

# 定义命名元组
Point = namedtuple('Point', ['x', 'y'])
p = Point(10, 20)

# 访问
print(p.x)  # 10
print(p.y)  # 20

# 转换为字典
p_dict = p._asdict()  # {'x': 10, 'y': 20}

# 替换字段（返回新实例，原实例不变）
p2 = p._replace(x=30)  # Point(x=30, y=20)

# 实际案例：数据库记录
User = namedtuple('User', ['id', 'name', 'email'])
user = User(1, "Alice", "alice@example.com")
```

---

## 第三部分：函数式编程与装饰器

### 一、函数即对象

#### 1.1 高阶函数

```python
# 函数可以作为参数传递
def apply(func, value):
    return func(value)

def double(x):
    return x * 2

result = apply(double, 5)  # 10

# 函数可以作为返回值
def make_multiplier(factor):
    def multiplier(x):
        return x * factor
    return multiplier

times_three = make_multiplier(3)
print(times_three(10))  # 30
```

#### 1.2 lambda 表达式

```python
# 基础用法
add = lambda x, y: x + y

# 作为排序键
students = [("Alice", 25), ("Bob", 20), ("Charlie", 30)]
sorted_students = sorted(students, key=lambda x: x[1])

# 注意：lambda 应该只用于简单场景
# ❌ 过度使用
complex_calc = lambda x: x**2 if x > 0 else -x**2

# ✅ 改用普通函数
def square_or_negate(x):
    if x > 0:
        return x**2
    else:
        return -x**2
```

---

### 二、装饰器完全指南

#### 2.1 装饰器基础

```python
# 最简单的装饰器
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("调用前")
        result = func(*args, **kwargs)
        print("调用后")
        return result
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")

say_hello()
# 输出:
# 调用前
# Hello!
# 调用后
```

#### 2.2 保留函数元信息（functools.wraps）

```python
from functools import wraps

def decorator_with_metadata(func):
    @wraps(func)  # 保留原函数的 __name__, __doc__ 等
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@decorator_with_metadata
def original_function():
    """这是原文档"""
    pass

print(original_function.__name__)  # 'original_function'
print(original_function.__doc__)   # '这是原文档'
```

#### 2.3 带参数的装饰器

```python
from functools import wraps

def repeat(times):
    """重复执行指定次数的装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def greet(name):
    print(f"Hello, {name}!")

greet("Alice")  # 打印 3 次
```

#### 2.4 实用装饰器示例

##### 计时装饰器

```python
import time
from functools import wraps

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__name__} 耗时：{end - start:.4f}秒")
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(1)
```

##### 缓存装饰器（memoization）

```python
from functools import lru_cache

# 手动实现
def memoize(func):
    cache = {}
    
    @wraps(func)
    def wrapper(*args):
        if args in cache:
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result
    return wrapper

# 使用标准库
@lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

##### 重试装饰器

```python
import time
from functools import wraps

def retry(max_attempts=3, delay=1, backoff=2):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            current_delay = delay
            
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        raise
                    print(f"失败，{current_delay}秒后重试...")
                    time.sleep(current_delay)
                    current_delay *= backoff
        return wrapper
    return decorator

@retry(max_attempts=3, delay=2)
def unstable_api():
    # 可能失败的 API 调用
    pass
```

##### 权限验证装饰器

```python
from functools import wraps

def require_permission(permission):
    def decorator(func):
        @wraps(func)
        def wrapper(user, *args, **kwargs):
            if permission not in user.permissions:
                raise PermissionError(f"需要 {permission} 权限")
            return func(user, *args, **kwargs)
        return wrapper
    return decorator

@require_permission("admin")
def delete_user(user, target_user):
    pass
```

---

### 三、生成器与迭代器

#### 3.1 迭代器协议

```python
# 自定义迭代器
class CountDown:
    def __init__(self, start):
        self.start = start
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.start <= 0:
            raise StopIteration
        self.start -= 1
        return self.start

for i in CountDown(5):
    print(i)  # 4, 3, 2, 1, 0
```

#### 3.2 生成器函数

```python
# yield 关键字
def countdown(start):
    current = start
    while current > 0:
        current -= 1
        yield current

# 惰性求值（节省内存）
def read_large_file(file_path):
    with open(file_path) as f:
        for line in f:
            yield line.strip()

# 生成器表达式（类似列表推导式）
squares_gen = (x**2 for x in range(10))
sum_squares = sum(x**2 for x in range(1000))  # 不需要方括号
```

#### 3.3 yield from（委托生成器）

```python
def chain(iterables):
    for iterable in iterables:
        yield from iterable  # 等价于 for item in iterable: yield item

# 实际案例：树形结构遍历
def tree_flatten(tree):
    if isinstance(tree, list):
        for subtree in tree:
            yield from tree_flatten(subtree)
    else:
        yield tree

nested = [1, [2, 3], [4, [5, 6]]]
list(tree_flatten(nested))  # [1, 2, 3, 4, 5, 6]
```

#### 3.4 生成器的高级用法

```python
# send() - 向生成器发送值
def accumulator():
    total = 0
    while True:
        value = yield total
        if value is not None:
            total += value

acc = accumulator()
next(acc)        # 0
acc.send(10)     # 10
acc.send(20)     # 30

# throw() - 在生成器内抛出异常
# close() - 关闭生成器
```

---

### 四、itertools 模块（高效迭代工具）

```python
import itertools

# 无限迭代器
itertools.count(10, 2)      # 10, 12, 14, ...
itertools.cycle([1, 2, 3])  # 1, 2, 3, 1, 2, 3, ...
itertools.repeat('A', 3)    # A, A, A

# 有限迭代器
itertools.chain([1, 2], [3, 4])           # 1, 2, 3, 4
itertools.islice('ABCDEFG', 2, 5)         # C, D, E
itertools.compress('ABCDEF', [1,0,1,0,1,0])  # A, C, E

# 组合学
itertools.permutations([1, 2, 3], 2)  # (1,2), (1,3), (2,1), ...
itertools.combinations([1, 2, 3], 2)  # (1,2), (1,3), (2,3)
itertools.product('AB', 'xy')         # Ax, Ay, Bx, By

# 分组
data = sorted([('A', 1), ('B', 2), ('A', 3)], key=lambda x: x[0])
for key, group in itertools.groupby(data, key=lambda x: x[0]):
    print(key, list(group))
# A [(A, 1), (A, 3)]
# B [(B, 2)]

# 实际案例：分块处理
def chunker(iterable, size):
    it = iter(iterable)
    while True:
        chunk = list(itertools.islice(it, size))
        if not chunk:
            break
        yield chunk

for batch in chunker(range(100), 10):
    process(batch)
```

---

## 第四部分：面向对象高级特性

### 一、类的继承与多态

#### 1.1 多重继承与 MRO

```python
# 方法解析顺序（MRO）
class A:
    def method(self):
        print("A")

class B(A):
    def method(self):
        print("B")

class C(A):
    def method(self):
        print("C")

class D(B, C):
    pass

d = D()
d.method()  # B（遵循 C3 线性化算法）

# 查看 MRO
print(D.__mro__)  
# (<class 'D'>, <class 'B'>, <class 'C'>, <class 'A'>, <class 'object'>)

# super() 的正确使用
class D(B, C):
    def method(self):
        super().method()  # 按照 MRO 调用下一个
        print("D")
```

#### 1.2 抽象基类（ABC）

```python
from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def make_sound(self):
        """发出声音"""
        pass
    
    @abstractmethod
    def move(self):
        """移动方式"""
        pass
    
    def sleep(self):  # 具体方法
        print("睡觉中...")

# ❌ 这会报错：不能实例化抽象类
# animal = Animal()

# ✅ 必须实现所有抽象方法
class Dog(Animal):
    def make_sound(self):
        return "汪汪汪"
    
    def move(self):
        return "用四条腿跑"

dog = Dog()
```

---

### 二、属性控制

#### 2.1 @property 装饰器

```python
class Circle:
    def __init__(self, radius):
        self._radius = radius
    
    @property
    def radius(self):
        """getter"""
        return self._radius
    
    @radius.setter
    def radius(self, value):
        """setter"""
        if value < 0:
            raise ValueError("半径不能为负")
        self._radius = value
    
    @property
    def area(self):
        """计算属性（只读）"""
        return 3.14159 * self._radius ** 2

circle = Circle(5)
print(circle.area)  # 78.53975
circle.radius = 10  # 触发 setter
# circle.area = 100  # ❌ AttributeError: 只读属性
```

#### 2.2 __slots__ 优化内存

```python
# 默认情况：每个实例都有 __dict__
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# 使用 __slots__ 节省内存
class OptimizedPoint:
    __slots__ = ['x', 'y']  # 限制属性
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

# 好处：
# 1. 节省 40-50% 内存
# 2. 更快的属性访问
# 缺点：不能动态添加属性
```

---

### 三、描述符（Descriptor）

```python
# 描述符协议
class Descriptor:
    def __get__(self, instance, owner):
        """访问属性时调用"""
        pass
    
    def __set__(self, instance, value):
        """设置属性时调用"""
        pass
    
    def __delete__(self, instance):
        """删除属性时调用"""
        pass

# 实际应用：类型检查描述符
class Typed:
    def __init__(self, name, expected_type):
        self.name = name
        self.expected_type = expected_type
    
    def __get__(self, instance, owner):
        return instance.__dict__[self.name]
    
    def __set__(self, instance, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(f"期望 {self.expected_type}, 得到 {type(value)}")
        instance.__dict__[self.name] = value
    
    def __delete__(self, instance):
        del instance.__dict__[self.name]

# 类装饰器：批量应用描述符
def typeassert(cls):
    for name, expected_type in cls.__annotations__.items():
        setattr(cls, name, Typed(name, expected_type))
    return cls

@typeassert
class Person:
    name: str
    age: int
    email: str
```

---

### 四、元类（Metaclass）

```python
# 元类是创建类的类
# type 是默认的元类

# 自定义元类
class SingletonMeta(type):
    """单例元类"""
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

# 使用元类
class Database(metaclass=SingletonMeta):
    def __init__(self):
        self.connection = "connected"

db1 = Database()
db2 = Database()
print(db1 is db2)  # True（同一个实例）

# 元类的典型用途：
# 1. 注册子类（插件系统）
# 2. 自动添加方法/属性
# 3. ORM 框架（如 SQLAlchemy）
# 4. API 客户端自动生成
```

---

### 五、数据类（dataclass）

```python
from dataclasses import dataclass, field
from typing import List

@dataclass
class Product:
    name: str
    price: float
    quantity: int = 0  # 默认值
    
    # 计算属性
    @property
    def total_value(self):
        return self.price * self.quantity
    
    # 自定义方法
    def add_stock(self, amount):
        self.quantity += amount

@dataclass
class Employee:
    name: str
    department: str
    skills: List[str] = field(default_factory=list)  # 可变默认值

# 自动生成的方法：
# __init__, __repr__, __eq__, __hash__（如果可能）

# 比较高级的用法
@dataclass(order=True)
class PriorityItem:
    priority: int
    description: str = field(compare=False)  # 不参与比较

# 冻结的数据类（不可变）
@dataclass(frozen=True)
class ImmutablePoint:
    x: int
    y: int
```

---

## 第五部分：异步编程与并发

### 一、asyncio 基础

#### 1.1 协程（Coroutine）

```python
import asyncio

# 定义协程
async def fetch_data(url):
    print(f"开始获取 {url}")
    await asyncio.sleep(1)  # 模拟 IO 操作
    print(f"获取完成 {url}")
    return f"data from {url}"

# 运行协程
async def main():
    # 串行执行
    result1 = await fetch_data("url1")
    result2 = await fetch_data("url2")
    
    # 并发执行
    results = await asyncio.gather(
        fetch_data("url1"),
        fetch_data("url2"),
        fetch_data("url3")
    )

asyncio.run(main())  # Python 3.7+
```

#### 1.2 Task 管理

```python
async def worker(id, delay):
    for i in range(5):
        await asyncio.sleep(delay)
        print(f"Worker {id}: {i}")

async def main():
    # 创建任务
    task1 = asyncio.create_task(worker(1, 1))
    task2 = asyncio.create_task(worker(2, 2))
    
    # 等待完成
    await task1
    await task2
    
    # 批量创建
    tasks = [asyncio.create_task(worker(i, 0.5)) for i in range(10)]
    await asyncio.gather(*tasks)
    
    # 超时控制
    try:
        await asyncio.wait_for(fetch_data("slow_url"), timeout=5.0)
    except asyncio.TimeoutError:
        print("超时了")

asyncio.run(main())
```

---

### 二、异步上下文管理器

```python
class AsyncConnection:
    async def __aenter__(self):
        self.conn = await establish_connection()
        return self.conn
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.conn.close()

# 使用
async with AsyncConnection() as conn:
    data = await conn.fetch()

# 异步生成器
async def async_range(start, end):
    for i in range(start, end):
        yield i
        await asyncio.sleep(0.1)

async for num in async_range(1, 5):
    print(num)
```

---

### 三、并发编程

#### 3.1 threading 模块

```python
from threading import Thread, Lock
import threading

# 创建线程
def worker(name):
    print(f"{name} 开始工作")

thread = Thread(target=worker, args=("Thread-1",))
thread.start()
thread.join()

# 线程锁
lock = Lock()
counter = 0

def safe_increment():
    global counter
    with lock:  # 或 lock.acquire(); lock.release()
        counter += 1

# 守护线程（主程序结束时自动终止）
daemon_thread = Thread(target=background_task, daemon=True)
```

#### 3.2 multiprocessing 模块

```python
from multiprocessing import Process, Pool, cpu_count

# 多进程
def process_data(data):
    return data * 2

if __name__ == '__main__':
    # 进程池
    with Pool(processes=cpu_count()) as pool:
        results = pool.map(process_data, range(10))
    
    # 单独进程
    p = Process(target=process_data, args=(42,))
    p.start()
    p.join()
```

#### 3.3 concurrent.futures（统一接口）

```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed

# 线程池
with ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(fetch_url, url) for url in urls]
    
    for future in as_completed(futures):
        result = future.result()
        print(result)

# 进程池（CPU 密集型任务）
with ProcessPoolExecutor() as executor:
    results = executor.map(compute_intensive, data)
```

---

## 第六部分：元编程与魔法方法

### 一、常用魔法方法

#### 1.1 对象生命周期

```python
class MyClass:
    def __new__(cls, *args, **kwargs):
        """创建实例（在 __init__ 之前调用）"""
        instance = super().__new__(cls)
        return instance
    
    def __init__(self, value):
        """初始化实例"""
        self.value = value
    
    def __del__(self):
        """析构函数（垃圾回收前调用）"""
        print("对象被销毁")
```

#### 1.2 字符串表示

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def __str__(self):
        """用户友好的字符串表示（print 时使用）"""
        return f"{self.name}({self.age}岁)"
    
    def __repr__(self):
        """开发者友好的表示（调试时使用）"""
        return f"Person('{self.name}', {self.age})"
    
    def __format__(self, format_spec):
        """格式化字符串"""
        if format_spec == 'detailed':
            return f"Person: {self.name}, Age: {self.age}"
        return str(self)

p = Person("Alice", 30)
print(str(p))      # Alice(30 岁)
print(repr(p))     # Person('Alice', 30)
print(f"{p:detailed}")  # Person: Alice, Age: 30
```

#### 1.3 容器协议

```python
class MyCollection:
    def __init__(self):
        self._items = []
    
    def __len__(self):
        return len(self._items)
    
    def __getitem__(self, index):
        return self._items[index]
    
    def __setitem__(self, index, value):
        self._items[index] = value
    
    def __delitem__(self, index):
        del self._items[index]
    
    def __contains__(self, item):
        return item in self._items
    
    def __iter__(self):
        return iter(self._items)
    
    def __reversed__(self):
        return reversed(self._items)

coll = MyCollection()
print(len(coll))      # 0
coll.append(1)
print(1 in coll)      # True
for item in coll:     # 可迭代
    print(item)
```

#### 1.4 数值运算

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        """加法"""
        return Vector(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        """减法"""
        return Vector(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar):
        """数乘"""
        return Vector(self.x * scalar, self.y * scalar)
    
    def __eq__(self, other):
        """相等比较"""
        return self.x == other.x and self.y == other.y
    
    def __lt__(self, other):
        """小于比较"""
        return self.x < other.x or (self.x == other.x and self.y < other.y)
    
    def __abs__(self):
        """绝对值"""
        return (self.x**2 + self.y**2)**0.5
    
    def __neg__(self):
        """取反"""
        return Vector(-self.x, -self.y)

v1 = Vector(2, 3)
v2 = Vector(1, 2)
print(v1 + v2)  # Vector(3, 5)
print(v1 * 2)   # Vector(4, 6)
```

---

### 二、动态属性拦截

```python
class DynamicAccess:
    def __getattr__(self, name):
        """访问不存在的属性时调用"""
        return f"属性 {name} 不存在"
    
    def __setattr__(self, name, value):
        """设置任何属性时调用"""
        print(f"设置 {name} = {value}")
        super().__setattr__(name, value)
    
    def __delattr__(self, name):
        """删除属性时调用"""
        print(f"删除属性 {name}")
        super().__delattr__(name)

# __getattribute__ 拦截所有属性访问（慎用）
class StrictAccess:
    def __getattribute__(self, name):
        print(f"访问属性：{name}")
        return super().__getattribute__(name)
```

---

### 三、上下文管理器

```python
# 基于类的上下文管理器
class FileManager:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.file = None
    
    def __enter__(self):
        print("进入上下文")
        self.file = open(self.filename, self.mode)
        return self.file
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("退出上下文")
        self.file.close()
        # 返回 True 可以吞掉异常
        return False

# 使用
with FileManager("test.txt", "w") as f:
    f.write("Hello")

# 基于 contextlib 的简化
from contextlib import contextmanager

@contextmanager
def file_manager(filename, mode):
    f = open(filename, mode)
    try:
        yield f
    finally:
        f.close()

# 使用
with file_manager("test.txt", "w") as f:
    f.write("Hello")
```

---

## 第七部分：性能优化与最佳实践

### 一、性能分析工具

#### 1.1 cProfile - 性能分析

```python
import cProfile
import pstats

def slow_function():
    total = 0
    for i in range(1000000):
        total += i
    return total

# 命令行分析
# python -m cProfile script.py

# 代码中分析
profiler = cProfile.Profile()
profiler.enable()

slow_function()

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(10)  # 打印前 10 个最耗时的函数
```

#### 1.2 timeit - 精确计时

```python
import timeit

# 命令行
# python -m timeit '"-".join(str(n) for n in range(100))'

# 代码中
time = timeit.timeit(
    stmt="[x**2 for x in range(1000)]",
    number=10000
)
print(f"耗时：{time:.4f}秒")

# 比较不同实现
setup = "from math import sqrt"
stmt1 = "[x**0.5 for x in range(1000)]"
stmt2 = "[sqrt(x) for x in range(1000)]"

t1 = timeit.timeit(stmt1, number=10000)
t2 = timeit.timeit(stmt2, setup=setup, number=10000)

print(f"列表推导式：{t1:.4f}")
print(f"math.sqrt: {t2:.4f}")
```

---

### 二、性能优化技巧

#### 2.1 选择合适的数据结构

```python
# ❌ 列表查找 O(n)
items = [1, 2, 3, 4, 5]
if 5 in items:
    pass

# ✅ 集合查找 O(1)
items_set = {1, 2, 3, 4, 5}
if 5 in items_set:
    pass

# ❌ 频繁字符串拼接（每次创建新对象）
result = ""
for i in range(1000):
    result += str(i)

# ✅ 使用 join（一次性创建）
result = "".join(str(i) for i in range(1000))

# ✅ 或使用列表
parts = []
for i in range(1000):
    parts.append(str(i))
result = "".join(parts)
```

#### 2.2 生成器 vs 列表

```python
# ❌ 占用大量内存
squares_list = [x**2 for x in range(1000000)]

# ✅ 惰性求值，节省内存
squares_gen = (x**2 for x in range(1000000))

# 只需要遍历一次时用生成器
total = sum(x**2 for x in range(1000000))
```

#### 2.3 缓存优化

```python
from functools import lru_cache

# ❌ 重复计算
def fibonacci_slow(n):
    if n < 2:
        return n
    return fibonacci_slow(n-1) + fibonacci_slow(n-2)

# ✅ 使用缓存
@lru_cache(maxsize=None)
def fibonacci_fast(n):
    if n < 2:
        return n
    return fibonacci_fast(n-1) + fibonacci_fast(n-2)

# 性能对比：fibonacci_fast(100) 瞬间完成
```

---

### 三、代码质量工具

```bash
# 代码格式化
black my_code.py
autopep8 --in-place my_code.py

# 代码检查
flake8 my_code.py
pylint my_code.py

# 类型检查
mypy my_code.py

# 测试覆盖率
pytest --cov=my_package tests/

# 依赖检查
pip-audit
safety check
```

---

### 四、最佳实践清单

#### 4.1 命名规范

```python
# 变量和函数：小写 + 下划线
user_name = "Alice"
def calculate_total():
    pass

# 类名：大驼峰
class UserProfile:
    pass

# 常量：全大写
MAX_CONNECTIONS = 100
PI = 3.14159

# 私有成员：单下划线前缀
_internal_var = 42
def _helper_function():
    pass

# 名称修饰：双下划线前缀（避免子类覆盖）
class Parent:
    def __private_method(self):
        pass

# 魔法方法：双下划线前后
def __init__(self):
    pass
```

#### 4.2 异常处理

```python
# ✅ 捕获具体异常
try:
    result = int(user_input)
except ValueError as e:
    print(f"输入无效：{e}")

# ❌ 避免裸 except
try:
    risky_operation()
except:  # 会捕获所有异常，包括 KeyboardInterrupt
    pass

# ✅ 使用 else 和 finally
try:
    file = open("data.txt")
    content = file.read()
except FileNotFoundError:
    print("文件不存在")
else:
    print("读取成功")
finally:
    file.close()

# ✅ 自定义异常
class ValidationError(Exception):
    def __init__(self, field, message):
        self.field = field
        self.message = message
        super().__init__(self.message)
```

#### 4.3 文档字符串

```python
def process_payment(amount, currency="USD"):
    """
    处理支付请求
    
    Args:
        amount (float): 支付金额，必须大于 0
        currency (str): 货币类型，默认为 USD
    
    Returns:
        dict: 包含 transaction_id 和 status 的字典
    
    Raises:
        ValueError: 当金额无效时
        PaymentError: 当支付失败时
    
    Example:
        >>> result = process_payment(100.50)
        >>> print(result['status'])
        'success'
    """
    if amount <= 0:
        raise ValueError("金额必须大于 0")
    
    # 实现...
```

---

### 五、常见陷阱与解决方案

#### 5.1 可变默认参数

```python
# ❌ 危险！默认参数在函数定义时求值
def append_to_list(item, my_list=[]):
    my_list.append(item)
    return my_list

print(append_to_list(1))  # [1]
print(append_to_list(2))  # [1, 2] ❌ 不是预期的 [2]

# ✅ 使用 None
def append_to_list_safe(item, my_list=None):
    if my_list is None:
        my_list = []
    my_list.append(item)
    return my_list
```

#### 5.2 闭包延迟绑定

```python
# ❌ 延迟绑定问题
functions = []
for i in range(5):
    functions.append(lambda: i)

print([f() for f in functions])  # [4, 4, 4, 4, 4] ❌

# ✅ 立即绑定
functions = []
for i in range(5):
    functions.append(lambda x=i: x)

print([f() for f in functions])  # [0, 1, 2, 3, 4] ✅
```

#### 5.3 GIL（全局解释器锁）

```python
# CPU 密集型任务受 GIL 限制
# 多线程不会真正并行

# ❌ 多线程对 CPU 密集型任务帮助不大
from threading import Thread

def compute():
    total = 0
    for i in range(10**7):
        total += i

threads = [Thread(target=compute) for _ in range(4)]
for t in threads: t.start()
for t in threads: t.join()

# ✅ 使用多进程
from multiprocessing import Process

processes = [Process(target=compute) for _ in range(4)]
for p in processes: p.start()
for p in processes: p.join()
```

---

## 总结

本指南涵盖了 Python 开发的核心知识点：

### 📚 基础核心
- Python 设计哲学与版本选择
- 变量、作用域、类型注解
- 控制流高级用法

### 🔧 数据结构
- 列表、字典、集合的深度应用
- collections 模块高级数据结构

### 🎯 函数式编程
- 装饰器完全指南
- 生成器与迭代器
- itertools 高效工具

### 🏗️ 面向对象
- 继承、多态、抽象基类
- 属性控制、描述符、元类
- 数据类

### ⚡ 异步与并发
- asyncio 协程
- 多线程、多进程
- concurrent.futures

### 🔮 元编程
- 魔法方法大全
- 动态属性拦截
- 上下文管理器

### 🚀 性能优化
- 性能分析工具
- 优化技巧
- 最佳实践

---

*文档版本：v1.0*  
*最后更新：2026 年 3 月*  
*适用版本：Python 3.8 - 3.12*
