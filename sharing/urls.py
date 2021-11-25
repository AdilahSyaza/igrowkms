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

app_name = 'sharing'
urlpatterns = [
    path('MainSharing',views.mainSharing, name="MainSharing"),
    path('SharingGroup/<str:pk>',views.sharingGroup, name="SharingGroup"),
    path('UpdateSharing/<str:pk>',views.updateSharing, name="UpdateSharing"),
    path('DeleteSharing/<str:pk>', views.deleteSharing, name="DeleteSharing"),
    path('Forum/<str:pk>', views.viewForum, name="Forum"),
    path('Forum/<str:pk>/Comment/', views.addComment, name="AddComment"),
    path('UpdateComment/<str:pk>',views.updateComment, name="UpdateComment"),
    path('DeleteComment/<str:pk>', views.deleteComment, name="DeleteComment"),


] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()







