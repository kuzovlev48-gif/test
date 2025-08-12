import math
import random
from typing import List, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Color:
    r: int
    g: int
    b: int
    
    def __post_init__(self):
        # Ограничиваем значения RGB в диапазоне 0-255
        self.r = max(0, min(255, self.r))
        self.g = max(0, min(255, self.g))
        self.b = max(0, min(255, self.b))
    
    @classmethod
    def from_tuple(cls, rgb_tuple):
        return cls(rgb_tuple[0], rgb_tuple[1], rgb_tuple[2])
    
    def to_tuple(self):
        return (self.r, self.g, self.b)

# Предопределённые цвета
class Colors:
    RED = Color(255, 0, 0)
    GREEN = Color(0, 255, 0)
    BLUE = Color(0, 0, 255)
    YELLOW = Color(255, 255, 0)
    MAGENTA = Color(255, 0, 255)
    CYAN = Color(0, 255, 255)
    ORANGE = Color(255, 165, 0)
    PURPLE = Color(128, 0, 128)

@dataclass
class Ball:
    x: float
    y: float
    vx: float
    vy: float
    radius: float
    color: Color
    id: int

class GameLogic:
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.balls: List[Ball] = []
        self.inventory: List[Ball] = []
        self.ball_counter = 0
        self.delete_zone = (screen_width - 100, 0, 100, 100)  # x, y, width, height
        
        # Физические параметры
        self.friction = 0.98
        self.gravity = 0.2
        self.bounce_factor = 0.8
        
    def add_ball(self, x: float, y: float, color: Optional[Color] = None) -> Ball:
        """Добавляет новый шарик в игру"""
        if color is None:
            # Выбираем случайный предопределённый цвет
            predefined_colors = [Colors.RED, Colors.GREEN, Colors.BLUE, Colors.YELLOW, 
                               Colors.MAGENTA, Colors.CYAN, Colors.ORANGE, Colors.PURPLE]
            color = random.choice(predefined_colors)
            
        ball = Ball(
            x=x,
            y=y,
            vx=random.uniform(-3, 3),
            vy=random.uniform(-3, 3),
            radius=15,
            color=color,
            id=self.ball_counter
        )
        self.ball_counter += 1
        self.balls.append(ball)
        return ball
    
    def update_ball_physics(self, ball: Ball):
        """Обновляет физику движения шарика"""
        # Применяем гравитацию
        ball.vy += self.gravity
        
        # Применяем трение
        ball.vx *= self.friction
        ball.vy *= self.friction
        
        # Обновляем позицию
        ball.x += ball.vx
        ball.y += ball.vy
        
        # Обработка столкновений со стенами
        if ball.x - ball.radius <= 0:
            ball.x = ball.radius
            ball.vx = -ball.vx * self.bounce_factor
        elif ball.x + ball.radius >= self.screen_width:
            ball.x = self.screen_width - ball.radius
            ball.vx = -ball.vx * self.bounce_factor
            
        if ball.y - ball.radius <= 0:
            ball.y = ball.radius
            ball.vy = -ball.vy * self.bounce_factor
        elif ball.y + ball.radius >= self.screen_height:
            ball.y = self.screen_height - ball.radius
            ball.vy = -ball.vy * self.bounce_factor
    
    def check_ball_collision(self, ball1: Ball, ball2: Ball) -> bool:
        """Проверяет столкновение между двумя шариками"""
        distance = math.sqrt((ball1.x - ball2.x)**2 + (ball1.y - ball2.y)**2)
        return distance <= ball1.radius + ball2.radius
    
    def mix_colors(self, color1: Color, color2: Color) -> Color:
        """Смешивает два цвета по RGB-модели и возвращает результат"""
        # Математическое смешивание RGB - усреднённое значение
        mixed_r = (color1.r + color2.r) // 2
        mixed_g = (color1.g + color2.g) // 2
        mixed_b = (color1.b + color2.b) // 2
        
        # Создаём новый цвет с точными RGB значениями
        return Color(mixed_r, mixed_g, mixed_b)
    
    def handle_ball_collisions(self):
        """Обрабатывает столкновения между шариками"""
        for i in range(len(self.balls)):
            for j in range(i + 1, len(self.balls)):
                ball1 = self.balls[i]
                ball2 = self.balls[j]
                
                if self.check_ball_collision(ball1, ball2):
                    # Смешиваем цвета
                    new_color = self.mix_colors(ball1.color, ball2.color)
                    ball1.color = new_color
                    ball2.color = new_color
                    
                    # Шарики не отталкиваются, просто меняют цвет
    
    def suck_ball(self, mouse_x: float, mouse_y: float, suck_radius: float = 50) -> Optional[Ball]:
        """Всасывает ближайший шарик в инвентарь"""
        closest_ball = None
        min_distance = float('inf')
        
        for ball in self.balls:
            distance = math.sqrt((ball.x - mouse_x)**2 + (ball.y - mouse_y)**2)
            if distance <= suck_radius and distance < min_distance:
                min_distance = distance
                closest_ball = ball
        
        if closest_ball:
            self.balls.remove(closest_ball)
            self.inventory.append(closest_ball)
            return closest_ball
        
        return None
    
    def spit_ball(self, mouse_x: float, mouse_y: float) -> Optional[Ball]:
        """Выплёвывает шарик из инвентаря обратно в игру"""
        if self.inventory:
            ball = self.inventory.pop()
            ball.x = mouse_x
            ball.y = mouse_y
            ball.vx = random.uniform(-5, 5)
            ball.vy = random.uniform(-5, 5)
            self.balls.append(ball)
            return ball
        
        return None
    
    def is_in_delete_zone(self, x: float, y: float) -> bool:
        """Проверяет, находится ли точка в зоне удаления"""
        dx, dy, dw, dh = self.delete_zone
        return dx <= x <= dx + dw and dy <= y <= dy + dh
    
    def delete_ball_from_inventory(self, mouse_x: float, mouse_y: float) -> bool:
        """Удаляет шарик из инвентаря, если мышь в зоне удаления"""
        if self.is_in_delete_zone(mouse_x, mouse_y) and self.inventory:
            self.inventory.pop()
            return True
        return False
    
    def update(self):
        """Основной метод обновления игровой логики"""
        # Обновляем физику всех шариков
        for ball in self.balls:
            self.update_ball_physics(ball)
        
        # Обрабатываем столкновения
        self.handle_ball_collisions()
    
    def get_balls(self) -> List[Ball]:
        """Возвращает список всех шариков в игре"""
        return self.balls.copy()
    
    def get_inventory(self) -> List[Ball]:
        """Возвращает список шариков в инвентаре"""
        return self.inventory.copy()
    
    def get_delete_zone(self) -> Tuple[float, float, float, float]:
        """Возвращает координаты зоны удаления"""
        return self.delete_zone
    
    def clear_all(self):
        """Очищает все шарики и инвентарь"""
        self.balls.clear()
        self.inventory.clear()
        self.ball_counter = 0

# Пример использования
if __name__ == "__main__":
    # Создаём игровую логику
    game = GameLogic(800, 600)
    
    # Добавляем несколько шариков
    game.add_ball(100, 100, Colors.RED)
    game.add_ball(200, 150, Colors.BLUE)
    game.add_ball(300, 200, Colors.GREEN)
    
    # Демонстрация смешивания цветов
    print("Игровая логика создана!")
    print(f"Шариков в игре: {len(game.get_balls())}")
    print(f"Шариков в инвентаре: {len(game.get_inventory())}")
    
    # Тест смешивания цветов
    red = Colors.RED
    blue = Colors.BLUE
    mixed = game.mix_colors(red, blue)
    print(f"Смешивание красного {red.to_tuple()} и синего {blue.to_tuple()}")
    print(f"Результат: {mixed.to_tuple()} (фиолетовый)")
