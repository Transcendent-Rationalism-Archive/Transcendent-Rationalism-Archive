#!/usr/bin/env python3
"""
scanner_v2.py - Улучшенный сканер ИИ-Садовода
Версия: 0.2.0
Назначение: Анализ структуры архива с игнорированием служебных папок
"""

import os
from pathlib import Path

def scan_archive(root_path="."):
    """Сканирует структуру архива, игнорируя служебные папки"""
    print("🔍 Улучшенный сканер архива...")
    print("=" * 50)
    
    root = Path(root_path)
    
    # Папки, которые нужно игнорировать
    ignore_folders = {'.git', '.github', '__pycache__', '.idea', '.vscode', 'node_modules'}
    
    # Считаем файлы по типам
    total_files = 0
    markdown_files = []
    
    for file_path in root.rglob("*"):
        if file_path.is_file():
            # Пропускаем файлы в игнорируемых папках
            if any(part in ignore_folders for part in file_path.parts):
                continue
            total_files += 1
            if file_path.suffix == ".md":
                markdown_files.append(file_path)
    
    # Анализируем структуру папок (исключая игнорируемые)
    folders = []
    for folder in root.rglob("*/"):
        if folder.is_dir():
            # Пропускаем игнорируемые папки
            if any(part in ignore_folders for part in folder.parts):
                continue
            folders.append(str(folder.relative_to(root)))
    
    # Проверяем наличие README в папках проекта
    project_folders = ['concepts', 'dialoguesstrategies', 'strategies', 'system', 'templates', 'core']
    folders_without_readme = []
    
    for folder in folders:
        # Проверяем только основные папки проекта
        folder_name = Path(folder).name
        if folder_name in project_folders or folder in project_folders:
            readme_path = root / folder / "README.md"
            if not readme_path.exists():
                folders_without_readme.append(folder)
    
    print(f"📊 РЕЗУЛЬТАТЫ СКАНИРОВАНИЯ:")
    print(f"   📁 Всего файлов: {total_files}")
    print(f"   📄 Markdown документов: {len(markdown_files)}")
    print(f"   📂 Папок проекта: {len(folders)}")
    print(f"   ⚠️  Папок без README: {len(folders_without_readme)}")
    
    if folders_without_readme:
        print(f"\n📌 Папки проекта без README.md:")
        for folder in folders_without_readme:
            print(f"   - {folder}")
    
    # Анализируем основные документы
    print(f"\n📚 ОСНОВНЫЕ ДОКУМЕНТЫ:")
    important_docs = [
        "manifest.md",
        "concepts/transcendental-rationalism.md",
        "concepts/garden-of-minds.md",
        "system/memory_protocols.md",
        "CHRONOLOGY.md",
        "core/companion-ai-manifesto-v1.md"
    ]
    
    for doc in important_docs:
        doc_path = root / doc
        if doc_path.exists():
            # Получаем размер файла
            size = doc_path.stat().st_size
            print(f"   ✅ {doc} ({size} байт)")
        else:
            print(f"   ❌ {doc} (отсутствует!)")
    
    # Анализ core
    print(f"\n🤖 КОМПОНЕНТЫ ИИ-СОРАТНИКА:")
    core_files = list((root / "core").rglob("*")) if (root / "core").exists() else []
    
    for file_type, extension in [("Python скрипты", ".py"), ("Документы", ".md"), ("Все файлы", "*")]:
        if extension == "*":
            files = core_files
        else:
            files = [f for f in core_files if f.suffix == extension]
        print(f"   📂 {file_type}: {len(files)}")
    
    print(f"\n💡 РЕКОМЕНДАЦИИ:")
    if len(markdown_files) < 30:
        print("   1. Добавить больше Markdown документов для развития архива")
    if folders_without_readme:
        print("   2. Создать README.md в папках проекта")
    print("   3. Проверить связи между документами")
    
    return {
        "total_files": total_files,
        "markdown_files": len(markdown_files),
        "project_folders": len(folders),
        "folders_without_readme": folders_without_readme
    }

def generate_structure_map(root_path="."):
    """Генерирует карту структуры проекта"""
    print(f"\n🗺️  КАРТА СТРУКТУРЫ ПРОЕКТА:")
    print("=" * 50)
    
    root = Path(root_path)
    ignore_folders = {'.git', '.github', '__pycache__', '.idea', '.vscode'}
    
    # Основные папки проекта
    project_folders = ['concepts', 'dialoguesstrategies', 'strategies', 'system', 'templates', 'core']
    
    for folder_name in project_folders:
        folder_path = root / folder_name
        if folder_path.exists():
            # Считаем файлы в папке
            files = list(folder_path.rglob("*"))
            # Исключаем файлы в подпапках для простоты
            direct_files = [f for f in folder_path.iterdir() if f.is_file()]
            
            print(f"\n{folder_name}/")
            print(f"  📁 Подпапок: {len([f for f in folder_path.iterdir() if f.is_dir()])}")
            print(f"  📄 Файлов: {len(direct_files)}")
            
            # Показываем первые 5 файлов
            for i, file in enumerate(direct_files[:5]):
                if i == 4 and len(direct_files) > 5:
                    print(f"  ... и ещё {len(direct_files) - 5} файлов")
                    break
                print(f"  - {file.name}")
        else:
            print(f"\n{folder_name}/ (отсутствует!)")

if __name__ == "__main__":
    print("=" * 60)
    print("ИИ-СОРАТНИК: АНАЛИЗ АРХИВА")
    print("=" * 60)
    
    results = scan_archive()
    generate_structure_map()
    
    print(f"\n" + "=" * 60)
    print("✅ Анализ завершен. Архив готов к развитию.")
    print("=" * 60)
