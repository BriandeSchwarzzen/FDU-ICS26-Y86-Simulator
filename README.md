# Y86-64 Simulator (Python 框架)

## 简介

本项目实现一个 Y86-64 指令集 CPU 模拟器（软件层面的顺序执行处理器）。`cpu.py` 中已搭建好文件解析器（Parser）和主循环骨架，六个执行阶段（fetch / decode / execute / memory / write_back / update_pc）的核心数据通路逻辑在 `cpu.py` 中实现。

```bash
.
├─ test/           # 测试指令文件 (.yo 机器码文件)
├─ answer/         # 指令执行的标准结果快照 (.json)
├─ test.py         # 自动化评测脚本：运行模拟器 + 严格比对结果
├─ assets/         # 汇报演示文稿与配图
└─ cpu.py          # 模拟器源代码（六阶段实现）
```

## 实现说明

- 12 类指令（icode 0~B）全覆盖：halt / nop / rrmovq / cmovXX / irmovq / rmmovq / mrmovq / OPq / jXX / call / ret / pushq / popq
- 顺序执行六阶段状态机：每周期按 fetch → decode → execute → memory → write_back → update_pc 执行一条指令，每周期记录一次状态快照（CC / MEM / PC / REG / STAT）
- 栈语义：`pushq %rsp` 压入旧栈指针值；`popq %rsp` 时内存读出的值覆盖递增后的 %rsp
- 异常处理：非法指令 → INS；取指 / 访存越界 → ADR（非法读返回 0、非法写静默拦截）；memory 阶段触发 ADR 后 write_back 仍执行

## 测试方法

请确保在 Python 3 环境下运行。使用以下命令进行自动化测试与评分：

```bash
python test.py --bin "python cpu.py"
```

如果你只想测试单个文件以观察输出格式，可以使用标准输入重定向：
```bash
python cpu.py < test/asumr.yo
```

## 测试结果

全部 21 个官方测试用例通过（60/60 基础分）。
