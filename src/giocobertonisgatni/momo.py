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

def start_screen(screen):
    """Schermata di avvio del gioco"""
    
    background = pygame.image.load("Scene_Overview.png")
    background = pygame.transform.scale(background, (1920, 1020))
    
    overlay = pygame.Surface((1920, 1020))
    overlay.set_alpha(150)
    overlay.fill((0, 0, 0))
    
    title_font = pygame.font.Font(None, 120)
    subtitle_font = pygame.font.Font(None, 60)
    button_font = pygame.font.Font(None, 50)
    
    button_rect = pygame.Rect(760, 500, 400, 100)
    title_bob = 0
    
    clock = pygame.time.Clock()
    waiting = True
    
    while waiting:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    waiting = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    waiting = False
        
        title_bob = math.sin(pygame.time.get_ticks() * 0.003) * 10
        
        screen.blit(background, (0, 0))
        screen.blit(overlay, (0, 0))
        
        title_text = title_font.render("TEMPLAR'S TRIAL", True, (255, 215, 0))
        title_rect = title_text.get_rect(center=(960, 300 + title_bob))
        screen.blit(title_text, title_rect)
        
        subtitle_text = subtitle_font.render("La Prova del Templare", True, (200, 200, 200))
        subtitle_rect = subtitle_text.get_rect(center=(960, 400))
        screen.blit(subtitle_text, subtitle_rect)
        
        mouse_pos = pygame.mouse.get_pos()
        if button_rect.collidepoint(mouse_pos):
            button_color = (255, 215, 0)
            text_color = (0, 0, 0)
        else:
            button_color = (100, 100, 100)
            text_color = (255, 255, 255)
        
        pygame.draw.rect(screen, button_color, button_rect, border_radius=15)
        pygame.draw.rect(screen, (255, 215, 0), button_rect, 3, border_radius=15)
        
        play_text = button_font.render("GIOCA", True, text_color)
        play_rect = play_text.get_rect(center=button_rect.center)
        screen.blit(play_text, play_rect)
        
        instruction_text = subtitle_font.render("Premi SPAZIO o clicca GIOCA per iniziare", True, (150, 150, 150))
        instruction_rect = instruction_text.get_rect(center=(960, 700))
        screen.blit(instruction_text, instruction_rect)
        
        credits_font = pygame.font.Font(None, 30)
        credits_text = credits_font.render("Usa le FRECCE per muoverti", True, (120, 120, 120))
        credits_rect = credits_text.get_rect(center=(960, 900))
        screen.blit(credits_text, credits_rect)
        
        pygame.display.flip()
        clock.tick(60)

