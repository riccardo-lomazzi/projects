import math
import random

def selezione(A,k):
	if len(A) < 50:
		A.sort()
		return A[k]
	else:
		B = chunks(A,k)
		for i in range(0, len(B)):
			B[i].sort()
	#build M of medium values of K subsets
	M = []
	for j in range(0, len(B)):
		M.append(B[j][3])
	m = selezione(M, math.ceil(len(M)/2))
	A1 = [] 
	A2 = []
	A3 = []
	for i in range(0, len(A)):
		if(A[i] < m):
			A1.append(A[i])
		if(A[i] == m):
			A2.append(A[i])
		if(A[i] > m):
			A3.append(A[i])
	if(len(A1)>=k):
		x = selezione(A1,k)
		return x
	else:
		if(len(A1)+len(A2)>=k):
			return m
		else:
			x = selezione(A3, k - (len(A1)+len(A2)))
			return x


#divides A in subsets of 5 elements and returns an array of them
# def divideArraySubsets(A, y):
# 	subsets = len(A)/y
# 	B = []
# 	while(subsets>0):
# 		B.append(A[])
# 		subsets--
def chunks(A, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(A), n):
        yield A[i:i + n]

# def chunks2(l, n):
# 	n = max(1, n)
#     return (l[i:i+n] for i in range(0, len(l), n))

def randomgenArray(A, n):
	for i in range(0,n):
		A.append(random.randint(0,n))
	return A

A = []
A = randomgenArray(A, 60)
for k in range(0,5):
	print("Il " + str(k) + "-esimo più piccolo elemento è: " + selezione(A,k))