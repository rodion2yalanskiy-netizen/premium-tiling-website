#!/usr/bin/env python3
"""
save_report.py — Сохраняет ответ агента как .md заметку в reports/ и делает git commit.
Запускается после antigravity.py в GitHub Actions.
"""

import os
import sys
import subprocess
from datetime import datetime, timezone
from pathlib import Path


def read_agent_output() -> tuple[str, str]:
    """Читает ответ агента и имя задачи из временных файлов."""
    response_file = Path("/tmp/agent_response.txt")
    task_name_file = Path("/tmp/agent_task_name.txt")

    if not response_file.exists():
        print("❌ /tmp/agent_response.txt не найден — antigravity.py не запускался?")
        sys.exit(1)

    response = response_file.read_text(encoding="utf-8").strip()
    task_name = task_name_file.read_text(encoding="utf-8").strip() if task_name_file.exists() else "unknown-task"

    return response, task_name


def save_report(response: str, task_name: str) -> Path:
    """Сохраняет отчёт в reports/ с датой и статусом."""
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)

    now = datetime.now(timezone.utc)
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M UTC")
    safe_name = task_name.replace(" ", "_").replace("/", "-")[:50]
    filename = f"report_{date_str}_{safe_name}.md"

    content = f"""---
task: {task_name}
date: {date_str}
time: {time_str}
status: completed
source: github-actions
model: anthropic/claude-sonnet-4-20250514
---

# Отчёт: {task_name}

**Дата:** {date_str} {time_str}
**Статус:** ✅ Выполнено

---

{response}
"""

    report_path = reports_dir / filename
    report_path.write_text(content, encoding="utf-8")
    print(f"📄 Отчёт сохранён: {report_path}")
    return report_path


def git_commit(report_path: Path, task_name: str):
    """Делает git add + commit для отчёта."""
    subprocess.run(["git", "add", str(report_path)], check=True)

    commit_msg = f"Agent report: {task_name}"
    result = subprocess.run(
        ["git", "commit", "-m", commit_msg],
        capture_output=True,
        text=True,
    )

    if result.returncode == 0:
        print(f"✅ Git commit: {commit_msg}")
    else:
        if "nothing to commit" in result.stdout + result.stderr:
            print("ℹ️  Нечего коммитить (файл уже актуален)")
        else:
            print(f"❌ Git commit failed: {result.stderr}")
            sys.exit(1)


def main():
    response, task_name = read_agent_output()
    report_path = save_report(response, task_name)
    git_commit(report_path, task_name)
    print(f"🎉 Готово! Отчёт: {report_path}")


if __name__ == "__main__":
    main()
