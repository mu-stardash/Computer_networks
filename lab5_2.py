# nc localhost 8080 для подключения как клиент
# файловый дескриптор - номер файла (ссылка на файловый обьект)

import socket
import sys
from select import select

# для мониторинга
to_monitor = []

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind(("localhost", 8080))
socket.listen()

# передаем серверный сокет
to_monitor.append(socket)

print("Listening...")

def accept_connection(sock):
    # Если подключение ещё не является клиентом, то принимаем его и сохраняем
    client, addr = sock.accept()
    print(f"{addr[0]}:{addr[1]} connected")
    # передаем клиентский сокет
    to_monitor.append(client)

def send_message(sock):
    req = sock.recv(4096)
    if req:
    # Отправляем ответ
        sock.send(req)
    else:
    # Если данных нет, то закрываем подключение и удаляем его
        print("disconnected")
        sock.close()
        to_monitor.remove(sock)

while True:
    try:
        # Выбираем подключения готовые для чтения
        # select - сист. фун., кот. нужна для мнониторинга изменений состояний файловых объектов и сокетов
        # нам нужно только для чтения
        readable, _, _ = select(to_monitor, [], []) # read, write, error
    except:
        pass

    for sock in readable:
        if sock is socket: # если сокет явл серверным
            accept_connection(sock)
        else:
            # Если подключение уже добавлено, то принимаем данные от него
            try:              
                send_message(sock)  
                
            except WindowsError:
                print("disconnected")
                sock.close()
                to_monitor.remove(sock)
            except OSError:            
                sys.exit(0)