import pygame

pygame.init()

Placeholder_map = "Candy"
Coin_convergence = 50
Maps = {
    "Map1": "Maps/MAP.tmx",
    "Food1": "Maps/Food1.tmx",
    "Candy": "Maps/Candy.tmx",
    "Grass": "Maps/Grass.tmx",
    "Farm": "Maps/Farm.tmx",
    "Factory": "Maps/Factory.tmx",
}
Text = pygame.font.SysFont("Arial", 20)


def cut_image(image, width, height, index_x, index_y, sizex, sizey):
    coupure = pygame.Surface((width, height))
    coupure.set_colorkey((0, 0, 0))
    coupure.blit(image, (0, 0), (width * index_x, height * index_y, width, height))
    coupure = pygame.transform.scale(coupure, (sizex, sizey))
    return coupure


def animate(animation_list, animation_cooldown, last_update, action, frame):
    current_time = pygame.time.get_ticks()
    if current_time - last_update >= animation_cooldown:
        frame += 1
        last_update = current_time
        if frame >= len(animation_list[action]):
            frame = 0
    return last_update, frame


def create_animation(
    spritesheet, animation_length, width, height, index_x, index_y, sizex, sizey
):
    animation_list = []
    steps = index_x
    for ani in animation_length:
        temp = []
        for i in range(ani):
            cut = cut_image(spritesheet, width, height, steps, index_y, sizex, sizey)
            temp.append(cut)
            steps += 1
        animation_list.append(temp)
    return animation_list


Dinos = [
    "Sprites/DinoSprites - doux.png",
    "Sprites/DinoSprites - mort.png",
    "Sprites/DinoSprites - tard.png",
    "Sprites/DinoSprites - vita.png",
]
Extra_Dinos_Idle = [
    "Sprites/download/male/cole/base/idle.png",
    "Sprites/download/male/kuro/base/idle.png",
    "Sprites/download/male/nico/base/idle.png",
    "Sprites/download/male/kira/base/idle.png",
]
Extra_Dinos_Walk = [
    "Sprites/download/male/cole/base/move.png",
    "Sprites/download/male/kuro/base/move.png",
    "Sprites/download/male/nico/base/move.png",
    "Sprites/download/male/kira/base/move.png",
]
Extra_Dinos_Kick = [
    "Sprites/download/male/cole/base/kick.png",
    "Sprites/download/male/kuro/base/kick.png",
    "Sprites/download/male/nico/base/kick.png",
    "Sprites/download/male/kira/base/kick.png",
]
Extra_Dinos_Hurt = [
    "Sprites/download/male/cole/base/hurt.png",
    "Sprites/download/male/kuro/base/hurt.png",
    "Sprites/download/male/nico/base/hurt.png",
    "Sprites/download/male/kira/base/hurt.png",
]

Useful_Item_sprites = pygame.image.load(
    "Sprites/coins-chests-etc-2-0.png"
).convert_alpha()
Weapons_sprites = pygame.image.load(
    "Sprites/Medieval weapons pack v1.2/Medieval weapons pack/steel/outline x4.png"
).convert_alpha()
Ice = pygame.image.load(
    "Sprites/Ice Effect 01/Ice Effect 01/Ice VFX 2/Ice VFX 2 Active.png"
).convert_alpha()
Light = pygame.image.load(
    "Sprites/Thunder Effect 02/Thunder Effect 02/Thunder Strike/Thunderstrike wo blur.png"
).convert_alpha()
Lightning_icon = pygame.image.load(
    "Sprites/download-icon-lightning-131982518827228370_64.png"
)
Ice_animation = create_animation(Ice, [8], 32, 32, 0, 0, 50, 50)
Lightning_animation = create_animation(Light, [12], 75, 64, 0, 0, 100, 100)
Ice_cream = pygame.image.load("Sprites/download-icon-cream-131982518805283723_64.png")
Bomb_explosion = pygame.image.load(
    "Sprites/explosions-pack-web/explosions-pack-web/spritesheets/explosion-6.png"
)
Block_text = pygame.font.Font("Sprites/kenney_kenney-fonts/Fonts/Kenney Blocks.ttf", 60)
Mini_square_text = pygame.font.Font(
    "Sprites/kenney_kenney-fonts/Fonts/Kenney Mini Square.ttf", 30
)
Starfight = pygame.font.SysFont("Arial", 40)
Text = pygame.font.SysFont("Arial", 20)
Character_sprites = pygame.image.load(
    "Sprites/kenney_pixel-platformer/Tilemap/tilemap-characters_packed.png"
)
Artilery_sprites = pygame.image.load(
    "Sprites/kenney_pixel-shmup/Tilemap/tiles_packed.png"
)
Star_background = pygame.image.load("Sprites/Enjl-Starry Space Background/preview.png")

