import smtplib
import webbrowser
import imaplib
import email
import time
import speech_recognition as sr
import pyttsx3

def email_automation():
    recognizer = sr.Recognizer()
    speaker = pyttsx3.init()
    speaker.say("Welcome to this Email automation system.")
    speaker.say("I am here to help you to send,read, or check your messages!")
    speaker.runAndWait()
    def listen_microphone():
        with sr.Microphone() as source:
            print("Listening...")
            speaker.say("Listening...")
            speaker.runAndWait()
            audio = recognizer.listen(source)

        try:
            print("Recognizing...")
            speaker.say("Recognizing...")
            speaker.runAndWait()
            text = recognizer.recognize_google(audio)
            return text.lower()
        except sr.UnknownValueError:
            speaker.say("Sorry, I couldn't understand.")
        except sr.RequestError:
            speaker.say("Sorry, I'm unable to access the speech recognition service.")

        return ""


    def send_email(sender_email, sender_password, recipient_email, subject, message):
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender_email, sender_password)

            msg = f"Subject: {subject}\n\n{message}"
            smtp.sendmail(sender_email, recipient_email, msg)

    def read_emails(email_address, password, num_emails):
        with imaplib.IMAP4_SSL("imap.gmail.com", 993) as imap:
            imap.login(email_address, password)
            imap.select("INBOX")

            _, data = imap.search(None, "UNSEEN")
            email_ids = data[0].split()

            emails = []
            for email_id in email_ids[:num_emails]:
                _, data = imap.fetch(email_id, "(RFC822)")
                raw_email = data[0][1]
                email_message = email.message_from_bytes(raw_email)
                emails.append(email_message)

            return emails

    def extract_information(email_message):
        subject = email_message["Subject"]
        sender = email.utils.parseaddr(email_message["From"])[1]
        date = email_message["Date"]

        return subject, sender, date

    sender_email = "iamrion.rk@gmail.com"
    sender_password = "qpxfebewpswkhfir"
    email_address = "iamrion.rk@gmail.com"
    password = "qpxfebewpswkhfir"

    while True:
        command = listen_microphone()
 

        if "send a mail" in command:
            print("Please provide the recipient's email address:")
            speaker.say("Please provide the recipient's email address:")
            speaker.runAndWait()
            recipient_email = input()  # Manual text input for recipient's email address
            print("Please write the mail:")
            speaker.say("Please write the mail:")
            speaker.runAndWait()
            message = input()
            send_email(sender_email, sender_password, recipient_email, "Subject", message)
            print("Email sent successfully.")
            speaker.say("Email sent successfully.")
            speaker.runAndWait()
            
        elif "check my mail" in command:
            num_emails = 5  # Set the desired number of new emails to retrieve
            emails = read_emails(email_address, password, num_emails)
            print(f"You have {len(emails)} new emails.")
            speaker.say(f"You have {len(emails)} new emails.")
            speaker.runAndWait()

            print("Do you want to show the new messages? (yes/no): ")
            response = input("Do you want to show the new messages? (yes/no): ")
            
            if response.lower() == "yes":
                for email_message in emails:
                    subject, sender, date = extract_information(email_message)
                    print(f"Subject: {subject}")
                    print(f"From: {sender}")
                    print(f"Date: {date}")
                    
        elif "open mailbox" in command:
            webbrowser.open("https://mail.google.com/")

        elif "exit" in command:
            break

if __name__ == "__main__":
     
     email_automation()
