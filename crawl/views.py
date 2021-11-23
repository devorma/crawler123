from django.shortcuts import render
from django.http import HttpResponse
from django.db import IntegrityError
from datetime import time
import time
from django.db.models import Count
#   
import http.client
import json
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



MBFACTOR = float(1 << 20) #for converting byted to Megabytes


try:
    from googlesearch import search
except ImportError:
    print("No module named 'google' found")


#list of websites to crawl
l2 = ['portalebandi.regione.basilicata.it', 'http://www.unioncamerelombardia.it','http://www.sistema.puglia.it','http://moliseineuropa.regione.molise.it']
all_links = []


# Creating views here.
def home(request):
    return render(request,'home.html')


def initiate(request):
    return render(request,'result.html')


def crawl(request):
    try:
        for site in l2:
            urlStr = 'site:' + site + '%20' + 'filetype:pdf' #search string for google search
            for j in search(urlStr, num_results=1):
                all_links.append(j) #appending all the pdf url to list
            for u in all_links:
                print('The links are:\n',u)
                response = requests.get(u) #fetching each the url from the list
                #if response.status_code == 200: #checking if the url is responsive and available
                a = urlparse(u)
                fl=os.path.basename(a.path) #parsing the filename from the url
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
                        print('Found Duplicate item:\n',row.name)
                        row.delete()
            extracted_links=[]#empty list to store all the extracted links from the database

            for link in Publisher.objects.values_list('links'):
                    print('The final links are:\n',link)
                    extracted_links.append('<li><a href='+link[0]+">"+link[0]+"</a></li>") #appending all the links to a list

            url = os.environ['https://be.trustifi.com']+'/api/i/v1/email'
            conn = http.client.HTTPSConnection("be.trustifi.com")
            payload = json.dumps({"recipients": [{"email": "aman777444@gmail.com","name": "Aman Mishra","body":''.join(extracted_links)}]})
            headers = {'x-trustifi-key': 'fff4ae6104486fc20de26cb0501f4310c663f9c0cbc8bf49','x-trustifi-secret': '0f7c288aad8a9542f1c355b60b05e0f0','Content-Type': 'application/json'}
            conn_req=conn.request("POST", url, payload, headers)
            res = conn_req.getresponse()
            print('The response fromt the email is :\n',res)
            data = res.read()
            print('The data which is read is:\n',data)
            print(data.decode("utf-8"))
    except Exception as exc:
        pass
        return render(request, 'result.html', {'list':all_links}) #redirecting to the results template page



# def email_pdf(request):
#     subject = "An email with attachment from Python"
#     sender_email = 'aman.mishra1496@gmail.com'
#     receiver_email = 'aman777444@gmail.com'
#     password = 'amanelvisbella'

#     # Create a multipart message and set header
#     message = MIMEMultipart('alternative')
#     message["From"] = sender_email
#     message["To"] = receiver_email
#     message["Subject"] = subject
#     # message["Bcc"] = receiver_email  # Recommended for mass emails


#     extracted_links=[]#empty list to store all the extracted links from the database

#     for link in Publisher.objects.values_list('links'):
#         print('The links are:\n',link)
#         extracted_links.append('<li><a href='+link[0]+">"+link[0]+"</a></li>") #appending all the links to a list


    # html = """
    #         <html>
    #         <body>
    #             <p>Good Morning,<br>
    #             I hope you are well. These are the links which have been generated for your convinience.<br></p><br>
    #             <ul>"""+''.join(extracted_links)+"""</ul><br><p>Regards,<br>Aman Mishra</p>
    #         </body>
    #         </html>
    #         """


#     message.attach(MIMEText(html, "html"))

#     context = ssl.create_default_context()
#     with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
#         server.login(sender_email, password)
#         server.sendmail(sender_email, receiver_email,message.as_string()) #text

#     return render(request, 'email_result.html')

#2nd part
        # url = os.environ['https://be.trustifi.com']+'/api/i/v1/email'
        # extracted_links=[]#empty list to store all the extracted links from the database
        # for link in Publisher.objects.values_list('links'):
        #         print('The links are:\n',link)
        #         extracted_links.append('<li><a href='+link[0]+">"+link[0]+"</a></li>") #appending all the links to a list

        # postData ={
        #     "name": "my_template",
        #     "title": "Email Template",
        #     "html": " <body><p>Good Morning,<br>I hope you are well. These are the links which have been generated for your convinience.<br></p><br><ul>"+''.join(extracted_links)+"</ul><br><p>Regards,<br>Aman Mishra</p></body>"}

        # payload = {"{\"recipients\":[{\"email\":\"aman777444@gmail.com\"}]}",postData}
        # headers = {
        # 'x-trustifi-key': os.environ['fff4ae6104486fc20de26cb0501f4310c663f9c0cbc8bf49'],
        # 'x-trustifi-secret': os.environ['0f7c288aad8a9542f1c355b60b05e0f0'],
        # 'Content-Type': 'application/json'
        # }

        # response = requests.request('POST', url, headers = headers, data = payload)
        # print(response.json())
        # return render(request, 'email_result.html')





# def email_pdf(request):

#         extracted_links=[]#empty list to store all the extracted links from the database

#         for link in Publisher.objects.values_list('links'):
#                 print('The links are:\n',link)
#                 extracted_links.append('<li><a href='+link[0]+">"+link[0]+"</a></li>") #appending all the links to a list

#         url = os.environ['https://be.trustifi.com']+'/api/i/v1/email'
#         conn = http.client.HTTPSConnection("be.trustifi.com")
#         payload = json.dumps({
#         "recipients": [
#             {
#             "email": "aman777444@gmail.com",
#             "name": "Aman Mishra",
#             "body":''.join(extracted_links)
#             }
#         ],
#         })
#         headers = {
#         'x-trustifi-key': 'fff4ae6104486fc20de26cb0501f4310c663f9c0cbc8bf49',
#         'x-trustifi-secret': '0f7c288aad8a9542f1c355b60b05e0f0',
#         'Content-Type': 'application/json'
#         }
#         conn.request("POST", url, payload, headers)
#         res = conn.getresponse()
#         print('The response fromt the email is :\n',res)
#         data = res.read()
#         print('The data which is read is:\n',data)
#         print(data.decode("utf-8"))
#         return render(request, 'email_result.html')