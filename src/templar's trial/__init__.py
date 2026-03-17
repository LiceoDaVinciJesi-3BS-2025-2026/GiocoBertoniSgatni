# libreria Standard
import random
import math

# libreria  pip
import pygame

# ==============================================================================
# FUNZIONE: carica_record
# Legge il file record.txt e restituisce i record salvati per ogni livello.
#
# Il file ha una riga per livello nel formato "livello:tempo", esempio:
#   1:23.5
#   2:None
#   3:41.0
#
# Ritorna un dizionario {1: float/None, 2: float/None, 3: float/None}
# dove None significa che quel livello non è mai stato completato.
# ==============================================================================
def carica_record():
    f = open("record.txt", "r")
    contenuto = f.read()
    f.close()
    
    righe = contenuto.splitlines()
    record = {1: None, 2: None, 3: None}
    
    for riga in righe:
        parti = riga.split(":")
        livello = int(parti[0])
        valore = parti[1]
        
        if valore == "None":
            record[livello] = None
        else:
            record[livello] = float(valore)
    
    return record


# ==============================================================================
# FUNZIONE: salva_record
# Confronta il tempo appena fatto con il record salvato per quel livello.
# Se è migliore (o se non c'era ancora nessun record) aggiorna il file.
#
# Parametri:
#   level_number → il livello appena completato (1, 2 o 3)
#   tempo        → il tempo impiegato in secondi (float)
#
# Ritorna True se è un nuovo record, False se il record precedente era migliore.
# ==============================================================================
def salva_record(level_number, tempo):
    record = carica_record()
    
    # Nessun record precedente oppure tempo migliore
    if record[level_number] is None:
        nuovo = True
    elif tempo < record[level_number]:
        nuovo = True
    else:
        nuovo = False
    
    if nuovo:
        record[level_number] = tempo
        
        f = open("record.txt", "w")
        for k, v in record.items():
            f.write(f"{k}:{v}\n")
        f.close()
    
    return nuovo
# ==============================================================================
# FUNZIONE: load_spritesheet
# Serve per ritagliare i singoli frame da uno spritesheet (una grande immagine
# che contiene tutte le pose di un'animazione disposte in una griglia).
#
# Parametri:
#   path         → percorso del file immagine
#   frame_width  → larghezza di ogni singolo frame (in pixel)
#   frame_height → altezza di ogni singolo frame (in pixel)
#   cols         → numero di colonne nella griglia
#   rows         → numero di righe nella griglia
#
# Ritorna una lista di Surface pygame, ognuna contenente un frame dell'animazione.
# L'ordine è: riga per riga, da sinistra a destra.
# ==============================================================================
def load_spritesheet(path, frame_width, frame_height, cols, rows):
    """Ritaglia tutti i frame dallo spritesheet"""
    sheet = pygame.image.load(path).convert_alpha()  # Carica con trasparenza
    frames = []
    for row in range(rows):
        for col in range(cols):
            # subsurface() estrae un rettangolo dall'immagine originale senza copiarla
            frame = sheet.subsurface(pygame.Rect(
                col * frame_width,
                row * frame_height,
                frame_width,
                frame_height
            ))
            frames.append(frame)
    return frames



