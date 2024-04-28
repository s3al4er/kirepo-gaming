import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Определение констант
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
PLAYER_SIZE = 50
ENEMY_SIZE = 30
BULLET_SIZE = 5
PLAYER_SPEED = 5
BULLET_SPEED = 7
ENEMY_SPEED = 3
ENEMY_SPAWN_RATE = 25
PLAYER_HP = 50
ENEMY_KILL_COUNT = 0
ENEMY_KILL_WIN = 100

# Создание экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Shooter")

# Загрузка изображений
player_img = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
player_img.fill(WHITE)
bullet_img = pygame.Surface((BULLET_SIZE, BULLET_SIZE))
bullet_img.fill(YELLOW)
enemy_img = pygame.Surface((ENEMY_SIZE, ENEMY_SIZE))
enemy_img.fill(RED)

# Создание игрока
player_rect = player_img.get_rect()
player_rect.centerx = SCREEN_WIDTH // 2
player_rect.bottom = SCREEN_HEIGHT - 10

# Создание списка для хранения врагов и пуль
enemies = []
bullets = []

# Функция для создания врагов
def spawn_enemy():
    enemy = enemy_img.get_rect()
    enemy.x = random.randint(0, SCREEN_WIDTH - ENEMY_SIZE)
    enemy.y = random.randint(-ENEMY_SIZE * 2, -ENEMY_SIZE)
    enemies.append(enemy)

# Функция для рисования игровых объектов
def draw():
    screen.fill((0, 0, 0))
    screen.blit(player_img, player_rect)
    for enemy in enemies:
        screen.blit(enemy_img, enemy)
    for bullet in bullets:
        pygame.draw.rect(screen, YELLOW, bullet)
    pygame.draw.rect(screen, GRAY, (0, 0, player_rect.width * (PLAYER_HP / 50), 10))

# Основной игровой цикл
clock = pygame.time.Clock()
running = True
while running:
    clock.tick(60)

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Управление игроком
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and player_rect.left > 0:
        player_rect.x -= PLAYER_SPEED
    if keys[pygame.K_d] and player_rect.right < SCREEN_WIDTH:
        player_rect.x += PLAYER_SPEED
    if keys[pygame.K_w] and player_rect.top > 0:
        player_rect.y -= PLAYER_SPEED
    if keys[pygame.K_s] and player_rect.bottom < SCREEN_HEIGHT:
        player_rect.y += PLAYER_SPEED

    # Проверка на выстрел
    mouse_buttons = pygame.mouse.get_pressed()
    if mouse_buttons[0]:  # ЛКМ
        bullet = pygame.Rect(player_rect.centerx - BULLET_SIZE // 2, player_rect.top - BULLET_SIZE, BULLET_SIZE, BULLET_SIZE)
        bullets.append(bullet)

    # Перемещение пуль
    for bullet in bullets:
        bullet.y -= BULLET_SPEED
        if bullet.y < 0:
            bullets.remove(bullet)

    # Проверка столкновений пуль с врагами
    for bullet in bullets:
        for enemy in enemies:
            if bullet.colliderect(enemy):
                bullets.remove(bullet)
                enemies.remove(enemy)
                ENEMY_KILL_COUNT += 1

    # Перемещение и создание врагов
    for enemy in enemies:
        enemy.y += ENEMY_SPEED
        if enemy.y > SCREEN_HEIGHT:
            enemies.remove(enemy)
    if random.randint(0, ENEMY_SPAWN_RATE) == 0:
        spawn_enemy()

    # Проверка столкновений врагов с игроком
    for enemy in enemies:
        if player_rect.colliderect(enemy):
            PLAYER_HP -= 3
            # enemies.remove(enemy)

    # Проверка конца игры
    if PLAYER_HP <= 0:
        running = False
        print("Вы проиграли!")
    elif ENEMY_KILL_COUNT >= ENEMY_KILL_WIN:
        running = False
        print("Вы победили!")

    # Рисование
    draw()

    # Обновление экрана
    pygame.display.flip()

# Завершение Pygame
pygame.quit()
