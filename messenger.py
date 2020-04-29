import smtplib
from email.message import EmailMessage
from string import Template
from pathlib import Path


# forwards messages to email
def forward_message(data):
    html = Template(Path('auto_email.html').read_text())
    msg = EmailMessage()
    msg['from'] = 'Vaida\'s Web'
    msg['to'] = 'vaida.dryzaite@gmail.com'
    msg['subject'] = 'UHU! New message on Web!'
    msg.set_content(html.substitute(data), 'html')
    with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login('dryzaitev@gmail.com', '0v7ojWv8cShq')
        smtp.send_message(msg)
        print('yo, python master, message forwarded!')