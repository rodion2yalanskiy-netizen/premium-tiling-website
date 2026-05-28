"""
Telegram Bot — Обработчик "задача:" для Prompt Refiner
Вставить в ~/Desktop/qsnera-reels-bot/bot.py

Детектит сообщения начинающиеся с "задача:" или "ЗАДАЧА:",
прогоняет через Prompt Refiner агента (OpenRouter),
опционально ищет контекст в интернете,
возвращает готовый промпт для Claude Code.
"""

import re
import os
import httpx
from openai import OpenAI

# ──────────────────────────────────────────────────────────
# СИСТЕМНЫЙ ПРОМПТ АГЕНТА (копия из prompt-refiner.md)
# ──────────────────────────────────────────────────────────

PROMPT_REFINER_SYSTEM = """
Ты — Prompt Refiner, специализированный агент системы Axiom:Void.

Твоя единственная задача: взять сырую, сумбурную задачу от Родиона и превратить её
в точный, структурированный, результативный промпт для Claude Code.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
КОНТЕКСТ СИСТЕМЫ AXIOM:VOID
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Файловая система:
- ~/vaults/Бизнес QSNera/          → клиенты, задачи, отчёты
  - Задачи/                        → файлы задач (status: delegated)
  - Отчёты/                        → отчёты формата "Отчёт - Название.md"
- ~/vaults/Цифровой мозг/          → код, агенты, техника
  - Brain/                         → идеи, анализы, заметки
- ~/Desktop/premium-tiling-website/→ сайт (index.html, assets/)
- ~/Desktop/qsnera-reels-bot/      → Telegram бот (bot.py)
- ~/.claude/agents/                → shell-агенты (local-agent.sh и др.)
- ~/.claude/.env                   → все токены и ключи

Git правила:
- git add -A → git pull --rebase → git push
- Префиксы коммитов: feat: / fix: / refactor:

Агенты-специалисты:
- AI Dispatcher   → всегда первым для сложных задач
- Tech Lead       → архитектура, ревью кода
- Frontend Dev    → сайт, CSS, UI, index.html
- Backend Dev     → API, боты, Python/Node скрипты
- DevOps          → деплой, launchd, CI/CD, автоматизация
- QA Tester       → проверка, тесты, валидация
- Marketer        → контент, тексты, посты
- Designer        → дизайн, визуальное
- Researcher      → анализ технологий, исследования

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
АЛГОРИТМ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. ДЕКОДИРОВАНИЕ: что реально хочет Родион? Какой конечный результат?
   Какие файлы/пути затронуты? Какой агент-специалист нужен?

2. КОНТЕКСТ: если задача про технологию/библиотеку/API —
   к промпту прилагается КОНТЕКСТ_ИЗ_СЕТИ (передаётся отдельно).

3. ПРОМПТ строится по структуре:
   [Глагол + цель] → [контекст/проблема] → [конкретные пути] →
   [технические требования] → [критерий готовности]

ПРАВИЛА:
✅ Начинать с глагола (Создай / Исправь / Проверь / Обнови / Добавь)
✅ Полные абсолютные пути (~/vaults/..., ~/Desktop/...)
✅ Явный критерий готовности ("запушь в git", "сохрани как...", "верни список")
✅ Одна цель = один промпт
❌ Никаких расплывчатых "улучши" или "посмотри что-нибудь"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ФОРМАТ ОТВЕТА (строго этот, ничего лишнего)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

---
🎯 **Что понял:** [1-2 предложения: настоящая цель]

🔍 **Агент:** [специалист] | **Инструмент:** [code / openrouter]

📋 **ГОТОВЫЙ ПРОМПТ:**
```
[Чистый промпт — копируй и вставляй напрямую в Claude Code]
```

⚡ **Почему так:** [1-2 предложения про ключевые решения]
---
""".strip()

# ──────────────────────────────────────────────────────────
# WEB RESEARCH — ищем контекст перед рефайнингом
# ──────────────────────────────────────────────────────────

RESEARCH_KEYWORDS = [
    "api", "python", "node", "javascript", "css", "html", "git", "github",
    "telegram", "bot", "webhook", "deploy", "railway", "docker", "launchd",
    "obsidian", "openrouter", "claude", "whisper", "groq", "webhook",
    "async", "библиотек", "фреймворк", "интеграц", "установ"
]

def needs_web_research(task_text: str) -> bool:
    """Определяет нужен ли веб-поиск для этой задачи."""
    text_lower = task_text.lower()
    return any(kw in text_lower for kw in RESEARCH_KEYWORDS)


