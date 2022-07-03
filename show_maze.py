#! /usr/bin/env python3
''' Show off mazes and their algorithms. '''
import pygame
import pygame.gfxdraw
from pygame.locals import *
import mazes

portal1 = pygame.image.load("images.png")
portal1 = pygame.transform.scale(portal1, (1034 / 32, 778 / 24))
portal2 = pygame.image.load("portal.png")
portal2 = pygame.transform.scale(portal2, (1034 / 32, 778 / 24))

def show_maze():
    markup = None
    g = mazes.Grid(24,32)
    mazes.aldous_broder(g)
    return g, markup


def display_grid(g, markup, screen, avatar_x, avatar_y, destination_x, destination_y, enemies, portals):
    for row in range(g.num_rows):
        for col in range(g.num_columns):
            counter = 0
            c = g.cell_at(row, col)
            cell_x = col * 32 + 5
            cell_y = row * 32 + 5
            if (row, col) in enemies:
                pygame.draw.circle(screen,
                                    (255, 0, 0),
                                    (cell_x+15,cell_y+15),
                                    7,  #radius
                                    0)  #filled
            if row == avatar_x and col == avatar_y:
                counter += 1
                pygame.draw.circle(screen,
                                    (0, 0, 255),
                                    (cell_x+15,cell_y+15),
                                    7,  #radius
                                    0)  #filled
            if row == destination_x and col == destination_y:
                pygame.draw.circle(screen,
                                    (0, 255, 0),
                                    (cell_x+15,cell_y+15),
                                    7,  #radius
                                    0)  #filled
            if (row == portals[0][0].row and col == portals[0][0].column) or (row == portals[0][1].row and col == portals[0][1].column):
                screen.blit(portal1, (cell_x, cell_y))

            if (row == portals[1][0].row and col == portals[1][0].column) or (row == portals[1][1].row and col == portals[1][1].column):
                screen.blit(portal2, (cell_x, cell_y))

            if not c.north or not c.is_linked(c.north):
                pygame.gfxdraw.hline(screen,
                                     cell_x, cell_x+31, cell_y,
                                     (100,100,100))
            if not c.south or not c.is_linked(c.south):
                pygame.gfxdraw.hline(screen,
                                     cell_x, cell_x+31, cell_y+31,
                                     (100,100,100))
            if not c.east or not c.is_linked(c.east):
                pygame.gfxdraw.vline(screen,
                                     cell_x+31, cell_y, cell_y+31,
                                     (100,100,100))
            if not c.west or not c.is_linked(c.west):
                pygame.gfxdraw.vline(screen,
                                     cell_x, cell_y, cell_y+31,
                                     (100,100,100))
            print(counter)