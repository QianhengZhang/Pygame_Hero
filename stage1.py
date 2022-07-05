import pygame
import start_menu
from controller import check_events
from model import Hero, Skeleton_blue, TextBox, Skeleton_red, GameManager, Warlock, Warlock_bullet, Fire, Portal, Meteor, Boss_icon
import random
import time

def start_stage(game):
    pygame.init()
    window_size_x = 1034
    window_size_y = 778
    surface = pygame.display.set_mode([window_size_x,window_size_y])
    suggestions = ['Using WASD to move!', 'J is attack and K is block!', 'Be careful with the magic attack!']
    pygame.display.set_caption('Game')
    background = pygame.image.load('assets/imgs/Battleground2.png').convert()
    background = pygame. transform. scale(background, (window_size_x, window_size_y))
    avatar_group = pygame.sprite.GroupSingle()
    avatar = Hero((100, 500))
    avatar_group.add(avatar)
    skeleton_group = pygame.sprite.Group()
    warlock_group = pygame.sprite.Group()
    bullet_group = pygame.sprite.Group()
    fire_effect = pygame.sprite.Group()
    meteor_group = pygame.sprite.Group()
    count = time.time()
    meteor_ready = False
    aimopen = False
    skeleton = Skeleton_red((300, 400))
    skeleton_group.add(skeleton)
    skeleton = Skeleton_red((350, 550))
    skeleton_group.add(skeleton)
    skeleton = Skeleton_blue((300, 700))
    skeleton_group.add(skeleton)
    warlock_group.add(Warlock((450, 550)))
    pop = TextBox(surface)
    clock = pygame.time.Clock()
    state = 'running'
    demon_group = pygame.sprite.GroupSingle()
    demon_group.add(Boss_icon((800, 20)))
    portal_group = pygame.sprite.GroupSingle()
    portal_group.add(Portal((500, 500)))

    if game.difficulty == 0:
        max_skeleton = 3
        max_warlock = 1
        score_requirement = 400
    elif game.difficulty == 1:
        max_skeleton = 4
        max_warlock = 2
        score_requirement = 500
    else:
        max_skeleton = 5
        max_warlock = 3
        score_requirement = 600

    while True:
        clock.tick(18)

        controls = check_events()
        if controls['quit']:
            game.next = False
            break
        elif (game.score >= score_requirement and len(portal_group) == 0):
            game.next = True
            break
        if controls['reborn'] and len(avatar_group) == 0:
            avatar_group.add(Hero((100, 400)))
        if len(avatar_group) == 0 and state != 'pause':
            controls['pop'] = True
        if controls['pop']:
            state = pop.update(controls)
            index = random.randint(0, len(suggestions)-1)
        if controls['aimchange'] and meteor_ready:
            aimopen = not aimopen

        if game.score >= score_requirement and len(skeleton_group) == 0 and len(warlock_group) == 0:
            portal_group.update()
            if len(portal_group) > 0 and len(avatar_group) > 0:
                teleport = pygame.sprite.spritecollide(portal_group.sprite, avatar_group, dokill=False, collided=pygame.sprite.collide_mask)
                if len(teleport) > 0:
                    portal_collision(teleport, portal_group.sprite)
                    game.state = 'done'
        if state == 'pause' and game.state == 'running':
            if len(avatar_group) == 0:
                score = str(game.score)
                pop.pop_up(['You are dead', 'Current Score is ' + score,'Press R to rejoin the fight!'])
            else:
                pop.pop_up(['Notes:', 'Press Q to quit', 'Press P to resume the game!', suggestions[index]])
        else:
            if game.score < score_requirement and (len(skeleton_group) < max_skeleton or len(warlock_group) < max_warlock):
                position_x = random.randint(600, 800)
                position_y = random.randint(350, 550)
                chance = random.randint(1,100)
                if chance > 0 and chance <= 70 and len(skeleton_group) < max_skeleton:
                    skeleton_group.add(random.choice([Skeleton_red((position_x, position_y)), Skeleton_blue((position_x, position_y))]))
                elif chance > 70 and chance <= 100 and len(warlock_group) < max_warlock:
                    warlock_group.add(Warlock((position_x, position_y)))
            surface.blit(background, (0,0))
            avatar_group.update(controls)
            bullet_group.update()
            fire_effect.update()
            demon_group.update()
            if len(avatar_group) > 0:
                if len(skeleton_group) > 0:
                    battle = pygame.sprite.spritecollide(avatar_group.sprite, skeleton_group, dokill=False, collided=pygame.sprite.collide_mask)
                    avatar_group.sprite.update_collision(battle)
                if len(warlock_group) > 0:
                    battle = pygame.sprite.spritecollide(avatar_group.sprite, warlock_group, dokill=False, collided=pygame.sprite.collide_mask)
                    avatar_group.sprite.update_collision(battle)
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
            warlock_group.draw(surface)
            bullet_group.draw(surface)
            fire_effect.draw(surface)
            portal_group.draw(surface)
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
            meteor_group.update()
            meteor_group.draw(surface)
            demon_group.draw(surface)
        pygame.display.flip()

def portal_collision(teleport, portal):
    for hero in teleport:
        hero.kill()
    portal.status = 'close'

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
        image_surf = pygame.image.load('meteor.png').convert()
        image.blit(image_surf, (0,0))
        image.set_colorkey((0, 0, 0))
        rect = image_surf.get_rect(center=(50,50))
        surface.blit(image, rect)
        return True
    return False

def draw_skill_icon(surface):
    pygame.draw.circle(surface, (0,0,0), (50,50), 40)

def group_update(avatar, groups, control):
    avatar.update(control)
    for group in groups:
        group.update()

def group_draw(groups, surface):
    for group in groups:
        group.draw(surface)

def draw_health_bar(hero, surface):
    font = setup_fonts(24)
    max_width = 240
    width = hero.hp/hero.maxHp * 240
    number = str(int(hero.hp)) + '/' + str(hero.maxHp)
    height = 30
    text_pos = (750, 50)
    text_rect = hero.image.get_rect(topleft=text_pos)
    number_pos = (110 + max_width, 50)
    number_rect = hero.image.get_rect(topleft=number_pos)
    #text_surface = font.render('HP:', True, (255, 255, 255))
    number_surface = font.render(number, True, (255, 255, 255))
    base_bar_rect = pygame.Rect(110, 53, max_width, height)
    bar_rect = pygame.Rect(110, 53, width, height)
    base_color = (120, 120, 120)
    color = (255,0,0)
    #surface.blit(text_surface, text_rect)
    pygame.draw.rect(surface, base_color, base_bar_rect)
    pygame.draw.rect(surface, color, bar_rect)
    pygame.draw.rect(surface, (0,0,0), base_bar_rect, 2)
    surface.blit(number_surface, number_rect)

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