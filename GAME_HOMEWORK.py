import pygame
 
WIN_WIDTH = 860
WIN_HEIGHT = 640
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (125, 125, 125)
LIGHT_BLUE = (64, 128, 255)
GREEN = (0, 200, 64)
YELLOW = (225, 225, 0)
PINK = (230, 50, 230)
ORANGE = (255, 150, 100)
BLUE = (0, 70, 225)
RED = (180, 0, 0)
FON = (255,211,155)
FPS = 60
P_WIDTH = 70
P_HEIGHT = 10
INDENT = 100
GAME_WIDTH = 660
GAME_HEIGHT = 440
b_MOVE_SPEED_x = 3
p_MOVE_SPEED_x = 6
MOVE_SPEED_y = 3
BRICK_WIDTH = 33
BRICK_HEIGHT = 22
LIFE = 3
NEW_GAME = True
SCORE = 0

entities = pygame.sprite.Group()

level = [
       [0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0],
       [0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0],
       [0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0],
       [0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
       [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
       [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
       [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
       [0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
       [0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0],
       [0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0],
       [0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
     
class OBJECT(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, COLOR):
        pygame.sprite.Sprite.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.startX = x 
        self.startY = y
        self.image = pygame.Surface((w,h))
        self.image.fill(COLOR)
        self.rect = pygame.Rect(x, y, w, h)

    def update(self,  left_x, right_x, down_y, up_y, MOVE_SPEED_x, MOVE_SPEED_y):
        if left_x:
            self.xvel = -MOVE_SPEED_x 
        if right_x:
            self.xvel = MOVE_SPEED_x         
        if not(left_x or right_x):
            self.xvel = 0        
        if up_y:
            self.yvel = -MOVE_SPEED_y 
        if down_y:
            self.yvel = MOVE_SPEED_y         
        if not(down_y or up_y):
            self.yvel = 0
        self.rect.x += self.xvel
        self.rect.y += self.yvel
        
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        
class BRICK(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.startX = x
        self.startY = y
        self.image = pygame.Surface((BRICK_WIDTH - 1, BRICK_HEIGHT - 1))
        self.image.fill(PINK)
        self.rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)
 
BALL_OBJECT = OBJECT(INDENT + P_WIDTH//2, 510 , 20, 20, GREEN)    
PLATFORM_OBJECT = OBJECT(100, 530, 70, 10, BLUE)
 
pygame.init()
sc = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
surf = pygame.Surface((WIN_WIDTH - 200, WIN_HEIGHT - 200)) 
surf.fill(WHITE) 
sc.blit(surf, (100, 100))
pygame.display.set_caption('Game')
clock = pygame.time.Clock()
pygame.draw.rect(sc, BLUE, PLATFORM_OBJECT)
pygame.display.update()
 
r = 10
p_left = p_right = False
b_left_x = b_up_y = b_right_x = b_down_y = False
start = False

while True:    
    if NEW_GAME:
        SCORE = 0
        Xb = Yb = 100
        for i in level:
            for j in i:
                if j == 1:
                    pf = BRICK(Xb,Yb)
                    entities.add(pf)
                    SCORE += 1
                    Xb += BRICK_WIDTH
            Yb += BRICK_HEIGHT
            Xb = 100
        NEW_GAME = False
    if SCORE <= 0:
        sc.fill(WHITE)
        f1 = pygame.font.Font(None, 56)
        text1 = f1.render('YOY WIN! PRESS SPACE AND START NEW GAME', 1, (180, 0, 0))
        sc.blit(text1, (100, 100))
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                pygame.quit()
                exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            start = False
            LIFE = 3
            NEW_GAME = True        
        pygame.display.update()
    else:
        if LIFE>0:
            sc.fill(FON)
            surf.fill(WHITE)
            sc.blit(surf, (100, 100))
            entities.update()
            entities.draw(sc)
            for b in range(1,LIFE  + 1):
                pygame.draw.circle(sc, RED, (WIN_WIDTH - b * 70 ,50), 30)
                f0 = pygame.font.Font(None, 48)
            text0 = f0.render('LIFE: ', 1, (180, 0, 0))
            sc.blit(text0, (WIN_WIDTH - (LIFE+2)*70, 50))
            if start:
                PLATFORM_OBJECT.update(p_left, p_right, False, False, p_MOVE_SPEED_x, 0)
                if PLATFORM_OBJECT.rect.x<=100:
                    PLATFORM_OBJECT.rect.x = 100
                if PLATFORM_OBJECT.rect.x + 70 >= 760:
                    PLATFORM_OBJECT.rect.x = 690
                PLATFORM_OBJECT.draw(sc)
                BALL_OBJECT.update(b_left_x, b_right_x, b_down_y, b_up_y, b_MOVE_SPEED_x, MOVE_SPEED_y) # передвижение
                BALL_OBJECT.draw(sc)
            else:
                PLATFORM_OBJECT.update(p_left, p_right, False, False, p_MOVE_SPEED_x, 0)
                if PLATFORM_OBJECT.rect.x<=100:
                    PLATFORM_OBJECT.rect.x = 100
                elif PLATFORM_OBJECT.rect.x + 70 >= 760:
                    PLATFORM_OBJECT.rect.x = 690
                else:
                    BALL_OBJECT.update(b_left_x, b_right_x, b_down_y, b_up_y, p_MOVE_SPEED_x, MOVE_SPEED_y) # передвижение
                BALL_OBJECT.draw(sc)
                PLATFORM_OBJECT.draw(sc)
            clock.tick(FPS)         
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    pygame.quit()
                    exit()         
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                start = True
                b_right_x = True
                b_up_y = True
            if keys[pygame.K_LEFT]:
                p_left = True
                p_right = False
                if start == False:
                    b_left_x = True
                    b_right_x = False
            elif keys[pygame.K_RIGHT]:
                p_right = True
                p_left = False
                if start == False:
                    b_left_x = False
                    b_right_x = True
            else:
                p_left = False
                p_right = False
                if not(start):
                    b_left_x = False
                    b_right_x = False 
            if start:
                if BALL_OBJECT.rect.x + r >= WIN_WIDTH - 110:
                    b_left_x = True
                    b_right_x = False
                if BALL_OBJECT.rect.x - r <= 90:
                    b_left_x = False
                    b_right_x = True
                if BALL_OBJECT.rect.y + r >= WIN_HEIGHT - 100:
                    b_down_y = False
                    b_up_y = False
                    b_left_x = False
                    b_right_x = False
                    LIFE-=1
                    start = False
                    pygame.time.delay(1000)
                    BALL_OBJECT.rect.x = PLATFORM_OBJECT.rect.x + P_WIDTH//2
                    BALL_OBJECT.rect.y = 510
                    srart = False
                if BALL_OBJECT.rect.y - r <= 90:
                    b_down_y = True
                    b_up_y = False
                if  BALL_OBJECT.rect.colliderect(PLATFORM_OBJECT.rect):
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_LEFT]:
                        b_left_x = True
                        b_right_x = False
                    elif keys[pygame.K_RIGHT]:
                        b_right_x = True
                        b_left_x = False
                    b_up_y = True
                    b_down_y = False
                    BALL_OBJECT.rect.y = 510
                    BALL_OBJECT.rect.x += -p_MOVE_SPEED_x*p_left*2 + p_MOVE_SPEED_x*p_right*2
                blocks_hit_list = pygame.sprite.spritecollide(BALL_OBJECT, entities, True)
                SCORE -= len(blocks_hit_list)
                if len(blocks_hit_list)!=0:
                    for a in blocks_hit_list:
                        if BRICK_WIDTH - 4 <= abs(a.rect.x - BALL_OBJECT.rect.x) <= BRICK_WIDTH:
                            t = b_left_x
                            b_left_x = b_right_x
                            b_right_x = t
                        else:
                            t = b_up_y
                            b_up_y = b_down_y
                            b_down_y = t
                        break
            pygame.display.update()
        else:
            sc.fill(BLACK)
            f1 = pygame.font.Font(None, 48)
            text1 = f1.render('GAME OVER!', 1, (180, 0, 0))
            text11 = f1.render('PRESS SPACE AND START NEW GAME', 1, (180, 0, 0))
            sc.blit(text1, (300, 300))
            sc.blit(text11, (70, 350))
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                start = False
                LIFE = 3
                NEW_GAME = True
            
            pygame.display.update()