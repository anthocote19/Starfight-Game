import pygame
pygame.init()

window = pygame.display.set_mode((500, 500))
pygame.display.set_caption("First game")
x = 50
y = 50
width = 20
height = 30
velocity = 10

isJump = False
jumpCount = 8

run = True
while run:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_q] and x > 0:
        x -= velocity
        
    if keys[pygame.K_RIGHT] or keys[pygame.K_d] and x < window.get_width() - width:
        x += velocity

    if not(isJump):
        if keys[pygame.K_UP] or keys[pygame.K_z] and y > 0:
            y -= velocity
        if keys[pygame.K_DOWN] or keys[pygame.K_s] and y < window.get_height() - height:
            y += velocity
        if keys[pygame.K_SPACE]:
            isJump = True
    else:
        if jumpCount >= -8:
            neg = 1
            if jumpCount < 0:
                neg = -1
            y -= (jumpCount ** 2) / 2 * neg
            jumpCount -= 1

        else:
            isJump = False
            jumpCount = 8

    window.fill((0,0,0))
    pygame.draw.rect(window, (255, 0, 255), (x, y, width, height))
    pygame.display.update()


pygame.quit()
