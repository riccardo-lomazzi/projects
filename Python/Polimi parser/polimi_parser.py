from html.parser import HTMLParser
from bs4 import BeautifulSoup
from urllib.request import urlopen


#///////////////POLIMI PARSER v. 0.8 beta //////////////#


#PROGRAM LOGIC: COUNT ALL THE TD WITH ID='EMPTY' BEFORE THE START OF THE LESSON
#how to count
# 1 - contare tutte le td con classe che contiene 'empty', valgono 15 minuti l'uno
# 2 - l'equazione è 8 (ora iniziale) + 0,25 (cioè 15m/60 -> ore) * x (numero di td contate) = y (ora da trovare)
# 3 - se esiste un td con colspan prima di lui (cioè un'altra lezione), devo convertire il numero di quarti d'ora occupati da quel colspan in ore ed aggiungerle. Quindi y + (colspan/60)
# 4 - inserisco y in datetime.timedelta(hours=y) che converte i td in ore corrette (anche nel caso di decimali, ad es ora=9.25 -> 09:15:00)


#///////////////PROBLEMI DA RISOLVERE//////////////#
#1 [RISOLTO] Orario iniziale sbagliato di 15m. Probabilmente non viene contato un td - SOLUTION FOUND: era sbagliato scrivere int(listResult[el]['colspan'][0]) 
#perché così andava a prendere la prima cifra della stringa e la trasformava in intero
#2 [RISOLTO] non mi piace molto la funzione rowReturner, che usa un flag per vedere se restituire la riga. Vedere se si può fare meglio SOLUTION: va bene così. Tanto la riga la devo ricopiare comunque come sequenza di td, e devo assicurarmi che copi solo quelli
#se non mettessi il for su column, mi conterebbe anche altri tag
#3 [DA RISOLVERE] Non va la pagina di prova. Non funziona con certe aule, non riesce a trovare il link a su alcune righe. Forse alcune aule non hanno il link, oppure esistono delle righe di classe "normalRow" che non sono della tabella/sono vuote. Bisogna migliorare la ricerca su queste 
#///////////////AGGIUNTE DA FARE////////////////////#
#1 - GIORNO NELL'URL: per ora è predefinito, ma va preso il giorno corrente e aggiunto nella stringa dell'url
#2 Input utente
#3 Bot Telegram


#///////CLASSE LESSON_TIME///////////////
#Contiene l'orario in ore, minuti, secondi e lo restituisce formattato in una stringa di "ore:minuti"
 
class Lesson_Time:
    def __init__(self, hrs):
        self.hours = int(hrs)
        self.minutes = (hrs*60) % 60
        self.seconds = (hrs*3600) % 60
        
    def getLessonTimeToString(self):
        return "%d:%02d" % (self.hours, self.minutes)


    
#step 1
def findLessonStartHour(tdList, lessonTDIndex):
    TDSum=0
    for i in range(0,lessonTDIndex):
        #se prima della lezione, ce n'è un'altra, somma quel colspan
        if tdList[i].has_attr('colspan'): #in questo caso non ci sono lezioni prima di Sistemi Radio Satellitari, perciò questa parte non sarà mai conteggiata
            TDSum+=int(tdList[i]['colspan'])
            #altrimenti, conto solo i td che indicano i quarti d'ora
        elif (tdList[i]['class'][0] == 'empty' or tdList[i]['class'][0] == 'empty_prima'):
            TDSum+=1 
    return TDSum

#step 2, 3 of 'empty' counting; 0.25 stands for 15 minutes/60, which means a quarter of hour (a single 'empty' td) 
#initialSpan is for the missing td in the table (before initialSpan am -> 8pm for polimi timetables)
def convertTDNumberToHours(tdNumber, initialTDSpan):
    return initialTDSpan+(0.25*tdNumber)        

#sto facendo due cose insieme: salvare la lista, e scorrerla per vedere se la riga è quella cercata. 
# #returns the row of the searched classroom
# def rowReturner(soup, aula):
    # result=False
    # contaTD=[]
    # TRList = soup.find_all('tr', class_='normalRow')
    # # EXCEPTION 1 - NO ROWS FOUND - return null (beta) - Alternative: encapsulate everything in a try-catch-finally block
    # if(len(TRList) == 0):
        # return null, null
    # for row in TRList: #for every row of the table
        # returnedTDList=[]
        # TDList = row.find_all('td')
        # # EXCEPTION 2 - NO COLUMNS FOUND - return null (beta) - Alternative: encapsulate everything in a try-catch-finally block
        # if(len(TDList) == 0):
            # return null, null
        # for column in TDList: #if there's a column that contains the 'dove' attribute, that indicates the classroom
            # returnedTDList.append(column) #save the column in the list of columns that's going to be returned
            # if(column['class'][0] == 'slot'):
                # contaTD.append(returnedTDList.index(column)) #if the td is a lesson, save its index
            # if (column['class'][0] == 'dove' and column.a is not None and column.a.string.replace(".","").strip('\n ') == aula): #if it matches with the input classroom
                # result = True #save the information
    # if result is True: #only if the row is found, return the list with all the columns, and the list with indexes of the td that contain the lessons
        # return returnedTDList, contaTD