# ==============================================================================
# FUNZIONE: start_screen
# Mostra la schermata iniziale del gioco con titolo, sottotitolo e bottone GIOCA.
#
# Usa un effetto "bob" sul titolo (oscillazione verticale via math.sin)
# per dare movimento alla UI.
#
# Il giocatore può avanzare cliccando il bottone oppure premendo SPAZIO/INVIO.
# La funzione blocca l'esecuzione finché l'utente non sceglie di partire.
# ==============================================================================
def start_screen(screen):
    """Schermata di avvio del gioco"""
   
    background = pygame.image.load("immagini/Scene_Overview.png")
    background = pygame.transform.scale(background, (1920, 1020))
   
    # Overlay semitrasparente nero sopra lo sfondo per far risaltare il testo
    overlay = pygame.Surface((1920, 1020))
    overlay.set_alpha(150) # 0 = invisibile, 255 = opaco
    overlay.fill((0, 0, 0))
   
    title_font = pygame.font.Font(None, 120)
    subtitle_font = pygame.font.Font(None, 60)
    button_font = pygame.font.Font(None, 50)
   
    button_rect = pygame.Rect(760, 500, 400, 100)
    title_bob = 0  # Offset verticale per l'animazione del titolo
   
    clock = pygame.time.Clock()
    waiting = True
   
    while waiting:
       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            # Click sul bottone GIOCA    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    waiting = False
            
            # Scorciatoia da tastiera per avviare
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    waiting = False
        
        # Calcola offset bobbing: oscillazione sinusoidale basata sul tempo in ms
        title_bob = math.sin(pygame.time.get_ticks() * 0.003) * 10
       
        screen.blit(background, (0, 0))
        screen.blit(overlay, (0, 0))
       
        title_text = title_font.render("TEMPLAR'S TRIAL", True, (255, 215, 0))
        title_rect = title_text.get_rect(center=(960, 300 + title_bob))
        screen.blit(title_text, title_rect)
       
        subtitle_text = subtitle_font.render("La Prova del Templare", True, (200, 200, 200))
        subtitle_rect = subtitle_text.get_rect(center=(960, 400))
        screen.blit(subtitle_text, subtitle_rect)
        
        # Hover effect: il bottone cambia colore quando ci passa il mouse sopra
        mouse_pos = pygame.mouse.get_pos()
        if button_rect.collidepoint(mouse_pos):
            button_color = (255, 215, 0)
            text_color = (0, 0, 0)
        else:
            button_color = (100, 100, 100)
            text_color = (255, 255, 255)
       
        pygame.draw.rect(screen, button_color, button_rect, border_radius=15)
        pygame.draw.rect(screen, (255, 215, 0), button_rect, 3, border_radius=15)# Bordo dorato
       
        play_text = button_font.render("GIOCA", True, text_color)
        play_rect = play_text.get_rect(center=button_rect.center)
        screen.blit(play_text, play_rect)
       
        instruction_text = subtitle_font.render("Premi SPAZIO o clicca GIOCA per iniziare", True, (150, 150, 150))
        instruction_rect = instruction_text.get_rect(center=(960, 700))
        screen.blit(instruction_text, instruction_rect)
       
        credits_font = pygame.font.Font(None, 30)
        credits_text = credits_font.render("Usa le FRECCE per muoverti | SPAZIO per attaccare", True, (120, 120, 120))
        credits_rect = credits_text.get_rect(center=(960, 900))
        screen.blit(credits_text, credits_rect)
       
        pygame.display.flip()
        clock.tick(60)

# ==============================================================================
# FUNZIONE: death_screen
# Mostra la schermata di morte quando il giocatore esaurisce le vite.
#
# Mostra un overlay rosso con fade-in animato, il titolo "SEI MORTO" pulsante,
# e due bottoni cliccabili: RIPROVA (rigioca lo stesso livello) e MENU (torna
# alla selezione livelli). Supporta anche i tasti R e ESC come scorciatoie.
#
# Parametri:
#   screen       → la Surface principale di pygame su cui disegnare
#   level_number → il livello in cui il giocatore è morto (mostrato nel testo)
#
# Ritorna 'retry' se vuole riprovare, 'menu' se torna al menu, 'quit' se chiude.
# ==============================================================================
def death_screen(screen, level_number):
    overlay = pygame.Surface((1920, 1020))
    overlay.fill((120, 0, 0))
    title_font    = pygame.font.Font(None, 180)
    subtitle_font = pygame.font.Font(None, 60)
    button_font   = pygame.font.Font(None, 55)
    retry_rect = pygame.Rect(560,  600, 350, 90)
    menu_rect  = pygame.Rect(1010, 600, 350, 90)
    clock = pygame.time.Clock()
    alpha = 0
    fade_done = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            if event.type == pygame.MOUSEBUTTONDOWN and fade_done:
                if retry_rect.collidepoint(event.pos):
                    return 'retry'
                if menu_rect.collidepoint(event.pos):
                    return 'menu'
            if event.type == pygame.KEYDOWN and fade_done:
                if event.key == pygame.K_r:
                    return 'retry'
                if event.key == pygame.K_ESCAPE:
                    return 'menu'
        if not fade_done:
            alpha = min(alpha + 3, 180)
            if alpha >= 180:
                fade_done = True
        screen.fill((15, 0, 0))
        overlay.set_alpha(alpha)
        screen.blit(overlay, (0, 0))
        pulse = math.sin(pygame.time.get_ticks() * 0.004) * 8
        shadow = title_font.render("SEI MORTO", True, (60, 0, 0))
        screen.blit(shadow, shadow.get_rect(center=(964, 304 + pulse)))
        title = title_font.render("SEI MORTO", True, (220, 30, 30))
        screen.blit(title, title.get_rect(center=(960, 300 + pulse)))
        sub = subtitle_font.render(f"Il tuo cammino termina al Livello {level_number}...", True, (180, 120, 120))
        screen.blit(sub, sub.get_rect(center=(960, 460)))
        if fade_done:
            mouse_pos = pygame.mouse.get_pos()
            rc  = (220, 180, 0) if retry_rect.collidepoint(mouse_pos) else (80, 80, 80)
            rtc = (0, 0, 0)     if retry_rect.collidepoint(mouse_pos) else (255, 255, 255)
            pygame.draw.rect(screen, rc, retry_rect, border_radius=12)
            pygame.draw.rect(screen, (220, 180, 0), retry_rect, 3, border_radius=12)
            rt = button_font.render("RIPROVA", True, rtc)
            screen.blit(rt, rt.get_rect(center=retry_rect.center))
            mc  = (220, 180, 0) if menu_rect.collidepoint(mouse_pos) else (80, 80, 80)
            mtc = (0, 0, 0)     if menu_rect.collidepoint(mouse_pos) else (255, 255, 255)
            pygame.draw.rect(screen, mc, menu_rect, border_radius=12)
            pygame.draw.rect(screen, (220, 180, 0), menu_rect, 3, border_radius=12)
            mt = button_font.render("MENU", True, mtc)
            screen.blit(mt, mt.get_rect(center=menu_rect.center))
            hint_font = pygame.font.Font(None, 35)
            hint = hint_font.render("R = Riprova  |  ESC = Menu", True, (120, 80, 80))
            screen.blit(hint, hint.get_rect(center=(960, 730)))
        pygame.display.flip()
        clock.tick(60)

