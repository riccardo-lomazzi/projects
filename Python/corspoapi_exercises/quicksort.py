def partition(A, p, r):
	x = A[r]
	i = p-1
	for j in range(p,r-1):
		if(A[j]<=x):
			i = i+1
			A[i],A[j] = A[j], A[i]
	A[i+1],A[r] = A[r], A[i+1]
	print(A)
	return i+1


def quicksort(A, p, r):
	if(p<r):
		q = partition(A, p, r)
		quicksort(A, p, q-1)
		quicksort(A, q+1, r)


a = [70, 60, 50, 40, 30, 20, 10]
print("unsorted array:", a)
quicksort(a,0,len(a)-1)
print("sorted array:", a)