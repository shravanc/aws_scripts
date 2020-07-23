import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


class Mailer:
    def __init__(self, config):
        self.fromaddr = config.fromaddr #'no.place.like.co@gmail.com'
        self.toaddr = config.toaddr #'shravan007.c@gmail.com'
        self.msg = MIMEMultipart()
        self.msg['From'] = self.fromaddr
        self.msg['To'] = self.toaddr
        self.msg['Subject'] = 'Testing Attachment'
        self.body = 'Sample Body'

        self.filename = config.log_file.split('/')[-1]
        self.filepath = config.log_file

        attachment = open(self.filepath, 'rb')

        self.p = MIMEBase('application', 'octet-stream')
        self.p.set_payload((attachment).read())
        encoders.encode_base64(self.p)

        self.p.add_header('Content-Disposition', f"attachment; filename= {self.filename.split('/')[-1]}")

        self.msg.attach(self.p)

        self.s = smtplib.SMTP('smtp.gmail.com', 587)

        self.s.starttls()
        self.s.login(self.fromaddr, config.password)

        self.text = self.msg.as_string()


    def deliver(self):
        self.s.sendmail(self.fromaddr, self.toaddr, self.text)
        self.s.quit()

