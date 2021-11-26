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
from urllib.request import urlopen


#mailscript libraries
import email, smtplib, ssl
import os
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import glob

from os import environ
import email.utils

#importing libraries for reading pdf and spacy
import PyPDF2 as pdf
import spacy
# from StringIO import StringIO

from spacy.lang.it.stop_words import STOP_WORDS as stopwords #getting the italian stop words




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
                #if response.status_code == 200: #checking if the url is responsive and available but removed due to time complexity issues with heroku
                a = urlparse(u)
                fl=os.path.basename(a.path) #parsing the filename from the url
                ### NLP SPACY
                String = "La Camera di Commercio territorialmente competente effettuerà controlli su un campione pari" #the search string from a pdf 
                print('The search string is :\n',String)
                
                file_read=urlopen(u).read()
                print('The pdf with urlopen is:\n',file_read)
                
                file = open(fl + ".pdf", 'wb')
                pdf_reader= pdf.PdfFileReader(file(u, "rb"))
                print('The pdf is:\n',pdf_reader)
                
                NumPages = pdf_reader.getNumPages()
                print('The number of pages in the pdf are:\n',NumPages)

                PageObj = pdf_reader.getPage(i)
                print("This is page " + str(i))
                Text = PageObj.extractText() #Extracting the text from the pdf page and then using the nlp to find the matching pattersns in the later stage 
                print(f'The extracted text from the page {i} is :\n{Text}')
                ResSearch = re.search(String, Text)
                print('The ResSearch result is :\n',ResSearch)
                # if ResSearch =='True':
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
                
                    #This will only execute the unencrypted files and valid files which contain the search string

                ###The previous v1.0 version is codeed below
                # file_size=response.headers.get('content-length', 0)
                # content_type=response.headers.get('Content-Type', 0)
                # last_modified=response.headers.get('Last-Modified', 0)
                # expiry_date=response.headers.get('Expires', 0)
                # cache_control=response.headers.get('Cache', 0)
                # server=response.headers.get('Server', 0)

                # pub_instance = Publisher.objects.create(name=fl,links=u,file_size=file_size,content_type=content_type,last_modified_y=last_modified,expiry_date_y=expiry_date,cache_control_y=cache_control,server_y=server) #creating the entry in the database
                # pub_instance.save() #saving the info for each url to database

                # for row in Publisher.objects.all().reverse(): #removing all the duplicate items from the database
                #     if Publisher.objects.filter(name=row.name).count() > 1: #using name as a filter
                #         print('Found Duplicate item:\n',row.name)
                #         row.delete()
    except Exception as exc:
        pass
        return render(request, 'result.html', {'list':all_links}) #redirecting to the results template page
        #if integrity exception error is passed or value error is thrown



def email_pdf(request):
    # read MailerToGo env vars
    url = os.environ['TRUSTIFI_URL']+'/api/i/v1/email'
    extracted_links=[]#empty list to store all the extracted links from the database

    for link in Publisher.objects.values_list('links'):
        print('The links are:\n',link)
        extracted_links.append('<li><a href='+link[0]+">"+link[0]+"</a></li>") #appending all the links to a list

    payload = "{\"recipients\":[{\"email\":\"aman777444@gmail.com\"}],\"title\":\"Crawler Result Dialy Mails\",\"html\":\"I hope you are well. These are the links which have been generated for your convinience.<br>"+''.join(extracted_links)+"<p>Regards,<br>Aman Mishra</p>\"}"
    headers = {
    'x-trustifi-key': os.environ['TRUSTIFI_KEY'], #automatically retrieves the key from the environment from os library
    'x-trustifi-secret': os.environ['TRUSTIFI_SECRET'], #this is also retrieved from os library
    'Content-Type': 'application/json' #the type of file we are passing 
    }
    
    response = requests.request('POST', url, headers = headers, data = payload)
    return render(request, 'email_result.html')

