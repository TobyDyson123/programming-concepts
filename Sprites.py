import pygame as p
import math
import random
from Settings import *

class Spritesheet:
    def __init__(self, file):
        self.sheet = p.image.load(file).convert_alpha() #loads spritesheet specified in file parameter

    def get_sprite(self, x, y, width, height):
        sprite = p.Surface((width,height)) #creates a Surface equal to the size of the desired sprite
        sprite.blit(self.sheet, (0,0), (x, y, width, height)) #selects only the sprite between the x, y, width and height of the spritesheet
        sprite.set_colorkey(black) #removes background
        return sprite

class Player(p.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = layer_player
        self.groups = self.game.all_sprites
        p.sprite.Sprite.__init__(self, self.groups)

        self.x = x * tile_size
        self.y = y * tile_size
        self.width = tile_size
        self.height = tile_size

        self.facing = "down"
        self.animation_loop = 1

        self.x_change = 0
        self.y_change = 0

        self.image = self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height)

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

##        distance_from_center_x = self.x + self.width/2 - display_width/2 #calculates the distance between the x value of center of screen and the x value of the player
##        distance_from_center_y = self.y + self.height/2 - display_height/2 #calculates the distance between the y value of center of screen and the y value of the player
##        print ("player center: ", self.x + self.width/2, self.y + self.height/2)
##        print ("display width and display height center: ",display_width/2,display_height/2)
##        print ("distance from center: ", distance_from_center_x, distance_from_center_y)
##        spritexlist1, spriteylist1,spritexlist2,spriteylist2 = [],[],[],[]
##        for sprite in self.game.all_sprites: #iterates through all sprites
##            #print("self.x value: ", self.x)
##            #print ("before x and y: ",sprite.rect.x, sprite.rect.y)
##            xval = sprite.rect.x
##            spritexlist1.append(xval)
##            yval = sprite.rect.y
##            spriteylist1.append(yval)
##            sprite.rect.x -= int(distance_from_center_x) #moves the sprite to the left by distance between x value of player and x value of center of screen 
##            sprite.rect.y -= int(distance_from_center_y) #moves the sprite up by distance between y value of player and y value of center of screen
##            spritexlist2.append(sprite.rect.x)
##            spriteylist2.append(sprite.rect.y)
##            #print ("after x and y: ",sprite.rect.x, sprite.rect.y)
##            #print (sprite.rect.x - xval == -distance_from_center_x and sprite.rect.y - yval == -distance_from_center_y)
##        print (len(spritexlist1))
##        for i in range(len(spritexlist1)):
##            print (spritexlist1[i], spriteylist1[i], spritexlist2[i], spriteylist2[i],
##                   spritexlist2[i] - spritexlist1[i] == -distance_from_center_x and spriteylist2[i] - spriteylist1[i] == -distance_from_center_y, list(game.all_sprites)[i])
##
####        distance_from_center_x = self.x + self.width/2 - display_width/2 #calculates the distance between the x value of center of screen and the x value of the player
####        distance_from_center_y = self.y + self.height/2 - display_height/2 #calculates the distance between the y value of center of screen and the y value of the player
####        for sprite in self.game.all_sprites: #iterates through all sprites
####            sprite.rect.x -= int(distance_from_center_x) #moves the sprite to the left by distance between x value of player and x value of center of screen 
####            sprite.rect.y -= int(distance_from_center_y) #moves the sprite up by distance between y value of player and y value of center of screen
##            
                

    def update(self):
        self.collide_shop()
        self.movement()
        self.animate()
        self.collide_enemy()
        self.collide_coin()

        self.rect.x += self.x_change
        self.collide_blocks("x")
        self.rect.y += self.y_change
        self.collide_blocks("y")

        self.x_change = 0
        self.y_change = 0

    def movement(self):
        self.centerOfPlayer = (self.rect.x + self.width/2, self.rect.y + self.height/2)
        keys = p.key.get_pressed()
        if keys[p.K_a]:
            #for sprite in self.game.all_sprites:
            #    sprite.rect.x += player_speed
            self.x_change = -player_speed
            #self.y_change = 0
            #self.facing = "left"
        if keys[p.K_d]:
            #for sprite in self.game.all_sprites:
            #    sprite.rect.x -= player_speed
            self.x_change = player_speed
            #self.y_change = 0
            #self.facing = "right"
        if keys[p.K_w]:
            #for sprite in self.game.all_sprites:
            #    sprite.rect.y += player_speed
            self.y_change = -player_speed
            #self.x_change = 0
            #self.facing = "up"
        if keys[p.K_s]:
            #for sprite in self.game.all_sprites:
            #    sprite.rect.y -= player_speed
            self.y_change = player_speed
            #self.x_change = 0
            #self.facing = "down"

        if self.x_change < 0:
            self.facing = "left"
        elif self.x_change > 0:
            self.facing = "right"
        elif self.y_change < 0:
            self.facing = "up"
        elif self.y_change > 0:
            self.facing = "down"

        if self.centerOfPlayer[0] < 0: #left
            self.game.current_room -= 1
            self.game.change_room(rooms[self.game.current_room], display_width - self.width, self.rect.y)
            print (self.game.current_room)
            print ("\n".join(rooms[self.game.current_room]))
                    
        elif self.centerOfPlayer[0] > display_width: #right
            self.game.current_room += 1
            self.game.change_room(rooms[self.game.current_room], self.width, self.rect.y)
            print (self.game.current_room)
            print ("\n".join(rooms[self.game.current_room]))
            
        elif self.centerOfPlayer[1] < 0: #up
            self.game.current_room -= 6
            self.game.change_room(rooms[self.game.current_room], self.rect.x, display_height - self.height - (3 * tile_size))
            print (self.game.current_room)
            print ("\n".join(rooms[self.game.current_room]))
                    
        elif self.centerOfPlayer[1] > display_height - (3 * tile_size):#down
            self.game.current_room += 6
            self.game.change_room(rooms[self.game.current_room], self.rect.x, 0)
            print (self.game.current_room)
            print ("\n".join(rooms[self.game.current_room]))
        

    def collide_enemy(self):
        self.typing = False
        self.enemy_collision = True
        hits = p.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            self.input_text = ""
            input_button = Button("", self.game.font_name, 25, black, (display_width/10), display_height-100, (display_width/10)*8, 50, yellow, cyan)
            while self.enemy_collision:
                for event in p.event.get():
                    if event.type == p.QUIT:
                        self.enemy_collision = False
                        self.game.playing = False
                        self.game.active = False
                    if event.type == p.KEYDOWN:
                        if self.typing:
                            if event.key == p.K_RETURN:
                                self.input_text = input_button.msg
                            elif event.key == p.K_BACKSPACE:
                                if not input_button.msg:
                                    pass
                                else:
                                    input_button.msg = input_button.msg[:-1]
                            elif event.key == p.K_SPACE:
                                input_button.msg += " "
                            else:
                                if len(p.key.name(event.key)) == 1:
                                    if (ord(p.key.name(event.key)) >= 97 and ord(p.key.name(event.key)) <= 122 or
                                        ord(p.key.name(event.key)) >= 48 and ord(p.key.name(event.key)) <= 57):
                                        input_button.msg += str(p.key.name(event.key))

                p.draw.rect(self.game.screen, blue, (0,display_height-200,display_width,200))
                self.game.draw_text("You have hit an enemy. Would you like to try and fight it", 32, orange, display_width/2, display_height-180)
                self.game.draw_text("or would you like to run away?", 32, orange, display_width/2, display_height-150)
                
                mouse_pos = p.mouse.get_pos()
                mouse_pressed = p.mouse.get_pressed()
                    
                if not input_button.rect.collidepoint(mouse_pos):
                    if mouse_pressed[0]:
                        self.typing = False
                        
                if input_button.is_pressed(mouse_pos, mouse_pressed):
                    self.typing = True

                if not self.typing and not input_button.msg:
                    input_button.text_colour = lightgrey
                    input_button.msg = "Click to type answer"

                if self.typing:
                    if input_button.msg == "Click to type answer":
                        input_button.msg = ""
                        input_button.text_colour = black
                    input_button.image.fill(input_button.active_colour)

                input_button.load()

                if "fight" in self.input_text.lower():
                    choice = random.choice(["kill", "kill", "killButHurt", "killButHurt", "killButCritical"])
                    if choice == "kill":
                        self.game.give_coins_to_player(coins_per_kill)
                        self.game.give_score_to_player(score_per_kill)
