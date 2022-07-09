#! /usr/bin/env python3
''' Show off mazes and their algorithms. '''
import pygame
import pygame.gfxdraw
from pygame.locals import *
import mazes
from model import Skeleton_blue

portal1 = pygame.image.load("assets/imgs/portal1.png")
portal1 = pygame.transform.scale(portal1, (int(1034 / 32), int(778 / 24)))
portal2 = pygame.image.load("assets/imgs/portal2.png")
portal2 = pygame.transform.scale(portal2, (int(1034 / 32), int(778 / 24)))

def show_maze():
    markup = None
    g = mazes.Grid(24,32)
    mazes.aldous_broder(g)
    return g, markup

avatar = pygame.image.load('./assets/imgs/Sprites/HeroKnight/Idle/HeroKnight_Idle_0.png')
avatar = pygame.transform.scale(avatar, (int(1034 / 32), int(778 / 24)))

enemy = pygame.image.load("assets/imgs/enemy.png")
enemy = pygame.transform.scale(enemy, (int(1034 / 32), int(778 / 24)))

def display_grid(g, markup, screen, avatar_x, avatar_y, destination_x, destination_y, enemies, portals):
    for row in range(g.num_rows):
        for col in range(g.num_columns):
            c = g.cell_at(row, col)
            cell_x = col * 32 + 5
            cell_y = row * 32 + 5
            if (row, col) in enemies:
                screen.blit(enemy, (cell_x, cell_y))
            if row == avatar_x and col == avatar_y:
                screen.blit(avatar, (cell_x,cell_y))

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