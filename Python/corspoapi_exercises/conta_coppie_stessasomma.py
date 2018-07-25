def check(arr):
    if(len(arr)%2 == 0):
        arr.sort()
        print("Sorted:")
        print(arr)
        t = arr[0]+arr[len(arr)-1]
        print("t: " + str(t))
        for i in range(1,len(arr)):
            sum = arr[i]+arr[len(arr)-i-1]
            print("arr[i]: " + str(arr[i]))
            print("arr[n-i-1]" + str(arr[len(arr)-i-1]))
            print("Sum: " + str(sum))
            if((sum) !=  t):
                return False
        return True
    
arr = [1, 7 ,4 ,2 ,4 ,0 ,8, 6]
print(arr)
print(check(arr))