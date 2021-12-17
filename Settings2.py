#-----Colours-----
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)
magenta = (255,0,255)
cyan = (0,255,255)
orange = (255,165,0)
purple = (106,12,173)
grey = (106,106,106)
lightgrey = (209,209,209)
lime = (191,255,0)

#-----Display Constants-----
display_width = 640
display_height = 480
tile_size = 32
title = "Dungeon Escape"
FPS = 60
font_name = "ariel"

#-----Game Config-----
player_speed = 8
player_health = 50

#-----Sprite Constants-----
layer_player = 6
layer_npc = 5
layer_enemy = 5
layer_wizard = 3
layer_chest = 3
layer_door = 3
layer_coin = 3
layer_block = 2
layer_ground = 1

#-----Tile Maps-----

#Room 1 - Start
tilemap_room1 = [
    "BBBBBBBBBBBBBB*BBBBB",
    "B..................B",
    "B...C..............B",
    "B..................B",
    "B..................B",
    "B..................B",
    "B....P.............B",
    "B...............:..B",
    "B..................B",
    "BBBBBBBBBBBBBBBBBBBB"]


#Room 2 - Courtyard
tilemap_room2 = [
    "BBBBBBBBBBBBBB=BBBBB",
    "B..................B",
    "B......N...........B",
    "|..................B",
    "B..................B",
    "B...............W..B",
    "B....P.............-",
    "B..................B",
    "B..................B",
    "BBBBB*BBBBBBBBBBBBBB"]


#Room 3 - 3
tilemap_room3 = [
    "BBBBBBBBBBBBBB*BBBBB",
    "B.....N............B",
    "B...............W..B",
    "*..................B",
    "B..................B",
    "B..................B",
    "B....P.............B",
    "B...............C..B",
    "B..................B",
    "BBBBB*BBBBBBBBBBBBBB"]


#Room 4 - 4
tilemap_room4 = [
    "BBBBBBBBBBBBBBBBBBBB",
    "B..................B",
    "B..................B",
    "*..................B",
    "B..................B",
    "B..................B",
    "B.............P....*",
    "B..W...............B",
    "B..................B",
    "BBBBBBBBBBBBBBBBBBBB"]


#Room 5 - 5
tilemap_room5 = [
    "BBBBBBBBBBBBBB*BBBBB",
    "B..C...............B",
    "B..................B",
    "B..................B",
    "B..................B",
    "B..................B",
    "B....P.............*",
    "B..]...............B",
    "B..................B",
    "BBBBB*BBBBBBBBBBBBBB"]


#Room 6 - 6
tilemap_room6 = [
    "BBBBBBBBBBBBBB*BBBBB",
    "B...............W..B",
    "B....N.............B",
    "B..................B",
    "B..................B",
    "B..................B",
    "B....P.............B",
    "B..............2...B",
    "B..................B",
    "BBBBBBBBBBBBBBBBBBBB"]


#Room 7 - Vault
tilemap_room7 = [
    "BBBBBBBBBBBBBBBBBBBB",
    "B..................B",
    "B..................B",
    "*...............1..B",
    "B..................B",
    "B..................B",
    "B....P.............B",
    "B..................B",
    "B..................B",
    "BBBBBBBBBBBBBBBBBBBB"]


#Room 8 - 8
tilemap_room8 = [
    "BBBBBBBBBBBBBBBBBBBB",
    "B..W...............B",
    "B..................B",
    "B..................B",
    "B..................B",
    "B..................B",
    "B....P.............*",
    "B...............C..B",
    "B..................B",
    "BBBBB*BBBBBBBBBBBBBB"]


#Room 9 - 9
tilemap_room9 = [
    "BBBBBBBBBBBBBBBBBBBB",
    "B..................B",
    "B..................B",
    "*..................B",
    "B..................B",
    "B................W.B",
    "B....P.............B",
    "B.;................B",
    "B..................B",
    "BBBBBBBBBBBBBBBBBBBB"]


#Room 10 - 10
tilemap_room10 = [
    "BBBBBBBBBBBBBB*BBBBB",
    "B......C...........B",
    "B..................B",
    "B..................B",
    "B..................B",
    "B..................B",
    "B....P.............B",
    "B.......N..........B",
    "B..................B",
    "BBBBB*BBBBBBBBBBBBBB"]


#Room 11 - 11
tilemap_room11 = [
    "BBBBBBBBBBBBBBBBBBBB",
    "B..................B",
    "B..................B",
    "B..................B",
    "B..................B",
    "B..................B",
    "B....P.............*",
    "B..................B",
    "B..................B",
    "BBBBB*BBBBBBBBBBBBBB"]


#Room 12 - 12
tilemap_room12 = [
    "BBBBBBBBBBBBBBBBBBBB",
    "B..!...............B",
    "B...............W..B",
    "*..................B",
    "B..................B",
    "B..................B",
    "B....P.............B",
    "B...............C..B",
    "B..................B",
    "BBBBBBBBBBBBBBBBBBBB"]


