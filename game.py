import pygame
import start_menu
import stage1
import chase
from model import GameManager

def main():
	game = GameManager()

	start_page = True
	while start_page:
		start_page = start_menu.start_menu()
		start_menu.get_difficulty(game)
	stage = True
	print(game.difficulty)
	while stage:
		stage = stage1.start_stage(game)
		chase_stage = game.next

	while chase_stage:
  		chase_stage = chase.start_chase(game)

if __name__ == "__main__":
    main()