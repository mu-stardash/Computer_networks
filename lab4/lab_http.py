# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 22:57:23 2021

@author: DashaEfimova
"""

# b_obj = BytesIO()
# crl = pycurl.Curl()

# crl.setopt(crl.URL, 'http://www.example.com')
# crl.setopt(crl.WRITEDATA, b_obj)
# crl.perform()
# crl.close()
# get_body = b_obj.getvalue()
# print('Output of GET requeast:\n%s' %get_body.decode('utf-8'))




import socket
import sys
# import pycurl
# from io import BytesIO
# import requests

if (len(sys.argv) < 1):
    print("not enough arguments")
    quit(1)
host = sys.argv[1]
#host = 'http://cs.petrsu.ru:80'

port = -1
urlIsExist = False
neededHost=''
s =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(host)
for ch in host:
    if (ch =='/'):
        urlIsExist = True
        break


if (urlIsExist == False):
    neededHost = host
else:
    neededHost = host[host.find('/')+2:]

for i in range(len(neededHost)):
    if neededHost[i]==':':
        k = i
        port = neededHost[k+1:]
        neededHost = neededHost[:k]
        break

if port == -1:
    port = 80


# host2 = socket.gethostbyname(neededHost) # try-catch

# s.connect((host2, int(port)))


target = socket.getaddrinfo(neededHost, port) #получаем список из 5 кортежей, где есть\
 #инфа для создания сокета

s.connect(target[0][4])              #передаем в connect sockaddr (adress, po\
#rt)

stri =  "\nGET / HTTP/1.0\r\nhost: "+neededHost+'\n\n'
#kappa.cs.petrsu.ruprint(stri)
print(neededHost)
s.send(bytes(stri).encode('utf-8'))

tmp = s.recv(1024)
data = b''
#вывод данных
while tmp:
    data+=tmp
    tmp = s.recv(1024)
newData = data.decode('utf-8')

s.close()


header = newData.split('\r\n\r\n')[0]

res = {sub.split(":")[0]:sub.split(":")[1:] for sub in header[1:].split('\n')}

# r =''
# flag = True
# response = requests.get(host)
# k = response.headers
# if 'Transfer-Encoding' in k:
#     r = response.headers['Transfer-Encoding']
#     flag = False
#     print('\n' + r + '\n')

x = header[9:12]
if x != '200':
    print('!!!BAD REQUEST!!!')
    sys.exit(1)
elif 'Transfer-Encoding' in res:
    if res['Transfer-Encoding'] != 'identity':
        print('Данная кодировка ответа не поддерживается!!!\n')
        sys.exit(1)
else:
    body = newData.split('\r\n\r\n')[1]
    print('HEADER:\n' + header +'\n')
    print('BODY:\n' + body)

