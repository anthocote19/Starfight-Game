"""Fenêtre qui programme le joueur"""

import pygame
import Items
import Levels
import random
import time
from Settings import *

pygame.init()
Text = pygame.font.SysFont("Arial", 20)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, id, name):
        super().__init__(group)
        self.id = id
        self.name = name

        self.star_lost = False
        self.star_count = 0
        self.star_list = []

        self.hp = 3
        self.healthbar = [
            Hud_Item(0, "heart"),
            Hud_Item(1, "heart"),
            Hud_Item(2, "heart"),
        ]
        self.hudframe = 0
        self.hudspin = [pygame.time.get_ticks(), pygame.time.get_ticks()]

        self.death_timer = pygame.time.get_ticks()
        self.appear = False

        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 4
        self.extra_speed = 0
        self.facing = "right"
        self.prev_time = time.time()

        self.flyback_mesure = pygame.time.get_ticks()
        self.taking_knockback = False
        self.knockback_direction = pygame.math.Vector2()

        self.took_damage = False
        self.invincibilty = False
        self.invincibilty_power = False
        self.invincibilty_power_mesure = pygame.time.get_ticks()
        self.invincibilty_mesure = pygame.time.get_ticks()

        self.frozen = False
        self.frozen_mesure = pygame.time.get_ticks()
        self.ingame = True
        self.items_list = ["", "", ""]
        self.coin_count = 0
        self.item_hud = [Hud_Item(0, ""), Hud_Item(1, ""), Hud_Item(2, "")]
        self.bonus_item = []
        self.using_item = False
        self.item_timer = pygame.time.get_ticks()
        self.inusage = None
        self.weaponask = False
        self.bowask = False
        if self.id <= 3:
            self.spritesheet = pygame.image.load(Dinos[self.id]).convert_alpha()
        else:
            idle, walk, kick, hurt = (
                pygame.image.load(Extra_Dinos_Idle[self.id - 4]).convert_alpha(),
                pygame.image.load(Extra_Dinos_Walk[self.id - 4]).convert_alpha(),
                pygame.image.load(Extra_Dinos_Kick[self.id - 4]).convert_alpha(),
                pygame.image.load(Extra_Dinos_Hurt[self.id - 4]).convert_alpha(),
            )
        self.frame = 0
        self.action = 0
        self.last_update = pygame.time.get_ticks()
        if self.id <= 3:
            animation_length = [4, 6, 3, 4]
            self.animation_list = create_animation(
                self.spritesheet, animation_length, 24, 24, 0, 0, 45, 45
            )
        else:
            self.animation_list = (
                create_animation(idle, [3], 24, 24, 0, 0, 45, 45)
                + [create_animation(walk, [6], 24, 24, 0, 0, 45, 45)[0]]
                + [create_animation(kick, [3], 24, 24, 0, 0, 45, 45)[0]]
                + [create_animation(hurt, [4], 24, 24, 0, 0, 45, 45)[0]]
            )

        self.kill_list = []
        self.image = self.animation_list[self.action][self.frame]
        self.rect = self.image.get_rect(topleft=pos)
        self.nametag = Nametag(self, (Levels.map.visible_sprites))

    # Réuni tous les methodes du joueurs ainsi que gérer ses animations
    def update(self):
        animation_cooldown = 100
        heart_cooldown = 100
        spin_cooldown = 2000
        current_time = pygame.time.get_ticks()
        if not self.frozen:
            self.last_update, self.frame = animate(
                self.animation_list,
                animation_cooldown,
                self.last_update,
                self.action,
                self.frame,
            )
        if current_time - self.hudspin[1] >= spin_cooldown:
            self.hudspin[0], self.hudframe = animate(
                [["1", "2", "3", "4", "5", "6"]],
                heart_cooldown,
                self.hudspin[0],
                0,
                self.hudframe,
            )
            if self.hudframe == 0:
                self.hudspin[1] = current_time
        if self.hp > 0:
            self.Damage_Check()
            self.knockback()
            self.invincible_tick()
            self.freeze_tick()
            self.invincibilty_powerup()
            self.use_item()
            self.show_item()
            self.pickup()
            self.mouvement()
            self.flicker()
            self.image = self.animation_list[self.action][self.frame]
            self.nametag.rect.center = (self.rect.centerx, self.rect.centery - 30)
        self.dead()

    # On applique une animation de dégat quand le joueur est invincible.
    def flicker(self):
        if self.invincibilty:
            self.action = 3

    # Gère le mouvement et l'état de ses animations en fonction du mouvement.
    # Le joueur peut bouger dans les 8 huits directions.
    # On applique un animation de marche quand il bouge.
    def mouvement(self):
        keys = pygame.key.get_pressed()
        if not self.frozen and not self.taking_knockback:
            if keys[pygame.K_d]:
                self.direction.x = 1
                self.action = 1
                if self.facing == "left":
                    self.turn()
                    self.facing = "right"
            elif keys[pygame.K_q]:
                self.direction.x = -1
                self.action = 1
                if self.facing == "right":
                    self.turn()
                    self.facing = "left"
            else:
                self.direction.x = 0
            if keys[pygame.K_z]:
                self.direction.y = -1
                self.action = 1
            elif keys[pygame.K_s]:
                self.direction.y = 1
                self.action = 1
            else:
                self.direction.y = 0
            if self.direction.magnitude() != 0:
                self.direction = self.direction.normalize()
            now = time.time()
            dt = now - self.prev_time
            self.rect.x += self.direction.x * (self.speed + self.extra_speed) * dt * 60
            self.check_collision("horizontal")
            self.rect.y += self.direction.y * (self.speed + self.extra_speed) * dt * 60
            self.prev_time = now
            self.check_collision("vertical")

    # Gère les collisions avec les murs, le joueur ne peut pas franchir un mur.
    def check_collision(self, direction):
        if direction == "horizontal":
            for sprite in Levels.map.obsticle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.x > 0:
                        self.rect.right = sprite.rect.left
                    if self.direction.x < 0:
                        self.rect.left = sprite.rect.right

        if direction == "vertical":
            for sprite in Levels.map.obsticle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.y < 0:
                        self.rect.top = sprite.rect.bottom
                    if self.direction.y > 0:
                        self.rect.bottom = sprite.rect.top

    # Gère le ramassement des items et des étoiles.
    # On le tue l'item et on le met dans kill list pour qu'il puisse être tuer pour les autres joueurs.
    # On applique aussi son effet
    def pickup(self):
        if not self.invincibilty:
            for sprite in Levels.map.pickup_sprites:
                if sprite.rect.colliderect(self.rect):
                    sprite.effect_apply(self)
                    if sprite.effect == "star":
                        self.kill_list.append(sprite.id)
                        self.star_list.append(Hud_Item(self.star_count, "star"))
                    elif sprite.effect not in ["speedup", "slowdown", "gold", "heal"]:
                        self.kill_list.append(sprite.id)
                    sprite.kill()

    # met l'item dans item_list
    # Le nombre d'item ne peut pas dépasser 3
    # Si le list est remplie, les items déjà dans le list ne sont pas remplacés.
    def give(self, effect):
        for item in range(len(self.items_list)):
            if not self.items_list[item]:
                self.item_hud[item].type = effect
                if effect == "sword":
                    self.items_list[item] = Items.Weapon(
                        effect, (Levels.map.weapon_sprites), self.id
                    )

                    break
                if effect == "bow":
                    self.items_list[item] = Items.Weapon(
                        effect, (Levels.map.bow_sprites), self.id
                    )
                    break
                if (
                    effect == "bomb"
                    or effect == "invincible"
                    or effect == "freeze"
                    or effect == "lightning"
                ):
                    self.items_list[item] = Items.Spell(effect)
                    break

    # Applique les changement correspondants lorsque le joueur prend des dégats:
    # On perd un hp, on devient invincible et on perd un étoile si on à un.
    # On prend aussi de la knockback, la direction de ceci étant en fonction de la source des dégats.
    def Ouch(self, Damage, dealer=None):
        if not self.invincibilty and not self.invincibilty_power:
            if Damage:
                self.invincibilty = True
                self.took_damage = True
                self.hp -= 1
                self.healthbar.pop()
                Damage_sound.play(maxtime=100)
                if self.hp == 0:
                    Player_Death_sound.play()
            self.taking_knockback = True
            if dealer:
                if (
                    dealer in Levels.map.enemy_sprites
                    or dealer in Levels.map.other_player_sprites
                ):
                    if self.direction == (0, 0):
                        self.knockback_direction = pygame.math.Vector2(
                            tuple(dealer.direction)
                        )
                    else:
                        self.knockback_direction = -self.direction
                if (
                    dealer in Levels.map.weapon_sprites
                    or dealer in Levels.map.arrow_sprites
                ):
                    self.knockback_direction = pygame.math.Vector2(
                        tuple(dealer.direction)
                    )

            else:
                self.knockback_direction = pygame.math.Vector2(0, 0)
            if not self.invincibilty_power:
                if self.frame > 3:
                    self.frame = 0
                # self.action = 3

    # Vérifie si on à rentré en collision avec un source de dégats.
    # Si c'est un gèle, on devient gelé.
    def Damage_Check(self):
        for sprite in Levels.map.enemy_sprites:
            if sprite.rect.colliderect(self.rect):
                self.Ouch(True, sprite)
        for sprite in Levels.map.weapon_sprites:
            if sprite.rect.colliderect(self.rect):
                if sprite.id != self.id:
                    self.Ouch(True, sprite)
        for sprite in Levels.map.arrow_sprites:
            if sprite.rect.colliderect(self.rect):
                if sprite.id != self.id:
                    self.Ouch(True, sprite)
                    sprite.kill()
        for sprite in Levels.map.flash_sprites:
            if sprite.rect.colliderect(self.rect):
                if sprite.id != self.id:
                    Lightning_sound.play()
                    self.Ouch(True)
                    if sprite.type == "lightning":
                        Particle(
                            self.rect.center,
                            (Levels.map.visible_sprites, Levels.map.particle_sprites),
                            "lightning",
                        )
        for sprite in Levels.map.bomb_sprites:
            if sprite.rect.colliderect(self.rect):
                if sprite.id != self.id:
                    Items.Flash(
                        sprite,
                        (Levels.map.visible_sprites, Levels.map.flash_sprites),
                        200,
                        "explosion",
                        sprite.id,
                    )
                    sprite.kill()
        for sprite in Levels.map.freeze_sprites:
            if sprite.rect.colliderect(self.rect):
                if sprite.id != self.id:
                    self.frozen = True
                    Ice_sound.play()
                    Particle(
                        self.rect.center,
                        (Levels.map.visible_sprites, Levels.map.particle_sprites),
                        "freeze",
                    )
        for sprite in Levels.map.other_player_sprites:
            if sprite.rect.colliderect(self.rect):
                self.Ouch(False, sprite)

    # On prend de la knockback quand il est appelé pendant un certain temps.
    # On ne peut pas bouger quand on prend de la knockback.
    def knockback(self):
        current_time = pygame.time.get_ticks()
        duration = 50
        if self.taking_knockback:
            self.speed = 10
            self.direction = self.knockback_direction
            now = time.time()
            dt = now - self.prev_time
            self.rect.x += self.direction.x * self.speed * dt * 60
            self.check_collision("horizontal")
            self.rect.y += self.direction.y * self.speed * dt * 60
            self.prev_time = now
            self.check_collision("vertical")
            if current_time - self.flyback_mesure >= duration:
                self.taking_knockback = False
        else:
            self.flyback_mesure = pygame.time.get_ticks()
            self.speed = 4

    # Compte le temps pendant lequel on est invincible
    def invincible_tick(self):
        if self.invincibilty:
            invincibilty_frames = 1000
            current_time = pygame.time.get_ticks()
            if current_time - self.invincibilty_mesure >= invincibilty_frames:
                self.invincibilty = False
                self.invincibilty_mesure = current_time
                self.action = 0
                self.frame = 0
        else:
            self.invincibilty_mesure = pygame.time.get_ticks()

    # Compte le temps pendant lequel on est gelé
    def freeze_tick(self):
        if self.frozen:
            frozen_frames = 10000
            current_time = pygame.time.get_ticks()
            if current_time - self.frozen_mesure >= frozen_frames:
                self.frozen = False
                self.frozen_mesure = current_time
        else:
            self.frozen_mesure = pygame.time.get_ticks()

    # Permet d'utiliser les items, quand le bouton correspondant est appuié.
    def use_item(self):
        keys = pygame.key.get_pressed()
        keyboard = [keys[pygame.K_j], keys[pygame.K_k], keys[pygame.K_l]]
        if not self.using_item:
            for i in range(len(keyboard)):
                if keyboard[i]:
                    if self.items_list[i]:
                        if (
                            self.items_list[i].type == "sword"
                            or self.items_list[i].type == "bow"
                        ):
                            self.items_list[i].add(Levels.map.visible_sprites)
                            Item_sound.play(maxtime=200)
                            self.weaponask = self.items_list[i].type
                            self.inusage = self.items_list[i].type
                            self.using_item = i + 1
                        else:
                            self.items_list[i].cast(self, Levels.map)
                            self.weaponask = self.items_list[i].type
                            self.inusage = self.items_list[i].type
                            self.items_list[i] = ""
                            self.item_hud[i].type = ""

    # Montre l'item quand il est utilisé.
    # Si il s'agit d'un bow, on peut envoyer des arrows avec la touche espace.
    # Les items permettent de faire des dégats aux autres joueurs.
    def show_item(self):
        cooldown = 10000
        if self.using_item:
            current_time = pygame.time.get_ticks()
            self.items_list[self.using_item - 1].use_weapon(self)
            if self.items_list[self.using_item - 1].type == "sword":
                self.speed = 7
            self.items_list[self.using_item - 1].shoot_arrow(self, Levels.map)
            if current_time - self.item_timer >= cooldown:
                self.items_list[self.using_item - 1].kill()
                self.items_list[self.using_item - 1] = ""
                self.item_hud[self.using_item - 1].type = ""
                self.using_item = False
                self.inusage = None
                self.speed = 4
                self.item_timer = current_time

        else:
            self.item_timer = pygame.time.get_ticks()

    # Donne de l'invincibilité quand l'item invincible est utilisé
    def invincibilty_powerup(self):
        duration = 6000
        if self.invincibilty_power:
            current_time = pygame.time.get_ticks()
            if current_time - self.invincibilty_power_mesure >= duration:
                self.invincibilty_power = False
                self.invincibilty_power_mesure = current_time
        else:
            self.invincibilty_power_mesure = pygame.time.get_ticks()

    # Change l'animation du joueur quand il se retourne.
    def turn(self):
        for animation in self.animation_list:
            for frame in range(len(animation)):
                animation[frame] = pygame.transform.flip(animation[frame], True, False)

    # Gère la mort. Si l'hp du joueur est<=0 il meurt pendant un temps.
    # Il ne peut pas accèdé aux autres méthodes, et il n'apparait plus sur l'écran.
    # Après que le temps est écoulé, il réaparait à un position random.
    def dead(self):
        death_time = 10000
        death_time_post_tp = 4000
        self.prev_time = time.time()
        current_time = pygame.time.get_ticks()
        if self.hp <= 0:
            self.speed = 4
            self.extra_speed = 0
            self.bonus_item = []
            self.item_hud = [Hud_Item(0, ""), Hud_Item(1, ""), Hud_Item(2, "")]
            self.image.set_alpha(0)
            if self.star_count > 0 and self.took_damage:
                self.star_count -= 1
                self.star_list.pop()
                self.star_lost = True
                Levels.Star(
                    self.rect.center,
                    (
                        Levels.map.visible_sprites,
                        Levels.map.pickup_sprites,
                        Levels.map.star_sprites,
                    ),
                    "player",
                    0,
                )
            if self.using_item:
                self.items_list[self.using_item - 1].kill()
                self.using_item = False
                self.item_timer = pygame.time.get_ticks()
            self.inusage = None
            self.items_list = ["", "", ""]
            if current_time - self.death_timer >= death_time:
                if not self.appear:
                    self.rect.center = random.choice(
                        list(Levels.map.respawn_tile_sprites)
                    ).rect.topleft
                    self.appear = True
                if current_time - self.death_timer >= death_time + death_time_post_tp:
                    self.hp = 3
                    self.healthbar = [
                        Hud_Item(0, "heart"),
                        Hud_Item(1, "heart"),
                        Hud_Item(2, "heart"),
                    ]
                    self.death_timer = current_time
        else:
            self.death_timer = pygame.time.get_ticks()
            self.appear = False
            self.image.set_alpha(255)


