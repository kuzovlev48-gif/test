import pygame
import sys
from logic import GameLogic, Colors, Color
from settings import *

class BallGame:
    def __init__(self, width=WINDOW_WIDTH, height=WINDOW_HEIGHT):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Шарики: игра")
        
        # Инициализация игровой логики
        self.game_logic = GameLogic(width, height)
        
        # Настройки игры
        self.clock = pygame.time.Clock()
        self.FPS = FPS
        
        # Стартовое количество шариков
        self.start_ball_count = START_BALL_COUNT
        
        # Настройки всасывания
        self.suck_radius = SUCK_RADIUS
        self.suck_active = False
        
        # Цвета интерфейса
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (128, 128, 128)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        
        # Шрифт
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Инициализация стартовых шариков
        self.initialize_balls()
        
    def initialize_balls(self):
        """Создаёт стартовые шарики"""
        colors = [Colors.RED, Colors.GREEN, Colors.BLUE, Colors.YELLOW, 
                 Colors.MAGENTA, Colors.CYAN, Colors.ORANGE, Colors.PURPLE]
        
        for i in range(self.start_ball_count):
            x = 100 + i * 100
            y = 100 + (i % 3) * 100
            color = colors[i % len(colors)]
            self.game_logic.add_ball(x, y, color)
    
    def draw_ball(self, ball):
        """Отрисовывает шарик с градиентом и обводкой"""
        # Основной цвет шарика
        color = ball.color.to_tuple()
        
        # Создаём градиент (более светлый центр)
        center_color = tuple(min(255, c + 50) for c in color)
        
        # Рисуем основную окружность
        pygame.draw.circle(self.screen, color, (int(ball.x), int(ball.y)), int(ball.radius))
        
        # Рисуем светлый центр для эффекта объёма
        pygame.draw.circle(self.screen, center_color, (int(ball.x), int(ball.y)), int(ball.radius - 3))
        
        # Рисуем обводку
        pygame.draw.circle(self.screen, self.BLACK, (int(ball.x), int(ball.y)), int(ball.radius), 2)
        
        # Рисуем блик (маленький белый круг)
        highlight_pos = (int(ball.x - ball.radius * 0.3), int(ball.y - ball.radius * 0.3))
        pygame.draw.circle(self.screen, (255, 255, 255), highlight_pos, int(ball.radius * 0.2))
    
    def draw_suck_effect(self, mouse_pos):
        """Отрисовывает эффект всасывания"""
        if self.suck_active:
            # Рисуем круг всасывания
            pygame.draw.circle(self.screen, (255, 255, 0), mouse_pos, self.suck_radius, 3)
            
            # Рисуем пунктирную линию к ближайшему шарику
            for ball in self.game_logic.get_balls():
                distance = ((ball.x - mouse_pos[0])**2 + (ball.y - mouse_pos[1])**2)**0.5
                if distance <= self.suck_radius:
                    # Рисуем линию с пунктиром
                    points = []
                    dx = mouse_pos[0] - ball.x
                    dy = mouse_pos[1] - ball.y
                    steps = 10
                    for i in range(steps + 1):
                        if i % 2 == 0:  # Пропускаем каждый второй сегмент для пунктира
                            x = ball.x + (dx * i) // steps
                            y = ball.y + (dy * i) // steps
                            points.append((x, y))
                    
                    if len(points) > 1:
                        pygame.draw.lines(self.screen, (255, 255, 0), False, points, 2)
                    
                    # Добавляем анимацию всасывания
                    pygame.draw.circle(self.screen, (255, 255, 0), (int(ball.x), int(ball.y)), int(ball.radius + 5), 2)
            
            # Показываем стрелку к инвентарю
            inventory = self.game_logic.get_inventory()
            if inventory:
                # Рисуем стрелку от мыши к инвентарю
                arrow_start = mouse_pos
                arrow_end = (50, 30)  # Позиция инвентаря
                
                # Рисуем линию стрелки
                pygame.draw.line(self.screen, (0, 255, 0), arrow_start, arrow_end, 3)
                
                # Рисуем наконечник стрелки
                arrow_points = [
                    (arrow_end[0] - 10, arrow_end[1] - 5),
                    (arrow_end[0] - 10, arrow_end[1] + 5),
                    arrow_end
                ]
                pygame.draw.polygon(self.screen, (0, 255, 0), arrow_points)
    
    def draw_inventory(self):
        """Отрисовывает инвентарь"""
        inventory = self.game_logic.get_inventory()
        
        # Рисуем фон инвентаря
        inventory_bg = pygame.Rect(10, 10, 200, 80)
        pygame.draw.rect(self.screen, (240, 240, 240), inventory_bg)
        pygame.draw.rect(self.screen, self.BLACK, inventory_bg, 2)
        
        # Заголовок инвентаря
        text = self.font.render(f"Инвентарь: {len(inventory)}", True, self.BLACK)
        self.screen.blit(text, (20, 15))
        
        # Рисуем шарики в инвентаре
        for i, ball in enumerate(inventory):
            x = 25 + i * 35
            y = 45
            # Рисуем уменьшенные шарики с эффектами
            color = ball.color.to_tuple()
            pygame.draw.circle(self.screen, color, (x, y), 12)
            pygame.draw.circle(self.screen, self.BLACK, (x, y), 12, 2)
            
            # Добавляем номер шарика
            number_text = self.small_font.render(str(i+1), True, self.WHITE)
            text_rect = number_text.get_rect(center=(x, y))
            self.screen.blit(number_text, text_rect)
    
    def draw_delete_zone(self):
        """Отрисовывает зону удаления"""
        dx, dy, dw, dh = self.game_logic.get_delete_zone()
        
        # Рисуем зону удаления с градиентом
        pygame.draw.rect(self.screen, self.RED, (dx, dy, dw, dh))
        pygame.draw.rect(self.screen, (200, 0, 0), (dx+5, dy+5, dw-10, dh-10))
        pygame.draw.rect(self.screen, self.BLACK, (dx, dy, dw, dh), 3)
        
        # Текст "УДАЛИТЬ"
        text = self.font.render("УДАЛИТЬ", True, self.WHITE)
        text_rect = text.get_rect(center=(dx + dw//2, dy + dh//2))
        self.screen.blit(text, text_rect)
        
        # Добавляем иконку корзины
        trash_icon = "🗑️"
        icon_text = self.small_font.render(trash_icon, True, self.WHITE)
        icon_rect = icon_text.get_rect(center=(dx + dw//2, dy + dh//2 + 20))
        self.screen.blit(icon_text, icon_rect)
    
    def draw_instructions(self):
        """Отрисовывает инструкции"""
        instructions = [
            "ЛКМ - всасывать шарики",
            "ПКМ - выплёвывать шарики", 
            "Перетащи в красную зону - удалить"
        ]
        
        y_offset = self.height - 100
        for i, instruction in enumerate(instructions):
            text = self.small_font.render(instruction, True, self.BLACK)
            self.screen.blit(text, (10, y_offset + i * 25))
    
    def handle_events(self):
        """Обрабатывает события"""
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # ЛКМ - всасывание
                    self.suck_active = True
                    sucked_ball = self.game_logic.suck_ball(mouse_pos[0], mouse_pos[1], self.suck_radius)
                    if sucked_ball:
                        print(f"Всасан шарик цвета {sucked_ball.color.to_tuple()}")
                
                elif event.button == 3:  # ПКМ - выплёвывание
                    spat_ball = self.game_logic.spit_ball(mouse_pos[0], mouse_pos[1])
                    if spat_ball:
                        print(f"Выплюнут шарик цвета {spat_ball.color.to_tuple()}")
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # ЛКМ отпущена
                    self.suck_active = False
            
            elif event.type == pygame.MOUSEMOTION:
                if self.suck_active:
                    # Постоянное всасывание при движении мыши
                    self.game_logic.suck_ball(mouse_pos[0], mouse_pos[1], self.suck_radius)
                
                # Проверяем удаление из инвентаря
                if self.game_logic.is_in_delete_zone(mouse_pos[0], mouse_pos[1]):
                    if self.game_logic.delete_ball_from_inventory(mouse_pos[0], mouse_pos[1]):
                        print("Шарик удалён из инвентаря")
        
        return True
    
    def run(self):
        """Основной игровой цикл"""
        running = True
        
        while running:
            # Обработка событий
            running = self.handle_events()
            
            # Обновление игровой логики
            self.game_logic.update()
            
            # Отрисовка
            self.screen.fill(self.WHITE)  # Белый фон
            
            # Рисуем шарики
            for ball in self.game_logic.get_balls():
                self.draw_ball(ball)
            
            # Рисуем эффект всасывания
            mouse_pos = pygame.mouse.get_pos()
            self.draw_suck_effect(mouse_pos)
            
            # Рисуем интерфейс
            self.draw_inventory()
            self.draw_delete_zone()
            self.draw_instructions()
            
            # Обновление экрана
            pygame.display.flip()
            self.clock.tick(self.FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = BallGame()
    game.run()
