import os
from dotenv import load_dotenv
from app.modules.zwc_freq.message_hiding import hide_secret_in_carrier
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import ssl
import pandas as pd
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

load_dotenv()
def load_messages(secret_path, carrier_path):
    with open(secret_path, "r") as f:
        secret_message = f.read().strip()
    with open(carrier_path, "r") as f:
        carrier_message = f.read().strip()
    return secret_message, carrier_message


def create_stego_message(secret_message, carrier_message, file_path= './modules/zwc_freq/unique_array.csv'):
    stego_message = hide_secret_in_carrier(secret_message, carrier_message,file_path)
    if stego_message is None:
        raise ValueError("Could not hide the secret message in the carrier message.")
    return stego_message


def send_email(subject, body):
    #--------email data--------
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = os.getenv("SENDER_EMAIL")  # Enter your address
    receiver_email = os.getenv("RECIPIENT_EMAIL")  # Enter receiver address
    password = os.getenv("APP_PASSWD")

    #--------message creation
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    body_plain = f"Hello,\nThis message is sent from Python.\n{body}"
    body_html = f"""
    <html>
    <body>
        <p>Hello,<br>
        This message is sent from <b>Python</b>.<br>
        <span style='display:none'>{body}</span>
        </p>
    </body>
    </html>
    """
    
    

    message.attach(MIMEText(body_plain, "plain"))
    message.attach(MIMEText(body_html, "html"))
    
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("Stego email sent successfully.")
    except Exception as e:
        print(f"Error sending stego email: {e}")


class StegoMailRequest(BaseModel):
    secret_message: str
    carrier_message: str
    subject: str = "Stego Mail"


@router.post("/send_stego_mail/")
def send_stego_mail(request: StegoMailRequest):
    
    try:
        stego_message = create_stego_message(
            request.secret_message, request.carrier_message
        )
        send_email(
            request.subject,
            stego_message,
        )
        return {"status": "success", "message": "Stego email sent successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
