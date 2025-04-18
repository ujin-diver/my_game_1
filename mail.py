import pygame
import random
import time
import json
import os

# Инициализация
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Игра на выживание")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 30)

# Цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 100, 255)
GREEN = (0, 200, 0)
BLACK = (0, 0, 0)

# Игрок
player_radius = 20
player_color = BLUE

# Враги
enemy_radius = 15
enemy_color = RED
enemy_speed = 3
enemy_spawn_time = 1000  # мс

# Звуки
hit_sound = None
score_sound = None
try:
    hit_sound = pygame.mixer.Sound("hit.wav")
except:
    print("⚠️ Не найден файл hit.wav")

try:
    score_sound = pygame.mixer.Sound("score.wav")
except:
    print("⚠️ Не найден файл score.wav")

# Таблица рекордов
score_file = "highscores.json"
high_scores = []

if os.path.exists(score_file):
    with open(score_file, "r") as f:
        try:
            high_scores = json.load(f)
        except:
            high_scores = []

def save_score(score):
    high_scores.append(score)
    high_scores.sort(reverse=True)
    high_scores[:] = high_scores[:5]  # максимум 5 лучших
    with open(score_file, "w") as f:
        json.dump(high_scores, f)

def draw_text(text, size, color, x, y, center=True):
    font_obj = pygame.font.SysFont("arial", size)
    text_surf = font_obj.render(text, True, color)
    text_rect = text_surf.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    screen.blit(text_surf, text_rect)

def show_menu():
    screen.fill(BLACK)
    draw_text("ИГРА НА ВЫЖИВАНИЕ", 48, WHITE, WIDTH // 2, HEIGHT // 3)
    draw_text("Нажмите ЛКМ, чтобы начать", 30, WHITE, WIDTH // 2, HEIGHT // 2)
    draw_text("Рекорды:", 28, GREEN, WIDTH // 2, HEIGHT // 2 + 60)
    for i, score in enumerate(high_scores):
        draw_text(f"{i+1}. {score:.2f} сек", 24, WHITE, WIDTH // 2, HEIGHT // 2 + 100 + i*30)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

def main_game():
    player_pos = list(pygame.mouse.get_pos())
    enemies = []
    pygame.time.set_timer(pygame.USEREVENT, enemy_spawn_time)

    start_time = time.time()
    running = True

    while running:
        clock.tick(60)
        screen.fill(BLACK)
        player_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.USEREVENT:
                x = random.randint(0, WIDTH)
                y = random.randint(0, HEIGHT)
                enemies.append([x, y])

        for enemy in enemies:
            dx = player_pos[0] - enemy[0]
            dy = player_pos[1] - enemy[1]
            dist = max((dx ** 2 + dy ** 2) ** 0.5, 1)
            enemy[0] += dx / dist * enemy_speed
            enemy[1] += dy / dist * enemy_speed

        for enemy in enemies:
            distance = ((enemy[0] - player_pos[0]) ** 2 + (enemy[1] - player_pos[1]) ** 2) ** 0.5
            if distance < player_radius + enemy_radius:
                if hit_sound:
                    hit_sound.play()
                running = False

        for enemy in enemies:
            pygame.draw.circle(screen, enemy_color, (int(enemy[0]), int(enemy[1])), enemy_radius)

        pygame.draw.circle(screen, player_color, player_pos, player_radius)

        elapsed = time.time() - start_time
        draw_text(f"Время: {elapsed:.2f}", 24, WHITE, 10, 10, center=False)
        pygame.display.flip()

    if score_sound:
        score_sound.play()
    save_score(elapsed)
    show_menu()

if __name__ == "__main__":
    show_menu()
    while True:
        main_game()
