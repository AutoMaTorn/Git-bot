#!/usr/bin/env python3
import json
import datetime
import random
import os
import sys

# Добавляем путь для импорта
sys.path.append(os.path.dirname(__file__))
from telegram_notifier import send_telegram_message, format_commit_message

def generate_commit_data():
    """Генерирует данные для коммита"""
    activities = [
        "Рефакторинг кода",
        "Обновление документации", 
        "Исправление опечаток",
        "Оптимизация производительности",
        "Добавление комментариев",
        "Обновление зависимостей",
        "Тестирование новых функций",
        "Улучшение README",
        "Багофиксинг",
        "Код ревью",
        "Улучшение архитектуры",
        "Добавление тестов"
    ]
    
    filename = "activities.json"
    
    # Читаем существующие данные
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {"commits": [], "statistics": {}}
    else:
        data = {"commits": [], "statistics": {}}
    
    # Создаем новую запись
    current_time = datetime.datetime.utcnow()
    new_commit = {
        "timestamp": current_time.isoformat(),
        "message": f"Автоматический коммит от {current_time.strftime('%Y-%m-%d %H:%M:%S')}",
        "random_number": random.randint(1, 1000),
        "activity": random.choice(activities),
        "weekday": current_time.strftime("%A"),
        "commit_hash": f"auto_{current_time.strftime('%Y%m%d_%H%M%S')}"
    }
    
    data["commits"].append(new_commit)
    total_commits = len(data["commits"])
    
    # Обновляем статистику
    week_ago = current_time - datetime.timedelta(days=7)
    weekly_commits = len([
        c for c in data["commits"] 
        if datetime.datetime.fromisoformat(c["timestamp"]).date() >= week_ago.date()
    ])
    
    data["statistics"] = {
        "total_commits": total_commits,
        "last_updated": current_time.isoformat(),
        "this_week_commits": weekly_commits,
        "this_month_commits": len([
            c for c in data["commits"] 
            if datetime.datetime.fromisoformat(c["timestamp"]).month == current_time.month
        ])
    }
    
    # Сохраняем файл
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Файл обновлен! Всего коммитов: {total_commits}")
    
    return {
        "total_commits": total_commits,
        "weekly_commits": weekly_commits,
        "current_commit": new_commit,
        "filename": filename
    }

def main():
    try:
        # Генерируем данные коммита
        commit_data = generate_commit_data()
        
        # Формируем и отправляем сообщение в Telegram
        message = format_commit_message(commit_data)
        success = send_telegram_message(message)
        
        if success:
            print("📱 Уведомление отправлено в Telegram")
        else:
            print("⚠️ Не удалось отправить уведомление в Telegram")
            
        return commit_data
        
    except Exception as e:
        error_message = f"❌ <b>Ошибка в Git Auto-Commit</b>\n\n"
        error_message += f"<b>Ошибка:</b> {str(e)}\n"
        error_message += f"<b>Время:</b> {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        send_telegram_message(error_message)
        raise e

if __name__ == "__main__":
    main()