# ==============================================================================
# FUNZIONE: level_selection_screen
# Mostra la schermata di selezione del livello con anteprima dei 3 livelli.
#
# L'utente può cliccare su uno dei 3 riquadri oppure premere i tasti 1, 2, 3.
# La funzione ritorna il numero del livello scelto (1, 2 o 3), che viene
# poi passato a game_loop() per caricare la mappa e gli ostacoli corretti.
# ==============================================================================
def level_selection_screen(screen):
    """Schermata di selezione livelli - ritorna il numero del livello scelto (1, 2, o 3)"""
    
    # Carica le anteprime dei 3 livelli
    forest_map = pygame.image.load("immagini/foresta_livello_1.jpg")
    village_map = pygame.image.load("immagini/villaggio_livello_2.jpg")
    castle_map = pygame.image.load("immagini/castello_livello_3.jpg")
   
    # Ridimensiona tutte le anteprime alla stessa dimensione
    preview_size = (500, 350)
    forest_preview = pygame.transform.scale(forest_map, preview_size)
    village_preview = pygame.transform.scale(village_map, preview_size)
    castle_preview = pygame.transform.scale(castle_map, preview_size)
    
    # Rettangoli cliccabili per ogni livello (più grandi delle anteprime
    # perché includono anche il testo descrittivo sotto)
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
                # Controlla su quale riquadro ha cliccato l'utente
                if level1_rect.collidepoint(mouse_pos):
                    return 1
                elif level2_rect.collidepoint(mouse_pos):
                    return 2
                elif level3_rect.collidepoint(mouse_pos):
                    return 3
            
            # Selezione rapida da tastiera
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
       
        # --- LIVELLO 1 ---
        # Il bordo diventa dorato e più spesso quando il mouse è sopra (hover effect)
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
       
        # --- LIVELLO 2 ---
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
       
        # --- LIVELLO 3 ---
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


