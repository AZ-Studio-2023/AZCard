import random
import requests

# 程序设置
# 这个生成算法比较垃圾，有能力的还是自己写吧
api = "http://example.com/"  # 后端地址，务必按照这样的格式填写（网址结尾加"/"）
key = "1bae429c52273ba32808382c338fead4"  # 管理密钥，需和后端填写一致

letter = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
          'W', 'X', 'Y', 'Z']
number = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]


def random_id():
    id_text = ""
    for i in range(12):
        if random.randint(0, 1) == 0:
            id_text = id_text + letter[random.randint(0, 25)]
        else:
            id_text = id_text + number[random.randint(0, 9)]
    return id_text


u = int(input("请输入个数："))
for i in range(u):
    y = random_id()
    requests.get("{}gen?login_key=b67164441f5a550678b926febd0e0f6d&key={}".format(api, y))
    print(y)
    u = open("激活码.txt", "a")
    u.write("{}\n".format(y))
    u.close()
