from cProfile import run
from numpy import True_
import mazes
import pygame
import show_maze
import random

pygame.init()
clock = pygame.time.Clock()
screen_width = 1070
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("The Medieval Knight Game!")

background = pygame.image.load("Run.png")
background = pygame.transform.scale(background, (1070, 720))

def update_enemy(maze, enemies):
    valid = False
    new_enemies = list()
    counter = 0
    for enemy in enemies:
        currentCell = maze.cell_at(enemy[0], enemy[1])
        while not valid:
            if (counter > 10):
                new_enemies.append(enemy)
                break
            direction = random.randint(0, 3)
            # north
            if (direction == 0 and currentCell.north != None and currentCell.is_linked(currentCell.north) and ((enemy[0] - 1, enemy[1]) not in new_enemies) and ((enemy[0] - 1, enemy[1]) not in enemies)):
                valid = True
                new_enemies.append((enemy[0] - 1, enemy[1]))
            # south
            elif (direction == 1 and currentCell.south != None and currentCell.is_linked(currentCell.south) and ((enemy[0] + 1, enemy[1]) not in new_enemies) and ((enemy[0] - 1, enemy[1]) not in enemies)):
                valid = True
                new_enemies.append((enemy[0] + 1, enemy[1]))
            # west
            elif (direction == 2 and currentCell.west != None and currentCell.is_linked(currentCell.west) and ((enemy[0], enemy[1] - 1) not in new_enemies) and ((enemy[0] - 1, enemy[1]) not in enemies)):
                valid = True
                new_enemies.append((enemy[0], enemy[1] - 1))
            # east
            elif (direction == 3 and currentCell.east != None and currentCell.is_linked(currentCell.east) and ((enemy[0], enemy[1] + 1) not in new_enemies) and ((enemy[0] - 1, enemy[1]) not in enemies)):
                valid = True
                new_enemies.append((enemy[0], enemy[1] + 1))
            counter += 1
        counter = 0

        valid = False
    return new_enemies


if __name__ == "__main__":
    screen = pygame.display.set_mode([1034,778])
    maze, markup = show_maze.show_maze()
    running = True
    pygame.init()

    # Initial position for the player
    (init_x, init_y) = (random.randrange(0, 24), random.randrange(0, 32))
    (avatar_x, avatar_y) = (init_x, init_y)

    # Determine the destination
    determinator = mazes.DijkstraMarkup(maze, maze.cell_at(init_x, init_y))
    destination = determinator.farthest_cell()[0]
    (destination_x, destination_y) = (destination.row, destination.column)

    # Create a bunch of enemies
    enemies = list()
    counter = 0
    num_enemies = 8
    while counter < num_enemies:
        (enemy_x, enemy_y) = (random.randrange(0, 24), random.randrange(0, 32))
        if not ((enemy_x == init_x and enemy_y == init_y) or ((enemy_x, enemy_y) in enemies)):
            enemies.append((enemy_x, enemy_y))
            counter += 1

    update_enemy_countdown = 100

    while running:
        update_enemy_countdown -= 1
        currentCell = maze.cell_at(avatar_x, avatar_y)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_q:  # Quit
                    running = False
                elif event.key == pygame.K_a:  # Move to the left
                    if currentCell.west != None:
                        if currentCell.is_linked(currentCell.west):
                            avatar_y -= 1
                elif event.key == pygame.K_d:  # Move to the right
                    if currentCell.east != None:
                        if currentCell.is_linked(currentCell.east):
                            avatar_y += 1
                elif event.key == pygame.K_w:  # Move up
                    if currentCell.north != None:
                        if currentCell.is_linked(currentCell.north):
                            avatar_x -= 1
                elif event.key == pygame.K_s:  # Move down
                    if currentCell.south != None:
                        if currentCell.is_linked(currentCell.south):
                            avatar_x += 1
                            
        if (avatar_x == destination_x and avatar_y == destination_y):
            running = False
            # Connect with the next page.
            # Implement me!!! Print "You win" for now
            print("You win!")

        if (update_enemy_countdown == 0):
            enemies = update_enemy(maze, enemies)
            update_enemy_countdown = 100

        if ((avatar_x, avatar_y) in enemies):
            running = False
            print("You ran into enemies!! Try again.")
        
        screen.blit(background, (0, 0))
        show_maze.display_grid(maze, markup, screen, avatar_x, avatar_y, destination_x, destination_y, enemies)
        pygame.display.flip()