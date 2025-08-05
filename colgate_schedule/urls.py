from django.urls import path
from .views.colgate_plan import ColgateProcessSchedule, ColgateMenuView
from .views.ajax import 

app_name = 'colgate_schedule'

urlpatterns = [
    path('memu/', ColgateMenuView.as_view(), name='menu'),
    path('colgate/schedule/<str:date_str>/<str:flute>/', ColgateProcessSchedule.as_view(), name='colgate_schedule'),

]