#The Collatz Sequence

#collatz function
def collatz(number):
    if (number%2 == 0):
        newNumber=number//2
        print(newNumber)
        return newNumber
    else:
        newNumber=3*number+1
        print(newNumber)
        return newNumber



#input validation
def inputValidation():
    try:
        userInput=int(input())
        return userInput
    except ValueError:
        print('Enter a integer!')
    
#main
print('Type the integer you want')
userInput=inputValidation()
#check the user's input to actually be a integer
while(userInput==None):
    userInput=inputValidation()

#creating collatz sequence 
result=collatz(userInput)
while(result!=1):
    result=collatz(result)
print('End of sequence')
    
