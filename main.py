import pygame
from model import Knight

def main():
    global avatar
    pygame.init()
    window_size_x = 1200
    window_size_y = 950
    surface = pygame.display.set_mode([window_size_x,window_size_y])
    pygame.display.set_caption('Arena Game')

    background = pygame.image.load('assets/imgs/background/BG.png').convert()

    avatar = Knight((100, 700))
    clock = pygame.time.Clock()

    while True:
        clock.tick(60)

        quit, left, right, click = check_events()
        if quit:
            break

        avatar.update(click, left, right)

        surface.blit(background, (0,0))
        avatar.draw(surface)
        pygame.display.flip()


def check_events():
    ''' A controller of sorts.  Looks for Quit, arrow type events.  Space initiates a jump.
    '''
    quit = False
    click = None
    left = False
    right = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                quit = True
            if event.key == pygame.K_ESCAPE:
                quit = True
            if event.key == pygame.K_a:
                left = True
            if event.key == pygame.K_d:
                right = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                left = False
            if event.key == pygame.K_d:
                right = False
        if event.type == pygame.MOUSEBUTTONUP:
                click = event.pos
    if right and left:
        right = False
        left = False

    return (quit, left, right, click)


if __name__ == "__main__":
    main()