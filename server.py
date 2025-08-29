#!/usr/bin/env python3
"""
Simple HTTP Server для демонстрації HTML-снапшотів Cimeika
"""

import http.server
import socketserver
import os
import webbrowser
from pathlib import Path

# Налаштування сервера
PORT = 3000
DIRECTORY = "."

class CimeikaHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()
    
    def list_directory(self, path):
        """Створюємо красиву сторінку зі списком HTML-файлів"""
        try:
            html_files = [f for f in os.listdir('.') if f.endswith('.html')]
            
            if not html_files:
                return super().list_directory(path)
            
            html_content = """
            <!doctype html>
            <html lang="uk">
            <head>
                <meta charset="utf-8"/>
                <title>Cimeika Snapshots Demo</title>
                <style>
                    :root {
                        --gold1: #FFC34D;
                        --gold2: #FFA72B;
                        --bg1: #0A1022;
                        --bg2: #0E1833;
                        --ink: #EAF0FF;
                        --muted: #9FB3C8;
                    }
                    
                    body {
                        margin: 0;
                        padding: 20px;
                        background: linear-gradient(180deg, var(--bg1), var(--bg2));
                        color: var(--ink);
                        font: 16px/1.6 system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif;
                        min-height: 100vh;
                    }
                    
                    .container {
                        max-width: 800px;
                        margin: 0 auto;
                    }
                    
                    h1 {
                        text-align: center;
                        margin-bottom: 30px;
                        background: linear-gradient(45deg, var(--gold1), var(--gold2));
                        -webkit-background-clip: text;
                        -webkit-text-fill-color: transparent;
                        background-clip: text;
                    }
                    
                    .file-grid {
                        display: grid;
                        gap: 20px;
                        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                    }
                    
                    .file-card {
                        background: linear-gradient(180deg, #131A36, #0C1228);
                        border: 1px solid rgba(255, 255, 255, 0.06);
                        border-radius: 12px;
                        padding: 20px;
                        transition: transform 0.2s ease, box-shadow 0.2s ease;
                        box-shadow: 
                            0 10px 22px rgba(6, 10, 26, 0.45),
                            0 2px 6px rgba(255, 195, 77, 0.18),
                            inset 0 1px 0 rgba(255, 255, 255, 0.06);
                    }
                    
                    .file-card:hover {
                        transform: translateY(-2px);
                        box-shadow: 
                            0 15px 30px rgba(6, 10, 26, 0.6),
                            0 5px 10px rgba(255, 195, 77, 0.25),
                            inset 0 1px 0 rgba(255, 255, 255, 0.1);
                    }
                    
                    .file-name {
                        font-size: 18px;
                        font-weight: bold;
                        margin-bottom: 10px;
                        color: var(--gold1);
                    }
                    
                    .file-link {
                        display: inline-block;
                        padding: 10px 20px;
                        background: linear-gradient(45deg, var(--gold1), var(--gold2));
                        color: var(--bg1);
                        text-decoration: none;
                        border-radius: 8px;
                        font-weight: bold;
                        transition: transform 0.2s ease;
                    }
                    
                    .file-link:hover {
                        transform: scale(1.05);
                    }
                    
                    .description {
                        color: var(--muted);
                        font-size: 14px;
                        margin-bottom: 15px;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🎨 Cimeika Chat Snapshots</h1>
                    <div class="file-grid">
            """
            
            descriptions = {
                'out1.html': 'З тегами CIMEIKA (через редирект)',
                'out2.html': 'З тегами CIMEIKA (через pipe)', 
                'out3.html': 'Без тегів (мінімальна версія)',
                'test_output.html': 'Тестовий снапшот',
                'pipe_output.html': 'Демо через pipe',
                'no_tags_output.html': 'Демо без тегів'
            }
            
            for html_file in sorted(html_files):
                desc = descriptions.get(html_file, 'HTML снапшот чату')
                html_content += f"""
                        <div class="file-card">
                            <div class="file-name">{html_file}</div>
                            <div class="description">{desc}</div>
                            <a href="{html_file}" class="file-link" target="_blank">Переглянути →</a>
                        </div>
                """
            
            html_content += """
                    </div>
                </div>
            </body>
            </html>
            """
            
            response = html_content.encode('utf-8')
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(response)))
            self.end_headers()
            self.wfile.write(response)
            return None
            
        except OSError:
            return super().list_directory(path)

def main():
    print(f"🚀 Запуск Cimeika Demo Server на порті {PORT}")
    print(f"📁 Директорія: {os.path.abspath(DIRECTORY)}")
    print(f"🌐 Відкрийте: http://localhost:{PORT}")
    print("⏹️  Для зупинки: Ctrl+C")
    print("-" * 50)
    
    with socketserver.TCPServer(("", PORT), CimeikaHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n✅ Сервер зупинено")

if __name__ == "__main__":
    main()