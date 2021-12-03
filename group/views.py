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
from .models import Group, GroupMembership, GroupSoilTag, GroupPlantTag
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
    
    if request.method=='POST':
        Name=request.POST.get('Name')
        About=request.POST.get('About')
        Media = request.FILES['Photo']
        fss =FileSystemStorage()
        file = fss.save(Media.name, Media)

        groupID = Group(Name=Name,About=About,Media=Media,Username=Username).save()
        group = Group.objects.get(id=groupID)

        soilTags = request.POST.getlist('SoilTag')
        plantTags = request.POST.getlist('PlantTag')

        for soilTag in soilTags:
            GroupSoilTag(SoilTagGroup=group, soilTag = soilTag).save()

        for plantTag in plantTags:
            GroupPlantTag(PlantTagGroup=group, plantTag = plantTag).save()

        messages.success(request,'The new group ' + request.POST['Name'] + " is create succesfully..!")
        
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


def updateGroup(request, pk):
    try:
        group=Group.objects.get(id=pk)
        group_farming = Group.objects.get(id=pk)
        soilTag=GroupSoilTag.objects.filter(SoilTagGroup=group)
        plantTag=GroupPlantTag.objects.filter(PlantTagGroup=group)
        if request.method=='POST':
            group.Name=request.POST.get('Name')
            group.About=request.POST.get('About')
            group.Media = request.POST.get('Photo')
            
            group_id=group.save()
            group_obj = Group.objects.get(id=group_id)

            # soilTags = request.POST.getlist('SoilTag')
            currentSoilTag=GroupSoilTag.objects.filter(SoilTagGroup=group)
            farmingSoilTag2=GroupSoilTag.objects.filter(SoilTagGroup=group_farming)

            currentPlantTag=GroupPlantTag.objects.filter(PlantTagGroup=group)
            farmingPlantTag2=GroupPlantTag.objects.filter(PlantTagGroup=group_farming)

        
            newSoilTags = request.POST.getlist('SoilTag')
            newPlantTags = request.POST.getlist('PlantTag')

            try:
                if soilTag:
                    for currentSoilTag in currentSoilTag:
                        currentSoilTag.deleteRecordFarming()
                    for farmingSoilTag2 in farmingSoilTag2:
                        farmingSoilTag2.deleteRecordIgrow()

                for newSoilTag in newSoilTags:
                    GroupSoilTag(SoilTagGroup=group_obj, soilTag = newSoilTag).save()

                if plantTag:
                    for currentPlantTag in currentPlantTag:
                        currentPlantTag.deleteRecordFarming()
                    for farmingPlantTag2 in farmingPlantTag2:
                        farmingPlantTag2.deleteRecordIgrow()

                for newPlantTag in newPlantTags:
                    GroupPlantTag(PlantTagGroup=group_obj, plantTag = newPlantTag).save()

            except IntegrityError:
                messages.error(request,'The group is already been tagged with the chosen tag(s)!')

            messages.success(request,'The ' + request.POST['Name'] + " is updated succesfully..!")
            # return render(request,'MyGroup.html')
            return redirect('group:MyGroup')
        else :
            return render(request,'UpdateGroup.html', {'data':group, 'soilTag':soilTag, 'plantTag':plantTag})
    
    except Group.DoesNotExist:
            raise Http404('Data does not exist')
