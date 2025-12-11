class Stats:
    def __init__(self):
        # Ініціалізація атрибутів з діаграми класів
        self.current_gold = 0
        self.creep_score = 0
        self.gametime = 0.0

    # Метод для оновлення стану об'єкта
    def update_stats(self, gold, cs, time):
        self.current_gold = gold
        self.creep_score = cs
        self.gametime = time

    def calculate_gpm(self):
        # Використовує внутрішній стан об'єкта (self.gametime)
        if self.gametime <= 0:
            return 0.0
        return self.current_gold / (self.gametime / 60)

    def calculate_cspm(self):
        # Використовує внутрішній стан об'єкта
        if self.gametime <= 0:
            return 0.0
        return self.creep_score / (self.gametime / 60)