import pygame
from model import Hero

def main():
    global avatar
    pygame.init()
    window_size_x = 1050
    window_size_y = 700
    surface = pygame.display.set_mode([window_size_x,window_size_y])
    pygame.display.set_caption('Game')

    background = pygame.image.load('Run.png').convert()
    background = pygame. transform. scale(background, (window_size_x, window_size_y))
    avatar = Hero((60, 350))
    clock = pygame.time.Clock()

    while True:
        clock.tick(21)

        controls = check_events()
        if controls['quit']:
            break
        surface.blit(background, (0,0))
        avatar.update(controls)
        avatar.draw(surface)
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
        'down': False
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