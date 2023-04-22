from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name="home"),
   # path('recording/', views.recording, name='recording'),
    path('record_audio/', views.record_audio, name='record_audio'),
    path('save_audio/', views.save_audio, name='save_audio'),
    path('<slug:slug>/',views.DisplayCatalog, name="bookCatalog"),
    path('<slug:book_slug>/<slug:sub_slug>/',views.Displaycontent, name="bookContent"),



]