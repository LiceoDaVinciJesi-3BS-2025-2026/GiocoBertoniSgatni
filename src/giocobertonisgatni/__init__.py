# progettone pazzo sgravato
import pygame

def main() -> None:
    
    pygame.init()
    
    # schermo e titolo del gioco <33
    screen = pygame.display.set_mode((1920, 1020))
    pygame.display.set_caption("Templar's Trial")
    
    # carica la mappa di sfondo
    background = pygame.image.load("Scene_Overview.png")
    # scala la mappa per adattarla allo schermo
    background = pygame.transform.scale(background, (1920, 1020))
    
    # carica le immagini del cavaliere
    knight_front = pygame.image.load("knight-removebg-preview.png")
    knight_side = pygame.image.load("knight_90_nosfondo.png")
    knight_back = pygame.image.load("knight_180_degrees_nosfondo.png")
    
    # scala le immagini
    knight_front = pygame.transform.scale(knight_front, (100, 100))
    knight_side = pygame.transform.scale(knight_side, (100, 100))
    knight_back = pygame.transform.scale(knight_back, (100, 100))
    
    # immagine corrente del cavaliere
    current_knight = knight_front
    
    # posizione iniziale del cavaliere (AL CENTRO DELLA MAPPA)
    knight_x = 960 - 50  # centro schermo
    knight_y = 510 - 50
    knight_speed = 5
    
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
        
        if keys[pygame.K_LEFT]:
            knight_x -= knight_speed
            current_knight = pygame.transform.flip(knight_side, True, False)
            
        elif keys[pygame.K_RIGHT]:
            knight_x += knight_speed
            current_knight = knight_side
            
        elif keys[pygame.K_UP]:
            knight_y -= knight_speed
            current_knight = knight_back
            
        elif keys[pygame.K_DOWN]:
            knight_y += knight_speed
            current_knight = knight_front
        
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
        
        # disegna il cavaliere
        screen.blit(current_knight, (knight_x, knight_y))
        
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