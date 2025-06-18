from dotenv import load_dotenv
from app.modules.zwc_freq.message_hiding import hide_secret_in_carrier
from app.modules.aitsteg.aitsteg_functions import embed_secret
from email.mime.text import MIMEText
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import smtplib
import ssl
import os

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

def embed_pass_in_subject(passwd, subject):
    stego_subject = embed_secret(passwd,subject)
    return stego_subject

def send_email(subject, body):
    #--------email data--------
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = os.getenv("SENDER_EMAIL")  # Enter your address
    receiver_email = os.getenv("RECIPIENT_EMAIL")  # Enter receiver address
    password = os.getenv("APP_PASSWD")

    #--------message creation
    body_plain = f"Hello,\nThis message is sent from Python.\n{body}"
    message = MIMEText(body_plain, "plain")
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
    except Exception as e:
        print(f"Error sending stego email: {e}")


class StegoMailRequest(BaseModel):
    passwd: str
    secret_message: str
    carrier_message: str
    subject: str = "Stego Mail"
    


@router.post("/send_stego_mail/")
def send_stego_mail(request: StegoMailRequest):
    
    try:
        stego_message = create_stego_message(
            request.secret_message, request.carrier_message
        )
        stego_subject = embed_pass_in_subject(request.passwd, request.subject)
        send_email(
            stego_subject,
            stego_message,
        )
        return {"status": "success", "message": "Stego email sent successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
