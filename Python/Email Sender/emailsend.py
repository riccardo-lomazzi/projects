# Import smtplib for the actual sending function
import smtplib, re

# Import the email modules we'll need
from email.mime.text import MIMEText


def checkMailFormat(mail_address):
    #regex \A(\w+[\w.]+@gmail\.com)\Z - dall'inizio alla fine del testo, cerca tutto quello vuoi fino ad arrivare a @gmail.com, che deve apparire una volta sola
    result = re.findall(r'\A(\w+[\w.]+@gmail\.com)\Z', mail_address)
       
    if(len(result)==0):
        return False
    else:
        return True
    

mail_address = input('Google SMTP Credentials\nEnter Google Email Address: ')

while(checkMailFormat(mail_address) is False):
    mail_address = input('Invalid email address. Enter again: ')
   
    
    
password = input('Valid email. Enter Google password or app password: ')
#should test connection here
receiver = input("Write receiver's address: ")
subject = input('Write Subject: ')
mail_text = input('Write your email text: ')


# Create a text/plain message
msg = MIMEText(mail_text)


msg['Subject'] = subject
msg['From'] = mail_address
msg['To'] = receiver

# Send the message via our own SMTP server, but don't include the
# envelope header.
try:
    s = smtplib.SMTP('smtp.gmail.com', 587) #password: xuyzeilbbntemdzv
    s.ehlo()
    s.starttls()
    s.login(mail_address , password)
    s.sendmail(mail_address, receiver, msg.as_string())
    s.quit()
    print("Success!")
except SMTPException as e:
   print("Error: unable to send email. " + str(e))
