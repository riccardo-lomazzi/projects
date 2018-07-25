import math

def ordina(A):
    #soluzione Mandrioli - non funziona
    # pos = len(A)-1
    # neg = 0
    # print("neg: " + str(neg) + "pos: " + str(pos))
    # prettyprint(A)
    # while(neg<pos):
    #     if(A[neg] > 0 and A[pos]<0):
    #         A[neg], A[pos] = A[pos], A[neg]
    #     neg+=1
    #     pos-=1
    #     print("neg: " + str(neg) + "pos: " + str(pos))
    #     prettyprint(A)
    x = 0
    i = -1
    for j in range(0,len(A)):
        if(A[j]<x):
            i+=1
            A[i], A[j] = A[j], A[i]
        prettyprint(A)

    

def prettyprint(a):
    for x in range(len(a)):
        print (a[x], end=" ")
    print("")
    
A = [-2,8,7,-1,-3,5,6,4]
ordina(A)

