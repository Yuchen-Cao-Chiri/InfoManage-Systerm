"""infoManage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path,include
from Comsearch import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
admin.autodiscover()
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('register/',views.register,name='register'),
    path('index/',views.index,name='index'),
    path('index/welcome/',views.welcome,name='welcome'),
    path('information/',views.information,name='information'),
    path('search/',views.search,name='search'),
    path('add/',views.add_cominfo,name='add_cominfo'),
    path('del/',views.del_cominfo,name='del_cominfo'),
    path('sdel/',views.deleteSelect,name='deleteSelect'),
    path('mod/',views.mod_cominfo,name='mod_cominfo'),

]
urlpatterns += staticfiles_urlpatterns()

