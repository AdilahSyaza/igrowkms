from django.http.response import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
# from LOGIN.models import Person as FarmingPerson
# from LOGIN.models import Feed, Booking, Workshop, Group, Member 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
# from .forms import CreateInDiscussion, PersonForm, UserUpdateForm
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.db.models.signals import post_save
from django.dispatch import receiver
from cryptography.fernet import Fernet
from .models import Feed, Comment
from group.models import Group
from member.models import Person

# Create your views here.


#sharing
def mainSharing(request):
    try:
        feed=Feed.objects.all()
        return render(request,'MainSharing.html',{'feed':feed})
    except Feed.DoesNotExist:
        raise Http404('Data does not exist')



def sharingGroup(request, pk):
    creator=Person.objects.get(Email=request.session['Email'])
    group_forum = Group.objects.get(id=pk)
    if request.method=='POST':
        Title=request.POST.get('Title')
        Message=request.POST.get('Message')
        Photo=request.POST.get('Photo')
        Video=request.POST.get('Video')
        Graph=request.POST.get('Graph')
        Feed(Title=Title,Message=Message,Photo=Photo,Video=Video,Graph=Graph,Group=group_forum,Creator=creator).save(),
        messages.success(request,'The new feed is save succesfully..!')
        return render(request,'sharing.html')
    else :
        return render(request,'sharing.html')

  

def updateSharing(request, pk):
    # feed = Feed.objects.filter(id=pk)
    feed = Feed.objects.get(id=pk)
    if request.method=='POST':
       
       feed.Title=request.POST['Title']
       feed.Message=request.POST.get('Message')
       feed.Photo=request.POST.get('Photo')
       feed.Video=request.POST.get('Video')
       feed.Graph=request.POST.get('Graph')
       feed.save()
       messages.success(request,'The post of ' + request.POST['Title'] + " is updated succesfully..!")
       return render(request,'ViewSharing.html')
    else:
        return render(request, 'ViewSharing.html', {'feed': feed})

def deleteSharing(request,pk):
    try:
        feed=Feed.objects.get(id=pk)
        feed2=Feed.objects.get(id=pk)

        data=Feed.objects.all()
        if request.method=='POST':
            feed.deleteRecordIgrow()
            feed2.deleteRecordFarming()
            # messages.success(request,'The ' + feed.Title + " is deleted succesfully..!")
            return redirect('sharing:MainSharing')
        
        else:
            return render(request, 'deleteSharing.html', {'feed':feed})
        
    except Feed.DoesNotExist:
        messages.success(request,'No record of the feed!')
        return redirect('sharing:MainSharing')


def viewForum(request, pk):
    data = Group.objects.get(id=pk)
    feed = Feed.objects.filter(Group = data)
    return render(request, 'Forum.html', {'feed': feed, 'data':data})


def addComment(request, pk):
    commenter=Person.objects.get(Email=request.session['Email'])
    feed = Feed.objects.get(id=pk)
    group_id = feed.Group.id
    
    if request.method=='POST':
        
        Message=request.POST.get('Message')
        Picture=request.POST.get('Pictures')
        Video=request.POST.get('Video')
        
        Comment(Message=Message,Pictures=Picture,Video=Video,Commenter=commenter,Feed=feed).save(),
        # messages.success(request,'The comment is save succesfully..!')
        # return render(request,'addComment.html')
        return redirect('sharing:Forum', group_id)
    else :
        return render(request,'addComment.html', {'feed':feed})

# def viewFeed(request, pk_feed, pk_group):

#     group = Group.objects.get(id=pk_group)
#     feed = Feed.objects.get(id=pk_feed,Group=group)
#     return render(request,'Forum.html', {'feed':feed})

def updateComment(request, pk):
   
    comment = Comment.objects.get(id=pk)
    group_id=comment.Feed.Group.id
    feed = comment.Feed
    if request.method=='POST':
       
       comment.Message=request.POST.get('Message')
       comment.Photo=request.POST.get('Picture')
       comment.Video=request.POST.get('Video')
       comment.save()
    #    messages.success(request,"The comment of is updated succesfully..!")
       return redirect('sharing:Forum', group_id)
    else:
        return render(request, 'addComment.html', {'comment': comment})

def deleteComment(request,pk):
    comment = Comment.objects.get(id=pk)
    group_id=comment.Feed.Group.id
    feed = comment.Feed
    try:
        comment=Comment.objects.get(id=pk)
        comment2=Comment.objects.get(id=pk)

        if request.method=='POST':
            comment.deleteRecordIgrow()
            comment2.deleteRecordFarming()
            # messages.success(request,'The ' + feed.Title + " is deleted succesfully..!")
            return redirect('sharing:Forum', group_id)
        
        else:
            return render(request, 'deleteComment.html', {'comment':comment})
        
    except Comment.DoesNotExist:
        messages.success(request,'No record of the comment!')
        return redirect('sharing:Forum', group_id)