def level_selection_screen(screen):
    """Schermata di selezione livelli - ritorna il numero del livello scelto (1, 2, o 3)"""
    
    forest_map = pygame.image.load("foresta_livello_1.jpg")
    village_map = pygame.image.load("villaggio_livello_2.jpg")
    castle_map = pygame.image.load("castello_livello_3.jpg")
    
    preview_size = (500, 350)
    forest_preview = pygame.transform.scale(forest_map, preview_size)
    village_preview = pygame.transform.scale(village_map, preview_size)
    castle_preview = pygame.transform.scale(castle_map, preview_size)
    
    level1_rect = pygame.Rect(100, 250, 500, 500)
    level2_rect = pygame.Rect(710, 250, 500, 500)
    level3_rect = pygame.Rect(1320, 250, 500, 500)
    
    title_font = pygame.font.Font(None, 100)
    level_font = pygame.font.Font(None, 60)
    desc_font = pygame.font.Font(None, 35)
    
    clock = pygame.time.Clock()
    selecting = True
    
    while selecting:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if level1_rect.collidepoint(mouse_pos):
                    return 1
                elif level2_rect.collidepoint(mouse_pos):
                    return 2
                elif level3_rect.collidepoint(mouse_pos):
                    return 3
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 1
                elif event.key == pygame.K_2:
                    return 2
                elif event.key == pygame.K_3:
                    return 3
        
        mouse_pos = pygame.mouse.get_pos()
        
        screen.fill((20, 20, 30))
        
        title_text = title_font.render("SELEZIONA IL LIVELLO", True, (255, 215, 0))
        title_rect = title_text.get_rect(center=(960, 120))
        screen.blit(title_text, title_rect)
        
        # LIVELLO 1
        hover1 = level1_rect.collidepoint(mouse_pos)
        border_color1 = (255, 215, 0) if hover1 else (100, 100, 100)
        border_width1 = 5 if hover1 else 3
        
        pygame.draw.rect(screen, (40, 40, 50), level1_rect, border_radius=10)
        pygame.draw.rect(screen, border_color1, level1_rect, border_width1, border_radius=10)
        screen.blit(forest_preview, (level1_rect.x, level1_rect.y))
        
        level1_title = level_font.render("LIVELLO 1", True, (100, 255, 100))
        level1_name = desc_font.render("Foresta Oscura", True, (200, 200, 200))
        level1_diff = desc_font.render("Difficoltà: Facile", True, (150, 150, 150))
        
        screen.blit(level1_title, (level1_rect.centerx - level1_title.get_width()//2, level1_rect.y + 370))
        screen.blit(level1_name, (level1_rect.centerx - level1_name.get_width()//2, level1_rect.y + 430))
        screen.blit(level1_diff, (level1_rect.centerx - level1_diff.get_width()//2, level1_rect.y + 465))
        
        # LIVELLO 2
        hover2 = level2_rect.collidepoint(mouse_pos)
        border_color2 = (255, 215, 0) if hover2 else (100, 100, 100)
        border_width2 = 5 if hover2 else 3
        
        pygame.draw.rect(screen, (40, 40, 50), level2_rect, border_radius=10)
        pygame.draw.rect(screen, border_color2, level2_rect, border_width2, border_radius=10)
        screen.blit(village_preview, (level2_rect.x, level2_rect.y))
        
        level2_title = level_font.render("LIVELLO 2", True, (255, 200, 100))
        level2_name = desc_font.render("Villaggio Assediato", True, (200, 200, 200))
        level2_diff = desc_font.render("Difficoltà: Medio", True, (150, 150, 150))
        
        screen.blit(level2_title, (level2_rect.centerx - level2_title.get_width()//2, level2_rect.y + 370))
        screen.blit(level2_name, (level2_rect.centerx - level2_name.get_width()//2, level2_rect.y + 430))
        screen.blit(level2_diff, (level2_rect.centerx - level2_diff.get_width()//2, level2_rect.y + 465))
        
        # LIVELLO 3
        hover3 = level3_rect.collidepoint(mouse_pos)
        border_color3 = (255, 215, 0) if hover3 else (100, 100, 100)
        border_width3 = 5 if hover3 else 3
        
        pygame.draw.rect(screen, (40, 40, 50), level3_rect, border_radius=10)
        pygame.draw.rect(screen, border_color3, level3_rect, border_width3, border_radius=10)
        screen.blit(castle_preview, (level3_rect.x, level3_rect.y))
        
        level3_title = level_font.render("LIVELLO 3", True, (255, 100, 100))
        level3_name = desc_font.render("Castello del Re", True, (200, 200, 200))
        level3_diff = desc_font.render("Difficoltà: Difficile", True, (150, 150, 150))
        
        screen.blit(level3_title, (level3_rect.centerx - level3_title.get_width()//2, level3_rect.y + 370))
        screen.blit(level3_name, (level3_rect.centerx - level3_name.get_width()//2, level3_rect.y + 430))
        screen.blit(level3_diff, (level3_rect.centerx - level3_diff.get_width()//2, level3_rect.y + 465))
        
        instruction_font = pygame.font.Font(None, 40)
        instruction = instruction_font.render("Clicca su un livello o premi 1, 2, 3", True, (150, 150, 150))
        screen.blit(instruction, (960 - instruction.get_width()//2, 850))
        
        pygame.display.flip()
        clock.tick(60)

def game_loop(screen, level_number):
    """Loop di gioco principale - riceve il numero del livello"""
    
    # Carica la mappa corretta in base al livello scelto
    if level_number == 1:
        background = pygame.image.load("foresta_livello_1.jpg")
    elif level_number == 2:
        background = pygame.image.load("villaggio_livello_2.jpg")
    else:  # level_number == 3
        background = pygame.image.load("castello_livello_3.jpg")
    
    background = pygame.transform.scale(background, (1920, 1020))
    
    knight_front = pygame.image.load("knight-removebg-preview.png")
    knight_back = pygame.image.load("knight_180_degrees_nosfondo.png")
    knight_front = pygame.transform.scale(knight_front, (100, 100))
    knight_back = pygame.transform.scale(knight_back, (100, 100))

    sheet_idle = pygame.image.load("knight-spritesheet.png")
    w, h = sheet_idle.get_size()
    idle_frames = load_spritesheet("knight-spritesheet.png", w // 5, h // 5, 5, 5)
    idle_frames = [pygame.transform.scale(f, (100, 100)) for f in idle_frames]

    sheet_walk = pygame.image.load("knight-removebg-preview-spritesheet.png")
    ww, wh = sheet_walk.get_size()
    walk_frames = load_spritesheet("knight-removebg-preview-spritesheet.png", ww // 5, wh // 5, 5, 5)
    walk_frames = [pygame.transform.scale(f, (100, 100)) for f in walk_frames]

    knight_x = 960 - 50
    knight_y = 510 - 50
    knight_speed = 5

    idle_frame_index = 0
    idle_timer = 0
    idle_speed = 6

    walk_frame_index = 0
    walk_timer = 0
    walk_speed = 4

    is_moving = False
    direction = "down"
    flip_left = False

    # HITBOX PER OGNI LIVELLO
    if level_number == 1:
        # LIVELLO 1 - FORESTA OSCURA
        obstacles = [
            pygame.Rect(564, -22, 465, 287),
            pygame.Rect(1, 1, 563, 506),
            pygame.Rect(561, 262, 60, 234),
            pygame.Rect(619, 263, 106, 79),
            pygame.Rect(790, 264, 78, 77),
            pygame.Rect(0, 607, 619, 442),
            pygame.Rect(620, 736, 42, 91),
            pygame.Rect(666, 769, 351, 60),
            pygame.Rect(617, 829, 400, 216),
            pygame.Rect(1172, 774, 393, 275),
            pygame.Rect(1497, 611, 422, 160),
            pygame.Rect(1565, 772, 354, 274),
            pygame.Rect(1489, 226, 430, 273),
            pygame.Rect(1414, 258, 75, 76),
            pygame.Rect(1159, -30, 319, 285),
            pygame.Rect(1475, -18, 444, 242)
        ]
    
    elif level_number == 2:
        # LIVELLO 2 - VILLAGGIO ASSEDIATO
        obstacles = [
            pygame.Rect(0, -7, 558, 541),
            pygame.Rect(553, -11, 488, 262),
            pygame.Rect(1042, -22, 238, 142),
            pygame.Rect(1039, -30, 880, 277),
            pygame.Rect(1525, 246, 394, 290),
            pygame.Rect(0, 534, 199, 515),
            pygame.Rect(193, 623, 357, 426),
            pygame.Rect(549, 888, 491, 161),
            pygame.Rect(1144, 891, 775, 158),
            pygame.Rect(1537, 613, 382, 273),
            pygame.Rect(1817, 531, 102, 83),
            pygame.Rect(1015, 466, 138, 170)
        ]
    
    else:  # level_number == 3
        # LIVELLO 3 - CASTELLO DEL RE
        obstacles = [
            pygame.Rect(772, 792, 178, 257),
            pygame.Rect(1223, 790, 175, 259),
            pygame.Rect(1397, 877, 434, 172),
            pygame.Rect(1744, 675, 175, 198),
            pygame.Rect(1773, -30, 146, 704),
            pygame.Rect(1225, -30, 546, 337),
            pygame.Rect(0, -30, 1222, 318),
            pygame.Rect(0, 286, 275, 272),
            pygame.Rect(0, 557, 261, 492),
            pygame.Rect(260, 879, 577, 170),
            pygame.Rect(301, 390, 50, 162),
            pygame.Rect(446, 337, 17, 76),
            pygame.Rect(582, 348, 12, 62),
            pygame.Rect(891, 342, 56, 164),
            pygame.Rect(754, 285, 195, 61),
            pygame.Rect(1227, 305, 184, 46),
            pygame.Rect(1226, 349, 59, 157),
            pygame.Rect(1693, 389, 77, 168),
            pygame.Rect(1705, 741, 15, 67),
            pygame.Rect(1575, 801, 14, 74),
            pygame.Rect(1571, 354, 20, 54),
            pygame.Rect(447, 812, 17, 60),
            pygame.Rect(316, 750, 18, 59),
            pygame.Rect(1045, 285, 86, 60)
        ]
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True
        
        old_x = knight_x
        old_y = knight_y
        
        keys = pygame.key.get_pressed()
        is_moving = False
        
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

        if not is_moving:
            walk_frame_index = 0
            walk_timer = 0
            idle_timer += 1
            if idle_timer >= idle_speed:
                idle_timer = 0
                idle_frame_index = (idle_frame_index + 1) % len(idle_frames)
        else:
            idle_frame_index = 0
            idle_timer = 0
            walk_timer += 1
            if walk_timer >= walk_speed:
                walk_timer = 0
                walk_frame_index = (walk_frame_index + 1) % len(walk_frames)
        
        knight_rect = pygame.Rect(knight_x + 30, knight_y + 40, 40, 50)
        
        for obstacle in obstacles:
            if knight_rect.colliderect(obstacle):
                knight_x = old_x
                knight_y = old_y
                break
        
        knight_x = max(0, min(knight_x, 1820))
        knight_y = max(0, min(knight_y, 920))
        
        screen.blit(background, (0, 0))
        
        if not is_moving:
            screen.blit(idle_frames[idle_frame_index], (knight_x, knight_y))

        elif direction in ("left", "right"):
            frame = pygame.transform.flip(walk_frames[walk_frame_index], flip_left, False)
            screen.blit(frame, (knight_x, knight_y))

        elif direction == "up":
            bob = int(math.sin(pygame.time.get_ticks() * 0.01) * 4)
            screen.blit(knight_back, (knight_x, knight_y + bob))

        elif direction == "down":
            bob = int(math.sin(pygame.time.get_ticks() * 0.01) * 4)
            screen.blit(knight_front, (knight_x, knight_y + bob))
        
        font = pygame.font.Font(None, 36)
        level_text = font.render(f"LIVELLO {level_number} | ESC = Menu", True, (255, 255, 255))
        screen.blit(level_text, (10, 10))
        
        pygame.display.flip()
        clock.tick(60)
    
    return False

def main() -> None:
    
    pygame.init()
    screen = pygame.display.set_mode((1920, 1020))
    pygame.display.set_caption("Templar's Trial")
    
    start_screen(screen)
    
    game_running = True
    while game_running:
        selected_level = level_selection_screen(screen)
        continue_playing = game_loop(screen, selected_level)
        if not continue_playing:
            game_running = False
    
    pygame.quit()

if __name__ == "__main__":
    main()