#!/usr/bin/env python3
"""
Cimeika Chat Snapshot Generator
Створює HTML-снапшот чату у стилі Cimeika з елегантним дизайном.

Використання:
    cat chat.txt | python cimeika_snapshot.py out.html --title "Мій чат" --tags
    або
    pbpaste | python cimeika_snapshot.py out.html --tags   # macOS: із буфера
    або
    python cimeika_snapshot.py out.html --tags < chat.txt
"""

import sys
import argparse
import datetime
import html

TEMPLATE = """<!doctype html>
<html lang="uk">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{title}</title>
<style>
:root {{
    --gold1: #FFC34D;
    --gold2: #FFA72B;
    --bg1: #0A1022;
    --bg2: #0E1833;
    --ink: #EAF0FF;
    --muted: #9FB3C8;
}}

html, body {{
    margin: 0;
    padding: 0;
    background: linear-gradient(180deg, var(--bg1), var(--bg2));
    color: var(--ink);
    font: 16px/1.6 system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif;
}}

.wrap {{
    max-width: 860px;
    margin: 0 auto;
    padding: 22px 20px 90px;
}}

h1 {{
    margin: 0 0 6px;
    font-weight: 700;
    letter-spacing: 0.2px;
}}

.time {{
    color: var(--muted);
    font-size: 12px;
    margin-bottom: 16px;
}}

.goldline {{
    height: 2px;
    background: linear-gradient(90deg, var(--gold1), var(--gold2), transparent);
    filter: blur(0.3px);
    opacity: 0.95;
    margin: 12px 0 18px;
}}

.note {{
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 14px;
    padding: 14px 16px;
    margin: 12px 0;
}}

pre {{
    white-space: pre-wrap;
    word-wrap: break-word;
    background: linear-gradient(180deg, #131A36, #0C1228);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 12px;
    padding: 14px 16px;
    box-shadow: 
        0 10px 22px rgba(6, 10, 26, 0.45),
        0 2px 6px rgba(255, 195, 77, 0.18),
        inset 0 1px 0 rgba(255, 255, 255, 0.06);
}}

.tags {{
    list-style: none;
    padding: 0;
    margin: 10px 0;
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 10px;
}}

.tags li {{
    background: linear-gradient(180deg, #131A36, #0C1228);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 12px;
    padding: 10px 12px;
    box-shadow: 
        0 10px 22px rgba(6, 10, 26, 0.45),
        0 2px 6px rgba(255, 195, 77, 0.18),
        inset 0 1px 0 rgba(255, 255, 255, 0.06);
}}

footer {{
    position: fixed;
    left: 0;
    right: 0;
    bottom: 0;
    height: 90px;
    pointer-events: none;
    background: linear-gradient(0deg, rgba(255, 195, 77, 0.18), rgba(255, 195, 77, 0));
}}

/* Нижній золотий відлив-хвиля */
body::after {{
    content: "";
    position: fixed;
    left: -20%;
    right: -20%;
    bottom: -18%;
    height: 50%;
    border-radius: 50%;
    background: radial-gradient(60% 80% at 60% 100%, rgba(255, 195, 77, 0.22), rgba(255, 195, 77, 0));
    filter: blur(20px);
    opacity: 0.55;
    pointer-events: none;
}}

/* Адаптивний дизайн */
@media (max-width: 768px) {{
    .wrap {{
        padding: 16px 12px 90px;
    }}
    
    .tags {{
        grid-template-columns: 1fr;
    }}
    
    pre {{
        font-size: 14px;
        padding: 12px;
    }}
}}
</style>
</head>
<body>
  <div class="wrap">
    <h1>{title}</h1>
    <div class="time">Створено: {ts}</div>
    <div class="goldline"></div>
    {tags_block}
    <div class="note">Снапшот чату (офлайн-версія для перегляду у браузері).</div>
    <pre>{content}</pre>
  </div>
  <footer></footer>
</body>
</html>"""

def build(tags=False, title="Cimeika — Chat Snapshot", content=""):
    """
    Створює HTML-контент для снапшоту чату.
    
    Args:
        tags (bool): Чи додавати теги CIMEIKA
        title (str): Заголовок сторінки
        content (str): Вміст чату
    
    Returns:
        str: Готовий HTML-документ
    """
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    tags_block = ""
    if tags:
        tags_block = (
            '<h3>7 тегів CIMEIKA</h3>'
            '<ul class="tags">'
            "<li>ci</li><li>ПоДія</li><li>Настрій</li><li>Маля</li>"
            "<li>Казкар</li><li>Календар</li><li>Галерея</li>"
            "</ul><div class='goldline'></div>"
        )
    
    return TEMPLATE.format(
        title=html.escape(title),
        ts=ts,
        tags_block=tags_block,
        content=html.escape(content)
    )

def main():
    """Основна функція для обробки аргументів командного рядка."""
    parser = argparse.ArgumentParser(
        description="Створити HTML-снапшот чату у стилі Cimeika.",
        epilog="""
Приклади використання:
    cat chat.txt | python cimeika_snapshot.py out.html --title "Мій чат" --tags
    pbpaste | python cimeika_snapshot.py out.html --tags   # macOS
    python cimeika_snapshot.py out.html --tags < chat.txt
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "output", 
        help="Шлях до вихідного HTML файлу (наприклад, snapshot.html)"
    )
    parser.add_argument(
        "--title", 
        default="Cimeika — Chat Snapshot", 
        help="Заголовок сторінки"
    )
    parser.add_argument(
        "--tags", 
        action="store_true", 
        help="Додати 7 тегів CIMEIKA зверху"
    )
    
    args = parser.parse_args()
    
    # Читаємо текст із stdin
    try:
        text = sys.stdin.read()
    except KeyboardInterrupt:
        print("Операцію скасовано користувачем.")
        sys.exit(1)
    except Exception as e:
        print(f"Помилка при читанні даних: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Генеруємо HTML
    html_output = build(tags=args.tags, title=args.title, content=text)
    
    # Зберігаємо у файл
    try:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(html_output)
        print(f"✅ Успішно створено: {args.output}")
    except Exception as e:
        print(f"❌ Помилка при збереженні файлу: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()