class otherPlayer(pygame.sprite.Sprite):
    def __init__(self, pos, group, id, name):
        super().__init__(group)
        self.id = id
        self.name = name

        if self.id <= 3:
            self.spritesheet = pygame.image.load(Dinos[self.id]).convert_alpha()
        else:
            idle, walk, kick, hurt = (
                pygame.image.load(Extra_Dinos_Idle[self.id - 4]).convert_alpha(),
                pygame.image.load(Extra_Dinos_Walk[self.id - 4]).convert_alpha(),
                pygame.image.load(Extra_Dinos_Kick[self.id - 4]).convert_alpha(),
                pygame.image.load(Extra_Dinos_Hurt[self.id - 4]).convert_alpha(),
            )
        self.facing = "right"
        self.action = 0
        self.frame = 0
        self.weapon = None
        self.direction = pygame.math.Vector2()

        if self.id <= 3:
            animation_length = [4, 6, 3, 4]
            self.animation_list = create_animation(
                self.spritesheet, animation_length, 24, 24, 0, 0, 45, 45
            )
        else:
            self.animation_list = (
                create_animation(idle, [3], 24, 24, 0, 0, 45, 45)
                + [create_animation(walk, [6], 24, 24, 0, 0, 45, 45)[0]]
                + [create_animation(kick, [3], 24, 24, 0, 0, 45, 45)[0]]
                + [create_animation(hurt, [4], 24, 24, 0, 0, 45, 45)[0]]
            )

        self.image = self.animation_list[self.action][self.frame]
        self.rect = self.image.get_rect(center=pos)
        self.nametag = Nametag(self, (Levels.map.visible_sprites))

    def turn(self):
        for animation in self.animation_list:
            for frame in range(len(animation)):
                animation[frame] = pygame.transform.flip(animation[frame], True, False)

    # Fonction qui met à jour l'état des autres joueurs en fonction de l'information reçu par le serveur.
    def update(self, player_information):
        # Le position est mise à jour
        self.rect.center = player_information[self.id]["position"]
        self.nametag.rect.center = (self.rect.centerx, self.rect.centery - 30)
        self.direction = player_information[self.id]["direction"]
        # L'animation effectué est donné.
        self.action, self.frame = (
            player_information[self.id]["action_frame"][0],
            player_information[self.id]["action_frame"][1],
        )
        if self.facing != player_information[self.id]["facing"]:
            self.turn()
            self.facing = player_information[self.id]["facing"]
        # Si il demande d'utilisé un arme on lui donne
        if (player_information[self.id]["weaponask"] == "sword") and not self.weapon:
            self.weapon = Items.Weapon(
                player_information[self.id]["weaponask"],
                (Levels.map.weapon_sprites),
                self.id,
            )
        if (player_information[self.id]["weaponask"] == "bow") and not self.weapon:
            self.weapon = Items.Weapon(
                player_information[self.id]["weaponask"],
                (Levels.map.bow_sprites),
                self.id,
            )
        if player_information[self.id]["weaponask"] == "bomb":
            Items.Bomb(
                self,
                (Levels.map.visible_sprites, Levels.map.bomb_sprites),
                self.id,
                "Invisible",
            )
        if player_information[self.id]["weaponask"] == "freeze":
            Items.Freeze(
                self, (Levels.map.visible_sprites, Levels.map.freeze_sprites), self.id
            )
        if player_information[self.id]["weaponask"] == "lightning":
            Items.Flash(
                self,
                (Levels.map.visible_sprites, Levels.map.flash_sprites),
                500,
                "lightning",
                self.id,
            )
        # Si il utilse un arme on lui donne l'arme.
        if player_information[self.id]["inusage"] and self.weapon:
            if self.weapon not in Levels.map.visible_sprites:
                self.weapon.add(Levels.map.visible_sprites)
            self.weapon.use_weapon(self)
            if player_information[self.id]["bowask"]:
                Items.Arrow(
                    self.weapon,
                    (Levels.map.visible_sprites, Levels.map.arrow_sprites),
                    self.id,
                )
        else:
            if self.weapon:
                self.weapon.kill()
                self.weapon = None
        # Pris des dégats
        if (
            player_information[self.id]["took_damage"]
            and player_information[self.id]["invincibilty"]
        ):
            if player_information[self.id]["star_lost"]:
                Items.Star(
                    self.rect.center,
                    (
                        Levels.map.visible_sprites,
                        Levels.map.pickup_sprites,
                        Levels.map.star_sprites,
                    ),
                    "player",
                    0,
                )
        # Si il récupère un étoile on le tue
        for sprite in Levels.map.star_sprites:
            if (
                sprite.origin == "player"
                and sprite.rect.colliderect(self.rect)
                and not player_information[self.id]["invincibilty"]
            ):
                sprite.kill()
        for sprite in Levels.map.pickup_sprites:
            if (
                sprite.effect in ["speedup", "slowdown", "gold", "heal"]
                and sprite.rect.colliderect(self.rect)
                and not player_information[self.id]["invincibilty"]
            ):
                sprite.kill()
        # Pour le particle
        for sprite in Levels.map.freeze_sprites:
            if sprite.rect.colliderect(self.rect):
                if sprite.id != self.id:
                    Particle(
                        self.rect.center,
                        (Levels.map.visible_sprites, Levels.map.particle_sprites),
                        "freeze",
                    )
        for sprite in Levels.map.flash_sprites:
            if sprite.rect.colliderect(self.rect):
                if sprite.id != self.id:
                    if sprite.type == "lightning":
                        Particle(
                            self.rect.center,
                            (Levels.map.visible_sprites, Levels.map.particle_sprites),
                            "lightning",
                        )
        for sprite in Levels.map.arrow_sprites:
            if sprite.rect.colliderect(self.rect):
                if sprite.id != self.id:
                    sprite.kill()

        self.image = self.animation_list[self.action][self.frame]
        # Il disparait quand il meurt
        if player_information[self.id]["hp"] <= 0:
            self.image.set_alpha(0)
        else:
            self.image.set_alpha(255)
