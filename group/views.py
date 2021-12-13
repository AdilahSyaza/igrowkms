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
from .models import Group, GroupMembership, GroupPlantTagging, GroupSoilTagging
from .forms import GroupForm
from member.models import Person, SoilTag, PlantTag


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
    soilTagList=SoilTag.objects.all()
    plantTagList=PlantTag.objects.all()
    
    if request.method=='POST':
        Name=request.POST.get('Name')
        About=request.POST.get('About')
        Media = request.FILES['Photo']
        fss =FileSystemStorage()
        file = fss.save(Media.name, Media)

        groupID = Group(Name=Name,About=About,Media=Media,Username=Username).save()
        group = Group.objects.get(id=groupID)

        soilTagsID = request.POST.getlist('SoilTag')
        plantTagsID = request.POST.getlist('PlantTag')

        for soilTagsID in soilTagsID:
            soilTag = SoilTag.objects.get(id=soilTagsID)
            GroupSoilTagging(GroupSoilTag = group, soilTag=soilTag).save()

        for plantTagsID in plantTagsID:
            plantTag = PlantTag.objects.get(id=plantTagsID)
            GroupPlantTagging(GroupPlantTag = group, plantTag=plantTag).save()

        messages.success(request,'The new group ' + request.POST['Name'] + " is create succesfully..!")
        
        return redirect('group:JoinGroup', groupID)
    else :
        return render(request,'group.html', {'SoilTag':soilTagList, 'PlantTag':plantTagList})


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
        # group_farming = Group.objects.get(id=pk)
        soilTag=GroupSoilTagging.objects.filter(GroupSoilTag=group)
        plantTag=GroupPlantTagging.objects.filter(GroupPlantTag=group)
        
        soilTag=GroupSoilTagging.objects.filter(GroupSoilTag=group)
        soilTagList=SoilTag.objects.all()

        plantTag=GroupPlantTagging.objects.filter(GroupPlantTag=group)
        plantTagList=PlantTag.objects.all()

        if request.method=='POST':
            group.Name=request.POST.get('Name')
            group.About=request.POST.get('About')
            group.Media = request.POST.get('Photo')
                    
            currentSoilTag=GroupSoilTagging.objects.filter(GroupSoilTag=group)
            farmingSoilTag2=GroupSoilTagging.objects.filter(GroupSoilTag=group)

            currentPlantTag=GroupPlantTagging.objects.filter(GroupPlantTag=group)
            farmingPlantTag2=GroupPlantTagging.objects.filter(GroupPlantTag=group)

        
            newSoilTags = request.POST.getlist('SoilTag')
            newPlantTags = request.POST.getlist('PlantTag')

            try:
                if soilTag:
                    for currentSoilTag in currentSoilTag:
                        currentSoilTag.deleteRecordFarming()
                    for farmingSoilTag2 in farmingSoilTag2:
                        farmingSoilTag2.deleteRecordIgrow()

                for newSoilTag in newSoilTags:
                    new_soilTag = SoilTag.objects.get(id=newSoilTag)
                    GroupSoilTagging(GroupSoilTag=group, soilTag = new_soilTag).save()

                
                if plantTag:
                    for currentPlantTag in currentPlantTag:
                        currentPlantTag.deleteRecordFarming()
                    for farmingPlantTag2 in farmingPlantTag2:
                        farmingPlantTag2.deleteRecordIgrow()

                for newPlantTag in newPlantTags:
                    new_plantTag = PlantTag.objects.get(id=newPlantTag)
                    GroupPlantTagging(GroupPlantTag = group, plantTag=new_plantTag).save()


            except IntegrityError:
                messages.error(request,'The group is already been tagged with the chosen tag(s)!')
            
            group.save()

            messages.success(request,'The ' + request.POST['Name'] + " is updated succesfully..!")
            # return render(request,'MyGroup.html')
            return redirect('group:MyGroup')
        else :
            return render(request,'UpdateGroup.html', {'data':group, 'SoilTag':soilTagList, 'currentSoilTag':soilTag, 'PlantTag':plantTagList, 'currentPlantTag':plantTag})
    
    except Group.DoesNotExist:
            raise Http404('Data does not exist')


def Group_SoilTag(request):

    person=Person.objects.get(Email=request.session['Email'])
    group=Group.objects.all()
    fss =FileSystemStorage()
    uploaded_file = fss.url(group)
        

    if request.method=='POST':
        
        soilTagsID = request.POST.get('SoilTag')
        soilTagging = SoilTag.objects.get(id=soilTagsID)

        filteredGroup = GroupSoilTagging.objects.filter(soilTag=soilTagging)
        # filteredGroup = filtered_Soiltag.filter(GroupSoilTag__in=feed)

        return render(request,'SoilFilteredGroup.html', {'filteredGroup':filteredGroup, 'chosen_soilTag':soilTagging, 'ori_group':group})

    else:

        context = {
            'SoilTags': SoilTag.objects.all(), 
        }

        # return render(request, 'MainGroup.html', {'data':groupData, 'context_SoilTags':context})   
        return render(request,'MainGroup.html',{'group':group, 'uploaded_file':uploaded_file, 'person':person, 'context_SoilTags':context}) 


def Group_PlantTag(request):

    person=Person.objects.get(Email=request.session['Email'])
    group=Group.objects.all()
    fss =FileSystemStorage()
    uploaded_file = fss.url(group)

    if request.method=='POST':
        
        plantTagsID = request.POST.get('PlantTag')
        plantTagging = PlantTag.objects.get(id=plantTagsID)

        filteredGroup = GroupPlantTagging.objects.filter(plantTag=plantTagging)

        return render(request,'PlantFilteredGroup.html', {'filteredGroup':filteredGroup, 'chosen_plantTag':plantTagging, 'ori_group':group})

    else:

        context = {
            'PlantTags' : PlantTag.objects.all(),
        }
        
        return render(request,'MainGroup.html',{'group':group, 'uploaded_file':uploaded_file, 'person':person, 'context_PlantTags':context}) 
