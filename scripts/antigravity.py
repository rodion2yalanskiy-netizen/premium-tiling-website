#!/usr/bin/env python3
"""
antigravity.py — Читает задачу из tasks/, отправляет в OpenRouter, сохраняет ответ.
Запускается из GitHub Actions. Результат сохраняется в /tmp/agent_response.txt
"""

import os
import sys
import json
import requests
from pathlib import Path

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
TASK_FILE = os.environ.get("TASK_FILE", "")
MODEL = "anthropic/claude-sonnet-4-20250514"
MAX_TOKENS = 2000


def find_task_file() -> Path:
    """Находит файл задачи — из env или берёт самый новый в tasks/."""
    if TASK_FILE:
        p = Path(TASK_FILE)
        if p.exists():
            return p
        print(f"⚠️  Файл {TASK_FILE} не найден, ищу в tasks/")

    tasks_dir = Path("tasks")
    md_files = sorted(tasks_dir.glob("*.md"), key=lambda f: f.stat().st_mtime, reverse=True)
    if not md_files:
        print("❌ В папке tasks/ нет .md файлов")
        sys.exit(1)
    return md_files[0]


def read_task(task_path: Path) -> str:
    """Читает только текст задачи без метаданных vault."""
    content = task_path.read_text(encoding="utf-8").strip()

    # Убираем YAML frontmatter если есть
    if content.startswith("---"):
        end = content.find("---", 3)
        if end != -1:
            content = content[end + 3:].strip()

    return content


def call_openrouter(task_text: str, task_name: str) -> str:
    """Отправляет задачу в OpenRouter и возвращает ответ."""
    if not OPENROUTER_API_KEY:
        print("❌ OPENROUTER_API_KEY не задан в secrets")
        sys.exit(1)

    prompt = f"""Ты — AI-агент для выполнения задач из системы управления проектами QSNera.

Задача: {task_name}

Содержание:
{task_text}

Выполни задачу. Ответ дай в формате Markdown с разделами:
## ✅ Выполнено
## 📋 Детали
## 💡 Рекомендации (если есть)"""

    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": MAX_TOKENS,
        "stream": False,
    }

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/rodion2yalanskiy-netizen/premium-tiling-website",
        "X-Title": "QSNera Agent Pipeline",
    }

    print(f"📤 Отправляю задачу '{task_name}' в OpenRouter ({MODEL})...")

    resp = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=60,
    )
    resp.raise_for_status()

    data = resp.json()
    answer = data["choices"][0]["message"]["content"]

    usage = data.get("usage", {})
    print(f"✅ Ответ получен. Токены: {usage.get('prompt_tokens', '?')} in / {usage.get('completion_tokens', '?')} out")

    return answer


def main():
    task_path = find_task_file()
    task_name = task_path.stem
    print(f"📄 Задача: {task_path}")

    task_text = read_task(task_path)
    if not task_text:
        print("❌ Файл задачи пустой")
        sys.exit(1)

    response = call_openrouter(task_text, task_name)

    # Сохраняем ответ и имя задачи для save_report.py
    Path("/tmp/agent_response.txt").write_text(response, encoding="utf-8")
    Path("/tmp/agent_task_name.txt").write_text(task_name, encoding="utf-8")
    print(f"💾 Ответ сохранён во временный файл")


if __name__ == "__main__":
    main()
