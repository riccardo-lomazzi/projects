import re

#first approach
def firstMethod(word, toSearch):
    m = re.compile(toSearch) #cambiare la split
    if(m.search(word)):
        return 'MATCH FOUND FOR ' + toSearch
    else:
        return 'NO MATCH FOUND FOR' + toSearch

def secondMethod(word, toSearch):
    if(bool(re.search(toSearch,word))):
        return 'MATCH FOUND FOR ' + toSearch
    else:
        return 'NO MATCH FOUND FOR' + toSearch
        
#main
userInput=''
while(userInput!='exit'):
    print('Insert string')
    userInput = input() #get user input
    print(secondMethod(userInput,r'(?i)\borario\b\s[a-zA-Z]\.\d\.\d')) #tutte le altre aule con una sola cifra
    print(secondMethod(userInput,r'(?i)\borario\b\s[a-zA-Z]\.\d\d\.\d\d')) #L26
    
    #print(secondMethod(userInput,'def'))#
