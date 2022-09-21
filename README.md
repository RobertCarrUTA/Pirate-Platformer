*README.md and project still under construction*
# Pirate Platformer
![Alt text](https://github.com/RobertCarrUTA/Pirate-Platformer/blob/main/gif/pirate.gif)


## Table of Contents
- Pirate Platformer
  * [About](#about)
  * [Compile Instructions](#compile-instructions)
    * [Windows Compile Instructions](#windows-compile-instructions)
    * [Linux Compile Instructions](#linux-compile-instructions)
  * [Controls](#controls)

## About
This game is a Python-based pirate platformer using Pygame. The maps were map with [Tiled Map Editor](https://thorbjorn.itch.io/tiled). In addition to making maps quick and easy, Tile also made spawning the player and enemies much easier. In Tile, we can set the player's start and end points as well as set enemies' movement constraints. This simplifies enemy logic by only allowing enemies to move left or right until they reach a restricted tile. Once they reach the restricted tile, they turn and walk the other way. Collision detection does not need to be complicated with this approach.

**DO NOT ROTATE A TILE IN TILED WHEN CREATING A LEVEL**. I had to figure this out and it took a while among other things. If you find a fix, please let me know.


## Compile Instructions


### Windows Compile Instructions
You will need to have [Python](https://www.python.org/) installed on your machine. After this you will need to make sure you have [Pygame](https://www.pygame.org/wiki/GettingStarted) installed. On Windows you can enter the following commands into the terminal:
* To install [Pygame](https://www.pygame.org/wiki/GettingStarted): pip install pygame
* To run in src folder: python main.py


### Linux Compile Instructions
You will need to have [Python](https://www.python.org/) installed on your machine. After this you will need to make sure you have [Pygame](https://www.pygame.org/wiki/GettingStarted) installed. On Linux you can enter the following commands into the terminal:
* To install [Pygame](https://www.pygame.org/wiki/GettingStarted): sudo apt-get install python3-pygame
* To run in src folder: python3 main.py


## Controls


### Player Controls
* Move left: Left Arrow
* Move right: Right Arrow
* Jump: Up Arrow


### Overworld Controls
*Overworld level 1 will cause a crash right now, and other levels past it will too beause they are level 1*
* Move to next level: Right Arrow
* Move to previous level: Left Arrow
* Enter Level: Space