##                        for sprite in hits:
##                            for i, row in enumerate(rooms[self.game.current_room]):
##                                for j, column in enumerate(row):
##                                    if column == "N" and j == sprite.x/tile_size and i == sprite.y/tile_size:
##                                        rooms[self.game.current_room][i] = rooms[self.game.current_room][i][:j] + "." + rooms[self.game.current_room][i][j+1:]
                        hits[0].kill()
                        p.draw.rect(self.game.screen, blue, (0,display_height-200,display_width,200))
                        self.game.draw_text("You have successfully slain the enemy!", 32, green, display_width/2, display_height-180)
                        self.game.draw_text("+" + str(coins_per_kill) + " coins!", 32, yellow, display_width/2, display_height-150)
                        self.game.draw_text("+" + str(score_per_kill) + " score!", 32, yellow, display_width/2, display_height-120)
                        self.game.draw_text("Press c to continue", 32, black, display_width/2, display_height-90)
                        self.game.wait_for_key()
                        self.enemy_collision = False
                    elif choice == "killButHurt":
                        self.game.give_coins_to_player(coins_per_kill)
                        self.game.give_score_to_player(score_per_kill)
                        damage_taken = int(random.randint(3,10) * self.game.player_armour)
                        self.game.damage_player(damage_taken)
