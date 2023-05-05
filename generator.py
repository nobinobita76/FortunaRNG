import hashlib
import math

from Crypto.Cipher import AES


class Generator:
    # 生成器负责将固定长度的内部状态转换为任意长度的输出
    def __init__(self):
        # 初始化密钥和计数器，表示没有获取种子
        self.key = b''
        self.counter = 0

    def reseed(self, seed):
        # 更新密钥
        sha256 = hashlib.sha256()
        sha256.update(self.key + seed)
        self.key = sha256.digest()
        self.counter += 1

    def generate_blocks(self, n):
        # 生成n个随机块
        assert self.counter, "计数器不能为0"
        cipher = AES.new(key=self.key, mode=AES.MODE_CTR)  # 计数器模式AES

        res = b''
        for _ in range(n):
            # counter拓展至128位bytes
            hex_str = '{:0<32}'.format(hex(self.counter))
            expand_counter = int(hex_str, 16).to_bytes(16, byteorder='big')

            res += cipher.encrypt(expand_counter)

            self.counter += 1

        return res

    def pseudo_random_data(self, n):
        # 生成n字节随机数据
        assert 0 <= n <= 2**20
        res = self.generate_blocks(math.ceil(n / 16))[:n]
        self.key = self.generate_blocks(2)
        return res
