import pygame ,os, sys ,neat, random

WIN_WIDTH = 500
WIN_HEIGHT = 800
BIRDS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird1.png"))),
         pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird2.png"))),
         pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird3.png")))]
PIPE = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png")))
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

        win.blit(self.img,(self.x, self.y))

class Pipe:
    PIPE_GAP = 300
    VELOCITY = 5
    PIPE_TOP = pygame.transform.rotate(PIPE,180)
    PIPE_BOTTOM = PIPE

    def __init__(self,x):
        self.x_top = x                            # top pipe bottom left corner x axis
        self.x_bottom = self.x_top
        self.y_top = random.randrange(50,500) - PIPE.get_height()                  
        self.y_bottom = self.y_top + self.PIPE_GAP + PIPE.get_height()

    def move(self):
        self.x_top -= self.VELOCITY
        self.x_bottom -= self.VELOCITY

    def draw(self):
        win.blit(self.PIPE_TOP,(self.x_top,self.y_top))
        win.blit(self.PIPE_BOTTOM,(self.x_bottom,self.y_bottom))

        

        

        

def draw_canvas(bird,pipes):

    win.fill((0,0,0))
    for pipe in pipes:
        Pipe.draw(pipe)


    Bird.draw(bird)
    


pygame.init()

def main():
    
    running = True
    
    bird = Bird(200,200)
    pipes = [Pipe(200),Pipe(400)]
    
    clock = pygame.time.Clock()

    while running:

        clock.tick(30)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            bird.jump()

        for pipe in pipes:
            pipe.move()
            
        bird.move()
        draw_canvas(bird,pipes)
        pygame.display.update()  
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()