#! python3
# PM.py - An insecure password manager program

import pyperclip, sys

PASSWORDS={'prova1' : 'abcd',
           'prova2' : '01234',
           'prova3' : 'boh123'}

if (len(sys.argv)<2):
    print("Usage: python PM.py [account] - copy account password. Type exit to leave")
    sys.exit()
elif sys.argv[1].lower() == 'help':
    print("PM.py is an insecure password manager program that will copy to your clipboard the password of whatever account you specified")
        
account = sys.argv[1] #account name

if (len(sys.argv)>2):
    blargh = sys.argv[2] #test
    print(blargh)

if (account in PASSWORDS):
    pyperclip.copy(PASSWORDS[account])
    print("Password copied to clipboard")
else:
    print("No account found")
    