# ==============================================================================
# FUNZIONE: game_loop
# È il cuore del gioco. Gestisce tutta la logica di gameplay per il livello scelto.
#
# Cosa fa:
#   - Carica la mappa di sfondo e tutti gli spritesheet del cavaliere e dell'ascia
#   - Gestisce il movimento del personaggio con le frecce direzionali
#   - Seleziona l'animazione giusta in base alla direzione di movimento
#   - Gestisce l'attacco con SPAZIO (con cooldown per non spammare)
#   - Controlla le collisioni con gli ostacoli (rettangoli invisibili sulla mappa)
#   - Tiene il personaggio nei limiti dello schermo
#   - Disegna tutto a ogni frame: sfondo, personaggio, ascia, HUD
#
# Parametri:
#   screen       → la Surface principale di pygame su cui disegnare
#   level_number → il livello scelto (1, 2 o 3), determina mappa e ostacoli
#
# Ritorna True se il giocatore preme ESC (torna al menu), False se chiude il gioco.
# ==============================================================================
def game_loop(screen, level_number):
    """Loop di gioco principale"""
   
    # ---- CARICAMENTO MAPPA ----
    if level_number == 1:
        background = pygame.image.load("immagini/foresta_livello_1.jpg")
    elif level_number == 2:
        background = pygame.image.load("immagini/villaggio_livello_2.jpg")
    else:
        background = pygame.image.load("immagini/castello_livello_3.jpg")
   
    background = pygame.transform.scale(background, (1920, 1020))

    # ---- CARICAMENTO SPRITE E ANIMAZIONI ----

    knight_back = pygame.image.load("personaggio/knight_180_degrees_nosfondo.png")
    knight_back = pygame.transform.scale(knight_back, (100, 100))

    sheet_idle = pygame.image.load("personaggio/knight-spritesheet.png")
    w, h = sheet_idle.get_size()
    idle_frames = load_spritesheet("personaggio/knight-spritesheet.png", w // 5, h // 5, 5, 5)
    idle_frames = [pygame.transform.scale(f, (100, 100)) for f in idle_frames]

    sheet_walk_side = pygame.image.load("personaggio/knight-removebg-preview-spritesheet.png")
    ws, hs = sheet_walk_side.get_size()
    walk_side_frames = load_spritesheet("personaggio/knight-removebg-preview-spritesheet.png", ws // 5, hs // 5, 5, 5)
    walk_side_frames = [pygame.transform.scale(f, (100, 100)) for f in walk_side_frames]

    sheet_walk_down = pygame.image.load("personaggio/knight_movingspritesheet.png")
    wd, hd = sheet_walk_down.get_size()
    walk_down_frames = load_spritesheet("personaggio/knight_movingspritesheet.png", wd // 5, hd // 5, 5, 5)
    walk_down_frames = [pygame.transform.scale(f, (100, 100)) for f in walk_down_frames]
    
    sheet_walk_up = pygame.image.load("personaggio/pisello.png")
    wu, hu = sheet_walk_up.get_size()
    walk_up_frames = load_spritesheet("personaggio/pisello.png", wu // 5, hu // 5, 5, 5)
    walk_up_frames = [pygame.transform.scale(f, (100, 100)) for f in walk_up_frames]

    sheet_axe = pygame.image.load("personaggio/ascia-spritesheet.png")
    axe_w, axe_h = sheet_axe.get_size()
    axe_frames = load_spritesheet("personaggio/ascia-spritesheet.png", axe_w // 5, axe_h // 5, 5, 5)
    axe_frames = [pygame.transform.scale(f, (60, 60)) for f in axe_frames]

    # ---- CARICAMENTO SPRITESHEET UGO (nemico) ----
    # ugo-walk-v1.png: griglia 5x5 = 25 frame di animazione walk
    # Lo sfondo nero viene rimosso con set_colorkey
    sheet_ugo = pygame.image.load("nemico/ugo-walk-v1.png")
    ugo_w, ugo_h = sheet_ugo.get_size()
    ugo_frames_raw = load_spritesheet("nemico/ugo-walk-v1.png", ugo_w // 5, ugo_h // 5, 5, 5)
    ugo_frames = []
    for f in ugo_frames_raw:
        f = pygame.transform.scale(f, (60, 60))
        f.set_colorkey((0, 0, 0))  # rimuove lo sfondo nero
        ugo_frames.append(f)

    # ---- POSIZIONE INIZIALE DEL CAVALIERE ----
    knight_x = 960 - 50
    knight_y = 510 - 50
    knight_speed = 5
    knight_lives = 3

    # ---- VARIABILI DI STATO ANIMAZIONE ----
    idle_frame_index = 0
    idle_timer = 0
    idle_speed = 6

    walk_side_frame_index = 0
    walk_side_timer = 0
    walk_side_speed = 4

    walk_down_frame_index = 0
    walk_down_timer = 0
    walk_down_speed = 4

    walk_up_frame_index = 0
    walk_up_timer = 0
    walk_up_speed = 4

    # ---- VARIABILI DI STATO ATTACCO ----
    is_attacking = False
    attack_frame_index = 0
    attack_timer = 0
    attack_speed = 2
    attack_cooldown = 0
    
    # ---- VARIABILI DI STATO MOVIMENTO ----
    is_moving = False
    direction = "down"
    flip_left = False

    # ---- SISTEMA NEMICI ----
    enemies = []
    num_enemies = {1: 5, 2: 10, 3: 18}[level_number]
    
    for i in range(num_enemies):
        enemy = {
            'x': random.randint(100, 1700),
            'y': random.randint(100, 800),
            'size': 60,               # aggiornato a 60 per corrispondere allo sprite Ugo
            'speed': 2,
            'alive': True,
            'anim_index': 0,          # frame corrente animazione Ugo
            'anim_timer': 0,          # timer per avanzare i frame
            'anim_speed': 5,          # ogni quanti tick cambia frame
            'flip': False             # True se Ugo guarda a sinistra
        }
        enemies.append(enemy)
    
    enemy_damage_cooldown = 0

    # ---- OSTACOLI PER LIVELLO ----
    if level_number == 1:
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
    else:
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
    tempo_inizio = pygame.time.get_ticks()
    running = True
    
    while running:
        # ---- GESTIONE EVENTI ----
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return False
           
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True
                if event.key == pygame.K_SPACE and not is_attacking and attack_cooldown == 0:
                    is_attacking = True
                    attack_frame_index = 0
                    attack_timer = 0
       
        # ---- COOLDOWN ----
        if attack_cooldown > 0:
            attack_cooldown -= 1
        if enemy_damage_cooldown > 0:
            enemy_damage_cooldown -= 1

        old_x = knight_x
        old_y = knight_y
       
        # ---- INPUT MOVIMENTO ----
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

        # ---- AGGIORNAMENTO ANIMAZIONE ATTACCO ----
        if is_attacking:
            attack_timer += 1
            if attack_timer >= attack_speed:
                attack_timer = 0
                attack_frame_index += 1
                if attack_frame_index >= len(axe_frames):
                    is_attacking = False
                    attack_frame_index = 0
                    attack_cooldown = 20

        # ---- AGGIORNAMENTO ANIMAZIONI MOVIMENTO/IDLE ----
        if not is_moving:
            walk_side_frame_index = 0
            walk_side_timer = 0
            walk_down_frame_index = 0
            walk_down_timer = 0
            walk_up_frame_index = 0
            walk_up_timer = 0
            idle_timer += 1
            if idle_timer >= idle_speed:
                idle_timer = 0
                idle_frame_index = (idle_frame_index + 1) % len(idle_frames)
        else:
            idle_frame_index = 0
            idle_timer = 0
            if direction in ("left", "right"):
                walk_down_frame_index = 0
                walk_down_timer = 0
                walk_up_frame_index = 0
                walk_up_timer = 0
                walk_side_timer += 1
                if walk_side_timer >= walk_side_speed:
                    walk_side_timer = 0
                    walk_side_frame_index = (walk_side_frame_index + 1) % len(walk_side_frames)
            elif direction == "down":
                walk_side_frame_index = 0
                walk_side_timer = 0
                walk_up_frame_index = 0
                walk_up_timer = 0
                walk_down_timer += 1
                if walk_down_timer >= walk_down_speed:
                    walk_down_timer = 0
                    walk_down_frame_index = (walk_down_frame_index + 1) % len(walk_down_frames)
            elif direction == "up":
                walk_side_frame_index = 0
                walk_side_timer = 0
                walk_down_frame_index = 0
                walk_down_timer = 0
                walk_up_timer += 1
                if walk_up_timer >= walk_up_speed:
                    walk_up_timer = 0
                    walk_up_frame_index = (walk_up_frame_index + 1) % len(walk_up_frames)
       
        # ---- AGGIORNAMENTO NEMICI ----
        for enemy in enemies:
            if not enemy['alive']:
                continue
            
            # Calcola direzione verso il player
            dx = knight_x - enemy['x']
            dy = knight_y - enemy['y']
            distance = math.sqrt(dx**2 + dy**2)
            
            if distance > 0:
                dx = dx / distance
                dy = dy / distance
                enemy['x'] += dx * enemy['speed']
                enemy['y'] += dy * enemy['speed']
                # Flip: Ugo guarda a sinistra se si muove a sinistra
                enemy['flip'] = dx < 0

            # Avanza animazione Ugo (sempre in movimento quando insegue)
            enemy['anim_timer'] += 1
            if enemy['anim_timer'] >= enemy['anim_speed']:
                enemy['anim_timer'] = 0
                enemy['anim_index'] = (enemy['anim_index'] + 1) % len(ugo_frames)

            # Collisione nemico con player
            enemy_rect = pygame.Rect(enemy['x'], enemy['y'], enemy['size'], enemy['size'])
            knight_rect_full = pygame.Rect(knight_x, knight_y, 100, 100)
            
            if enemy_rect.colliderect(knight_rect_full) and enemy_damage_cooldown == 0:
                knight_lives -= 1
                enemy_damage_cooldown = 60
                if knight_lives <= 0:
                    result = death_screen(screen, level_number)
                    if result == 'retry':
                        return 'retry'
                    elif result == 'quit':
                        return False
                    else:
                        return True
            
            # Collisione ascia con nemico
            if is_attacking:
                if direction == "right":
                    axe_rect = pygame.Rect(knight_x + 55, knight_y + 30, 60, 60)
                elif direction == "left":
                    axe_rect = pygame.Rect(knight_x - 15, knight_y + 30, 60, 60)
                elif direction == "up":
                    axe_rect = pygame.Rect(knight_x + 20, knight_y - 10, 60, 60)
                else:
                    axe_rect = pygame.Rect(knight_x + 20, knight_y + 50, 60, 60)
                
                if enemy_rect.colliderect(axe_rect):
                    enemy['alive'] = False
       
        # ---- COLLISIONI CON OSTACOLI ----
        knight_rect = pygame.Rect(knight_x + 30, knight_y + 40, 40, 50)
        for obstacle in obstacles:
            if knight_rect.colliderect(obstacle):
                knight_x = old_x
                knight_y = old_y
                break
       
        # ---- LIMITI DELLO SCHERMO ----
        knight_x = max(0, min(knight_x, 1820))
        knight_y = max(0, min(knight_y, 920))
       
        # ================================================================
        # RENDERING
        # ================================================================
        screen.blit(background, (0, 0))
       
        # ---- DISEGNO NEMICI (Ugo animato) ----
        for enemy in enemies:
            if enemy['alive']:
                # Prende il frame corrente dell'animazione
                ugo_frame = ugo_frames[enemy['anim_index']]
                # Flip orizzontale se Ugo si muove a sinistra
                if enemy['flip']:
                    ugo_frame = pygame.transform.flip(ugo_frame, True, False)
                screen.blit(ugo_frame, (enemy['x'], enemy['y']))
       
        # ---- DISEGNO CAVALIERE ----
        if not is_moving:
            screen.blit(idle_frames[idle_frame_index], (knight_x, knight_y))
        elif direction in ("left", "right"):
            frame = pygame.transform.flip(walk_side_frames[walk_side_frame_index], flip_left, False)
            screen.blit(frame, (knight_x, knight_y))
        elif direction == "up":
            screen.blit(walk_up_frames[walk_up_frame_index], (knight_x, knight_y))
        elif direction == "down":
            screen.blit(walk_down_frames[walk_down_frame_index], (knight_x, knight_y))
        
        # ---- DISEGNO ASCIA ----
        if is_attacking:
            if direction == "right":
                axe_x = knight_x + 55
                axe_y = knight_y + 30
                current_axe = axe_frames[attack_frame_index]
            elif direction == "left":
                axe_x = knight_x - 15
                axe_y = knight_y + 30
                current_axe = pygame.transform.flip(axe_frames[attack_frame_index], True, False)
            elif direction == "up":
                axe_x = knight_x + 20
                axe_y = knight_y - 10
                current_axe = pygame.transform.rotate(axe_frames[attack_frame_index], 90)
            else:
                axe_x = knight_x + 20
                axe_y = knight_y + 50
                current_axe = pygame.transform.rotate(axe_frames[attack_frame_index], -90)
            
            screen.blit(current_axe, (axe_x, axe_y))
       
        # ---- HUD ----
        font = pygame.font.Font(None, 36)
        lives_text = font.render(f"Vite: {'❤️ ' * knight_lives}", True, (255, 255, 255))
        screen.blit(lives_text, (10, 50))
        enemies_alive = sum(1 for e in enemies if e['alive'])
        enemies_text = font.render(f"Nemici: {enemies_alive}/{len(enemies)}", True, (255, 255, 255))
        screen.blit(enemies_text, (10, 85))
        level_text = font.render(f"LIVELLO {level_number} | ESC = Menu | SPAZIO = Attacco", True, (255, 255, 255))
        screen.blit(level_text, (10, 10))
        
        pygame.display.flip()
        clock.tick(60)
   
    return False
    # ================================================================
    # GAME LOOP PRINCIPALE
    # Viene eseguito 60 volte al secondo (clock.tick(60)).
    # Ogni iterazione: gestisce eventi -> aggiorna logica -> disegna.
    # ================================================================
    while running:
        # ---- GESTIONE EVENTI ----
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return False # Chiude il gioco completamente
           
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True # Torna al menu principale
                # Avvia attacco solo se non sta già attaccando e il cooldown è scaduto
                if event.key == pygame.K_SPACE and not is_attacking and attack_cooldown == 0:
                    is_attacking = True
                    attack_frame_index = 0
                    attack_timer = 0
       
        # ---- COOLDOWN ATTACCO ----
        # Decrementa ogni frame finché non torna a 0 (permette nuovo attacco)
        if attack_cooldown > 0:
            attack_cooldown -= 1
        
        if enemy_damage_cooldown > 0:
            enemy_damage_cooldown -= 1

        # ---- SALVATAGGIO POSIZIONE PRECEDENTE ----
        # Serve per il sistema di collisioni: se il cavaliere finisce dentro un ostacolo,
        # lo si riporta alla posizione valida del frame precedente.
        old_x = knight_x
        old_y = knight_y
       
        # ---- INPUT MOVIMENTO ----
        # get_pressed() legge tutti i tasti tenuti premuti in questo frame.
        # Solo una direzione alla volta (if/elif garantisce priorità: sinistra > destra > su > giù).
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

        # ---- AGGIORNAMENTO ANIMAZIONE ATTACCO ----
        # Avanza di un frame ogni `attack_speed` tick.
        # Quando finisce tutti i frame, termina l'attacco e avvia il cooldown.
        if is_attacking:
            attack_timer += 1
            if attack_timer >= attack_speed:
                attack_timer = 0
                attack_frame_index += 1
                if attack_frame_index >= len(axe_frames):
                    is_attacking = False
                    attack_frame_index = 0
                    attack_cooldown = 20 # ~0.33 secondi a 60 FPS prima del prossimo attacco

        # ---- AGGIORNAMENTO ANIMAZIONI MOVIMENTO/IDLE ----
        if not is_moving:
            walk_side_frame_index = 0
            walk_side_timer = 0
            walk_down_frame_index = 0
            walk_down_timer = 0
            walk_up_frame_index = 0
            walk_up_timer = 0
            # Avanza l'animazione idle
            idle_timer += 1
            if idle_timer >= idle_speed:
                idle_timer = 0
                idle_frame_index = (idle_frame_index + 1) % len(idle_frames)
        else:
            # Reset idle quando il personaggio si muove
            idle_frame_index = 0
            idle_timer = 0
            
            
            # Avanza solo l'animazione corrispondente alla direzione attuale,
            # resettando le altre per evitare che rimangano a metà ciclo
            if direction in ("left", "right"):
                walk_down_frame_index = 0
                walk_down_timer = 0
                walk_up_frame_index = 0
                walk_up_timer = 0
                walk_side_timer += 1
                if walk_side_timer >= walk_side_speed:
                    walk_side_timer = 0
                    walk_side_frame_index = (walk_side_frame_index + 1) % len(walk_side_frames)
            elif direction == "down":
                walk_side_frame_index = 0
                walk_side_timer = 0
                walk_up_frame_index = 0
                walk_up_timer = 0
                walk_down_timer += 1
                if walk_down_timer >= walk_down_speed:
                    walk_down_timer = 0
                    walk_down_frame_index = (walk_down_frame_index + 1) % len(walk_down_frames)
            elif direction == "up":
                walk_side_frame_index = 0
                walk_side_timer = 0
                walk_down_frame_index = 0
                walk_down_timer = 0
                walk_up_timer += 1
                if walk_up_timer >= walk_up_speed:
                    walk_up_timer = 0
                    walk_up_frame_index = (walk_up_frame_index + 1) % len(walk_up_frames)
       
        # Aggiorna nemici
        for enemy in enemies:
            if not enemy['alive']:
                continue
            
            # Inseguimento player
            dx = knight_x - enemy['x']
            dy = knight_y - enemy['y']
            distance = math.sqrt(dx**2 + dy**2)
            
            if distance > 0:
                dx = dx / distance
                dy = dy / distance
                enemy['x'] += dx * enemy['speed']
                enemy['y'] += dy * enemy['speed']
            
            # Collisione nemico con player
            enemy_rect = pygame.Rect(enemy['x'], enemy['y'], enemy['size'], enemy['size'])
            knight_rect_full = pygame.Rect(knight_x, knight_y, 100, 100)
            
            # ==================== Toglie 1 vita invece di danno graduale ====================
            if enemy_rect.colliderect(knight_rect_full) and enemy_damage_cooldown == 0:
                knight_lives -= 1
                enemy_damage_cooldown = 60  # invincibilità di 1 secondo
                if knight_lives <= 0:
                    print("GAME OVER!")
                    return True
            # ===========================================================================================
            
            # ==================== Nemico muore con un colpo ====================
            if is_attacking:
                if direction == "right":
                    axe_rect = pygame.Rect(knight_x + 55, knight_y + 30, 60, 60)
                elif direction == "left":
                    axe_rect = pygame.Rect(knight_x - 15, knight_y + 30, 60, 60)
                elif direction == "up":
                    axe_rect = pygame.Rect(knight_x + 20, knight_y - 10, 60, 60)
                else:
                    axe_rect = pygame.Rect(knight_x + 20, knight_y + 50, 60, 60)
                
                if enemy_rect.colliderect(axe_rect):
                    enemy['alive'] = False  # Muore subito
            # ================================================================================
       
        # ---- COLLISIONI CON OSTACOLI ----
        # La hitbox del cavaliere è più piccola dello sprite (30px da sinistra, 40px dall'alto)
        # per avere collisioni più precise e non far "bloccare" il personaggio troppo presto.
        knight_rect = pygame.Rect(knight_x + 30, knight_y + 40, 40, 50)
        for obstacle in obstacles:
            if knight_rect.colliderect(obstacle):
                # Collisione rilevata: annulla il movimento tornando alla posizione precedente
                knight_x = old_x
                knight_y = old_y
                break # Basta trovare un ostacolo, non serve controllare gli altri
       
        # ---- LIMITI DELLO SCHERMO ----
        # Impedisce al cavaliere di uscire dai bordi della finestra
        knight_x = max(0, min(knight_x, 1820))
        knight_y = max(0, min(knight_y, 920))
       
        # ================================================================
        # RENDERING (disegno a schermo)
        # L'ordine è importante: prima lo sfondo, poi il personaggio sopra.
        # ================================================================
        screen.blit(background, (0, 0))
       
        # ==================== Disegna nemici senza barra vita ====================
        for enemy in enemies:
            if enemy['alive']:
                pygame.draw.rect(screen, (255, 0, 0), (enemy['x'], enemy['y'], enemy['size'], enemy['size']))
        # ====================================================================================
       
        # Sceglie quale sprite disegnare in base allo stato corrente
        if not is_moving:
            # Fermo → idle
            screen.blit(idle_frames[idle_frame_index], (knight_x, knight_y))
        elif direction in ("left", "right"):
            # Movimento laterale → flip se va a sinistra
            frame = pygame.transform.flip(walk_side_frames[walk_side_frame_index], flip_left, False)
            screen.blit(frame, (knight_x, knight_y))
        elif direction == "up":
            screen.blit(walk_up_frames[walk_up_frame_index], (knight_x, knight_y))
        elif direction == "down":
            screen.blit(walk_down_frames[walk_down_frame_index], (knight_x, knight_y))
        
        # ---- DISEGNO ASCIA DURANTE L'ATTACCO ----
        # L'ascia viene posizionata e ruotata in modo diverso a seconda della direzione,
        # così sembra sempre coerente con la posizione del cavaliere.
        if is_attacking:
            if direction == "right":
                axe_x = knight_x + 55 # A destra del personaggio
                axe_y = knight_y + 30
                current_axe = axe_frames[attack_frame_index]
            elif direction == "left":
                axe_x = knight_x - 15 # A sinistra del personaggio
                axe_y = knight_y + 30
                current_axe = pygame.transform.flip(axe_frames[attack_frame_index], True, False)
            elif direction == "up":
                axe_x = knight_x + 20
                axe_y = knight_y - 10 # Sopra il personaggio
                current_axe = pygame.transform.rotate(axe_frames[attack_frame_index], 90)
            else: # direction == "down"
                axe_x = knight_x + 20
                axe_y = knight_y + 50 # Sotto il personaggio
                current_axe = pygame.transform.rotate(axe_frames[attack_frame_index], -90)
            
            screen.blit(current_axe, (axe_x, axe_y))
       
        # ==================== HUD con vite e nemici rimasti ====================
        font = pygame.font.Font(None, 36)
        
        # Vite (cuori o icone)
        lives_text = font.render(f"Vite: {'❤️ ' * knight_lives}", True, (255, 255, 255))
        screen.blit(lives_text, (10, 50))
        
        # Nemici rimasti
        enemies_alive = sum(1 for e in enemies if e['alive'])
        enemies_text = font.render(f"Nemici: {enemies_alive}/{len(enemies)}", True, (255, 255, 255))
        screen.blit(enemies_text, (10, 85))
        
        #questa parte serve per far funzionare le prime due funzioni ma non va molto bene.... 
        if enemies_alive == 0:
            tempo_finale = round((pygame.time.get_ticks() - tempo_inizio) / 1000, 1) #arrotonda i secs
            nuovo_record = salva_record(level_number, tempo_finale) #non so pk ma non mi carica sta cosa..
            record = carica_record()
            screen.fill((0, 20, 0))
            font_big = pygame.font.Font(None, 120)
            font_med = pygame.font.Font(None, 60)
            font_sml = pygame.font.Font(None, 40)
            t1 = font_big.render("LIVELLO COMPLETATO!", True, (100, 255, 100))
            t2 = font_med.render(f"Tempo: {tempo_finale}s", True, (255, 255, 255))
            t3 = font_med.render(f"Record: {record[level_number]}s", True, (255, 215, 0))
            t4 = font_sml.render("INVIO = Menu", True, (150, 150, 150))
            screen.blit(t1, t1.get_rect(center=(960, 250)))
            screen.blit(t2, t2.get_rect(center=(960, 380)))
            screen.blit(t3, t3.get_rect(center=(960, 460)))
            if nuovo_record:
                nr = font_med.render("NUOVO RECORD!", True, (255, 50, 50))
                screen.blit(nr, nr.get_rect(center=(960, 540)))
            screen.blit(t4, t4.get_rect(center=(960, 700)))
            pygame.display.flip()
            
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return False
                    if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                        return True
        
        level_text = font.render(f"LIVELLO {level_number} | ESC = Menu | SPAZIO = Attacco", True, (255, 255, 255))
        screen.blit(level_text, (10, 10))
        # ===================================================================================
        
        # Presenta il frame completato a schermo (doppio buffer)
        pygame.display.flip()
        clock.tick(60) # Limita a 60 FPS per avere un gioco consistente su qualsiasi PC
   
    return False

# ==============================================================================
# FUNZIONE: main
# Punto di ingresso del programma.
#
# Flusso:
#   1. Inizializza pygame e crea la finestra
#   2. Mostra la start screen
#   3. Loop principale: mostra selezione livelli -> avvia il gioco -> ripeti
#      (il loop si interrompe solo se il giocatore chiude la finestra)
# ==============================================================================
def main():
    pygame.init()
    screen = pygame.display.set_mode((1920, 1020))
    pygame.display.set_caption("Templar's Trial")
   
    start_screen(screen)
   
    game_running = True
    while game_running:
        selected_level = level_selection_screen(screen)
        while True:
            result = game_loop(screen, selected_level)
            if result == 'retry':
                continue
            elif result == True:
                break
            else:
                game_running = False
                break
   
    pygame.quit()

if __name__ == "__main__":
    main()
