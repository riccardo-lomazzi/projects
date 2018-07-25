def comma_code(list1):
    if(len(list1)==0 or list1 is None):
        return 'List is empty'
    
    newString = ''
    size = len(list1)
    for i in range(size):
        if(i==size-1):
            newString+=('and ' + str(list1[i]))
        else:
            newString+=(str(list1[i]) + ', ')
    return newString

print('Initialize list. Insert END to end the list')
userList = []
userInput=input()
while(userInput!='END'):
    userList.append(userInput)
    print('element inserted')
    userInput=input()
print('Insertion completed. Showing list with comma code')
print(comma_code(userList))
    
        
        
