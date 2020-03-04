import smtplib
from email import *
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import textwrap
import os

def mail(SUBJECT: object, msg: object) -> object:
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login("courriel.pmu@gmail.com", "devenir_millionaire")

	message = textwrap.dedent("""\
	From: %s
	To: %s
	Subject: %s
	%s
	""" % ("courriel.pmu@gmail.com", ", ", SUBJECT, msg))

	server.sendmail("courriel.pmu@gmail.com", "arnaud.jegoux@gmail.com", message)
	server.quit()



def mail2 (SUBJECT,file):
	sender = 'courriel.pmu@gmail.com'
	COMMASPACE = ', '
	recipients=COMMASPACE.join(["arnaud.jegoux@gmail.com", "arnaud.jegoux@gmail.com"])
	

	outer = MIMEMultipart()
	outer['Subject'] = SUBJECT
	outer['To'] = recipients
	outer['From'] = sender

	attachments = ['../05 - Documents/'+file]

	# Add the attachments to the message
	for file in attachments:
	
		with open(file, 'rb') as fp:
			msg = MIMEBase('application', "octet-stream")
			msg.set_payload(fp.read())

		encoders.encode_base64(msg)
		msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file) )
		outer.attach(msg)

	composed = outer.as_string()


	smtp = smtplib.SMTP('smtp.gmail.com', 587)
	smtp.starttls()
	smtp.login("courriel.pmu@gmail.com", "devenir_millionaire")

	smtp.sendmail(sender,recipients,composed)
	smtp.quit()


