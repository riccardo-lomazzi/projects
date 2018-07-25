import sys, getpass

def somma(a,b):
    return a+b

nameLogin=''
wrongPasswordRetries = 3
#Enter username
while(not nameLogin): #this way, the program keeps asking for a name if an empty string is inserted 
    print('Enter your credentials\nEnter your name')
    nameLogin = input()
print('Hello '+nameLogin)
#Enter password
passwordLogin = getpass.getpass('please enter your password: ')
while(passwordLogin != 'password'):
    wrongPasswordRetries = wrongPasswordRetries - 1
    print('Wrong password. Please enter the correct one. Retries = ' + str(wrongPasswordRetries))
    if (wrongPasswordRetries <= 0):
        print('Entered wrong password too many times.')
        sys.exit()
    else:
        passwordLogin = getpass.getpass('please re-enter your password: ')
print('Done!')
print('Total length of your name + password: ' + str(somma(len(nameLogin),len(passwordLogin))))



        
