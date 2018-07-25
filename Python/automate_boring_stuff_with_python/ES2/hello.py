print('Hello World')
print ('What is your name?')
myName=input()
print('Nice to meet you, ' + myName)
print('Length of your name is ' + str(len(myName)))
print('Awaiting your input "1" to close the program')
print('spam'*3)
esc=int(input())
while(esc != 1):
    print('Wrong input, insert "1"')
    esc=int(input()) #int(input()) realizza il casting del risultato di input(), che è una stringa
