import pygame ,os, sys ,neat, random

WIN_WIDTH = 1000
WIN_HEIGHT = 800
BIRDS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird1.png"))),
         pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird2.png"))),
         pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird3.png")))]
PIPE = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png")))
BASE = pygame.image.load(os.path.join('imgs','base.png'))
BG = pygame.transform.scale(pygame.image.load(os.path.join("imgs","bg.png")),(500,800))
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
        self.y += self.tick_count * ( 0.1)          # acceleration 

    def move_right(self):
        self.x += 1

    def get_mask(self):
        return pygame.mask.from_surface(self.img)

    def draw(self):
        # self.tick_count += 1
        self.animation_frame += 1

        if self.animation_frame >= 5:               # animating each frame
            self.bird_index = (self.bird_index + 1) % len(BIRDS)
            self.img = BIRDS[self.bird_index]   
            self.animation_frame = 0

        self.move()

        win.blit(self.img,(self.x, self.y))

class Base:
    Y_TOP = 700
    VELOCITY = 5
    WIDTH = BASE.get_width()
    base = pygame.transform.scale(BASE, (500,BASE.get_height()))  

    def __init__(self,x):
        self.x1 = x 
        self.x2 = self.x1 + self.WIDTH
      
    def move(self):
        self.x1 -= self.VELOCITY
        self.x2 -= self.VELOCITY

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH
    
    def draw(self):
        win.blit(self.base,(self.x1,self.Y_TOP))
        win.blit(self.base,(self.x2,self.Y_TOP))
        
class Pipe:
    PIPE_GAP = 200
    VELOCITY = 5
    PIPE_TOP = pygame.transform.rotate(PIPE,180)
    PIPE_BOTTOM = PIPE

    def __init__(self,x):
        self.x_top = x                               
        self.x_bottom = self.x_top
        self.y_top = random.randrange(50,400) - PIPE.get_height()     # top_pipe top height    
        self.top_edge =  self.y_top + PIPE.get_height()                # top pipe bottom height
        self.y_bottom = self.y_top + self.PIPE_GAP + PIPE.get_height()    # bottom pipe top height
        self.passed = False    

    def move(self):
        self.x_top -= self.VELOCITY
        self.x_bottom -= self.VELOCITY

    def collition(self, bird):
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
        bird_mask = bird.get_mask()  

        top_offset = (self.x_top - bird.x, self.y_top - round(bird.y))
        bottom_offset = (self.x_bottom- bird.x, self.y_bottom - round(bird.y))

        collide_top = bird_mask.overlap(top_mask, top_offset)
        collide_bottom = bird_mask.overlap(bottom_mask, bottom_offset)

        if collide_top or collide_bottom:
            return True  # Optional, so you can use it in `if pipe.collition(bird)`
        
        return False
        
    def draw(self):
        win.blit(self.PIPE_TOP,(self.x_top,self.y_top))
        win.blit(self.PIPE_BOTTOM,(self.x_bottom,self.y_bottom))


def draw_canvas(birds,pipes,base):
    win.fill((0,0,0))
    win.blit(BG,(0,0))
    for pipe in pipes:
        Pipe.draw(pipe)

    for bird in birds:
        Bird.draw(bird)

    Base.draw(base)
    

def dataVisualization():
    data_canvas = pygame.Surface((500, 800))
    data_canvas.fill((30,30,30))
    win.blit(data_canvas,(500,0))

pygame.init()

def main(genomes,config):
    
    running = True
    pipes = [Pipe(600)]
    pipe_distance = 100
    base = Base(0)

    nets = []
    birds= []
    gene = [] 
    for genome_id, genome in genomes:
        # genome.fitness = 4.0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        birds.append(Bird(250,400))
        genome.fitness = 0
        gene.append(genome)



    clock = pygame.time.Clock()

    while running  and len(birds) > 0:

        clock.tick(30)     # frames per second 
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        add_pipe = False
        remove_pipes = []
        dead_birds =[]
        pipe_ind = 0

        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x_top + pipes[0].PIPE_TOP.get_width():  
                pipe_ind = 1                                                                 

        for id, bird in enumerate(birds):
            gene[id].fitness += 0.1

            output = nets[birds.index(bird)].activate((bird.y, abs(bird.y - pipes[pipe_ind].top_edge), abs(bird.y - pipes[pipe_ind].y_bottom)))

            if output[0] > 0.5:  
                bird.jump()

        for pipe in pipes:

            pipe.move()

            for id ,bird in enumerate(birds):

                if pipe.x_top + pipe.PIPE_TOP.get_width() < 0:
                    remove_pipes.append(pipe)

                if not pipe.passed and birds[id].x > pipe.x_top:
                    pipe.passed = True
                    add_pipe = True
                    gene[id].fitness += 5
                
                if(pipe.collition(bird)) or bird.y < 0 or bird.y > 700:
                    print(birds,"\n",bird)
                    dead_birds.append(id)
                    gene[id].fitness -= 5

        for i in reversed(dead_birds):   # removing collide birds after collition checking loop
            birds.pop(i)
            nets.pop(i)
            gene.pop(i)         

        if add_pipe:
            pipes.append(Pipe(500))  # new pipe from right

        for r in remove_pipes:
            if r in pipes:
                pipes.remove(r)

        base.move()

        draw_canvas(birds,pipes,base)
        dataVisualization()
        pygame.display.update()  
    
    return


def run():

    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "neatParameters.txt")

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    
       # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)


    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))


    # Run for up to 50 generations.
    winner = p.run(main, 10)
    print(winner)


if __name__ == "__main__":
    run()
