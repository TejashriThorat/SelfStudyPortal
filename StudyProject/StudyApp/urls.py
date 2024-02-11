"""
URL configuration for StudyProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('', views.home, name='home'),
    path('', views.home, name='home'),
    path('notes', views.notes, name='notes'),
    path('delete_note/<int:pk>', views.delete_note, name='delete_note'),
    path('notes_detail/<int:pk>',views.NotesDetailView.as_view(), name='notes_detail'),
    path('homework', views.homework, name='homework'),
    path('update_homework/<int:pk>', views.update_homework, name='update_homework'),
    path('delete_homework/<int:pk>', views.delete_homework, name='delete_homework'),
    path('youtube', views.youtube, name='youtube'),
    path('todo', views.todo, name='todo'),
    path('update_todo/<int:pk>', views.update_todo, name='update_todo'),
    path('delete_todo/<int:pk>', views.delete_todo, name='delete_todo'),
    path('books', views.books, name='books'),
    path('dictionary', views.dictionary, name='dictionary'),
    path('wiki', views.wiki, name='wiki'),
    path('conversion', views.conversion, name='conversion'),
    
    path("logout/",views.logout_user,name="logout")
]
