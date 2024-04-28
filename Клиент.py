import socket
import threading
# Функція для отримання повідомлень від сервера
def receive_messages(client_socket):
    while True:
        try:
            # Отримати повідомлення від сервера
            message = client_socket.recv(1024).decode()
            if message:
                print(message)
        except:
            # Якщо сталася помилка, закрити з'єднання
            print("Помилка: втрачено з'єднання з сервером.")
            client_socket.close()
            break

# Основна функція клієнта
def main():
    # Задати IP-адресу та порт сервера
    #host = '127.0.0.1'
    #port = 12345
    # Введення IP-адреси та порту сервера
    host = input("Введіть IP-адресу сервера: ")
    port = int(input("Введіть порт сервера: "))

    # Підключитися до сервера
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
    except:
        print("Помилка: не вдалося підключитися до сервера.")
        return

    # Запустити окремий потік для отримання повідомлень від сервера
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    # Основний цикл для відправлення повідомлень
    while True:
        message = input()
        try:
            client_socket.send(message.encode())
        except:
            print("Помилка: втрачено з'єднання з сервером.")
            client_socket.close()
            break

if __name__ == "__main__":
    main()
