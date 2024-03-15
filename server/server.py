import os
import time
import random
from datetime import datetime
from bottle import route, run, request
import sqlite3
import base64

# 服务器全局配置
app_host = '0.0.0.0'  # 运行地址，一般不建议修改
app_port = 8080  # 运行端口号
global_key = "1bae429c52273ba32808382c338fead4"  # 管理密钥，生成卡密、初始化时要用到，建议使用加密算法加密
timeout = 86400  # 获取一张卡密后需要多久才能获取第二张

if not os.path.exists("key"):
    os.mkdir("key")

def txt():
    # 取目录下的卡密文件
    path = r"key"
    files = os.listdir(path)
    return files


def base64_decode(encode_data):
    # base64解码
    decode_data = base64.b64decode(encode_data).decode("utf-8")
    return decode_data


def calculate_seconds_between_timestamps(timestamp1, timestamp2):
    # 时间戳差值计算
    time1 = datetime.fromtimestamp(timestamp1)
    time2 = datetime.fromtimestamp(timestamp2)
    time_diff = time2 - time1
    seconds_diff = time_diff.total_seconds()
    return seconds_diff


conn = sqlite3.connect("main.db")


@route('/init')
def init():
    if request.query.get('login_key') == global_key:
        conn.execute('''CREATE TABLE user (
username VARCHAR(255),
password VARCHAR(255),
time VARCHAR(255)
);''')
        conn.execute('''CREATE TABLE code (
code VARCHAR(255)
); ''')
        return {"code": 200}
    else:
        return {"code": 401}


@route('/reg')
def reg():
    name = request.query.get('name')
    password = request.query.get('password')
    card = request.query.get('key')
    res = conn.execute("SELECT * FROM code WHERE code = ?", (card,))
    result = res.fetchone()
    if result:
        conn.execute("DELETE FROM code WHERE code = ?", (card,))
        conn.commit()
        conn.execute("INSERT INTO user (username, password, time) VALUES (?, ?, ?)", (name, password, "1709222400"))
        conn.commit()
        return {"code": 200}
    else:
        return {"code": 100}


@route('/login')
def login():
    name = request.query.get('name')
    password = request.query.get('password')
    res = conn.execute("SELECT * FROM user WHERE username=? AND password=?", (name, password))
    if res.fetchone() is not None:
        return {"code": 200}
    else:
        return {"code": 101}


@route('/gen')
def gen():
    key = request.query.get("key")
    login_key = request.query.get("login_key")
    if login_key == global_key:
        conn.execute("INSERT INTO code (code) VALUES (?)", (key,))
        conn.commit()
        return {"code": 200}
    else:
        return {"code": 401}


@route('/get')
def get():
    user_key = request.query.get("user_key")
    user_key = base64_decode(user_key)
    user = conn.execute("SELECT * FROM user WHERE username=?", (user_key,))
    user = user.fetchone()
    if user:
        t = conn.execute("SELECT time FROM user WHERE username=?", (user_key,))
        t = int(t.fetchone()[0])
        t = calculate_seconds_between_timestamps(t, time.time())
        if t > timeout:
            current_time = str(int(time.time()))
            conn.execute("UPDATE user SET time=? WHERE username=?", (current_time, user_key))
            conn.commit()
            try:
                g = txt()
                if not g:
                    time1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
                    print("[" + time1 + "]" + "[ERROR] 提醒您：卡密已用光")
                    data = "暂无卡密，请联系管理员补卡"
                    error = open("error.log", "a")
                    error.write("\n")
                    error.write("[" + time1 + "]")
                    error.write("[ERROR] 提醒您：卡密已用光")
                    info = open("info.log", "a")
                    info.write("\n")
                    info.write("[" + time1 + "]")
                    info.write("[ERROR] 提醒您：卡密已用光")
                    return {"code": 103, "msg": data}
                else:
                    time1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
                    u = g[random.randint(0, len(g) - 1)]
                    f = open(r"key/" + u, 'r')
                    data = f.readline()
                    f.close()
                    print("[" + time1 + "]" + "[INFO] 获取了一张卡密")
                    os.remove("key/" + u)
                    print("[INFO]" + "文件：" + u + "已删除")
                    info = open("info.log", "a")
                    info.write("\n")
                    info.write("[" + time1 + "]")
                    info.write("[INFO] 获取了一张卡密")
                    info.write("[INFO]" + "文件：" + u + "已删除")
                    return {"code": 200, "msg": data, "odd": len(g) - 1}
            except Exception as e:
                data = "服务端出现问题，请稍后再试~ 错误原因：{}".format(e)
                return {"code": 500, "msg": data}
        else:
            return {"code": 102, "msg": "请等待{}秒后再进行获取".format(str(int(timeout - t)))}
    else:
        return {"code": 401, "msg": "用户鉴权失败，请重新登录"}


@route('/odd')
def odd():
    g = txt()
    return {"code": 200, "odd": len(g)}


print("AZ卡密获取系统开源版 Ver.1.0")
print("AZ Studio版权所有")
print("Github: https://github.com/AZ-Studio-2023/")
print("本程序仅供娱乐，使用造成的后果由用户自行承担")

run(host=app_host, port=app_port)
