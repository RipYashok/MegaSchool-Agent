import requests
import xml.etree.ElementTree as ET
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
import os
from typing import List


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

API_KEY = os.getenv("API_KEY")
FOLDER_ID = os.getenv("FOLDER_ID")

class SearchRequest(BaseModel):
    query: str
    id: int

def get_llm_response(query: str) -> str:


    LLM_API_KEY = os.getenv("LLM_API_KEY")


    LLM_API_URL = 'https://api.together.xyz/v1/completions'



    headers = {
        'Authorization': f'Bearer {LLM_API_KEY}',
        'Content-Type': 'application/json'
    }


    data = {
        'model': 'meta-llama/Llama-Vision-Free',
        "messages": [{"role": "user", "content": query}],
        'max_tokens': 1000,
        'temperature': 0.7
    }

    
    response = requests.post(LLM_API_URL, headers=headers, json=data)

    
    if response.status_code == 200:
        result = response.json()
        if result['choices'][0]['text'] == '-1':
            return 'null'
        else:
            return int(result['choices'][0]['text'])
    else:
        error_message = f'Ошибка: {response.status_code}\n{response.text}'
        return error_message
    

@app.post("/api/request")
async def search(request: SearchRequest):
    try:
        logger.debug(f"Получен запрос с query: {request.query}")
        
        
        url = f"https://yandex.ru/search/xml?folderid={FOLDER_ID}&apikey={API_KEY}&query={request.query}"

        
        params = {
            "text": request.query,
            "lang": "ru", 
            "type": "web",
            "limit": 1,
        }
        
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        logger.debug("Получен ответ от API")
        
        
        logger.debug(f"Ответ API: {response.text}")
        
        
        root = ET.fromstring(response.text)
        search_results = []
        
        extended = ""
        sources = []
        
        for doc in root.findall('.//doc')[:3]: 
            url_elem = doc.find('.//url')
            extended_elem = doc.find('.//extended-text')
            
            url = (url_elem.text if url_elem is not None and url_elem.text 
                  else "URL не найден")
            sources.append(url)
            extended += (extended_elem.text + " " if extended_elem is not None and extended_elem.text 
                      else "")
            
            logger.debug(f"Найденные данные: url={url}, extended={extended}")
            
        result = '''Вопрос может включать в себя варианты ответа 1-10 или может быть открытым (без вариантов ответа)
    Формат вывода ответа:
    Если вопрос требует выбора варианта, верни ТОЛЬКО число, обозначающее номер ответа, например если варианты
    ответа - 1 X 2 Y - ты должен ответить "1" если правильный ответ "X". 
    Если вариантов ответа НЕТ - ответь ТОЛЬКО "-1".\n''' + request.query + "\n Дополнительная информация: \n" + extended
        
        answer = get_llm_response(result)

        search_results = {
            "id": request.id,
            "answer": answer,
            "reasoning": extended,
            "sources": sources
            }
              
        return search_results
        
    except Exception as e:
        logger.error(f"Произошла ошибка: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при выполнении поиска: {str(e)}"
        )

