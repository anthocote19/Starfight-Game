import pygame
from Settings import *
from Client import *
from _thread import *
import subprocess

pygame.init()


def server_start():
    import server1


class menu:
    def __init__(self):
        self.state = 0
        self.title_screen = pygame.sprite.Group()
        self.host_join = pygame.sprite.Group()
        self.hosting = pygame.sprite.Group()
        self.chosing_map_1 = pygame.sprite.Group()
        self.chosing_map_2 = pygame.sprite.Group()
        self.chosing_map_3 = pygame.sprite.Group()
        self.chosing_map_4 = pygame.sprite.Group()
        self.chosing_map_5 = pygame.sprite.Group()
        self.settings = pygame.sprite.Group()
        self.joining = pygame.sprite.Group()
        self.joining_join = pygame.sprite.Group()
        self.end_screen = pygame.sprite.Group()
        self.menus = [
            self.title_screen,
            self.host_join,
            self.hosting,
            self.joining,
            self.chosing_map_1,
            self.chosing_map_2,
            self.chosing_map_3,
            self.chosing_map_4,
            self.chosing_map_5,
            self.settings,
            self.joining_join,
            self.end_screen,
        ]
        Button((250, 250), 100, 100, self.title_screen, "Play")

        Button((100, 250), 100, 100, self.host_join, "Host")
        Button((400, 250), 100, 100, self.host_join, "Join")
        Button((250, 400), 100, 50, self.host_join, "Back")

        Button((150, 475), 100, 50, self.hosting, "Maps")

        Button((100, 400), 100, 50, self.joining, "Back")

        Button(
            (50, 450),
            100,
            25,
            (
                self.chosing_map_1,
                self.chosing_map_2,
                self.chosing_map_3,
                self.chosing_map_4,
                self.chosing_map_5,
            ),
            "1",
        )
        Button(
            (150, 450),
            100,
            25,
            (
                self.chosing_map_1,
                self.chosing_map_2,
                self.chosing_map_3,
                self.chosing_map_4,
                self.chosing_map_5,
            ),
            "2",
        )
        Button(
            (250, 450),
            100,
            25,
            (
                self.chosing_map_1,
                self.chosing_map_2,
                self.chosing_map_3,
                self.chosing_map_4,
                self.chosing_map_5,
            ),
            "3",
        )
        Button(
            (350, 450),
            100,
            25,
            (
                self.chosing_map_1,
                self.chosing_map_2,
                self.chosing_map_3,
                self.chosing_map_4,
                self.chosing_map_5,
            ),
            "4",
        )
        Button(
            (450, 450),
            100,
            25,
            (
                self.chosing_map_1,
                self.chosing_map_2,
                self.chosing_map_3,
                self.chosing_map_4,
                self.chosing_map_5,
            ),
            "5",
        )

        Button((100, 400), 100, 50, self.settings, "Back")
        Button((340, 120), 70, 25, self.settings, "-time")
        Button((420, 120), 70, 25, self.settings, "+time")

        # Button((100, 100), 200, 100, self.chosing_map_1, "Map1")
        # Button((100, 200), 200, 100, self.chosing_map_1, "Food1")
        Button((100, 100), 200, 100, self.chosing_map_1, "Candy")
        Button((100, 100), 200, 100, self.chosing_map_2, "Grass")
        Button((100, 100), 200, 100, self.chosing_map_3, "Farm")
        Button((100, 100), 200, 100, self.chosing_map_4, "Factory")

        self.Start_button = Button((250, 475), 100, 50, (self.hosting,), "Start")
        Button((350, 475), 100, 50, self.hosting, "Set")

        self.flashcards = [
            FlashCard((20, 50), (self.hosting, self.joining_join), 0),
            FlashCard((140, 50), (self.hosting, self.joining_join), 1),
            FlashCard((260, 50), (self.hosting, self.joining_join), 2),
            FlashCard((380, 50), (self.hosting, self.joining_join), 3),
            FlashCard((20, 250), (self.hosting, self.joining_join), 4),
            FlashCard((140, 250), (self.hosting, self.joining_join), 5),
            FlashCard((260, 250), (self.hosting, self.joining_join), 6),
            FlashCard((380, 250), (self.hosting, self.joining_join), 7),
        ]
        self.inputboxes = [
            inputbox((100, 350), self.title_screen, "Name"),
            inputbox((100, 250), self.joining, "Join"),
        ]
        self.serverstarted = False
        self.inmenu = True
        self.host_start = False
        self.Connected_list = []
        self.network = ""
        self.map_chosen = "Candy"
        self.Game_time = 300
        self.name = ""
        self.name_list = []

    def show_menu(self, screen):
        self.menus[self.state].draw(screen)
        if self.state == 0 and self.name == "":
            screen.blit(
                Mini_square_text.render(
                    f"Enter a name and press enter", False, (255, 255, 255)
                ),
                (20, 400),
            )
        if self.state == 0 or self.state == 1:
            screen.blit(
                Block_text.render(f"STARFIGHT", False, (255, 255, 255)), (55, 0)
            )
        if self.state == 2:
            screen.blit(Starfight.render(f"HOST", False, (255, 255, 255)), (205, 0))
        if self.state == 3 or self.state == 10:
            screen.blit(Starfight.render(f"JOIN", False, (255, 255, 255)), (205, 0))
        if self.state == 3:
            screen.blit(
                Mini_square_text.render(f"Enter the host's IP", False, (255, 255, 255)),
                (100, 300),
            )
        if self.state == 9:
            screen.blit(Starfight.render(f"SET", False, (255, 255, 255)), (205, 0))
            screen.blit(
                Mini_square_text.render(
                    f"TIME : {self.Game_time}", False, (255, 255, 255)
                ),
                (100, 100),
            )
        if self.name:
            screen.blit(
                Text.render(f"Name : {self.name}", False, (255, 255, 255)), (0, 0)
            )
        if self.state == 2 or self.state >= 4:
            screen.blit(
                Text.render(f"Map : {self.map_chosen}", False, (255, 255, 255)), (0, 25)
            )
        screen.blit(Text.render(f"IP : {MyIP}", False, (255, 255, 255)), (350, 0))
        for button in self.menus[self.state]:
            button.update(self, screen)
        if self.host_start:
            self.Start_button.add(self.joining_join)


