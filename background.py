# Background
import pygame

def main():
    pygame.init()
    window_size_x = 1200
    window_size_y = 622
    surface = pygame.display.set_mode([window_size_x,window_size_y])
    pygame.display.set_caption('Background Image')
    background = pygame.image.load('Run.png').convert()
    background = pygame. transform. scale(background, (window_size_x, window_size_y))
    surface.blit(background, (0,0))

    while True:
        quit= check_events()
        if quit:
            break
        pygame.display.flip()

def check_events():
    ''' A controller of sorts.  Looks for Quit, several simple events.
        Returns: True/False for if a Quit event happened.
    '''

    quit = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                quit = True
            if event.key == pygame.K_ESCAPE:
                quit = True

    return quit

if __name__ == "__main__":
    main()