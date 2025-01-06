import pygame
pygame.init()
screen=pygame.display.set_mode((500,500))
clock=pygame.time.Clock()
Dino=pygame.image.load("Project NSI/DinoSprites - doux.png")
running=True
x=0
y=0
def cut_image(image,index,width,height):
    backround=pygame.Surface((width,height))
    backround.blit(image,(0,0),(width*index,0,width,height))
    backround=pygame.transform.scale(backround,(50,50))
    return backround

steps=0
animation_list=[]
animation_length=[4,6]
for ani in animation_length:
   temp=[]
   for i in range(ani):
       temp.append(cut_image(Dino,steps,24,24))
       steps+=1
   animation_list.append(temp)
def turn():
    for animation in animation_list:
        for i in range(len(animation)):
            animation[i]=pygame.transform.flip(animation[i],True,False)
    



last_upadate=pygame.time.get_ticks()
animation_cooldown=100
frame=0
action=0
direction=True
while running:

    for event in pygame.event.get():
        if event.type==pygame.QUIT:                                                                                               
            running=False
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_RIGHT and not direction:
                 turn()
                 direction=not direction
            if event.key==pygame.K_LEFT and direction:
                turn()
                direction=not direction
            action=1
            frame=0
        if event.type==pygame.KEYUP:
            action=0
            frame=0
    keys=pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
         x+=3
    if keys[pygame.K_UP]:
         y-=3
    if keys[pygame.K_DOWN]:
         y+=3
    if keys[pygame.K_LEFT]:
        x-=3
    screen.fill('black')
    
    current_time=pygame.time.get_ticks()
    if current_time-last_upadate>=animation_cooldown:
        frame+=1
        last_upadate=current_time
        if frame>=len(animation_list[action]):
           frame=0
    

    screen.blit(animation_list[action][frame],(x,y))

    pygame.display.update()
    clock.tick(60)


pygame.quit()

