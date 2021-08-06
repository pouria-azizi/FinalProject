from django.urls import path
from . import views


app_name = 'quotes'

urlpatterns = [
    path('create_quote/', views.CreateItemQuotes.as_view(), name='create_quote'),
    path('new_quote/', views.CreateQuotes.as_view(), name='new_quote'),
    path('quote_list/', views.QuoteList.as_view(), name='quote_list'),
    path('quote_detail/<int:pk>', views.QuoteDetail.as_view(), name='quote_detail'),
    path('quote_pdf/<int:pk>', views.QuotePDF.as_view(), name='quote_pdf'),
    path('send_email/<int:pk>', views.send_email_to_organs, name='send-email')
]
