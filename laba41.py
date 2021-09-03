# This Python file uses the following encoding: utf-8

import socket
from socket import *
import ssl
import base64
import getpass
import string
import sys

context = ssl.create_default_context()

addr = raw_input('input server: ')

conn = context.wrap_socket(socket(AF_INET), server_hostname=addr)
conn.connect((addr, 465))
recv = conn.recv(1024).decode()
print(recv)
if recv[:3] != '220':
    print ('Нет ответа от данного сервера')# проверка на готовность сервера
    sys.exit(1)


conn.send("ehlo addr\r\n".encode())
recv1 = conn.recv(1024).decode()
print(recv1)
if recv1[:3] !='250':
    print ('В запрашиваемом почтовом действии возникла ошибка')
    sys.exit(1)
print ('autorization, Please write login and password')
username = raw_input('Login: ')
#password = raw_input()
password = getpass.getpass('Password: ')

base64_str = ("\x00"+username+"\x00"+password).encode()
base64_str = base64.b64encode(base64_str)

authMsg = "AUTH PLAIN ".encode()+base64_str+"\r\n".encode()
conn.send(authMsg)
recv_auth = conn.recv(1024)
print(recv_auth.decode())
if recv_auth[:3] !='235':
    print ('Произошла ошибка аутентификации')
    sys.exit(1)


mailFrom=raw_input('From: ')

conn.send("mail from: ".encode()+mailFrom+"\r\n".encode()) #от кого письмо
recv1 = conn.recv(1024).decode()
print(recv1)
if recv1[:3]!='250':
    print('неверный или несуществующий логин')

sendTo = raw_input('To: ')
conn.send("rcpt to: ".encode()+sendTo+"\r\n".encode()) #кому письмо
recv1 = conn.recv(1024).decode()
print(recv1)
if recv1[:3]!='250':
    print('неверный пароль')

conn.send("data\r\n".encode())
    
recv1 = conn.recv(1024).decode()
print(recv1.decode())
if recv1[:3]=='354':
    print('Все хорошо, вводите почтовые данные')

mailSubject = raw_input('Subject: ')
mailData = raw_input('Data: ')



mailData = mailData.split()
if mailData[0] == '.':
    mailData[0] = '..'    
mailData = ' '.join(mailData)



conn.send("Subject: "+mailSubject+"\n"+mailData+"\r\n.\r\n".encode())
recv1 = conn.recv(1024).decode()
print(recv1)
if recv1[:3]!='250':
    print('возникли проблемы при отправке письма')

conn.close()

