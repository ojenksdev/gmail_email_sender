# Script that sends plain text emails w/ or without attachments from a gmail account.

import sys, email, smtplib, ssl, getpass

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

port = 465 # for SSL
subject = input("Email subject: ")
sender_email = input("Enter your email address: ")
reciever_email = input("Enter reciever email address: ")
body = input("Enter email body: ")
password = getpass.getpass(prompt="Password: ", stream=None) #IDLE has issue, still shows input. Use terminal!


# Create multipart message and set headers
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = reciever_email
message["Subject"] = subject

# Add body to email
message.attach(MIMEText(body, "plain"))

prompt = "\n\n********INSTRUCTIONS FOR SENDING********"
prompt += "\nEnter exact filename w/ file extension (ie: example.jpg)."
prompt += "\nMake sure it's located in the same directory as the script!"
prompt += "\nLeave blank to send without attachment."
prompt += "\n\nEnter File: "

filename = input(prompt)

try:
    if filename:
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
        print("file attached!")
    else:
        text = body
        print("No filename provided....sending email")                
except FileNotFoundError:
    print("Sorry, I can't find the file. Please check the directory.")
    send_em_prompt = "\nWould you like to send the email without the file?"
    send_em_prompt += "\n\nType Y to continue or N to quit\n"
    keep_running = input(send_em_prompt)
    if keep_running.upper() == 'Y':
        print("Trying to send email without attachment....")
    else:
        print('Please make sure the file is in the proper location.')
        sys.exit()
        
try: 
    # Create a secure connection
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, reciever_email, text)

    print("Email sent!")
except Exception as e:
    print("Sorry, We were unable to connect. \nCheck your password and/or Internet connection." +
          "\nCheck the error.txt file for more information.")
    with open('error.txt', 'w') as f_obj:
        f_obj.write(str(e))
