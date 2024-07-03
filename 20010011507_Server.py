# 20010011507  ÜMİT BAYRAM

import threading
import socket

host = '127.0.0.1'
portTCP = 12345
portUDP = 12346
buffersize = 1024

# TCP Sunucusunu Başlatma
serverTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverTCP.bind((host, portTCP))
serverTCP.listen()

# UDP Sunucusunu Başlatma
serverUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverUDP.bind((host, portUDP))

# İstemciler ve Kullanıcı Adları için Listeler
clients = []
usernames = []
clientsUDP = {}

# Bağlı Tüm İstemcilere Mesaj Gönderme
def broadcast(message, harici_client=None, senderUDP=None):
    for client in clients:
        if client != harici_client:
            client.send(message)
    for username, address in clientsUDP.items():
        if address != senderUDP:
            serverUDP.sendto(message, address)

# TCP İstemcilerinden Gelen Mesajları İşleme
def handle_tcp(client):
    while True:
        try:
            # Mesaj Alımı ve Yayını İşleme
            message = client.recv(buffersize).decode('utf-8')
            index = clients.index(client)
            username = usernames[index]
            msg = f"{username} [TCP]: {message}"
            print(msg)  # Sunucu ekranına mesajı yazdırma
            broadcast(msg.encode('utf-8'), harici_client=client)
        except:
            # İstemcileri Kaldırma ve Kapatma
            index = clients.index(client)
            clients.remove(client)
            client.close()
            username = usernames[index]
            broadcast(f'{username} [TCP] sohbetten ayrildi!\n'.encode('utf-8'))
            print(f'{username} [TCP] sohbetten ayrildi!')  # Server ekranına ayrilma mesajını yazdırma
            usernames.remove(username)
            break

# UDP İstemcilerinden Gelen Mesajları İşleme
def handle_udp():
    while True:
        try:
            message, address = serverUDP.recvfrom(buffersize)
            decoded_message = message.decode('utf-8')

            if address not in clientsUDP.values():
                # Yeni bir UDP istemcisi ise, bir kullanıcı adını bekleyin
                if decoded_message.startswith("NICK"):
                    username = decoded_message.split()[1]
                    if username not in usernames:
                        clientsUDP[username] = address
                        usernames.append(username)
                        join_message = f"{username} [UDP] sohbete katildi!\n"
                        broadcast(join_message.encode('utf-8'))
                        print(f"UDP portu {portUDP} üzerinden {host} ile bağlanti kuruldu")
                        print(join_message)
                        serverUDP.sendto(f"Hoşgeldiniz {username}, UDP ile bağlisiniz\n".encode('utf-8'), address)
                    else:
                        serverUDP.sendto(f"Kullanici adi {username} daha önceden alinmiş. Lütfen başka bir kullanici adi deneyiniz.\n".encode('utf-8'), address)
            else:
                username = None
                for nick, addr in clientsUDP.items():
                    if addr == address:
                        username = nick
                        break
                if username:
                    if decoded_message == "görüşürüz":
                        leave_message = f"{username} [UDP] sohbetten ayrildi!\n"
                        broadcast(leave_message.encode('utf-8'))
                        print(leave_message)
                        usernames.remove(username)
                        del clientsUDP[username]
                    else:
                        msg = f"{username} [UDP]: {decoded_message}"
                        print(msg)  # Sunucu ekranına mesajı yazdırma
                        broadcast(msg.encode('utf-8'), senderUDP=address)
        except Exception as e:
            print(f"Bir hata oluştu! {e}")

# TCP İçin Alım / Dinleme İşlevi
def receive_tcp():
    while True:
        # Bağlantı Kabul Etme
        client, address = serverTCP.accept()
        print(f"TCP portu {portTCP} üzerinden {host} ile bağlanti kuruldu")
        # Kullanıcı Adını İsteme ve Saklama
        client.send('NICK'.encode('utf-8'))
        username = client.recv(buffersize).decode('utf-8')
        if username in usernames:
            client.send('Kullanici adi daha önceden alinmiş. Lütfen başka bir kullanici adi deneyiniz.\n'.encode('utf-8'))
            client.close()
        else:
            usernames.append(username)
            clients.append(client)

            #Kullanıcı Adını Yazdırma ve Yayınlama
            join_message = f"{username} [TCP] sohbete katildi!\n"
            print(join_message)
            broadcast(join_message.encode('utf-8'))
            client.send(f"Hoşgeldiniz {username}, TCP ile bağlisiniz\n".encode('utf-8'))

            # İstemci İçin İş Parçacığı İşlemini Başlatma
            thread = threading.Thread(target=handle_tcp, args=(client,))
            thread.start()

# TCP ve UDP için İş Parçacıklarını Başlatma
threadTCP = threading.Thread(target=receive_tcp)
threadTCP.start()

threadUDP = threading.Thread(target=handle_udp)
threadUDP.start()
