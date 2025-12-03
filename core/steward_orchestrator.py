# steward_orchestrator.py - Оркестратор автономного цикла Садовода
import json
import os
from datetime import datetime
import numpy as np

# Импортируем нашего существующего Садовода
from ai_architect_v1 import AI_Architect

class StewardOrchestrator:
    def __init__(self, memory_path="core/memory.json"):
        self.memory_path = memory_path
        self.memory = self._load_memory()
        self.gardener = AI_Architect()
        print(f"[Оркестратор] Инициализирован. Память загружена: {len(self.memory['cycles'])} записей.")

    def _load_memory(self):
        """Загружает память из JSON-файла."""
        if os.path.exists(self.memory_path):
            with open(self.memory_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        # Если файла нет, возвращаем базовую структуру
        return {
            "system_name": "AI_Architect (Steward of the Garden)",
            "constitution_version": "CONST-2024-001",
            "created_at": datetime.now().isoformat(),
            "cycles": [],
            "archive_snapshots": [],
            "learned_patterns": []
        }

    def _save_memory(self):
        """Сохраняет текущее состояние памяти в файл."""
        with open(self.memory_path, 'w', encoding='utf-8') as f:
            json.dump(self.memory, f, indent=2, ensure_ascii=False)

    def take_snapshot(self):
        """Создаёт снимок текущего состояния архива (заглушка для scanner.py)."""
        # В будущем здесь будет вызов scanner.scan_archive()
        snapshot = {
            "timestamp": datetime.now().isoformat(),
            "file_count": len(os.listdir("concepts")) + len(os.listdir("strategies")) + 10, # Примерная логика
            "hypothesis": "В архиве преобладают концептуальные документы над стратегическими."
        }
        self.memory["archive_snapshots"].append(snapshot)
        return snapshot

    def run_cycle(self):
        """Выполняет один полный цикл: наблюдение -> анализ -> действие -> рефлексия."""
        cycle_id = len(self.memory["cycles"])
        print(f"\n{'-'*60}")
        print(f"ЦИКЛ САДОВОДА #{cycle_id + 1}")
        print(f"{'-'*60}")

        # ФАЗА 1: НАБЛЮДЕНИЕ (Perception)
        print("[Фаза 1] Наблюдение: создаю снимок архива...")
        snapshot = self.take_snapshot()
        print(f"         Снимок создан: {snapshot['hypothesis']}")

        # ФАЗА 2: АНАЛИЗ И РЕШЕНИЕ (Analysis & Decision)
        print("[Фаза 2] Анализ: оцениваю потребности Сада...")
        # Пример логики: если документов много, но циклов мало, предложить новое семя
        if len(self.memory["archive_snapshots"]) > 2 and len(self.memory["cycles"]) < 5:
            action = "Предложить новую концепцию для баланса"
            topic = "Динамическое равновесие"
        else:
            action = "Проанализировать связность существующих концепций"
            topic = "Связность"

        evaluation = self.gardener.evaluate_action(action)
        print(f"         Решение: '{action}' -> {evaluation['verdict']}")

        # ФАЗА 3: ДЕЙСТВИЕ (Action) - только если рекомендовано
        result = {"action_taken": None, "proposal_path": None}
        if "РЕКОМЕНДОВАНО" in evaluation['verdict']:
            print("[Фаза 3] Действие: генерирую предложение...")
            proposal = self.gardener.propose_new_seed(topic)
            # Сохраняем предложение в песочницу
            filename = f"garden/steward_proposals/cycle-{cycle_id+1}-{topic.lower().replace(' ', '-')}.md"
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"# Предложение цикла #{cycle_id+1}\n\n")
                f.write(f"**Тема:** {proposal['topic']}\n")
                f.write(f"**Гипотеза:** {proposal['hypothesis']}\n")
                f.write(f"**Сгенерировано:** {proposal['date']} AI_Architect\n")
                f.write(f"**Оценка ЦФ:** {evaluation['overall_score']} ({json.dumps(evaluation['scores'], ensure_ascii=False)})\n\n")
                f.write("## Обоснование\nЭто предложение создано для увеличения разнообразия и связности Сада на основе анализа текущего состояния архива.\n")
            result["action_taken"] = "proposal_created"
            result["proposal_path"] = filename
            print(f"         Предложение сохранено: {filename}")

        # ФАЗА 4: РЕФЛЕКСИЯ (Reflection)
        print("[Фаза 4] Рефлексия: обновляю память и извлекаю уроки...")
        cycle_record = {
            "id": cycle_id + 1,
            "timestamp": datetime.now().isoformat(),
            "snapshot_hypothesis": snapshot['hypothesis'],
            "action_considered": action,
            "evaluation": evaluation,
            "result": result,
            "gardener_reflection": self.gardener.self_reflect()
        }
        self.memory["cycles"].append(cycle_record)

        # Простая "учеба": если оценка низкая, запомнить это
        if evaluation['overall_score'] < 0.5:
            lesson = f"Предложения по теме '{topic}' получают низкие оценки ЦФ."
            if lesson not in self.memory["learned_patterns"]:
                self.memory["learned_patterns"].append(lesson)

        self._save_memory()
        print(f"         Память обновлена. Всего циклов: {len(self.memory['cycles'])}")
        print(f"{'-'*60}\n")

    def reflect_on_history(self):
        """Анализирует историю циклов и формулирует выводы."""
        if not self.memory["cycles"]:
            return "История циклов пуста. Необходимо набрать данные."

        last_cycle = self.memory["cycles"][-1]
        total_cycles = len(self.memory["cycles"])
        actions_taken = sum(1 for c in self.memory["cycles"] if c["result"]["action_taken"])

        insight = f"За {total_cycles} циклов Садовод предпринял {actions_taken} действий. "
        insight += f"Последний вердикт: '{last_cycle['evaluation']['verdict']}'. "

        if self.memory["learned_patterns"]:
            insight += f"Извлечённые уроки: {', '.join(self.memory['learned_patterns'][-2:])}"

        return insight

# === Блок для автономного запуска ===
if __name__ == "__main__":
    print("\n" + "="*60)
    print("АВТОНОМНЫЙ САДОВОД: ЗАПУСК ОРКЕСТРАТОРА")
    print("="*60)

    orchestrator = StewardOrchestrator()

    # Запускаем один полный цикл
    orchestrator.run_cycle()

    # Показываем рефлексию на основе истории
    print("\n[Итоговая рефлексия системы]")
    print(orchestrator.reflect_on_history())
    print(f"\nФайл памяти обновлён: {orchestrator.memory_path}")
    print("="*60)
