import polimi_parser, datetime, logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
 
 
def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Ciao! PoliTimeBot è qui per aiutarti a scoprire l'orario di un'aula! Ti basta scrivere \n\n 'orario *Aula* *data*' \n\n per scoprire l'orario per l'aula indicata, nel giorno d'interesse. Prova subito!")
 
def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Scusami, ma non ho capito la tua richiesta")
 
#Message Handler
def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)
 
#timetable handler
def timetable_service(bot, update):
    classroom = update.message.text.replace(".","").replace("/orario","").strip()
    pp_message = polimi_parser_request(classroom)
    bot.send_message(chat_id=update.message.chat_id, text=pp_message)
 
#sets up and starts the polimi_parser function
def polimi_parser_request(classroom):
    now = datetime.datetime.now()
    day = now.day
    month = now.month
    year = now.year
    
    date = now
    
    url = "https://www7.ceda.polimi.it/spazi/spazi/controller/OccupazioniGiornoEsatto.do?csic=MIA&categoria=tutte&tipologia=tutte&giorno_day=" + str(day) + "&giorno_month=" + str(month) + "&giorno_year=" + str(year) + "&jaf_giorno_date_format=dd%2FMM%2Fyyyy&evn_visualizza=Visualizza+occupazioni" 
    message = polimi_parser.main(url, classroom, date)
    return message
    
#/////////////////// MAIN //////////////////////    
#activate cmdprompt logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#add token to Telegram Updater
updater = Updater(token='#myapikey#') 
dispatcher = updater.dispatcher #activated dispatcher
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

#added timetable command
timetable_handler = CommandHandler('orario', timetable_service)
dispatcher.add_handler(timetable_handler)

#//////////Unknown handler/////////// <-- THIS MUST STAY HERE
unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

#start thread
updater.start_polling() 
updater.idle() #read Ctrl+C input