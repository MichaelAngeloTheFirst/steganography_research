import smtplib
import ssl
import os
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

zw_joiner = "\u200d"
hidden_message = f"Hello World Hidden ZWC here ->{zw_joiner}<-Text"

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
message.add_header('X-Custom-Header', 'CustomHeaderValue')  # Custom header example

# Email body with hidden content (plain and HTML)
body_plain = f"Hello,\nThis message is sent from Python.\n{hidden_message}"
body_html = f"""
<html>
  <body>
    <p>Hello,<br>
       This message is sent from <b>Python</b>.<br>
       <span style='display:none'>{hidden_message}</span>
    </p>
  </body>
</html>
"""
message.attach(MIMEText(body_plain, "plain"))
message.attach(MIMEText(body_html, "html"))

# Send email
context = ssl.create_default_context()
try:
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        to_addrs = [receiver_email]
        server.sendmail(sender_email, to_addrs, message.as_string())
    print("Email sent successfully.")
except Exception as e:
    print(f"Error sending email: {e}")