##                        for sprite in hits:
##                            for i, row in enumerate(rooms[self.game.current_room]):
##                                for j, column in enumerate(row):
##                                    if column == "N" and j == sprite.x/tile_size and i == sprite.y/tile_size:
##                                        rooms[self.game.current_room][i] = rooms[self.game.current_room][i][:j] + "." + rooms[self.game.current_room][i][j+1:]
                        hits[0].kill()
                        p.draw.rect(self.game.screen, blue, (0,display_height-200,display_width,200))
                        self.game.draw_text("You have killed the enemy, but took " + str(damage_taken) + " damage!", 32, red, display_width/2, display_height-180)
                        self.game.draw_text("+" + str(coins_per_kill) + " coins!", 32, yellow, display_width/2, display_height-150)
                        self.game.draw_text("+" + str(score_per_kill) + " score!", 32, yellow, display_width/2, display_height-120)
                        self.game.draw_text("Press c to continue", 32, black, display_width/2, display_height-90)
                        self.game.wait_for_key()
                        self.enemy_collision = False
                    elif choice == "killButCritical":
                        self.game.give_coins_to_player(coins_per_kill)
                        self.game.give_score_to_player(score_per_kill)
                        damage_taken = int((random.randint(3,10) * crit_multiplier) * self.game.player_armour)
                        self.game.damage_player(damage_taken)
