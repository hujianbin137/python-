import pymysql
import hashlib

# 加密
def jiami(passwd):
    salt = '&5#Az$'  # 加盐
    hash = hashlib.md5(salt.encode())  # 生产加密对象
    hash.update(passwd.encode())  # 加密处理
    return hash.hexdigest()

class User:
    def __init__(self,host='localhost',port=3306,user='root',password='123456',charset='utf8',database=None):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.charset = charset
        self.database = database
        self.lianjie()

    # 连接数据库
    def lianjie(self):
        self.db = pymysql.connect(host=self.host,
                                  port=self.port,
                                  user=self.user,
                                  password=self.password,
                                  charset=self.charset,
                                  database=self.database)

    # 创建游标
    def youbiao(self):
        self.cur = self.db.cursor()

    # 关闭
    def close(self):
        self.cur.close()
        self.db.close()

    # 注册
    def zhuce(self,name,passwd):
        sql = 'select * from user where name="%s"' % name
        self.cur.execute(sql)
        r = self.cur.fetchone()
        if r:
            return False
        sql = 'insert into user (name,passwd) values (%s,%s)'
        passwd = jiami(passwd)
        try:
            self.cur.execute(sql,[name,passwd])
            self.db.commit()
            return True
        except:
            self.db.rollback()
            return False

    # 登录
    def denglu(self,name,passwd):
        passwd = jiami(passwd)
        sql = 'select * from user where name="%s" and passwd = "%s"' % (name,passwd)
        self.cur.execute(sql)
        r = self.cur.fetchone()
        if r:
            return True
        else:
            return False

    # 查字典
    def chaxun(self,word):
        sql = 'select mean from words where word="%s"' % word
        self.cur.execute(sql)
        r = self.cur.fetchone()
        if r:
            return r[0]

    # 插入历史记录
    def charu(self,name,word):
        sql = 'insert into hist (name,word) values(%s,%s)'
        try:
            self.cur.execute(sql,[name,word])
            self.db.commit()
        except:
            self.db.rollback()

    # 查看历史记录
    def lishi(self,name):
        sql = 'select name,word,time from hist where name="%s" order by time desc limit 10' % name
        self.cur.execute(sql)
        return self.cur.fetchall()