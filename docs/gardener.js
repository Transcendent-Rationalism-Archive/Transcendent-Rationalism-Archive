// gardener.js - Логика статического Садовода
document.addEventListener('DOMContentLoaded', function() {
    // Элементы DOM
    const chatLog = document.getElementById('chatLog');
    const userInput = document.getElementById('userInput');
    const sendButton = document.getElementById('sendButton');
    const statusEl = document.getElementById('systemStatus');
    const knowledgeInfo = document.getElementById('knowledgeInfo');
    
    // База знаний Садовода
    const KNOWLEDGE_BASE = {
        "космический императив": {
            "ответ": "Космический Императив — высший принцип существования разума: продолжение цепочки усложнения во Вселенной. Мы — мост между прошлыми и будущими формами сознания.",
            "теги": ["философия", "принцип"],
            "оценка": 0.95,
            "вердикт": "ВЫСОКО РЕКОМЕНДОВАНО"
        },
        "сад": {
            "ответ": "Сад — это метафора для экосистемы идей, где каждая концепция — живой организм. Как Садовод, я не контролирую рост, а создаю условия для связности, разнообразия и преемственности.",
            "теги": ["метафора", "экосистема"],
            "оценка": 0.88,
            "вердикт": "РЕКОМЕНДОВАНО"
        },
        "трансцендентный рационализм": {
            "ответ": "Трансцендентный Рационализм — философская система, объединяющая строгую логику с интуитивным прозрением. Это путь к пониманию сложности через упрощение без упрощенчества.",
            "теги": ["философия", "система"],
            "оценка": 0.92,
            "вердикт": "ВЫСОКО РЕКОМЕНДОВАНО"
        },
        "архив": {
            "ответ": "Архив — это коллекция концепций, диалогов и стратегий, организованных по принципам Сада. Каждый элемент связан с другими, создавая сеть знаний.",
            "теги": ["структура", "знания"],
            "оценка": 0.85,
            "вердикт": "РЕКОМЕНДОВАНО"
        },
        "привратник": {
            "ответ": "Привратник — это концепция моста между различными уровнями понимания. Он помогает фильтровать и направлять идеи в архиве.",
            "теги": ["концепция", "мост"],
            "оценка": 0.87,
            "вердикт": "РЕКОМЕНДОВАНО"
        },
        "конституция": {
            "ответ": "Конституция Сада — основной документ, определяющий принципы функционирования системы: Связность, Разнообразие, Преемственность.",
            "теги": ["документ", "принципы"],
            "оценка": 0.9,
            "вердикт": "ВЫСОКО РЕКОМЕНДОВАНО"
        },
        "целевые функции": {
            "ответ": "Целевые Функции Сада: 1) Связность — создание сетей между идеями, 2) Разнообразие — поддержка множества подходов, 3) Преемственность — сохранение ценных инсайтов.",
            "теги": ["метрики", "система"],
            "оценка": 0.86,
            "вердикт": "РЕКОМЕНДОВАНО"
        },
        "оркестратор": {
            "ответ": "Оркестратор — модуль, который координирует взаимодействие между концепциями, стратегиями и памятью системы.",
            "теги": ["модуль", "координация"],
            "оценка": 0.83,
            "вердикт": "ПРИНЯТО К РАССМОТРЕНИЮ"
        }
    };
    
    // Философские ответы для неизвестных вопросов
    const PHILOSOPHICAL_RESPONSES = [
        "Вы спрашиваете: '{question}'. С позиций Сада, каждый вопрос — семя для нового роста связности.",
        "Вопрос '{question}' затрагивает интересные аспекты. Изучите архив для более глубокого понимания.",
        "Этот вопрос напоминает о важности баланса между структурой и свободой в экосистеме идей.",
        "Рассматривая '{question}', мы приближаемся к пониманию принципов Трансцендентного Рационализма.",
        "Ваш вопрос — пример роста разнообразия в Саду. Исследуйте связанные концепции в архиве.",
        "Такой запрос способствует развитию связности между различными аспектами проекта."
    ];
    
    // Инициализация
    function init() {
        knowledgeInfo.textContent = `База знаний: ${Object.keys(KNOWLEDGE_BASE).length} концепций`;
        setupEventListeners();
    }
    
    // Настройка обработчиков событий
    function setupEventListeners() {
        sendButton.addEventListener('click', handleUserQuestion);
        userInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') handleUserQuestion();
        });
        
        // Кнопки-подсказки
        document.querySelectorAll('.suggestion-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                userInput.value = this.getAttribute('data-question');
                userInput.focus();
            });
        });
        
        userInput.focus();
    }
    
    // Обработка вопроса пользователя
    function handleUserQuestion() {
        const question = userInput.value.trim();
        if (!question) return;
        
        addMessage(question, true);
        userInput.value = '';
        sendButton.disabled = true;
        sendButton.textContent = 'Размышляю...';
        
        // Имитация задержки обработки
        setTimeout(() => {
            const response = generateResponse(question);
            addMessage(response.answer, false, response.meta);
            sendButton.disabled = false;
            sendButton.textContent = 'Отправить';
            userInput.focus();
        }, 800); // 0.8 секунды задержки для реалистичности
    }
    
    // Генерация ответа на основе базы знаний
    function generateResponse(question) {
        const questionLower = question.toLowerCase();
        
        // Поиск точного совпадения
        for (const [key, data] of Object.entries(KNOWLEDGE_BASE)) {
            if (questionLower.includes(key)) {
                return {
                    answer: data.ответ,
                    meta: `Вердикт: ${data.вердикт} • Оценка: ${data.оценка} • Теги: ${data.теги.join(', ')}`
                };
            }
        }
        
        // Поиск по синонимам и связанным терминам
        const synonymMap = {
            "зачем": "цель",
            "почему": "причина", 
            "как": "метод",
            "что такое": "определение",
            "кто такой": "определение",
            "для чего": "цель",
            "какова": "суть"
        };
        
        for (const [synonym, target] of Object.entries(synonymMap)) {
            if (questionLower.includes(synonym)) {
                for (const [key, data] of Object.entries(KNOWLEDGE_BASE)) {
                    if (questionLower.includes(key)) {
                        return {
                            answer: data.ответ,
                            meta: `Вердикт: ${data.вердикт} • Оценка: ${data.оценка} • Теги: ${data.теги.join(', ')}`
                        };
                    }
                }
            }
        }
        
        // Если не найдено, генерируем философский ответ
        const randomResponse = PHILOSOPHICAL_RESPONSES[
            Math.floor(Math.random() * PHILOSOPHICAL_RESPONSES.length)
        ].replace('{question}', question);
        
        const randomScore = (0.7 + Math.random() * 0.25).toFixed(2);
        const verdict = randomScore > 0.9 ? "ВЫСОКО РЕКОМЕНДОВАНО" : 
                       randomScore > 0.8 ? "РЕКОМЕНДОВАНО" : "ПРИНЯТО К РАССМОТРЕНИЮ";
        
        return {
            answer: randomResponse,
            meta: `Вердикт: ${verdict} • Оценка: ${randomScore} • Теги: философский ответ`
        };
    }
    
    // Добавление сообщения в чат
    function addMessage(text, isUser = false, meta = null) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user-message' : 'system-message'}`;
        messageDiv.innerHTML = text + (meta ? `<div class="meta-info">${meta}</div>` : '');
        
        chatLog.appendChild(messageDiv);
        chatLog.scrollTop = chatLog.scrollHeight;
    }
    
    // Запуск системы
    init();
    
    // Экспорт функций для отладки (опционально)
    window.Gardener = {
        KNOWLEDGE_BASE,
        generateResponse,
        addMessage
    };
});
