import logging
import re

# Настройка логирования
logging.basicConfig(
    level=logging.INFO, 
    filename='app.log', 
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Словарь синонимов
synonyms = {
    "привет": ["здравствуйте", "добрый день", "доброе утро"],
    "пока": ["до свидания", "до встречи"],
    "расскажи": ["познакомь", "объясни", "опиши"],
    "что такое": ["определение", "объясни", "расскажи про"],
    "как": ["каким образом", "способ", "метод"],
    "новое": ["новости", "обновление", "изменения"],
    "помочь": ["подсказать", "объяснить", "показать"],
    "информация": ["данные", "сведения", "факты"]
}

def expand_query(query):
    # Замена синонимов на базовые слова
    for key, values in synonyms.items():
        for syn in values:
            query = query.replace(syn, key)
    return query

def eval_expr(expression):
    try:
        return eval(expression)
    except Exception as e:
        logging.error(f"Ошибка при вычислении: {str(e)}")
        return "Ошибка вычисления"

def process_input(input_text):
    logging.info(f"Получен запрос: {input_text}")
    input_text = expand_query(input_text.lower())
    
    try:
        # Математические операции
        if any(char in input_text for char in '+-*/'):
            return str(eval_expr(input_text))
        
        # Обработка приветствий
        if re.search(r'\b(привет|здравствуйте|добрый день)\b', input_text):
            return "Здравствуйте! Как я могу вам помочь?"
        
        # Обработка прощаний
        if re.search(r'\b(пока|до свидания|до встречи)\b', input_text):
            return "До свидания! Было приятно помочь."
        
        # Вопросы о себе
        if re.search(r'\b(расскажи|познакомь|кто ты|о себе)\b', input_text):
            return "Я — интеллектуальный помощник, созданный для помощи в решении различных задач."
        
        # Вопросы о новостях
        if re.search(r'\b(новое|новости|обновление)\b', input_text):
            return "Я постоянно учусь и развиваюсь, чтобы лучше помогать вам! " \
                   "Недавно я улучшил понимание естественного языка и расширил базу знаний."
        
        # Вопросы по программированию
        if re.search(r'\b(python|java|javascript|программирование)\b', input_text):
            return "Я могу помочь с вопросами по программированию на различных языках. " \
                   "Какой язык вас интересует?"
        
        # Обработка общих вопросов
        if "что такое" in input_text:
            topic = input_text.split('что такое ')[1]
            return f"Давайте я расскажу про {topic.capitalize()}. " \
                   f"{topic.capitalize()} — это интересная тема, связанная с..."
        
        if "как" in input_text:
            action = input_text.split('как ')[1]
            return f"Вот как это работает: для {action} нужно..."
        
        # Обработка запросов на помощь
        if re.search(r'\b(помочь|подсказать|объяснить)\b', input_text):
            return "Конечно! Спрашивайте, я постараюсь помочь."
        
        # Если не нашли точного совпадения
        return "Не смогла найти точный ответ на ваш вопрос. " \
               "Попробуем спросить по-другому?"
    
    except Exception as e:
        logging.error(f"Ошибка при обработке: {str(e)}")
        return "Произошла ошибка при обработке запроса"
