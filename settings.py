# This acts as a level map, if there is an X, there will be a surface there on our level
# If there is a P, it will represent the player
level_map = [
"                        ",
"                        ",
" XX    XXX         XX   ",
" XX P                   ",
" XXXX         XX     XX ",
" XXXX       XX          ",
" XX    X XXXX   XX XX   ",
"       X XXXXX  XX XXX  ",
"    XXXX XXXXXX XX XXXX ",
"XXXXXXXX XXXXXX XX XXXX ",
]

tile_size       = 64
# Since we will be having multiple files of code, having access to screen_width and
# screen_height will be easier later on compared to it being in main.py
screen_width    = 1200
screen_height   = len(level_map) * tile_size # This needs to be relative to our level map (columns by rows, 7x10)
