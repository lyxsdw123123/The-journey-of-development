# -*- coding: utf-8 -*-
"""
1. Python 解释器执行流程 —— 可运行演示脚本
=====================================================

核心认知：Python 代码不是「直接执行」的，而是要经过一条流水线：

    .py 源码
        ↓
    词法分析 (Token)       —— 把字符切成一个个「词元」
        ↓
    语法分析 (AST)         —— 把词元组织成「抽象语法树」
        ↓
    编译                    —— 把语法树翻译成「字节码」
        ↓
    字节码 (Bytecode)      —— 一种面向虚拟机的中间形式
        ↓
    Python 虚拟机 (PVM)    —— 逐条解释执行字节码
        ↓
    CPU 执行                —— 最终由操作系统/硬件完成

运行方式：
    python "1. Python解释器执行流程.py"

配合同目录下的 markdown 文档一起学习，效果更好。
"""

import io
import sys
import ast
import dis
import time
import timeit
import tokenize

# 让 Windows 控制台用 UTF-8 正确显示中文输出
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except AttributeError:
    pass

SEP = "=" * 70
SUB = "-" * 70


def section(title):
    """打印一个醒目的章节标题，方便分段阅读输出。"""
    print()
    print(SEP)
    print(title)
    print(SEP)


# ----------------------------------------------------------------------
# 第 1 步：源码 (Source Code)
# ----------------------------------------------------------------------
section("第 1 步：源码（.py 文件里的纯文本）")

source = "a = 1\nb = a + 2\nprint(b)\n"
print("我们要分析的源码：")
print(source)

# ----------------------------------------------------------------------
# 第 2 步：词法分析 (Tokenization)
# ----------------------------------------------------------------------
section("第 2 步：词法分析 —— 切成 Token（词元）")

# tokenize 模块就是 CPython 内部词法分析器的公开接口。
# 它需要一个「逐行读入」的函数，这里用 StringIO 模拟（返回 str 行）。
readline = io.StringIO(source).readline

print(f"{'Token类型':<16} {'内容':<12} 位置")
print(SUB)
for tok in tokenize.generate_tokens(readline):
    # tok.type 是数字，tokenize.tok_name 把它翻译成人类可读的名字
    # tok.string 是这个词元对应的原始文本
    # tok.start 是 (行号, 列号) 元组
    print(f"{tokenize.tok_name[tok.type]:<18} {tok.string!r:<14} "
          f"第{tok.start[0]}行 第{tok.start[1]}列")

print()
print("观察：a、1、=、b、+、2、print 都被切成了独立的词元。")
print("这一步只关心「字符是什么」，还不关心「语法对不对」。")

# ----------------------------------------------------------------------
# 第 3 步：语法分析 (Parsing → AST)
# ----------------------------------------------------------------------
section("第 3 步：语法分析 —— 生成抽象语法树 (AST)")

tree = ast.parse(source)
print("AST 结构（缩进形式）：")
print(SUB)
print(ast.dump(tree, indent=2))

print()
print("观察：")
print("  * Module        —— 整个模块是根节点")
print("  * Assign        —— 赋值语句")
print("  * BinOp/Add     —— 加法运算")
print("  * Call          —— 函数调用 print(...)")
print("这一步只关心「结构对不对」，语法错误会在这一步被拦截。")

# ----------------------------------------------------------------------
# 第 4 步：编译 (Compile → Code Object)
# ----------------------------------------------------------------------
section("第 4 步：编译 —— AST 变成「代码对象」和「字节码」")

code_obj = compile(source, filename="<demo>", mode="exec")
print("编译得到的代码对象类型：", type(code_obj))
print("代码对象内部保存的常量 co_consts：", code_obj.co_consts)
print("代码对象内部保存的名字 co_names：  ", code_obj.co_names)
print("变量名列表 co_varnames：          ", code_obj.co_varnames)
print()
print("原始字节码（co_code，bytes 形式，机器不可读）：")
print("  ", code_obj.co_code)
print()
print("反汇编后的字节码（人类可读）：")
print(SUB)
dis.dis(code_obj)

print()
print("对照你参考里的例子：")
print("  x = 10        ->  LOAD_CONST 10 ; STORE_NAME x")
print("  y = x + 5     ->  LOAD_NAME x ; LOAD_CONST 5 ; BINARY_ADD ; STORE_NAME y")
print("字节码就是这种「基于栈」的中间指令，PVM 按顺序一条条执行。")

# ----------------------------------------------------------------------
# 第 5 步：函数与字节码（参考里的 dis.dis(add)）
# ----------------------------------------------------------------------
section("第 5 步：函数的字节码 —— 参考里的 dis.dis(add) 例子")


def add(a, b):
    return a + b


