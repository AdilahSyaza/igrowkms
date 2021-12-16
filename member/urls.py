"""LOGIN URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf.urls import url, include
# from LOGIN import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# from LOGIN.views import UserReg, sharing, discussion, view, workshop, booking, member
from .import views
from django.conf.urls import url
# from .import index

from .api import UserList, UserDetail, UserAuthentication

urlpatterns = [
    path('',views.Indexpage),
    path('Home',views.homepage, name="Home"),
    path('Registration', views.UserReg, name="Reg"),
    path('Loginpage', views.loginpage, name="Loginpage"),
    path('Logout',views.logout, name="Logout"),
    path('View',views.view,name="View"),

    path('MainMember', views.mainMember, name="MainMember"),
    path('Friendlist',views.friendlist, name="friendlist"),
    path('MainSearchbar/', views.MainSearchbar, name='MainSearchbar'),
    path('MainSearchbar/<str:pk>', views.v2MainSearchbar, name='v2MainSearchbar'),
    path('PendingMemberRequest', views.pendingMemberRequest, name='PendingMemberRequest'),
    path('sendMemberRequest/<str:userID>', views.sendMemberRequest, name='sendMemberRequest'),
    path('acceptMemberRequest/<str:requestID>', views.acceptMemberRequest, name='acceptMemberRequest'),
    path('Friendlist/Unfriend/<str:pk>', views.unfriend, name='unfriend'),
    path('ChatRoom/<str:room>', views.chatRoom, name='ChatRoom'),
    path('send', views.send, name='send'),
    path('getMessages/<str:room>/', views.getMessages, name='getMessages'),

    path('ViewProfile/<str:id>',views.viewProfile,name="ViewProfile"),

    path("add-soilTag/", views.add_SoilTag, name="add_SoilTag"),
    path("add-plantTag/", views.add_PlantTag, name="add_PlantTag"),

    url(r'^api/users_list/$', UserList.as_view(), name='user_list'),
    url(r'^api/users_list/(?P<Person>\d+)/$', UserDetail.as_view(), name='user_list'),
    url(r'^api/auth/$', UserAuthentication.as_view(), name='User Authentication API') 

] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()







