def trasposta(grid):
    newGrid = []
    for j in range(col_counter(grid)): #per ogni colonna di grid (devo prima calcolare il numero totale di colonne
        newGrid.append([]) #devo creare un nuovo elemento nella nuova lista, altrimenti non riesce a scrivere perché non trova l'indirizzo
        for i in range(len(grid)): #per tutte le righe della griglia
            #copy inside newGrid the column
            newGrid[j].append(grid[i][j]) #per la prima colonna di grid, scorre le righe e prende gli elementi
        #cambio colonna
        #itera
    return newGrid

#come era in origine la trasposta

def col_counter(grid):
    count = 0
    for j in range(len(grid[0])):
        count+=1
    return count

def printGrid(grid):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            print(grid[i][j], end='')
        print('\n')
    
    
grid = [['.', '.', '.', '.', '.', '.'],
 ['.', 'O', 'O', '.', '.', '.'],
 ['O', 'O', 'O', 'O', '.', '.'],
 ['O', 'O', 'O', 'O', 'O', '.'],
 ['.', 'O', 'O', 'O', 'O', 'O'],
 ['O', 'O', 'O', 'O', 'O', '.'],
 ['O', 'O', 'O', 'O', '.', '.'],
 ['.', 'O', 'O', '.', '.', '.'],
 ['.', '.', '.', '.', '.', '.']]

printGrid(grid)
print('Trasposta')
printGrid(trasposta(grid))

