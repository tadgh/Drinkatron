import smtplib


username = "Drinkatron@gmail.com"
class email:
    def __init__(self):
        self.session = smtplib.SMTP('smtp.gmail.com', 587)
        self.session.ehlo()
        self.session.starttls()
        self.session.login(username, "temptesting")

    def send_email(self, subject, message, recipient_list):
        headers = "\r\n".join(["from: " + username,
                               "subject: " + subject,
                               "to: " + recipient_list,
                               "mime-version: 1.0",
                               "content-type: text/html"])

        content = headers + "\r\n\r\n" + message
        self.session.sendmail(username, recipient_list, content)





