from projectile import Projectile
import pygame
import os

current_path = os.path.dirname(__file__)
bullets = []


class Tower:

    def __init__(self, x, y, lvl=1):
        self.x = x
        self.y = y
        self.count = 0
        self.damage = 1
        self.pic = pygame.image.load(os.path.join(current_path, 'Tack_shooter.png'))
        self.lvl = lvl
        self.max_lvl = 10
        self.upgrade_cost = 60
        self.max_dis = 150
        self.shoot_count = 0

    def move_bullets(self, wn):
        for bullet in bullets:
            # pops bullets that are out of the screen
            if -10 < bullet.x > 920 or -10 < bullet.y > 690:
                bullets.pop(bullets.index(bullet))

            # bullets are not allowed to travel over the maximum distance.
            elif abs(bullet.orx - bullet.x) > self.max_dis or abs(bullet.ory - bullet.y) > self.max_dis:
                bullets.pop(bullets.index(bullet))

            # moves all valid bullets (on the screen and haven't traveled their entire distance).
            else:
                bullet.x += bullet.xvel
                bullet.y += bullet.yvel
                pygame.draw.circle(wn, (255, 255, 0), (bullet.x, bullet.y), bullet.radius)

    def fire_bullet(self):
        # tac shooter picture is 75 * 86 pixels
        # fires one bullet in each one of the 4 directions.
        x = self.x + 37
        y = self.y + 42
        # the higher the level the more bullets and in more directions can be shot
        self.shoot_count += 1
        if self.shoot_count > 0:
            if self.lvl == 1:
                # horizontal bullets
                bullets.append(Projectile(x, y, yvel=0))
                bullets.append(Projectile(x, y, xvel=-10, yvel=0))
                self.shoot_count -= 30
            elif self.lvl == 2:
                # horizontal bullets
                bullets.append(Projectile(x, y, yvel=0))
                bullets.append(Projectile(x, y, xvel=-10, yvel=0))
                # vertical bullets
                bullets.append(Projectile(x, y, xvel=0))
                bullets.append(Projectile(x, y, yvel=-10, xvel=0))
                self.shoot_count -= 23
            elif self.lvl >= 3:
                # instead of making bullet levels, we append more bullets.
                # that also means that high level bullets can kill more than 1 enemy.
                for _ in range(self.lvl - 2):
                    # horizontal bullets
                    bullets.append(Projectile(x, y, yvel=0))
                    bullets.append(Projectile(x, y, xvel=-10, yvel=0))
                    # vertical bullets
                    bullets.append(Projectile(x, y, xvel=0))
                    bullets.append(Projectile(x, y, yvel=-10, xvel=0))
                    # slant bullets
                    bullets.append(Projectile(x, y))  # x and y speeds are 10 and 10
                    bullets.append(Projectile(x, y, xvel=-10, yvel=10))
                    bullets.append(Projectile(x, y, xvel=10, yvel=-10))
                    bullets.append(Projectile(x, y, xvel=-10, yvel=-10))
                    self.shoot_count -= 3
                self.shoot_count -= 16

    def show_upgrade(self, wn, cash):
        red_plus = pygame.image.load(os.path.join(current_path, 'plus_lvl_sign_red.png'))
        green_plus = pygame.image.load(os.path.join(current_path, 'plus_lvl_sign_green.png'))
        if self.lvl < self.max_lvl:
            # since the pluses are going to be shown level has to be shown on the side (not centered)
            font = pygame.font.SysFont('arial', size=12, bold=True)
            level = font.render(f'{self.lvl}', True, (0, 0, 0))
            wn.blit(level, (self.x + 20, self.y - 10))

            if self.upgrade_cost > cash:  # red plus if can't upgrade
                wn.blit(red_plus, (self.x + 30, self.y - 10))
            else:  # green plus if upgrade is available.
                wn.blit(green_plus, (self.x + 30, self.y - 10))

            upgrade_cost = font.render(f"{self.upgrade_cost}", True, (255, 255, 255))
            wn.blit(upgrade_cost, (self.x + 50, self.y - 10))
        else:  # shows the level in the top middle if in max level, since no plus sign appears.
            font = pygame.font.SysFont('arial', size=12, bold=True)
            level = font.render(f'{self.lvl}', True, (0, 0, 0))
            wn.blit(level, (self.x + 34, self.y - 10))

    def raise_level(self):
        self.lvl += 1
        self.upgrade_cost *= 3
        self.max_dis *= 1
