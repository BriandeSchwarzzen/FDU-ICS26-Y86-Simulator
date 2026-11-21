# -*- coding: utf-8 -*-
"""生成汇报用图：asumr.yo 控制流图 + 递归栈帧图（黑白极简风格）"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Polygon
import matplotlib.font_manager as fm

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

INK = '#111111'
GRAY = '#e8e8e8'
LGRAY = '#f5f5f5'
MGRAY = '#bbbbbb'
WHITE = '#ffffff'

def box(ax, x, y, w, h, text, fc=LGRAY, fs=10.5, lw=1.4, bold_first=True):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
        boxstyle='round,pad=0.008,rounding_size=0.02',
        fc=fc, ec=INK, lw=lw))
    lines = text.split('\n')
    if bold_first and len(lines) > 1:
        ax.text(x+w/2, y+h-0.13, lines[0], ha='center', va='top',
                fontsize=fs+1, fontweight='bold', color=INK, family='Microsoft YaHei')
        body = '\n'.join(lines[1:])
        ax.text(x+w/2, y+h-0.155, body, ha='center', va='top',
                fontsize=fs-1.5, color=INK, family='Microsoft YaHei')
    else:
        ax.text(x+w/2, y+h/2, text, ha='center', va='center',
                fontsize=fs, color=INK, family='Microsoft YaHei')

def arrow(ax, x1, y1, x2, y2, style='-|>', ls='-', lw=1.6, color=INK,
          label=None, lx=0.015, ly=0.015, lfs=9.5, rad=0.0, lpos=None):
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style,
                        mutation_scale=16, lw=lw, color=color,
                        linestyle=ls, connectionstyle=f'arc3,rad={rad}')
    ax.add_patch(a)
    if label:
        if lpos is None:
            lx, ly = lx, ly
        ax.text(x1 + (x2-x1)*0.5 + lx, y1 + (y2-y1)*0.5 + ly, label,
                fontsize=lfs, color=INK, family='Microsoft YaHei',
                ha='center', va='center', backgroundcolor='white')

# ============================================================
# 图 1: asumr.yo 控制流图
# ============================================================
fig, ax = plt.subplots(figsize=(11.5, 7.6), dpi=200)
ax.set_xlim(0, 11.5); ax.set_ylim(0, 7.6); ax.axis('off')

# --- 启动与 main 列（左） ---
box(ax, 0.4, 6.5, 2.9, 0.85, '0x000  启动\nirmovq 0x200, %rsp    # 设栈顶')
box(ax, 0.4, 5.3, 2.9, 0.85, '0x00a  call main\n压返回地址 0x13, 跳 0x38')
box(ax, 0.4, 4.15, 2.9, 0.85, '0x013  halt', fc=GRAY)
box(ax, 0.4, 2.75, 2.9, 1.55, '0x038  main\nirmovq array, %rdi\nirmovq $4, %rsi\n0x04c call rsum')
box(ax, 0.4, 1.6, 2.9, 0.85, '0x055  ret\n返回地址 0x13 → halt')

arrow(ax, 1.85, 6.5, 1.85, 6.15)
arrow(ax, 1.85, 5.3, 1.85, 5.0)
arrow(ax, 1.85, 4.15, 1.85, 4.30, lw=1.2, ls=':', color='#666666')
arrow(ax, 1.85, 4.30, 1.85, 2.75, lw=1.2, ls=':', color='#666666')
arrow(ax, 1.85, 2.75, 1.85, 2.45)

# --- rsum 列（右） ---
box(ax, 7.6, 5.9, 3.4, 1.3, '0x056  rsum 入口\nxorq %rax, %rax   # sum=0\nandq %rsi, %rsi   # 设 CC')
# 菱形 jle
dia = Polygon([(9.3, 5.25), (10.15, 4.85), (9.3, 4.45), (8.45, 4.85)],
              closed=True, fc='white', ec=INK, lw=1.4)
ax.add_patch(dia)
ax.text(9.3, 4.85, '0x05a\njle return?\n(count≤0)', ha='center', va='center',
        fontsize=9.5, family='Microsoft YaHei', color=INK)
box(ax, 7.6, 2.9, 3.4, 1.25, '0x063-0x085  递归体\npushq %rbx    # 保存\nmrmovq (%rdi), %rbx\ncount--, start++')
box(ax, 7.6, 1.6, 3.4, 0.9, '0x087  call rsum\n# 递归：压返回地址 0x90')
box(ax, 7.6, 0.4, 3.4, 0.85, '0x090  addq %rbx, %rax\npopq %rbx    # 恢复')
box(ax, 4.55, 0.4, 2.0, 0.85, '0x094  ret\n返回上层调用点', fc=GRAY)

# main -> rsum 入口
arrow(ax, 3.3, 3.5, 7.6, 6.3, rad=0.15, label='call rsum(4)')
# 入口 -> 菱形
arrow(ax, 9.3, 5.9, 9.3, 5.42)
# 菱形 -> 递归体（否）
arrow(ax, 8.7, 4.45, 8.7, 4.15, label='否 (count>0)', lx=-0.62, ly=0.05)
# 递归体 -> call rsum
arrow(ax, 9.3, 2.9, 9.3, 2.5)
# call rsum -> 入口（递归回边）
arrow(ax, 11.0, 2.05, 11.55, 6.5, rad=0.42, label='递归调用 rsum(count-1)',
      lx=-0.55, ly=1.7, lw=1.8)
# ret -> addq（返回 0x90）
arrow(ax, 6.55, 0.85, 7.6, 0.85, label='返回地址 0x90', ly=0.16)
# 菱形 -> ret（是, jle 提前返回）
arrow(ax, 8.45, 4.85, 6.9, 1.0, rad=-0.12, ls='--', lw=1.5,
      label='是 (count=0): 提前返回', lx=1.3, ly=-0.35)
# addq -> ret
arrow(ax, 9.3, 0.4, 6.55, 0.4)
# 顶层返回链：main ret -> halt
arrow(ax, 1.85, 1.6, 1.85, 0.0, lw=1.2, ls=':', color='#666666')
arrow(ax, 1.85, 0.0, 0.3, 0.0, lw=1.2, ls=':', color='#666666')
ax.text(0.9, -0.28, 'main 的 ret 经 0x55 返回 0x13 (halt)', fontsize=9,
        family='Microsoft YaHei', color='#666666')

ax.text(5.75, 7.35, 'asumr.yo 控制流：main → rsum 递归 4 层 → ret 链返回',
        ha='center', fontsize=14, fontweight='bold', color=INK, family='Microsoft YaHei')
plt.tight_layout()
plt.savefig('assets/control_flow.png', bbox_inches='tight', facecolor='white')
plt.close()

# ============================================================
# 图 2: 递归栈帧图（最深时刻 rsp=0x1b0）
# ============================================================
fig, ax = plt.subplots(figsize=(7.0, 5.6), dpi=200)
ax.set_xlim(0, 7); ax.set_ylim(0, 5.6); ax.axis('off')

frames = [
    (0x1f8, '0x13', 'call main 的返回地址', GRAY),
    (0x1f0, '0x55', 'main → rsum(4) 的返回地址', GRAY),
    (0x1e8, 'rbx1', 'rsum(4) 保存的 %rbx 第1层', LGRAY),
    (0x1e0, '0x90', '递归 rsum(3) 的返回地址', LGRAY),
    (0x1d8, 'rbx2', 'rsum(3) 保存的 %rbx 第2层', LGRAY),
    (0x1d0, '0x90', '递归 rsum(2) 的返回地址', LGRAY),
    (0x1c8, 'rbx3', 'rsum(2) 保存的 %rbx 第3层', LGRAY),
    (0x1c0, '0x90', '递归 rsum(1) 的返回地址', LGRAY),
    (0x1b8, 'rbx4', 'rsum(1) 保存的 %rbx 第4层', LGRAY),
    (0x1b0, '0x90', '递归 rsum(0) 的返回地址', LGRAY),
]
x0, w = 0.6, 2.6
top = 5.15
hh = 0.44
ax.text(x0+w/2, top+0.18, '递归最深时 (rsp=0x1b0) 的栈', ha='center',
        fontsize=12.5, fontweight='bold', family='Microsoft YaHei')
ax.text(x0+w+0.35, top+0.18, '0x200  初始栈顶', fontsize=9.5, va='center',
        family='Microsoft YaHei', color='#555555')
for i, (addr, val, desc, fc) in enumerate(frames):
    y = top - 0.2 - i*hh
    ax.add_patch(FancyBboxPatch((x0, y), w, hh-0.06,
        boxstyle='round,pad=0.005,rounding_size=0.015', fc=fc, ec=INK, lw=1.0))
    ax.text(x0+w/2, y+(hh-0.06)/2, val, ha='center', va='center',
            fontsize=10.5, fontweight='bold', family='Microsoft YaHei')
    ax.text(x0+w+0.35, y+(hh-0.06)/2, f'{addr:#x}  {desc}', fontsize=9.5,
            va='center', family='Microsoft YaHei', color='#333333')

yend = top - 0.2 - len(frames)*hh - 0.05
arrow(ax, x0+w/2, yend, x0+w/2, yend-0.3, label='', lw=1.2, color='#666666')
ax.text(x0+w/2, yend-0.38, 'rsp ↓ 向低地址增长', fontsize=9.5, ha='center',
        family='Microsoft YaHei', color='#666666')
ax.text(4.4, 2.4, '每层递归栈帧 = 16 字节：\n8B 返回地址 (call 压入)\n8B 保存的 %rbx (pushq 压入)\n\nret / popq 弹栈只移动 %rsp，\n不清除内存内容',
        fontsize=10.5, family='Microsoft YaHei', va='center', color='#222222',
        linespacing=1.9)
plt.tight_layout()
plt.savefig('assets/stack_frames.png', bbox_inches='tight', facecolor='white')
plt.close()

# ============================================================
# 图 3: 六阶段数据通路总览
# ============================================================
fig, ax = plt.subplots(figsize=(11.5, 3.9), dpi=200)
ax.set_xlim(0, 11.5); ax.set_ylim(0, 3.9); ax.axis('off')

stages = [
    ('fetch\n取指', 'icode ifun rA rB\nvalC valP'),
    ('decode\n译码', 'valA valB'),
    ('execute\n执行', 'valE Cnd\n条件码'),
    ('memory\n访存', 'valM'),
    ('write_back\n写回', 'REG'),
    ('update_pc\n更新PC', 'PC'),
]
w, h, y = 1.62, 1.15, 1.55
gap = 0.33
x = 0.35
for i, (name, out) in enumerate(stages):
    box(ax, x, y, w, h, name, fc=WHITE if i % 2 == 0 else LGRAY, fs=11.5, bold_first=False)
    ax.text(x + w/2, y - 0.16, out, ha='center', va='top', fontsize=9.5,
            family='Microsoft YaHei', color='#333333')
    if i < 5:
        arrow(ax, x + w + 0.02, y + h/2, x + w + gap - 0.02, y + h/2)
    x += w + gap
# 循环回边
arrow(ax, x - gap/2 + 0.1, y + h + 0.02, 0.35 + 0.1, y + h + 0.02, rad=-0.32, lw=1.4)
ax.text(5.9, 3.35, '一个时钟周期执行一条指令（顺序执行，非流水）', ha='center',
        fontsize=11.5, family='Microsoft YaHei', color='#333333')
ax.text(5.9, 0.55, '阶段之间用暂存器（valP/valA/valB/valE/valM/Cnd）传递数据，machine state（PC/REG/CC/MEM/STAT）跨周期保持',
        ha='center', fontsize=10, family='Microsoft YaHei', color='#555555')
plt.tight_layout()
plt.savefig('assets/pipeline.png', bbox_inches='tight', facecolor='white')
plt.close()
print('figs done')
