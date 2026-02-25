import sqlite3
import os
from datetime import datetime


class PetDatabase:
    def __init__(self, db_path="pet_tamagotchi.db"):
        """Инициализация базы данных питомца"""
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_table()
        self.initialize_pet()

    def connect(self):
        """Подключение к базе данных"""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def create_table(self):
        """Создание основной таблицы (без истории)"""
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS PetState (
            id INTEGER PRIMARY KEY CHECK (id = 1),

            -- Основная информация
            pet_name TEXT NOT NULL DEFAULT 'Питомец',
            last_save_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            -- Статы питомца
            health INTEGER DEFAULT 100,
            hunger INTEGER DEFAULT 100,
            happiness INTEGER DEFAULT 100,
            energy INTEGER DEFAULT 100,
            cleanliness INTEGER DEFAULT 100,
            age INTEGER DEFAULT 0,
            level INTEGER DEFAULT 1,

            -- Режимы и состояния
            is_sleeping BOOLEAN DEFAULT 0,
            is_sick BOOLEAN DEFAULT 0,
            is_dead BOOLEAN DEFAULT 0,

            -- Режим "откусывания"
            bite_mode_enabled BOOLEAN DEFAULT 0,
            bite_size INTEGER DEFAULT 10,

            -- Позиции окон
            main_window_x INTEGER DEFAULT 100,
            main_window_y INTEGER DEFAULT 100,
            main_window_width INTEGER DEFAULT 300,
            main_window_height INTEGER DEFAULT 400,

            hud_window_x INTEGER DEFAULT 500,
            hud_window_y INTEGER DEFAULT 100,
            hud_window_width INTEGER DEFAULT 250,
            hud_window_height INTEGER DEFAULT 150,
            hud_visible BOOLEAN DEFAULT 1,

            -- Статистика (опционально)
            times_fed INTEGER DEFAULT 0,
            times_played INTEGER DEFAULT 0,
            times_bitten INTEGER DEFAULT 0
        )
        ''')
        self.conn.commit()
        print("✅ Таблица PetState создана или уже существует")

    def initialize_pet(self):
        """Создание записи для питомца, если её нет"""
        self.cursor.execute("SELECT COUNT(*) FROM PetState")
        count = self.cursor.fetchone()[0]

        if count == 0:
            self.cursor.execute('''
            INSERT INTO PetState (id, pet_name, last_save_date)
            VALUES (1, 'Питомец', ?)
            ''', (datetime.now(),))
            self.conn.commit()
            print("✅ Создана новая запись для питомца")

    def save_state(self, pet_data):
        """Сохранение состояния питомца"""
        query = '''
        UPDATE PetState SET
            pet_name = ?,
            health = ?,
            hunger = ?,
            happiness = ?,
            energy = ?,
            cleanliness = ?,
            age = ?,
            level = ?,
            is_sleeping = ?,
            is_sick = ?,
            is_dead = ?,
            bite_mode_enabled = ?,
            bite_size = ?,
            main_window_x = ?,
            main_window_y = ?,
            main_window_width = ?,
            main_window_height = ?,
            hud_window_x = ?,
            hud_window_y = ?,
            hud_window_width = ?,
            hud_window_height = ?,
            hud_visible = ?,
            times_fed = ?,
            times_played = ?,
            times_bitten = ?,
            last_save_date = ?
        WHERE id = 1
        '''

        values = (
            pet_data.get('pet_name', 'Питомец'),
            pet_data.get('health', 100),
            pet_data.get('hunger', 100),
            pet_data.get('happiness', 100),
            pet_data.get('energy', 100),
            pet_data.get('cleanliness', 100),
            pet_data.get('age', 0),
            pet_data.get('level', 1),
            pet_data.get('is_sleeping', 0),
            pet_data.get('is_sick', 0),
            pet_data.get('is_dead', 0),
            pet_data.get('bite_mode_enabled', 0),
            pet_data.get('bite_size', 10),
            pet_data.get('main_window_x', 100),
            pet_data.get('main_window_y', 100),
            pet_data.get('main_window_width', 300),
            pet_data.get('main_window_height', 400),
            pet_data.get('hud_window_x', 500),
            pet_data.get('hud_window_y', 100),
            pet_data.get('hud_window_width', 250),
            pet_data.get('hud_window_height', 150),
            pet_data.get('hud_visible', 1),
            pet_data.get('times_fed', 0),
            pet_data.get('times_played', 0),
            pet_data.get('times_bitten', 0),
            datetime.now()
        )

        self.cursor.execute(query, values)
        self.conn.commit()
        print("💾 Состояние питомца сохранено в БД")

    def load_state(self):
        """Загрузка состояния питомца"""
        self.cursor.execute("SELECT * FROM PetState WHERE id = 1")
        row = self.cursor.fetchone()

        if row:
            columns = [description[0] for description in self.cursor.description]
            pet_data = dict(zip(columns, row))
            pet_data.pop('id', None)
            print("📂 Состояние питомца загружено из БД")
            return pet_data
        else:
            print("⚠️ Нет сохраненного состояния")
            return None

    def close(self):
        """Закрытие соединения с БД"""
        if self.conn:
            self.conn.close()
            print("🔒 Соединение с БД закрыто")


# Прямое использование в основном файле:
def main():
    # Создаем объект базы данных
    db = PetDatabase("my_pet.db")

    # Загружаем сохраненное состояние
    pet_state = db.load_state()

    if pet_state:
        print(f"Имя питомца: {pet_state['pet_name']}")
        print(f"Здоровье: {pet_state['health']}")
        print(f"Голод: {pet_state['hunger']}")
        print(f"Режим откусывания: {'Вкл' if pet_state['bite_mode_enabled'] else 'Выкл'}")
    else:
        print("Новый питомец создан!")

    # Изменяем состояние
    pet_state = {
        'pet_name': 'Барсик',
        'health': 95,
        'hunger': 70,
        'happiness': 85,
        'bite_mode_enabled': 1,
        'bite_size': 15,
        'main_window_x': 200,
        'main_window_y': 200,
        'times_fed': 5
    }

    # Сохраняем изменения
    db.save_state(pet_state)

    # Закрываем соединение
    db.close()


if __name__ == "__main__":
    main()