class Button(pygame.sprite.Sprite):
    def __init__(self, pos, width, height, group, function):
        super().__init__(group)
        self.image = pygame.Surface((width, height))
        self.image.fill("white")
        self.rect = self.image.get_rect(center=pos)
        self.function = function
        self.Functions = ["Play", "Host", "Join", "Maps"]
        self.map_list = {
            "Map1": Grass_Image,
            "Candy": Candy_Image,
            "Food1": Candy_Image,
            "Grass": Grass_Image,
            "Farm": Farm_Image,
            "Factory": Factory_Image,
        }
        self.map_screens = ["1", "2", "3", "4", "5"]
        self.buttoncooldown = pygame.time.get_ticks()

    def update(self, menu, screen):
        current_time = pygame.time.get_ticks()
        screen.blit(
            Mini_square_text.render(f"{self.function}", False, (0, 0, 0)),
            (self.rect.centerx - 35, self.rect.centery - 20),
        )
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.image.set_alpha(155)
            if self.function in self.map_list:
                screen.blit(self.map_list[self.function], (250, 100))
        else:
            self.image.set_alpha(255)
        if (
            pygame.mouse.get_pressed()[0]
            and self.rect.collidepoint(pygame.mouse.get_pos())
            and current_time - self.buttoncooldown >= 100
        ):
            self.buttoncooldown = current_time
            Button_press_sound.play(maxtime=100)
            if self.function in self.Functions and menu.name:
                menu.state = self.Functions.index(self.function) + 1
            elif self.function == "Start":
                menu.host_start = True
                menu.inmenu = False
            elif self.function in self.map_list:
                menu.map_chosen = self.function
                menu.state = 2
            elif self.function == "Back":
                if menu.state == 3:
                    menu.state = 1
                elif menu.state == 1:
                    menu.state = 0
                elif menu.state == 9:
                    menu.state = 2

            elif self.function in self.map_screens:
                menu.state = 3 + int(self.function)
            elif self.function == "Set":
                menu.state = 9
            elif self.function == "+time" and menu.Game_time < 500:
                menu.Game_time += 10
            elif self.function == "-time" and menu.Game_time > 0:
                menu.Game_time -= 10
            if self.function == "Host":
                # subprocess.Popen("python server1.py")
                start_new_thread(server_start, ())
                menu.network = Network()
                menu.serverstarted = True
        if self.function in self.map_screens and menu.state - 3 == int(self.function):
            self.image.set_alpha(155)
        elif self.rect.collidepoint(pygame.mouse.get_pos()):
            self.image.set_alpha(155)
        else:
            self.image.set_alpha(255)


