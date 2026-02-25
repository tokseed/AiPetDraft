import json
import os
from datetime import datetime


class Pet:
    def __init__(self, name="Призрак"):
        self.name = name
        self.hunger = 100
        self.energy = 100
        self.mood = 100
        self.state = "idle"
        self.bite_mode = False
        self.bite_count = 0
        self.load_state()

    def feed(self):
        self.hunger = min(100, self.hunger + 30)
        self.state = "eating"
        if self.bite_mode:
            self.bite_count += 1
        return f"🍖 {self.name} откусил кусок экрана!"

    def play(self):
        if self.energy < 10:
            return f"😴 {self.name} слишком устал"
        self.mood = min(100, self.mood + 25)
        self.energy = max(0, self.energy - 15)
        self.state = "playing"
        return f"🎾 {self.name} поиграл!"

    def sleep(self):
        self.energy = min(100, self.energy + 40)
        self.hunger = max(0, self.hunger - 10)
        self.state = "sleeping"
        return f"😴 {self.name} поспал!"

    def tick(self):
        self.hunger = max(0, self.hunger - 3)
        self.energy = max(0, self.energy - 2)
        self.mood = max(0, self.mood - 1)

        if self.hunger < 20:
            self.mood = max(0, self.mood - 5)
        if self.energy < 20:
            self.mood = max(0, self.mood - 3)

        self.state = "idle"
        self.save_state()

    def get_status(self):
        return f"{self.name}\n🍖 Голод: {self.hunger}\n⚡ Энергия: {self.energy}\n😊 Настроение: {self.mood}"

    def get_emotion(self):
        if self.mood > 70:
            return "👻"
        elif self.mood > 40:
            return "👻"
        else:
            return "💀"

    def reset_bites(self):
        self.bite_count = 0
        self.save_state()

    def save_state(self):
        data = {
            "name": self.name,
            "hunger": self.hunger,
            "energy": self.energy,
            "mood": self.mood,
            "bite_mode": self.bite_mode,
            "bite_count": self.bite_count,
            "last_update": datetime.now().isoformat()
        }
        with open("pet_state.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)

    def load_state(self):
        if os.path.exists("pet_state.json"):
            try:
                with open("pet_state.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.name = data.get("name", self.name)
                    self.hunger = data.get("hunger", 100)
                    self.energy = data.get("energy", 100)
                    self.mood = data.get("mood", 100)
                    self.bite_mode = data.get("bite_mode", False)
                    self.bite_count = data.get("bite_count", 0)
            except:
                pass

