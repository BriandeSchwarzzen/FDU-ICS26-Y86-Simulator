# -*- coding: utf-8 -*-
"""生成 Y86-64 Simulator 汇报演示文稿（黑白极简，16:9，大字号短要点）"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
import copy

BLACK = RGBColor(0x11, 0x11, 0x11)
DGRAY = RGBColor(0x55, 0x55, 0x55)
GRAY  = RGBColor(0x99, 0x99, 0x99)
LGRAY = RGBColor(0xE8, 0xE8, 0xE8)
MGRAY = RGBColor(0xCC, 0xCC, 0xCC)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)

FONT = 'Microsoft YaHei'
MONO = 'Consolas'

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]

def _set_run(run, text, size, bold=False, color=BLACK, font=FONT, italic=False):
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    run.font.name = font
    rPr = run._r.get_or_add_rPr()
    ea = rPr.find(qn('a:ea'))
    if ea is None:
        ea = rPr.makeelement(qn('a:ea'), {})
        rPr.append(ea)
    ea.set('typeface', font)

def new_slide():
    return prs.slides.add_slide(BLANK)

def add_text(slide, l, t, w, h, lines, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    """lines: list of (text, size, bold, color) or list of dict runs per line"""
    tb = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    first = True
    for line in lines:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.alignment = align
        p.space_after = Pt(6)
        if isinstance(line, tuple):
            line = [line]
        for tup in line:
            txt, size, bold, color = tup[:4]
            font = tup[4] if len(tup) > 4 else FONT
            r = p.add_run()
            _set_run(r, txt, size, bold, color, font)
    return tb

def add_box(slide, l, t, w, h, fill=WHITE, line_color=BLACK, line_w=1.2):
    sh = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                                Inches(l), Inches(t), Inches(w), Inches(h))
    sh.adjustments[0] = 0.08
    sh.fill.solid()
    sh.fill.fore_color.rgb = fill
    sh.line.color.rgb = line_color
    sh.line.width = Pt(line_w)
    sh.shadow.inherit = False
    return sh

def add_arrow(slide, l, t, w, h):
    sh = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW,
                                Inches(l), Inches(t), Inches(w), Inches(h))
    sh.fill.solid(); sh.fill.fore_color.rgb = BLACK
    sh.line.fill.background()
    sh.shadow.inherit = False
    return sh

def add_title(slide, text, num=None):
    add_text(slide, 0.55, 0.32, 12.2, 0.8, [(text, 30, True, BLACK)])
    # 顶部细线
    ln = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                                Inches(0.55), Inches(1.12), Inches(12.23), Pt(2.2))
    ln.fill.solid(); ln.fill.fore_color.rgb = BLACK
    ln.line.fill.background(); ln.shadow.inherit = False
    if num is not None:
        add_text(slide, 12.35, 0.40, 0.8, 0.6, [(num, 16, False, GRAY)], align=PP_ALIGN.RIGHT)

def add_notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text

def bullets(slide, items, l=0.85, t=1.45, w=11.6, h=5.6, size=19, gap=10):
    """items: list of (主文, [缩进子文, ...]) or str"""
    tb = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = tb.text_frame; tf.word_wrap = True
    first = True
    for it in items:
        if isinstance(it, tuple):
            main, subs = it
        else:
            main, subs = it, []
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.space_after = Pt(gap)
        r = p.add_run(); _set_run(r, '■  ' + main, size, True, BLACK)
        for s in subs:
            sp = tf.add_paragraph()
            sp.space_after = Pt(gap - 4)
            sr = sp.add_run(); _set_run(sr, '      ' + s, size - 2, False, DGRAY)
    return tb

# ============================================================
# 1. 封面
# ============================================================
s = new_slide()
add_text(s, 0.85, 2.2, 11.6, 1.2, [('Y86-64 CPU 模拟器', 48, True, BLACK)])
add_text(s, 0.85, 3.35, 11.6, 0.7, [('顺序执行 · 六阶段数据通路 · Python 实现', 22, False, DGRAY)])
add_text(s, 0.85, 4.35, 11.6, 0.6, [('计算机系统基础（ICS）课程项目汇报', 18, False, GRAY)])
add_text(s, 0.85, 5.6, 11.6, 0.6, [('姓名：____________    学号：____________    班级：AIE210006', 18, False, BLACK)])
add_text(s, 0.85, 6.4, 11.6, 0.5, [('2026 年 11 月', 14, False, GRAY)])
add_notes(s, '开场：各位老师同学好，我汇报的是 ICS 课程项目——用 Python 实现的 Y86-64 顺序执行 CPU 模拟器。')

# ============================================================
# 2. 汇报路线
# ============================================================
s = new_slide()
add_title(s, '汇报路线', '2')
add_box(s, 0.85, 1.6, 2.85, 1.9, fill=LGRAY)
add_text(s, 0.95, 1.78, 2.65, 1.6, [
    [('① 指令分类与数据流', 16, True, BLACK)],
    [('12 类指令 · 六阶段', 13, False, DGRAY)],
    [('2–3 分钟', 13, False, GRAY)],
])
add_box(s, 3.95, 1.6, 2.85, 1.9, fill=LGRAY)
add_text(s, 4.05, 1.78, 2.65, 1.6, [
    [('② 印象深刻之处', 16, True, BLACK)],
    [('实现中的坑与语义', 13, False, DGRAY)],
    [('1 分钟', 13, False, GRAY)],
])
add_box(s, 7.05, 1.6, 2.85, 1.9, fill=LGRAY)
add_text(s, 7.15, 1.78, 2.65, 1.6, [
    [('③ 现场演示', 16, True, BLACK)],
    [('asumr.yo 控制流', 13, False, DGRAY)],
    [('1–2 分钟', 13, False, GRAY)],
])
add_box(s, 10.15, 1.6, 2.6, 1.9, fill=LGRAY)
add_text(s, 10.25, 1.78, 2.4, 1.6, [
    [('④ 源码细讲', 16, True, BLACK)],
    [('六阶段任选其一', 13, False, DGRAY)],
    [('1–2 分钟', 13, False, GRAY)],
])
add_text(s, 0.85, 4.1, 11.6, 2.0, [
    [('演示环境：python cpu.py < test/asumr.yo', 17, False, BLACK, MONO)],
    [('全部 21 个官方测试用例通过（60/60 基础分）', 17, False, BLACK)],
], align=PP_ALIGN.CENTER)
add_notes(s, '一句话预告结构。总共控制在 8 分钟以内。')

# ============================================================
# 3. 12 类指令分类
# ============================================================
s = new_slide()
add_title(s, 'Y86-64 指令集：12 类指令', '3')
add_text(s, 0.85, 1.35, 11.6, 0.5, [
    [('每条指令 1 字节操作码 = icode(高4位) + ifun(低4位)，icode 0~B 共 12 类', 17, False, DGRAY)],
])
groups = [
    ('系统控制', ['halt —— 停机（STAT=HLT）', 'nop —— 空操作，只推进 PC']),
    ('数据传送', ['rrmovq rA, rB —— 寄存器间传送', 'irmovq V, rB —— 立即数装入寄存器', 'rmmovq / mrmovq —— 寄存器 ⇄ 内存']),
    ('条件传送', ['cmovXX rA, rB —— 条件成立才写 rB（le/l/e/ne/ge/g）']),
    ('算术逻辑 OPq', ['addq / subq / andq / xorq —— 同时更新条件码 ZF SF OF']),
    ('跳转 jXX', ['jmp / jle / jl / je / jne / jge / jg —— 决定 PC 走 valC 还是 valP']),
    ('栈与函数调用', ['pushq / popq —— 隐式操作 %rsp', 'call / ret —— 压入弹出返回地址']),
]
y = 1.95
for name, items in groups:
    add_box(s, 0.85, y, 2.3, 0.78, fill=LGRAY, line_w=1.0)
    add_text(s, 0.95, y + 0.16, 2.1, 0.5, [(name, 15, True, BLACK)], align=PP_ALIGN.CENTER)
    txt = '\n'.join('· ' + i for i in items)
    add_text(s, 3.35, y + 0.07, 9.4, 0.72, [(txt, 12.5, False, BLACK)])
    y += 0.86
add_notes(s, '分类要点：CSAPP 图 4-2 共 12 行，rrmovq 与 cmovXX 共用 icode 2（ifun=0 是 rrmovq，1~6 是 cmov），OPq 与 jXX 也靠 ifun 区分变体。汇报时用自然语言讲：我按"有没有数据、数据经过哪几站"来分组。')

# ============================================================
# 4. 六阶段数据通路总览
# ============================================================
s = new_slide()
add_title(s, '六阶段顺序数据通路：一条指令的旅程', '4')
stages = [
    ('fetch', '取指', 'icode ifun\nrA rB valC\nvalP'),
    ('decode', '译码', 'valA valB'),
    ('execute', '执行', 'valE Cnd\n条件码 CC'),
    ('memory', '访存', 'valM'),
    ('write_back', '写回', 'REG'),
    ('update_pc', '更新PC', 'PC'),
]
w, h, y, gap = 1.72, 1.35, 1.75, 0.34
x = 0.7
for i, (en, cn, data) in enumerate(stages):
    add_box(s, x, y, w, h, fill=WHITE)
    add_text(s, x, y + 0.12, w, 0.75, [
        [(en, 15, True, BLACK)],
        [(cn, 13, False, DGRAY)],
    ], align=PP_ALIGN.CENTER)
    add_text(s, x + 0.05, y + h + 0.08, w - 0.1, 0.75, [(data, 11, False, DGRAY)], align=PP_ALIGN.CENTER)
    if i < 5:
        add_arrow(s, x + w + 0.02, y + 0.52, gap - 0.04, 0.32)
    x += w + gap
add_text(s, 0.7, 4.55, 12.0, 1.0, [
    [('每个时钟周期：六阶段依次执行完一条指令，再开始下一条（顺序、非流水）', 17, True, BLACK)],
    [('阶段之间用暂存器传数据 —— valP/valA/valB/valE/valM/Cnd 是数据通路的核心', 15, False, DGRAY)],
], align=PP_ALIGN.CENTER)
add_text(s, 0.7, 5.6, 12.0, 0.9, [
    [('run() 主循环：STAT 为 AOK 时循环 { fetch → decode → execute → memory → write_back → update_pc }，每周期记录一次状态快照', 14, False, GRAY, MONO)],
], align=PP_ALIGN.CENTER)
add_notes(s, '这是整场汇报的主线。后面每一类指令都回到这张图：数据从哪一站进、经哪些暂存器、从哪一站出。')

# ============================================================
# 5. 数据传送类
# ============================================================
s = new_slide()
add_title(s, '类别① 数据传送：数据如何流动', '5')
bullets(s, [
    ('irmovq V, rB（最短路径）', ['fetch 读出 8 字节常数 → valC', 'execute：valE = valC', 'write_back：valE → %rb']),
    ('rrmovq rA, rB', ['decode：valA = R[rA]', 'execute：valE = valA', 'write_back：valE → R[rB]']),
    ('rmmovq rA, D(rB)（寄存器 → 内存）', ['execute：valE = valB + valC（有效地址）', 'memory：把 valA 写入内存 [valE]', '不写回寄存器']),
    ('mrmovq D(rB), rA（内存 → 寄存器）', ['execute：valE = valB + valC', 'memory：valM = 内存 [valE]', 'write_back：valM → R[rA]']),
    ('cmovXX rA, rB（条件传送）', ['路径与 rrmovq 相同，但 write_back 由 Cnd 把关', '条件不成立 → 不写，数据被"挡住"']),
], size=17, gap=8)
add_notes(s, '要点：所有数据都先进暂存器 valX，再由下一站取用；访存指令的地址在 execute 算好，memory 只负责读写。cmovXX 是唯一"带开关"的传送。')

# ============================================================
# 6. OPq 与条件码
# ============================================================
s = new_slide()
add_title(s, '类别② 算术逻辑 OPq 与条件码', '6')
bullets(s, [
    ('decode：valA = R[rA]，valB = R[rB]（两个源操作数）', []),
    ('execute：按 ifun 计算 —— addq / subq / andq / xorq → valE', ['subq 是 valB − valA（汇编里 subq %r10,%r11 得到 %r11−%r10）']),
    ('同步更新条件码（只有 OPq 会改条件码）', ['ZF：结果是否为 0', 'SF：结果的符号位（第 63 位）', 'OF：带符号溢出 —— 同号相加结果变号、异号相减结果变号']),
    ('write_back：valE → R[rB]', []),
    ('jXX / cmovXX 在 execute 用 check_cond(ifun) 组合三个条件码 → Cnd', []),
], size=17, gap=8)
add_notes(s, 'OF 判定要先用补码解释操作数。条件码是"上一条 OPq 留下的痕迹"，jXX/cmovXX 消费它。')

# ============================================================
# 7. 跳转类
# ============================================================
s = new_slide()
add_title(s, '类别③ 跳转 jXX：PC 的二选一', '7')
bullets(s, [
    ('fetch：读出目标地址 → valC；同时算出顺序下一条 → valP', []),
    ('execute：Cnd = check_cond(ifun)（jmp 的 ifun=0，恒成立）', []),
    ('update_pc：PC = Cnd ? valC : valP', ['成立 → 跳走（控制流改变）', '不成立 → 顺序执行']),
    ('跳转指令不读不写寄存器、不动内存', ['只消费条件码，只影响 PC']),
], size=19, gap=12)
add_notes(s, '关键：fetch 阶段 valC 和 valP 都要算出来备着，最后一步才二选一。条件码由之前的 OPq 设置（如 andq %rsi,%rsi 自与测零）。')

# ============================================================
# 8. 栈与调用类
# ============================================================
s = new_slide()
add_title(s, '类别④ 栈与函数调用：隐式操作 %rsp', '8')
bullets(s, [
    ('pushq rA', ['decode：valA = R[rA]，valB = R[%rsp]', 'execute：valE = %rsp − 8', 'memory：valA 写入 [valE]；write_back：valE → %rsp']),
    ('popq rA', ['decode：valA = %rsp（读内存的地址）', 'execute：valE = %rsp + 8', 'memory：valM = 内存 [valA]', 'write_back：%rsp ← valE，R[rA] ← valM']),
    ('call Dest', ['execute：valE = %rsp − 8；memory：把 valP（返回地址）写入 [valE]', 'update_pc：PC = valC（进入被调函数）']),
    ('ret', ['memory：valM = 内存 [%rsp]；execute：valE = %rsp + 8', 'write_back：valE → %rsp；update_pc：PC = valM（返回）']),
], size=16, gap=9)
add_notes(s, '这四条指令的 srcA/srcB 在 decode 由 icode 隐式指定为 %rsp，不来自寄存器指示符字节。call 压返回地址、ret 弹出到 PC。')

# ============================================================
# 9. 印象深刻 ①
# ============================================================
s = new_slide()
add_title(s, '印象深刻 ①：栈操作的"歧义语义"', '9')
bullets(s, [
    ('pushq %rsp 压入的是旧值还是新值？', ['规范：压入修改前的旧栈指针', '实现顺序天然满足：decode 先把旧 %rsp 读进 valA → memory 写 valA → write_back 才更新 %rsp']),
    ('popq %rsp：%rsp 同时是目标寄存器和栈指针', ['规范：内存读出的值必须覆盖"加 8 后的 %rsp"', '实现：write_back 先写 valE（%rsp+8），再写 valM —— 顺序即语义']),
    ('这让我意识到：六阶段的先后次序本身承载了架构语义', []),
], size=18, gap=12)
add_notes(s, '讲自己动手时的理解过程：初看以为是规范在"规定特例"，实现完才发现是六阶段顺序的自然结果，不需要任何特判。')

# ============================================================
# 10. 印象深刻 ②
# ============================================================
s = new_slide()
add_title(s, '印象深刻 ②：我踩过的坑与异常语义', '10')
bullets(s, [
    ('ret 的返回地址只进 PC，不写回 %rsp', ['我最初把 valM 也写回了 %rsp —— 栈指针被返回地址覆盖，程序跑飞', '对照 CSAPP 的 HCL 才发现 dstM 只包含 mrmovq/popq，ret 不在其中']),
    ('ADR 异常后 write_back 仍执行', ['memory 阶段写越界 → STAT=ADR，但 %rsp 的递减仍照常写回，随后才停机（模板已实现）', '异常后：非法读返回 0，非法写被静默拦截']),
    ('OF 的判定必须用带符号解释', ['64 位补码运算：同号相加变号、异号相减变号才算溢出']),
], size=17, gap=11)
add_notes(s, '第二个坑是真实调试经历：跑 asum.yo 时 rsp 变成 0x55（返回地址），逐状态对比才发现。这页讲"调试方法"：答案 JSON 是逐周期快照，二分定位。')

# ============================================================
# 11. 演示：asumr.yo 功能与控制流
# ============================================================
s = new_slide()
add_title(s, '现场演示：asumr.yo 递归求和', '11')
add_text(s, 0.85, 1.3, 11.6, 0.9, [
    [('功能：rsum(array, 4) 递归求和，4 层递归，63 个时钟周期，最终 %rax = 0xABCDABCDABCD', 17, True, BLACK)],
])
add_pic_w = 8.0
s.shapes.add_picture('assets/control_flow.png', Inches((13.333 - add_pic_w) / 2), Inches(1.95), width=Inches(add_pic_w))
add_notes(s, '先演示：python cpu.py < test/asumr.yo。再讲控制流：0x00a call main → 0x038 main 传参 → 0x04c call rsum → rsum 内 count≤0 时 jle 提前返回，否则 pushq %rbx、读元素、count--/start++、递归 call 自己 → 返回 0x090 加和、popq %rbx、ret 回上层。递归 4 层后沿 ret 链原路返回，最终回到 halt。')

# ============================================================
# 12. 演示：运行结果与栈
# ============================================================
s = new_slide()
add_title(s, '现场演示：栈帧与最终状态', '12')
add_text(s, 0.85, 1.3, 11.6, 0.9, [
    [('最终：%rax = 0xABCDABCDABCD  ✔   %rsp = 0x200 栈平衡  ✔   STAT = HLT，PC = 0x13', 17, True, BLACK)],
])
s.shapes.add_picture('assets/stack_frames.png', Inches(0.9), Inches(2.1), width=Inches(5.6))
add_text(s, 7.0, 2.3, 5.6, 3.6, [
    [('trace 里的细节', 17, True, BLACK)],
    [('· 每周期一个状态快照，共 63 个', 14, False, DGRAY)],
    [('· 返回地址 0x13 / 0x55 / 0x90 仍残留在栈区 —— 弹栈只移动 %rsp，不清内存', 14, False, DGRAY)],
    [('· 每层递归栈帧 16B = 8B 返回地址 + 8B 保存的 %rbx', 14, False, DGRAY)],
])
add_notes(s, '演示时可以 tail 看 trace 末尾：PC=0x13、STAT=2、rax=0xABCDABCDABCD。若 TA 问数据：0x000d000d000d+0x00c000c000c0+0x0b000b000b00+0xa000a000a000=0xABCDABCDABCD。')

# ============================================================
# 13. 源码总览
# ============================================================
s = new_slide()
add_title(s, '源码总览：一个类，六个方法', '13')
add_text(s, 0.85, 1.4, 11.6, 1.0, [
    [('Y86Simulator 类 —— 机器状态 + 数据通路 + 六个阶段方法', 18, True, BLACK)],
])
bullets(s, [
    ('机器状态', ['memory（8192B 字节数组）、PC、STAT（AOK/HLT/ADR/INS）', 'REG（15 个 64 位寄存器文件）、CC（ZF/SF/OF 条件码）']),
    ('数据通路暂存器', ['icode ifun rA rB valC valP valA valB valE valM Cnd —— 阶段间传数据的"寄存器"']),
    ('run() 主循环', ['每周期顺序调用六个阶段，每周期 dump_state() 记录 CC/MEM/PC/REG/STAT 快照 → trace']),
    ('read_mem / write_mem', ['所有内存访问的唯二入口，越界统一置 STAT=ADR，非法读返回 0、非法写静默拦截']),
], t=2.5, h=4.8, size=16, gap=10)
add_notes(s, '强调分层：辅助方法（符号扩展/截断/条件判断）→ 六个阶段 → run 主循环 → trace 输出。这样 TA 点任意阶段都能展开。')

# ============================================================
# 14-19. 六个阶段
# ============================================================
stages = [
    ('阶段 1 · Fetch 取指', '14', [
        ('输入：PC', ['输出：icode ifun rA rB valC valP']),
        ('按需读字节：1B 操作码 → 1B 寄存器指示符 → 8B 常数（小端）', ['need_reg / need_valC 由 icode 决定']),
        ('valP = PC + 指令长度（顺序下一条，跳转与否由 update_pc 决定）', []),
        ('异常出口：PC 越界 → ADR；opcode > 0xB → INS；halt → HLT，立即停机', []),
    ]),
    ('阶段 2 · Decode 译码', '15', [
        ('读寄存器文件：valA = R[srcA]，valB = R[srcB]', ['srcA/srcB 由 icode 查表：OPq 取 rA/rB，rmmovq 取 rA/rB，mrmovq 只取 rB …']),
        ('隐式 %rsp：pushq 的 srcB、popq 的 srcA/srcB、call 的 srcB、ret 的 srcA/srcB', []),
        ('无源操作数（RNONE=0xF）读 0', ['REG[15] 恒为 0']),
    ]),
    ('阶段 3 · Execute 执行', '16', [
        ('ALU 操作数选择：OPq→(valB,valA)；访存→(valB,valC)；栈→(valB,±8)；传送→(0,valA/valC)', []),
        ('OPq 按 ifun 运算并更新 CC：ZF/SF/OF（补码溢出判定）', []),
        ('jXX / cmovXX：Cnd = check_cond(ifun) —— 三条件码的布尔组合', []),
        ('结果统一放 valE（uint64 截断）', []),
    ]),
    ('阶段 4 · Memory 访存', '17', [
        ('写内存：rmmovq 写 valA；pushq 写 valA（旧值）；call 写 valP（返回地址）', ['地址都是 execute 算好的 valE']),
        ('读内存：mrmovq 读 [valE]；popq / ret 读 [valA]（旧 %rsp 指向处）→ valM', []),
        ('越界：STAT=ADR，非法读返回 0、非法写静默拦截', []),
    ]),
    ('阶段 5 · Write Back 写回', '18', [
        ('dstE → valE：rB（rrmovq/irmovq/OPq）或 %rsp（栈类）', ['cmovXX 条件不成立则 dstE 置 RNONE，不写']),
        ('dstM → valM：rA（mrmovq/popq）', ['注意：ret 没有 dstM —— 返回地址只进 PC']),
        ('写入顺序：先 valE 后 valM', ['保证 popq %rsp 时内存值覆盖 %rsp+8 —— 规范要求']),
    ]),
    ('阶段 6 · Update PC 更新 PC', '19', [
        ('四分支选择下一个 PC', ['call → valC（调用目标）', 'jXX → Cnd ? valC : valP', 'ret → valM（返回地址）', '其余 → valP（顺序执行）']),
        ('本阶段只改 PC，不碰寄存器与内存', []),
    ]),
]
for title, num, items in stages:
    s = new_slide()
    add_title(s, title, num)
    bullets(s, items, size=18, gap=12)
    add_notes(s, 'TA 若选此阶段：先讲职责一句话，再讲关键字段（数据结构），再讲方法逻辑，最后讲边界情况。详细讲稿见 Obsidian 汇报稿。')

# ============================================================
# 20. 结束
# ============================================================
s = new_slide()
add_text(s, 0.85, 2.6, 11.6, 1.2, [('谢谢，请老师和同学们指正', 40, True, BLACK)], align=PP_ALIGN.CENTER)
add_text(s, 0.85, 4.0, 11.6, 0.7, [('代码仓库：FDU-ICS26-Y86-Simulator（GitHub）', 16, False, DGRAY)], align=PP_ALIGN.CENTER)
add_notes(s, '结束。等待 TA 提问。')

prs.save('assets/Y86-64模拟器汇报.pptx')
print('ppt done, slides:', len(prs.slides.__iter__.__self__._sldIdLst))
