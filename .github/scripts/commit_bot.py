#!/usr/bin/env python3
import json
import datetime
import random
import os

def generate_commit_data():
    """Генерирует данные для коммита и возвращает статистику"""
    activities = [
        "Рефакторинг кода", "Обновление документации", "Исправление опечаток",
        "Оптимизация производительности", "Добавление комментариев", "Обновление зависимостей"
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
        "weekday": current_time.strftime("%A")
    }
    
    data["commits"].append(new_commit)
    total_commits = len(data["commits"])
    
    # Статистика за неделю
    week_ago = current_time - datetime.timedelta(days=7)
    weekly_commits = len([
        c for c in data["commits"] 
        if datetime.datetime.fromisoformat(c["timestamp"]).date() >= week_ago.date()
    ])
    
    # Обновляем статистику
    data["statistics"] = {
        "total_commits": total_commits,
        "last_updated": current_time.isoformat(),
        "this_week_commits": weekly_commits
    }
    
    # Сохраняем файл
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Файл обновлен! Всего коммитов: {total_commits}")
    
    return {
        "total_commits": total_commits,
        "weekly_commits": weekly_commits,
        "new_commit": new_commit
    }

def main():
    try:
        commit_data = generate_commit_data()
        
        # Сохраняем статистику для использования в workflow
        print(f"::set-output name=total_commits::{commit_data['total_commits']}")
        print(f"::set-output name=weekly_commits::{commit_data['weekly_commits']}")
        print(f"::set-output name=activity::{commit_data['new_commit']['activity']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

if __name__ == "__main__":
    main()