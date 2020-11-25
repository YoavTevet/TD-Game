import random
import pygame
import os

current_path = os.path.dirname(__file__)
money = []


def place_money(wn):
    for coin in money:
        wn.blit(coin.pic, (coin.x, coin.y))


class Cash:
    pic = pygame.image.load(os.path.join(current_path, 'Coin.png'))

    def __init__(self, multiplier=1):
        self.value = random.randint(5, 20) * multiplier
        self.x = random.randint(100, 800)
        self.y = random.randint(100, 570)


class PowerUp:

    def __init__(self):
        self.lvl = random.randint(1, 3)


class MoneyMultiplier:

    def __init__(self):
        self.multiplier = 1