#///////////////ROW RETURNER ALTERNATIVO////////////////////#    
#Scorre la lista 3 volte: una per trovare le righe, una per inserire i td in una lista, infine una per salvare l'indirizzo delle TD che contengono le lezioni      
#Codice più pulito, ma sicuramente più lento. 

def rowReturnerAlt(soup, aula):
    TRList = soup.find_all('tr', class_='normalRow')
    LessonIndexes = []
    # EXCEPTION 1 - NO ROWS FOUND - return null (beta) - Alternative: encapsulate everything in a try-catch-finally block
    if(len(TRList) == 0):
        return None, None
    for row in TRList:
        TDList = findCorrectRow(row, aula)
        # EXCEPTION 2 - NO COLUMNS FOUND - don't worry, let's try the next row by interrupting the for with a continue
        if(TDList == None or len(TDList) == 0):
            continue
        else:
            TDList = saveTDInList(row)
            LessonIndexes = findLessonIndexes(TDList)
            return TDList, LessonIndexes
    # EXCEPTION 3 - NO ROW FOUND - return None
    return None, None 
            
def findLessonIndexes(TDList):
    LessonIndexes = []
    for column in TDList:
        if(column['class'][0] == 'slot'):
            LessonIndexes.append(TDList.index(column)) #if the td is a lesson, save its index
    return LessonIndexes
            
def findCorrectRow(row, aula):
    rowtds = row.findAll('td')
    if(row is None or len(rowtds) == 0):
        return None
    for column in rowtds: 
        if (column['class'][0] == 'dove' and column.a is not None and column.a.string.replace(".","").strip('\n ') == aula):
            return row
    return None

def saveTDInList(row):
    temp = []
    for column in row.findAll('td'):
        temp.append(column)
    return temp

#///////////////FINE ROW RETURNER ALTERNATIVO////////////////////#      
    




#/////////////////// MAIN ////////////////////#   

#/////////////// MAIN FUNCTION //////////////////

def main(timetableURL, classroom, date):
    #set URL and get raw html data
    raw_html = urlopen(timetableURL)
    soup = BeautifulSoup(raw_html, 'html.parser')
    
    #print only the row that has td with the correct classroom
    listResult, LessonsTDIndexList = rowReturnerAlt(soup, classroom)
    if(listResult is None or listResult[0]=='NF'):
        #print('Aula non trovata')
        message = 'Aula non trovata'
    elif (LessonsTDIndexList is None or len(LessonsTDIndexList) == 0):
        #print('Nessuna lezione programmata per la giornata')
        message = 'Nessuna lezione programmata per la giornata'
    else:
        #create dictionary
        lessons_dictionary = {}
        #print('Trovate le seguenti lezioni: ')
        message = "Trovate le seguenti lezioni per l'aula " + classroom + 'in data ' + date.strftime("%d-%m-%Y") + '\n' 
        i = 0
        for el in LessonsTDIndexList:
            lessonStartCount = findLessonStartHour(listResult,el)
            lessonStartHour = convertTDNumberToHours(lessonStartCount,8)
            lessonEndHour = lessonStartHour + convertTDNumberToHours(int(listResult[el]['colspan']),0)
            #salvo nel dizionario -> nome corso, ora inizio, ora fine - step 4
            lessons_dictionary[i] = [listResult[el].a.string , Lesson_Time(lessonStartHour), Lesson_Time(lessonEndHour)]
            # print('Corso: ', lessons_dictionary[i][0], '\nOra inizio:', lessons_dictionary[i][1].getLessonTimeToString(), '\nOra fine:', lessons_dictionary[i][2].getLessonTimeToString() + '\n')    
            message += 'Corso: ' + lessons_dictionary[i][0] + '\nOra inizio:' + lessons_dictionary[i][1].getLessonTimeToString() + "\nOra fine:" + lessons_dictionary[i][2].getLessonTimeToString() + '\n'
            i+=1
    return message