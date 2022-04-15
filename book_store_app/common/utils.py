from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

import os

password = os.getenv("password")
my_email = os.getenv("my_email")


def send_mail(email, message):
    msg = MIMEMultipart()

    passwrd = password
    msg['From'] = my_email
    msg['To'] = email
    msg['Subject'] = "Click on the link"

    msg.attach(MIMEText(message, 'html'))

    server = smtplib.SMTP('smtp.gmail.com: 587')

    server.starttls()

    server.login(msg['From'], passwrd)

    server.sendmail(msg['From'], msg['To'], msg.as_string())

    server.quit()
