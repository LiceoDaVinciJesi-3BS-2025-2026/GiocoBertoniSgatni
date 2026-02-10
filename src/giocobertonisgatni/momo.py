import pygame
import random

pygame.init()

# Setup finestra
WIDTH, HEIGHT = 1920, 1020
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Il Mio Gioco")
clock = pygame.time.Clock()

# Player
player_x = WIDTH // 2
player_y = HEIGHT - 100
player_speed = 5
player_size = 50

# Lista nemici che inseguono
enemies = []
num_enemies = 3

# Crea nemici iniziali
for i in range(num_enemies):
    enemy = {
        'x': random.randint(0, WIDTH - 50),
        'y': random.randint(0, HEIGHT // 2),
        'size': 50,
        'speed': 2  # Più lenti del player per renderlo giocabile!
    }
    enemies.append(enemy)

# Punteggio e vite
score = 0
lives = 3

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Movimento player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
        player_x += player_speed
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= player_speed
    if keys[pygame.K_DOWN] and player_y < HEIGHT - player_size:
        player_y += player_speed
    
    # Movimento e collisione nemici
    for enemy in enemies:
        # Inseguimento: muovi verso il player
        if enemy['x'] < player_x:
            enemy['x'] += enemy['speed']
        elif enemy['x'] > player_x:
            enemy['x'] -= enemy['speed']
        
        if enemy['y'] < player_y:
            enemy['y'] += enemy['speed']
        elif enemy['y'] > player_y:
            enemy['y'] -= enemy['speed']
        
        # Collisione con questo nemico
        if (player_x < enemy['x'] + enemy['size'] and
            player_x + player_size > enemy['x'] and
            player_y < enemy['y'] + enemy['size'] and
            player_y + player_size > enemy['y']):
            lives -= 1
            # Respawn nemico lontano
            enemy['x'] = random.randint(0, WIDTH - 50)
            enemy['y'] = random.randint(0, HEIGHT // 3)
            if lives <= 0:
                print("GAME OVER! Score finale:", score)
                running = False
    
    # Punteggio aumenta col tempo
    score += 1
    
    # Aumenta difficoltà: aggiungi nemico ogni 500 punti
    if score % 500 == 0 and score > 0:
        new_enemy = {
            'x': random.randint(0, WIDTH - 50),
            'y': 0,
            'size': 50,
            'speed': 2
        }
        enemies.append(new_enemy)
    
    # Disegna tutto
    screen.fill((0, 0, 0))
    
    # Disegna player (verde)
    pygame.draw.rect(screen, (0, 255, 0), (player_x, player_y, player_size, player_size))
    
    # Disegna tutti i nemici (rossi)
    for enemy in enemies:
        pygame.draw.rect(screen, (255, 0, 0), (enemy['x'], enemy['y'], enemy['size'], enemy['size']))
    
    # Mostra punteggio e vite
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}  Vite: {lives}  Nemici: {len(enemies)}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()