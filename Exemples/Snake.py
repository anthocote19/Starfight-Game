""" AHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH"""

import pygame
import time
import random

pygame.init()
pygame.font.init()
width, height = 500, 500
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
Text = pygame.font.SysFont("Arial", 30)
running = True

All_sprites, Cherrys, Tails = (
    pygame.sprite.Group(),
    pygame.sprite.Group(),
    pygame.sprite.Group(),
)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.image = pygame.Surface((50, 50))
        self.image.fill("purple")
        self.rect = self.image.get_rect(topleft=pos)
        self.prevx = pos[0] - 50
        self.prevy = pos[1]
        self.direction = pygame.math.Vector2(50, 0)
        self.cooldown = pygame.time.get_ticks()
        self.tail = [Tail(self, (All_sprites, Tails))]
        self.score = 0
        self.dead = False

    def movement(self):
        current_time = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()
        if self.direction != (-50, 0) and keys[pygame.K_d]:
            self.direction = pygame.math.Vector2(50, 0)
        if self.direction != (50, 0) and keys[pygame.K_q]:
            self.direction = pygame.math.Vector2(-50, 0)
        if self.direction != (0, 50) and keys[pygame.K_z]:
            self.direction = pygame.math.Vector2(0, -50)
        if self.direction != (0, -50) and keys[pygame.K_s]:
            self.direction = pygame.math.Vector2(0, 50)
        if current_time - self.cooldown >= 400:
            self.prevx = self.rect.x
            self.prevy = self.rect.y
            self.cooldown = current_time
            self.rect.x += self.direction.x
            self.rect.y += self.direction.y
            if self.rect.x >= width:
                self.rect.x = 0
            if self.rect.x < 0:
                self.rect.x = width
            if self.rect.y >= height:
                self.rect.y = 0
            if self.rect.y < 0:
                self.rect.y = height
            for sprite in player.tail:
                sprite.follow()

    def get_bigger(self):
        self.score += 1
        self.tail.append(Tail(self.tail[-1], (All_sprites, Tails)))

    def pickup_cherry(self):
        for cherry in Cherrys:
            if self.rect.colliderect(cherry.rect):
                cherry.kill()
                self.get_bigger()

    def die(self):
        for tail in Tails:
            if self.rect.colliderect(tail.rect):
                self.image.fill("blue")
                tail.image.fill("blue")
                self.dead = True


class Tail(pygame.sprite.Sprite):
    def __init__(self, next_tail, group):
        super().__init__(group)
        self.image = pygame.Surface((50, 50))
        self.image.fill("green")
        self.rect = self.image.get_rect(topleft=(next_tail.prevx, next_tail.prevy))
        self.next_tail = next_tail
        self.prevx = self.rect.x - 50
        self.prevy = self.rect.y

    def follow(self):
        self.prevx = self.rect.x
        self.prevy = self.rect.y
        self.rect.x = self.next_tail.prevx
        self.rect.y = self.next_tail.prevy


class Cherry(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.image = pygame.Surface((50, 50))
        self.image.fill("red")
        self.rect = self.image.get_rect(center=pos)


player = Player((250, 250), All_sprites)
Timer = time.time()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_SPACE:
        #         start = True

    if not player.dead:
        player.movement()
        player.pickup_cherry()
        player.die()

        if time.time() - Timer >= 1:
            Cherry(
                (random.randint(0, width), random.randint(0, height)),
                (All_sprites, Cherrys),
            )
            Timer = time.time()
    screen.fill("black")
    All_sprites.draw(screen)
    screen.blit(
        Text.render(f"Score : {player.score}", False, (255, 255, 255)), (380, 400)
    )
    pygame.display.update()
    clock.tick(60)

pygame.quit()
