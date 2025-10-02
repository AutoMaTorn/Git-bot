#!/usr/bin/env python3
import json
import datetime
import random
import os
import sys

def generate_commit_data():
    """Генерирует данные для коммита"""
    activities = [
        "Рефакторинг кода",
        "Обновление документации", 
        "Исправление опечаток",
        "Оптимизация производительности",
        "Добавление комментариев"
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
    
    # Обновляем статистику
    data["statistics"] = {
        "total_commits": total_commits,
        "last_updated": current_time.isoformat()
    }
    
    # Сохраняем файл
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Файл обновлен! Всего коммитов: {total_commits}")
    
    return True

def main():
    try:
        # Генерируем данные коммита
        success = generate_commit_data()
        
        if success:
            print("✅ Коммит данные созданы успешно")
            return True
        else:
            print("❌ Ошибка создания коммита данных")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

if __name__ == "__main__":
    main()