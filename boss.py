import pygame
from model import Hero, Tester, TextBox, Skeleton_red, GameManager, Warlock, Warlock_bullet, Fire, Portal, Meteor, Boss, Breath
import random
import time

def start_stage():
    pygame.init()
    window_size_x = 1080
    window_size_y = 720
    surface = pygame.display.set_mode([window_size_x,window_size_y])
    suggestions = ['Using WASD to move!', 'J is attack and K is block!', 'Be careful with the magic attack!']
    pygame.display.set_caption('Game')
    background = pygame.image.load('assets/imgs/Battleground.png').convert()
    background = pygame. transform. scale(background, (window_size_x, window_size_y))
    avatar_group = pygame.sprite.GroupSingle()
    avatar = Hero((100, 500))
    avatar_group.add(avatar)
    test_group = pygame.sprite.Group()
    warlock_group = pygame.sprite.Group()
    bullet_group = pygame.sprite.Group()
    fire_effect = pygame.sprite.Group()
    meteor_group = pygame.sprite.Group()
    breath_group = pygame.sprite.Group()
    count = time.time()
    meteor_ready = False
    aimopen = False
    pop = TextBox(surface)
    clock = pygame.time.Clock()
    state = 'running'
    boss_group = pygame.sprite.GroupSingle()
    boss_group.add(Boss((500, 200)))
    game = GameManager()
    if game.difficulty == 0:
        max_skeleton = 2
        max_warlock = 1
        score_requirement = 300
    elif game.difficulty == 1:
        max_skeleton = 3
        max_warlock = 1
        score_requirement = 400
    else:
        max_skeleton = 3
        max_warlock = 2
        score_requirement = 500

    while True:
        clock.tick(18)

        controls = check_events()
        if controls['quit']:
            game.next = False
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
        if state == 'pause' and game.state == 'running':
            if len(avatar_group) == 0:
                score = str(game.score)
                pop.pop_up(['You are dead', 'Current Score is ' + score,'Press R to rejoin the fight!'])
            else:
                pop.pop_up(['Notes:', 'Press Q to quit', 'Press P to resume the game!', suggestions[index]])
        else:
            if controls['click']:
                print(controls['click'])
            surface.blit(background, (0,0))
            avatar_group.update(controls)
            bullet_group.update()
            fire_effect.update()
            boss_group.update(avatar_group.sprite.rect.center)
            breath_group.update()
            if len(avatar_group) > 0 and len(test_group) > 0:
                battle = pygame.sprite.spritecollide(avatar_group.sprite, test_group, dokill=False, collided=pygame.sprite.collide_mask)
                avatar_group.sprite.update_collision(battle)
            if len(avatar_group) > 0 and len(warlock_group) > 0:
                battle = pygame.sprite.spritecollide(avatar_group.sprite, warlock_group, dokill=False, collided=pygame.sprite.collide_mask)
                avatar_group.sprite.update_collision(battle)
                for warlock_sprite in warlock_group.sprites():
                    if warlock_sprite.fire == 1:
                        bullet_group.add(Warlock_bullet((warlock_sprite.rect.center[0] + 15 * warlock_sprite.direction, warlock_sprite.rect.center[1] - 30),-(warlock_sprite.direction)))
                    if warlock_sprite.cast == 1:
                        fire_effect.add(Fire(avatar_group.sprite.rect.move(15,0).topleft))
            if len(avatar_group) > 0:
                if len(bullet_group) > 0:
                    battle = pygame.sprite.spritecollide(avatar_group.sprite, bullet_group, dokill=False, collided=pygame.sprite.collide_mask)
                    avatar_group.sprite.update_bullet_collision(battle)
                if len(fire_effect) > 0:
                    battle = pygame.sprite.spritecollide(avatar_group.sprite, fire_effect, dokill=False, collided=pygame.sprite.collide_mask)
                    avatar_group.sprite.update_bullet_collision(battle)
                test_group.update(avatar_group.sprite.rect.center, game)
                warlock_group.update(avatar_group.sprite.rect.center, game)
                draw_health_bar(avatar_group.sprite, surface)
                meteor_ready = draw_meteor_icon(count, surface)
                if boss_group.sprite.breath == 1:
                    breath_group.add(Breath(boss_group.sprite.rect.bottomleft, boss_group.sprite.direction))
                if boss_group.sprite.callminion == 1:
                    warlock_group.add(Warlock((500,500)))
            warlock_group.draw(surface)
            bullet_group.draw(surface)
            fire_effect.draw(surface)
            avatar_group.draw(surface)
            test_group.draw(surface)
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
        image_surf = pygame.image.load('meteor.png').convert()
        image.blit(image_surf, (0,0))
        image.set_colorkey((0, 0, 0))
        rect = image_surf.get_rect(center=(50,50))
        surface.blit(image, rect)
        return True
    return False

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

def check_events():
    ''' A controller of sorts.  Looks for Quit, arrow type events.  Space initiates a jump.
    '''
    controls = {
        'quit' : False,
        'left' : False,
        'right' : False,
        'attack': False,
        'block': False,
        'up': False,
        'down': False,
        'reborn': False,
        'click': None,
        'pop': False,
        'close': False,
        'aimchange': False
    }

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            controls['quit'] = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                controls['quit'] = True
            if event.key == pygame.K_ESCAPE:
                controls['quit'] = True
            if event.key == pygame.K_SPACE:
                controls['jump'] = True
            if event.key == pygame.K_j:
                controls['attack'] = True
            if event.key == pygame.K_r:
                controls['reborn'] = True
            if event.key == pygame.K_e:
                controls['aimchange'] = True
            if event.key == pygame.K_p:
                controls['pop'] = True
            if event.key == pygame.K_0:
                controls['close'] = True
        if event.type == pygame.MOUSEBUTTONDOWN:
                controls['click'] = event.pos
        if event.type == pygame.KEYUP:
            pass
    key_pressed = pygame.key.get_pressed()
    if key_pressed[pygame.K_a]:
        controls['left'] = True
    else:
        controls['left'] = False
    if key_pressed[pygame.K_d]:
        controls['right'] = True
    else:
        controls['right'] = False
    if key_pressed[pygame.K_w]:
        controls['up'] = True
    else:
        controls['up'] = False
    if key_pressed[pygame.K_s]:
        controls['down'] = True
    else:
        controls['down'] = False

    if key_pressed[pygame.K_k]:
        controls['block'] = True
        controls['left'] = False
        controls['right'] = False
        controls['up'] = False
        controls['down'] = False
    if controls['left'] and controls['right']:
        controls['left'] = False
        controls['right'] = False
    if controls['up'] and controls['down']:
        controls['up'] = False
        controls['down'] = False
    return controls



if __name__ == "__main__":
    start_stage()