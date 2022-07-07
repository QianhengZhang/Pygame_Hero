import start_menu
import stage1
import chase
import boss
import time
import result
from model import GameManager

def main():
    game = GameManager()

    start_page = True
    while start_page:
        start_page = start_menu.start_menu(game)
        start_menu.get_difficulty(game)
    stage = True
    while stage:
        stage = stage1.start_stage(game)
        chase_stage = game.next

    start = time.time()
    while chase_stage:
        chase_stage = chase.start_chase(game)
        final_boss =  game.next
    game.maze_time = time.time() - start

    while final_boss:
        final_boss = boss.start_stage(game)
        score = game.next
    while score:
        score = result.show_result(game)
if __name__ == "__main__":
    main()