import hashlib
import os
import random
import time

from generator import Generator


class Accumulator:
    # 累加器负责从不同的熵源中获取实随机数, 并用来更新生成器的种子
    pool = []
    reseed_cnt = 0  # 种子更新计数器
    seed_interval = 0.1  # 种子间隔时间(s)

    def __init__(self, pool_num=32, min_pool_size=64):
        self.pool_num = pool_num  # 熵池数目
        self.min_pool_size = min_pool_size  # 最小熵池大小
        self.pool = [b''] * pool_num  # 初始化熵池
        self.generator = Generator()  # 初始化生成器
        self.last_seed = time.time()  # 最后种子时间

    def random_data(self, n):
        # 获取n字节随机数据
        if len(self.pool[0]) >= self.min_pool_size or time.time() - self.last_seed > self.seed_interval:
            # 需要更新种子, 从熵池获取数据
            self.reseed_cnt += 1
            s = b''
            sha256 = hashlib.sha256()
            for i in [j for j in range(self.pool_num) if self.reseed_cnt % (2 ** j) == 0]:
                sha256.update(self.pool[i])
                s += sha256.digest()
                self.pool[i] = b''
            self.generator.reseed(s)  # 更新种子
            self.last_seed = time.time()

        assert self.reseed_cnt

        return self.generator.pseudo_random_data(n)

    def add_random_event(self, s, i, e):
        # 通过熵源号(s), 熵池号(i), 事件数据(e)添加事件
        assert 1 <= len(e) <= 32
        assert 0 <= s <= 255
        assert 0 <= i <= 31
        # 将事件添加到熵池
        self.pool[i] += bytes((s, )) + bytes((len(e), )) + e

    def get_event(self):
        s = 0
        i = 0
        while True:
            if len(self.pool[i]) >= self.min_pool_size:
                continue
            e = os.urandom(random.randint(1, 32))  # 从随机源获取64字节数据
            self.add_random_event(s, i, e)
            s = (s + 1) % 256
            i = (i + 1) % self.pool_num
