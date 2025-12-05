import logging
import re
import requests
from googlesearch import search # нужно установить библиотеку: pip install googlesearch-python

# Настройка логирования
logging.basicConfig(level=logging.INFO, filename='app.log', filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Инициализация памяти диалога
dialog_history = []

def search_in_internet(query, num_results=3):
    try:
        results = search(query, num_results=num_results)
        return results
    except Exception as e:
        logging.error(f"Ошибка при поиске: {str(e)}")
        return []

def process_input(input_text):
    global dialog_history
    logging.info(f"Получен запрос: {input_text}")
    input_text = input_text.lower()
    
    # Добавляем запрос в историю диалога
    dialog_history.append(input_text)
    
    try:
        # Проверяем известные запросы
        if any(char in input_text for char in '+-*/'):
            return str(eval_expr(input_text))
        
        # Если не нашли подходящего ответа, ищем в интернете
        if not any(keyword in input_text for keyword in known_keywords):
            search_results = search_in_internet(input_text)
            if search_results:
                return f"Не нашла точного ответа, но вот полезные ссылки:\n" + "\n".join(search_results)
        
        # Обработка диалога
        if "помню ли я" in input_text:
            return f"В нашей беседе мы обсуждали: {', '.join(dialog_history)}"
        
        # Остальные проверки остаются без изменений
        # ... (предыдущий код)
        
        return "Не смогла найти ответ на ваш вопрос. Давайте попробуем спросить по-другому?"
    
    except Exception as e:
        logging.error(f"Ошибка при обработке: {str(e)}")
        return "Произошла ошибка при обработке запроса"

def eval_expr(expression):
    try:
        return eval(expression)
    except Exception as e:
        logging.error(f"Ошибка при вычислении: {str(e)}")
        return "Ошибка вычисления"

# Установка необходимых библиотек
# pip install googlesearch-python

# Важно: для работы с поисковыми API может потребоваться:
# - Регистрация в Google Custom Search
# - Получение API ключа
# - Настройка безопасности в Google Cloud Console

