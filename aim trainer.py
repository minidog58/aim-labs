import math
import random
import time
import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600


WINDOW = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("aim trainer game")

TARGET_TIMER = 400 #rate at which targets appear in miliseconds
TARGET_EVENT = pygame.USEREVENT
TARGET_PADDING = 100
SCORE_BOARD_HIEGHT = 50
SCORE_BOARD_WIDTH = WIDTH

GAME_TIME = 10

FONT = pygame.font.SysFont("comicsans", 24)

class Target: 
    MAX_SIZE = 40
    GROWTH_RATE = 0.2
    COLOR = ["red", "yellow"]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 0
        self.grow = True

    def update(self):# once the target becomes it's max size it will stop growing
        if self.size + self.GROWTH_RATE >= self.MAX_SIZE:
            self.grow = False

        if self.grow:# this will change the size of the target to grow or shrink
            self.size += self.GROWTH_RATE
        else:
            self.size -= self.GROWTH_RATE

    def draw(self, WINDOW):
        pygame.draw.circle(WINDOW,self.COLOR[0], (self.x, self.y), self.size)#draw the target on the window with the obj values color, (x,y) , size
        pygame.draw.circle(WINDOW,self.COLOR[1], (self.x, self.y), self.size * 0.8)
        pygame.draw.circle(WINDOW,self.COLOR[0], (self.x, self.y), self.size * 0.6)
        pygame.draw.circle(WINDOW,self.COLOR[1], (self.x, self.y), self.size * 0.4)

    def targetHit(self, x , y):
        distance = math.sqrt((self.x - x)**2 + (self.y - y)**2)
        return distance <= self.size
    
def drawTarget(WINDOW, targets):
    WINDOW.fill("white")

    for target in targets:# for every target in array draw target on WINDOW
        target.draw(WINDOW)


def format_time(secs):
    milli = math.floor(int(secs * 1000 % 1000)/100)
    seconds = int(round(secs%60,1))
    return f"{seconds:02d}:{milli}"


def draw_score_Board(WINDOW, elapsed_time, targets_hit, misses):
    pygame.draw.rect(WINDOW, "black" , (0,0, SCORE_BOARD_WIDTH, SCORE_BOARD_HIEGHT))
    time_text = FONT.render(f"Time: {format_time(elapsed_time)}", 1, "white")
    hits_text = FONT.render(f"HITS: {targets_hit}", 1 , "white")
    misses_text = FONT.render(f"MISSES: {misses}", 1 , "white")

    WINDOW.blit(time_text, (5,5))
    WINDOW.blit(hits_text, (200,5))
    WINDOW.blit(misses_text, (400,5))

def end_screen(WINDOW, time, targets_hit, misses):
    WINDOW.fill("white")

    time_text = FONT.render(f"Time: {format_time(time)}", 1, "black")
    hits_text = FONT.render(f"HITS: {targets_hit}", 1 , "black")
    misses_text = FONT.render(f"MISSES: {misses}", 1 , "black")

    WINDOW.blit(time_text, (300, 150))
    WINDOW.blit(hits_text, (300, 300))
    WINDOW.blit(misses_text, (300, 450))

    pygame.display.update()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                quit()



def main():
    game = True

    targets = []
    frameRate = pygame.time.Clock()

    target_hit = 0
    hits = 0
    misses = 0
    start_timer = time.time() 


    pygame.time.set_timer(TARGET_EVENT, TARGET_TIMER)

    while game:
        frameRate.tick(100)
        click = False

        mouse_pos = pygame.mouse.get_pos()
        clock_timer = time.time() - start_timer


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
                break
            
            if event.type == TARGET_EVENT: # create the target within the window at random and add the target to the targets array
                x = random.randint(TARGET_PADDING, WIDTH - TARGET_PADDING)
                y = random.randint(TARGET_PADDING, HEIGHT - TARGET_PADDING)
                target = Target(x,y)
                targets.append(target)

            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                hits += 1

                
        for target in targets: # update the target
            target.update()
            if target.size <= 0:
                targets.remove(target) # remove target 
                misses += 1

            if click and target.targetHit(*mouse_pos):
                targets.remove(target)
                target_hit += 1
        
        if clock_timer > GAME_TIME:
            end_screen(WINDOW, clock_timer, target_hit, misses)

        drawTarget(WINDOW, targets) # draw the target on screen
        draw_score_Board(WINDOW, clock_timer, target_hit, misses)
        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()