##                        for sprite in hits:
##                            for i, row in enumerate(rooms[self.game.current_room]):
##                                for j, column in enumerate(row):
##                                    if column == "N" and j == sprite.x/tile_size and i == sprite.y/tile_size:
##                                        rooms[self.game.current_room][i] = rooms[self.game.current_room][i][:j] + "." + rooms[self.game.current_room][i][j+1:]
                        hits[0].kill()
                        p.draw.rect(self.game.screen, blue, (0,display_height-200,display_width,200))
                        self.game.draw_text("You have killed the enemy, but took " + str(damage_taken) + " critical damage!", 32, red, display_width/2, display_height-180)
                        self.game.draw_text("+" + str(coins_per_kill) + " coins!", 32, yellow, display_width/2, display_height-150)
                        self.game.draw_text("+" + str(score_per_kill) + " score!", 32, yellow, display_width/2, display_height-120)
                        self.game.draw_text("Press c to continue", 32, black, display_width/2, display_height-90)
                        self.game.wait_for_key()
                        self.enemy_collision = False

                if "run" in self.input_text.lower():
                    choice = random.choice(["run", "run", "runButHurt", "runButCritical"])
                    if choice == "run":
                        for i, row in enumerate(rooms[self.game.current_room]):
                            for j, column in enumerate(row):
                                if column == "P":
                                    self.rect.x = j * tile_size
                                    self.rect.y = i * tile_size
                        p.draw.rect(self.game.screen, blue, (0,display_height-200,display_width,200))
                        self.game.draw_text("You have successfully fled!", 32, green, display_width/2, display_height-180)
                        self.game.draw_text("Press c to continue", 32, black, display_width/2, display_height-150)
                        self.game.wait_for_key()
                        self.enemy_collision = False
                    elif choice == "runButHurt":
                        damage_taken = int(random.randint(7,10) * self.game.player_armour)
                        self.game.damage_player(damage_taken)
                        for i, row in enumerate(rooms[self.game.current_room]):
                            for j, column in enumerate(row):
                                if column == "P":
                                    self.rect.x = j * tile_size
                                    self.rect.y = i * tile_size
                        p.draw.rect(self.game.screen, blue, (0,display_height-200,display_width,200))
                        self.game.draw_text("You have ran away, but taken " + str(damage_taken) + " damage!", 32, red, display_width/2, display_height-180)
                        self.game.draw_text("Press c to continue", 32, black, display_width/2, display_height-150)
                        self.game.wait_for_key()
                        self.enemy_collision = False
                    elif choice == "runButCritical":
                        damage_taken = int((random.randint(7,10) * crit_multiplier) * self.player_armour)
                        self.game.damage_player(damage_taken)
                        for i, row in enumerate(rooms[self.game.current_room]):
                            for j, column in enumerate(row):
                                if column == "P":
                                    self.rect.x = j * tile_size
                                    self.rect.y = i * tile_size
                        p.draw.rect(self.game.screen, blue, (0,display_height-200,display_width,200))
                        self.game.draw_text("You have ran away, but taken " + str(damage_taken) + " critical damage!", 32, red, display_width/2, display_height-180)
                        self.game.draw_text("Press c to continue", 32, black, display_width/2, display_height-150)
                        self.game.wait_for_key()
                        self.enemy_collision = False
                p.display.update()

    def collide_blocks(self, direction):
        if direction == "x":
            hits = p.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                    #for sprite in self.game.all_sprites:
                    #    sprite.rect.x += player_speed
                       
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
                    #for sprite in self.game.all_sprites:
                    #    sprite.rect.x -= player_speed

        if direction == "y":
            hits = p.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                    #for sprite in self.game.all_sprites:
                    #    sprite.rect.y += player_speed
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
                    #for sprite in self.game.all_sprites:
                    #   sprite.rect.y -= player_speed

    def animate(self):
        if self.facing == "down":
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3 ,2, self.width, self.height)
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "up":
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3 ,34, self.width, self.height)
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "left":
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3 ,98, self.width, self.height)
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "right":
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 66, self.width, self.height)
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

    def collide_coin(self):
        hits = p.sprite.spritecollide(self, self.game.coins, False)
        if hits:
            for sprite in hits:
                for i, row in enumerate(rooms[self.game.current_room]):
                    for j, column in enumerate(row):
                        if column == "C" and j == sprite.x/tile_size and i == sprite.y/tile_size:
                            rooms[self.game.current_room][i] = rooms[self.game.current_room][i][:j] + "." + rooms[self.game.current_room][i][j+1:]
                sprite.kill()
            self.game.give_coins_to_player(coins_per_pickup)

    def collide_shop(self):
        hits = p.sprite.spritecollide(self, self.game.wizard, False)
        if hits:
            self.facing = "left"
            self.rect.x = hits[0].rect.x - 2 * self.width
            self.game.shop()
            

