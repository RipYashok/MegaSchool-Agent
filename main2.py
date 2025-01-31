import requests

def get_llm_response(prompt: str) -> str:


    LLM_API_KEY = 'b00f6f6100f8a03080f6c3df294e0bbd9716fa55c8f58541660ab47a92fa4740'


    LLM_API_URL = 'https://api.together.xyz/v1/completions'

    # query = '''Вопрос может включать в себя варианты ответа 1-10 или может быть открытым (без вариантов ответа)
    # Формат вывода ответа:
    # Если вопрос требует выбора варианта, верни ТОЛЬКО число, обозначающее номер ответа, например если варианты
    # ответа - 1. X 2. Y - ты должен ответить "1." если правильный ответ "X". 
    # Если вариантов ответа НЕТ - ответь ТОЛЬКО "-1".\n''' + prompt

    query = '''Вопрос может включать в себя варианты ответа 1-10 или может быть открытым (без вариантов ответа)
    Формат вывода ответа:
    Если вопрос требует выбора варианта, верни СНАЧАЛА число, обозначающее номер ответа, например если варианты
    ответа - 1 X 2 Y - ты должен ответить "1" если правильный ответ "X". Потом пояснение, почему ты выбрал этот ответ.
    Если вариантов ответа НЕТ - ответь ТОЛЬКО "-1".\n''' + prompt

    headers = {
        'Authorization': f'Bearer {LLM_API_KEY}',
        'Content-Type': 'application/json'
    }


    data = {
        'model': 'meta-llama/Llama-3.3-70B-Instruct-Turbo-Free',
        "messages": [{"role": "user", "content": query}],
        'max_tokens': 1000,
        'temperature': 0.7
    }

    # Выполнение POST-запроса
    response = requests.post(LLM_API_URL, headers=headers, json=data)

    # Проверка статуса ответа
    if response.status_code == 200:
        result = response.json()
        if result['choices'][0]['text'] == '-1':
            return 'null'
        else:
            return result['choices'][0]['text'][0]
    else:
        error_message = f'Ошибка: {response.status_code}\n{response.text}'
        return error_message
    
print(get_llm_response("В каком году Университет ИТМО был включён в число Национальных исследовательских университетов России?\n1. 2007\n2. 2009\n3. 2011\n4. 2015"))