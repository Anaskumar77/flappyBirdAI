import pygame ,os, sys ,neat

WIN_WIDTH = 500
WIN_HEIGHT = 800
win  = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))



pygame.init()

def main():
    
    running = True

    clock = pygame.time.Clock()

    while running:

        clock.tick(30)
        win.fill((0,0,0))


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        pygame.display.update()  
    
    pygame.quit()
    sys.exit()



if __name__ == "__main__":
    main()