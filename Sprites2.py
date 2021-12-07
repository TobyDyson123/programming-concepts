import pygame as p
import math
import random
from Settings2 import *

class Spritesheet:
    #spritesheet class constructor
    def __init__(self, file):
        self.sheet = p.image.load(file).convert_alpha() #loads spritesheet specified in file parameter

    #get sprite function to get the specific sprite from the spritesheet file in parameter
    def get_sprite(self, x, y, width, height):
        sprite = p.Surface((width,height)) #creates a Surface equal to the size of the desired sprite
        sprite.blit(self.sheet, (0,0), (x, y, width, height)) #selects only the sprite between the x, y, width and height of the spritesheet
        sprite.set_colorkey(black) #removes background
        return sprite

class Player(p.sprite.Sprite):
    #player class constructor
    def __init__(self, game, x, y):
        self.game = game
        self._layer = layer_player
        self.groups = self.game.all_sprites, self.game.player
        p.sprite.Sprite.__init__(self, self.groups)
        self.game.player_sprite = self

        self.x = x * tile_size
        self.y = y * tile_size
        self.width = tile_size
        self.height = tile_size

        self.facing = "down"

        self.image = self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height)
        self.resting_image = self.image
        self.animation_loop = 0
        self.moving = False

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.down_animations = [self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(35, 2, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(68, 2, self.width, self.height)]

        self.up_animations = [self.game.character_spritesheet.get_sprite(3, 34, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(35, 34, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(68, 34, self.width, self.height)]

        self.left_animations = [self.game.character_spritesheet.get_sprite(3, 98, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(35, 98, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(68, 98, self.width, self.height)]

        self.right_animations = [self.game.character_spritesheet.get_sprite(3, 66, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(35, 66, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(68, 66, self.width, self.height)]

    #updates player sprite
    def update(self):
        self.movement()

    #manages player movement and movement animations
    def movement(self, direction="still"):
        self.facing = direction
        if direction == "still":
            self.image = self.resting_image
            return
        
        if self.facing == "down":
            if self.animation_loop > 3:
                self.animation_loop = 0
            self.image = self.down_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.2

        if self.facing == "up":
            if self.animation_loop > 3:
                self.animation_loop = 0
            self.image = self.up_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.2
            
        if self.facing == "left":
            if self.animation_loop > 3:
                self.animation_loop = 0
            self.image = self.left_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.2

        if self.facing == "right":
            if self.animation_loop > 3:
                self.animation_loop = 0
            self.image = self.right_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.2


        pass

class Enemy(p.sprite.Sprite):
    #Enemy class constructor
    def __init__(self, game, x, y):
        self.game = game
        self._layer = layer_enemy
        self.groups = self.game.all_sprites, self.game.enemies
        p.sprite.Sprite.__init__(self, self.groups)

        self.x = x * tile_size
        self.y = y * tile_size
        self.width = tile_size
        self.height = tile_size
        
        self.facing = random.choice(["left","right","up","down"])

        self.image = self.image = self.game.enemies_spritesheet.get_sprite(3, 2, self.width, self.height)
        self.image.set_colorkey(black)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.down_animation = self.game.enemies_spritesheet.get_sprite(3, 2, self.width, self.height)

        self.up_animation = self.game.enemies_spritesheet.get_sprite(3, 34, self.width, self.height)

        self.left_animation = self.game.enemies_spritesheet.get_sprite(3, 98, self.width, self.height)

        self.right_animation = self.game.enemies_spritesheet.get_sprite(3, 66, self.width, self.height)

    #updates enemy sprite
    def update(self):
        self.movement()
        self.animate()
        
        self.collide_blocks("x")
        self.collide_blocks("y")


        pass

    #controls enemy sprite animations
    def animate(self):
        if self.facing == "down":
            self.image = self.down_animation

        if self.facing == "up":
            self.image = self.up_animation

        if self.facing == "left":
            self.image = self.left_animation

        if self.facing == "right":
            self.image = self.right_animation                    

class Block(p.sprite.Sprite):
    #block class constructor
    def __init__(self, game, x, y):
        self.game = game
        self._layer = layer_block
        self.groups = self.game.all_sprites, self.game.blocks
        p.sprite.Sprite.__init__(self, self.groups)

        self.x = x * tile_size
        self.y = y * tile_size
        self.width = tile_size
        self.height = tile_size

        self.image = self.game.terrain_spritesheet.get_sprite(960, 448, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Ground(p.sprite.Sprite):
    #ground class constructor
    def __init__(self, game, x, y, cover=False):
        self.game = game
        if cover:
            self.layer = layer_ground + 10
        else:
           self._layer = layer_ground
        self.groups = self.game.all_sprites
        p.sprite.Sprite.__init__(self, self.groups)

        self.x = x * tile_size
        self.y = y * tile_size
        self.width = tile_size
        self.height = tile_size

        self.image = self.game.terrain_spritesheet.get_sprite(64 ,352, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Button:
    #button class constructor
    def __init__(self, msg, font_name, text_size, text_colour, button_x, button_y, button_width, button_height, initial_colour, active_colour):
        self.screen = p.display.set_mode((display_width,display_height))
        self.msg = msg
        self.font_name = font_name
        self.text_size = text_size
        self.text_colour = text_colour

        self.button_x = button_x
        self.button_y = button_y
        self.button_width = button_width
        self.button_height = button_height
        self.initial_colour = initial_colour
        self.active_colour = active_colour

        self.image = p.Surface((self.button_width, self.button_height))
        self.rect = self.image.get_rect()

        self.rect.x = self.button_x
        self.rect.y = self.button_y

    #loads button and draws in on screen
    def load(self):
        self.font = p.font.Font(self.font_name, self.text_size)
        self.text_surface = self.font.render(self.msg, True, self.text_colour)
        self.text_rect = self.text_surface.get_rect(center=(self.rect.x + self.button_width/2, self.rect.y + self.button_height/2))
        self.screen.blit(self.image, self.rect)
        self.screen.blit(self.text_surface, self.text_rect)

    #checks whether button is pressed and returns True or False
    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            self.image.fill(self.active_colour)
            if pressed[0]:
                return True
            else:
                return False
        self.image.fill(self.initial_colour)
        return False

class Coin(p.sprite.Sprite):
    #coin class constructor
    def __init__(self, game, x, y):
        self.game = game
        self._layer = layer_coin
        self.groups = self.game.all_sprites, self.game.coins
        p.sprite.Sprite.__init__(self, self.groups)

        self.x = x * tile_size
        self.y = y * tile_size
        self.width = tile_size
        self.height = tile_size

        self.animation_loop = 1
        
        self.image = self.game.coin_spritesheet.get_sprite(0 , 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Wizard(p.sprite.Sprite):
    #wizard class constructor
    def __init__(self, game, x, y):
        self.game = game
        self._layer = layer_wizard
        self.groups = self.game.all_sprites, self.game.wizard
        p.sprite.Sprite.__init__(self, self.groups)

        self.x = x * tile_size
        self.y = y * tile_size
        self.width = tile_size
        self.height = tile_size
        
        self.colours_list = ["red","blue","green","yellow","orange","pink","cyan","brown","white"]
        self.colour = random.choice(self.colours_list)
        self.image = self.game.wizard_spritesheet.get_sprite(32 * (self.colours_list.index(self.colour) + 1),0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Chest(p.sprite.Sprite):
    #chest class constructor
    def __init__(self, game, x, y, chest_type):
        self.game = game
        self._layer = layer_chest
        self.groups = self.game.all_sprites, self.game.chest
        p.sprite.Sprite.__init__(self, self.groups)
        self.name = ""

        self.x = x * tile_size
        self.y = y * tile_size
        self.width = tile_size
        self.height = tile_size

        self.chest_type = chest_type
        if self.chest_type == "1":
            self.image = self.game.chest_spritesheet.get_sprite(0 ,0, self.width, self.height)
            self.name = "yellow chest"
        elif self.chest_type == "2":
            self.image = self.game.chest_spritesheet.get_sprite(65 ,0, self.width, self.height)
            self.name = "green chest"
        elif self.chest_type == "3":
            self.image = self.game.chest_spritesheet.get_sprite(129 ,0, self.width, self.height)
            self.name = "red chest"
        elif self.chest_type == "4":
            self.image = self.game.chest_spritesheet.get_sprite(193,0, self.width, self.height)
            self.name = "blue chest"
        elif self.chest_type == "5":
            self.image = self.game.chest_spritesheet.get_sprite(33 ,0, self.width, self.height)
            self.name = "opened yellow chest"
        elif self.chest_type == "6":
            self.image = self.game.chest_spritesheet.get_sprite(97 ,0, self.width, self.height)
            self.name = "opened green chest"
        elif self.chest_type == "7":
            self.image = self.game.chest_spritesheet.get_sprite(161 ,0, self.width, self.height)
            self.name = "opened red chest"
        elif self.chest_type == "8":
            self.image = self.game.chest_spritesheet.get_sprite(225,0, self.width, self.height)
            self.name = "opened blue chest"

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class NPC(p.sprite.Sprite):
    #npc class constructor
    def __init__(self, game, x, y, npc_type):
        self.game = game
        self._layer = layer_npc
        self.groups = self.game.all_sprites, self.game.npcs
        p.sprite.Sprite.__init__(self, self.groups)
        self.name = ""

        self.x = x * tile_size
        self.y = y * tile_size
        self.width = tile_size
        self.height = tile_size

        self.npc_type = npc_type
        if self.npc_type == "!":
            self.image = self.game.npc_spritesheet.get_sprite(0 ,0, self.width, self.height)
            self.name = "Jerrard"
        elif self.npc_type == ":":
            self.image = self.game.npc_spritesheet.get_sprite(33 ,0, self.width, self.height)
            self.name = "Ash"
        elif self.npc_type == ";":
            self.image = self.game.npc_spritesheet.get_sprite(65 ,0, self.width, self.height)
            self.name = "Bazza"
        elif self.npc_type == "(":
            self.image = self.game.npc_spritesheet.get_sprite(97,0, self.width, self.height)
            self.name = "Gordon"
        elif self.npc_type == ")":
            self.image = self.game.npc_spritesheet.get_sprite(129 ,0, self.width, self.height)
            self.name = "Gale"
        elif self.npc_type == "[":
            self.image = self.game.npc_spritesheet.get_sprite(161 ,0, self.width, self.height)
            self.name = "Eddie"
        elif self.npc_type == "]":
            self.image = self.game.npc_spritesheet.get_sprite(193 ,0, self.width, self.height)
            self.name = "Roderick"
        elif self.npc_type == "{":
            self.image = self.game.npc_spritesheet.get_sprite(225,0, self.width, self.height)
            self.name = "Kane"
        elif self.npc_type == "}":
            self.image = self.game.npc_spritesheet.get_sprite(257,0, self.width, self.height)
            self.name = "Leo"

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
    
class Door(p.sprite.Sprite):
    #door class constructor
    def __init__(self, game, x, y, door_type):
        self.game = game
        self.door_type = door_type
        if self.door_type == "*":
            self._layer = layer_door + 4
        else:
            self._layer = layer_door
        self.groups = self.game.all_sprites, self.game.doors
        p.sprite.Sprite.__init__(self, self.groups)

        self.x = x * tile_size
        self.y = y * tile_size
        self.width = tile_size
        self.height = tile_size

        if self.door_type == "|": #green door
            self.image = self.game.door_spritesheet.get_sprite(0 ,0, self.width, self.height)
        elif self.door_type == "-": #blue door
            self.image = self.game.door_spritesheet.get_sprite(32 ,0, self.width, self.height)
        elif self.door_type == "=": #red door
            self.image = self.game.door_spritesheet.get_sprite(64 ,0, self.width, self.height)
        elif self.door_type == "~": #yellow door
            self.image = self.game.door_spritesheet.get_sprite(96 ,0, self.width, self.height)
        elif self.door_type == "*": #open door
            self.image = self.game.door_spritesheet.get_sprite(128 ,0, self.width, self.height)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    
        
        

        

        
        
