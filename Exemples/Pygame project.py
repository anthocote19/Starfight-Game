import pygame

pygame.init()
screen=pygame.display.set_mode((500,500))
pygame.display.set_caption("Noughts and crosses")

clock=pygame.time.Clock()
image=pygame.image.load("Project NSI/Board.png")
image=pygame.transform.scale(image,(550,550))
cross=pygame.image.load("Project NSI/cross.png")
cross=pygame.transform.scale(cross,(300,300))
nought=pygame.image.load("Project NSI/nought.png")
nought=pygame.transform.scale(nought,(300,300))
buttoncord=[(50,60),(200,60),(350,60),
            (50,200),(200,200),(350,200),
            (50,350),(200,350),(350,350)]
buttonlist=[]
class button(pygame.Rect):

    def __init__(self,coord_s):
        super().__init__(coord_s,(100,100))
        buttonlist.append(self)
        self.pressed=False
    def __repr__(self):
        return "I"
    
running=True
class grille:
    def __init__(self):
        self.board=[[0,0,0],
                    [0,0,0],
                    [0,0,0]]
        self.tuple=[(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]
    
    def ThereIsWinner(self,player):
        for i in range(3):
            g=0
            for j in range(3):
               if self.board[i][j]==player:
                   g+=1
            if g==3:
                return player
        for j in range(3):
            g=0
            for i in range(3):
               if self.board[i][j]==player:
                   g+=1
            if g==3:
                return player
        g=0
        for i in range(3):
            if self.board[i][i]==player:
                g+=1
            if g==3:
                return player
        for i in range(3,-1,-1):
            if self.board[0][2]==player and self.board[1][1]==player and self.board[2][0]==player:
                return player
        return None

Turn=True
def buttoning(Turn,i,Platform):
    print(Cords_list[i])
    if Turn:
        screen.blit(cross,Cords_list[i])
        Platform.board[Platform.tuple[i][0]][Platform.tuple[i][1]]=1
        print(Platform.ThereIsWinner(1))
    else:
        screen.blit(nought,Cords_list[i])
        Platform.board[Platform.tuple[i][0]][Platform.tuple[i][1]]=2
        print(Platform.ThereIsWinner(2))
    pygame.display.update()
    return not Turn

def reset(Platform,buttonlist):
    Platform.board=[[0,0,0],[0,0,0],[0,0,0]]
    screen.fill("white")
    screen.blit(image,(0,0))
    for i in buttonlist:
       i.pressed=False
       pygame.draw.rect(screen,(255,255,255), i)
    pygame.display.update()
    




Platform=grille()
Cords_list=[(0,0),(150,0),(250,0),
             (0,150),(150,150),(250,150),
             (0,295),(150,295),(250,295)]
for i in buttoncord:
    button(i)


reset(Platform,buttonlist)
while running:

    for event in pygame.event.get():
        if event.type==pygame.QUIT:                                                                                               
            running=False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            for i in range(len(buttonlist)):
                if buttonlist[i].collidepoint(x, y) and not buttonlist[i].pressed:
                    buttonlist[i].pressed=True
                    Turn=buttoning(Turn,i,Platform)
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                reset(Platform,buttonlist)

                    

    clock.tick(60)
    
pygame.quit()
