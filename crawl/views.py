from django.shortcuts import render
from django.http import HttpResponse
from django.db import IntegrityError
from datetime import time
import time
from django.db.models import Count
#   

#importing files from main project
from bs4 import BeautifulSoup
import re, requests, hashlib, os
from django.shortcuts import render

#for crawler
import os
from urllib.request import urlretrieve
import uuid
import requests
import googlesearch
from urllib.parse import urljoin, unquote
from bs4 import BeautifulSoup

import os
from urllib.parse import urlparse
import smtplib
#Connection with the Database
# import mysql.connector
 
from .models import Publisher
import urllib


#mailscript libraries
import email, smtplib, ssl
import os
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import glob




# output_dir = os.chdir(r"C:\scraping output")
#output_dir = os.chdir(r"C:\Users\amanm\PycharmProjects\My_Web_Crwaler\crawler\crawler")
MBFACTOR = float(1 << 20) #for converting byted to Megabytes


try:
    from googlesearch import search
except ImportError:
    print("No module named 'google' found")


#list of websites to crawl
l2 = ['portalebandi.regione.basilicata.it', 'http://www.unioncamerelombardia.it', 'http://www.sistema.puglia.it',
      'http://moliseineuropa.regione.molise.it']
all_links = []


# Creating views here.
def home(request):
    return render(request,'home.html')


def initiate(request):
    return render(request,'result.html')


def crawl(request):
    for site in l2:
        urlStr = 'site:' + site + '%20' + 'filetype:pdf' #search string for google search
        for j in search(urlStr, num_results=4):
            print(j)
            all_links.append(j) #appending all the pdf url to list
        for u in all_links:
            response = requests.get(u) #fetching each the url from the list
            if response.status_code == 200: #checking if the url is responsive and available
                a = urlparse(u)
                print('The path name is:\n',a.path) #parsing the path of the url
                fl=os.path.basename(a.path) #parsing the filename from the url
                print('The extracted Filename is:\n',fl)
                file_size=response.headers.get('content-length', 0)
                content_type=response.headers.get('Content-Type', 0)
                last_modified=response.headers.get('Last-Modified', 0)
                expiry_date=response.headers.get('Expires', 0)
                cache_control=response.headers.get('Cache', 0)
                server=response.headers.get('Server', 0)

                pub_instance = Publisher.objects.create(name=fl,links=u,file_size=file_size,content_type=content_type,last_modified_y=last_modified,expiry_date_y=expiry_date,cache_control_y=cache_control,server_y=server) #creating the entry in the database
                pub_instance.save() #saving the info for each url to database

                for row in Publisher.objects.all().reverse(): #removing all the duplicate items from the database
                    if Publisher.objects.filter(name=row.name).count() > 1: #using name as a filter
                        row.delete()
    return render(request, 'result.html', {'list':all_links})
    # except Exception as exc:
    #     pass
    #     return render(request, 'result.html', {'list':all_links}) #redirecting to the results template page



def email_pdf(request):
    my_path = os.getcwd()
    subject = "An email with attachment from Python"
    body = "These are the links that are shared for your convinience."
    sender_email = 'aman.mishra1496@gmail.com'
    receiver_email = 'aman777444@gmail.com'
    password = 'amanelvisbella'

    # Create a multipart message and set header
    message = MIMEMultipart('alternative')
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    # message["Bcc"] = receiver_email  # Recommended for mass emails


    extracted_links=[]#empty list to store all the extracted links from the database

    for link in Publisher.objects.values_list('links'):
        print('The links are:\n',link)
        extracted_links.append('<li><a href='+link[0]+">"+link[0]+"</a></li>") #appending all the links to a list

    #temp=" "
    html = """\
            <html>
            <body>
                <p>Good Morning,<br>
                I hope you are well. These are the links which have been generated for your convinience.<br></p><br>
                <ul>"""+''.join(extracted_links)+"""</ul><br><p>Regards,<br>Aman Mishra</p>
            </body>
            </html>
            """


    message.attach(MIMEText(html, "html"))

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email,message.as_string()) #text

    return render(request, 'email_result.html')



#CODE FOR HEROKU DEPLOYMENT OF DJANGO APPLICATION










 #UNUSED CODE BLOCKS FOR LATER USE  
 # 
 # 
 #  # with open(fl + '.pdf', 'wb') as f: #writing the file to the direrctory for record
    #     f.write(response.content) 
    #message = MIMEMultipart("alternative", None, [MIMEText(text), MIMEText(html,'html')])
    # filename = [f for f in glob.glob("*.pdf")]

    # for i in filename:
    #     # Open PDF file in binary mode
    #     with open(i, "rb") as attachment:
    #         # Add file as application/octet-stream
    #         # Email client can usually download this automatically as attachment
    #         part = MIMEBase("application", "octet-stream")
    #         part.set_payload(attachment.read())

    #     # Encode file in ASCII characters to send by email
    #     encoders.encode_base64(part)

    #     # Add header as key/value pair to attachment part
    #     part.add_header(
    #         "Content-Disposition",
    #         f"attachment; filename= {i}",
    #     )

    #     # Add attachment to message and convert message to string
    #     message.attach(part)
    #     text = message.as_string()

    # Log in to server using secure context and send email