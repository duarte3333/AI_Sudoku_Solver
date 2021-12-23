import pygame
import os
import time
import sys
from sudoky import criar_tabuleiro,empty_spot
from sudoky import is_safe
import copy
from ai_solver import*

pygame.init()
pygame.font.init()
pygame.mixer.init()

# Set window resolution
cell = 500/9
val = 0
WIDTH, HEIGHT = 500,550
CENTER = WIDTH // 2 - 100
WHITE = (255,255,255)
BLUE = (0,180,200)
BLACK = (0,0,0)
GREEN = (100,255,100)
RED = (255, 55, 0)
GRAY = (211,211,211)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("SUDOKU")
img = pygame.image.load('image2.png')
pygame.display.set_icon(img)
background_image = pygame.image.load("blue-background.jpg").convert()
#background_sound = pygame.mixer.Sound("background.mp3")
correct_sound = pygame.mixer.Sound("correct.mp3")
wrong_sound = pygame.mixer.Sound("wrong.mp3")
# Load test fonts for future use

font1 = pygame.font.SysFont("PRESSSTART2P", 30)
font2 = pygame.font.SysFont("PRESSSTART2P", 50)
numbers = pygame.font.SysFont("None", 40)
font3 = pygame.font.SysFont("PRESSSTART2P", 9)
font4 = pygame.font.SysFont("Atari", 40)

def get_cord(pos):
    global x
    x = pos[0]//cell
    global y
    y = pos[1]//cell
    
    
def draw_draftval(val):
    BLANK = pygame.Rect(x * cell + 2 , y * cell + 2 , cell - 1.5, cell - 1.5)
    pygame.draw.rect(WIN,GRAY,BLANK,0)        
    text1 = numbers.render(str(val), 1, (0, 0, 0))
    WIN.blit(text1, (x * cell + 15, y * cell + 15))
    
    
def draw_blank():
    BLANK = pygame.Rect(x * cell + 2 , y * cell + 2 , cell - 1.5, cell - 1.5)
    pygame.draw.rect(WIN,WHITE,BLANK,0)        
    text1 = numbers.render(" ", 1, (0, 0, 0))
    WIN.blit(text1, (x * cell + 15, y * cell + 15))

def draw_greenval(val,sound):
    if sound:
        pygame.mixer.Sound.play(correct_sound)
    BLANK = pygame.Rect(x * cell + 2 , y * cell + 2 , cell - 1.5, cell - 1.5)
    pygame.draw.rect(WIN,BLUE,BLANK,0)        
    text1 = numbers.render(str(val), 1, (0, 0, 0))
    WIN.blit(text1, (x * cell + 15, y * cell + 15))

def draw_redval(val,counter,sound):
    if sound:
        pygame.mixer.Sound.play(wrong_sound)
    text = font1.render("X " * (counter+1), 1, (255, 0, 0))
    WIN.blit(text, (20, 510)) 
    BLANK = pygame.Rect(x * cell + 2 , y * cell + 2 , cell - 1.5, cell - 1.5)
    pygame.draw.rect(WIN,RED,BLANK,0)        
    text1 = numbers.render(str(val), 1, (0, 0, 0))
    WIN.blit(text1, (x * cell + 15, y * cell + 15))
    
def draw_cross(counter):
    text = font1.render("X " * (counter+1), 1, (255, 0, 0))
    WIN.blit(text, (20, 510))     
    

def draw_menu(level1,level2,level3):
    WIN.blit(background_image, [0, 0])  
    TITLE = pygame.Rect(CENTER-40,75,200,50)
    text0 = font2.render("SUDOKU", True, WHITE)
    text1 = font1.render("EASY", True, WHITE)
    text_rect1 = text1.get_rect(center=(CENTER+100, CENTER+50))
    text2 = font1.render("MEDIUM", True, WHITE)
    text_rect2 = text2.get_rect(center=(CENTER+100, CENTER+150))
    text3 = font1.render("HARD", True, WHITE)
    text_rect3 = text3.get_rect(center=(CENTER+100, CENTER+250))
    text5 = font1.render("SCAN", True, WHITE)
    text_rect5 = text5.get_rect(center=(CENTER+100, CENTER+350))    
    text4 = font1.render("?", True, WHITE)
    text_rect4 = text4.get_rect(center=(440, 470))
    WIN.blit(text0,TITLE)
    WIN.blit(text1,text_rect1)
    WIN.blit(text2,text_rect2)
    WIN.blit(text3,text_rect3)
    WIN.blit(text5,text_rect5)
    WIN.blit(text4,text_rect4)
    
def show_commands():
    WIN.fill(WHITE)
    WIN.blit(background_image, [0, 0])
    TITLE = pygame.Rect(CENTER-65,50,250,50)
    R = pygame.Rect(CENTER-75,125, 250,20)
    CREDITS = pygame.Rect(CENTER-75, 175, 250, 20)    
    #pygame.draw.rect(WIN,GREEN,TITLE,0)
    #pygame.draw.rect(WIN,BLACK,R,0)
    #pygame.draw.rect(WIN,BLACK,CREDITS,0)
    text0 = font1.render("COMMANDS", True, WHITE)
    text1 = font3.render("- R is used to go back to the main menu", True, WHITE)
    text3 = font3.render("Authors: Duarte Morais and Martim Baltazar", True, WHITE)
    text4 = font3.render("if Mecanica + Informatica == True:", True, WHITE)
    text5 = font3.render("      job = good job;        ", True, WHITE)
    text2 = font3.render("- Credits", True, WHITE)  
    WIN.blit(text0,TITLE)
    WIN.blit(text1,R)
    WIN.blit(text3,R)
    WIN.blit(text4,R)
    WIN.blit(text5,R)
    WIN.blit(text2,CREDITS)    

