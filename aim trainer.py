import math
import random
import time
import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600


WINDOW = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("aim trainer game")

TARGET_TIMER = 300 #rate at which targets appear in miliseconds
TARGET_EVENT = pygame.USEREVENT
TARGET_PADDING = 50

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


def drawTarget(WINDOW, targets):
    WINDOW.fill("white")

    for target in targets:# for every target in array draw target on WINDOW
        target.draw(WINDOW)

    pygame.display.update()

def main():
    game = True

    targets = []
    frameRate = pygame.time.Clock()

    pygame.time.set_timer(TARGET_EVENT, TARGET_TIMER)

    while game:
        frameRate.tick(100)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
                break
            
            if event.type == TARGET_EVENT: # create the target within the window at random and add the target to the targets array
                x = random.randint(TARGET_PADDING, WIDTH - TARGET_PADDING)
                y = random.randint(TARGET_PADDING, HEIGHT - TARGET_PADDING)
                target = Target(x,y)
                targets.append(target)

        for target in targets: # update the target
            target.update()
            if target.size <= 0:
                targets.remove(target) # remove target 
        
        drawTarget(WINDOW, targets) # draw the target on screen
        
    pygame.quit()

if __name__ == "__main__":
    main()