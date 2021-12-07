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

#-----Display Constants-----
display_width = 640
display_height = 480
tile_size = 32
title = "Title"
FPS = 60
font_name = "ariel"

#-----Game Config-----
player_speed = 4
enemy_speed = 2
player_health = 50
crit_multiplier = 1.5
coins_per_kill = 5
coins_per_pickup = 2
enemy_min_distance = 1
enemy_max_distance = 50
score_per_kill = 50
armour_per_level = 0.05
health_per_potion = 15
price_potion = 20
price_armour = 25


#-----Sprite Constants-----
layer_player = 6
layer_enemy = 5
layer_wizard = 4
layer_coin = 3
layer_block = 2
layer_ground = 1

#-----Tile Maps-----

#Room 1 - Start
tilemap_room1 = [
    "BBBBBBBBB..BBBBBBBBB",
    "B........UC.N......B",
    "B...N..............B",
    "B........BB........B",
    "B.......BBBB.......B",
    "B..C...B.BB.B......B",
    "B.....B..BB..B.....B",
    "B..N.....BB.....C..B",
    "B........BB....N...B",
    "B..................B",
    "B.........P........B",
    "BBBBBBBBBBBBBBBBBBBB"]

#Room 2 - Courtyard
tilemap_room2 = [
    "BBBBBBBBB..BBBBBBBBB",
    "B..N.....U.....C...B",
    "B..................B",
    "B....BBBB..BBBB....B",
    "B....B........B....B",
    ".L......N.........R.",
    ".C.......C...N......",
    "B....B........B....B",
    "B....BBBB.CBBBB....B",
    "B.N............N...B",
    "B........DP........B",
    "BBBBBBBBB..BBBBBBBBB"]

#Room 3 - Graveyard
tilemap_room3 = [
    "BBBBBBBBB..BBBBBBBBB",
    "B..N.....U.........B",
    "B...........N......B",
    "B...B.CB..B.CB.CB..B",
    "B..................B",
    ".L.....N...........B",
    ".P..B..B.CB..B.CB..B",
    "B..................B",
    "B...........N......B",
    "B...B.CB.CB.CB..B..B",
    "B........N....D....B",
    "BBBBBBBBBBBBBB..BBBB"]

#Room 4 - City
tilemap_room4 = [
    "BBBBBBBBBBBBBBBBBBBB",
    "B..C......BB.......B",
    "B...BB..N.BB.......B",
    "B...BB.........N...B",
    "B.............BB...B",
    ".L.....N......BB..R.",
    "...BBB..B.........P.",
    "B..B....B...BB.....B",
    "B..B.C..B...BB..N..B",
    "B..BBBBBB...C......B",
    "B...............C..B",
    "BBBBBBBBBBBBBBBBBBBBB"]

#Room 5 - Maze
tilemap_room5 = [
    "BBBBBBBBBBBBBBBBB..B",
    "B...............BU.B",
    "B.............N....B",
    "B..BBBBBBBBBB......B",
    "B..B.C......B...BBBB",
    "B..B......N.B.....R.",
    "B..BBBBBBB..B.....P.",
    "B....N...B..BBBBB..B",
    "B........B..BBBBB..B",
    "BBBBBBB..B.........B",
    "B.D......B.........B",
    "B..BBBBBBBBBBBBBBBBB"]

#Room 6 - Vault Entrance
tilemap_room6 = [
    "B..BBBBBBBBBBBBBBBBB",
    "BUPB......N........B",
    "B.NB..N.......N....B",
    "BN.B..BBBBBBBBBBB.R.",
    "B..B..B..N.....N....",
    "BN.B..BBBBBBBBBBBBBB",
    "B..B....N.......N..B",
    "BN.B........N......B",
    "B..BBBBBBBBBBBBBB..B",
    "BN....N........N...B",
    "B..........N.......B",
    "BBBBBBBBBBBBBBBBBBBB"]

