import random
# 一个很垃圾的添加程序，赶出来的，有能力还是自己写吧
a = input("要添加的文件（一行一个卡密）:")
bi = input("生成的文件名头（不填即无）：")
c = input("每行的开头：")
s = []
f = open(a, 'r')
for lines in f:
    ls = lines.strip('\n').replace(' ', '').replace('、', '/').replace('?', '').split('/')
    for i in ls:
        s.append(i)
f.close()

for j in s:
    b = random.randint(0, 99999999999)
    f1 = open(r"key/" + str(bi) + str(b), 'w', encoding="utf-8")
    f1.write(str(c) + j)
f1.close()
exit = input("任务已完成，回车退出")
