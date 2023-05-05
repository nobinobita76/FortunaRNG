import threading

from accumulator import Accumulator
from seed_file_management import SeedFileManagement

if __name__ == "__main__":
    # 初始化 PRNG
    acc = Accumulator()
    seed_man = SeedFileManagement()
    # seed_man.update_seed_file(acc)

    # 开启子进程，从熵源维护熵池
    t = threading.Thread(target=acc.get_event)
    t.start()

    while True:
        try:  # 捕获CTRL+C
            print('输入要生成的随机数长度(输入"u"可更新种子文件): ')
            n_raw = input()

            if n_raw == 'u':  # 更新种子文件
                print('更新前')
                print(seed_man.read_seed_file().hex())

                seed_man.update_seed_file(acc)

                print('更新后')
                print(seed_man.read_seed_file().hex())

            else:
                try:
                    n = int(n_raw)
                    print(acc.random_data(n).hex())
                except ValueError:
                    print('输入必须是整数或"u"')
                    break

        except KeyboardInterrupt:
            # 在关机前更新种子文件
            seed_man.update_seed_file(acc)
            print('bye')
            exit(0)
