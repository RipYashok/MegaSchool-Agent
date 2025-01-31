import socket
import os
from dotenv import load_dotenv

def get_local_ip():
    try:
        # Получаем локальный IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"

def create_env_file():
    # Загружаем существующие переменные, если есть
    load_dotenv()
    
    # Получаем IP
    ip = get_local_ip()
    
    # Создаем или обновляем .env файл
    with open('.env', 'w') as f:
        f.write(f'HOST_IP={ip}\n')
        f.write(f'HOST_PORT={os.getenv("HOST_PORT", "8000")}\n')
        f.write(f'LLM_API_KEY={os.getenv("LLM_API_KEY", "your_api_key_here")}\n')

if __name__ == "__main__":
    create_env_file()
    print("Файл .env создан/обновлен успешно!") 