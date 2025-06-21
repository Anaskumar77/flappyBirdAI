import pygame ,os, sys ,neat

WIN_WIDTH = 500
WIN_HEIGHT = 800
BIRDS = [pygame.image.load(os.path.join("imgs","bird1.png")),pygame.image.load(os.path.join("imgs","bird2.png")),pygame.image.load(os.path.join("imgs","bird3.png"))]

win  = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))

class Bird:
    VELOCITY = -10
    MAX_ROTATION = 35
    


    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.tick_count = 0
        self.velocity = 0
        self.bird_index = 0
        self.imgs = BIRDS
        self.animation_frame = 0
        self.img = self.imgs[0]

    def jump(self):
        self.tick_count = 0

        self.y -= 15

    def move(self):
        self.tick_count += 1
        self.y += self.tick_count * ( 0.1)  # acceleration 

    def draw(self):
        # self.tick_count += 1
        self.animation_frame += 1

        if self.animation_frame >= 5:        # animating each frame
            self.bird_index = (self.bird_index + 1) % len(BIRDS)
            self.img = BIRDS[self.bird_index]   
            self.animation_frame = 0

        self.move()
        self.jump()

        win.blit(self.img,(self.x, self.y))
        
        
        

def draw_canvas(bird):
    win.fill((0,0,0))

    Bird.draw(bird)
    


pygame.init()

def main():
    
    running = True
    
    bird = Bird(200,200)

    clock = pygame.time.Clock()

    while running:

        clock.tick(30)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_canvas(bird)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            bird.jump()

        bird.move()
        
        pygame
        
        pygame.display.update()  
    
    pygame.quit()
    sys.exit()




if __name__ == "__main__":
    main()