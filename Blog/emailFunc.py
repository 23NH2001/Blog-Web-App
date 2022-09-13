# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.message import EmailMessage

# Open the plain text file whose name is in textfile for reading.
def SendEmail(fname,lname,user_email,query):
    
    msg = EmailMessage()
    msg.set_content(query)

    # me == the sender's email address
    # you == the recipient's email address
    msg['Subject'] = f'Message from {fname} {lname}'
    msg['From'] = 'hinguneveelW@gmail.com'
    msg['To'] = you

    # Send the message via our own SMTP server.
    s = smtplib.SMTP('localhost')
    s.send_message(msg)
    s.quit()