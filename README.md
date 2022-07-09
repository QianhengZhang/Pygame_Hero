# Medieval Knight Project

## Introduction


This is a Medieval knight game made by team1. You will play as a hero knight called Sir Gawaine and kill all the monsters in the dungeon.


## Setup

1. Required Packages: Pygame, Sympy, Numpy

2. Open the game.py and run it to start the game!

You will have to choose a difficulty level at the begining:

0 - A few numbers of monsters and easy maze

1 - Normal numbers of monsters and an AI driven maze

2 - A lot of monsters and a super AI enemy in the maze


## Control Guide:
### Battle:
WASD - Moving in fightings and maze

J - Melee attack

K - Block in your direction

WASD + J - Running attack

K+J - Block attack

E: Cast a meteor rain on the selected field. It will start as
a red circle until you click a spot

### Game Play:

P - Pause the game during the fight(not in maze)

R - Revive if you are dead, but it will decrease your score

Q - Quit the game whenever you want, but the game will not save your progress


## File List:
### View Layer
1. game.py - Controlling the start of the game and connections
between stages.
2. start_menu.py - The start menu, you can set up the difficulty
level and enter the game.
3. stage1.py - The first stage, there are some minions for you
to practice how to attack, block and dodge.
4. chase.py - The maze stage, you can use the portals to travel
between points and the goal is the green dot.
5. boss.py - The boss stage, careful with him. There are only few
chances to beat him!
6. result.py - After beating the boss, you can see your final score!

### Controller
7. controller.py - The controls for fighting stage.

### Model Layer
8. Model.py - Game manager, hero sprite class, monster classes,
and magic sprite.
9. mazes.py - The support file for chase stage.
10. show_maze.py - The support file for chase stage.

## Acknowledgement

Thanks for all the help from Professor William Nace and TA Shuo Wang.

All asstes all from internet:
1. https://itch.io/game-assets/free/tag-pixel-art
2. https://opengameart.org/
3. https://itch.io/game-assets/free
4. https://soundimage.org/puzzle-music/
5. https://mixkit.co/free-sound-effects/game/
6. https://www.zapsplat.com/sound-effect-category/game-sounds/

Our team members are Frank(Yijie) Shi, Jimmy(Yuehuan) Qiu, and Joshua(Qianheng) Zhang. Thank you for playing our game!