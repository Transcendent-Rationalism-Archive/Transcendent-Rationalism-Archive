#!/usr/bin/env python3
"""
link_analyzer.py - Анализатор связей между документами
Версия: 0.1.0
Назначение: Поиск и анализ ссылок между документами архива
"""

import re
from pathlib import Path

class LinkAnalyzer:
    def __init__(self, root_path="."):
        self.root = Path(root_path)
        self.documents = {}
        self.links = []
        self.broken_links = []
    
    def analyze_links(self):
        """Анализирует все ссылки между документами"""
        print("🔗 Анализирую связи между документами...")
        
        # Находим все Markdown файлы
        md_files = list(self.root.rglob("*.md"))
        
        for md_file in md_files:
            # Пропускаем служебные папки
            if any(part in ['.git', '__pycache__'] for part in md_file.parts):
                continue
            
            rel_path = md_file.relative_to(self.root)
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Извлекаем все ссылки вида [текст](ссылка)
            links_in_file = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
            
            for link_text, link_target in links_in_file:
                # Игнорируем внешние ссылки и якоря
                if link_target.startswith(('http://', 'https://', '#', 'mailto:')):
                    continue
                
                # Нормализуем путь
                target_path = (md_file.parent / link_target).resolve()
                
                self.links.append({
                    'source': str(rel_path),
                    'target': link_target,
                    'text': link_text,
                    'exists': target_path.exists(),
                    'target_abs': str(target_path.relative_to(self.root) if target_path.exists() else link_target)
                })
        
        # Анализируем результаты
        self.broken_links = [link for link in self.links if not link['exists']]
        
        return self
    
    def print_report(self):
        """Печатает отчет о связях"""
        print(f"\n📊 ОТЧЕТ О СВЯЗЯХ:")
        print(f"   Всего внутренних ссылок: {len(self.links)}")
        print(f"   Рабочих ссылок: {len(self.links) - len(self.broken_links)}")
        print(f"   Битых ссылок: {len(self.broken_links)}")
        
        if self.broken_links:
            print(f"\n⚠️  БИТЫЕ ССЫЛКИ:")
            for link in self.broken_links[:10]:  # Показываем первые 10
                print(f"   Из: {link['source']}")
                print(f"   В: {link['target']}")
                print(f"   Текст: {link['text'][:50]}...")
                print()
        
        # Находим документы без входящих ссылок
        all_targets = [link['target_abs'] for link in self.links if link['exists']]
        all_sources = list(set(link['source'] for link in self.links))
        
        print(f"\n📄 ДОКУМЕНТЫ БЕЗ ВХОДЯЩИХ ССЫЛОК:")
        md_files = list(self.root.rglob("*.md"))
        for md_file in md_files[:20]:  # Проверяем первые 20
            rel_path = str(md_file.relative_to(self.root))
            if rel_path not in all_targets and not any(part in ['.git'] for part in md_file.parts):
                print(f"   - {rel_path}")
    
    def suggest_improvements(self):
        """Предлагает улучшения для архива"""
        print(f"\n💡 ПРЕДЛОЖЕНИЯ ПО УЛУЧШЕНИЮ:")
        
        if len(self.links) < 10:
            print("   1. Добавить больше перекрестных ссылок между документами")
        
        if self.broken_links:
            print(f"   2. Исправить {len(self.broken_links)} битых ссылок")
        
        # Проверяем наличие метаданных в документах
        md_files = list(self.root.rglob("*.md"))
        docs_without_id = []
        
        for md_file in md_files[:10]:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if '**ID:**' not in content and 'manifest.md' not in str(md_file):
                    docs_without_id.append(str(md_file.relative_to(self.root)))
        
        if docs_without_id:
            print(f"   3. Добавить метаданные (ID, автор, дата) в документы:")
            for doc in docs_without_id[:3]:
                print(f"      - {doc}")

if __name__ == "__main__":
    print("=" * 60)
    print("АНАЛИЗАТОР СВЯЗЕЙ ДОКУМЕНТОВ")
    print("=" * 60)
    
    analyzer = LinkAnalyzer()
    analyzer.analyze_links()
    analyzer.print_report()
    analyzer.suggest_improvements()
    
    print(f"\n" + "=" * 60)
    print("✅ Анализ связей завершен.")
    print("=" * 60)
