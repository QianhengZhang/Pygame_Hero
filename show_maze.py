#! /usr/bin/env python3
''' Show off mazes and their algorithms. '''
import pygame
import pygame.gfxdraw
from pygame.locals import *
import mazes

def show_maze():
    markup = None
    g = mazes.Grid(24,32)
    mazes.aldous_broder(g)
    return g, markup
        

def display_grid(g, markup, screen, avatar_x, avatar_y, destination_x, destination_y, enemies):
    for row in range(g.num_rows):
        for col in range(g.num_columns):
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
            
