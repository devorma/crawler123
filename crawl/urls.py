from django.urls import path

from . import views

urlpatterns=[
    path('',views.home,name='home'),
    path('initiate',views.crawl,name='crawl')
    # path('email',views.email_pdf,name='emailpdf')
]

