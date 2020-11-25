import pygame
import os

current_path = os.path.dirname(__file__)


class Enemy:
    pic = [pygame.image.load(os.path.join(current_path, 'R1.png')),
           pygame.image.load(os.path.join(current_path, 'R2.png')),
           pygame.image.load(os.path.join(current_path, 'R3.png')),
           pygame.image.load(os.path.join(current_path, 'R4.png')),
           pygame.image.load(os.path.join(current_path, 'R5.png')),
           pygame.image.load(os.path.join(current_path, 'R6.png')),
           pygame.image.load(os.path.join(current_path, 'R7.png')),
           pygame.image.load(os.path.join(current_path, 'R8.png')),
           pygame.image.load(os.path.join(current_path, 'R9.png'))]

    def __init__(self, x, y, speed=1, health=1):
        self.x = x
        self.y = y
        self.speed = speed
        self.hp = health
        self.starthp = health  # to be able to tell how to multiply the coin value once the enemy dies.
        self.walk_count = 0  # to have walking animation each image displayed 2 or 3 time in a row then next image
        self.width = self.height = 64
        self.orhp = health  # original / default health that never changes.

    def hit_box(self, wn):  # for development
        # picture actual character dimensions (not picture dimensions)
        wid = 45
        hei = 64
        box = [self.x + 12, self.y + 8, self.x + wid, self.y + hei]  # box coordinates
        pygame.draw.rect(wn, (255, 0, 0), (box[0], box[1], wid - 8, 5))  # top one
        pygame.draw.rect(wn, (255, 0, 0), (box[0], box[3], wid - 8, 5))  # bottom one
        pygame.draw.rect(wn, (255, 0, 0), (box[0], box[1], 5, hei - 5))  # left one
        pygame.draw.rect(wn, (255, 0, 0), (box[2], box[1], 5, hei - 5))  # right one

    def health_bar(self, wn):
        # draws red bar first, then green bar. once health drops green bar gets smaller, reveals the red one.
        pygame.draw.rect(wn, (255, 0, 0), (self.x + 15, self.y, (30 // self.orhp) * self.orhp, 5))
        pygame.draw.rect(wn, (0, 255, 0), (self.x + 15, self.y, (30 // self.orhp) * self.hp, 5))

    def walk(self, wn):  # the course of walking over the map
        self.walk_count += 1
        if self.walk_count >= 17:
            self.walk_count = 0

        if self.x <= 285:  # gets to turn 1
            self.x += self.speed

        if 400 >= self.x >= 285 and 500 >= self.y >= 230:
            if self.y > 230:  # starts going up at turn 1
                self.y -= self.speed

            if 370 <= self.y <= 440:  # makes turn 1 smooth
                self.x += self.speed

        # smoothing turn 2
        if self.y <= 250 and self.x <= 400:
            self.x += self.speed
            self.y -= self.speed

        # moving between turn 2 and turn 3
        if 390 <= self.x <= 435:
            self.x += self.speed

        # smoothing turn 3
        if self.x >= 435 and 160 <= self.y < 235:
            self.x += self.speed
            self.y += self.speed

        # moving between turns 3 and 4
        if 495 <= self.x and 230 <= self.y <= 300:
            self.y += self.speed
            self.x += self.speed // 2  # to get in the middle of the road (very close to side from prev statement)

        # if 495 <= self.x and 250 <= self.y <= 280:
        #     self.y += self.speed

        # smoothing turn 4
        if 320 >= self.y >= 280 and self.x >= 495:
            self.y += self.speed
            self.x += self.speed

        # way between turns 4 and 5
        if self.y >= 320 and 640 >= self.x >= 525:
            self.x += self.speed

        # making turn 5 smoother
        if self.y >= 320 and 700 >= self.x >= 640:
            self.x += self.speed
            self.y += self.speed

        # getting to the middle of the last straight
        if self.x >= 700 and 380 <= self.y <= 400:
            self.y += self.speed

        # going hard till end
        if self.x >= 700:
            self.x += self.speed

        wn.blit(Enemy.pic[self.walk_count // 2], (self.x, self.y))
