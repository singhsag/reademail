import email
import imaplib
from pprint import pprint

from urlextract import URLExtract

EMAIL_ACCOUNT = "gradeyoursite@gmail.com"
PASSWORD = ''

mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(EMAIL_ACCOUNT, PASSWORD)
mail.list()
mail.select("INBOX")
result, data = mail.uid("search", '(FROM "info@paid-to-read-email.com")', "UNSEEN")  # (ALL/UNSEEN)
i = len(data[0].split())

arrayList = []

for x in range(i):
    latest_email_uid = data[0].split()[x]
    result, email_data = mail.uid('fetch', latest_email_uid, '(RFC822)')
    raw_email = email_data[0][1]
    raw_email_string = raw_email.decode('utf-8')
    email_message = email.message_from_string(raw_email_string)
    email_from = str(email.header.make_header(email.header.decode_header(email_message['From'])))
    email_to = str(email.header.make_header(email.header.decode_header(email_message['To'])))
    subject = str(email.header.make_header(email.header.decode_header(email_message['Subject'])))

    for part in email_message.walk():
        body = part.get_payload(decode=True)
        body_str = str(body)

        if "paid-to-read-email.com/" in body_str:
            new_body_str = body_str.replace('\\n', ' $ ')
            final_body_str = new_body_str.replace('\\r', ' $ ')
            extractor = URLExtract()
            urls = extractor.find_urls(final_body_str)
            for url in urls:
                if (url.startswith("https://www.paid-to-read-email.com/open")
                    and not (url.endswith("amp") or (url.endswith("trkopen=1")))) \
                        or (url.startswith("https://www.paid-to-read-email.com/mail")
                            and not (url.endswith("amp") or (url.endswith("trkopen=1")))):
                    if url in arrayList:
                        continue
                    else:
                        arrayList.append(url)
                        break


def get_urls_list():
    pprint(arrayList)
    print('Total number of links - ', len(arrayList))
    return arrayList


# get_urls_list()