Background = cut_image(Star_background, 256, 224, 0, 0, 500, 500)
Button_press_sound = pygame.mixer.Sound("Sound/Button_press_sound.mp3")
Coin_sound = pygame.mixer.Sound("Sound/Coin_sound.mp3")
Damage_sound = pygame.mixer.Sound("Sound/Damage_sound.mp3")
Enemy_Death_sound = pygame.mixer.Sound("Sound/Enemy_Death_sound.mp3")
Game_start_sound = pygame.mixer.Sound("Sound/Game_start_sound.mp3")
Ice_sound = pygame.mixer.Sound("Sound/Ice_sound.mp3")
Item_sound = pygame.mixer.Sound("Sound/Item_sound.mp3")
Lightning_sound = pygame.mixer.Sound("Sound/Lightning_sound.mp3")
Player_Death_sound = pygame.mixer.Sound("Sound/Player_Death_sound.mp3")
Slowdown_sound = pygame.mixer.Sound("Sound/Slowdown_sound.mp3")
Speedup_sound = pygame.mixer.Sound("Sound/Speedup_sound.mp3")
Star_sound = pygame.mixer.Sound("Sound/Star_sound.mp3")
Arrow_sound = pygame.mixer.Sound("Sound/Arrow_sound.mp3")

Grass_Image = cut_image(
    pygame.image.load("Sprites/Map_Images/Grass_Image.png"), 770, 765, 0, 0, 250, 250
)
Candy_Image = cut_image(
    pygame.image.load("Sprites/Map_Images/Candy_Image.png"), 770, 765, 0, 0, 250, 250
)
Farm_Image = cut_image(
    pygame.image.load("Sprites/Map_Images/Farm_Image.png"), 770, 765, 0, 0, 250, 250
)
Factory_Image = cut_image(
    pygame.image.load("Sprites/Map_Images/Factory_Image.png"), 770, 765, 0, 0, 250, 250
)


class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, group, type):
        super().__init__(group)
        self.frame = 0
        self.type = type
        self.last_update = pygame.time.get_ticks()
        if type == "freeze":
            self.animation_list = Ice_animation
        if type == "lightning":
            self.animation_list = Lightning_animation
        self.image = self.animation_list[0][self.frame]
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        cooldown = 100
        self.last_update, self.frame = animate(
            self.animation_list, cooldown, self.last_update, 0, self.frame
        )
        self.image = self.animation_list[0][self.frame]
        if (self.frame == 7 and self.type == "freeze") or (
            self.frame == 11 and self.type == "lightning"
        ):
            self.kill()


class Nametag(pygame.sprite.Sprite):
    def __init__(self, player, group):
        super().__init__(group)
        self.image = Text.render(
            f"{player.name}",
            False,
            (0, 0, 0),
        )

        self.rect = self.image.get_rect(
            center=(player.rect.centerx, player.rect.centery - 30)
        )


class Hud_Item(pygame.sprite.Sprite):
    def __init__(self, id, type):
        self.type = type
        if self.type == "heart":
            self.animation_list = create_animation(
                Useful_Item_sprites, [6], 16, 16, 25, 14, 30, 30
            )
            self.image = self.animation_list[0][0]
            self.rect = self.image.get_rect(center=(id * 30, 30))
        if self.type == "star":
            self.animation_list = create_animation(
                Useful_Item_sprites, [6], 16, 16, 12, 12, 30, 30
            )
            self.image = self.animation_list[0][0]
            self.rect = self.image.get_rect(
                center=(((id - 1) % 16) * 30, 60 + 30 * ((id - 1) // 16))
            )
        if self.type == "speedup":
            self.image = cut_image(Useful_Item_sprites, 16, 15, 36, 14, 50, 50)
            self.rect = self.image.get_rect(
                center=(
                    pygame.display.get_surface().get_width() - 100,
                    (pygame.display.get_surface().get_height() - 100) - (id - 1) * 50,
                )
            )
        if self.type == "slowdown":
            self.image = cut_image(Useful_Item_sprites, 16, 15, 36, 16, 50, 50)
            self.rect = self.image.get_rect(
                center=(
                    pygame.display.get_surface().get_width() - 100,
                    (pygame.display.get_surface().get_height() - 100) + (id + 1) * 50,
                )
            )

        self.id = id

    def show(self, player, screen, map_chosen):
        if self.type == "heart":
            # if player.hp >= self.id + 1:
            screen.blit(self.image, self.rect.center)
            self.image = self.animation_list[0][player.hudframe]
        if self.type == "star":
            # if player.star_count >= self.id:
            screen.blit(self.image, self.rect.center)
            self.image = self.animation_list[0][player.hudframe]
        if self.type in ["invincible", "sword", "bow", "bomb", "freeze", "lightning"]:
            effect_index = [
                "invincible",
                "sword",
                "bow",
                "bomb",
                "freeze",
                "lightning",
            ].index(self.type)
            self.image = [
                cut_image(Useful_Item_sprites, 16, 16, 48, 36, 50, 50),
                cut_image(Useful_Item_sprites, 16, 16, 46, 35, 50, 50),
                cut_image(Useful_Item_sprites, 16, 16, 46, 37, 50, 50),
                cut_image(Useful_Item_sprites, 16, 16, 53, 35, 50, 50),
                cut_image(Ice_cream, 64, 64, 0, 0, 50, 50),
                cut_image(Lightning_icon, 64, 64, 0, 0, 50, 50),
            ][effect_index]
            self.rect = self.image.get_rect(
                center=(50 * self.id, pygame.display.get_surface().get_height() - 100)
            )
            screen.blit(self.image, self.rect.center)
        if self.type == "speedup" or self.type == "slowdown":
            screen.blit(self.image, self.rect.center)
        screen.blit(
            Mini_square_text.render(f"Coins : {player.coin_count}", False, (0, 0, 0)),
            (0, pygame.display.get_surface().get_height() - 200),
        )

    def __repr__(self):
        return self.type
