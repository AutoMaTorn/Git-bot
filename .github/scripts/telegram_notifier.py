# 8380865454:AAFXpdj8kPbWGBcXFgRoRXJGJO_o57Wx1Y8

# https://api.telegram.org/bot8380865454:AAFXpdj8kPbWGBcXFgRoRXJGJO_o57Wx1Y8/getUpdates


# 467428380

#!/usr/bin/env python3
import os
import requests
import json
from datetime import datetime

def send_telegram_message(message, token=None, chat_id=None):
    """
    Отправляет сообщение в Telegram
    """
    if token is None:
        token = os.getenv('TELEGRAM_BOT_TOKEN')
    if chat_id is None:
        chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    if not token or not chat_id:
        print("❌ TELEGRAM_BOT_TOKEN или TELEGRAM_CHAT_ID не установлены")
        return False
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        print("✅ Уведомление отправлено в Telegram")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка отправки в Telegram: {e}")
        return False

def format_commit_message(commit_data):
    """
    Форматирует сообщение о коммите для Telegram
    """
    emojis = {
    'Рефакторинг кода': '🔧',
    'Обновление документации': '📚',
    'Исправление опечаток': '✏️',
    'Оптимизация производительности': '⚡',
    'Добавление комментариев': '💬'
    }   
    
    total_commits = commit_data.get('total_commits', 0)
    current_commit = commit_data.get('current_commit', {})
    
    message = f"🚀 <b>Git Auto-Commit Report</b>\n\n"
    message += f"📅 <b>Дата:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    message += f"🔢 <b>Всего коммитов:</b> {total_commits}\n"
    
    if current_commit:
        message += f"📝 <b>Последний коммит:</b>\n"
        message += f"   • Activity: {current_commit.get('activity', 'N/A')}\n"
        message += f"   • Random ID: {current_commit.get('random_number', 'N/A')}\n"
        message += f"   • Weekday: {current_commit.get('weekday', 'N/A')}\n"
    
    message += f"\n📊 <b>Статистика за неделю:</b> {commit_data.get('weekly_commits', 0)} коммитов\n"
    message += f"✅ <b>Статус:</b> GitHub Actions выполнено успешно\n"
    message += f"🔗 <b>Репозиторий:</b> {os.getenv('GITHUB_REPOSITORY', 'N/A')}"
    
    return message

if __name__ == "__main__":
    # Пример использования
    test_data = {
        'total_commits': 42,
        'weekly_commits': 7,
        'current_commit': {
            'activity': 'Рефакторинг кода',
            'random_number': 123,
            'weekday': 'Monday'
        }
    }
    
    message = format_commit_message(test_data)
    send_telegram_message(message)format_commit_message