def solver(grid,i=[0]):
    
    i[0]+=1
    l =[0, 0] #Inicializacao do indice das linhas e das colunas
    
    if (empty_spot(grid,l) == False):
        return True
    
    row = l[0] #guarda o indice das linhas atraves da funcao empty_spot
    col = l[1] #guarda o indice das colunas atraves da funcao empty_spot
    pygame.event.pump()   
    for i in range(1, 10): #i e numero de 0 a 9
            if is_safe(grid,row,col,i) : #Verifica se o numero i passa nas 
                #condicoes basicas do jogo do Sudoko: ser unico na linha, na coluna e na celula
                global x, y
                x = row
                y = col               
                grid[row][col] = i   
                WIN.fill(WHITE)
                draw_grid(grid)
                pygame.display.update()
                pygame.time.delay(25)                
                     
                if(solver(grid)):
                    return True
                
                grid[row][col] = 0 
                WIN.fill(WHITE)
                draw_grid(grid)
                draw_redval(i,2,False)
                pygame.display.update()
                pygame.time.delay(25)                   
                
    return False    

def draw_grid(grid):
    state = False
    WIN.fill(WHITE) #restore WIN
    for i in range (9):
        for j in range (9):
            if grid[i][j]!= 0:
                pygame.draw.rect(WIN, BLUE, (i * cell, j * cell, cell + 1, cell + 1))
                number = numbers.render(str(grid[i][j]), 1, (0, 0, 0))
                WIN.blit(number, (i * cell + 15, j * cell + 15))
    # Draw lines horizontally and vertically to form grid          
    for i in range(10):
        if i % 3 == 0 :
            thick = 6
        else:
            thick = 2
        pygame.draw.line(WIN, (0, 0, 0), (0, i * cell), (500, i * cell), thick)
        pygame.draw.line(WIN, (0, 0, 0), (i * cell, 0), (i * cell, 500), thick)
    
    for i in range(9):
        for j in range(9):
            if (grid[i][j] == 0):
                state = True
    if state == False:
        text2 = font1.render("GGS,TRY AGAIN!", True, BLACK)
        text_rect2 = text2.get_rect(center=(260,530))
        WIN.blit(text2,text_rect2)
        


def main():
    EASY = pygame.Rect(CENTER,175, 200,50)
    MEDIUM = pygame.Rect(CENTER, 275, 200, 50)
    HARD = pygame.Rect(CENTER, 375, 200, 50)
    draw_menu(EASY,MEDIUM,HARD)
    counter = 0
    val = 0
    grid = []
    state = True
    run = True
    while run:
        if counter == 3:
            if solver(copy_grid2) == True:
                state = True
                draw_grid(copy_grid2)
                counter = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if state:
                if event.type == pygame.MOUSEBUTTONUP:
                    mouseX = event.pos[0]
                    mouseY = event.pos[1]
                    if CENTER < mouseX < (CENTER + 200) and 175 < mouseY < 225:
                        grid = criar_tabuleiro(1)
                        copy_grid = copy.deepcopy(grid)
                        copy_grid2 = copy.deepcopy(grid)
                        draw_grid(grid)
                    if CENTER < mouseX < (CENTER + 200) and 275 < mouseY < 325:
                        grid = criar_tabuleiro(2)
                        copy_grid = copy.deepcopy(grid)
                        copy_grid2 = copy.deepcopy(grid)
                        
                        draw_grid(grid)
                    if CENTER < mouseX < (CENTER + 200) and 375 < mouseY < 425:
                        grid = criar_tabuleiro(3)
                        copy_grid = copy.deepcopy(grid)
                        copy_grid2 = copy.deepcopy(grid)
                        draw_grid(grid)
                    if CENTER < mouseX < (CENTER + 200) and 475 < mouseY < 525:
                        grid1 = main_ai()
                        zipped_rows = zip(*grid1)
                        grid = [list(row) for row in zipped_rows]
                        copy_grid = copy.deepcopy(grid)
                        copy_grid2 = copy.deepcopy(grid)
                        draw_grid(grid)                    
                    elif 425 < mouseX < 465 and 450 < mouseY < 490:
                        show_commands()           
                    state = False
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                get_cord(pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    val = 1
                if event.key == pygame.K_2:
                    val = 2   
                if event.key == pygame.K_3:
                    val = 3
                if event.key == pygame.K_4:
                    val = 4
                if event.key == pygame.K_5:
                    val = 5
                if event.key == pygame.K_6:
                    val = 6
                if event.key == pygame.K_7:
                    val = 7
                if event.key == pygame.K_8:
                    val = 8
                if event.key == pygame.K_9:
                    val = 9                             
                if event.key == pygame.K_r:
                    WIN.fill(WHITE)
                    draw_menu(EASY,MEDIUM,HARD)
                    state = True 
                    counter = 0
                if val != 0:
                        draw_draftval(val)
                        copy_grid[int(x)][int(y)]= val
                        val = 0
                if event.key == pygame.K_RETURN:
                    val = copy_grid[int(x)][int(y)]
                    if is_safe(grid,int(x),int(y),val):
                        draw_greenval(val,True)
                        grid[int(x)][int(y)] = val
                    else:
                        draw_redval(val,counter,True)
                        counter += 1
                    val = 0
                if event.key == pygame.K_BACKSPACE:
                    copy_grid[int(x)][int(y)] = 0
                    grid[int(x)][int(y)] = 0
                    draw_blank()
    
        pygame.display.update()
    pygame.display.quit()
    pygame.quit()
    sys.exit()

main()