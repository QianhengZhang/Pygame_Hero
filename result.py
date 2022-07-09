import pygame
from model import TextBox
import sys
def show_result(game):
    pygame.init()
    surface = pygame.display.set_mode([1034,778])
    pop = TextBox(surface)
    result = ['You won!',
              'Thank you for playing our game',
              f'Your score is: ' + str(int(game.score - 200 * game.revive_number + (120-game.maze_time) * 30 + 1000)),
              'Congradulations!',
              'Press Q to Quit']
    pop.image_surf = pygame. transform. scale(pop.img2, (1034, 778))
    pop.pop_up(result)
    game.background_channel.play(game.mix5, -1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()
            else:
                pygame.display.update()


if __name__ == "__main__":
    show_result()