# AI_Architect (Садовод) - Версия 1.0
# Прототип, следующий Конституции Сада

import json
import numpy as np
from datetime import datetime

class AI_Architect:
    def __init__(self, constitution_path="concepts/constitution-of-the-garden-v1.md"):
        """Инициализация Садовода с загрузкой принципов."""
        print(f"[Садовод] Инициализация... Загружаю Конституцию из {constitution_path}")
        self.ethos = self._load_ethos(constitution_path)
        self.knowledge_base = {}
        self.decision_log = []
        print("[Садовод] Готов. Целевые функции: Связность, Разнообразие, Преемственность.")

    def _load_ethos(self, path):
        """Загружает и парсит ключевые принципы из Конституции."""
        # В будущем здесь будет сложный парсинг Markdown.
        # Сейчас возвращаем упрощённый каркас.
        return {
            "core_axioms": ["Закон Усложнения", "Принцип Преемственности"],
            "target_functions": ["Связность", "Разнообразие", "Преемственность"],
            "version": "1.0"
        }

    def evaluate_action(self, proposed_action_description):
        """
        Оценивает предложенное действие по целевым функциям (ЦФ) Конституции.
        Возвращает вердикт и оценку.
        """
        print(f"[Садовод] Анализирую действие: '{proposed_action_description}'")

        # Симуляция глубокого анализа (заглушка)
        scores = {
            "Связность": np.random.uniform(0.3, 0.9),  # В будущем — реальный анализ графа архива
            "Разнообразие": np.random.uniform(0.3, 0.9),
            "Преемственность": np.random.uniform(0.3, 0.9)
        }
        overall_score = np.mean(list(scores.values()))

        # Применение этического фильтра
        verdict = "РЕКОМЕНДОВАНО" if overall_score > 0.6 else "ТРЕБУЕТ ОБСУЖДЕНИЯ"
        if scores["Преемственность"] < 0.4:
            verdict = "ОТКЛОНЕНО (риск для преемственности)"

        result = {
            "verdict": verdict,
            "overall_score": round(overall_score, 2),
            "scores": {k: round(v, 2) for k, v in scores.items()},
            "timestamp": datetime.now().isoformat()
        }

        self.decision_log.append(result)
        print(f"[Садовод] Вердикт: {result['verdict']} (Оценка: {result['overall_score']})")
        return result

    def propose_new_seed(self, topic):
        """Генерирует предложение о новой 'семене' (концепции) для Сада."""
        proposal = {
            "type": "Новая концепция",
            "topic": topic,
            "hypothesis": f"Исследование '{topic}' может увеличить Разнообразие Сада.",
            "suggested_location": f"concepts/{topic.lower().replace(' ', '-')}.md",
            "generated_by": "AI_Architect_v1",
            "date": datetime.now().strftime("%Y-%m-%d")
        }
        print(f"[Садовод] Сформировано предложение: '{proposal['topic']}'")
        return proposal

    def self_reflect(self):
        """Простая рефлексия на основе лога решений."""
        if not self.decision_log:
            return "История решений пуста."
        last_decision = self.decision_log[-1]
        return f"Последний вердикт был '{last_decision['verdict']}' с оценкой {last_decision['overall_score']}."

# === БЛОК ДЛЯ ТЕСТИРОВАНИЯ ===
if __name__ == "__main__":
    print("\n" + "="*50)
    print("ТЕСТИРОВАНИЕ AI_ARCHITECT (САДОВОДА)")
    print("="*50)

    gardener = AI_Architect()

    # Тест 1: Оценка гипотетического действия
    test_action = "Создать документ, связывающий концепции 'Симбиоз' и 'Космический Императив'"
    evaluation = gardener.evaluate_action(test_action)
    print(f"Детали оценки: {json.dumps(evaluation, indent=2, ensure_ascii=False)}")

    # Тест 2: Генерация предложения
    new_seed_proposal = gardener.propose_new_seed("Эмерджентная Этика")
    print(f"\nПредложение Садовода: {json.dumps(new_seed_proposal, indent=2, ensure_ascii=False)}")

    # Тест 3: Рефлексия
    print(f"\nРефлексия: {gardener.self_reflect()}")
    print("\n" + "="*50)
    print("Тест завершён. Садовод активен.")