#Room 13 - 13
tilemap_room13 = [
    "BBBBBBBBBBBBBBBBBBBB",
    "B..................B",
    "B..................B",
    "B..................B",
    "B..................B",
    "B..................B",
    "B....P.............*",
    "B..................B",
    "B..................B",
    "BBBBB*BBBBBBBBBBBBBB"]


#Room 14 - 14
tilemap_room14 = [
    "BBBBBBBBBBBBBB*BBBBB",
    "B..................B",
    "B..................B",
    "*..................B",
    "B..............N...B",
    "B.......W..........B",
    "B....P.............*",
    "B..................B",
    "B..................B",
    "BBBBBBBBBBBBBBBBBBBB"]


#Room 15 - 15
tilemap_room15 = [
    "BBBBBBBBBBBBBBBBBBBB",
    "B..................B",
    "B.N................B",
    "*..................B",
    "B...............C..B",
    "B..................B",
    "B....P.............B",
    "B..................B",
    "B...........(......B",
    "BBBBBBBBBBBBBBBBBBBB"]


#Room 16 - 16
tilemap_room16 = [
    "BBBBBBBBBBBBBB*BBBBB",
    "B..................B",
    "B..................B",
    "B..................B",
    "B..................B",
    "B..................B",
    "B....P.............*",
    "B...............{..B",
    "B..W...............B",
    "BBBBBBBBBBBBBBBBBBBB"]


#Room 17 - 17
tilemap_room17 = [
    "BBBBBBBBBBBBBBBBBBBB",
    "B..................B",
    "B...C..............B",
    "*..................B",
    "B..................B",
    "B..................B",
    "B....P.............B",
    "B..................B",
    "B..........4.......B",
    "BBBBBBBBBBBBBBBBBBBB"]


#Room 18 - 18
tilemap_room18 = [
    "BBBBBBBBBBBBBB*BBBBB",
    "B...3..............B",
    "B..................B",
    "B..................B",
    "B..................B",
    "B................).B",
    "B....P.............B",
    "B..................B",
    "B...............W..B",
    "BBBBBBBBBBBBBBBBBBBB"]


#Room 19 - 19
tilemap_room19 = [
    "BBBBBBBBBBBBBBBBBBBB",
    "B..................B",
    "B..............C...B",
    "*..................B",
    "B..................B",
    "B..................B",
    "B....P.............B",
    "B..................B",
    "B...............W..B",
    "BBBBB*BBBBBBBBBBBBBB"]


#Room 20 - 20
tilemap_room20 = [
    "BBBBBBBBBBBBBBBBBBBB",
    "B................C.B",
    "B..................B",
    "*..................B",
    "B.}................B",
    "B..................B",
    "B....P.............*",
    "B..................B",
    "B..................B",
    "BBBBBBBBBBBBBBBBBBBB"]


#Room 21 - 21
tilemap_room21 = [
    "BBBBBBBBBBBBBBBBBBBB",
    "B..................B",
    "B..................B",
    "*..................B",
    "B.......W..........B",
    "B..................B",
    "B....P.............*",
    "B...............N..B",
    "B..................B",
    "BBBBBBBBBBBBBBBBBBBB"]


#Room 22 - 22
tilemap_room22 = [
    "BBBBBBBBBBBBBBBBBBBB",
    "B..................B",
    "B..................B",
    "*..................B",
    "B..................B",
    "B...............C..B",
    "B....P.............*",
    "B..................B",
    "B..................B",
    "BBBBB*BBBBBBBBBBBBBB"]


#Room 23 - 23
tilemap_room23 = [
    "BBBBBBBBBBBBBBBBBBBB",
    "B..N...............B",
    "B............[.....B",
    "~..................B",
    "B..................B",
    "B..................B",
    "B....P.............*",
    "B..................B",
    "B..............W...B",
    "BBBBBBBBBBBBBBBBBBBB"]


#Room 24 - 24
tilemap_room24 = [
    "BBBBBBBBBBBBBBBBBBBB",
    "B..................B",
    "B..................B",
    "B..................B",
    "B..................B",
    "B..................B",
    "B....P.............*",
    "B..................B",
    "B..................B",
    "BBBBBBBBBBBBBBBBBBBB"]



#-----Room Lists-----
starting_room = 20

rooms = [
    tilemap_room24,tilemap_room23,tilemap_room22,tilemap_room21,tilemap_room20,tilemap_room19,
    tilemap_room8,tilemap_room9,tilemap_room10,tilemap_room11,tilemap_room12,tilemap_room18,
    tilemap_room5,tilemap_room4,tilemap_room2,tilemap_room3,tilemap_room13,tilemap_room17,
    tilemap_room6,tilemap_room7,tilemap_room1,tilemap_room16,tilemap_room14,tilemap_room15
    ]

room_names = [
    "Room 24","Room 23","Room 22","Room 21","Room 20","Room 19",
    "Room 8","Room 9","Room 10","Room 11","Room 12","Room 18",
    "Room 5","Room 4","Courtyard","Room 3","Room 13","Room 17",
    "Room 6","Vault","Start","Room 16","Room 14","Room 15"
    ]



    
    
    

    

