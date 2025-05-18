import smtplib
import ssl
import os
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

zw_joiner = "\u200d"
hidden_message = f"Hello World Hidden{zw_joiner}Text"

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = os.getenv("SENDER_EMAIL")  # Enter your address
receiver_email = os.getenv("RECIPIENT_EMAIL")  # Enter receiver address
password = os.getenv("APP_PASSWD")

# Construct the email
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = "Hi there"

# Email body with hidden content
body = f"Hello,\nThis message is sent from Python.\n{hidden_message}"
message.attach(MIMEText(body, "plain"))

# Send email
context = ssl.create_default_context()
try:
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
    print("Email sent successfully.")
except Exception as e:
    print(f"Error sending email: {e}")
