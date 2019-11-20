from socket import *
import json

s = socket()
s.bind(('0.0.0.0',8080))
s.listen(3)

c,addr = s.accept()
data = c.recv(1024).decode()
print(data)
c.send(json.dumps({'status':'200',\
                   'data':'http test'}).encode())
c.close()
s.close()