import pygame
from controller import check_events
from model import Hero, Skeleton_blue, TextBox, Skeleton_red, Warlock, Warlock_bullet, Fire, Meteor, Boss, Breath
import random
import time

def start_stage(game):
    pygame.init()
    surface = pygame.display.set_mode([game.window_size_x,game.window_size_y])
    suggestions = ['Using WASD to move!', 'J is attack and K is block!', 'Be careful with the magic attack!']
    background = pygame.image.load('assets/imgs/Battleground.png').convert()
    background = pygame. transform. scale(background, (game.window_size_x, game.window_size_y))
    avatar_group = pygame.sprite.GroupSingle()
    avatar = Hero((100, 500))
    avatar_group.add(avatar)
    skeleton_group = pygame.sprite.Group()
    warlock_group = pygame.sprite.Group()
    bullet_group = pygame.sprite.Group()
    fire_effect = pygame.sprite.Group()
    meteor_group = pygame.sprite.GroupSingle()
    breath_group = pygame.sprite.GroupSingle()
    count = time.time()
    meteor_ready = False
    aimopen = False
    pop = TextBox(surface)
    clock = pygame.time.Clock()
    state = 'running'
    boss_group = pygame.sprite.GroupSingle()
    boss_group.add(Boss((500, 200)))
    monsters = [skeleton_group, warlock_group, boss_group]
    groups = [avatar_group, skeleton_group, warlock_group]
    pop_state = -1

    while True:
        clock.tick(18)
        controls = check_events()
        if controls['quit']:
            game.next = False
            break
        if len(boss_group) == 0:
            game.next = True
            break
        if len(avatar_group) == 0 and state != 'pause':
            controls['pop'] = True
        if controls['pop']:
            if pop_state in [-1, 1]:
                state = pop.update(controls)
            if state != 'pause':
                pop_state = -1
            index = random.randint(0, len(suggestions)-1)
        if controls['aimchange'] and meteor_ready:
            aimopen = not aimopen
        if controls['reborn'] and len(avatar_group) == 0:
            avatar_group.add(Hero((100, 400)))
        if state == 'pause':
            if len(avatar_group) == 0:
                score = str(game.score)
                pop.pop_up(['You are dead', 'Current Score is ' + score,'Press R to rejoin the fight!'])
                pop_state = 0
            else:
                pop.pop_up(['Notes:', 'Press Q to quit', 'Press P to resume the game!', suggestions[index]])
                pop_state = 1
        else:
            surface.blit(background, (0,0))
            avatar_group.update(controls)
            bullet_group.update()
            fire_effect.update()
            breath_group.update()
            if len(avatar_group) > 0:
                boss_group.update(avatar_group.sprite.rect.center)
                if len(skeleton_group) > 0:
                    if (avatar_group.sprite.status in ['attack', 'attack2', 'attack3']):
                        monsters = skeleton_group.sprites()
                        avatar_group.sprite.update_attack_collision(monsters)
                    else:
                        battle = pygame.sprite.spritecollide(avatar_group.sprite, skeleton_group, dokill=False, collided=pygame.sprite.collide_mask)
                        avatar_group.sprite.update_hurt_collision(battle)
                if len(warlock_group) > 0:
                    if (avatar_group.sprite.status in ['attack', 'attack2', 'attack3']):
                        monsters = warlock_group.sprites()
                        avatar_group.sprite.update_attack_collision(monsters)
                    else:
                        battle = pygame.sprite.spritecollide(avatar_group.sprite, warlock_group, dokill=False, collided=pygame.sprite.collide_mask)
                        avatar_group.sprite.update_hurt_collision(battle)
                    for warlock_sprite in warlock_group.sprites():
                        if warlock_sprite.fire == 1:
                            bullet_group.add(Warlock_bullet((warlock_sprite.rect.center[0] + 15 * warlock_sprite.direction, warlock_sprite.rect.center[1] - 30),-(warlock_sprite.direction)))
                        if warlock_sprite.cast == 1:
                            fire_effect.add(Fire(avatar_group.sprite.rect.move(15,0).topleft))
                if len(bullet_group) > 0:
                    battle = pygame.sprite.spritecollide(avatar_group.sprite, bullet_group, dokill=False, collided=pygame.sprite.collide_mask)
                    avatar_group.sprite.update_bullet_collision(battle)
                if len(fire_effect) > 0:
                    battle = pygame.sprite.spritecollide(avatar_group.sprite, fire_effect, dokill=False, collided=pygame.sprite.collide_mask)
                    avatar_group.sprite.update_bullet_collision(battle)
                skeleton_group.update(avatar_group.sprite.rect.center, game)
                warlock_group.update(avatar_group.sprite.rect.center, game)
                draw_health_bar(avatar_group.sprite, surface)
                if game.magic == True:
                    meteor_ready = draw_meteor_icon(count, surface)
                else:
                    draw_skill_icon(surface)
                    meteor_ready = False
                if len(boss_group) > 0:
                    if boss_group.sprite.mode == 1:
                        if boss_group.sprite.state == 'run_idle':
                            draw_boss_heath_bar(boss_group.sprite, surface)
                            if (avatar_group.sprite.status in ['attack', 'attack2', 'attack3']):
                                monsters = [boss_group.sprite]
                                avatar_group.sprite.update_attack_collision(monsters)
                        else:
                            battle = pygame.sprite.spritecollide(avatar_group.sprite, boss_group, dokill=False, collided=pygame.sprite.collide_mask)
                            avatar_group.sprite.update_hurt_collision(battle)
                    if boss_group.sprite.breath == 1:
                        breath_group.add(Breath(boss_group.sprite.rect.bottomleft, boss_group.sprite.direction))
                    if boss_group.sprite.callminion == 1:
                        warlock_group.add(Warlock((500,500)))
                        skeleton_group.add(Skeleton_red((400, 400)))
                        skeleton_group.add(Skeleton_blue((400, 600)))
                        skeleton_group.add(Skeleton_red((700, 500)))
            warlock_group.draw(surface)
            bullet_group.draw(surface)
            fire_effect.draw(surface)
            avatar_group.draw(surface)
            skeleton_group.draw(surface)
            game.draw(surface)
            if aimopen:
                pygame.draw.circle(surface,(255,0,0),pygame.mouse.get_pos(),20,5)
            if controls['click'] and aimopen and meteor_ready:
                count = time.time()
                meteor = Meteor(controls['click'])
                meteor_group.add(meteor)
                aimopen = False
            if len(breath_group) > 0:
                magic_collision(breath_group.sprite, avatar_group, skeleton_group, warlock_group)
            if len(meteor_group) > 0:
                magic_collision(meteor_group.sprite, skeleton_group, warlock_group, boss_group)
            meteor_group.update()
            meteor_group.draw(surface)
            boss_group.draw(surface)
            breath_group.draw(surface)
        pygame.display.flip()


