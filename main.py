import pygame ,os, sys ,neat, random

WIN_WIDTH = 1000
WIN_HEIGHT = 800
BIRDS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird1.png"))),
         pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird2.png"))),
         pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird3.png")))]
PIPE = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png")))
BASE = pygame.image.load(os.path.join('imgs','base.png'))
BG = pygame.transform.scale(pygame.image.load(os.path.join("imgs","bg.png")),(500,800))
NODESIMG = pygame.transform.smoothscale(pygame.image.load(os.path.join("imgs","nodes.png")),(500,281))
win  = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
GEN = 0

class Bird:

    VELOCITY = -10
    MAX_ROTATION = 25
    
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.tick_count = 0
        self.velocity = 0
        self.gravity = 1.3
        self.bird_index = 0
        self.imgs = BIRDS
        self.animation_frame = 0
        self.img = self.imgs[0]
        self.angle = 0

    def jump(self):
        # self.angle = 0
        self.velocity = -12

    def move(self):
        self.velocity += self.gravity                  # acceleration 
        self.y += self.velocity
        if self.velocity < 0:
            self.angle = min(self.angle + 5, self.MAX_ROTATION)
        else:
            self.angle = max(self.angle - 3, -90)
        # self.img = pygame.transform.rotate(self.img,self.MAX_ROTATION)


    def get_mask(self):
        return pygame.mask.from_surface(self.img)

    def draw(self):
        self.animation_frame += 1

        if self.animation_frame >= 5:                   # animating each frame
            self.bird_index = (self.bird_index + 1) % len(BIRDS)
            self.img = BIRDS[self.bird_index]   
            self.animation_frame = 0

        self.move()

        # win.blit(self.img,(self.x, self.y))

        rotated_img = pygame.transform.rotate(self.img, self.angle)
        new_rect = rotated_img.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)

        win.blit(rotated_img, new_rect.topleft)



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
    PIPE_GAP = 110
    VELOCITY = 5
    PIPE_TOP = pygame.transform.rotate(PIPE,180)
    PIPE_BOTTOM = PIPE

    def __init__(self,x):
        self.x_top = x                               
        self.x_bottom = self.x_top
        self.y_top = random.randrange(100,470) - PIPE.get_height()     # top_pipe top height    
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
            return True 
        
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
    

def dataVisualization(birds,best,inputs):
    canvas = pygame.Surface((500, 800),pygame.SRCALPHA)

    height = canvas.get_height()
    width = canvas.get_width()
    top_color = (41, 3, 70)
    bottom_color =(54, 26, 75)

    for y in range(height):
        rotation = y / height
        r = int(top_color[0] * (1 - rotation) + bottom_color[0] * rotation)
        g = int(top_color[1] * (1 - rotation) + bottom_color[1] * rotation)
        b = int(top_color[2] * (1 - rotation) + bottom_color[2] * rotation)
        pygame.draw.line(canvas, (r, g, b), (0, y), (width, y))
    


    divs = pygame.Surface((450,50))
    divs.fill((37,37,56))


    
    font1 = pygame.font.SysFont("Gotham", 45)

    font2 = pygame.font.SysFont("Cascadia Mono", 45)
    font3 = pygame.font.SysFont("Circular Spotify", 45)
    text_gen = font1.render(f"GEN : {GEN}", True, (255, 255, 255))
    text_birds = font2.render(f"Birds : {len(birds)}", True, (255, 255, 255))
    text_max_fitness = font3.render(f"Max-fitness : {best.fitness:.3f}", True, (255, 255, 255))

    pygame.draw.rect(canvas, (133, 36, 208), (25,20,450,60), border_radius=10)
    pygame.draw.rect(canvas, (154, 38, 243), (25,100,450,60), border_radius=10)
    pygame.draw.rect(canvas, (108, 0, 190), (25,180,450,60), border_radius=10)

    canvas.blit(text_gen,(50,36))
    canvas.blit(text_birds,(50,118))
    canvas.blit(text_max_fitness,(50,196))
    canvas.blit(NODESIMG,(0,300))


    

    font1 = pygame.font.SysFont("Gotham", 35)

    WEIGHTS = []

    for conn_key, conn in best.connections.items():
        WEIGHTS.append(f"{conn.weight:.2f}")
        # print(f"Connection from {conn_key[0]} to {conn_key[1]} has weight: {conn.weight}")
    while len(WEIGHTS) < 3:
        WEIGHTS.append("0.00")


    text_input1 = font1.render(f"{inputs[0]:.1f}", True, (255, 255, 255))
    text_input2 = font1.render(f"{inputs[1]:.1f}", True, (255, 255, 255))
    text_input3 = font1.render(f"{inputs[2]:.1f}", True, (255, 255, 255))
    text_output = font1.render(f"{inputs[3]:.1f}", True, (255, 255, 255))

    # WEIGHTS_1, WEIGHTS_2, WEIGHTS_3 = WEIGHTS

    text_w1 = font1.render(WEIGHTS[0] , True, (255, 255, 255))
    text_w2 = font1.render(WEIGHTS[1], True, (255, 255, 255))
    text_w3 = font1.render(WEIGHTS[2] , True, (255, 255, 255))

    canvas.blit(text_w1,(168,345))
    canvas.blit(text_w2,(168,438))
    canvas.blit(text_w3,(168,531))

    canvas.blit(text_input1,(47,345))
    canvas.blit(text_input2,(48,438))
    canvas.blit(text_input3,(45,531))
    canvas.blit(text_output,(415,534))


    win.blit(canvas,(500,0))    


    # for node_key, node in best.nodes.items():
    #     print(f"Node {node_key} bias: {node.bias}, activation: {node.activation}")


pygame.init()

def main(genomes,config):
    
    global GEN
    GEN += 1
    
    PIPE_DIFF = 530
    running = True
    pipes = [Pipe(PIPE_DIFF)]
    base = Base(0)

    nets = []
    birds= []
    gene = [] 
    best = None;
    best_bird_index = 0;
    inputs = [];

    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        birds.append(Bird(250,400))
        genome.fitness = 0
        gene.append(genome)

        if best is None or genome.fitness > best.fitness:
            best = genome
            best_bird_index = gene.index(genome)
        

    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()

    clock = pygame.time.Clock()

    while running  and len(birds) > 0:

        clock.tick(30)     # frames per second 
                
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
            
            if(id == best_bird_index):
                inputs = [bird.y, abs(bird.y - pipes[pipe_ind].top_edge), abs(bird.y - pipes[pipe_ind].y_bottom),output[0]]
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
                
                if(pipe.collition(bird)) or (bird.y + bird.img.get_width()) < 0 or bird.y > 700:
                    dead_birds.append(id)
                    gene[id].fitness -= 5

        for i in reversed(dead_birds):   # removing collide birds after collition checking loop
            if len(birds) > 0:
                birds.pop(i)
            nets.pop(i)
            gene.pop(i)         

        if add_pipe:
            pipes.append(Pipe(PIPE_DIFF))  # new pipe from right

        for r in remove_pipes:
            if r in pipes:
                pipes.remove(r)

        base.move()

    
        draw_canvas(birds,pipes,base,)
        dataVisualization(birds,best,inputs)

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
    # p.add_reporter(neat.StdOutReporter(True))
    # stats = neat.StatisticsReporter()
    # p.add_reporter(stats)
    # p.add_reporter(neat.Checkpointer(5))

    # Run for up to 50 generations.
    winner = p.run(main, 50)
    print(winner)



if __name__ == "__main__":
    run()
