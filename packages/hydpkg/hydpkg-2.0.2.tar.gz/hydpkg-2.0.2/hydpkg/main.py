import faker
import psutil
import time
from faker import Faker

def cat_cpu():
    # 获取cpu数量
    print("当前电脑共有{}个cup".format(psutil.cpu_count()))

    # 获取硬盘利用率，返回的是使用多少、还剩多少，以及使用率
    print("当前硬盘使用情况为{}".format(psutil.disk_usage("C:\\"))) # 查看C盘
    #
    # # # 获取当前网络的IO情况，返回IO的字节、包的数量
    print("当前网络情况为{}".format(psutil.net_io_counters()))

def make_somename(n):
    faker =Faker("zh_CN")
    list1=[]
    for i in range(n):
        list1.append(faker.name())
    print(list1)
    return list1
