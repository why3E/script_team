# oluh mknb mkqp xdoo

import mimetypes
import mysmtplib
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from xmlRead import xmlRead

fetcher = xmlRead()

host = "smtp.gmail.com"
port = "587"
htmlFileName = "logo.html"

senderAddr = "s159753s@tukorea.ac.kr"
recipientAddr = "s159753s@tukorea.ac.kr"


class msg:
    def __init__(self, subject):
        self.msg = MIMEBase("multipart", "alternative")
        self.msg['Subject'] = subject
        self.msg['From'] = senderAddr
        self.msg['To'] = recipientAddr

    def attach_show_details(self, title, msgtext, img_url):
        html = f"""
        <html>
        <body>
        <h1>{title}</h1>
        <hr>
        <div style="display: flex; align-items: center; margin-bottom: 20px;">
            <p style="margin: 0;">{msgtext}</p>
            <img src="{img_url}" alt="이미지" style="margin-left: 25px; width: 200px; height: auto;" />
        </div>
        </body>
        </html>
        """
        self.msg.attach(MIMEText(html, 'html'))

    def attach_place_details(self, title, msgtext):
        html = f"""
        <html>
        <body>
        <h1>{title}</h1>
        <hr>
        <div style="display: flex; align-items: center; margin-bottom: 20px;">
            <p style="margin: 0;">{msgtext}</p>
        </div>
        </body>
        </html>
        """
        self.msg.attach(MIMEText(html, 'html'))

    def send(self):
        s = mysmtplib.MySMTP(host, port)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login("s159753s@tukorea.ac.kr", "oluh mknb mkqp xdoo")
        s.sendmail(senderAddr, [recipientAddr], self.msg.as_string())
        s.close()
