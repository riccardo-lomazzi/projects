#Table Printer 1.0 - works only with quad matrix

def printTable(userList):
    colMaxWidth = [0] * len(userList)
    #salvo tutte le max larghezze di colonne, mi servono per giustificare il testo
    
    for i in range(len(userList)):
        colMaxWidth[i]=(findMaxWidthInList(userList[i]))
    #mentre scorro la matrice trasposta (perché devo contare per colonna e non per riga), stampo i dati giustificati
    for j in range(col_counter(userList)):
        for i in range(len(userList)):
            print(userList[i][j].rjust(colMaxWidth[i],' '), end=' ')
        print('\n')

def findMaxElementWidthInList(userList):
    maxWidth = len(userList[0])
    for i in range(len(userList)):
        if(len(userList[i]) > maxWidth):
            maxWidth = len(userList[i])
    return maxWidth

def col_counter(grid): #vale solo per matrici quadrate
    count = 0
    for j in range(len(grid[0])):
        count+=1
    return count
        
tableData = [['apples', 'oranges', 'cherries', 'banana'],
['Alice', 'Bob', 'Carol', 'David'],
['dogs', 'cats', 'moose', 'goose']]
printTable(tableData)
