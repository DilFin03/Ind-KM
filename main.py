import socket
import threading
import json
from datetime import datetime

# Шлях до файлу з користувачами
USERS_FILE = "users.txt"

# Шлях до файлу для збереження історії повідомлень
HISTORY_FILE = "messages_history.txt"

# Завантаження користувачів з файлу
def load_users():
    users = {}
    try:
        with open(USERS_FILE, "r") as file:
            for line in file:
                parts = line.strip().split(":")
                if len(parts) == 2:
                    users[parts[0]] = parts[1]
    except FileNotFoundError:
        print("Файл з користувачами не знайдено.")
    return users

# Функція для збереження повідомлення в історії
def save_message_to_history(username, message):
    with open(HISTORY_FILE, "a") as file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = {"username": username, "message": message, "timestamp": timestamp}
        file.write(json.dumps(data) + "\n")

# Функція для обробки підключеного клієнта
def handle_client(client_socket, addr):
    # Аутентифікація користувача
    authenticated = False
    username = ""
    while not authenticated:
        client_socket.send(b"Enter username: ")
        username = client_socket.recv(1024).decode().strip()
        client_socket.send(b"Enter password: ")
        password = client_socket.recv(1024).decode().strip()
        if username in users and users[username] == password:
            authenticated = True
            client_socket.send(b"Authentication successful!\n")
        else:
            client_socket.send(b"Invalid username or password. Please try again.\n")

    # Додати клієнта до списку підключених клієнтів
    clients.append(client_socket)

    while True:
        try:
            # Отримати повідомлення від клієнта
            message = client_socket.recv(1024).decode().strip()
            if message:
                # Додати ім'я користувача до повідомлення
                message_with_username = f"{username}: {message}"
                # Переслати повідомлення всім клієнтам
                for c in clients:
                    c.send(message_with_username.encode())
                # Зберігати повідомлення в історії
                save_message_to_history(username, message)
        except:
            # Якщо сталася помилка, видалити клієнта зі списку
            clients.remove(client_socket)
            client_socket.close()
            break

# Головна функція для запуску сервера
def main():
    global users
    users = load_users()

    # Задати IP-адресу та порт сервера
    host = '127.0.0.1'
    port = 12345

    # Створити сокет
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Прив'язати сокет до IP-адреси та порту
    server_socket.bind((host, port))

    # Почекати на підключення
    server_socket.listen(5)
    print(f"Сервер запущено на {host}:{port}")

    # Список для збереження підключених клієнтів
    global clients
    clients = []

    while True:
        # Приймати підключення
        client_socket, addr = server_socket.accept()
        print(f"Новий клієнт підключився: {addr}")

        # Створити окремий потік для обробки клієнта
        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_thread.start()

if __name__ == "__main__":
    main()
