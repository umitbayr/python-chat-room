# 20010011507  ÜMİT BAYRAM

import socket
import threading

TCP_PORT = 12345
BUFFER_SIZE = 1024

# Kullanıcı adı seçme
username = input("Size nasil hitap edilsin-> ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", TCP_PORT))

# Server'ı Dinle ve Kullanıcı Adını Gönder
def receive():
    while True:
        try:
            # Sunucudan Mesaj Al
            message = client.recv(BUFFER_SIZE).decode('utf-8')
            if message == 'NICK':
                client.send(username.encode('utf-8'))
            else:
                print(message)
        except:
            #  Hata Oluştuğunda Bağlantıyı Kapat
            print("Bir hata oluştu!")
            client.close()
            break

# Sunucuya Mesaj Gönderme
def write():
    while True:
        message = input('')
        client.send(f'{message}'.encode('utf-8'))

#  Listening ve Writing için Thread'leri Başlatma
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
