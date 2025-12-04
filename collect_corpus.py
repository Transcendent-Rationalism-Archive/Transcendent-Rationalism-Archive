#!/usr/bin/env python3
import os, re
from pathlib import Path

def clean_text(text):
    text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
    return text.strip()

corpus_lines = []
root = Path('.').resolve()

for filepath in root.rglob('*'):
    if filepath.is_file() and filepath.suffix.lower() in {'.md', '.txt', '.py', '.js', '.html'}:
        try:
            content = filepath.read_text(encoding='utf-8', errors='ignore')
            if content.strip():
                cleaned = clean_text(content)
                rel_path = filepath.relative_to(root)
                corpus_lines.append(f"\n{'='*60}\n📄 ФАЙЛ: {rel_path}\n{'='*60}\n{cleaned}")
                print(f"✓ {rel_path}")
        except:
            pass

output = '\n'.join(corpus_lines)
(Path('docs') / 'corpus.txt').write_text(output, encoding='utf-8')
short = output[:5000] + "\n[...]"
(Path('docs') / 'corpus_short.txt').write_text(short, encoding='utf-8')
print(f"\n✅ corpus.txt создан в docs/. Полный размер: {len(output)} символов")
