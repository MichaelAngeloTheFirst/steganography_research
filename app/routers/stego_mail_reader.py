import base64
from re import sub
from fastapi import APIRouter, HTTPException
import os
from dotenv import load_dotenv
import imaplib
import email
from email.header import decode_header
import pandas as pd
from app.modules.zwc_freq.message_finding import extract_secret_from_carrier, print_visible_zwc
from app.modules.aitsteg.aitsteg_functions import extract_secret
from dateutil import parser as date_parser
from pydantic import BaseModel
import pytz

router = APIRouter()
load_dotenv()

class StegoMailRequest(BaseModel):
    passwd: str

class StegoMailResponse(BaseModel):
    from_: str
    subject: str
    date: str
    body: str
    hidden_message: str


@router.post("/read_latest_stego_mail/")
def read_latest_stego_mail(request: StegoMailRequest):
    EMAIL = os.getenv('RECIPIENT_EMAIL')
    PASSWORD = os.getenv('RECIPIENT_APP_PASSWD')
    IMAP_SERVER = os.getenv('IMAP_SERVER')
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL, PASSWORD)
        mail.select("inbox")
        _, messages = mail.search(None, 'ALL')
        email_ids = messages[0].split()
        if not email_ids:
            mail.logout()
            raise HTTPException(status_code=404, detail="No emails found in inbox.")
        for eid in list(reversed(email_ids))[:5]:
            _, msg_data = mail.fetch(eid, "(RFC822)")
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)
            subject_header = msg["Subject"]
            if subject_header is None:
                continue  # skip emails with no subject
            subject_parts = decode_header(subject_header)
            subject = ''
            for part, enc in subject_parts:
                if isinstance(part, bytes):
                    try:
                        subject += part.decode(enc or 'utf-8', errors='replace')
                    except Exception:
                        subject += part.decode('utf-8', errors='replace')
                else:
                    subject += part
            # Check the secret
            if request.passwd == extract_secret(subject):
                from_ = msg.get("From")
                date_ = msg.get("Date")
                try:
                    dt_utc = date_parser.parse(date_)
                    if dt_utc.tzinfo is None:
                        dt_utc = pytz.utc.localize(dt_utc)
                    dt_cet = dt_utc.astimezone(pytz.timezone("Europe/Warsaw"))
                    date_cet = dt_cet.strftime("%Y-%m-%d %H:%M:%S %Z")
                except Exception:
                    date_cet = date_
                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        if content_type == "text/plain" and "attachment" not in part.get("Content-Disposition", ""):
                            body = part.get_payload(decode=True).decode(errors="ignore")
                            break
                    else:
                        body = ""
                else:
                    body = msg.get_payload(decode=True).decode(errors="ignore")
                unique_array_header = msg.get("X-Unique-Array", None)
                decoded_csv = None
                if unique_array_header:
                    print("X-Unique-Array header data (base64):")
                    print(unique_array_header)
                    
                    try:
                        decoded_csv = base64.b64decode(unique_array_header).decode('utf-8')
                        print("Decoded X-Unique-Array header data (CSV):")
                        print(decoded_csv)
                        from io import StringIO
                        df = pd.read_csv(StringIO(decoded_csv))
                        print("DataFrame from decoded_csv:")
                        print(df)
                        mail.logout()
                        hidden_message = extract_secret_from_carrier(stego=body,collected_data=df )
                        print_visible_zwc(subject)
                        print_visible_zwc(body)
                        response = StegoMailResponse(
                            from_=from_,
                            subject=subject,
                            date=date_cet,
                            body=body,
                            hidden_message=hidden_message
                        )
                        return response
                        
                    except Exception as e:
                        print(f"Error decoding X-Unique-Array header: {e}")
                else:
                    mail.logout()
                    hidden_message = extract_secret_from_carrier(body, './modules/zwc_freq/unique_array.csv')
                    print_visible_zwc(subject)
                    print_visible_zwc(body)
                    response = StegoMailResponse(
                        from_=from_,
                        subject=subject,
                        date=date_cet,
                        body=body,
                        hidden_message=hidden_message
                    )
                    return response
        mail.logout()
        return StegoMailResponse(
            from_="",
            subject="",
            date="",
            body="",
            hidden_message="No available data."
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))