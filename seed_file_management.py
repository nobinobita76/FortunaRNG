import os


class SeedFileManagement:
    # 种子文件管理
    file = 'seed'  # 种子文件路径
    # s = 0  # 熵源号(0-255)
    # i = 0  # 熵池号

    def write_seed_file(self, accumulator):
        # 生成 64 字节的随机数据, 然后写入文件
        with open(self.file, 'wb') as f:
            f.write(accumulator.random_data(64))

    def read_seed_file(self):
        with open(self.file, 'rb') as f:
            seed = f.read(64)
        return seed

    def update_seed_file(self, accumulator):
        # 更新种子文件
        seed = self.read_seed_file()
        assert len(seed) == 64
        accumulator.generator.reseed(seed)
        self.write_seed_file(accumulator)
