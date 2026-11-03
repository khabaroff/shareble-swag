# Персональный куратор контента с n8n

**Демо-лекция для Podlodka Crew**

**Дата:** 17 февраля 2026, вторник

**Спикер:** Сергей Хабаров

[![Запись демо](<AI Crew Lecture Cover Khabarov.jpg>)](https://www.youtube.com/watch?v=aMFlrcwkxAI)

- **[▶ Запись демо (YouTube)](https://www.youtube.com/watch?v=aMFlrcwkxAI)**
- **[→ Разбор на khabaroff.com](https://khabaroff.com/personal-content-filter/)**

## О демо

Создаем персональный фильтр контента с Youtube за час. Чтобы попробовать собрать параллельно на встрече или отдельно до/после, нам понадобится:

1. Завести ТГ-бота через @BotFather
2. Узнать свой номер телеграма @userinfobot
3. Зарегистрироваться https://n8n.io/
4. Зарегистрироваться на https://www.firecrawl.dev/
5. И на https://openrouter.ai/ или OpenAI API или Anthropic API

### Что делаем

Строим n8n-автоматизацию для интеллектуальной фильтрации контента:

1. **Сбор** — YouTube, Telegram, email-рассылки
2. **Анализ** — AI-агент фильтрует по вашим критериям
3. **Доставка** — получаете только релевантное

### Результат

Работающий сценарий для масштабирования на всю команду.

## Материалы

- [README-detailed.md](README-detailed.md) — полное техническое описание сценария, архитектуры и инструкции по запуску
- [Prompt to start with](<Prompt to start with.md>) — стартовый промпт для генерации базового сценария в n8n AI
- [Prompt NoCode Short](<Prompt NoCode Short.md>) — краткая версия промпта для автоматизации
- [Prompt NoCode Long](<Prompt NoCode Long.md>) — расширенная версия с деталями реализации
- [Prompt Video Eval](<Prompt Video Eval.md>) — промпт для оценки видео по 100-балльной шкале
- [Презентация](2026-02-17%20Podlodka%20Crew.pdf) — слайды лекции
- [Эволюция фильтра контента](<Эволюция фильтра контента.excalidraw>) — схема итераций (открыть в [excalidraw.com](https://excalidraw.com/))
- Workflow JSON для импорта в n8n — четыре шага эволюции сценария, от простого (001) до самого полного (004) с AI-оценкой и саммари:
  [001](<001 YouTube Channel Monitor with Telegram Notifications.json>) ·
  [002](<002 YouTube Channel Monitor with Telegram Notifications.json>) ·
  [003](<003 YouTube Channel Monitor with Telegram Notifications.json>) ·
  [004](<004 YouTube Channel Monitor with Telegram Notifications.json>).
  После импорта подключите свои credentials и замените `YOUR_TELEGRAM_CHAT_ID` на свой Telegram ID.

---

**Вопросы:** @khabaroff
