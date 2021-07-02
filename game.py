import pygame
import random 
import sys

pygame.init()

WIDTH = 900
HEIGHT = 700
BACKGROUND_COLOR = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
player_size = [50,50]
player_speed = 10
player_position = [WIDTH/2-player_size[0]/2,HEIGHT-player_size[1]*3]


frames = pygame.time.Clock()

"""Game settings"""
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS',25)
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.key.set_repeat(10,player_speed)
game_over = False
game_paused = False

enemy_size = [50,50]
enemy_list = []

"""Game Functionalities"""
def createEnemies(enemy_list):
    delay = random.random()
    if len(enemy_list) < 10 and delay < 0.1:
        x_pos = random.randint(0,WIDTH-enemy_size[0])
        y_pos = 0
        enemy_list.append([x_pos,y_pos])

def drawEnemies(enemy_list):
    for enemy_position in enemy_list:
        pygame.draw.rect(screen, BLUE, (enemy_position[0],enemy_position[1],enemy_size[0],enemy_size[1]))

def updateEnemyPostion(enemy_list):
    for index, enemy_position in enumerate(enemy_list):
        if enemy_position[1]>=0 and enemy_position[1] < HEIGHT:
            enemy_position[1]+=10
        else:
            enemy_list.pop(index)

def collisions(enemy_list, player_position,enemy_size, player_size):
    for enemy in enemy_list:
        e_x = enemy[0]
        e_y = enemy[1]
        p_x = player_position[0]
        p_y = player_position[1]

        if (e_x >= p_x and e_x < (p_x + player_size[0])) or (p_x >= e_x and p_x <= (e_x + enemy_size[0])):
            if (e_y >= p_y and e_y < (p_y+player_size[1])) or (p_y >= e_y and p_y <= (e_y+enemy_size[1])):
                return True

"""Game objects"""
continueButton = font.render('Continue',False,(0,0,0))
quitButton = font.render('Quit',False,(0,0,0))


def blur(x):
    while x>=0:
        surf_size = screen.get_size()
        scale_size = (int(surf_size[0]*2),int(surf_size[1])*2)
        surf = pygame.transform.smoothscale(screen,scale_size)
        surf = pygame.transform.smoothscale(surf,surf_size)
        screen.blit(surf,(0,0))
        x-=1


def paused(paused, enemy_list, player_position):
    continue_position_x = WIDTH/5-2
    continue_position_y = HEIGHT/1.7
    continue_size = [110,35]

    quit_position_x = WIDTH/3*2-2
    quit_position_y = HEIGHT/1.7
    quit_size = [110,35]
    
    blur(10)
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_position = pygame.mouse.get_pos()
                if mouse_position[0] >= continue_position_x and mouse_position[0] < (continue_position_x + continue_size[0]):
                    if mouse_position[1] >= continue_position_y and mouse_position[1] < continue_position_y + continue_size[1]:
                        for enemy in enemy_list:
                            enemy[0] = random.randint(0,WIDTH-enemy_size[0])
                            enemy[1] = 0
                        player_position[0] = WIDTH/2-player_size[0]/2
                        player_position[1] = HEIGHT-player_size[1]*3
                        paused = False
                if mouse_position[0] >= quit_position_x and mouse_position[0] < (quit_position_x + quit_size[0]):
                    if mouse_position[1] >= quit_position_y and mouse_position[1] < quit_position_y + quit_size[1]:
                        sys.exit()

        
        pygame.draw.rect(screen,GREEN,(continue_position_x,continue_position_y,continue_size[0],continue_size[1]))
        screen.blit(continueButton,(WIDTH/5,HEIGHT/1.7))
        
        pygame.draw.rect(screen,RED,(quit_position_x,quit_position_y,quit_size[0],quit_size[1]))
        screen.blit(quitButton,(WIDTH/3*2+25,HEIGHT/1.7))

        #blur 
        pygame.display.update()
        frames.tick(30) 
    

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    
        if event.type == pygame.KEYDOWN:
            x = player_position[0]
            y = player_position[1]

            if event.key == pygame.K_LEFT:
                if x>0:
                    x-=10
            elif event.key == pygame.K_RIGHT:
                if x<WIDTH-player_size[0]:
                    x+=10
            elif event.key == pygame.K_UP:
                if y>0:
                    y-=10
            elif event.key == pygame.K_DOWN:
                if y < HEIGHT-player_size[1]:
                    y+=10
                
            player_position = [x,y]
        
    screen.fill(BACKGROUND_COLOR)
    #player
    pygame.draw.rect(screen, RED, ( player_position[0], player_position[1], player_size[0], player_size[1] )) 
    

    #enemy
    createEnemies(enemy_list)
    updateEnemyPostion(enemy_list)
    drawEnemies(enemy_list)
    
    #collisions
    game_paused = collisions(enemy_list, player_position,enemy_size, player_size)
    if game_paused:
        paused(game_paused,enemy_list,player_position)
        updateEnemyPostion(enemy_list)
    frames.tick(20)
    pygame.display.update()
