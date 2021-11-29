from django.db import models


# Create your models here.

class Publisher(models.Model):
     name = models.CharField(max_length=200) #primary key
     links = models.CharField(max_length=200)#primary key
     date_added = models.DateTimeField(auto_now_add=True)
     file_size = models.FloatField()
     content_type =models.CharField(max_length=200)
     last_modified_y = models.DateTimeField(auto_now_add=True)  
     expiry_date_y = models.DateTimeField(auto_now_add=True)
     cache_control_y = models.CharField(max_length=200) 
     server_y = models.CharField(max_length=200) 
     #storing the files to db
    #  filepath= models.FileField(upload_to='files/', null=True, verbose_name="")
     def __str__(self):
         return self.headline


