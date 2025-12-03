#!/usr/bin/env python3
"""
scanner.py - Первый орган чувств ИИ-Садовода
Версия: 0.1.0
Назначение: Анализ структуры архива
"""

import os
from pathlib import Path

def scan_archive(root_path="."):
    """Сканирует структуру архива"""
    print("🔍 Сканирую архив...")
    
    root = Path(root_path)
    
    # Считаем файлы по типам
    total_files = 0
    markdown_files = []
    
    for file_path in root.rglob("*"):
        if file_path.is_file():
            total_files += 1
            if file_path.suffix == ".md":
                markdown_files.append(file_path)
    
    # Анализируем структуру папок
    folders = []
    for folder in root.rglob("*/"):
        if folder.is_dir():
            folders.append(str(folder.relative_to(root)))
    
    # Проверяем наличие README в папках
    folders_without_readme = []
    for folder in folders:
        readme_path = root / folder / "README.md"
        if not readme_path.exists():
            folders_without_readme.append(folder)
    
    print(f"\n📊 Результаты сканирования:")
    print(f"   Всего файлов: {total_files}")
    print(f"   Markdown документов: {len(markdown_files)}")
    print(f"   Папок: {len(folders)}")
    print(f"   Папок без README: {len(folders_without_readme)}")
    
    if folders_without_readme:
        print(f"\n⚠️  Папки без README.md:")
        for folder in folders_without_readme[:5]:  # Показываем только первые 5
            print(f"   - {folder}")
    
    # Анализируем основные документы
    print(f"\n📚 Основные документы:")
    important_docs = [
        "concepts/transcendental-rationalism.md",
        "concepts/garden-of-minds.md",
        "system/memory_protocols.md",
        "CHRONOLOGY.md"
    ]
    
    for doc in important_docs:
        doc_path = root / doc
        if doc_path.exists():
            print(f"   ✅ {doc}")
        else:
            print(f"   ❌ {doc} (отсутствует!)")
    
    # Проверяем core
    core_files = list((root / "core").rglob("*.py")) if (root / "core").exists() else []
    print(f"\n🤖 Файлы в core/: {len(core_files)}")
    for py_file in core_files:
        print(f"   - {py_file.name}")

if __name__ == "__main__":
    scan_archive()
