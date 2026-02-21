# progettone pazzo sgravato
import pygame
import math

def load_spritesheet(path, frame_width, frame_height, cols, rows):
    """Ritaglia tutti i frame dallo spritesheet"""
    sheet = pygame.image.load(path).convert_alpha()
    frames = []
    for row in range(rows):
        for col in range(cols):
            frame = sheet.subsurface(pygame.Rect(
                col * frame_width,
                row * frame_height,
                frame_width,
                frame_height
            ))
            frames.append(frame)
    return frames

def main() -> None:
    
    pygame.init()
    
    # schermo e titolo del gioco <33
    screen = pygame.display.set_mode((1920, 1020))
    pygame.display.set_caption("Templar's Trial")
    
    # carica la mappa di sfondo
    background = pygame.image.load("Scene_Overview.png")
    # scala la mappa per adattarla allo schermo
    background = pygame.transform.scale(background, (1920, 1020))
    
    # carica le immagini del cavaliere per su/giù
    knight_front = pygame.image.load("knight-removebg-preview.png")
    knight_back = pygame.image.load("knight_180_degrees_nosfondo.png")
    knight_front = pygame.transform.scale(knight_front, (100, 100))
    knight_back = pygame.transform.scale(knight_back, (100, 100))

    # carica spritesheet IDLE (griglia 5x5 = 25 frame)
    sheet_idle = pygame.image.load("knight-spritesheet.png")
    w, h = sheet_idle.get_size()
    idle_frames = load_spritesheet("knight-spritesheet.png", w // 5, h // 5, 5, 5)
    idle_frames = [pygame.transform.scale(f, (100, 100)) for f in idle_frames]

    # carica spritesheet CAMMINATA LATERALE (griglia 5x5 = 25 frame)
    sheet_walk = pygame.image.load("knight-removebg-preview-spritesheet.png")
    ww, wh = sheet_walk.get_size()
    walk_frames = load_spritesheet("knight-removebg-preview-spritesheet.png", ww // 5, wh // 5, 5, 5)
    walk_frames = [pygame.transform.scale(f, (100, 100)) for f in walk_frames]

    # posizione iniziale del cavaliere (AL CENTRO DELLA MAPPA)
    knight_x = 960 - 50
    knight_y = 510 - 50
    knight_speed = 5

    # STATO ANIMAZIONE
    idle_frame_index = 0
    idle_timer = 0
    idle_speed = 6       # tick tra un frame idle e l'altro

    walk_frame_index = 0
    walk_timer = 0
    walk_speed = 4       # tick tra un frame di camminata e l'altro

    is_moving = False
    direction = "down"   # ultima direzione: down, up, left, right
    flip_left = False

    # COLLISIONI - Lista vuota per ora, le aggiungeremo dopo
    obstacles = []
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        
        # serve a gestire la X di chiusura in alto
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # salva posizione precedente (per collisioni)
        old_x = knight_x
        old_y = knight_y
        
        # movimento con i tasti freccia
        keys = pygame.key.get_pressed()
        is_moving = False  # reset ogni frame
        
        if keys[pygame.K_LEFT]:
            knight_x -= knight_speed
            direction = "left"
            flip_left = True
            is_moving = True
            
        elif keys[pygame.K_RIGHT]:
            knight_x += knight_speed
            direction = "right"
            flip_left = False
            is_moving = True
            
        elif keys[pygame.K_UP]:
            knight_y -= knight_speed
            direction = "up"
            is_moving = True
            
        elif keys[pygame.K_DOWN]:
            knight_y += knight_speed
            direction = "down"
            is_moving = True

        # aggiorna animazione idle (solo se fermo)
        if not is_moving:
            walk_frame_index = 0
            walk_timer = 0
            idle_timer += 1
            if idle_timer >= idle_speed:
                idle_timer = 0
                idle_frame_index = (idle_frame_index + 1) % len(idle_frames)
        else:
            # aggiorna animazione camminata
            idle_frame_index = 0
            idle_timer = 0
            walk_timer += 1
            if walk_timer >= walk_speed:
                walk_timer = 0
                walk_frame_index = (walk_frame_index + 1) % len(walk_frames)
        
        # crea rettangolo del cavaliere per collisioni
        knight_rect = pygame.Rect(knight_x + 30, knight_y + 40, 40, 50)
        
        # controlla collisioni con ostacoli
        for obstacle in obstacles:
            if knight_rect.colliderect(obstacle):
                knight_x = old_x
                knight_y = old_y
                break
        
        # limiti dello schermo
        knight_x = max(0, min(knight_x, 1820))
        knight_y = max(0, min(knight_y, 920))
        
        # disegna lo sfondo (la mappa)
        screen.blit(background, (0, 0))
        
        # disegna il cavaliere in base allo stato
        if not is_moving:
            # FERMO: animazione idle
            screen.blit(idle_frames[idle_frame_index], (knight_x, knight_y))

        elif direction in ("left", "right"):
            # MOVIMENTO LATERALE: spritesheet camminata con eventuale flip
            frame = pygame.transform.flip(walk_frames[walk_frame_index], flip_left, False)
            screen.blit(frame, (knight_x, knight_y))

        elif direction == "up":
            # SU: sprite statica con bob
            bob = int(math.sin(pygame.time.get_ticks() * 0.01) * 4)
            screen.blit(knight_back, (knight_x, knight_y + bob))

        elif direction == "down":
            # GIÙ: sprite statica con bob
            bob = int(math.sin(pygame.time.get_ticks() * 0.01) * 4)
            screen.blit(knight_front, (knight_x, knight_y + bob))
        
        # DEBUG: mostra la posizione del cavaliere, l'ho fatto pk può essere utile per fare le hitboxes
        font = pygame.font.Font(None, 36)
        pos_text = font.render(f"X: {int(knight_x)}, Y: {int(knight_y)}", True, (255, 255, 255))
        screen.blit(pos_text, (10, 10))
        
        # serve ad aggiornare il contenuto dello schermo
        pygame.display.flip()
        clock.tick(60)  # 60 FPS
        
    pygame.quit()

if __name__ == "__main__":
    main()