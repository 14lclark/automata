# Cellular Automata

A terminal based cellular automata simulator written in Python. 

## Game of Life

To play the Game of Life, run game_of_life.py. Currently, the initial state must be given using the coordinates. 
I plan to add input of a state using a text file with 0s and 1s or the LifeViewer notation.

Wouldn't be too hard to change this code to work for the different Life-like games.

## Visualizer

Use the numpad or arrow keys to navigate (corner keys on numpad move diagonally). Use p to toggle pause, q to exit,
+/- to increase or decrease speed, and = to return to the default speed.

I think I'm going to split the visualization stuff off into its own project at some point as well. 


# Plans

* Different Life-like rulesets.
* Split visualization into separate project.
  - Jump to coordinates with input.
  - Change curses rendering to only update changes, not re-print entire screen. (Does curses already do this?)
  - Colors with curses.
  - Non-terminal rendering?
  - 3D rendering?
