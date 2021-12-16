import pygame as p
import time
from Settings2 import *
from Sprites2 import *
from Database2 import *
import json

#---------------------------------Game Class---------------------------------
class Game:
    #game class constructor
    def __init__(self):
        p.init()
        p.mixer.init()
        p.mixer.music.load("background_music.mp3")
        self.screen = p.display.set_mode((display_width,display_height))
        p.display.set_caption(title)
        self.clock = p.time.Clock()
        self.active = True
        self.font_name = p.font.match_font(font_name)
        self.message_queue = [None, None, None, None, None]
        self.colour_queue = [white, white, white, white, white]
        self.anagram_words = {"computer" : "has a CPU", "keyboard" : "an input device", "programming" : "coding", 
                            "internet" : "connection", "binary" : "base 2", "function" : "can accept parameters",
                            "generator" : "uses yield in python", "iteration" : "repetition", "hexadecimal" : "base 16", 
                            "algorithm" : "set of instructions", "software" : "a computer program", "processor" : "clock speed",
                            "interpreter" : "translates line-by-line", "compiler" : "translates to binary", 
                            "assembly" : "low-level language", "directory" : "path", "python" : "programming language",
                            "system" : "collection of components", "memory" : "storage location", 
                            "ascii" : "character encoding standard", "unicode" : "character encoding standard", 
                            "denary" : "base 10", "domain" : "targeted subject area", "encryption" : "secure transmittion"}

        self.character_spritesheet = Spritesheet("Images/character.png") #img (2020) img [Online]. Available at https://www.mediafire.com/file/024qld0tru7azh9/img.zip/file (Accessed 16 December 2021).
        self.terrain_spritesheet = Spritesheet("Images/terrain.png") #img (2020) img [Online]. Available at https://www.mediafire.com/file/024qld0tru7azh9/img.zip/file (Accessed 16 December 2021).
        self.enemies_spritesheet = Spritesheet("Images/enemy.png") #img (2020) img [Online]. Available at https://www.mediafire.com/file/024qld0tru7azh9/img.zip/file (Accessed 16 December 2021).
        self.coin_spritesheet = Spritesheet("Images/coin.png") #vhv.rshttps://www.vhv.rs/viewpic/hbibibJ_coins-clipart-sprite-coin-sprite-sheet-png-transparent/ (2019) Coins Clipart Sprite - Coin Sprite Sheet Png, Transparent Png - vhv [Online]. (Accessed 16 December 2021).
        self.wizard_spritesheet = Spritesheet("Images/wizard.png")
        self.chest_spritesheet = Spritesheet("Images/chest.png")
        self.npc_spritesheet = Spritesheet("Images/npcs.png") #img (2020) img [Online]. Available at https://www.mediafire.com/file/024qld0tru7azh9/img.zip/file (Accessed 16 December 2021).
        self.door_spritesheet = Spritesheet("Images/doors.png") #Pixilarthttps://www.pixilart.com/draw/pixel-door-0fc84f0c3d4c39f (2021) Pixilart [Online]. (Accessed 16 December 2021).

        self.player_health = player_health
        self.player_gold = 0
        self.player_sprite = ""
        self.player_name = ""

        self.current_room = starting_room
        self.show_map = False
        self.saved_elapsed_time = 0
        self.game_sound = True

        self.up_text = False
        self.down_text = False
        self.left_text = False
        self.right_text = False
        self.up_coords = ()
        self.down_coords = ()
        self.left_coords = ()
        self.right_coords = ()

        self.player_inventory = {}
    
    #function for drawing text
    def draw_text(self, text, size, colour, x, y):
        font = p.font.Font(self.font_name, size)
        text_surface = font.render(text, True, colour)
        text_rect = text_surface.get_rect(center=(int(x),int(y)))
        self.screen.blit(text_surface, text_rect)
    
    #decision function for managing user inputs
    def decision(self, show_room_info = True):

        #self.room_findings indices
        #0) quadrant_sting
        #1) player position in room
        #2) where player can move
        #3) list of items in area
        #4) is an exit
        #5) is a locked door
        #6) npc in area
        #7) chest in area
        #8) is a wizard in area
        self.update()
        self.draw()
        self.analysis = self.scan_room()
        self.actions = []
        self.text = "You are at the " + self.analysis[1] + " of " + room_names[self.current_room] + ". "
        if self.analysis[3] != None:
            self.text += "The room contains: " + ", ".join(self.analysis[3]) + ". "
            if "coin" in self.analysis[3]:
                self.actions.append("[collect]")
            if "enemy" in self.analysis[3]:
                self.actions.append("[fight]")
        else:
            self.text += "The area is empty. "
        if self.analysis[2] != None:
            self.text += "You can move " + " or ".join(self.analysis[2]) + ". "
            self.actions.append("[move]")
        if self.analysis[4] != None:
            self.text += "There is an exit. "
            self.actions.append("[exit]")
        if self.analysis[5] != None:
            if self.analysis[5] == "green door":
                self.text += "There is a green door. "
            elif self.analysis[5] == "blue door":
                self.text += "There is a blue door. "
            elif self.analysis[5] == "red door":
                self.text += "There is a red door. "
            elif self.analysis[5] == "yellow door":
                self.text += "There is a yellow door. "
            self.actions.append("[open]")
        if self.analysis[6] != None:
            for sprite in self.npcs:
                if sprite.npc_type == self.analysis[6]:
                    self.text += "You can speak to " + sprite.name + ", maybe he could help. "
                    self.actions.append("[speak]")
        if self.analysis[7] != None:
            for chest in self.chest:
                if chest.chest_type == self.analysis[7] and int(chest.chest_type) <= 4:
                    self.text += "There is a " + chest.name + " to search. "
                    self.actions.append("[search]")
        if self.analysis[8] != None:
            self.text += "You can approach a wizard, but be cautious... "
            self.actions.append("[approach]")
        self.actions.extend(("[view]", "[save]", "[quit]"))
        if show_room_info:
            self.write_text(self.text, colour=green)
        self.choice = ""
        self.found = False
        while not self.found:
            self.choice = self.write_text("What would you like to do? " + " ".join(self.actions), True, colour=lightgrey)
            if "move" in self.choice:
                if "[move]" in self.actions:
                    if self.choice.strip() == "move":
                        self.choice = self.write_text("Where would you like to move to? You can move " + " or ".join(self.analysis[2]), True, colour=cyan)
                    if self.analysis[2][0] in self.choice:
                        self.write_text("Moved " + self.analysis[2][0], colour=yellow)
                        self.move_player(self.analysis[2][0])
                        self.found = True
                    elif self.analysis[2][1] in self.choice:
                        self.write_text("Moved " + self.analysis[2][1], colour=yellow)
                        self.move_player(self.analysis[2][1])
                        self.found = True
                    else:
                        self.write_text("You cannot move that direction. Try moving " + " or ".join(self.analysis[2]), colour=red)
                else:
                    self.write_text("You cannot move from here",colour=red)
            elif "exit" in self.choice:
                if "[exit]" in self.actions:
                    self.player_found = False
                    self.write_text("You have left " + room_names[self.current_room], colour=yellow)
                    if self.analysis[1] == "top left": #if moving left
                        while self.player_sprite.rect.x >= -tile_size/2:
                            self.player_sprite.rect.x -= player_speed
                            self.player_sprite.movement("left")
                            self.clock.tick(FPS)
                            self.draw()
                            p.display.update()
                        self.current_room -= 1
                        self.change_room(rooms[self.current_room], int((display_width - tile_size)/tile_size), 6)
                        for i, row in enumerate(rooms[self.current_room]):
                            for j, column in enumerate(row):
                                if column == "P" and self.player_found == False:
                                    rooms[self.current_room][i] = rooms[self.current_room][i][:j] + "." + rooms[self.current_room][i][j+1:]
                                    self.player_found = True
                        rooms[self.current_room][6] = rooms[self.current_room][6][:14] + "P" + rooms[self.current_room][6][15:]
                        while self.player_sprite.rect.x >= 14 * tile_size:
                            self.player_sprite.rect.x -= player_speed
                            self.player_sprite.movement("left")
                            self.clock.tick(FPS)
                            self.draw()
                            p.display.update()
                        self.player_sprite.rect.x = 14 * tile_size
                        self.decision()
                        #self.current_room -= 1
                        #self.change_room(rooms[self.current_room], 14, 6)
                        
                    elif self.analysis[1] == "top right": #if moving up
                        while self.player_sprite.rect.y >= -tile_size:
                            self.player_sprite.rect.y -= player_speed
                            self.player_sprite.movement("up")
                            self.clock.tick(FPS)
                            self.draw()
                            p.display.update()
                        self.current_room -= 6
                        self.change_room(rooms[self.current_room], 5, int((display_height - tile_size * 6)/tile_size))
                        for i, row in enumerate(rooms[self.current_room]):
                            for j, column in enumerate(row):
                                if column == "P" and self.player_found == False:
                                    rooms[self.current_room][i] = rooms[self.current_room][i][:j] + "." + rooms[self.current_room][i][j+1:]
                                    self.player_found = True
                        rooms[self.current_room][6] = rooms[self.current_room][6][:5] + "P" + rooms[self.current_room][6][6:]
                        while self.player_sprite.rect.y >= 6 * tile_size:
                            self.player_sprite.rect.y -= player_speed
                            self.player_sprite.movement("up")
                            self.clock.tick(FPS)
                            self.draw()
                            p.display.update()
                        self.player_sprite.rect.y = 6 * tile_size
                        self.decision()
                        #self.current_room -= 6
                        #self.change_room(rooms[self.current_room], 5, 6)
                        
                    elif self.analysis[1] == "bottom left": #if moving down
                        while self.player_sprite.rect.y <= display_height - tile_size * 6 - player_speed:
                            self.player_sprite.rect.y += player_speed
                            self.player_sprite.movement("down")
                            self.clock.tick(FPS)
                            self.draw()
                            p.display.update()
                        self.current_room += 6
                        self.change_room(rooms[self.current_room], 14, 0)
                        for i, row in enumerate(rooms[self.current_room]):
                            for j, column in enumerate(row):
                                if column == "P" and self.player_found == False:
                                    rooms[self.current_room][i] = rooms[self.current_room][i][:j] + "." + rooms[self.current_room][i][j+1:]
                                    self.player_found = True
                        rooms[self.current_room][3] = rooms[self.current_room][3][:14] + "P" + rooms[self.current_room][3][15:]
                        while self.player_sprite.rect.y <= 3 * tile_size:
                            self.player_sprite.rect.y += player_speed
                            self.player_sprite.movement("down")
                            self.clock.tick(FPS)
                            self.draw()
                            p.display.update()
                        self.player_sprite.rect.y = 3 * tile_size
                        self.decision()
                        #self.current_room += 6
                        #self.change_room(rooms[self.current_room], 14, 3)
                        
                    elif self.analysis[1] == "bottom right": #if moving right
                        while self.player_sprite.rect.x <= display_width - tile_size:
                            self.player_sprite.rect.x += player_speed
                            self.player_sprite.movement("right")
                            self.clock.tick(FPS)
                            self.draw()
                            p.display.update()
                        self.current_room += 1
                        self.change_room(rooms[self.current_room], 0, 3)
                        for i, row in enumerate(rooms[self.current_room]):
                            for j, column in enumerate(row):
                                if column == "P" and self.player_found == False:
                                    rooms[self.current_room][i] = rooms[self.current_room][i][:j] + "." + rooms[self.current_room][i][j+1:]
                                    self.player_found = True
                        rooms[self.current_room][3] = rooms[self.current_room][3][:5] + "P" + rooms[self.current_room][3][6:]
                        while self.player_sprite.rect.x <= 5 * tile_size:
                            self.player_sprite.rect.x += player_speed
                            self.player_sprite.movement("right")
                            self.clock.tick(FPS)
                            self.draw()
                            p.display.update()
                        self.player_sprite.rect.x = 5 * tile_size
                        self.decision()
                        #self.current_room += 1
                        #self.change_room(rooms[self.current_room], 5, 3)
                else:
                    self.write_text("You cannot exit from here, try moving to do a different area of the room", colour=red)

            elif "open" in self.choice:
                if "[open]" in self.actions:
                    if self.choice.strip() == "open":
                        self.choice = self.write_text("What would you like to open? You can open the " + self.analysis[5], True, colour=cyan)
                    if "green door" in self.choice and "Green Key" in self.player_inventory.keys():
                        for i, row in enumerate(rooms[self.current_room]):
                            for j, column in enumerate(row):
                                if column == "|":
                                    rooms[self.current_room][i] = rooms[self.current_room][i][:j] + "*" + rooms[self.current_room][i][j+1:]
                                    Ground(self, j, i, True)
                        self.write_text("You have used the green key to open the green door", colour=yellow)
                        self.new(rooms[self.current_room], False)
                        self.draw()
                        self.update()
                        p.display.update()
                    elif "blue door" in self.choice and "Blue Key" in self.player_inventory.keys():
                        for i, row in enumerate(rooms[self.current_room]):
                            for j, column in enumerate(row):
                                if column == "-":
                                    rooms[self.current_room][i] = rooms[self.current_room][i][:j] + "*" + rooms[self.current_room][i][j+1:]
                                    Ground(self, j, i, True)
                        self.write_text("You have used the blue key to open the blue door", colour=yellow)
                        self.new(rooms[self.current_room], False)
                        self.draw()
                        self.update()
                        p.display.update()
                    elif "red door" in self.choice and "Red Key" in self.player_inventory.keys():
                        for i, row in enumerate(rooms[self.current_room]):
                            for j, column in enumerate(row):
                                if column == "=":
                                    rooms[self.current_room][i] = rooms[self.current_room][i][:j] + "*" + rooms[self.current_room][i][j+1:]
                                    Ground(self, j, i, True)
                        self.write_text("You have used the red key to open the red door", colour=yellow)
                        self.new(rooms[self.current_room], False)
                        self.draw()
                        self.update()
                        p.display.update()
                    elif "yellow door" in self.choice and "Yellow Key" in self.player_inventory.keys():
                        for i, row in enumerate(rooms[self.current_room]):
                            for j, column in enumerate(row):
                                if column == "~":
                                    rooms[self.current_room][i] = rooms[self.current_room][i][:j] + "*" + rooms[self.current_room][i][j+1:]
                                    Ground(self, j, i, True)
                        self.write_text("You have used the yellow key to open the yellow door", colour=yellow)
                        self.new(rooms[self.current_room], False)
                        self.draw()
                        self.update()
                        p.display.update()
                    elif "green door" in self.choice and "Green Key" not in self.player_inventory.keys():
                        self.write_text("It appears the green door is locked, there must be a key to open it somewhere...", colour=yellow)
                    elif "blue door" in self.choice and "Blue Key" not in self.player_inventory.keys():
                        self.write_text("It appears the blue door is locked, there must be a key to open it somewhere...", colour=yellow)
                    elif "red door" in self.choice and "Red Key" not in self.player_inventory.keys():
                        self.write_text("It appears the red door is locked, there must be a key to open it somewhere...", colour=yellow)
                    elif "yellow door" in self.choice and "Yellow Key" not in self.player_inventory.keys():
                        self.write_text("It appears the yellow door is locked, there must be a key to open it somewhere...", colour=yellow)
                    else:
                        self.write_text("There is no door to open named that, try opening " + self.analysis[5], colour=red)

                else:
                    self.write_text("There is nothing to open here, try looking for doors", colour=red)

            elif "speak" in self.choice:
                self.target_name = ""
                if "[speak]" in self.actions:
                    for sprite in self.npcs:
                        if sprite.npc_type == self.analysis[6]:
                            self.target_name = sprite.name
                    if self.choice.strip() == "speak":
                        self.choice = self.write_text("Who would you like to speak to? You can speak to " + self.target_name, True, colour=cyan)
                    if self.target_name.lower() in self.choice.lower():
                        if self.target_name == "Ash":
                            if "Green Key" in self.player_inventory.keys():
                                self.write_text("You have already spoken to Ash; he gave you the green key", colour=red)
                            else:
                                self.write_text("You spoke to " + sprite.name + " and he gave you a green key. Maybe it could unlock something...", colour=yellow)
                                self.player_inventory.update({"Green Key" : 1})
                        elif self.target_name == "Bazza":
                            if "Blue Key" in self.player_inventory.keys():
                                self.write_text("You have already spoken to Bazza; he gave you the blue key", colour=red)
                            else:
                                self.write_text("You spoke to " + sprite.name + " and he gave you a blue key. Maybe it could unlock something...", colour=yellow)
                                self.player_inventory.update({"Blue Key" : 1})
                        elif self.target_name == "Gordon":
                            if "Red Key" in self.player_inventory.keys():
                                self.write_text("You have already spoken to Gordon; he gave you the red key", colour=red)
                            else:
                                self.write_text("You spoke to " + sprite.name + " and he gave you a red key. Maybe it could unlock something...", colour=yellow)
                                self.player_inventory.update({"Red Key" : 1})
                        elif self.target_name == "Gale":
                            if "Yellow Key" in self.player_inventory.keys():
                                self.write_text("You have already spoken to Gale; he gave you the yellow key", colour=red)
                            else:
                                self.write_text("You spoke to " + sprite.name + " and he gave you a yellow key. Maybe it could unlock something...", colour=yellow)
                                self.player_inventory.update({"Yellow Key" : 1})
                        elif self.target_name == "Jerrard":
                            self.write_text("Jerrard tells you that he thinks the wall in the bottom right of " + room_names[18] + " looks unstable. He recommends punching the wall. Who knows what's on the other side...", colour=yellow)
                        elif self.target_name == "Roderick":
                            self.write_text("Roderick tells you that he has heard rumours from Jerrard about the room below. He recommends speaking to Jerrard.", colour=yellow)
                        elif self.target_name == "Kane":
                            self.write_text("Kane tells you that he has seen treasure chests hidden in some of the areas...", colour=yellow)
                        elif self.target_name == "Leo":
                            self.write_text("Leo warns you that although fighting enemies earns you gold, they can hurt you", colour=yellow)
                        elif self.target_name == "Eddie":
                            self.write_text("Eddie tells you that he last saw Jerrard in " + str(room_names[10]), colour=yellow)      
                    else:
                        self.write_text("There is nobody around to speak to with that name, try speaking with " + self.target_name, colour=red)
                else:
                    self.write_text("There is nobody to speak to in this area, try finding someone", colour=red)

            elif "search" in self.choice:
                self.target_chest = ""
                if "[search]" in self.actions:
                    for chest in self.chest:
                        if chest.chest_type == self.analysis[7]:
                            self.target_chest = chest.name
                    if self.choice.strip() == "search":
                        self.choice = self.write_text("What would you like to search? You can search " + self.target_chest, True, colour=cyan)
                    if self.target_chest in self.choice:
                        if self.target_chest == "yellow chest":
                            self.gold_to_player = random.randint(600,800)
                            self.give_gold_to_player(self.gold_to_player)
                            for i, row in enumerate(rooms[self.current_room]):
                                for j, column in enumerate(row):
                                    if column == "1":
                                        rooms[self.current_room][i] = rooms[self.current_room][i][:j] + "5" + rooms[self.current_room][i][j+1:]
                        elif self.target_chest == "green chest":
                            self.gold_to_player = random.randint(100,200)
                            self.give_gold_to_player(self.gold_to_player)
                            for i, row in enumerate(rooms[self.current_room]):
                                for j, column in enumerate(row):
                                    if column == "2":
                                        rooms[self.current_room][i] = rooms[self.current_room][i][:j] + "6" + rooms[self.current_room][i][j+1:]
                        elif self.target_chest == "red chest":
                            self.gold_to_player = random.randint(400,500)
                            self.give_gold_to_player(self.gold_to_player)
                            for i, row in enumerate(rooms[self.current_room]):
                                for j, column in enumerate(row):
                                    if column == "3":
                                        rooms[self.current_room][i] = rooms[self.current_room][i][:j] + "7" + rooms[self.current_room][i][j+1:]
                        elif self.target_chest == "blue chest":
                            self.gold_to_player = random.randint(250,350)
                            self.give_gold_to_player(self.gold_to_player)
                            for i, row in enumerate(rooms[self.current_room]):
                                for j, column in enumerate(row):
                                    if column == "4":
                                        rooms[self.current_room][i] = rooms[self.current_room][i][:j] + "8" + rooms[self.current_room][i][j+1:]
                        self.write_text("You have searched the " + self.target_chest + " and found " + str(self.gold_to_player) + " gold! You now have " + str(self.player_gold) + " gold!", colour=yellow)
                        self.new(rooms[self.current_room], False)
                        self.draw()
                        self.update()
                        p.display.update()
                    else:
                        self.write_text("There is nothing to search with that name, try searching the " + self.target_chest, colour=red)
                else:
                    self.write_text("There is nothing to search around here, try moving somewhere else", colour=red)
            elif "punch" in self.choice:
                if self.analysis[1] == "bottom right":
                    if self.current_room == 18:
                        rooms[self.current_room][6] = rooms[self.current_room][6][:19] + "*"
                        self.write_text("The wall has crumbled, revealing an entrance to a secret room...", colour=yellow)
                        self.new(rooms[self.current_room], False)
                        self.draw()
                        self.update()
                        p.display.update()
                    else:
                        self.write_text("Unknown action.", colour=red)
                else:
                    self.write_text("Unknown action.", colour=red)
            elif "fight" in self.choice:
                if "[fight]" in self.actions:
                    if self.choice.strip() == "fight":
                        self.choice = self.write_text("What would you like to fight? You can fight enemy", True, colour=cyan)
                    if "enemy" in self.choice:
                        for i, row in enumerate(rooms[self.current_room]):
                            for j, column in enumerate(row):
                                if column == "N":
                                    rooms[self.current_room][i] = rooms[self.current_room][i][:j] + "." + rooms[self.current_room][i][j+1:]
                        self.gold_to_player = random.randint(5,10)
                        self.give_gold_to_player(self.gold_to_player)
                        if random.randint(1,2) == 1:
                            self.write_text("You have killed the enemy and found " + str(self.gold_to_player) + " gold! You now have " + str(self.player_gold) + " gold!", colour=yellow)
                        else:
                            self.damage_to_player = random.randint(7,13)
                            self.damage_player(self.damage_to_player) 
                            self.write_text("You have killed the enemy and found " + str(self.gold_to_player) + " gold, but took " + str(self.damage_to_player) + " damage! You now have " + str(self.player_gold) + " gold and " + str(self.player_health) + " health!", colour=yellow)
                        self.new(rooms[self.current_room], False)
                        self.draw()
                        self.update()
                        p.display.update()
                    else:
                        self.write_text("There is nothing to fight here named that, try fighting enemy", colour=red)
                else:
                    self.write_text("There is nothing to fight here", colour=red)
            elif "collect" in self.choice:
                if "[collect]" in self.actions:
                    if self.choice.strip() == "collect":
                        self.choice = self.write_text("What would you like to collect? You can collect coin", True, colour=cyan)
                    if "coin" in self.choice:
                        for i, row in enumerate(rooms[self.current_room]):
                            for j, column in enumerate(row):
                                if column == "C":
                                    rooms[self.current_room][i] = rooms[self.current_room][i][:j] + "." + rooms[self.current_room][i][j+1:]
                        self.gold_to_player = random.randint(10,20)
                        self.give_gold_to_player(self.gold_to_player)
                        self.write_text("You have collected the coin and received " + str(self.gold_to_player) + " gold! You now have " + str(self.player_gold) + " gold!", colour=yellow)
                        self.new(rooms[self.current_room], False)
                        self.draw()
                        self.update()
                        p.display.update()
                    else:
                        self.write_text("There is nothing to collect here named that, try collecting coin", colour=red)
                else:
                    self.write_text("There is nothing to collect here", colour=red)
            elif "approach" in self.choice:
                if "[approach]" in self.actions:
                    if self.choice.strip() == "approach":
                        self.choice = self.write_text("Who would you like to approach? You can approach the wizard", True, colour=cyan)
                    if "wizard" in self.choice:
                        self.word = random.choice(list(self.anagram_words.keys()))
                        self.scrambled_word = self.anagram(self.word)
                        self.write_text("The wizard has offered you gold in exchange for solving this anagram:", colour=yellow)
                        self.guess = self.write_text(self.scrambled_word + "              hint: " + self.anagram_words[self.word], True, colour=yellow)
                        if self.guess.strip() == self.word:
                            self.gold_to_player = random.randint(3 * len(self.word), 5 * len(self.word))
                            self.give_gold_to_player(self.gold_to_player)
                            self.write_text("That was correct! The wizard grants you " + str(self.gold_to_player) + " gold! You now have " + str(self.player_gold) + " gold!", colour=yellow)
                        else:
                            self.gold_from_player = random.randint(5,15)
                            self.take_gold_from_player(self.gold_from_player)
                            self.write_text("That was incorrect! The wizard has stolen " + str(self.gold_from_player) + " gold! You now have " + str(self.player_gold) + " gold!", colour=yellow)
                        for i, row in enumerate(rooms[self.current_room]):
                            for j, column in enumerate(row):
                                if column == "W":
                                    rooms[self.current_room][i] = rooms[self.current_room][i][:j] + "." + rooms[self.current_room][i][j+1:]
                        self.write_text("The wizard has vanished!", colour=yellow)
                        self.new(rooms[self.current_room], False)
                        self.draw()
                        self.update()
                        p.display.update()
                    else:
                        self.write_text("There is nothing to approach here named that, try approaching wizard", colour=red)
                else:
                    self.write_text("There is nothing to approach here", colour=red)
            elif "view" in self.choice:
                if "[view]" in self.actions:
                    if self.choice.strip() == "view":
                        self.choice = self.write_text("What would you like to view? You can view your health, gold and inventory", True, colour=cyan)
                    if "health" in self.choice:
                        self.write_text("You have " + str(self.player_health) + " health.", colour=yellow)
                    elif "gold" in self.choice:
                        self.write_text("You have " + str(self.player_gold) + " gold.", colour=yellow)
                    elif "inventory" in self.choice:
                        if not self.player_inventory:
                            self.write_text("Your inventory is empty", colour=yellow)
                        else:
                            self.write_text("Your inventory contains " + ", ".join(["x" + str(value) + " " + key for key, value in self.player_inventory.items()]) + ".", colour=yellow)
            elif "quit" in self.choice:
                if "[quit]" in self.actions:
                    self.choice = self.write_text("Are you sure you want to end the game?", True, colour=cyan)
                    if self.choice.strip() == "yes":
                        p.quit()
                    else:
                        self.write_text("Game end aborted",colour=yellow)

            elif "save" in self.choice:
                if self.player_name:
                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    user_list = [] #list to hold JSON dictionary
                    user_dict = {"self.player_name" : self.player_name, #dictionary containing items wanting to add to dictionary
                                "self.current_room" : self.current_room,
                                "tilemap_room1" : tilemap_room1,
                                "tilemap_room2" : tilemap_room2,
                                "tilemap_room3" : tilemap_room3,
                                "tilemap_room4" : tilemap_room4,
                                "tilemap_room5" : tilemap_room5,
                                "tilemap_room6" : tilemap_room6,
                                "tilemap_room7" : tilemap_room7,
                                "tilemap_room8" : tilemap_room8,
                                "tilemap_room9" : tilemap_room9,
                                "tilemap_room10" : tilemap_room10,
                                "tilemap_room11" : tilemap_room11,
                                "tilemap_room12" : tilemap_room12,
                                "tilemap_room13" : tilemap_room13,
                                "tilemap_room14" : tilemap_room14,
                                "tilemap_room15" : tilemap_room15,
                                "tilemap_room16" : tilemap_room16,
                                "tilemap_room17" : tilemap_room17,
                                "tilemap_room18" : tilemap_room18,
                                "tilemap_room19" : tilemap_room19,
                                "tilemap_room20" : tilemap_room20,
                                "tilemap_room21" : tilemap_room21,
                                "tilemap_room22" : tilemap_room22,
                                "tilemap_room23" : tilemap_room23,
                                "tilemap_room24" : tilemap_room24,
                                "self.player_sprite.rect.x" : self.player_sprite.rect.x,
                                "self.player_sprite.rect.y" : self.player_sprite.rect.y,
                                "self.player_inventory" : self.player_inventory,
                                "self.player_health" : self.player_health,
                                "self.player_gold" : self.player_gold,
                                "self.saved_elapsed_time" : self.saved_elapsed_time + elapsed_time}
                    with open("saved data.json", "r") as file:
                        for obj in file:                    #for each object in the json file
                            json_dict = json.loads(obj)         #load the object into a variable
                            user_list.append(json_dict)         #and append it to user_list
                        file.close()
                    with open("saved data.json", "w") as file:
                        if not user_list:                     #if file was empty before the wipe
                            string = json.dumps([user_dict])          #just add the dictionary to the new empty file
                            file.write(string)
                        else:                               #otherwise
                            self.dict_found = False
                            for element in user_list:    
                                for user in element:           #for each dictionary in user_list
                                    if user["self.player_name"] == self.player_name: #if the dictionary was a save from the current player
                                        element[element.index(user)] = user_dict #override the contents with the new save
                                        self.dict_found = True
                            if self.dict_found:
                                for element in user_list:
                                    string = json.dumps(element)
                                    file.write(string)
                            if not self.dict_found:   #if user doesn't have a previous save
                                for element in user_list:
                                    element.append(user_dict) #add the dictionary to the user_list list as a new save for the user
                                for element in user_list:       #for each dictionary in user_list
                                    string = json.dumps(element)        #add the dictionary to the file
                                    file.write(string)
                        file.close()
                    self.write_text("Progress has been saved!", colour=yellow) #finally, let the user know their progress is saved

                else:
                    self.write_text("Unable to save!", colour=red)
            elif "die" in self.choice:
                self.damage_player(self.player_health)

            elif "win" in self.choice:
                self.game_complete()
            
            elif "give" in self.choice:
                amount = int(''.join(filter(lambda x : x.isdigit(), self.choice)))
                self.give_gold_to_player(amount)
                self.write_text("Received " + str(amount) + " gold. Gold: " + str(self.player_gold), colour=yellow)
                
            else:
                self.write_text("Unknown action.", colour=red)

    #new game function for when game starts   
    def new(self, room, show_room_info = True):
        self.playing = True
        self.all_sprites = p.sprite.LayeredUpdates()
        self.player = p.sprite.LayeredUpdates()
        self.blocks = p.sprite.LayeredUpdates()
        self.enemies = p.sprite.LayeredUpdates()
        self.coins = p.sprite.LayeredUpdates()
        self.wizard = p.sprite.LayeredUpdates()
        self.chest = p.sprite.LayeredUpdates()
        self.npcs = p.sprite.LayeredUpdates()
        self.doors = p.sprite.LayeredUpdates()

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
                if column == "1":
                    Chest(self, j, i, "1")
                if column == "2":
                    Chest(self, j, i, "2")
                if column == "3":
                    Chest(self, j, i, "3")
                if column == "4":
                    Chest(self, j, i, "4")
                if column == "5":
                    Chest(self, j, i, "5")
                if column == "6":
                    Chest(self, j, i, "6")
                if column == "7":
                    Chest(self, j, i, "7")
                if column == "8":
                    Chest(self, j, i, "8")
                if column == "!":
                    NPC(self, j, i, "!")
                if column == ":":
                    NPC(self, j, i, ":")
                if column == ";":
                    NPC(self, j, i, ";")
                if column == "(":
                    NPC(self, j, i, "(")
                if column == ")":
                    NPC(self, j, i, ")")
                if column == "[":
                    NPC(self, j, i, "[")
                if column == "]":
                    NPC(self, j, i, "]")
                if column == "{":
                    NPC(self, j, i, "{")
                if column == "}":
                    NPC(self, j, i, "}")
                if column == "|":
                    Door(self, j, i, "|")
                if column == "-":
                    Door(self, j, i, "-")
                if column == "=":
                    Door(self, j, i, "=")
                if column == "~":
                    Door(self, j, i, "~")
                if column == "*":
                    Door(self, j, i, "*")
                 
        if show_room_info:    
            self.decision()
        else:
            self.decision(False)

    #movement function                   
    def move_player(self, direction):
        self.found = False
        if direction == "north":
            for i, row in enumerate(rooms[self.current_room]):
                for j, column in enumerate(row):
                    if column == "P" and self.found == False:
                        rooms[self.current_room][i] = rooms[self.current_room][i][:j] + "." + rooms[self.current_room][i][j+1:]
                        rooms[self.current_room][i-3] = rooms[self.current_room][i-3][:j] + "P" + rooms[self.current_room][i-3][j+1:]
                        while self.player_sprite.rect.y != (i-3) * tile_size:
                            self.player_sprite.rect.y -= player_speed
                            self.player_sprite.movement("up")
                            self.clock.tick(FPS)
                            self.draw()
                            p.display.update()
                        self.found = True
                        break
                        

        elif direction == "south":
            for i, row in enumerate(rooms[self.current_room]):
                for j, column in enumerate(row):
                    if column == "P" and self.found == False:
                        rooms[self.current_room][i] = rooms[self.current_room][i][:j] + "." + rooms[self.current_room][i][j+1:]
                        rooms[self.current_room][i+3] = rooms[self.current_room][i+3][:j] + "P" + rooms[self.current_room][i+3][j+1:]
                        while self.player_sprite.rect.y != (i+3) * tile_size:
                            self.player_sprite.rect.y += player_speed
                            self.player_sprite.movement("down")
                            self.clock.tick(FPS)
                            self.draw()
                            p.display.update()
                        self.found = True
                        break

        elif direction == "east":
            for i, row in enumerate(rooms[self.current_room]):
                for j, column in enumerate(row):
                    if column == "P" and self.found == False:
                        rooms[self.current_room][i] = rooms[self.current_room][i][:j] + "." + rooms[self.current_room][i][j+1:]
                        rooms[self.current_room][i] = rooms[self.current_room][i][:j+9] + "P" + rooms[self.current_room][i][j+10:]
                        while self.player_sprite.rect.x != (j+9) * tile_size:
                            self.player_sprite.rect.x += player_speed
                            self.player_sprite.movement("right")
                            self.clock.tick(FPS)
                            self.draw()
                            p.display.update()
                        self.found = True
                        break

        elif direction == "west":
            for i, row in enumerate(rooms[self.current_room]):
                for j, column in enumerate(row):
                    if column == "P" and self.found == False:
                        rooms[self.current_room][i] = rooms[self.current_room][i][:j] + "." + rooms[self.current_room][i][j+1:]
                        rooms[self.current_room][i] = rooms[self.current_room][i][:j-9] + "P" + rooms[self.current_room][i][j-8:]
                        while self.player_sprite.rect.x != (j-9) * tile_size:
                            self.player_sprite.rect.x -= player_speed
                            self.player_sprite.movement("left")
                            self.clock.tick(FPS)
                            self.draw()
                            p.display.update()
                        self.found = True
                        break
                
        self.decision()

    #change room function for when player enters a new room     
    def change_room(self, room, playerx, playery):
        #player enters new room - room is changed
        if self.current_room == 0:
            self.game_complete()
        self.up_text = False
        self.down_text = False
        self.left_text = False
        self.right_text = False
        self.playing = True
        self.all_sprites = p.sprite.LayeredUpdates()
        self.player = p.sprite.LayeredUpdates()
        self.blocks = p.sprite.LayeredUpdates()
        self.enemies = p.sprite.LayeredUpdates()
        self.coins = p.sprite.LayeredUpdates()
        self.wizard = p.sprite.LayeredUpdates()
        self.chest = p.sprite.LayeredUpdates()
        self.npcs = p.sprite.LayeredUpdates()
        self.doors = p.sprite.LayeredUpdates()

        for i, row in enumerate(room):
            for j, column in enumerate(row):
                Ground(self, j, i)
                if column == "B":
                    Block(self, j, i)
                if column == "N":
                    Enemy(self, j, i)
                if column == "P":
                    Player(self, int(playerx), int(playery))
                if column == "C":
                    Coin(self, j, i)
                if column == "W":
                    Wizard(self, j, i)
                if column == "1":
                    Chest(self, j, i, "1")
                if column == "2":
                    Chest(self, j, i, "2")
                if column == "3":
                    Chest(self, j, i, "3")
                if column == "4":
                    Chest(self, j, i, "4")
                if column == "5":
                    Chest(self, j, i, "5")
                if column == "6":
                    Chest(self, j, i, "6")
                if column == "7":
                    Chest(self, j, i, "7")
                if column == "8":
                    Chest(self, j, i, "8")
                if column == "!":
                    NPC(self, j, i, "!")
                if column == ":":
                    NPC(self, j, i, ":")
                if column == ";":
                    NPC(self, j, i, ";")
                if column == "(":
                    NPC(self, j, i, "(")
                if column == ")":
                    NPC(self, j, i, ")")
                if column == "[":
                    NPC(self, j, i, "[")
                if column == "]":
                    NPC(self, j, i, "]")
                if column == "{":
                    NPC(self, j, i, "{")
                if column == "}":
                    NPC(self, j, i, "}")
                if column == "|":
                    Door(self, j, i, "|")
                if column == "-":
                    Door(self, j, i, "-")
                if column == "=":
                    Door(self, j, i, "=")
                if column == "~":
                    Door(self, j, i, "~")
                if column == "*":
                    Door(self, j, i, "*")

    #running function
    def run(self):
        #game loop
        while self.playing:
            self.draw()
            self.events()
            self.update()

    #drawing function for drawing sprites and cross on screen
    def draw(self):
        self.all_sprites.draw(self.screen)
        p.draw.rect(self.screen, lightgrey, p.Rect(int(display_width/2), 0, 1, int(display_height - 5 * tile_size)))
        p.draw.rect(self.screen, lightgrey, p.Rect(0, int((display_height - 5 * tile_size)/2), display_width, 1))
        self.clock.tick(FPS)

    #events function manages events
    def events(self):
        #game loop events
        for event in p.event.get():
            if event.type == p.QUIT:
                self.playing = False
                self.active = False
                p.quit()
            if event.type == p.KEYDOWN:
                if event.key == p.K_m:
                    if self.show_map == False:
                        self.show_map = True
                    else:
                        self.show_map = False
                if event.key == p.K_r:
                    self.write_text((chr(random.randint(96,122)) + chr(random.randint(96,122))) * 20)

        if self.show_map == True:
            self.display_map()

    #update function which refreshes screen and updates sprites            
    def update(self):
        #game loop updates
        self.all_sprites.update()
        p.display.update()

    #intro screen function
    def intro_screen(self):
        global tilemap_room1
        global tilemap_room2
        global tilemap_room3
        global tilemap_room4
        global tilemap_room5
        global tilemap_room6
        global tilemap_room7
        global tilemap_room8
        global tilemap_room9
        global tilemap_room10
        global tilemap_room11
        global tilemap_room12
        global tilemap_room13
        global tilemap_room14
        global tilemap_room15
        global tilemap_room16
        global tilemap_room17
        global tilemap_room18
        global tilemap_room19
        global tilemap_room20
        global tilemap_room21
        global tilemap_room22
        global tilemap_room23
        global tilemap_room24
        global rooms
        global start_time
        
        self.intro = True
        self.can_click = True

        play_button = Button("Start", self.font_name, 30, black, int((display_width/5)*2), int((display_height/5)*2), int(display_width/5), int(display_height/10), blue, cyan)
        load_button = Button("Load", self.font_name, 30, black, int((display_width/5)*2), int((display_height/5)*3), int(display_width/5), int(display_height/10), blue, cyan)
        login_button = Button("Login", self.font_name, 30, black, int((display_width/5)*1), int((display_height/5)*4), int(display_width/5), int(display_height/10), blue, cyan)
        register_button = Button("Register", self.font_name, 30, black, int((display_width/5)*3), int((display_height/5)*4), int(display_width/5), int(display_height/10), blue, cyan)
        logout_button = Button("Logout", self.font_name, 30, black, int((display_width/5)*2), int((display_height/5)*4), int(display_width/5), int(display_height/10), blue, cyan)
        music_button = Button("Mute Music", self.font_name, 30, black, int((display_width/5)*3.5), int((display_height/20)), int(display_width/4), int(display_height/10), blue, cyan)

        while self.intro:
            for event in p.event.get():
                if event.type == p.QUIT:
                    self.intro = False
                    self.playing = False
                    self.active = False
                    p.quit()

            mouse_pos = p.mouse.get_pos()
            mouse_pressed = p.mouse.get_pressed()

            self.screen.fill(yellow)
            self.draw_text(title, 100, black, int(display_width/2), int(display_height/5))
            music_button.load()

            if not mouse_pressed[0]:
                self.can_click = True

            if self.game_sound:
                music_button.msg = "Mute Music"
            elif not self.game_sound:
                music_button.msg = "Unmute Music"

            if music_button.is_pressed(mouse_pos, mouse_pressed) and self.can_click:
                if self.game_sound:
                    self.game_sound = False
                elif not self.game_sound:
                    self.game_sound = True
                self.can_click = False
            
            if self.player_name:
                play_button.load()
                load_button.load()
                logout_button.load()
                self.draw_text("Hello, " + str(self.player_name), 30, black, int(display_width/2), int((display_height/5)*0.25))

                if play_button.is_pressed(mouse_pos, mouse_pressed):
                    start_time = time.time()
                    if self.game_sound:
                        p.mixer.music.play(-1)
                    self.new(rooms[starting_room])

                if load_button.is_pressed(mouse_pos, mouse_pressed):
                    try:
                        json_data = []
                        with open("saved data.json", "r") as file:
                            for object in file:
                                json_data.append(json.loads(object))
                        for object in json_data:
                            for user in object:
                                if self.player_name == user['self.player_name']:                                
                                    self.current_room = user['self.current_room']
                                    tilemap_room1 = user['tilemap_room1']
                                    tilemap_room2 = user['tilemap_room2']
                                    tilemap_room3 = user['tilemap_room3']
                                    tilemap_room4 = user['tilemap_room4']
                                    tilemap_room5 = user['tilemap_room5']
                                    tilemap_room6 = user['tilemap_room6']
                                    tilemap_room7 = user['tilemap_room7']
                                    tilemap_room8 = user['tilemap_room8']
                                    tilemap_room9 = user['tilemap_room9']
                                    tilemap_room10 = user['tilemap_room10']
                                    tilemap_room11 = user['tilemap_room11']
                                    tilemap_room12 = user['tilemap_room12']
                                    tilemap_room13 = user['tilemap_room13']
                                    tilemap_room14 = user['tilemap_room14']
                                    tilemap_room15 = user['tilemap_room15']
                                    tilemap_room16 = user['tilemap_room16']                              
                                    tilemap_room17 = user['tilemap_room17']                                
                                    tilemap_room18 = user['tilemap_room18']                              
                                    tilemap_room19 = user['tilemap_room19']                            
                                    tilemap_room20 = user['tilemap_room20']                              
                                    tilemap_room21 = user['tilemap_room21']                              
                                    tilemap_room22 = user['tilemap_room22']                          
                                    tilemap_room23 = user['tilemap_room23']                            
                                    tilemap_room24 = user['tilemap_room24']  
                                    self.saved_elapsed_time = user['self.saved_elapsed_time']             
                                    xPos = int(user['self.player_sprite.rect.x']/32)
                                    yPos = int(user['self.player_sprite.rect.y']/32)
                                    self.player_inventory =  user['self.player_inventory']
                                    self.player_health =  user['self.player_health']
                                    self.player_gold =  user['self.player_gold']
                        if xPos == 5 and yPos == 3: #top left
                            rooms[self.current_room][3] = rooms[self.current_room][3][:5] + "P" + rooms[self.current_room][3][6:]
                        elif xPos == 14 and yPos == 3: #top right
                            rooms[self.current_room][3] = rooms[self.current_room][3][:14] + "P" + rooms[self.current_room][3][15:]
                        elif xPos == 5 and yPos == 6: #bottom left
                            rooms[self.current_room][6] = rooms[self.current_room][6][:5] + "P" + rooms[self.current_room][6][6:]
                        elif xPos == 14 and yPos == 6: #bottom right
                            rooms[self.current_room][6] = rooms[self.current_room][6][:14] + "P" + rooms[self.current_room][6][15:]
                        rooms = [tilemap_room24,tilemap_room23,tilemap_room22,tilemap_room21,tilemap_room20,tilemap_room19,
                                tilemap_room8,tilemap_room9,tilemap_room10,tilemap_room11,tilemap_room12,tilemap_room18,
                                tilemap_room5,tilemap_room4,tilemap_room2,tilemap_room3,tilemap_room13,tilemap_room17,
                                tilemap_room6,tilemap_room7,tilemap_room1,tilemap_room16,tilemap_room14,tilemap_room15
                                ]
                        self.intro = False
                        start_time = time.time()
                        if self.game_sound:
                            p.mixer.music.play(-1)
                        self.change_room(rooms[self.current_room], xPos, yPos)
                        self.update()
                        self.decision()

                    except:
                        pass
            
                if logout_button.is_pressed(mouse_pos, mouse_pressed):
                    self.player_name = ""
            
            else:
                self.draw_text("Login or register below", 32, black, int((display_width/2)), int((display_height/5)*3.5))
                login_button.load()
                register_button.load()

                if login_button.is_pressed(mouse_pos, mouse_pressed):
                    self.login_screen()

                if register_button.is_pressed(mouse_pos, mouse_pressed):
                    self.register_screen()
                
            p.display.update()
            self.clock.tick(FPS)
        self.screen.fill(black)

    #game over screen function        
    def game_over(self):
        p.mixer.music.stop()
        exit_button = Button("Exit", self.font_name, 30, black, int((display_width/5)*2), int((display_height/5)*2), int(display_width/5), int(display_height/10), blue, cyan)

        for sprite in self.all_sprites:
            sprite.kill()

        while self.active:
            for event in p.event.get():
                if event.type == p.QUIT:
                    self.active = False
                    p.quit()
            
            mouse_pos = p.mouse.get_pos()
            mouse_pressed = p.mouse.get_pressed()

            if exit_button.is_pressed(mouse_pos, mouse_pressed):
                p.quit()

            self.screen.fill(red)
            self.draw_text("Game Over", 100, black, int(display_width/2), int(display_height/5))
            exit_button.load()
            self.clock.tick(FPS)
            p.display.update()

    #function to wait for c key to be pressed before continuing
    def wait_for_key(self):
        p.display.update()
        while not p.key.get_pressed()[p.K_c]:
            for event in p.event.get():
                if event.type == p.QUIT:
                    self.playing = False
                    self.active = False
                    p.quit()
                if event.type == p.KEYDOWN:
                    if event.key == p.K_c:
                        pass

    #damage player function to take health from player
    def damage_player(self, damage_taken):
        self.player_health -= damage_taken
        if self.player_health <= 0:
            self.game_over()

    #heal player function to give player health
    def heal_player(self, heal_amount):
        if player_health - heal_amount > self.player_health:
            self.player_health += heal_amount
        else:
            self.player_health = player_health

    #give gold function to give gold to player        
    def give_gold_to_player(self, gold):
        self.player_gold += gold

    #take gold function to take gold from player
    def take_gold_from_player(self, gold):
        if self.player_gold - gold >= 0:
            self.player_gold -= gold
        else:
            self.player_gold = 0

    #add text function to add user input to screen
    def add_text(self, text, y, colour):
        font = p.font.Font(self.font_name, 23)
        text_surface = font.render(text, True, colour)
        text_rect = text_surface.get_rect(midleft=(int(10),int(display_height - tile_size * (4.5 - y))))
        self.screen.blit(text_surface, text_rect)

    #write text function to control where text it written on the screen, including order and colour
    def write_text(self, text, type_after=False, colour=white):
        self.text2 = ""
        self.maxchar = 80

        if len(self.colour_queue) == 5:
            if self.message_queue[-1] == "|":
                del self.colour_queue[-1]
            else:
                del self.colour_queue[0]
            self.colour_queue.append(colour)

        if len(text) > self.maxchar:
            i = text.rfind(" ", 0, self.maxchar)
            self.text2 = text[i + 1:]
            text = text[:i]
            
        p.draw.rect(self.screen, black, p.Rect(0,display_height - tile_size * 5, display_width, tile_size * 5))
        if len(self.message_queue) == 5:
            if self.message_queue[-1] == "|":
                del self.message_queue[-1]
            else:
                del self.message_queue[0]
            self.message_queue.append(text)
            for i, msg in enumerate(self.message_queue):
                if msg == None:
                    continue
                self.add_text(msg, i, self.colour_queue[i])

        if self.text2:
            self.write_text(self.text2, colour=colour)

        if type_after == True:
            self.write_text("|")
            self.typing = True
            self.input_text = ""
            self.user_input = ""
            while self.typing:
                for event in p.event.get():
                    if event.type == p.QUIT:
                        self.typing = False
                        self.playing = False
                        self.active = False
                        p.quit()
                    if event.type == p.KEYDOWN:
                        if event.key == p.K_RETURN:
                            self.input_text = self.user_input
                            self.write_text(self.user_input)
                            return self.input_text
                        elif event.key == p.K_BACKSPACE:
                            if not self.user_input:
                                pass
                            else:
                                self.user_input = self.user_input[:-1]
                        elif event.key == p.K_SPACE:
                            self.user_input += " "
                        else:
                            if len(p.key.name(event.key)) == 1:
                                if (ord(p.key.name(event.key)) >= 97 and ord(p.key.name(event.key)) <= 122 or
                                    ord(p.key.name(event.key)) >= 48 and ord(p.key.name(event.key)) <= 57) and (
                                    len(self.user_input) <= self.maxchar - 30):
                                    self.user_input += str(p.key.name(event.key))
                        p.draw.rect(self.screen, black, p.Rect(0,display_height - tile_size, display_width, tile_size))
                        self.add_text(self.user_input, 4, self.colour_queue[-1])
                p.display.update()

    #function to scan room and determine what is within the quadrant the user is in
    def scan_room(self):
        #self.room_findings indices
        #0) quadrant_sting
        #1) player position in room
        #2) where player can move
        #3) list of items in area
        #4) is an exit
        #5) is a locked door
        #6) npc in area
        #7) chest in area
        #8) is a wizard in area
        self.room_findings = []
        self.quadrant_string = ""
        self.quadrant = ""
        self.can_move = []
        
        self.player_found = False
        if not self.player_found:
            for y, row in enumerate(rooms[self.current_room]): #top left
                for x, column in enumerate(row):
                    if x < len(rooms[self.current_room][y])/2 and y < len(rooms[self.current_room])/2:
                        if column == "P":
                            self.player_found = True
                            self.quadrant = "top left"
                            for y, row in enumerate(rooms[self.current_room]): #top left
                                for x, column in enumerate(row):
                                    if x < len(rooms[self.current_room][y])/2 and y < len(rooms[self.current_room])/2:
                                        self.quadrant_string += column
                            break
                                        

        if not self.player_found:
            for y, row in enumerate(rooms[self.current_room]): #top right
                for x, column in enumerate(row):
                    if x >= len(rooms[self.current_room][y])/2 and y < len(rooms[self.current_room])/2:
                        if column == "P":
                            self.player_found = True
                            self.quadrant = "top right"
                            for y, row in enumerate(rooms[self.current_room]): #top right
                                for x, column in enumerate(row):
                                    if x >= len(rooms[self.current_room][y])/2 and y < len(rooms[self.current_room])/2:
                                        self.quadrant_string += column
                            break

        if not self.player_found:
            for y, row in enumerate(rooms[self.current_room]): #bottom left
                for x, column in enumerate(row):
                    if x < len(rooms[self.current_room][y])/2 and y >= len(rooms[self.current_room])/2:
                        if column == "P":
                            self.player_found = True
                            self.quadrant = "bottom left"
                            for y, row in enumerate(rooms[self.current_room]): #bottom left
                                for x, column in enumerate(row):
                                    if x < len(rooms[self.current_room][y])/2 and y >= len(rooms[self.current_room])/2:
                                        self.quadrant_string += column
                            break

        if not self.player_found:
            for y, row in enumerate(rooms[self.current_room]): #bottom right
                for x, column in enumerate(row):
                    if x >= len(rooms[self.current_room][y])/2 and y >= len(rooms[self.current_room])/2:
                        if column == "P":
                            self.player_found = True
                            self.quadrant = "bottom right"
                            for y, row in enumerate(rooms[self.current_room]): #bottom right
                                for x, column in enumerate(row):
                                    if x >= len(rooms[self.current_room][y])/2 and y >= len(rooms[self.current_room])/2:
                                        self.quadrant_string += column
                            break

        if self.quadrant == "top left":
            self.can_move.extend(("east", "south"))
        elif self.quadrant == "top right":
            self.can_move.extend(("west", "south"))
        elif self.quadrant == "bottom left":
            self.can_move.extend(("east", "north"))
        elif self.quadrant == "bottom right":
            self.can_move.extend(("west", "north"))
            
        self.room_findings.extend((self.quadrant_string, self.quadrant, self.can_move))

        self.room_items = []
        if "N" in self.quadrant_string:
            self.room_items.append("enemy")
        if "C" in self.quadrant_string:
            self.room_items.append("coin")

        self.room_findings.append(self.room_items) if self.room_items else self.room_findings.append(None)

        self.room_findings.append("exit") if "*" in self.quadrant_string else self.room_findings.append(None)

        if "|" in self.quadrant_string:
            self.room_findings.append("green door")
        elif "-" in self.quadrant_string:
            self.room_findings.append("blue door")
        elif "=" in self.quadrant_string:
            self.room_findings.append("red door")
        elif "~" in self.quadrant_string:
            self.room_findings.append("yellow door")
        else:
            self.room_findings.append(None)  

        if "!" in self.quadrant_string:   
            self.room_findings.append("!")
        elif ":" in self.quadrant_string:
            self.room_findings.append(":")
        elif ";" in self.quadrant_string:
            self.room_findings.append(";")
        elif "(" in self.quadrant_string:
            self.room_findings.append("(")
        elif ")" in self.quadrant_string:
            self.room_findings.append(")")
        elif "[" in self.quadrant_string:
            self.room_findings.append("[")
        elif "]" in self.quadrant_string:
            self.room_findings.append("]")
        elif "{" in self.quadrant_string:
            self.room_findings.append("{")
        elif "}" in self.quadrant_string:
            self.room_findings.append("}")
        else:
            self.room_findings.append(None)

        if "1" in self.quadrant_string:
            self.room_findings.append("1")
        elif "2" in self.quadrant_string:
            self.room_findings.append("2")
        elif "3" in self.quadrant_string:
            self.room_findings.append("3")
        elif "4" in self.quadrant_string:
            self.room_findings.append("4")
        elif "5" in self.quadrant_string:
            self.room_findings.append("5")
        elif "6" in self.quadrant_string:
            self.room_findings.append("6")
        elif "7" in self.quadrant_string:
            self.room_findings.append("7")
        elif "8" in self.quadrant_string:
            self.room_findings.append("8")
        else:
            self.room_findings.append(None)
        
        self.room_findings.append("wizard") if "W" in self.quadrant_string else self.room_findings.append(None)
            
        return self.room_findings

    #anagram function which scrambles a word and returns the scrambled word
    def anagram(self, word):
        letters = []
        for letter in word:
            letters.append(letter)
        random.shuffle(letters)
        return "".join(letters)

    #game complete function onces player has escaped dungeon
    def game_complete(self):
        p.mixer.music.stop()
        global end_time
        exit_button = Button("Exit", self.font_name, 30, black, int((display_width/5)*2), int((display_height/5)*4), int(display_width/5), int(display_height/10), blue, cyan)
        byGold_button = Button("Sort by Gold", self.font_name, 30, black, int((display_width/20)), int((display_height/5)*2), int(display_width/5), int(display_height/10), blue, cyan)
        byTime_button = Button("Sort by Time", self.font_name, 30, black, int((display_width/20)), int((display_height/5)*2.6), int(display_width/5), int(display_height/10), blue, cyan)
        
        sort_by_gold = True
        sort_by_time = False

        end_time = time.time()
        elapsed_time = int(end_time - start_time + self.saved_elapsed_time)
        time_taken = ""
        minutes = elapsed_time//60
        minutes_remainder = elapsed_time%60
        seconds = minutes_remainder
        if minutes > 0:
            time_taken += str(minutes) + " minutes, "
        time_taken += str(seconds) + " seconds"

        user_list = []
        with open("saved data.json", "r") as file:
            for obj in file:                    #for each object in the json file
                json_dict = json.loads(obj)         #load the object into a variable
                user_list.append(json_dict)         #and append it to user_list
            file.close()
        with open("saved data.json", "w") as file:
            self.dict_found = False
            for element in user_list:    
                for user in element:           #for each dictionary in user_list
                    if user["self.player_name"] == self.player_name: #if the dictionary was a save from the current player
                        del element[element.index(user)]  #delete the save
                        self.dict_found = True
            for element in user_list:       #for each dictionary in user_list
                string = json.dumps(element)        #add the dictionary to the file
                file.write(string)
            file.close()

        add_user_score_to_database(self.player_name, self.player_gold, elapsed_time)

        for sprite in self.all_sprites:
            sprite.kill()

        while self.active:
            for event in p.event.get():
                if event.type == p.QUIT:
                    self.active = False
                    p.quit()
            
            mouse_pos = p.mouse.get_pos()
            mouse_pressed = p.mouse.get_pressed()

            if exit_button.is_pressed(mouse_pos, mouse_pressed):
                p.quit()
            
            if byGold_button.is_pressed(mouse_pos, mouse_pressed):
                sort_by_gold = True
                sort_by_time = False
            
            if byTime_button.is_pressed(mouse_pos, mouse_pressed):
                sort_by_time = True
                sort_by_gold = False

            self.screen.fill(lime)

            self.draw_text("You have escaped with " + str(self.player_gold) + " gold in", 45, black, int(display_width/2), int((display_height/5)*0.5))
            self.draw_text(time_taken, 40, black, int(display_width/2), int((display_height/5)))

            self.draw_text("Highscores:", 35, black, int((display_width/5)*3), int((display_height/5)*1.5))

            if sort_by_gold:
                highscores = get_all_highscores_by_gold()
            elif sort_by_time:
                highscores = get_all_highscores_by_time()
            for i, entry in enumerate(highscores):
                if i > 4:
                    break
                self.draw_text(str(entry[0]) + ": " + str(entry[1]) + " gold in " + str(entry[2]) + " seconds", 28, black, int((display_width/5)*3), int((display_height/5)*(1.5 + 0.35 * (1 + i))))
           
            exit_button.load()
            byGold_button.load()
            byTime_button.load()
            
            self.clock.tick(FPS)
            p.display.update()

    #login screen function if user is logging into an account
    def login_screen(self):
        self.login = True
        self.typing_username = False
        self.typing_password = False
        self.input_text_username = ""
        self.input_text_password = ""
        self.username_flag = False
        self.password_flag = False
        self.incorrect_flag = False
        self.max_user_char = 10
        self.max_pass_char = 10

        username_button = Button("", self.font_name, 30, black, int((display_width/5)), int((display_height/5)*1.5), int((display_width/5)*3), int(display_height/10), blue, cyan)
        password_button = Button("", self.font_name, 30, black, int((display_width/5)), int((display_height/5)*3), int((display_width/5)*3), int(display_height/10), blue, cyan)
        enter_button = Button("Enter", self.font_name, 30, black, int((display_width/5)*2), int((display_height/5)*4), int(display_width/5), int(display_height/10), blue, cyan)
        clear_username_button = Button("Clear", self.font_name, 20, black, int((display_width/5)*4), int((display_height/5)*1.5), int((display_width/10)), int(display_height/10), green, lime)
        clear_password_button = Button("Clear", self.font_name, 20, black, int((display_width/5)*4), int((display_height/5)*3), int((display_width/10)), int(display_height/10), green, lime)
        return_button = Button("Return", self.font_name, 30, black, int((display_width/5)*2), int((display_height/5)*2.5), int(display_width/5), int(display_height/10), blue, cyan)
        back_button = Button("Back", self.font_name, 30, black, int((display_width/20)), int((display_height/5)*4), int(display_width/7), int(display_height/10), blue, cyan)

        while self.login:
            self.screen.fill(yellow)
            for event in p.event.get():
                if event.type == p.QUIT:
                    self.login = False
                    self.intro = False
                    self.playing = False
                    self.active = False
                    p.quit()
                if event.type == p.KEYDOWN:
                    if self.typing_password:
                        if event.key == p.K_RETURN:
                            self.typing_password = False
                        elif event.key == p.K_BACKSPACE:
                            if not password_button.msg:
                                pass
                            else:
                                password_button.msg = password_button.msg[:-1]
                                self.input_text_password = password_button.msg
                        elif event.key == p.K_SPACE:
                            password_button.msg += " "
                        else:
                            if len(p.key.name(event.key)) == 1:
                                if (ord(p.key.name(event.key)) >= 97 and ord(p.key.name(event.key)) <= 122 or
                                    ord(p.key.name(event.key)) >= 48 and ord(p.key.name(event.key)) <= 57):
                                    if len(self.input_text_password) < self.max_pass_char:
                                        password_button.msg += str(p.key.name(event.key))
                                        self.input_text_password = password_button.msg
                                        self.incorrect_flag = False
                    if self.typing_username:
                        if event.key == p.K_RETURN:
                            self.typing_password = True
                            self.typing_username = False
                        elif event.key == p.K_BACKSPACE:
                            if not username_button.msg:
                                pass
                            else:
                                username_button.msg = username_button.msg[:-1]
                                self.input_text_username = username_button.msg
                        else:
                            if len(p.key.name(event.key)) == 1:
                                if (ord(p.key.name(event.key)) >= 97 and ord(p.key.name(event.key)) <= 122 or
                                    ord(p.key.name(event.key)) >= 48 and ord(p.key.name(event.key)) <= 57):
                                    if len(self.input_text_username) < self.max_user_char:
                                        username_button.msg += str(p.key.name(event.key))
                                        self.input_text_username = username_button.msg
                                        self.incorrect_flag = False

            mouse_pos = p.mouse.get_pos()
            mouse_pressed = p.mouse.get_pressed()

            if not username_button.rect.collidepoint(mouse_pos):
                if mouse_pressed[0]:
                    self.typing_username = False

            if username_button.is_pressed(mouse_pos, mouse_pressed):
                self.typing_username = True

            if not self.typing_username and not username_button.msg:
                username_button.text_colour = lightgrey
                username_button.msg = "Click to type your username"

            if self.typing_username:
                if username_button.msg == "Click to type your username":
                    username_button.msg = ""
                    username_button.text_colour = black
                username_button.image.fill(username_button.active_colour)

            if not password_button.rect.collidepoint(mouse_pos):
                if mouse_pressed[0]:
                    self.typing_password = False

            if password_button.is_pressed(mouse_pos, mouse_pressed):
                self.typing_password = True

            if not self.typing_password and not password_button.msg:
                password_button.text_colour = lightgrey
                password_button.msg = "Click to type your password"

            if self.typing_password:
                if password_button.msg == "Click to type your password":
                    password_button.msg = ""
                    password_button.text_colour = black
                password_button.image.fill(password_button.active_colour)

            self.draw_text("Username:", 30, black, int(display_width/2), int((display_height/5)*1.25))
            self.draw_text("Password:", 30, black, int(display_width/2), int((display_height/5)*2.75))
            username_button.load()
            password_button.load()
            enter_button.load()
            clear_username_button.load()
            clear_password_button.load()
            back_button.load()

            if enter_button.is_pressed(mouse_pos, mouse_pressed):
                if not self.input_text_username:
                    self.username_flag = True
                else:
                    self.username_flag = False
                if not self.input_text_password:
                    self.password_flag = True
                else:
                    self.password_flag = False
                if self.input_text_username and self.input_text_password:
                    found = check_if_user_exists(self.input_text_username,self.input_text_password)
                    if found:
                        self.player_name = self.input_text_username
                        while found:
                            self.screen.fill(yellow)
                            for event in p.event.get():
                                if event.type == p.QUIT:
                                    found = False
                                    self.login = False
                                    self.playing = False
                                    self.active = False
                                    p.quit()

                            self.draw_text("Logged in as " + self.player_name, 50, black, int(display_width/2), int((display_height/5)*1.5))
                            return_button.load()
                            
                            mouse_pos = p.mouse.get_pos()
                            mouse_pressed = p.mouse.get_pressed()

                            if return_button.is_pressed(mouse_pos, mouse_pressed):
                                found = False
                                self.login = False
                                self.intro_screen()
                            p.display.update()
                    else:
                        self.incorrect_flag = True


            if clear_username_button.is_pressed(mouse_pos, mouse_pressed):
                self.input_text_username = ""
                username_button.msg = ""
            if clear_password_button.is_pressed(mouse_pos, mouse_pressed):
                self.input_text_password = ""
                password_button.msg = ""
                
            if self.username_flag:
                self.draw_text("You must enter a username", 20, red, int(display_width/2), int((display_height/5)*2.15))
            if self.password_flag:
                self.draw_text("You must enter a password", 20, red, int(display_width/2), int((display_height/5)*3.65))
            if self.incorrect_flag:
                self.draw_text("Credentials are incorrect", 30, red, int(display_width/2), int((display_height/5)*4.75))

            if back_button.is_pressed(mouse_pos, mouse_pressed):
                self.login = False
            
            p.display.update()

    #register screen function if user is registering an account
    def register_screen(self):
        self.register = True
        self.typing_username = False
        self.typing_password = False
        self.input_text_username = ""
        self.input_text_password = ""
        self.username_flag = False
        self.password_flag = False
        self.exists_flag = False
        self.max_user_char = 10
        self.max_pass_char = 10

        username_button = Button("", self.font_name, 30, black, int((display_width/5)), int((display_height/5)*1.5), int((display_width/5)*3), int(display_height/10), blue, cyan)
        password_button = Button("", self.font_name, 30, black, int((display_width/5)), int((display_height/5)*3), int((display_width/5)*3), int(display_height/10), blue, cyan)
        enter_button = Button("Enter", self.font_name, 30, black, int((display_width/5)*2), int((display_height/5)*4), int(display_width/5), int(display_height/10), blue, cyan)
        clear_username_button = Button("Clear", self.font_name, 20, black, int((display_width/5)*4), int((display_height/5)*1.5), int((display_width/10)), int(display_height/10), green, lime)
        clear_password_button = Button("Clear", self.font_name, 20, black, int((display_width/5)*4), int((display_height/5)*3), int((display_width/10)), int(display_height/10), green, lime)
        return_button = Button("Return", self.font_name, 30, black, int((display_width/5)*2), int((display_height/5)*2.5), int(display_width/5), int(display_height/10), blue, cyan)
        back_button = Button("Back", self.font_name, 30, black, int((display_width/20)), int((display_height/5)*4), int(display_width/7), int(display_height/10), blue, cyan)

        while self.register:
            self.screen.fill(yellow)
            for event in p.event.get():
                if event.type == p.QUIT:
                    self.register = False
                    self.intro = False
                    self.playing = False
                    self.active = False
                    p.quit()
                if event.type == p.KEYDOWN:
                    if self.typing_password:
                        if event.key == p.K_RETURN:
                            self.typing_password = False
                        elif event.key == p.K_BACKSPACE:
                            if not password_button.msg:
                                pass
                            else:
                                password_button.msg = password_button.msg[:-1]
                                self.input_text_password = password_button.msg
                        elif event.key == p.K_SPACE:
                            password_button.msg += " "
                        else:
                            if len(p.key.name(event.key)) == 1:
                                if (ord(p.key.name(event.key)) >= 97 and ord(p.key.name(event.key)) <= 122 or
                                    ord(p.key.name(event.key)) >= 48 and ord(p.key.name(event.key)) <= 57):
                                    if len(self.input_text_password) < self.max_pass_char:
                                        password_button.msg += str(p.key.name(event.key))
                                        self.input_text_password = password_button.msg
                    if self.typing_username:
                        if event.key == p.K_RETURN:
                            self.typing_password = True
                            self.typing_username = False
                        elif event.key == p.K_BACKSPACE:
                            if not username_button.msg:
                                pass
                            else:
                                username_button.msg = username_button.msg[:-1]
                                self.input_text_username = username_button.msg
                        else:
                            if len(p.key.name(event.key)) == 1:
                                if (ord(p.key.name(event.key)) >= 97 and ord(p.key.name(event.key)) <= 122 or
                                    ord(p.key.name(event.key)) >= 48 and ord(p.key.name(event.key)) <= 57):
                                    if len(self.input_text_username) < self.max_user_char:
                                        username_button.msg += str(p.key.name(event.key))
                                        self.input_text_username = username_button.msg
                                        self.exists_flag = False

            mouse_pos = p.mouse.get_pos()
            mouse_pressed = p.mouse.get_pressed()

            if not username_button.rect.collidepoint(mouse_pos):
                if mouse_pressed[0]:
                    self.typing_username = False

            if username_button.is_pressed(mouse_pos, mouse_pressed):
                self.typing_username = True

            if not self.typing_username and not username_button.msg:
                username_button.text_colour = lightgrey
                username_button.msg = "Click to type your username"

            if self.typing_username:
                if username_button.msg == "Click to type your username":
                    username_button.msg = ""
                    username_button.text_colour = black
                username_button.image.fill(username_button.active_colour)

            if not password_button.rect.collidepoint(mouse_pos):
                if mouse_pressed[0]:
                    self.typing_password = False

            if password_button.is_pressed(mouse_pos, mouse_pressed):
                self.typing_password = True

            if not self.typing_password and not password_button.msg:
                password_button.text_colour = lightgrey
                password_button.msg = "Click to type your password"

            if self.typing_password:
                if password_button.msg == "Click to type your password":
                    password_button.msg = ""
                    password_button.text_colour = black
                password_button.image.fill(password_button.active_colour)

            self.draw_text("Username:", 30, black, int(display_width/2), int((display_height/5)*1.25))
            self.draw_text("Password:", 30, black, int(display_width/2), int((display_height/5)*2.75))
            username_button.load()
            password_button.load()
            enter_button.load()
            clear_username_button.load()
            clear_password_button.load()
            back_button.load()

            if enter_button.is_pressed(mouse_pos, mouse_pressed):
                if not self.input_text_username:
                    self.username_flag = True
                else:
                    self.username_flag = False
                if not self.input_text_password:
                    self.password_flag = True
                else:
                    self.password_flag = False
                if self.input_text_username and self.input_text_password:
                    name_found = check_if_name_taken(self.input_text_username)
                    if not name_found:
                        add_details_to_database(self.input_text_username, self.input_text_password)
                        registered = check_if_user_exists(self.input_text_username,self.input_text_password)
                        if registered:
                            while registered:
                                self.screen.fill(yellow)
                                for event in p.event.get():
                                    if event.type == p.QUIT:
                                        registered = False
                                        self.register = False
                                        self.playing = False
                                        self.active = False
                                        p.quit()

                                return_button.load()
                                
                                mouse_pos = p.mouse.get_pos()
                                mouse_pressed = p.mouse.get_pressed()

                                self.draw_text("Account successfully registered!", 50, black, int(display_width/2), int((display_height/5)*1.5))
                                if return_button.is_pressed(mouse_pos, mouse_pressed):
                                    registered = False
                                    self.register = False
                                    self.intro_screen()
                                p.display.update()
                    else:
                        self.exists_flag = True


            if clear_username_button.is_pressed(mouse_pos, mouse_pressed):
                self.input_text_username = ""
                username_button.msg = ""
            if clear_password_button.is_pressed(mouse_pos, mouse_pressed):
                self.input_text_password = ""
                password_button.msg = ""
                
            if self.username_flag:
                self.draw_text("You must enter a username", 20, red, int(display_width/2), int((display_height/5)*2.15))
            if self.password_flag:
                self.draw_text("You must enter a password", 20, red, int(display_width/2), int((display_height/5)*3.65))
            if self.exists_flag:
                self.draw_text("Username already exists", 30, red, int(display_width/2), int((display_height/5)*4.75))

            if back_button.is_pressed(mouse_pos, mouse_pressed):
                self.register = False
            
            p.display.update()

#---------------------------------Game Loop---------------------------------
g = Game()
g.intro_screen()
p.quit()