class Enemy(p.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = layer_enemy
        self.groups = self.game.all_sprites, self.game.enemies
        p.sprite.Sprite.__init__(self, self.groups)

        self.x = x * tile_size
        self.y = y * tile_size
        self.width = tile_size
        self.height = tile_size

        self.x_change = 0
        self.y_change = 0

        self.facing = random.choice(["left","right","up","down"])
        self.animation_loop = 1
        self.movement_loop = 0
        self.max_travel = random.randint(enemy_min_distance,enemy_max_distance)

        self.image = self.image = self.game.enemies_spritesheet.get_sprite(3, 2, self.width, self.height)
        self.image.set_colorkey(black)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.down_animations = [self.game.enemies_spritesheet.get_sprite(3, 2, self.width, self.height),
                           self.game.enemies_spritesheet.get_sprite(35, 2, self.width, self.height),
                           self.game.enemies_spritesheet.get_sprite(68, 2, self.width, self.height)]

        self.up_animations = [self.game.enemies_spritesheet.get_sprite(3, 34, self.width, self.height),
                         self.game.enemies_spritesheet.get_sprite(35, 34, self.width, self.height),
                         self.game.enemies_spritesheet.get_sprite(68, 34, self.width, self.height)]

        self.left_animations = [self.game.enemies_spritesheet.get_sprite(3, 98, self.width, self.height),
                           self.game.enemies_spritesheet.get_sprite(35, 98, self.width, self.height),
                           self.game.enemies_spritesheet.get_sprite(68, 98, self.width, self.height)]

        self.right_animations = [self.game.enemies_spritesheet.get_sprite(3, 66, self.width, self.height),
                            self.game.enemies_spritesheet.get_sprite(35, 66, self.width, self.height),
                            self.game.enemies_spritesheet.get_sprite(68, 66, self.width, self.height)]

    def update(self):
        self.movement()
        self.animate()
        
        self.rect.x += self.x_change
        self.collide_blocks("x")
        self.rect.y += self.y_change
        self.collide_blocks("y")

        self.x_change = 0
        self.y_change = 0

    def movement(self):
        self.centerOfEnemy = (self.rect.x + self.width/2, self.rect.y + self.height/2)
        if self.facing == "left":
            self.x_change = -enemy_speed
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = random.choice(["left","right","up","down"])
                self.max_travel = random.randint(enemy_min_distance,enemy_max_distance)

        if self.facing == "right":
            self.x_change = enemy_speed
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = random.choice(["left","right","up","down"])
                self.max_travel = random.randint(enemy_min_distance,enemy_max_distance)

        if self.facing == "up":
            self.y_change = -enemy_speed
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = random.choice(["left","right","up","down"])
                self.max_travel = random.randint(enemy_min_distance,enemy_max_distance)

        if self.facing == "down":
            self.y_change = enemy_speed
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = random.choice(["left","right","up","down"])
                self.max_travel = random.randint(enemy_min_distance,enemy_max_distance)

        if self.centerOfEnemy[0] < 0: #left
            self.facing = "right"
                    
        elif self.centerOfEnemy[0] > display_width: #right
            self.facing = "left"
            
        elif self.centerOfEnemy[1] < 0: #up
            self.facing = "down"
                    
        elif self.centerOfEnemy[1] > display_height - (3 * tile_size):#down
            self.facing = "up"

    def animate(self):
        if self.facing == "down":
            if self.y_change == 0:
                self.image = self.game.enemies_spritesheet.get_sprite(3 ,2, self.width, self.height)
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "up":
            if self.y_change == 0:
                self.image = self.game.enemies_spritesheet.get_sprite(3 ,34, self.width, self.height)
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "left":
            if self.x_change == 0:
                self.image = self.game.enemies_spritesheet.get_sprite(3 ,98, self.width, self.height)
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == "right":
            if self.x_change == 0:
                self.image = self.game.enemies_spritesheet.get_sprite(3, 66, self.width, self.height)
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

    def collide_blocks(self, direction):
        if direction == "x":
            hits = p.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.facing = "left"
                elif self.x_change < 0:
                    self.facing = "right"

        if direction == "y":
            hits = p.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.facing = "up"   
                elif self.y_change < 0:
                    self.facing = "down"
                    

class Block(p.sprite.Sprite):
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
    def __init__(self, game, x, y):
        self.game = game
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

    def load(self):
        self.font = p.font.Font(self.font_name, self.text_size)
        self.text_surface = self.font.render(self.msg, True, self.text_colour)
        self.text_rect = self.text_surface.get_rect(center=(self.rect.x + self.button_width/2, self.rect.y + self.button_height/2))
        self.screen.blit(self.image, self.rect)
        self.screen.blit(self.text_surface, self.text_rect)

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

        self.coin_animations = [self.game.coin_spritesheet.get_sprite(0, 0, self.width, self.height),
                           self.game.coin_spritesheet.get_sprite(32, 0, self.width, self.height),
                           self.game.coin_spritesheet.get_sprite(64, 0, self.width, self.height),
                            self.game.coin_spritesheet.get_sprite(96, 0, self.width, self.height),
                           self.game.coin_spritesheet.get_sprite(128, 0, self.width, self.height),
                           self.game.coin_spritesheet.get_sprite(160, 0, self.width, self.height)]

        self.image = self.game.coin_spritesheet.get_sprite(0 ,0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def animate(self):
        self.image = self.coin_animations[math.floor(self.animation_loop)]
        self.animation_loop += 0.2
        if self.animation_loop >= 6:
            self.animation_loop = 1

    def update(self):
        self.animate()

class Wizard(p.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = layer_wizard
        self.groups = self.game.all_sprites, self.game.wizard
        p.sprite.Sprite.__init__(self, self.groups)

        self.x = x * tile_size
        self.y = y * tile_size
        self.width = tile_size
        self.height = tile_size

        self.image = self.game.wizard_spritesheet.get_sprite(0 ,0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        

    
        
        

        

        
        
