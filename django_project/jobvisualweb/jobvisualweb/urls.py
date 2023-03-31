"""jobvisualweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from mainsite import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.table, name='table'),
    path('table/', views.table, name='table'),

    path('word_cloud/', views.word_cloud, name='word_cloud'),
    path('wordcloud/', views.wordcloud, name='wordcloud'),

    path('pie_chart/', views.pie_chart, name='pie_chart'),
    path('piechart/', views.piechart, name='piechart'),

    path('lollipop_chart/', views.lollipop_chart, name='lollipop_chart'),
    path('lollipopchart/', views.lollipopchart, name='lollipopchart'),
]