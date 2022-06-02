import pygame
from model import HealthBar, Hero, Tester

def main():
    global avatar
    pygame.init()
    window_size_x = 800
    window_size_y = 600
    surface = pygame.display.set_mode([window_size_x,window_size_y])
    pygame.display.set_caption('Game')

    background = pygame.image.load('assets/imgs/Battleground2.png').convert()
    background = pygame. transform. scale(background, (window_size_x, window_size_y))
    avatar_group = pygame.sprite.GroupSingle()
    avatar = Hero((100, 400))
    avatar_group.add(avatar)
    test_group = pygame.sprite.Group()
    tester = Tester((550, 450))
    test_group.add(tester)
    clock = pygame.time.Clock()

    while True:
        clock.tick(21)

        controls = check_events()
        if controls['quit']:
            break
        elif controls['reborn']:
            avatar_group.add(Hero((300, 300)))
        elif controls['click']:
            test_group.add(Tester(controls['click']))
        surface.blit(background, (0,0))
        avatar_group.update(controls)
        if len(avatar_group) > 0 and len(test_group) > 0:
            battle = pygame.sprite.spritecollide(avatar_group.sprite, test_group, dokill=False, collided=pygame.sprite.collide_mask)
            avatar_group.sprite.update_collisiton(battle)
        test_group.update()
        healthBar = HealthBar(avatar_group.sprite)
        healthBar.draw(surface)
        avatar_group.draw(surface)
        test_group.draw(surface)
        pygame.display.flip()


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
        'click': None
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
    main()