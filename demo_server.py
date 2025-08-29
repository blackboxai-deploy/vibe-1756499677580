#!/usr/bin/env python3
"""
Простий HTTP-сервер для демонстрації HTML-снапшотів чату
"""

import http.server
import socketserver
import webbrowser
import os
import sys

PORT = 3000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

def main():
    try:
        # Змінюємо директорію на поточну
        os.chdir('.')
        
        # Створюємо сервер
        with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
            print(f"✅ Сервер запущено на http://localhost:{PORT}")
            print(f"📁 Обслуговую директорію: {os.getcwd()}")
            print("\n📋 Доступні HTML-снапшоти:")
            
            # Показуємо список HTML файлів
            html_files = [f for f in os.listdir('.') if f.endswith('.html')]
            for html_file in html_files:
                print(f"   • http://localhost:{PORT}/{html_file}")
            
            print(f"\n🛑 Натисніть Ctrl+C для зупинки сервера")
            
            # Запускаємо сервер
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n\n✅ Сервер зупинено")
    except Exception as e:
        print(f"❌ Помилка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()