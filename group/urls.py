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
from .views import *

# from .api import UserList, UserDetail, UserAuthentication

app_name = 'group'
urlpatterns = [
    path('MainGroup',views.mainGroup, name="MainGroup"),
    path('Group',views.group, name="Group"),
    path('MyGroup',views.myGroup, name="MyGroup"),
    # path('ViewGroup',views.viewGroup, name="ViewGroup"),
    path('JoinGroup/<str:pk>',views.joinGroup, name="JoinGroup"),
    path('DeleteGroup/<str:pk>',views.deleteGroup, name="DeleteGroup"),
    path('UpdateGroup/<str:pk>',views.updateGroup, name="UpdateGroup"),
 

] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()







