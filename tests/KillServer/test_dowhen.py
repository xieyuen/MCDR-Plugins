import time

from dowhen import *


def f():
    pass


def test1():
    stat = False
    time.sleep(1)
    print("等待服务器关闭超时, 正在强制关闭服务器")
    if not stat:
        print("世界未完全保存, 重新等待")
        goto("time.sleep(1)").do("stat=True").when(test1, "15")
        f()
        return
    print("kill server")


if __name__ == '__main__':
    test1()
