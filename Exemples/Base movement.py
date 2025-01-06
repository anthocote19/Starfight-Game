import pygame

pygame.init()
screen = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()
Dino = pygame.image.load("Sprites/DinoSprites - doux.png")
Wall = pygame.image.load("Sprites/DinoSprites - doux.png")
running = True
x, y = 250, 250


def cut_image(image, index, width, height):
    backround = pygame.Surface((width, height))
    backround.set_colorkey((255, 255, 255))
    backround.blit(image, (0, 0), (width * index, 0, width, height))
    backround = pygame.transform.scale(backround, (50, 50))
    return backround


class Mur(pygame.Rect):
    def __init__(self, x, y):
        super().__init__((x, y), (50, 50))

    def placewall(self, offset):
        pygame.draw.rect(screen, (0, 0, 0), self)
        self.move_ip(offset[0], offset[1])
        pygame.draw.rect(screen, (255, 255, 255), self)


class hitbox(pygame.Rect):
    def __init__(self, x, y):
        super().__init__((x, y), (50, 50))

    def placewall(self):
        pygame.draw.rect(screen, (255, 255, 255), self)


steps = 0
animation_list = []
animation_length = [4, 6]
for ani in animation_length:
    temp = []
    for i in range(ani):
        temp.append(cut_image(Dino, steps, 24, 24))
        steps += 1
    animation_list.append(temp)


def turn():
    for animation in animation_list:
        for i in range(len(animation)):
            animation[i] = pygame.transform.flip(animation[i], True, False)


last_upadate = pygame.time.get_ticks()
animation_cooldown = 100
frame = 0
action = 0
direction = "right"
mur_blanc = Mur(100, 100)
collision = hitbox(x, y)
offset = [0, 0]
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYUP:
            action = 0
            frame = 0
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        x += 3
        collision.move_ip(3, 0)
        action = 1
        offset[0] += 3
        if direction == "left":
            turn()
            direction = "right"
        if collision.colliderect(mur_blanc):
            x -= 3
            collision.move_ip(-3, 0)
    if keys[pygame.K_UP]:
        y -= 3
        collision.move_ip(0, -3)
        action = 1
        offset[1] += 3
        if collision.colliderect(mur_blanc):
            y += 3
            collision.move_ip(0, 3)
    if keys[pygame.K_DOWN]:
        y += 3
        collision.move_ip(0, 3)
        action = 1
        offset[1] -= 3
        if collision.colliderect(mur_blanc):
            y -= 3
            collision.move_ip(0, -3)
    if keys[pygame.K_LEFT]:
        x -= 3
        collision.move_ip(-3, 0)
        action = 1
        offset[0] += 3
        if direction == "right":
            direction = "left"
            turn()
        if collision.colliderect(mur_blanc):
            x += 3
            collision.move_ip(3, 0)
    collision.placewall()

    current_time = pygame.time.get_ticks()
    if current_time - last_upadate >= animation_cooldown:
        frame += 1
        last_upadate = current_time
        if frame >= len(animation_list[action]):
            frame = 0
    screen.blit(animation_list[action][frame], (x, y))
    mur_blanc.placewall(offset)
    pygame.display.update()
    offset = [0, 0]
    clock.tick(60)


pygame.quit()
