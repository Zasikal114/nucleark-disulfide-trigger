# Disulfide Bond Redox Potential Calculator (二硫键氧化还原电位计算)

将所有半胱氨酸（CYS）突变为丙氨酸（ALA），通过 FoldX 计算折叠自由能变化（ΔΔG），从而评估二硫键对蛋白质复合物稳定性的贡献及其氧化还原电位。

## 原理

$$
E(V) = -\frac{\Delta\Delta G}{23.06 \times n_{cys}}
$$

- **ΔΔG**：所有 CYS → ALA 突变的总折叠自由能变化（kcal/mol）
- **n_cys**：半胱氨酸残基数
- **|E(V)| 越大**，说明二硫键对蛋白质稳定性的贡献越大，断裂所需能量也越大。

## 项目结构

```
├── README.md
├── cif2pdb.py           # CIF → PDB 批量转换脚本
├── foldx/               # 本地 FoldX 分析流程
│   ├── afoldx.sh        # 核心分析脚本
│   ├── foldx            # FoldX 可执行文件（Linux）
│   ├── CIF/             # 输入：存放 .cif 文件
│   ├── Input/           # 中间产物：转换后的 .pdb 文件
│   ├── results/         # 输出：分析结果
│   └── yasaraPlugin/    # YASARA 插件
├── space/               # Hugging Face Space 在线部署
│   ├── app.py           # Gradio Web 界面
│   ├── pipeline.sh      # 结构化分析流程
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── push_to_hf.py    # 部署到 Hugging Face
│   └── upload_foldx.py  # 上传 FoldX 二进制
└── molecules/           # 分子相关文件
```

## 环境要求

### 本地运行

- **Linux**（FoldX 仅支持 Linux）
- Python 3.10+（用于 CIF→PDB 转换）
- [pdb-tools](https://github.com/haddocking/pdb-tools)（conda 安装）

### 在线使用

无需本地环境，直接访问 Hugging Face Space：[FoldX-EV](https://huggingface.co/spaces/kalendar114/Foldx-EV)

---

## 方式一：在线 Web 界面（推荐）

1. 打开 [https://huggingface.co/spaces/kalendar114/Foldx-EV](https://huggingface.co/spaces/kalendar114/Foldx-EV)
2. 上传一个或多个 `.cif` 文件
3. 点击 **Submit**
4. 查看结果表格，可下载 `final_result.txt`

---

## 方式二：本地运行

### 1. 配置 FoldX 环境

在 Linux 终端中，将 foldx 可执行文件添加到 PATH：

```bash
vim ~/.bashrc
# 在文件末尾添加：
export PATH="/path/to/foldx:$PATH"
# 将 /path/to/foldx 替换为 foldx 文件所在目录的绝对路径

source ~/.bashrc
foldx --help   # 验证是否配置成功
```

### 2. 安装 pdb-tools（用于 CIF → PDB 转换）

```bash
conda create -n pdb_tools -c conda-forge pdb-tools -y
conda activate pdb_tools
```

### 3. 准备输入文件

将所有蛋白质复合物的 `.cif` 文件放入 `foldx/CIF/` 目录下。

### 4. 运行分析

**第一步：CIF 转 PDB**

```bash
python cif2pdb.py
```

转换后的 `.pdb` 文件将输出到 `foldx/Input/` 目录。

**第二步：运行 FoldX 分析**

```bash
cd foldx
bash afoldx.sh
```

### 5. 查看结果

结果位于 `foldx/results/` 目录下，主要输出文件：

| 文件 | 说明 |
|------|------|
| `final_result.txt` | 最终结果表，包含所有样本的计算结果 |

输出列说明：

| 列名 | 说明 |
|------|------|
| `filename` | 输入文件名 |
| `n.cys` | 半胱氨酸残基数量 |
| `total energy` | CYS→ALA 突变的总 ΔΔG（kcal/mol） |
| `E (V)` | 氧化还原电位 |

---

## 方式三：部署到 Hugging Face Space

### 1. 推送代码

```bash
cd space
python push_to_hf.py
```

### 2. 上传 FoldX 二进制文件

```bash
python upload_foldx.py
```

Space 将在 Hugging Face 上自动构建 Docker 镜像并启动。

---

## 输入要求

- 文件格式：`.cif`（AlphaFold / PDB 格式）
- 内容：含有二硫键的蛋白质复合物结构

## 输出解读

- **|E(V)| 较大** → 二硫键对复合物稳定性贡献大 → 断裂需要更多能量
- **|E(V)| 较小** → 二硫键贡献较小 → 较易断裂