#Room 7 - Vault
tilemap_room7 = [
    "BBBBBBBBBBBBBBBBBBBB",
    "B.C.C.......C...C.CB",
    "B....C.C..C..C.....B",
    ".L.C...C......C..C.B",
    ".P.C..C.C..C.C.C...B",
    "B.C....C......C...CB",
    "B....C.C.C..C...C..B",
    "B.C.C...C......C..CB",
    "B..C..C.....C.....CB",
    "B....C.....C...C..CB",
    "B...C...C.C..C.C...B",
    "BBBBBBBBBBBBBBBBBBBB"]

#Room 8 - 8
tilemap_room8 = [
    "BBBBBBBBBBBBBBBBBBBB",
    "B..................B",
    "B...C..............B",
    "B..........N.......B",
    "B..................B",
    "B...........C.....R.",
    "B...N...............",
    "B...............N..B",
    "B........N.........B",
    "B...C..............B",
    "B...........C....DPB",
    "BBBBBBBBBBBBBBBBB..B"]

#Room 9 - 9
tilemap_room9 = [
    "BBBBBBBBB..BBBBBBBBB",
    "B........U.........B",
    "B.......N......N...B",
    "B..................B",
    "B...........C......B",
    ".L........N....N..R.",
    ".P..................",
    "B.....N............B",
    "B........C.........B",
    "B...........N......B",
    "B.C................B",
    "BBBBBBBBBBBBBBBBBBBB"]


#Room 10 - 10
tilemap_room10 = [
    "BBBBBBBBBBBBBBBBBBBB",
    "B.......C..........B",
    "B..................B",
    "B.............N....B",
    "B....N.............B",
    ".L.................B",
    "................C..B",
    "B..........N.......B",
    "B..................B",
    "B..................B",
    "B........DP........B",
    "BBBBBBBBB..BBBBBBBBB"]


#Room 11 - 11
tilemap_room11 = [
    "BBBBBBBBBBBBBBBBBBBB",
    "B..................B",
    "B............C.....B",
    "B....N.............B",
    "B........C.........B",
    "B..............N..R.",
    "B..C................",
    "B........N.........B",
    "B................N.B",
    "B..N...............B",
    "B........DP........B",
    "BBBBBBBBB..BBBBBBBBB"]


#Room 12 - 12
tilemap_room12 = [
    "BBBBBBBBBBBBBBBBBBBB",
    "B..................B",
    "B......C...........B",
    "B..................B",
    "B.....N............B",
    ".L.............C..R.",
    ".P..................",
    "B.........C....N...B",
    "B....C....N........B",
    "B..................B",
    "B........C.....C...B",
    "BBBBBBBBBBBBBBBBBBBB"]


#Room 13 - 13
tilemap_room13 = [
    "BBBBBBBBBBBBBBBBBBBB",
    "B..................B",
    "B............N.....B",
    "B..................B",
    "B..................B",
    "B.....N...........R.",
    "B...................",
    "B..............N...B",
    "B......C...........B",
    "B....N.............B",
    "B........DP....C...B",
    "BBBBBBBBB..BBBBBBBBB"]


#Room 14 - 14
tilemap_room14 = [
    "BBBBBBBBB..BBBBBBBBB",
    "B........U.........B",
    "B....N.............B",
    "B..................B",
    "B.............N....B",
    ".L........C.......R.",
    ".P..................",
    "B...............N..B",
    "B.......N..........B",
    "B..................B",
    "B..................B",
    "BBBBBBBBBBBBBBBBBBBB"]


#Room 15 - Shop
tilemap_room15 = [
    "BBBBBBBBBBBBBBBBBBBB",
    "B..................B",
    "B.......C..........B",
    "B..................B",
    "B..................B",
    ".L...............W.B",
    ".P.................B",
    "B...C........C.....B",
    "B..................B",
    "B.........C........B",
    "B..................B",
    "BBBBBBBBBBBBBBBBBBBB"]


