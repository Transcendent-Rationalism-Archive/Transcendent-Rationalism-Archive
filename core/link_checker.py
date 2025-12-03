#!/usr/bin/env python3
"""
link_checker.py - Простой анализатор связей
Версия: 0.1.0
Назначение: Проверка ссылок между документами
"""

import os
import re
from pathlib import Path

def main():
    print("=" * 60)
    print("ПРОСТОЙ АНАЛИЗАТОР СВЯЗЕЙ")
    print("=" * 60)
    
    # Находим все .md файлы
    md_files = []
    for root, dirs, files in os.walk("."):
        # Пропускаем служебные папки
        if '.git' in root:
            continue
            
        for file in files:
            if file.endswith('.md'):
                full_path = os.path.join(root, file)
                md_files.append(full_path)
    
    print(f"Найдено Markdown файлов: {len(md_files)}")
    
    links = []
    broken_links = []
    
    for md_file in md_files[:50]:  # Проверяем первые 50 файлов
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Ищем ссылки вида [текст](ссылка)
            matches = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
            
            for text, target in matches:
                # Пропускаем внешние ссылки
                if target.startswith(('http://', 'https://', '#')):
                    continue
                
                # Проверяем, существует ли файл
                file_dir = os.path.dirname(md_file)
                target_path = os.path.join(file_dir, target)
                exists = os.path.exists(target_path)
                
                link_info = {
                    'source': md_file[2:],  # Убираем './' в начале
                    'target': target,
                    'exists': exists
                }
                
                links.append(link_info)
                if not exists:
                    broken_links.append(link_info)
                    
        except Exception as e:
            print(f"Ошибка при чтении {md_file}: {e}")
    
    print(f"\n📊 РЕЗУЛЬТАТЫ:")
    print(f"   Проверено ссылок: {len(links)}")
    print(f"   Битых ссылок: {len(broken_links)}")
    
    if broken_links:
        print(f"\n⚠️  БИТЫЕ ССЫЛКИ (первые 10):")
        for link in broken_links[:10]:
            print(f"   Из: {link['source']}")
            print(f"   В: {link['target']}")
            print()
    
    # Анализ структуры
    print(f"\n📁 СТРУКТУРА АРХИВА:")
    
    # Ключевые папки
    key_folders = ['concepts', 'dialoguesstrategies', 'strategies', 'system', 'templates', 'core']
    
    for folder in key_folders:
        if os.path.exists(folder):
            files = os.listdir(folder)
            md_count = sum(1 for f in files if f.endswith('.md'))
            print(f"   {folder}/: {len(files)} файлов, {md_count} .md")
        else:
            print(f"   {folder}/: отсутствует")
    
    print(f"\n" + "=" * 60)
    print("✅ Проверка завершена")
    print("=" * 60)
    
    # Сохраняем отчет
    with open('link_check_report.txt', 'w') as f:
        f.write(f"Отчет проверки ссылок\n")
        f.write(f"====================\n")
        f.write(f"Проверено ссылок: {len(links)}\n")
        f.write(f"Битых ссылок: {len(broken_links)}\n\n")
        
        if broken_links:
            f.write("Битые ссылки:\n")
            for link in broken_links:
                f.write(f"Из: {link['source']}\n")
                f.write(f"В: {link['target']}\n\n")

if __name__ == "__main__":
    main()
