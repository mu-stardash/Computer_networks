# nc localhost 8080 для подключения как клиент
# многопоточность!

import threading
import socket
import sys

def accept_data(client, addres):
    while True:
        try:
            # принимаем данные от клиента
            data = client.recv(1024)
            if data:
                client.send(data)
            else:
                # бросаем ошибку если от клиента ничего не приходит
                print(f"{addres[0]}:{addres[1]} disconnected")
                raise error()
        except:
            # закрываем соединение с клиентом
            print(f"{addres[0]}:{addres[1]} disconnected")
            client.close()
            break


socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind(("localhost", 8080)) # связываем сокет с хостом и портом
socket.listen()

print("Listening...")

while True:
    try:
        # принимаем входящее соединение
        client, addres = socket.accept()
        print(f"{addres[0]}:{addres[1]} connected")
        # создаем поток для функции accept_data
        thread = threading.Thread(target = accept_data, args = (client, addres))
        # запускаем поток
        thread.start()
    except KeyboardInterrupt: # исключение, если нажимаем опред. клавиши прерывания процесса
        sys.exit(0) 
