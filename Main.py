import pygame as p
from math import ceil
from Settings import *
from Sprites import *

#---------------------------------Game Class---------------------------------
class Game:
    def __init__(self):
        #game class constructor
        p.init()
        self.screen = p.display.set_mode((display_width,display_height))
        p.display.set_caption(title)
        self.clock = p.time.Clock()
        self.active = True
        self.font_name = p.font.match_font(font_name)

        self.character_spritesheet = Spritesheet("Images/character.png")
        self.terrain_spritesheet = Spritesheet("Images/terrain.png")
        self.enemies_spritesheet = Spritesheet("Images/enemy.png")
        self.coin_spritesheet = Spritesheet("Images/coin.png")
        self.wizard_spritesheet = Spritesheet("Images/wizard.png")

        self.player_health = player_health
        self.player_coins = 0
        self.player_score = 0
        self.player_armour = 1
        self.player_armour_level = 1

        self.current_room = starting_room
        self.show_map = False

        self.up_text = False
        self.down_text = False
        self.left_text = False
        self.right_text = False
        self.up_coords = ()
        self.down_coords = ()
        self.left_coords = ()
        self.right_coords = ()

        self.shop_items = {
              "Health Potion": [price_potion,"Restores " + str(health_per_potion) + " hp"],
              "Armour": [price_armour,"Reduces damage from zombies"]
              }

        self.player_inventory = {}
        self.inventory_button = Button("Inventory", self.font_name, 30, black, 500, display_height - 90, int(display_width/5), int(display_height/10), blue, cyan)


    def draw_text(self, text, size, colour, x, y):
        font = p.font.Font(self.font_name, size)
        text_surface = font.render(text, True, colour)
        text_rect = text_surface.get_rect(center=(int(x),int(y)))
        self.screen.blit(text_surface, text_rect)
        
    def new(self,room):
        #new game starts
        print ("\n".join(rooms[self.current_room]))
        self.playing = True
        self.all_sprites = p.sprite.LayeredUpdates()
        self.blocks = p.sprite.LayeredUpdates()
        self.enemies = p.sprite.LayeredUpdates()
        self.coins = p.sprite.LayeredUpdates()
        self.wizard = p.sprite.LayeredUpdates()

        for i, row in enumerate(room):
            for j, column in enumerate(row):
                Ground(self, j, i)
                if column == "B":
                    Block(self, j, i)
                if column == "N":
                    Enemy(self, j, i)
                if column == "P":
                    Player(self, j, i)
                if column == "C":
                    Coin(self, j, i)
                if column == "W":
                    Wizard(self, j, i)
                if column == "U":
                    self.up_text = True
                    self.up_coords = (j,i)
                if column == "D":
                    self.down_text = True
                    self.down_coords = (j,i)
                if column == "L":
                    self.left_text = True
                    self.left_coords = (j,i)
                if column == "R":
                    self.right_text = True
                    self.right_coords = (j,i)

    def change_room(self, room, playerx, playery):
        #new game starts
        self.up_text = False
        self.down_text = False
        self.left_text = False
        self.right_text = False
        self.playing = True
        self.all_sprites = p.sprite.LayeredUpdates()
        self.blocks = p.sprite.LayeredUpdates()
        self.enemies = p.sprite.LayeredUpdates()
        self.coins = p.sprite.LayeredUpdates()
        self.wizard = p.sprite.LayeredUpdates()

        for i, row in enumerate(room):
            for j, column in enumerate(row):
                Ground(self, j, i)
                if column == "B":
                    Block(self, j, i)
                if column == "N":
                    Enemy(self, j, i)
                if column == "P":
                    Player(self, int(playerx/32), int(playery/32))
                if column == "C":
                    Coin(self, j, i)
                if column == "W":
                    Wizard(self, j, i)
                if column == "U":
                    self.up_text = True
                    self.up_coords = (j,i)
                if column == "D":
                    self.down_text = True
                    self.down_coords = (j,i)
                if column == "L":
                    self.left_text = True
                    self.left_coords = (j,i)
                if column == "R":
                    self.right_text = True
                    self.right_coords = (j,i)

    def run(self):
        #game loop
        while self.playing:
            self.draw()
            self.events()
            self.update()

    def draw_hud(self):
        p.draw.rect(self.screen, green, p.Rect(0, display_height - (3 * tile_size), display_width, 3 * tile_size))
        self.draw_text("Player Health: " + str(self.player_health), 30, red, 150, display_height - 80)
        self.draw_text("Current Room: " + str(room_names[self.current_room]), 30, magenta, 150, display_height - 50)
        self.draw_text("Coins: " + str(self.player_coins), 30, yellow, 400, display_height - 80)
        self.draw_text("Score: " + str(self.player_score), 30, yellow, 400, display_height - 50)
            
        mouse_pos = p.mouse.get_pos()
        mouse_pressed = p.mouse.get_pressed()

        self.inventory_button.load()

        if self.inventory_button.is_pressed(mouse_pos, mouse_pressed):
            self.open_inventory()

    def open_inventory(self):
        self.inventory  = True
        self.typing = False
        self.input_text = ""
        self.item_to_delete = ""
        if self.player_inventory:
            self.purchasing_text1 = "What do you want to use,"
            self.purchasing_text2 = "or would you like to leave?"
        else:
            self.purchasing_text1 = "Your inventory is empty. Visit the shop to buy items."
            self.purchasing_text2 = "You may return to the game."
        inv_button = Button("", self.font_name, 30, black, int((display_width/5)), int((display_height/5)*4), int((display_width/5)*3), int(display_height/10), yellow, cyan)
        while self.inventory:
            for event in p.event.get():
                if event.type == p.QUIT:
                    self.inventory = False
                    self.playing = False
                    self.active = False
                if event.type == p.KEYDOWN:
                    if self.typing:
                        if event.key == p.K_RETURN:
                            self.input_text = inv_button.msg
                        elif event.key == p.K_BACKSPACE:
                            if not inv_button.msg:
                                pass
                            else:
                                inv_button.msg = inv_button.msg[:-1]
                        elif event.key == p.K_SPACE:
                            inv_button.msg += " "
                        else:
                            if len(p.key.name(event.key)) == 1:
                                if (ord(p.key.name(event.key)) >= 97 and ord(p.key.name(event.key)) <= 122 or
                                    ord(p.key.name(event.key)) >= 48 and ord(p.key.name(event.key)) <= 57):
                                    inv_button.msg += str(p.key.name(event.key))

            self.screen.fill(black)
            self.draw_text("Health: " + str(self.player_health), 30, yellow, int(display_width/7), 25)
            self.draw_text("Inventory", 50, white, int(display_width/2), 30)
            self.draw_text("--------------------------------------------------------------------------------", 30, white, int(display_width/2), 50)
            self.draw_text("Item", 30, orange, 100, 130)
            self.draw_text("Quantity", 30, orange, 210, 130)

            if self.player_inventory:
                for i, (item, quantity) in enumerate(self.player_inventory.items()):
                    self.draw_text(str(item), 25, white, 100, 160 + (30 * i))
                    self.draw_text("x" + str(quantity), 25, white, 210, 160 + (30 * i))

            self.draw_text(self.purchasing_text1, 32, orange, display_width/2, display_height-180)
            self.draw_text(self.purchasing_text2, 32, orange, display_width/2, display_height-150)
            
            mouse_pos = p.mouse.get_pos()
            mouse_pressed = p.mouse.get_pressed()
                
            if not inv_button.rect.collidepoint(mouse_pos):
                if mouse_pressed[0]:
                    self.typing = False
                    
            if inv_button.is_pressed(mouse_pos, mouse_pressed):
                self.typing = True

            if not self.typing and not inv_button.msg:
                inv_button.text_colour = lightgrey
                inv_button.msg = "Click to type what you want to use"

            if self.typing:
                if inv_button.msg == "Click to type what you want to use":
                    inv_button.msg = ""
                    inv_button.text_colour = black
                inv_button.image.fill(inv_button.active_colour)

            inv_button.load()

            if "use" in self.input_text.lower():
                for item, quantity in self.player_inventory.items():
                    if str(item).lower() in self.input_text.lower():
                        try:
                            amount = int(''.join(filter(lambda x : x.isdigit(), self.input_text)))
                            if amount <= quantity:

                                if item == "Health Potion":
                                    if self.player_health == player_health:
                                        self.purchasing_text1 = "You are already at full hp!"
                                        self.purchasing_text2 = "You may use something else, or choose to leave"
                                        inv_button.msg = ""
                                        self.input_text = ""
                                        self.typing = False
                                        
                                    else:
                                        if self.player_health + amount * health_per_potion > player_health:
                                            amount = int(ceil((player_health - self.player_health) / health_per_potion))
                                        self.player_inventory[item] -= amount
                                        self.heal_player(health_per_potion * amount)

                                        self.purchasing_text1 = "Successfully used " + str(amount) + " " + str(item) + "!"
                                        self.purchasing_text2 = "You may use something else, or choose to leave"
                                        inv_button.msg = ""
                                        self.input_text = ""
                                        self.typing = False
                            else:
                                self.purchasing_text1 = "You don't have enough of that item!"
                                self.purchasing_text2 = "Choose something else, or you may leave"
                                inv_button.msg = ""
                                self.input_text = ""
                                self.typing = False
                        except ValueError:
                            if quantity > 0:
                                if item == "Health Potion":
                                    if self.player_health == player_health:
                                        self.purchasing_text1 = "You are already at full hp!"
                                        self.purchasing_text2 = "You may use something else, or choose to leave"
                                        inv_button.msg = ""
                                        self.input_text = ""
                                        self.typing = False
                                        
                                    else:
                                        self.heal_player(health_per_potion)
                                        self.player_inventory[item] -= 1

                                        self.purchasing_text1 = "Successfully used " + str(item) + "!"
                                        self.purchasing_text2 = "You may use something else, or choose to leave"
                                        inv_button.msg = ""
                                        self.input_text = ""
                                        self.typing = False
                    else:
                        self.purchasing_text1 = "You do not own that item!"
                        self.purchasing_text2 = "Choose something else, or you may leave"
                        inv_button.msg = ""
                        self.input_text = ""
                        self.typing = False

                    if self.player_inventory[item] == 0:
                        self.item_to_delete = item
                        
            if "leave" in self.input_text.lower():
                self.inventory = False

            if self.input_text:
                self.purchasing_text1 = "Unrecognised answer. Try including 'use'"
                self.purchasing_text2 = "or 'leave' if you want to leave"
                inv_button.msg = ""
                self.input_text = ""
                self.typing = False

            if self.item_to_delete:
                self.player_inventory.pop(self.item_to_delete)
                self.item_to_delete = ""
            p.display.update()

    def draw(self):
        self.all_sprites.draw(self.screen)
        self.draw_hud()
        if self.up_text == True:
            self.draw_text(room_names[self.current_room - 6], 20, cyan, (self.up_coords[0] * tile_size) + tile_size/2, (self.up_coords[1] * tile_size) + tile_size/2)
        if self.down_text == True:
            self.draw_text(room_names[self.current_room + 6], 20, cyan, (self.down_coords[0] * tile_size) + tile_size/2, (self.down_coords[1] * tile_size) + tile_size/2)
        if self.left_text == True:
            self.draw_text(room_names[self.current_room - 1], 20, cyan, (self.left_coords[0] * tile_size) + tile_size/2, (self.left_coords[1] * tile_size) + tile_size/2)
        if self.right_text == True:
            self.draw_text(room_names[self.current_room + 1], 20, cyan, (self.right_coords[0] * tile_size) + tile_size/2, (self.right_coords[1] * tile_size) + tile_size/2)
        self.clock.tick(FPS)

    def events(self):
        #game loop events
        for event in p.event.get():
            if event.type == p.QUIT:
                self.playing = False
                self.active = False
            if event.type == p.KEYDOWN:
                if event.key == p.K_y:
                    self.damage_player(7)
                if event.key == p.K_i:
                    self.give_coins_to_player(10)
                if event.key == p.K_u:
                    self.up_text = False
                    self.down_text = False
                    self.left_text = False
                    self.right_text = False
                    self.new(tilemap_room15)
                    self.current_room = 23
                if event.key == p.K_m:
                    if self.show_map == False:
                        self.show_map = True
                    else:
                        self.show_map = False

        if self.show_map == True:
            self.display_map()
            

    def update(self):
        #game loop updates
        self.all_sprites.update()
        p.display.update()

    def intro_screen(self):
        self.intro = True

        play_button = Button("Start", self.font_name, 30, black, int((display_width/5)*2), int((display_height/5)*2), int(display_width/5), int(display_height/10), blue, cyan)
        
        while self.intro:
            for event in p.event.get():
                if event.type == p.QUIT:
                    self.intro = False
                    self.playing = False
                    self.active = False

            mouse_pos = p.mouse.get_pos()
            mouse_pressed = p.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                self.intro = False

            self.screen.fill(yellow)
            self.draw_text(title, 100, black, int(display_width/2), int(display_height/5))
            play_button.load()
            
            p.display.update()
            self.clock.tick(FPS)

    def instructions_screen(self):
        self.screen.fill(black)
        self.draw_text("Welcome to " + title, 30, white, int(display_width/2), 30)
        self.draw_text("The aim of the game is to collect as much score as possible", 30, white, int(display_width/2), 60)
        self.draw_text("while also defending yourself againsts zombies.", 30, white, int(display_width/2), 90)
        self.draw_text("You will find coins around the map, which can be picked up", 30, white, int(display_width/2), 120)
        self.draw_text("and spent at the shop for gear to help you last longer.", 30, white, int(display_width/2), 150)
        self.draw_text("But that's not the only way to collect coins.", 30, white, int(display_width/2), 180)
        self.draw_text("Slaying zombies will not only give you score but bonus coins.", 30, white, int(display_width/2), 210)
        self.draw_text("Be careful fighting zombies though, as they can", 30, white, int(display_width/2), 240)
        self.draw_text("damage you, and you only have so much health!", 30, white, int(display_width/2), 270)
        self.draw_text("Press c to get hunting!", 30, white, int(display_width/2), 300)

        self.draw_text("Controls:", 25, magenta, int((display_width/2)), 350)
        self.draw_text("W: Move up", 25, white, int((display_width/2)), 370)
        self.draw_text("A: Move left", 25, white, int((display_width/2)), 390)
        self.draw_text("S: Move down", 25, white, int((display_width/2)), 410)
        self.draw_text("D: Move right", 25, white, int((display_width/2)), 430)
        self.draw_text("M: Toggle map", 25, white, int((display_width/2)), 460)
        self.wait_for_key()
        
    def game_over(self):
        exit_button = Button("Exit", self.font_name, 30, black, int((display_width/5)*2), int((display_height/5)*2), int(display_width/5), int(display_height/10), blue, cyan)

        for sprite in self.all_sprites:
            sprite.kill()

        while self.active:
            for event in p.event.get():
                if event.type == p.QUIT:
                    self.active = False
            
            mouse_pos = p.mouse.get_pos()
            mouse_pressed = p.mouse.get_pressed()

            if exit_button.is_pressed(mouse_pos, mouse_pressed):
                self.active = False

            self.screen.fill(red)
            self.draw_text("Game Over", 100, black, int(display_width/2), int(display_height/5))
            exit_button.load()
            self.clock.tick(FPS)
            p.display.update()

    def wait_for_key(self):
        p.display.update()
        while not p.key.get_pressed()[p.K_c]:
            for event in p.event.get():
                if event.type == p.QUIT:
                    self.playing = False
                    self.active = False
                if event.type == p.KEYDOWN:
                    if event.key == p.K_c:
                        pass

    def damage_player(self, damage_taken):
        self.player_health -= damage_taken
        if self.player_health <= 0:
            self.playing = False

    def heal_player(self, heal_amount):
        if player_health - heal_amount > self.player_health:
            self.player_health += heal_amount
        else:
            self.player_health = player_health
        

    def give_coins_to_player(self, coins):
        self.player_coins += coins

    def take_coins_from_player(self, coins):
        self.player_coins -= coins

    def give_score_to_player(self, score):
        self.player_score += score

    def display_map(self):
        self.room_index = 0
        self.map_box = p.Surface((int((display_width/6)*4),int((display_height/6)*4)))  
        self.map_box.set_alpha(128)                
        self.map_box.fill(black)           
        self.screen.blit(self.map_box, (int(display_width/6),int((display_height/6) - 50)))
        
        self.map_rect = p.Rect(int(display_width/6), int(display_height/6) - 50, int((display_width/6) * 4), int((display_height/6) * 4)) 
        self.mapx = self.map_rect.x + int(self.map_rect.width/12)
        self.mapy = display_height/6
        
        for room in room_names:
            if room_names[self.current_room] == room:
                self.draw_text(str(room), 15, red, int(self.mapx), self.mapy)
            else:
                self.draw_text(str(room), 15, orange, int(self.mapx), self.mapy)

            try:
                if room_names[self.current_room + 6] == room and self.down_text == True:
                    self.draw_text(str(room), 15, cyan, int(self.mapx), self.mapy)
            except IndexError:
                pass
            try:
                if room_names[self.current_room - 6] == room and self.up_text == True:
                    self.draw_text(str(room), 15, cyan, int(self.mapx), self.mapy)
            except IndexError:
                pass
            try:
                if room_names[self.current_room + 1] == room and self.right_text == True:
                    self.draw_text(str(room), 15, cyan, int(self.mapx), self.mapy)
            except IndexError:
                pass
            try:
                if room_names[self.current_room - 1] == room and self.left_text == True:
                    self.draw_text(str(room), 15, cyan, int(self.mapx), self.mapy)
            except IndexError:
                pass
            
            self.mapx += int(self.map_rect.width/6)
            self.room_index += 1
            if self.room_index % 6 == 0 and self.room_index != 0:
                self.mapx = self.map_rect.x + int(self.map_rect.width/12)
                self.mapy += display_height/6
                self.room_index = 0

    def shop(self):
        self.shopping = True
        self.typing = False
        self.input_text = ""
        self.purchasing_text1 = "Welcome to the shop! Would you like to buy anything"
        self.purchasing_text2 = "or would you like to leave?"
        shopping_button = Button("", self.font_name, 30, black, int((display_width/5)), int((display_height/5)*4), int((display_width/5)*3), int(display_height/10), yellow, cyan)
        while self.shopping:
            for event in p.event.get():
                if event.type == p.QUIT:
                    self.shopping = False
                    self.playing = False
                    self.active = False
                if event.type == p.KEYDOWN:
                    if self.typing:
                        if event.key == p.K_RETURN:
                            self.input_text = shopping_button.msg
                        elif event.key == p.K_BACKSPACE:
                            if not shopping_button.msg:
                                pass
                            else:
                                shopping_button.msg = shopping_button.msg[:-1]
                        elif event.key == p.K_SPACE:
                            shopping_button.msg += " "
                        else:
                            if len(p.key.name(event.key)) == 1:
                                if (ord(p.key.name(event.key)) >= 97 and ord(p.key.name(event.key)) <= 122 or
                                    ord(p.key.name(event.key)) >= 48 and ord(p.key.name(event.key)) <= 57):
                                    shopping_button.msg += str(p.key.name(event.key))

            self.screen.fill(black)
            self.draw_text("Coins: " + str(self.player_coins), 30, yellow, int(display_width/7), 50)
            self.draw_text("Shop", 100, white, int(display_width/2), 50)
            self.draw_text("--------------------------------------------------------------------------------", 30, white, int(display_width/2), 100)
            self.draw_text("Item", 30, orange, 100, 130)
            self.draw_text("Cost", 30, orange, 210, 130)
            self.draw_text("Description", 30, orange, 450, 130)
            
            for i, (item, desc) in enumerate(self.shop_items.items()):
                self.draw_text(str(item), 25, white, 100, 160 + (30 * i))
                self.draw_text(str(desc[0]) + " coins", 25, white, 210, 160 + (30 * i))
                self.draw_text(str(desc[1]), 25, white, 450, 160 + (30 * i))

            self.draw_text(self.purchasing_text1, 32, orange, display_width/2, display_height-180)
            self.draw_text(self.purchasing_text2, 32, orange, display_width/2, display_height-150)
            
            mouse_pos = p.mouse.get_pos()
            mouse_pressed = p.mouse.get_pressed()
                
            if not shopping_button.rect.collidepoint(mouse_pos):
                if mouse_pressed[0]:
                    self.typing = False
                    
            if shopping_button.is_pressed(mouse_pos, mouse_pressed):
                self.typing = True

            if not self.typing and not shopping_button.msg:
                shopping_button.text_colour = lightgrey
                shopping_button.msg = "Click to type what you want to buy"

            if self.typing:
                if shopping_button.msg == "Click to type what you want to buy":
                    shopping_button.msg = ""
                    shopping_button.text_colour = black
                shopping_button.image.fill(shopping_button.active_colour)

            shopping_button.load()

            if "buy" in self.input_text.lower() or "purchase" in self.input_text.lower():
                for item, desc in self.shop_items.items():
                    if str(item).lower() in self.input_text.lower():
                        try:
                            amount = int(''.join(filter(lambda x : x.isdigit(), self.input_text)))
                            if amount * int(desc[0]) <= self.player_coins:
                                self.take_coins_from_player(amount * int(desc[0]))
                                if item in self.player_inventory.keys():
                                    self.player_inventory[item] += int(amount)
                                else:
                                    self.player_inventory.update({item : amount})
                                self.purchasing_text1 = "Successfully bought " + str(amount) + " " + str(item) + " for " + str(amount * desc[0]) + " coins!"
                                self.purchasing_text2 = "You may purchase more, or choose to leave"
                                shopping_button.msg = ""
                                self.input_text = ""
                                self.typing = False
                            else:
                                self.purchasing_text1 = "You don't have enough coins to buy that many!"
                                self.purchasing_text2 = "Choose something else, or you may leave"
                                shopping_button.msg = ""
                                self.input_text = ""
                                self.typing = False
                        except ValueError:
                            if desc[0] <= self.player_coins:
                                self.take_coins_from_player(desc[0])
                                if item in self.player_inventory.keys():
                                    self.player_inventory[item] += 1
                                else:
                                    self.player_inventory.update({item : 1})
                                self.purchasing_text1 = "Successfully bought " + str(item) + " for " + str(desc[0]) + " coins!"
                                self.purchasing_text2 = "You may purchase more, or choose to leave"
                                shopping_button.msg = ""
                                self.input_text = ""
                                self.typing = False
                            else:
                                self.purchasing_text1 = "You don't have enough coins to buy that!"
                                self.purchasing_text2 = "Choose something else, or you may leave"
                                shopping_button.msg = ""
                                self.input_text = ""
                                self.typing = False

            if "leave" in self.input_text.lower():
                self.shopping = False

            if self.input_text:
                self.purchasing_text1 = "Unrecognised answer. Try including 'buy'"
                self.purchasing_text2 = "or 'leave' if you want to leave"
                shopping_button.msg = ""
                self.input_text = ""
                self.typing = False 
            p.display.update()

#---------------------------------Game Loop---------------------------------
g = Game()
g.intro_screen()
g.instructions_screen()
g.new(rooms[starting_room])
while g.active:
    g.run()
    g.game_over()
p.quit()
