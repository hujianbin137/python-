from socket import *
from multiprocessing import Process
import sys,signal
from dict_db import User
from time import sleep

HOST = '0.0.0.0'
PORT = 8888
ADDR = (HOST,PORT)

# 数据库
db = User(database='dict')

# 注册
def zhuce(c,data):
    tmp = data.split(' ')
    name = tmp[1]
    passwd = tmp[2]
    if db.zhuce(name,passwd):
        c.send(b'OK')
    else:
        c.send(b'Fail')

# 登录
def denglu(c,data):
    tmp = data.split(' ')
    name = tmp[1]
    passwd = tmp[2]
    if db.denglu(name,passwd):
        c.send(b'OK')
    else:
        c.send(b'Fail')

# 查单词
def chazidian(c,data):
    tmp = data.split(' ')
    name = tmp[1]
    word = tmp[2]
    mean = db.chaxun(word)
    if mean:
        db.charu(name,word)
        msg = '%s : %s' % (word,mean)
    else:
        msg = '没有找到该单词'
    c.send(msg.encode())

# 查历史
def lishi(c,data):
    name = data.split(' ')[1]
    r = db.lishi(name)
    for i in r:
        msg = '%s %-16s %s' % i
        c.send(msg.encode())
        sleep(0.1)
    c.send(b'##')

# 处理客户端消息
def handle(c):
    db.youbiao()  # 每个子进程有自己的游标
    while True:
        data = c.recv(1024).decode()
        if not data or data[0] == 'E':
            sys.exit()
        elif data[0] == 'R':
            zhuce(c,data)
        elif data[0] == 'L':
            denglu(c,data)
        elif data[0] == 'Q':
            chazidian(c,data)
        elif data[0] == 'H':
            lishi(c,data)

def main():
    s = socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(ADDR)
    s.listen(5)
    # 处理僵尸进程
    signal.signal(signal.SIGCHLD,signal.SIG_IGN)
    print('等待连接中...')

    while True:
        try:
            c,addr = s.accept()
            print('客户端连接：',addr)
        except KeyboardInterrupt:
            sys.exit('退出')
        except Exception as e:
            print(e)
            continue
        # 创建子进程
        p = Process(target=handle,args=(c,))
        p.daemon = True
        p.start()

if __name__ == '__main__':
    main()