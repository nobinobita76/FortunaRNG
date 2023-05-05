# FortunaRNG
Python Fortuna PRNG for Windows

#### How to Run

```powershell
python fortuna.py
```

#### 环境

- Python 3
- Windows 10

#### 程序原理

**Fortuna** 是由 Bruce Schneier 和 Niels Ferguson设计并于 2003 年发布的密码学安全的伪随机数生成器（PRNG），由 Yarrow 算法改进而来，广泛应用于多个操作系统与软件。

Fortuna 由三个主要部分组成：

1. 生成器（generator）采用固定大小的种子来生成任意数量的伪随机数据。其基于安全的分组密码（如 AES，Serpent，Twofish），基本思想是以计数器模式运行密码，加密计数器（counter）的值。加密密钥会在每次获取随机数据后更改，以保证前向安全性（Forward secrecy）。
2. 累加器（accumulator）收集和混合从各种源产生的熵，有时还给发生器新的种子。累加器通过维护若干个熵池，从熵源中获取随机数据并均匀地添加到熵池中。在生成器的第 n 次重新产生种子（reseed）时，仅当 n 是 $2^k$ 的倍数时才使用池 k。重新产生种子的过程通过 SHA-256 哈希实现。
2. 种子文件管理（Seed File Management）部分主要用于维护种子文件。种子文件是 Fortuna 保存的一个充满了熵的独立文件，以便于在系统刚启动等时段仍能生成随机数。种子文件在每次使用后都需要重新写入内容。

#### 目录结构

```
.
├── accumulator.py  # 累加器
├── fortuna.py  # Fortuna 主文件
├── generator.py  # 生成器
├── seed  # 种子文件
└── seed_file_management.py  # 种子文件管理
```