def draw_meteor_icon(count, surface):
    now = time.time()
    pygame.draw.circle(surface, (0,0,0), (50,50), 40)
    image = pygame.Surface((64, 64))
    if now - count >= 2 and now - count < 3.6:
        pygame.draw.circle(surface, (255,255,255), (50,50), 6)
    elif now - count >= 3.6 and now - count < 5.2:
        pygame.draw.circle(surface, (255,255,255), (50,50), 12)
    elif now - count >= 5.2 and now - count < 6.8:
        pygame.draw.circle(surface, (255,255,255), (50,50), 18)
    elif now - count >= 6.8 and now - count < 8.4:
        pygame.draw.circle(surface, (255,255,255), (50,50), 24)
    elif now - count >= 8.4 and now - count < 10:
        pygame.draw.circle(surface, (255,255,255), (50,50), 30)
    elif now - count >= 10:
        pygame.draw.circle(surface, (255,255,255), (50,50), 36)
    if now - count > 10:
        image_surf = pygame.image.load('assets/imgs/meteor.png').convert()
        image.blit(image_surf, (0,0))
        image.set_colorkey((0, 0, 0))
        rect = image_surf.get_rect(center=(50,50))
        surface.blit(image, rect)
        return True
    return False

def draw_skill_icon(surface):
    pygame.draw.circle(surface, (0,0,0), (50,50), 40)
    pygame.draw.circle(surface, (255,255,255), (50,50), 36)

def magic_collision(magic, group1, group2, group3):
    collision = pygame.sprite.spritecollide(magic, group1, dokill=False, collided=pygame.sprite.collide_rect)
    magic.update_collision(collision)
    collision = pygame.sprite.spritecollide(magic, group2, dokill=False, collided=pygame.sprite.collide_rect)
    magic.update_collision(collision)
    collision = pygame.sprite.spritecollide(magic, group3, dokill=False, collided=pygame.sprite.collide_rect)
    magic.update_collision(collision)

def draw_health_bar(hero, surface):
    font = setup_fonts(24)
    max_width = 240
    width = hero.hp/hero.maxHp * 240
    number = str(int(hero.hp)) + '/' + str(hero.maxHp)
    height = 30
    number_pos = (110 + max_width, 50)
    number_rect = hero.image.get_rect(topleft=number_pos)
    number_surface = font.render(number, True, (255, 255, 255))
    base_bar_rect = pygame.Rect(110, 53, max_width, height)
    bar_rect = pygame.Rect(110, 53, width, height)
    base_color = (120, 120, 120)
    color = (255,0,0)
    pygame.draw.rect(surface, base_color, base_bar_rect)
    pygame.draw.rect(surface, color, bar_rect)
    pygame.draw.rect(surface, (0,0,0), base_bar_rect, 2)
    surface.blit(number_surface, number_rect)

def draw_boss_heath_bar(boss, surface):
    x = boss.rect.x
    y = boss.rect.y - 30
    max_width = 160
    width = boss.hp/boss.maxHp * 160
    height = 15
    base_bar_rect = pygame.Rect(x, y, max_width, height)
    bar_rect = pygame.Rect(x, y, width, height)
    base_color = (120, 120, 120)
    color = (255,0,0)
    pygame.draw.rect(surface, base_color, base_bar_rect)
    pygame.draw.rect(surface, color, bar_rect)
    pygame.draw.rect(surface, (0,0,0), base_bar_rect, 1)

def setup_fonts(font_size, bold=False, italic=False):
    ''' Load a font, given a list of preferences

        The preference list is a sorted list of strings (should probably be a parameter),
        provided in a form from the FontBook list.
        Any available font that starts with the same letters (lowercased, spaces removed)
        as a font in the font_preferences list will be loaded.
        If no font can be found from the preferences list, the pygame default will be returned.

        returns -- A Font object
    '''
    font_preferences = ['Helvetica Neue', 'Iosevka Regular', 'Comic Sans', 'Courier New']
    available = pygame.font.get_fonts()
    prefs = [x.lower().replace(' ', '') for x in font_preferences]
    for pref in prefs:
        a = [x
             for x in available
             if x.startswith(pref)
            ]
        if a:
            fonts = ','.join(a) #SysFont expects a string with font names in it
            return pygame.font.SysFont(fonts, font_size, bold, italic)
    return pygame.font.SysFont(None, font_size, bold, italic)


if __name__ == "__main__":
    start_stage()