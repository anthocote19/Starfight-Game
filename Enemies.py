# Crée des ennemies
import pygame
import time
import random
from Settings import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, group, type, id):
        super().__init__(group)
        self.id = id
        self.type = type
        self.frame = 0
        self.facing = "left"

        if self.type == "movement":
            random_enemy = random.choice([(6, 1), (0, 2), (6, 2)])
            self.animation_list = create_animation(
                Character_sprites, [3], 24, 24, random_enemy[0], random_enemy[1], 50, 50
            )
            self.image = self.animation_list[0][self.frame]
        elif self.type in ["m_ver", "m_hori", "stationary"]:
            self.image = cut_image(Character_sprites, 24, 24, 8, 0, 50, 50)
            self.animation_list = []
        else:
            self.image = cut_image(Artilery_sprites, 16, 16, 4, 2, 50, 50)
            directions = ["proj_down", "proj_right", "proj_up", "proj_left"]
            coef = 90 * directions.index(self.type)
            self.image = pygame.transform.rotate(self.image, coef)
            self.animation_list = []

        self.rect = self.image.get_rect(topleft=pos)

        self.direction = {
            "movement": pygame.math.Vector2(),
            "stationary": pygame.math.Vector2(),
            "proj_up": pygame.math.Vector2(0, -1),
            "proj_down": pygame.math.Vector2(0, 1),
            "proj_left": pygame.math.Vector2(-1, 0),
            "proj_right": pygame.math.Vector2(1, 0),
            "m_ver": pygame.math.Vector2(0, -1),
            "m_hori": pygame.math.Vector2(-1, 0),
        }[self.type]

        self.last_movement = pygame.time.get_ticks()
        self.last_update = pygame.time.get_ticks()
        self.prev_time = time.time()
        self.frozen = False
        self.frozen_timer = pygame.time.get_ticks()

    def move(self, map, map_info):
        self.direction.x = map_info["Enemies"][self.id]["movement"][0]
        self.direction.y = map_info["Enemies"][self.id]["movement"][1]
        if self.direction.x == 1 and self.facing == "left":
            self.turn()
            self.facing = "right"
        if self.direction.x == -1 and self.facing == "right":
            self.turn()
            self.facing = "left"
        if not self.frozen:
            self.last_update, self.frame = animate(
                self.animation_list, 100, self.last_update, 0, self.frame
            )
        self.image = self.animation_list[0][self.frame]
        if not self.frozen:
            now = time.time()
            dt = now - self.prev_time
            self.rect.x += self.direction.x * 2 * dt * 60
            self.check_collision("horizontal", map)
            self.rect.y += self.direction.y * 2 * dt * 60
            self.check_collision("vertical", map)
            self.prev_time = now

    def check_collision(self, direction, map):
        if direction == "horizontal":
            for sprite in map.obsticle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.x > 0:
                        self.rect.right = sprite.rect.left
                    if self.direction.x < 0:
                        self.rect.left = sprite.rect.right
        if direction == "vertical":
            for sprite in map.obsticle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.y < 0:
                        self.rect.top = sprite.rect.bottom
                    if self.direction.y > 0:
                        self.rect.bottom = sprite.rect.top

    def freezetime(self):
        duration = 10000
        if self.frozen:
            self.prev_time = time.time()
            current_time = pygame.time.get_ticks()
            if current_time - self.frozen_timer >= duration:
                self.frozen = False
                self.frozen_timer = current_time
        else:
            self.frozen_timer = pygame.time.get_ticks()

    def Take_damage(self, player, map):
        for sprite in map.weapon_sprites:
            if sprite.rect.colliderect(self.rect):
                player.kill_list.append(self.id)
                Enemy_Death_sound.play(maxtime=100)
                self.kill()
        for sprite in map.arrow_sprites:
            if sprite.rect.colliderect(self.rect):
                player.kill_list.append(self.id)
                Enemy_Death_sound.play(maxtime=100)
                self.kill()
        for sprite in map.flash_sprites:
            if sprite.rect.colliderect(self.rect):
                player.kill_list.append(self.id)
                if sprite.type == "lightning":
                    Particle(
                        self.rect.center,
                        (map.visible_sprites, map.particle_sprites),
                        "lightning",
                    )
                self.kill()
        for sprite in map.freeze_sprites:
            if sprite.rect.colliderect(self.rect):
                Particle(
                    self.rect.center,
                    (map.visible_sprites, map.particle_sprites),
                    "freeze",
                )
                self.frozen = True

    def slide(self, map):
        if map.start_sync:
            current_time = pygame.time.get_ticks()
            cooldown = 5000
            if current_time - self.last_movement >= cooldown:
                self.direction = -self.direction
                self.last_movement = current_time
            now = time.time()
            dt = now - self.prev_time
            self.rect.x += self.direction.x * 4 * dt * 60
            self.check_collision("horizontal", map)
            self.rect.y += self.direction.y * 4 * dt * 60
            self.check_collision("vertical", map)
            self.prev_time = now
        else:
            self.prev_time = time.time()
            self.last_movement = pygame.time.get_ticks()

    def project(self, map):
        if map.start_sync:
            current_time = pygame.time.get_ticks()
            cooldown = 1000
            if current_time - self.last_movement >= cooldown:
                self.last_movement = current_time
                Projectile(self, (map.visible_sprites, map.enemy_sprites), -1)

    def turn(self):
        for animation in self.animation_list:
            for frame in range(len(animation)):
                animation[frame] = pygame.transform.flip(animation[frame], True, False)

    def update(self, player, map, map_info):
        if self.type == "movement":
            self.freezetime()
            self.Take_damage(player, map)
            self.move(map, map_info)
        elif self.type in [
            "stationary",
            "m_ver",
            "m_hori",
        ]:
            self.slide(map)
        elif self.type in ["proj_up", "proj_down", "proj_left", "proj_right"]:
            self.project(map)


# class Range(pygame.sprite.Sprite):
#     def __init__(self,enemy,group):
#         super().__init__(group)
#         self.image=pygame.Surface((250,250))
#         self.image.set_colorkey((0,0,0))

#         self.image.fill("black")
#         self.rect=self.image.get_rect(center=enemy.rect.center)


class Projectile(pygame.sprite.Sprite):
    def __init__(self, enemy, group, id):
        super().__init__(group)
        self.id = id
        self.type = "projectile"
        self.image = pygame.Surface((25, 25))
        self.image.fill("brown")
        self.rect = self.image.get_rect(center=enemy.rect.center)
        self.time = pygame.time.get_ticks()
        self.direction = enemy.direction
        self.speed = 5
        self.prev_time = time.time()
        if self.direction.magnitude() != 0:
            self.direction.normalize()

        #     angle=self.direction.angle_to((1,0))
        #     pygame.transform.rotate(self.image,angle)
        # print(angle)

    def update(self, player, map, map_info):
        current_time = pygame.time.get_ticks()
        duration = 3000
        for sprite in map.obsticle_sprites:
            if sprite.rect.colliderect(self.rect):
                self.kill()
        if current_time - self.time >= duration:
            self.kill()
        now = time.time()
        dt = now - self.prev_time
        self.rect.x += self.direction.x * self.speed * dt * 60
        self.rect.y += self.direction.y * self.speed * dt * 60
        self.prev_time = now
