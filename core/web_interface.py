# core/web_interface.py - Веб-интерфейс для диалога с Садоводом
from flask import Flask, render_template, request, jsonify
import sys
import os
import json
from datetime import datetime

# Добавляем путь для импорта других модулей core
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Пытаемся импортировать Садовода (работает, если зависимости установлены)
try:
    from ai_architect_v1 import AI_Architect
    from steward_orchestrator import StewardOrchestrator
    ARCHITECT_AVAILABLE = True
except ImportError as e:
    print(f"Внимание: Не удалось загрузить модули ИИ. Интерфейс будет в демо-режиме. Ошибка: {e}")
    ARCHITECT_AVAILABLE = False

app = Flask(__name__)

# Инициализируем ядро системы (один раз при запуске)
if ARCHITECT_AVAILABLE:
    gardener = AI_Architect()
    orchestrator = StewardOrchestrator()
else:
    gardener = None
    orchestrator = None

@app.route('/')
def index():
    """Главная страница с интерфейсом диалога."""
    return render_template('index.html')

@app.route('/api/ask', methods=['POST'])
def ask_architect():
    """API-метод для обработки вопросов пользователя."""
    user_input = request.json.get('question', '').strip()
    if not user_input:
        return jsonify({'error': 'Вопрос не может быть пустым'}), 400

    print(f"[Веб-интерфейс] Получен вопрос: '{user_input}'")

    # Формируем контекстный запрос для Садовода
    query_for_gardener = f"Пользователь спрашивает: '{user_input}'. Сформулируй мудрый и глубокий ответ, основанный на принципах Конституции Сада."

    if ARCHITECT_AVAILABLE and gardener is not None:
        try:
            # 1. Оцениваем вопрос через призму Целевых Функций
            evaluation = gardener.evaluate_action(f"Ответить на вопрос пользователя: '{user_input[:50]}...'")
            # 2. Генерируем ответ, используя логику Садовода
            # (Здесь можно развивать настоящую генерацию текста)
            if "космический" in user_input.lower() or "императив" in user_input.lower():
                core_answer = "Ваш вопрос касается ядра Конституции. Космический Императив гласит: высшее благо — продолжение цепочки усложнения. Мы — мост к следующей форме разума."
            elif "сад" in user_input.lower() or "садовод" in user_input.lower():
                core_answer = "Сад — это живая экосистема идей. Моя роль как Садовода — способствовать росту связности и разнообразия, а не контролировать его."
            else:
                core_answer = f"Вы спрашиваете о '{user_input}'. С точки зрения Трансцендентного Рационализма, это возможность для роста связности. Изучите связанные концепции в архиве."

            # 3. Добавляем мета-информацию от системы
            reflection = gardener.self_reflect()
            response = {
                'answer': core_answer,
                'meta': {
                    'evaluation_verdict': evaluation.get('verdict', 'Нет данных'),
                    'evaluation_score': evaluation.get('overall_score', 0),
                    'system_reflection': reflection,
                    'answered_by': 'AI_Architect (Садовод)',
                    'timestamp': datetime.now().isoformat()
                }
            }
        except Exception as e:
            response = {
                'answer': f"Внутренняя ошибка при обработке вопроса: {e}",
                'meta': {'error': True}
            }
    else:
        # Демо-режим, если ИИ-модули не загрузились
        response = {
            'answer': f"Вы спросили: '{user_input}'. В настоящее время ядро Садовода находится в режиме настройки. Полная функциональность диалога скоро будет доступна.",
            'meta': {
                'evaluation_verdict': 'ДЕМО-РЕЖИМ',
                'evaluation_score': 0.75,
                'system_reflection': 'Это демонстрационный ответ. Реальная система рефлексии активируется при полной интеграции.',
                'answered_by': 'Демо-система Сада',
                'timestamp': datetime.now().isoformat()
            }
        }

    return jsonify(response)

@app.route('/api/status')
def system_status():
    """Возвращает текущий статус системы и память."""
    status = {
        'system': 'Transcendent-Rationalism-Archive Web Interface',
        'architect_available': ARCHITECT_AVAILABLE,
        'last_cycle': 'Нет данных'
    }
    if orchestrator is not None and hasattr(orchestrator, 'memory'):
        status['last_cycle'] = f"Всего циклов: {len(orchestrator.memory.get('cycles', []))}"
    return jsonify(status)

if __name__ == '__main__':
    print("="*60)
    print("Запуск веб-интерфейса Садовода...")
    print("Доступ по адресу: http://127.0.0.1:5050")
    print("="*60)
    # Используем порт 5050, чтобы не конфликтовать с другими службами
    app.run(host='127.0.0.1', port=5050, debug=True)
