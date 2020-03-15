# Python code to illustrate Sending mail from  
# your Gmail account  
import smtplib 
from email.mime.multipart import *
from email.mime import *
from email.mime.base import *
from email.mime.text import *
from email import encoders
import pickle

id_num = 0
datadict = {}

email_list =   [
		'gideonmitchell01@gmail.com',
		#'stockman1221@gmail.com',
		#'agoolsb@ucls.uchicago.edu',
		#'elight@ucls.uchicago.edu',
		#'steven@shermancapitalgroup.com',
		#'nedwards@ucls.uchicago.edu',
		#'heidismitchell@gmail.com',
		#'cjd.mitchell@gmail.com'
		]

# INFO BY COUNTRY

with open('data.pickle', 'rb') as handle:
    datadict = pickle.load(handle)
# creates SMTP session 
s = smtplib.SMTP('smtp.gmail.com', 587) 

# start TLS for security 
s.starttls() 

# Authentication 
s.login("coronavirusupdates726@gmail.com", "Bobisbest4401") 

# message to be sent 
msg = MIMEMultipart()
msg['From'] = 'coronavirusupdates726@gmail.com'
msg['To'] = 'gideonmitchell01@gmail.com'
msg['Subject'] = 'Coronavirus Update'

def attacth_image(filename: str, msg):
    global id_num
    with open(filename, 'rb') as f:
        mime = MIMEBase('image', 'png', filename=f'{id_num}.png')

        mime.add_header('Content-Disposition', 'attachment', filename=f'{id_num}.png')
        mime.add_header('X-Attachment-Id', str(id_num))
        mime.add_header('Content-ID', f'<{id_num}>')

        mime.set_payload(f.read())
        encoders.encode_base64(mime)

        msg.attach(mime)

    id_num += 1

attacth_image('infected.png', msg)
attacth_image('killed.png', msg)
attacth_image('recovered.png', msg)
attacth_image('US_cases.png', msg)


country_str = ''
for i,key in enumerate(list(datadict['Countries'].keys())):
    country_str += f'<p> {key}: {datadict["Countries"][key]} </p>' 

HTML_body = f"""
<html>
    <body>
        <h2>Current Patients Infected: {datadict["Infected"]}</h2>
        <h2>Total Patients Killed: {datadict["Deaths"]}</h2>
        <h2>Total Patients Recovered: {datadict["Recovered"]}</h2>

            <br>
        <p>{datadict["info1"]}</p>
        <p>{datadict["info2"]}</p>
        <p>{datadict["info3"]}</p>
            <br>
        <p><img src="cid:0"></p>
        <p><img src="cid:1"></p>
        <p><img src="cid:2"></p>
	<p><img src="cid:3"></p>

        <br>
        <h2>Infections By Country: </h2>
        {country_str}

	<br>
	<p>
		<small>
			All information is taken from CSSE at Johns Hopkins Universtiy and can be found at 
			<a>https://github.com/CSSEGISandData/COVID-19</a>
		</small>
	</p>
    </body>
</html>
"""


msg.attach(MIMEText(HTML_body, 'html', 'utf-8'))


# sending the mail 
for email in email_list:
	s.sendmail("coronavirusupdates726@gmail.com", email, msg.as_string()) 
  
# terminating the session 
s.quit()
