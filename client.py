from email.message import EmailMessage
import smtplib
import os
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

sender = "smtpdevelop@outlook.com"
recipient = "smtpdevelop@outlook.com"
message = "Hello world!"

email = EmailMessage()
email["From"] = sender
email["To"] = recipient
email["Subject"] = "Test Email"
email.set_content(message)

smtp = smtplib.SMTP("smtp-mail.outlook.com", port=587)
smtp.starttls()
smtp.login(sender, str(os.getenv("OUTLOOK_PASSWORD")))
smtp.sendmail(sender, recipient, email.as_string())
smtp.quit()