#Room 16 - 16
tilemap_room16 = [
    "BBBBBBBBBBBBBB..BBBB",
    "B.............U.P..B",
    "B..................B",
    "B.....C....N.......B",
    "B..................B",
    "B.................R.",
    "B............C......",
    "B..................B",
    "B....N.............B",
    "B..................B",
    "B...............N..B",
    "BBBBBBBBBBBBBBBBBBBB"]


#Room 17 - 17
tilemap_room17 = [
    "BBBBBBBBB..BBBBBBBBB",
    "B........UN........B",
    "B..................B",
    "B...N....C.......N.B",
    "B..................B",
    ".L..........N......B",
    ".P.................B",
    "B....C.......C.....B",
    "B..................B",
    "B.......N.C........B",
    "B..................B",
    "BBBBBBBBBBBBBBBBBBBB"]


#Room 18 - 18
tilemap_room18 = [
    "BBBBBBBBB..BBBBBBBBB",
    "B........UP........B",
    "B..................B",
    "B...............C..B",
    "B.....N............B",
    ".L.C...............B",
    "................N..B",
    "B.........N........B",
    "B...........C......B",
    "B...N..............B",
    "B........D.........B",
    "BBBBBBBBB..BBBBBBBBB"]


#Room 19 - 19
tilemap_room19 = [
    "BBBBBBBBBBBBBBBBBBBB",
    "B..................B",
    "B.......C.......N..B",
    "B....N.............B",
    "B........N.........B",
    ".L..N.........C....B",
    "...................B",
    "B....C........N....B",
    "B..N...............B",
    "B.............N....B",
    "B........DP........B",
    "BBBBBBBBB..BBBBBBBBB"]


#Room 20 - 20
tilemap_room20 = [
    "BBBBBBBBBBBBBBBBBBBB",
    "B..................B",
    "B..................B",
    "B......N......N....B",
    "B..................B",
    ".L................R.",
    ".......N..........P.",
    "B..............N...B",
    "B..................B",
    "B.....N............B",
    "B..................B",
    "BBBBBBBBBBBBBBBBBBBB"]


#Room 21 - 21
tilemap_room21 = [
    "BBBBBBBBBBBBBBBBBBBB",
    "B..................B",
    "B......N...........B",
    "B..................B",
    "B....C.N.......N...B",
    ".L..........C.....R.",
    "......N...........P.",
    "B...C..............B",
    "B............N.....B",
    "B..................B",
    "B..................B",
    "BBBBBBBBBBBBBBBBBBBB"]


#Room 22 - 22
tilemap_room22 = [
    "BBBBBBBBBBBBBBBBBBBB",
    "B..................B",
    "B......C......N....B",
    "B..N...............B",
    "B..............C...B",
    ".L...C...N........R.",
    "..................P.",
    "B....N......N......B",
    "B.........C........B",
    "B...C..............B",
    "B..................B",
    "BBBBBBBBBBBBBBBBBBBB"]

#Room 23 - 23
tilemap_room23 = [
    "BBBBBBBBBBBBBBBBBBBB",
    "B.C................B",
    "B..................B",
    "B....N.......N.....B",
    "B..................B",
    ".L...........N....R.",
    "....................",
    "B........N.........B",
    "B..N...............B",
    "B..............C...B",
    "B........DP........B",
    "BBBBBBBBB..BBBBBBBBB"]


#Room 24 - 24
tilemap_room24 = [
    "BBBBBBBBBBBBBBBBBBBB",
    "B..................B",
    "B.....N.......N....B",
    "B..C......N........B",
    "B..................B",
    "B.....N.......N...R.",
    "B.........N.......P.",
    "B......C...........B",
    "B.....N.......N....B",
    "B.........N........B",
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
    "Maze","City","Courtyard","Graveyard","Room 13","Room 17",
    "Room 6","Vault","Start","Room 16","Room 14","Shop"
    ]

    
    

    