class FlashCard(pygame.sprite.Sprite):
    def __init__(self, pos, group, id):
        super().__init__(group)
        self.id = id
        self.image = pygame.Surface((100, 170))
        self.image.fill("white")
        self.image.fill(
            ["blue", "red", "yellow", "green", "purple", "black", "gold", "pink"][id],
            (0, 100, 100, 100),
        )
        self.rect = self.image.get_rect(topleft=pos)
        self.name = f"Player {id+1}"
        self.connected = "Connected"

    def update(self, menu, screen):
        if self.id in menu.Connected_list:
            self.connected = "Connected"
        else:
            self.connected = ""
        screen.blit(
            Text.render(f"{self.connected}", False, (0, 0, 0)),
            (self.rect.centerx - 35, self.rect.centery - 90),
        )
        screen.blit(
            Text.render(f"{self.name}", False, (0, 0, 0)),
            (self.rect.centerx - 30, self.rect.centery - 60),
        )
        for name, id in menu.name_list:
            if id == self.id and self.id in menu.Connected_list:
                screen.blit(
                    Text.render(f"{name}", False, (0, 0, 0)),
                    (self.rect.centerx - 50, self.rect.centery - 40),
                )


class inputbox(pygame.sprite.Sprite):
    def __init__(self, pos, group, function):
        super().__init__(group)
        self.image = pygame.Surface((300, 50))
        self.image.fill("white")
        self.rect = self.image.get_rect(topleft=pos)
        self.text = "192.168.2.164"
        self.error = False
        self.exist = False
        self.function = function

    def insert(self, menu, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and self.exist:
                if self.function == "Join":
                    menu.network = Network(self.text)
                    if menu.network.id:
                        menu.serverstarted = True
                        menu.state = 10
                    else:
                        self.error = True
                if self.function == "Name":
                    menu.name = self.text
                    self.text = ""
                    self.error = False
                    if not menu.name:
                        self.error = True

            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif self.exist:
                if len(self.text) <= 30 and self.function == "Name":
                    self.text += event.unicode
                elif self.function == "Join":
                    self.text += event.unicode

    def update(self, menu, screen):
        if (menu.state == 0 and self.function == "Name") or (
            menu.state == 3 and self.function == "Join"
        ):
            self.exist = True
        else:
            self.exist = False
            self.text = ""
        screen.blit(Text.render(f"{self.text}", False, (0, 0, 0)), (self.rect.topleft))
        if self.error and self.function == "Join":
            screen.blit(
                Mini_square_text.render(f"Failed to connect", False, (255, 0, 0)),
                (100, 350),
            )
        if self.error and self.function == "Name":
            screen.blit(
                Mini_square_text.render(f"Invalid Name", False, (255, 0, 0)),
                (150, 450),
            )


Main_menu = menu()


def determine_winner(information):
    pass


def endscreen(information, screen):
    screen.blit(Starfight.render(f"RESULTS", False, (255, 255, 255)), (170, 0))
    for id in Main_menu.Connected_list:
        screen.blit(
            Mini_square_text.render(
                f"{information[id]['name']} : {information[id]['star_count']} stars",
                False,
                (255, 255, 255),
            ),
            (0, 50 * (id + 1)),
        )
    screen.blit(
        Mini_square_text.render(
            f"Close the game to play again", False, (255, 255, 255)
        ),
        (0, 450),
    )
