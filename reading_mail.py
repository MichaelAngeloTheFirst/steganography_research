import imaplib
import email
from email.header import decode_header
from dotenv import load_dotenv
import os 
from zwc_freq.message_finding import extract_secret_from_carrier
import pandas as pd
# from zwc_freq.message_hiding import extract_secret_from_carrier

load_dotenv()

# === Configuration ===
EMAIL = os.getenv('RECIPIENT_EMAIL')
PASSWORD = os.getenv('RECIPIENT_APP_PASSWD')
IMAP_SERVER = os.getenv('IMAP_SERVER')  # e.g., "imap.gmail.com" for Gmail
SEARCH_SUBJECT = "[EXT] Stego Mail"

# === Connect to the mail server ===
mail = imaplib.IMAP4_SSL(IMAP_SERVER)
mail.login(EMAIL, PASSWORD)
mail.select("inbox")  # or another folder like "INBOX"

# === Search for emails with subject ===
status, messages = mail.search(None, '(SUBJECT "{}")'.format(SEARCH_SUBJECT))

email_ids = messages[0].split()
if not email_ids:
    print("No emails found with that subject.")
else:
    latest_email_id = email_ids[-1]  # Get the newest one (last in list)

    # Fetch the email by ID
    status, msg_data = mail.fetch(latest_email_id, "(RFC822)")
    raw_email = msg_data[0][1]

    # Parse the email content
    msg = email.message_from_bytes(raw_email)
    subject, encoding = decode_header(msg["Subject"])[0]
    if isinstance(subject, bytes):
        subject = subject.decode(encoding if encoding else "utf-8")

    from_ = msg.get("From")
    date_ = msg.get("Date")

    print(f"From: {from_}")
    print(f"Subject: {subject}")
    print(f"Date: {date_}")

    # Extract email body
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain" and "attachment" not in part.get("Content-Disposition", ""):
                body = part.get_payload(decode=True).decode()
                print(f"Body:\n{body}")
                break
    else:
        body = msg.get_payload(decode=True).decode()
        print(f"Body:\n{body}")

    # Extract hidden message using unique_array
    # unique_array_df = pd.read_csv("zwc_freq/unique_array.csv")
    # unique_array = unique_array_df.values.tolist()
    # # Ensure unique_array is 26x8 and all values are single characters
    # unique_array = [row[:8] for row in unique_array[:26]]
    hidden_message = extract_secret_from_carrier(body,"zwc_freq/unique_array.csv")
    print(f"Hidden message: {hidden_message}")

mail.logout()
