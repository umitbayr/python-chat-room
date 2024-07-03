# 20010011507  ÜMİT BAYRAM

import socket
import threading

UDP_PORT = 12346
BUFFER_SIZE = 1024
SERVER_ADDRESS = ("127.0.0.1", UDP_PORT)

# Kullanıcı adı seçme
username2 = input("Size nasil hitap edilsin-> ")

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Servere kullanıcı adı gönderme
client.sendto(f"NICK {username2}".encode('utf-8'), SERVER_ADDRESS)

# Sunucuyu Dinleme
def receive():
    while True:
        try:
            # Sunucudan Mesaj Al
            message, _ = client.recvfrom(BUFFER_SIZE)
            print(message.decode('utf-8'))
        except:
            # Hata Oluştuğunda Bağlantıyı Kapat
            print("Bir hata oluştu!")
            client.close()
            break

# Sunucuya Mesaj Gönderme
def write():
    while True:
        message = input('')
        client.sendto(f'{message}'.encode('utf-8'), SERVER_ADDRESS)

# Listening ve Writing için Thread'leri Başlatma
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
