# generate random integer values
from random import seed
from random import randint
import random
import copy

#Funcao responsavel por retornar a coluna atual
def get_coluna(tab, n):
    col = []
    for a in range(0,len(tab)):
        col.append(tab[a][n])
     

    return col

#Funcao responsavel por retornar a celula atual
def get_celula(tab, l1,c1):
    cel = []
    il = 0
         
    if 0 <= l1 < 3:
        il = 0 
        jl = 3
    if 0 <= c1 < 3:
        ic = 0 
        jc = 3
    if 3 <= l1 < 6:
        il = 3 
        jl = 6
        
    if 3 <= c1 < 6:
        ic = 3 
        jc = 6
    
    if 6 <= l1 <=8:
        il = 6 
        jl = 9
        
    if 6 <= c1 <= 8:
        ic = 6 
        jc = 9
    
    
        
    for a in range(il,jl):
        for b in range(ic,jc):
            cel.append(tab[a][b])
     
    
    return cel
   
#get_celula(A,5,5)

#Funcao responsavel concluir se e possivel ou nao colocar um numero de 0 a 9 numa certa entrada do grid
def is_safe(grid,row,col,n):
    
    if (n not in grid[row]) and (n not in get_coluna(grid,col)) and (n not in get_celula(grid,row,col)) :
        return True
    else:
        return False

#Verifica se existe um zero no grid, ou seja, um lugar no grid que ainda nao foi preenchido
def empty_spot(grid,l):
    
    for col in range(0, len(grid)):
        for row in range(0, len(grid)):
            if (grid[row][col] == 0):
                l[0]= row
                l[1]= col
                return True
    return False     
 
#Funcao que resolve o sudoko
def solver(tab,i=[0]):

    i[0]+=1

    l =[0, 0] #Inicializacao do indice das linhas e das colunas
    
    if (empty_spot(tab,l) == False):
        return True
    
    row = l[0] #guarda o indice das linhas atraves da funcao empty_spot
    col = l[1] #guarda o indice das colunas atraves da funcao empty_spot
    
    for i in range(1, 10): #i e numero de 0 a 9

            if is_safe(tab,row,col,i) : #Verifica se o numero i passa nas 
                #condicoes basicas do jogo do Sudoko: ser unico na linha, na coluna e na celula
                   
                tab[row][col] = i   #Caso passe nas condicoes acima, coloca esse numero i na entrada row,col do grid e depois 
                #chama-se a funcao solver() de novo com o grid atualizado para esta entrada row col e tenta-se preencher 
                # a proxima entrada que esteja a zero ate ver se e possivel preencher todo o grid.
                
                #Caso se chegue a um "dead end" em que fiquem zeros por preencher e ja nao e possivel cumprir as regras, 
                #repete-se o processo todo de novo porque na linha 98 se da um reset na entrada inicial desta tentativa de grid resolvido e 
                #como isto e um loop for, logo a proxima tentativa sera diferente e serao tentadas todas as possibilidades.
                     
                if(solver(tab)): #Recursiva ocorre,ate que um grid seja preenchido sem deixar 
                #zeros e onde se cumprem as regras basicas do jogo
                    #print(i[0])
                    return True
                
                tab[row][col] = 0 #Isto executa o backtracking 
                
                
    
    return False
    


def criar_tabuleiro(level):
    grid = []

    lista = [0,1,2,3,4,5,6,7,8,9]
        
    #50 pistas e 31 zeros - nivel 1
    if level == 1:
        limit = 31

    #35 pistas e 46 zeros - nivel 2
    elif level == 2:
        limit = 46

    #20pistas e 61 zeros - nivel 3
    else:
        limit = 61
    run = True
    while run:
        m=100
        grid = [[0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0]]
        while m > limit:
            m = 0
            for i in range(9):
                m = m + grid[i].count(0)
            
            for i in range(9):
                
                s = random.randint(0,int(len(lista))-1)
                a = lista[s]
                for j in range(9):
                    if is_safe(grid,i,j,a):
                        grid[i][j] = a
        copia = copy.deepcopy(grid)
        print("new : \n")
        get_tabuleiro(copia)
        if solver(copia):
            run= False
            
                        
    return grid
                
#Funcao que da print do resultado obtido na funcao solver
def get_tabuleiro(tab):
    puzzle = ''
    state = False
    for a in range(0, len(tab)): #percorrer a matriz tab
        if state and ((a % 3 == 0) and a != 0): #condicao para so criar uma barra de tres em tres numeros
            
            puzzle = puzzle + '\n--------------------------------\n'
            
        elif state:
            
            puzzle = puzzle + '\n'
            
        state = True
        for b in range(0, len(tab)): #percorrer as listas de dentro da matriz tab
            if ((b+1) % 3 == 0 and b != 0):
                
                if tab[a][b] == 0:
                    puzzle = puzzle + ' 0' + ' | '
                        
                elif  tab[a][b] != 0:
                    puzzle = puzzle + ' ' + str(tab[a][b]) + ' | '
            else:
                
                if tab[a][b] == 0:
                        puzzle = puzzle + ' 0' + ' '
                        
                elif  tab[a][b] != 0:
                    puzzle = puzzle + ' ' + str(tab[a][b]) + ' '
    print(puzzle)
    return puzzle

    
#lsd = solver(A) 
#get_tabuleiro(lsd)

if __name__=="__main__":

    A = criar_tabuleiro(2)
    print("Tabuleiro por resolver: \n")
    get_tabuleiro(A)
    
    if (solver(A)):
        print("Tabuleiro Resolvido: \n")
        get_tabuleiro(A)
    else:
        print("No solution exists") 
