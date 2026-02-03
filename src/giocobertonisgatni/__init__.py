#progettone pazzo sgravato
import pygame

def main() -> None:
    print("Hello from giocobertonisgatni!")
    
    pygame.init()
    
    # schermo e titolo del gioco <33
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("titolo del gioco, lo decideremo un giorno...")
    
    running = True
    
    while running:
        # serve a gestire la X di chiusura in alto
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # colore dello sfondo.... poi vedremo...
        screen.fill((0, 0, 0)) #funzia come gli RGB, MAX 255
        
        # serve ad aggiornare il contenuto dello schermo
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()
    
    
    

    
    
    
    