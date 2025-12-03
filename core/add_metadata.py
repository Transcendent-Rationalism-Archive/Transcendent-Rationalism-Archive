#!/usr/bin/env python3
"""
add_metadata.py - Добавление метаданных в документы
Версия: 0.1.0
"""

import os
import re
from pathlib import Path
from datetime import datetime

def add_metadata_to_file(filepath, metadata):
    """Добавляет метаданные в начало файла"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Проверяем, есть ли уже метаданные
    if '**ID:**' in content:
        print(f"  ⏭️  {filepath} - уже имеет метаданные")
        return False
    
    # Создаем блок метаданных
    meta_block = "\n".join([f"**{k}:** {v}" for k, v in metadata.items()])
    meta_block = f"\n{meta_block}\n\n"
    
    # Вставляем после первого заголовка (#)
    lines = content.split('\n')
    new_lines = []
    
    for i, line in enumerate(lines):
        new_lines.append(line)
        if line.startswith('# ') and i == 0:
            # Нашли заголовок первого уровня
            new_lines.append(meta_block)
    
    new_content = '\n'.join(new_lines)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True

def main():
    print("=" * 60)
    print("ДОБАВЛЕНИЕ МЕТАДАННЫХ В ДОКУМЕНТЫ")
    print("=" * 60)
    
    # Маппинг папок к типам документов
    folder_types = {
        'concepts': 'CON',
        'strategies': 'STR',
        'system': 'SYS',
        'dialoguesstrategies': 'DLG',
        'templates': 'TPL'
    }
    
    total_added = 0
    
    for folder, prefix in folder_types.items():
        if not os.path.exists(folder):
            continue
            
        print(f"\n📁 Обрабатываю папку: {folder}/")
        
        for filename in os.listdir(folder):
            if filename.endswith('.md') and filename != 'README.md':
                filepath = os.path.join(folder, filename)
                
                # Генерируем ID
                doc_id = f"{prefix}-2024-{total_added + 1:03d}"
                
                metadata = {
                    'ID': doc_id,
                    'Автор': 'Водан',
                    'Дата создания': datetime.now().strftime('%Y-%m-%d'),
                    'Статус': 'Активный',
                    'Версия': '1.0.0'
                }
                
                if add_metadata_to_file(filepath, metadata):
                    print(f"  ✅ {filename} -> {doc_id}")
                    total_added += 1
    
    # Обрабатываем файлы в корне
    print(f"\n📁 Обрабатываю корневые файлы:")
    
    root_files = ['manifest.md', 'symbiosis-v2.md']
    
    for filename in root_files:
        if os.path.exists(filename):
            metadata = {
                'ID': 'ROOT-2024-001' if filename == 'manifest.md' else 'STR-2024-002',
                'Автор': 'Водан',
                'Дата создания': '2024-01-15',
                'Статус': 'Активный',
                'Версия': '1.0.0'
            }
            
            if add_metadata_to_file(filename, metadata):
                print(f"  ✅ {filename}")
                total_added += 1
    
    print(f"\n" + "=" * 60)
    print(f"✅ Добавлено метаданных: {total_added} документов")
    print("=" * 60)

if __name__ == "__main__":
    main()
