# Script that sends email w/ attachments from a gmail account.

import email, smtplib, ssl, getpass

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

port = 465 # for SSL
subject = input("Email subject: ")
sender_email = input("Enter your email: ")
reciever_email = input("Enter reciever email: ")
body = input("Enter email body: ")
password = getpass.getpass(prompt="Password: ", stream=None) #IDLE has issue, still shows input. Use terminal!


# Create multipart message and set headers
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = reciever_email
message["Subject"] = subject

# Add body to email
message.attach(MIMEText(body, "plain"))

filename = input("Enter exact document name \
                 (make sure it's in the same directory as this script!):")

# Open file in binary mode
with open(filename, "rb") as attachment:
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())

# Encode file in ASCII to send via email
encoders.encode_base64(part)

# Add header as key/value pair
part.add_header(
    "Content-Disposition",
    f"attachment; filename={filename}",
    )

# add attachment to message and convert to string
message.attach(part)
text = message.as_string()

# Create a secure connection
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, reciever_email, text)
    
    
