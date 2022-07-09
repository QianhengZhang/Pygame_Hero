from cProfile import run
from numpy import True_
import mazes
import pygame
import show_maze
import random

pygame.init()
clock = pygame.time.Clock()
screen_width = 1034
screen_height = 778
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("The Medieval Knight Game!")

background = pygame.image.load("assets/imgs/maze_background.png")
background = pygame.transform.scale(background, (1034, 778))

# Probably need fixing after integration !!!
# Difficulty
difficulty = 1

def update_enemy_random(maze, enemies):
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

def update_enemy_AI(maze, enemies, avatar_x, avatar_y):
    new_enemies = list()
    avatar_cell = maze.cell_at(avatar_x, avatar_y)
    for enemy in enemies:
        current_enemy_cell = maze.cell_at(enemy[0], enemy[1])
        markup = mazes.ShortestPathMarkup(maze, current_enemy_cell, avatar_cell)
        if (current_enemy_cell.north != None and markup.marks[current_enemy_cell.north] == "*" and current_enemy_cell.is_linked(current_enemy_cell.north)):
            new_enemies.append((enemy[0] - 1, enemy[1]))
        elif (current_enemy_cell.south != None and markup.marks[current_enemy_cell.south] == "*" and current_enemy_cell.is_linked(current_enemy_cell.south)):
            new_enemies.append((enemy[0] + 1, enemy[1]))
        elif (current_enemy_cell.west != None and markup.marks[current_enemy_cell.west] == "*" and current_enemy_cell.is_linked(current_enemy_cell.west)):
            new_enemies.append((enemy[0], enemy[1] - 1))
        elif (current_enemy_cell.east != None and markup.marks[current_enemy_cell.east] == "*" and current_enemy_cell.is_linked(current_enemy_cell.east)):
            new_enemies.append((enemy[0], enemy[1] + 1))
    return new_enemies

def update_enemy_cheat(maze, enemies, avatar_x, avatar_y):
    new_enemies = list()
    avatar_cell = maze.cell_at(avatar_x, avatar_y)
    for enemy in enemies:
        current_enemy_cell = maze.cell_at(enemy[0], enemy[1])
        markup = mazes.ShortestPathMarkup(maze, current_enemy_cell, avatar_cell)
        if (current_enemy_cell.north != None and markup.marks[current_enemy_cell.north] == "*"):
            new_enemies.append((enemy[0] - 1, enemy[1]))
        elif (current_enemy_cell.south != None and markup.marks[current_enemy_cell.south] == "*"):
            new_enemies.append((enemy[0] + 1, enemy[1]))
        elif (current_enemy_cell.west != None and markup.marks[current_enemy_cell.west] == "*"):
            new_enemies.append((enemy[0], enemy[1] - 1))
        elif (current_enemy_cell.east != None and markup.marks[current_enemy_cell.east] == "*"):
            new_enemies.append((enemy[0], enemy[1] + 1))
    return new_enemies

def start_chase(game):
    game.background_channel.play(game.mix3, -1)
    screen = pygame.display.set_mode([1034,778])
    maze, markup = show_maze.show_maze()
    running = True
    pygame.init()
    difficulty = game.difficulty

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
    num_enemies = 1
    while counter < num_enemies:
        (enemy_x, enemy_y) = (random.randrange(0, 24), random.randrange(0, 32))
        if not ((enemy_x == init_x and enemy_y == init_y) or ((enemy_x, enemy_y) in enemies)):
            enemies.append((enemy_x, enemy_y))
            counter += 1

    # Create portals.
    deadends = maze.deadends()
    portals = list()
    for _ in range(2):
        portal = list()
        for _ in range(2):
            index = random.randrange(0, len(deadends))
            cell = deadends[index]
            portal.append(cell)
            deadends.remove(cell)
        portals.append(portal)

    # Portal positions
    portals_pos = list()
    for i in range(2):
        portal_pos = list()
        for j in range(2):
            portal_pos.append((portals[i][j].row, portals[i][j].column))
        portals_pos.append(portal_pos)

    update_enemy_countdown = 100
    just_teleported = False
    while running:
        update_enemy_countdown -= 1
        currentCell = maze.cell_at(avatar_x, avatar_y)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game.next = False
                break
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
            game.magic = True
            running = False
            # Connect with the next page.
            # Implement me!!! Print "You win" for now
            print("You have gained the meteor Magic!")

        if ((avatar_x, avatar_y) in enemies):
            running = False
            print("You failed to find the magic power!")

        if ((avatar_x, avatar_y) in portals_pos[0]) and not just_teleported:
            if (avatar_x, avatar_y) == portals_pos[0][0]:
                (avatar_x, avatar_y) = portals_pos[0][1]
            else:
                (avatar_x, avatar_y) = portals_pos[0][0]
            just_teleported = True


        if ((avatar_x, avatar_y) in portals_pos[1]) and not just_teleported:
            if (avatar_x, avatar_y) == portals_pos[1][0]:
                (avatar_x, avatar_y) = portals_pos[1][1]
            else:
                (avatar_x, avatar_y) = portals_pos[1][0]
            just_teleported = True

        if ((avatar_x, avatar_y) not in portals_pos[0] and (avatar_x, avatar_y) not in portals_pos[1]):
            just_teleported = False

        screen.blit(background, (0, 0))

        if (update_enemy_countdown == 0):
            if difficulty == 0:
                enemies = update_enemy_random(maze, enemies)
            elif difficulty == 1:
                enemies = update_enemy_AI(maze, enemies, avatar_x, avatar_y)
            elif difficulty == 2:
                enemies = update_enemy_cheat(maze, enemies, avatar_x, avatar_y)
            update_enemy_countdown = 100

        show_maze.display_grid(maze, markup, screen, avatar_x, avatar_y, destination_x, destination_y, enemies, portals)
        pygame.display.flip()

if __name__ == "__main__":
    start_chase()