print("源码：def add(a, b): return a + b")
print()
print("dis.dis(add) 输出：")
print(SUB)
dis.dis(add)

print()
print("解读：")
print("  LOAD_FAST    a   —— 把局部变量 a 压入栈")
print("  LOAD_FAST    b   —— 把局部变量 b 压入栈")
print("  BINARY_ADD       —— 弹出栈顶两个值相加，结果再压回栈")
print("  RETURN_VALUE     —— 弹出栈顶作为函数返回值")
print()
print("注：不同 Python 版本里，BINARY_ADD 可能显示为 BINARY_OP/BINARY_ADD，")
print("    含义相同。这正是「字节码是版本相关的中间表示」的体现。")

# ----------------------------------------------------------------------
# 第 6 步：PVM 执行 —— 我们已经看到，字节码是被「解释」而非「编译成机器码」
# ----------------------------------------------------------------------
section("第 6 步：Python 虚拟机 (PVM) 逐条解释执行")

print("字节码不是 CPU 直接能懂的机器码，而是 PVM 的指令。")
print("PVM 是一个「大循环」：取指令 -> 解码 -> 执行 -> 取下一条。")
print()
print("下面用实际执行演示：把源码交给 exec（内部就走编译+P VM）：")
print(SUB)
namespace = {}
exec(source, namespace)  # 内部完成 编译 -> 字节码 -> PVM 执行
print(SUB)
print("上面 '3' 就是 PVM 执行 print(b) 的结果。")
print("PVM 执行时，每一行 LOAD/CALL/STORE 都有真实的时间开销。")

# ----------------------------------------------------------------------
# 第 7 步：为什么工程开发要懂字节码 —— 性能差异实验
# ----------------------------------------------------------------------
section("第 7 步：为什么工程开发要懂字节码（性能实验）")

N = 200_000

print(f"实验规模：N = {N:,}")
print()

# 方式 A：普通 for 循环 + append
def build_with_loop(n):
    result = []
    for i in range(n):
        result.append(i)
    return result


# 方式 B：列表推导式
def build_with_comprehension(n):
    return [i for i in range(n)]


# 先用 timeit 多次取最小时间，排除偶然抖动
loop_time = min(timeit.repeat(lambda: build_with_loop(N), number=20, repeat=3))
comp_time = min(timeit.repeat(lambda: build_with_comprehension(N), number=20, repeat=3))

print("普通 for 循环 + append 耗时：  %.4f 秒" % loop_time)
print("列表推导式耗时：              %.4f 秒" % comp_time)
print()
if comp_time > 0:
    speedup = loop_time / comp_time
    print("列表推导式大约快 %.2f 倍" % speedup)

print()
print("原因：")
print("  普通循环里，每一轮都要执行多次字节码指令：")
print("      LOAD_NAME result -> LOAD_METHOD append -> LOAD_FAST i -> CALL -> STORE ...")
print("  而且 append 是「动态查找的方法调用」，解释器很难优化。")
print()
print("  列表推导式是语言级语法，解释器知道你要干什么，")
print("  用专门的 LIST_APPEND 字节码完成，跳过了重复的方法查找和调用，")
print("  因此「解释器优化空间更大」。")
print()
print("看看两者的字节码数量差异：")
print(SUB)
print("for 循环 + append（核心部分）：")
dis.dis(build_with_loop)
print(SUB)
print("列表推导式：")
dis.dis(build_with_comprehension)

# ----------------------------------------------------------------------
# 第 8 步：高级开发者关注的三大成本
# ----------------------------------------------------------------------
section("第 8 步：高级 Python 开发者关注的三大成本")

print("1) 循环成本")
print("   每一轮循环都要执行一遍循环体内的多条字节码；")
print("   把热循环里的工作「向量化」或用内置函数（sum/map/推导式）能显著降低。")
print()
print("2) 函数调用成本")
print("   每次调用函数都要：压栈 -> 建立栈帧 -> 执行 -> 弹栈，")
print("   在极热路径里，函数调用本身可能比函数体还贵。")
print()
print("3) 对象创建成本")
print("   每个 int/list/dict 都要分配内存、初始化、最后还可能触发垃圾回收；")
print("   不必要的中间对象会让程序变慢、内存翻倍。")
print()
print("小结：读懂 dis.dis 输出，就是拿到了一份「性能透视报告」。")
print("当你怀疑某段代码慢时，先看它的字节码，再看算法。")

# ----------------------------------------------------------------------
section("运行结束 —— 建议下一步")
print("1. 打开同目录的 markdown 文档，系统回顾每一层。")
print("2. 自己写几行代码，用 tokenize / ast / dis 三件套去「解剖」它。")
print("3. 尝试：dis.dis(lambda: [x for x in range(10)]) 看看推导式字节码。")
