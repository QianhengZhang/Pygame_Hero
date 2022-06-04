import sys
import pygame
from datetime import date
import shelve # part of the standard library


pygame.init()
clock = pygame.time.Clock()
screen_width = 1070
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("The Financial Game")

# Initialize constants
font = pygame.font.SysFont("comicsansms", 30)
smallfont = pygame.font.SysFont("comicsansms", 14)
bigfont = pygame.font.SysFont("comicsansms", 70)
slategrey = (112, 128, 144)
lightgrey = (165, 175, 185)
blackish = (10, 10, 10)
white = (255, 255, 255)
black = (0, 0, 0)

background = pygame.image.load("Background.png")


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


# Start menu returns true until we click the Start button
def start_menu():
    startText = font.render("Medieval Knight", True, slategrey)
    welcomeText = font.render("Welcome!", True, (0, 255, 255))
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

        if start_button:
            print("Implement Me!")
            pygame.quit()

        # Start button text
        startbuttontext = smallfont.render("Start the Game!", True, blackish)
        screen.blit(startbuttontext, (screen_width - 125, 9))

        # Displays the board room picture
        screen.blit(background, (1, 40))
        screen.blit(welcomeText, ((screen_width - startText.get_width()) / 2, 100))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(15)
        return True


if __name__ == "__main__":
    while True:
        start_menu()