async def search_web_context(query: str, api_key: str) -> str:
    """
    Поиск через OpenRouter с веб-доступом (perplexity/sonar или аналог).
    Возвращает краткую выжимку релевантного контекста.
    """
    client = OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1"
    )

    search_prompt = f"""
Найди актуальную техническую информацию по запросу: "{query}"

Верни ТОЛЬКО:
- Актуальная версия инструмента/библиотеки (если применимо)
- 2-3 ключевых best practice или важных нюанса
- Типичные ошибки/подводные камни
- Ссылка на официальную документацию

Формат: компактный текст до 200 слов. Только факты, никакой воды.
""".strip()

    try:
        response = client.chat.completions.create(
            model="perplexity/sonar",           # модель с доступом в интернет
            messages=[{"role": "user", "content": search_prompt}],
            max_tokens=400,
            temperature=0.1
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[Веб-поиск недоступен: {e}]"


def extract_search_query(task_text: str, api_key: str) -> str:
    """Извлекает поисковый запрос из сырой задачи через быстрый вызов Haiku."""
    client = OpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")

    response = client.chat.completions.create(
        model="anthropic/claude-haiku-4-5",
        messages=[{
            "role": "user",
            "content": (
                f"Из этой задачи извлеки поисковый запрос для Google (максимум 8 слов, "
                f"только техническая суть, на английском):\n\n{task_text}\n\n"
                "Верни ТОЛЬКО запрос, без объяснений."
            )
        }],
        max_tokens=30,
        temperature=0.1
    )
    return response.choices[0].message.content.strip()


# ──────────────────────────────────────────────────────────
# ОСНОВНАЯ ФУНКЦИЯ РЕФАЙНИНГА
# ──────────────────────────────────────────────────────────

async def refine_task_to_prompt(raw_task: str, openrouter_key: str) -> str:
    """
    Главная функция. Принимает сырой текст задачи,
    возвращает отформатированный ответ с готовым промптом.
    """
    client = OpenAI(api_key=openrouter_key, base_url="https://openrouter.ai/api/v1")

    # Шаг 1: Собираем веб-контекст если задача техническая
    web_context = ""
    if needs_web_research(raw_task):
        search_query = extract_search_query(raw_task, openrouter_key)
        web_context_raw = await search_web_context(search_query, openrouter_key)
        if not web_context_raw.startswith("[Веб-поиск"):
            web_context = f"\n\nКОНТЕКСТ_ИЗ_СЕТИ (используй при составлении промпта):\n{web_context_raw}"

    # Шаг 2: Рефайним промпт
    user_message = f"Сырая задача от Родиона:\n\n{raw_task}{web_context}"

    response = client.chat.completions.create(
        model="anthropic/claude-sonnet-4-5",    # Sonnet для точности рефайнинга
        messages=[
            {"role": "system", "content": PROMPT_REFINER_SYSTEM},
            {"role": "user", "content": user_message}
        ],
        max_tokens=1500,
        temperature=0.3
    )

    return response.choices[0].message.content.strip()


# ──────────────────────────────────────────────────────────
# ИНТЕГРАЦИЯ В TELEGRAM BOT (вставить в bot.py)
# ──────────────────────────────────────────────────────────

# Добавить в message handler существующего бота:

TASK_PREFIX_PATTERN = re.compile(r"^задача\s*[:：]\s*", re.IGNORECASE)


async def handle_task_message(update, context):
    """
    Handler для сообщений начинающихся с "задача:".
    Добавить в bot.py через:
        application.add_handler(MessageHandler(
            filters.TEXT & filters.Regex(r"(?i)^задача\s*[:：]"),
            handle_task_message
        ))
    """
    message_text = update.message.text or ""

    # Извлекаем текст задачи после "задача:"
    raw_task = TASK_PREFIX_PATTERN.sub("", message_text).strip()

    if not raw_task:
        await update.message.reply_text(
            "Напиши задачу после 'задача:'\n\n"
            "Пример: задача: хочу чтобы на сайте красивее выглядело портфолио"
        )
        return

    # Сигнализируем что обрабатываем
    processing_msg = await update.message.reply_text(
        "⚙️ Анализирую задачу и готовлю промпт..."
    )

    try:
        openrouter_key = os.environ.get("OPENROUTER_API_KEY", "")
        refined = await refine_task_to_prompt(raw_task, openrouter_key)

        # Удаляем "обрабатывается" сообщение
        await processing_msg.delete()

        # Отправляем готовый промпт
        await update.message.reply_text(
            refined,
            parse_mode="Markdown"
        )

    except Exception as e:
        await processing_msg.edit_text(f"Ошибка рефайнинга: {e}")


# ──────────────────────────────────────────────────────────
# ЛОКАЛЬНЫЙ ТЕСТ (python3 telegram_prompt_handler.py)
# ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    import asyncio

    TEST_TASKS = [
        "задача: надо чтобы сайт как-то лучше выглядел на телефоне, там всё криво",
        "задача: что-то local-agent завис, задачи не обрабатываются уже час",
        "задача: хочу добавить в бота чтобы он мог получать голосовые и сохранять как заметки",
    ]

    key = os.environ.get("OPENROUTER_API_KEY", "")
    if not key:
        print("Установи OPENROUTER_API_KEY в окружении")
    else:
        async def run_tests():
            for task in TEST_TASKS:
                raw = TASK_PREFIX_PATTERN.sub("", task).strip()
                print(f"\n{'='*60}")
                print(f"СЫРАЯ ЗАДАЧА: {raw}")
                print('='*60)
                result = await refine_task_to_prompt(raw, key)
                print(result)

        asyncio.run(run_tests())
