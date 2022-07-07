import sys
#from black import diff
import pygame
from datetime import date
import shelve # part of the standard library
from pygame import mixer

# Fix me after integration!
global difficulty
difficulty = 1

pygame.init()
clock = pygame.time.Clock()
screen_width = 1034
screen_height = 778
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("The Medieval Knight Game!")

# Initialize constants
font = pygame.font.SysFont("comicsansms", 30)
smallfont = pygame.font.SysFont("comicsansms", 14)
bigfont = pygame.font.SysFont("comicsansms", 70)
slategrey = (112, 128, 144)
lightgrey = (165, 175, 185)
blackish = (10, 10, 10)
white = (255, 255, 255)
black = (0, 0, 0)

background = pygame.image.load("menu_background.png")
background = pygame.transform.scale(background, (1034, 778))


# Function to create a button
def create_button(x, y, width, height, hovercolor, defaultcolor):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed(3)
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, hovercolor, (x, y, width, height))
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(screen, defaultcolor, (x, y, width, height))

def create_difficulty_button(x, y, width, height, hovercolor, defaultcolor):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed(3)
    global difficulty
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, hovercolor, (x, y, width, height))
        if click[0] == 1:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    if difficulty == 0:
                        difficulty = 1
                    elif difficulty == 1:
                        difficulty = 2
                    else:
                        difficulty = 0
                    return True
    else:
        pygame.draw.rect(screen, defaultcolor, (x, y, width, height))

# Start menu returns true until we click the Start button
def start_menu(game):
    startText = font.render("Medieval Knight", True, slategrey)
    today = date.today()
    todayText = "Today is " + today.strftime("%A") + ", " + today.strftime("%B") + " " + today.strftime("%d") + \
                ", " + today.strftime("%Y")
    todayText = smallfont.render(todayText, True, slategrey)
    while True:
        screen.fill((0, 0, 0))
        screen.blit(todayText, (5, 10))
        screen.blit(startText, ((screen_width - startText.get_width()) / 2, 0))

        # start button (left, top, width, height)
        start_button = create_button(screen_width - 130, 7, 125, 26, lightgrey, slategrey)

        # difficulty button
        difficulty_button = create_difficulty_button(screen_width - 260 , 7, 125, 26, lightgrey, slategrey)
        difficulty_button_text = smallfont.render("Difficulty: " + str(difficulty), True, blackish)
        screen.blit(difficulty_button_text, (screen_width - 260, 9))

        if start_button:
           return False

        # Start button text
        startbuttontext = smallfont.render("Start the Game!", True, blackish)
        screen.blit(startbuttontext, (screen_width - 125, 9))

        # Displays the background picture
        screen.blit(background, (1, 40))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(15)
        return True

def get_difficulty(game):
    game.difficulty = difficulty

if __name__ == "__main__":
    while True:
        start_menu()