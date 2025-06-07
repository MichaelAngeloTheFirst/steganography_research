from fastapi import APIRouter, HTTPException
import os
from dotenv import load_dotenv
import imaplib
import email
from email.header import decode_header
import pandas as pd
from app.modules.zwc_freq.message_finding import extract_secret_from_carrier
from dateutil import parser as date_parser
import pytz

router = APIRouter()
load_dotenv()


@router.get("/read_latest_stego_mail/")
def read_latest_stego_mail():
    EMAIL = os.getenv('RECIPIENT_EMAIL')
    PASSWORD = os.getenv('RECIPIENT_APP_PASSWD')
    IMAP_SERVER = os.getenv('IMAP_SERVER')
    SEARCH_SUBJECT = "[EXT] Stego Mail"
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL, PASSWORD)
        mail.select("inbox")
        status, messages = mail.search(None, f'(SUBJECT "{SEARCH_SUBJECT}")')
        email_ids = messages[0].split()
        if not email_ids:
            mail.logout()
            raise HTTPException(status_code=404, detail="No emails found with that subject.")
        latest_email_id = email_ids[-1]
        status, msg_data = mail.fetch(latest_email_id, "(RFC822)")
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)
        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding if encoding else "utf-8")
        from_ = msg.get("From")
        date_ = msg.get("Date")
        # Convert date_ to Europe/Warsaw timezone (Central European Time/Central European Summer Time)
        try:
            dt_utc = date_parser.parse(date_)
            if dt_utc.tzinfo is None:
                dt_utc = pytz.utc.localize(dt_utc)
            dt_cet = dt_utc.astimezone(pytz.timezone("Europe/Warsaw"))
            date_cet = dt_cet.strftime("%Y-%m-%d %H:%M:%S %Z")
        except Exception:
            date_cet = date_
        # Extract email body
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
        mail.logout()
        hidden_message = extract_secret_from_carrier(body, './modules/zwc_freq/unique_array.csv')
        return {
            "from": from_,
            "subject": subject,
            "date": date_cet,
            "body": body,
            "hidden_message": hidden_message
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))