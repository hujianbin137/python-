from socket import *
import sys
from getpass import getpass

ADDR = ('127.0.0.1',8888)
s = socket()
s.connect(ADDR)

# 注册
def zhuce():
    while True:
        name = input('请输入用户名：')
        pwd = getpass('请输入密码：')
        pwd1 = getpass('再次输入密码：')
        if pwd != pwd1:
            print('两次密码不一致')
            continue
        elif (' ' in name) or (' ' in pwd):
            print('用户名和密码不可以有空格')
            continue

        msg = 'R %s %s' % (name,pwd)
        s.send(msg.encode())  # 发送请求
        data = s.recv(128).decode()  # 反馈
        if data == 'OK':
            print('注册成功')
            erji(name)
        else:
            print('注册失败')
        return

# 登录
def denglu():
    name = input('用户名：')
    passwd = getpass()
    msg = 'L %s %s' % (name,passwd)
    s.send(msg.encode())  # 发请求
    data = s.recv(128).decode()  # 得到反馈
    if data == 'OK':
        print('登录成功')
        erji(name)
    else:
        print('登录失败')

# 查字典
def chazidian(name):
    while True:
        word = input('单词:')
        if word == '':
            break
        msg = 'Q %s %s' % (name,word)
        s.send(msg.encode())
        data = s.recv(2048).decode()
        print(data)

# 查历史记录
def lishi(name):
    msg = 'H '+name
    s.send(msg.encode())
    while True:
        data = s.recv(1024).decode()
        if data == '##':
            break
        print(data)

# 二级界面
def erji(name):
    while True:
        print('''
        ===============
        1.查字典
        2.查历史记录
        3.退出查询
        ===============''')
        cmd = input('请选择:')
        if cmd == '1':
            chazidian(name)
        elif cmd == '2':
            lishi(name)
        elif cmd == '3':
            return  # 二级界面结束
        else:
            print('请输入正确的命令')

# 一级界面
def main():
    while True:
        print('''
        ====================
        1.注册  2.登录  3.退出
        ====================''')
        cmd = input('请选择：')
        if cmd == '1':
            zhuce()
        elif cmd == '2':
            denglu()
        elif cmd == '3':
            s.send(b'E')
            sys.exit('谢谢使用')
        else:
            print('请输入正确命令')

if __name__ == '__main__':
    main()