import random

print('Pallina magica')

messages = ['Andrà tutto bene', 'Potrebbe andare meglio, ma ok', "L'inverno sta arrivando"]

print('Digita E per uscire, o qualsiasi altro carattere per continuare')
userInput = input()
while(userInput != 'E'):
    print("Messaggio random: " + messages[random.randint(0, len(messages)-1)])
    print('Premi un pulsante per continuare o E per uscire')
    userInput = input()
