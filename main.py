import pygame
import os
from defenses import Tower
import defenses
from enemies import Enemy
import bonuses
from bonuses import Cash
import random


pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption("Tower Defense Game")
current_path = os.path.dirname(__file__)
win = pygame.display.set_mode((900, 674))
bg = pygame.image.load(os.path.join(current_path, 'background.jpg'))  # background
tow_pic = pygame.image.load(os.path.join(current_path, 'Tack_shooter.png'))
font = pygame.font.SysFont('arial', size=30, bold=True)
speed1 = pygame.image.load(os.path.join(current_path, 'speed_1x.png'))
speed2 = pygame.image.load(os.path.join(current_path, 'speed_2x.png'))
speed3 = pygame.image.load(os.path.join(current_path, 'speed_3x.png'))


def mouse_coordinates():  # helps find coordinates while developing.
    location = font.render(f'({mouse[0]}, {mouse[1]})', True, (255, 255, 0))
    win.blit(location, (50, 30))


def char_coordinates():  # also shows the number of bullets on the screen.
    if hostile:
        char_loc = font.render(f'({hostile[0].x}, {hostile[0].y})', True, (255, 255, 0))
        win.blit(char_loc, (50, 70))
    bullet_count = font.render(f'bullets:{len(defenses.bullets)}', True, (255, 255, 0))
    win.blit(bullet_count, (50, 110))


def redrawGameWindow():  # contains all the things to redraw every time the main loop occurs.
    win.blit(bg, (0, 0))  # background has to be redrawn everytime

    for t in towers:  # draws towers in their place
        win.blit(t.pic, (t.x, t.y))
        if towers.index(t) == 0:  # move_bullets() function already goes through all bullets of all towers
            t.move_bullets(win)

    # moves all necessary and removes all enemies that have exceeded track limits
    for enemy in hostile:
        if enemy.x < 920:
            enemy.walk(win)
            enemy.health_bar(win)
            # enemy.hit_box(win)  # for development

    # shows little plus sign next to tower when pointing mouse at it.
    for to in towers:
        if to.x == 245 and to.y == 322 and 250 < mouse[0] < 320 and 350 < mouse[1] < 410 and is_placed[0]:
            to.show_upgrade(win, money)
        elif to.x == 410 and to.y == 223 and 410 < mouse[0] < 480 and 250 < mouse[1] < 310 and is_placed[1]:
            to.show_upgrade(win, money)
        elif to.x == 582 and to.y == 262 and 580 < mouse[0] < 650 and 280 < mouse[1] < 350 and is_placed[2]:
            to.show_upgrade(win, money)
        elif to.x == 617 and to.y == 384 and 620 < mouse[0] < 690 and 410 < mouse[1] < 470 and is_placed[3]:
            to.show_upgrade(win, money)

    # draw coins (bonuses)
    bonuses.place_money(win)

    # shows how much money you have
    total_mon = font.render(f'money: {money}', True, (0, 255, 0))
    win.blit(total_mon, (720, 20))

    tot_lives = font.render(f'lives: {lives}', True, (0, 255, 255))
    win.blit(tot_lives, (500, 20))

    # speed motion buttons
    pygame.draw.rect(win, (0, 255, 0), (50, 25, 140, 40))
    win.blit(speed1, (50, 25))
    win.blit(speed2, (95, 25))
    win.blit(speed3, (140, 25))

    # displays mouse and character locations (for development)
    # mouse_coordinates()
    # char_coordinates()

    pygame.display.update()


towers = []  # all defenses the player has placed
hostile = []  # all hostile creatures/enemies currently on the map
is_placed = [False, False, False, False]  # which towers are placed
shoot_count = 0  # when reaches a certain amount towers shoot (obviously)
coin_collector = 120
money = 30
click_count = 0
speed = 1
enemies_killed = 0
spawn_max = 50  # the lower spawn_max is the higher the chance that enemies spawn.
lives = 50


