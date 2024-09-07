from django.urls import path
from . import views
app_name = 'calculator'
urlpatterns = [
    path('',views.home),
    path('percentage',views.per, name= 'percentage'),
    path('lots',views.lots, name = 'lots')
]