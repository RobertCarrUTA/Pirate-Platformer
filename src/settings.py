# This acts as a level map, if there is an X, there will be a surface there on our level
# If there is a P, it will represent the player
level_map = [
"                          ",
"                          ",
" XX    XXX         XX     ",
" XX P                     ",
" XXXX        XXX     XX   ",
" XXXX       XX            ",
" XX    X  XXXX    XX XX   ",
"       X  XXXXX   XX XXX  ",
"    XXXX  XXXXXX  XX XXXX ",
"XXXXXXXX  XXXXXX  XX XXXX ",
]

vertical_tile_number = 11
tile_size            = 64
screen_height        = vertical_tile_number * tile_size # This needs to be relative to our level map (columns by rows, 7x10)
screen_width         = 1200