run = True
while run:
    clock.tick(30 * speed)
    mouse = pygame.mouse.get_pos()  # tuple of two nums (x, y)

    # closes the game when x is pressed.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # closes the game if our of lives
    if lives <= 0:
        run = False

    max_health = (enemies_killed // 25) + 1  # the higher this is the more heath the enemies are likely to have.
    if max_health > 30:  # can't have max health over 30 because the health bar won't show up.
        max_health = 30
    spawn = random.randint(0, spawn_max)  # randomly spawn enemies
    if spawn == 1:
        hostile.append(Enemy(0, 410, health=random.randint(1, max_health)))

    # pops enemies that are out of the screen and decreases lives.
    for enemy in hostile:
        if enemy.x > 910:
            lives -= enemy.hp
            hostile.pop(hostile.index(enemy))
            print("Popped an enemy")

    # places towers in the spot that was clicked on.
    # find coins and collect them
    # speed up or slow down game
    if pygame.mouse.get_pressed(num_buttons=3)[0]:  # left click
        # for tower placement
        if money >= 30:
            if 250 < mouse[0] < 320 and 350 < mouse[1] < 410 and not is_placed[0]:  # tower 1
                towers.append(Tower(245, 322))
                is_placed[0] = True
                money -= 30
            elif 410 < mouse[0] < 480 and 250 < mouse[1] < 310 and not is_placed[1]:  # tower 2
                towers.append(Tower(410, 223))
                is_placed[1] = True
                money -= 30
            elif 580 < mouse[0] < 650 and 280 < mouse[1] < 350 and not is_placed[2]:  # tower 3
                towers.append(Tower(582, 262))
                is_placed[2] = True
                money -= 30
            elif 620 < mouse[0] < 690 and 410 < mouse[1] < 470 and not is_placed[3]:  # tower 4
                towers.append(Tower(617, 384))
                is_placed[3] = True
                money -= 30

        # for coin collection
        if bonuses.money:
            for coin in bonuses.money:
                if coin.x + 3 < mouse[0] < coin.x + 50:
                    if coin.y < mouse[1] < coin.y + 60:
                        money += coin.value  # gives money
                        bonuses.money.pop(bonuses.money.index(coin))  # deletes coin
                        print("money:", money)

        # for speed motion buttons
        if 25 < mouse[1] < 75:
            if 50 < mouse[0] < 90:
                speed = 1
            elif 95 < mouse[0] < 135:
                speed = 2
            elif 140 < mouse[0] < 180:
                speed = 3
        # end of speed motion buttons

        # for coin collection levels

    # make sure click is not spammed
    click_count += 1
    if click_count == 3:
        click_count = 0

    # upgrade towers
    for tow in towers:
        if pygame.mouse.get_pressed(num_buttons=3)[2] and click_count == 0 and tow.lvl < tow.max_lvl:  # right click
            if tow.upgrade_cost < money:
                if tow.x == 245 and tow.y == 322 and 250 < mouse[0] < 320 and 350 < mouse[1] < 410 and is_placed[0]:
                    money -= tow.upgrade_cost
                    tow.raise_level()
                    print(f"raised tower 1 to level {tow.lvl}")
                elif tow.x == 410 and tow.y == 223 and 410 < mouse[0] < 480 and 250 < mouse[1] < 310 and is_placed[1]:
                    money -= tow.upgrade_cost
                    tow.raise_level()
                    print(f"raised tower 2 to level {tow.lvl}")
                elif tow.x == 582 and tow.y == 262 and 580 < mouse[0] < 650 and 280 < mouse[1] < 350 and is_placed[2]:
                    money -= tow.upgrade_cost
                    tow.raise_level()
                    print(f"raised tower 3 to level {tow.lvl}")
                elif tow.x == 617 and tow.y == 384 and 620 < mouse[0] < 690 and 410 < mouse[1] < 470 and is_placed[3]:
                    money -= tow.upgrade_cost
                    tow.raise_level()
                    print(f"raised tower 4 to level {tow.lvl}")

    # collision with bullets
    for bull in defenses.bullets:
        for char in hostile:
            if char.x + 12 < bull.x < char.x + 45 and char.y + 8 < bull.y < char.y + 64:
                # print(char.hp)
                char.hp -= 1  # decrease character hp by 1
                # removes dead enemies.
                if char.hp == 0:
                    bonuses.money.append(Cash(multiplier=char.orhp))  # gives money for the dead.
                    hostile.pop(hostile.index(char))
                    print("hostiles left:", len(hostile))
                    enemies_killed += 1
                defenses.bullets.pop(defenses.bullets.index(bull))  # removes bullet from screen.
                break  # must break, can't find characters that collide with removed bullets.

    # shoots every once in a while, and only when enemies are in range.
    for tower in towers:
        can_shoot = False
        for enem in hostile:
            # if any enemy is within a tower.max_dis of the tower on any direction (in its range).
            if tower.x - tower.max_dis <= enem.x < tower.x + tower.max_dis and\
                    tower.y - tower.max_dis <= enem.y <= tower.max_dis + tower.y:
                can_shoot = True
                break
        if can_shoot:
            tower.fire_bullet()

    # auto coin collector  (should consider adding as a boost. currently good for development.)
    collect = random.randint(1, coin_collector)
    if collect > 100:
        for coin in bonuses.money:
            money += coin.value  # gives money
            bonuses.money.pop(bonuses.money.index(coin))  # deletes coin
            break

    redrawGameWindow()  # remakes the whole game and updates the screen.

pygame.quit()
