import os, smtplib
from PIL import Image
from dotenv import load_dotenv
from email.message import EmailMessage

load_dotenv()
password = os.getenv("MY_GMAIL_PASSWORD")
sender = os.getenv("SENDER_MAIL")
receiver = os.getenv("RECEIVER_MAIL")

def send_email(image_path):
    print("Send email function started")

    email_message = EmailMessage()
    email_message["Subject"] = "Object Detected!"
    email_message.set_content("Hey, someone is detected in this area!")

    with open(image_path, "rb") as file:
        content = file.read()
    img = Image.open(image_path)
    email_message.add_attachment(content, maintype="image", subtype=img.format.lower())

    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(user=sender, password=password)
    gmail.sendmail(from_addr=sender, to_addrs=receiver, msg=email_message.as_string())
    gmail.quit()

    print("Send email function ended")

if __name__=="__main__":
    send_email(image_path="steps.png")