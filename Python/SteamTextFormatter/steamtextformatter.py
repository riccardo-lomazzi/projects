print("Enter a string to format as a list for Steam")
unformattedText = input()

unformattedText = unformattedText.replace('LISTA:','',1)
unformattedText = unformattedText.replace(':FINELISTA','',1)

bulletList = unformattedText.split(';')

#aggiungi * ad ogni punto 
formattedText = '\n[*] '.join(bulletList)

print(formattedText)
