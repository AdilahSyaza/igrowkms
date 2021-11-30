from django.http.response import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
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
from django.db import IntegrityError
from .models import Group, GroupMembership
from .forms import GroupForm
from member.models import Person


#group
def mainGroup(request):
    try:
        
        person=Person.objects.get(Email=request.session['Email'])
        # cuba
        group=Group.objects.all()
        fss =FileSystemStorage()
        # file = fss.save(Media.name, Media)
        uploaded_file = fss.url(group)
        return render(request,'MainGroup.html',{'group':group, 'uploaded_file':uploaded_file, 'person':person})

    except Group.DoesNotExist:
        raise Http404('Data does not exist')

def group(request):
    Username=Person.objects.get(Email=request.session['Email'])
    # UserMember=Username
    
    if request.method=='POST':
        Name=request.POST.get('Name')
        About=request.POST.get('About')
        # Media=request.POST.get('Media')
        Media = request.FILES['Photo']
        # cuba
        fss =FileSystemStorage()
        file = fss.save(Media.name, Media)
        # uploaded_file = fss.url()
        # group = Group(Name=Name,About=About,Media=Media,Username=Username).save()
        groupID = Group(Name=Name,About=About,Media=Media,Username=Username).save()
        # Group(Name=Name,About=About,Media=Media,Username=Username).save()
        # GroupMembership(GroupName=group, GroupMember=UserMember).save()
        messages.success(request,'The new group ' + request.POST['Name'] + " is create succesfully..!")
        
        # return render(request,'group.html')
        # cuba
        return redirect('group:JoinGroup', groupID)
    else :
        return render(request,'group.html')

def myGroup(request):
    try:
        Username=Person.objects.get(Email=request.session['Email'])
        # ambil group yg user create
        group=Group.objects.filter(Username=Username)
        # ambil group yg user join
        groupMembership=GroupMembership.objects.filter(GroupMember=Username)
        return render(request,'MyGroup.html',{'group':group,'groupMembership':groupMembership})
    except Group.DoesNotExist:
        raise Http404('Data does not exist')


# cuba
def showGroup(request):

    lastGroup = Group.objects.last()

    Media = lastGroup.Media
    
    form = GroupForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()

    context={'Media':Media,
            'form':form
            }

    return render(request,'group.html',context)



def joinGroup(request, pk):
    try:
        group = Group.objects.get(id=pk)
        user=Person.objects.get(Email=request.session['Email'])
        userName = user.Name
        groupName = group.Name
        GroupMembership(GroupName=group, GroupMember=user).save()
        messages.success(request,'The joining of ' + userName + ' in group ' + groupName + ' is succesful..!')
        # return render(request,'MainGroup.html', {'group':group, 'uploaded_file':uploaded_file, 'person':person})
        return redirect('group:MainGroup')
    except Group.DoesNotExist:
        raise Http404('Data does not exist')

    except IntegrityError:
        messages.error(request,'You already joined group ' + groupName + '!')
        return redirect('group:MainGroup')


def deleteGroup(request, pk):
    
    try:
        group=Group.objects.get(id=pk)
        group2=Group.objects.get(id=pk)
        
        data=Group.objects.all()
        if request.method=='POST':
            group.deleteRecordIgrow()
            group2.deleteRecordFarming()
            messages.success(request,'The ' + group.Name + " is deleted succesfully..!")
            return redirect('group:MyGroup')
        
        else:
            return render(request, 'deleteGroup.html', {'group':group})
        
    except Group.DoesNotExist:
        messages.success(request,'No record of the workshop!')
        return redirect('group:MyGroup')
