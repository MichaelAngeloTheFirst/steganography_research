import smtplib
import ssl
import os
from dotenv import load_dotenv

load_dotenv()

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = os.getenv("SENDER_EMAIL")  # Enter your address
receiver_email = os.getenv("RECIPIENT_EMAIL")  # Enter receiver address
password = os.getenv("APP_PASSWD")  # input("Type your password and press enter: ")
message = """\
Subject: Hi there

This message is sent from Python."""

context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)
