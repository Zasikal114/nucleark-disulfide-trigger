# -*- coding: utf-8 -*-
"""
学推海报补图：① 构建体架构与 GSH 响应原理图  ② 干实验设计工具包总览图
风格对齐 ZF 罕见标签图表（青色标题条 + 白底圆角框）。300 dpi，可直接用于海报。
运行：python draw_diagrams.py
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
import numpy as np

plt.rcParams["font.family"] = "Microsoft YaHei"
plt.rcParams["axes.unicode_minus"] = False

TEAL   = "#1B6E7A"   # 标题条/主色
TEAL_L = "#DDEEF0"   # 浅底
ORANGE = "#E8853D"   # 二硫键 / GSH 强调色
PURPLE = "#7B5EA6"   # 核酸
GRAY   = "#4A4A4A"

def rbox(ax, x, y, w, h, text, fc="white", ec=TEAL, fs=11, tc=GRAY, lw=1.6, ls="-", bold=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.15,rounding_size=1.2",
                                fc=fc, ec=ec, lw=lw, linestyle=ls, mutation_aspect=1.0))
    ax.text(x + w/2, y + h/2, text, ha="center", va="center", fontsize=fs, color=tc,
            fontweight="bold" if bold else "normal", linespacing=1.35)

def arrow(ax, x1, y1, x2, y2, color=TEAL, lw=2.2, style="-|>", ms=16):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=ms,
                                 color=color, lw=lw, shrinkA=2, shrinkB=2))

# ============================================================
# 图 1：构建体架构 + GSH 响应工作原理
# ============================================================
fig, ax = plt.subplots(figsize=(14, 7.2))
ax.set_xlim(0, 140); ax.set_ylim(0, 72); ax.axis("off")

# ---- 左面板：模块化设计 ----
ax.add_patch(FancyBboxPatch((2, 4), 70, 64, boxstyle="round,pad=0.3,rounding_size=1.5",
                            fc="#F7FBFC", ec=TEAL, lw=1.4, linestyle="--", alpha=0.9))
ax.text(37, 64.4, "构建体模块化设计（3 互作域 × 3 IDR 组合矩阵，9/9 组合预测通过）",
        ha="center", fontsize=13, color=TEAL, fontweight="bold")

# A 链
rbox(ax, 6, 52, 20, 8, "互作域\nSH3 / PDZ3 / Myc-LZ", fs=10.5, bold=True)
rbox(ax, 30, 52, 22, 8, "IDR 相分离模块 ×3\nTDP43 / CPEB2 / MLLT1", fc=TEAL_L, fs=10.5)
rbox(ax, 56, 52, 13, 8, "核酸结合标签\n（ZF，可插）", fc="white", ec=PURPLE, tc=PURPLE, fs=9.5, ls="--")
arrow(ax, 26, 56, 30, 56); arrow(ax, 52, 56, 56, 56, color=PURPLE)
ax.text(15.5, 62, "A 链", ha="center", fontsize=11, color=GRAY, fontweight="bold")

# B 链
rbox(ax, 6, 38, 20, 8, "互作配体\n（A 链互作域的\n结合伙伴）", fs=9.5)
rbox(ax, 30, 38, 22, 8, "IDR 相分离模块 ×3\n（同 A 链）", fc=TEAL_L, fs=10.5)
rbox(ax, 56, 38, 13, 8, "核酸结合标签\n（ZF，可插）", fc="white", ec=PURPLE, tc=PURPLE, fs=9.5, ls="--")
arrow(ax, 26, 42, 30, 42); arrow(ax, 52, 42, 56, 42, color=PURPLE)
ax.text(6.2, 47.6, "B 链", ha="left", fontsize=11, color=GRAY, fontweight="bold")

# 链间二硫键
ax.plot([16, 16], [46.6, 51.4], color=ORANGE, lw=2.4)
ax.text(17.4, 49, "S–S\n链间二硫键", fontsize=10, color=ORANGE, fontweight="bold", va="center")

# 阈值可调注释
rbox(ax, 6, 8, 62, 12,
     "响应阈值可调的分子基础（空间可及性调控）\n"
     "① 半胱氨酸位置（N 端 / 中部 / C 端）  ② 侧链位阻（Cys 两侧氨基酸体积）\n"
     "③ 连接子长度与刚性  →  改变二硫键几何暴露程度 → 匹配不同 GSH 浓度场景",
     fc="#FFF4E8", ec=ORANGE, fs=10.5)

# ---- 右面板：GSH 响应原理 ----
ax.add_patch(FancyBboxPatch((76, 4), 62, 64, boxstyle="round,pad=0.3,rounding_size=1.5",
                            fc="#F7FBFC", ec=TEAL, lw=1.4, linestyle="--", alpha=0.9))
ax.text(107, 64.4, "GSH 梯度驱动：结合 → 断裂 → 释放", ha="center", fontsize=13,
        color=TEAL, fontweight="bold")

def wavy_chain(ax, cx, cy, n=3, amp=1.6, color=TEAL, seed=0):
    t = np.linspace(0, n * 2 * np.pi, 120)
    xs = cx + t * 0.55
    ys = cy + amp * np.sin(t + seed)
    ax.plot(xs, ys, color=color, lw=2.2, solid_capstyle="round")

# 状态①：血液/胞外，二硫键完整
d1 = Circle((89, 44), 11.5, fc=TEAL_L, ec=TEAL, lw=2)
ax.add_patch(d1)
wavy_chain(ax, 84.5, 47, seed=0); wavy_chain(ax, 84.5, 40.5, seed=2.1, color="#3D8E99")
ax.plot([89.5, 89.5], [43, 45.5], color=ORANGE, lw=2.6)
ax.text(90.6, 44.2, "S–S", fontsize=9.5, color=ORANGE, fontweight="bold", va="center")
# 质粒（核酸货物）
th = np.linspace(0, 2 * np.pi * 2.2, 160)
ax.plot(93 + 2.6 * np.cos(th) * (1 + 0.12 * np.sin(3 * th)), 41 + 2.6 * np.sin(th) * (1 + 0.12 * np.cos(2 * th)),
        color=PURPLE, lw=1.8)
ax.text(89, 58.5, "① 血液 / 细胞外", ha="center", fontsize=11, color=GRAY, fontweight="bold")
ax.text(89, 56.3, "GSH 2–20 µM（低）", ha="center", fontsize=10, color=GRAY)
ax.text(89, 28.5, "二硫键完整，凝聚体稳定\n结合并浓缩核酸货物", ha="center", fontsize=10.5, color=GRAY)

# 大箭头
arrow(ax, 102, 44, 111, 44, color=ORANGE, lw=3.0, ms=22)
ax.text(106.5, 50.5, "进入细胞\nGSH 1–10 mM\n二硫键断裂", ha="center", fontsize=10, color=ORANGE, fontweight="bold")

# 状态②：胞质，解聚释放
d2 = Circle((122, 44), 11.5, fc="none", ec=TEAL, lw=2, linestyle=(0, (4, 3)))
ax.add_patch(d2)
wavy_chain(ax, 116.5, 49.5, n=2, seed=0.5); wavy_chain(ax, 124.5, 37, n=2, seed=2.8, color="#3D8E99")
# 释放的核酸
t2 = np.linspace(0, 2 * np.pi * 1.3, 100)
ax.plot(124 + 3.0 * np.cos(t2), 49 + 3.0 * np.sin(t2), color=PURPLE, lw=1.8)
wavy_chain(ax, 121.5, 40.5, n=1.5, seed=4.2, color=PURPLE)
ax.text(122, 58.5, "② 细胞质", ha="center", fontsize=11, color=GRAY, fontweight="bold")
ax.text(122, 56.3, "GSH 1–10 mM（高，还原性）", ha="center", fontsize=10, color=GRAY)
ax.text(122, 28.5, "二硫键断裂 → 凝聚体解聚\n核酸货物功能性释放", ha="center", fontsize=10.5, color=GRAY)

plt.tight_layout()
plt.savefig("figA_构建体架构与GSH响应原理.png", dpi=300, bbox_inches="tight", facecolor="white")
plt.close(fig)

# ============================================================
# 图 2：干实验设计工具包总览
# ============================================================
fig, ax = plt.subplots(figsize=(14, 6.8))
ax.set_xlim(0, 140); ax.set_ylim(0, 68); ax.axis("off")

cols = [
    dict(x=3,  title="工具① 链间二硫键位点与响应电位预测", steps=[
        "AlphaFold-Multimer 复合物结构预测\n（5 个模型取一致性）",
        "跨链 Cys 对几何筛选\n（原子间距 / 构象阈值）",
        "Cys→Ser 突变 ΔΔG 计算\n（FoldX 能量项，重复 5 次）",
        "换算氧化还原电位 E(V)\n（E(V) / E_disulfide / E_combined 三口径）",
    ], badge="Foldx-EV 网页工具已上线\n（Hugging Face Space，批量 CIF 上传）"),
    dict(x=49, title="工具② 相分离能力多预测器共识", steps=[
        "AB 双链构建体 FASTA 输入\n（3 互作域 × 3 IDR 组合矩阵）",
        "六种外部预测器并行打分\nIUPred2A · PSPredictor · catGRANULE2\nFuzDrop · PhaSePred · PSPHunter",
        "BLAST→UniProt 映射\n（MMseqs2+Smith-Waterman 交叉复核）",
        "LLPSDB / PhaSePro 实测记录锚定\n输出蛋白浓度 / 盐 / pH 实验条件范围",
    ], badge="9/9 构建体 LLPS 阳性\n每个分值均有来源可溯（*_source 审计列）"),
    dict(x=95, title="工具③ 核酸结合标签设计（ZF 罕见标签）", steps=[
        "全基因组 k-mer 扫描\nhg38 + 大肠杆菌 K-12 + 15 种质粒",
        "0 位点 12-mer 22,378 个\n（独立脚本原始字符串搜索复核）",
        "CpG-free 过滤 → 101 个可用候选\n（避免活细胞内甲基化干扰）",
        "锌指可构建性评分（B1H 指模库）\n→ 4 指阵列 + 插入位点设计",
    ], badge="15 种质粒骨架 × 250 变体全部 0 命中\n输出 1,080 条可直接订购寡核苷酸"),
]

CW, CH = 42, 6.6   # 步骤框尺寸
top = 57
for c in cols:
    x = c["x"]
    # 标题条
    ax.add_patch(FancyBboxPatch((x, top + 2), CW, 6, boxstyle="round,pad=0.15,rounding_size=1.0",
                                fc=TEAL, ec=TEAL, lw=1.4))
    ax.text(x + CW/2, top + 5, c["title"], ha="center", va="center", fontsize=11.5,
            color="white", fontweight="bold")
    y = top - 2
    for s in c["steps"]:
        rbox(ax, x + 1, y - CH, CW - 2, CH, s, fs=9.6)
        y -= CH + 2.4
        if y - CH > 16:
            arrow(ax, x + CW/2, y + 2.4 - 0.0, x + CW/2, y + 0.6, lw=1.8, ms=12)
    # 徽章
    rbox(ax, x + 1, 8.5, CW - 2, 7.5, c["badge"], fc="#FFF4E8", ec=ORANGE, fs=9.6, tc="#8A4B12")
    arrow(ax, x + CW/2, y + 0.6, x + CW/2, 16.6, lw=1.8, ms=12, color=GRAY)

# 底部汇合条
ax.add_patch(FancyBboxPatch((10, 0.5), 120, 5.4, boxstyle="round,pad=0.15,rounding_size=1.0",
                            fc=TEAL_L, ec=TEAL, lw=1.6))
ax.text(70, 3.2, "三大工具包 → 指导构建体模块化设计（互作域 + IDR + 核酸结合标签）→ 预测–验证–迭代闭环",
        ha="center", va="center", fontsize=11.5, color=TEAL, fontweight="bold")
for c in cols:
    arrow(ax, c["x"] + CW/2, 8.2, c["x"] + CW/2, 6.4, lw=1.8, ms=12, color=GRAY)

plt.tight_layout()
plt.savefig("figB_干实验设计工具包总览.png", dpi=300, bbox_inches="tight", facecolor="white")
plt.close(fig)
print("done")
