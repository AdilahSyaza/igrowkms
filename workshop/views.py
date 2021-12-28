from django.http.response import Http404
from django.shortcuts import render, redirect, get_object_or_404
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
from .models import Workshop, Booking, WorkshopSoilTagging, WorkshopPlantTagging
from member.models import Person, SoilTag, PlantTag
from django.db import IntegrityError



# Create your views here.

#workshop
def workshop(request):
        try:
            data=Workshop.objects.all()
            person=Person.objects.get(Email=request.session['Email'])

            return render(request,'workshop.html', {'person':person,'data':data})
        except Workshop.DoesNotExist:
            raise Http404('Data does not exist')
            
def createWorkshop(request):

    soilTagList=SoilTag.objects.all()
    plantTagList=PlantTag.objects.all()

    if request.method=='POST':
        pic=Person.objects.get(Email=request.session['Email'])
        ProgrammeName=request.POST.get('ProgrammeName')
        Speaker=request.POST.get('Speaker')
        Description=request.POST.get('Description')
        Date=request.POST.get('Date')
        # Session=request.POST.get('Session')
        StartTime=request.POST.get('StartTime')
        EndTime=request.POST.get('EndTime')
        State=request.POST.get('State')
        workshop_id = Workshop(ProgrammeName=ProgrammeName,Speaker=Speaker,Description=Description,Date=Date,StartTime=StartTime,EndTime=EndTime,State=State,PIC=pic).save()
        workshop = Workshop.objects.get(id=workshop_id)

        soilTagsID = request.POST.getlist('SoilTag')
        plantTagsID = request.POST.getlist('PlantTag')

        for soilTagsID in soilTagsID:
            soilTag = SoilTag.objects.get(id=soilTagsID)
            WorkshopSoilTagging(WorkshopSoilTag = workshop, soilTag=soilTag).save()

        for plantTagsID in plantTagsID:
            plantTag = PlantTag.objects.get(id=plantTagsID)
            WorkshopPlantTagging(WorkshopPlantTag = workshop, plantTag=plantTag).save()

        
        messages.success(request,'The new ' + request.POST['ProgrammeName'] + " is save succesfully..!")   

        return render(request,'CreateWorkshop.html')
    else :
        return render(request,'CreateWorkshop.html', {'SoilTag':soilTagList, 'PlantTag':plantTagList})


def updateWorkshop(request, pk):
    try:
        workshop=Workshop.objects.get(id=pk)
        workshop_farming = Workshop.objects.get(id=pk)
        
        # soilTag=WorkshopSoilTagging.objects.filter(WorkshopSoilTag=workshop)
        # plantTag=WorkshopPlantTagging.objects.filter(WorkshopPlantTag=workshop)
        
        soilTag=WorkshopSoilTagging.objects.filter(WorkshopSoilTag=workshop)
        soilTagList=SoilTag.objects.all()

        plantTag=WorkshopPlantTagging.objects.filter(WorkshopPlantTag=workshop)
        plantTagList=PlantTag.objects.all()

        if request.method=='POST':
            workshop.ProgrammeName=request.POST.get('ProgrammeName')
            workshop.Speaker=request.POST.get('Speaker')
            workshop.Description=request.POST.get('Description')
            workshop.Date=request.POST.get('Date')
            workshop.StartTime=request.POST.get('StartTime')
            workshop.EndTime=request.POST.get('EndTime')
            workshop.State=request.POST.get('State')
            # workshop_id=workshop.save()
            # workshop_obj = Workshop.objects.get(id=workshop_id)

            currentSoilTag=WorkshopSoilTagging.objects.filter(WorkshopSoilTag=workshop)
            farmingSoilTag2=WorkshopSoilTagging.objects.filter(WorkshopSoilTag=workshop)

            currentPlantTag=WorkshopPlantTagging.objects.filter(WorkshopPlantTag=workshop)
            farmingPlantTag2=WorkshopPlantTagging.objects.filter(WorkshopPlantTag=workshop)

        
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
                    WorkshopSoilTagging(WorkshopSoilTag=workshop, soilTag = new_soilTag).save()

                
                if plantTag:
                    for currentPlantTag in currentPlantTag:
                        currentPlantTag.deleteRecordFarming()
                    for farmingPlantTag2 in farmingPlantTag2:
                        farmingPlantTag2.deleteRecordIgrow()

                for newPlantTag in newPlantTags:
                    new_plantTag = PlantTag.objects.get(id=newPlantTag)
                    WorkshopPlantTagging(WorkshopPlantTag = workshop, plantTag=new_plantTag).save()

            # sebenarnya tak yah dah exception IntegrityError ni, sebab mmg takkan sampai sini sebab kita dah delete dulu baru save
            except IntegrityError:
                messages.error(request,'The workshop is already been tagged with the chosen tag(s)!')
                # messages.success(request,'The ' + request.POST['ProgrammeName'] + " is updated succesfully..!")
                # return render(request,'UpdateWorkshop.html')

            workshop.save()

            messages.success(request,'The ' + request.POST['ProgrammeName'] + " is updated succesfully..!")
            return render(request,'UpdateWorkshop.html')
        else :
            return render(request,'UpdateWorkshop.html', {'data':workshop, 'SoilTag':soilTagList, 'currentSoilTag':soilTag, 'PlantTag':plantTagList, 'currentPlantTag':plantTag})
    
    except Workshop.DoesNotExist:
            raise Http404('Data does not exist')


def deleteWorkshop(request, pk):
    # workshop = get_object_or_404(Workshop, id=pk)
    try:
        workshop=Workshop.objects.get(id=pk)
        workshop2=Workshop.objects.get(id=pk)
        # workshop_farming=Workshop.objects.using('farming').get(id=pk)
        
        data=Workshop.objects.all()
        if request.method=='POST':
            workshop.deleteRecordIgrow()
            workshop2.deleteRecordFarming()
            # workshop_farming.delete()
            messages.success(request,'The ' + workshop.ProgrammeName + " is deleted succesfully..!")
            return redirect('workshop:Workshop')
        
        else:
            return render(request, 'deleteWorkshop.html', {'workshop':workshop})
        
    except Workshop.DoesNotExist:
        messages.success(request,'No record of the workshop!')
        return redirect('workshop:Workshop')


def booking(request, pk):
    person = Person.objects.get(Email=request.session['Email'])
    workshop = Workshop.objects.get(id=pk)
    #return render(request, 'booking.html',{'person': person})
    if request.method=='POST':
    #    Name=request.POST.get('Description')
        try:
            ProgrammeName=request.POST.get('ProgrammeName')
            Date=request.POST.get('Date')
            # Session=request.POST.get('Session')
            Booking(ProgrammeName=ProgrammeName,Date=Date,BookWorkshop=workshop,Participant=person).save()
            messages.success(request,'The booking of ' + request.POST['ProgrammeName'] + " is saved succesfully..!")
            return render(request,'booking.html')
    
        except IntegrityError:
            messages.error(request,'You have already booked ' + ProgrammeName + '!')
            return render(request,'booking.html')
    
    else:    
        try:
            data = Workshop.objects.get(id=pk)
            # data=Workshop.objects.all() #filter(ProgrammeName=request.session['ProgrammeName'])
            return render(request,'booking.html',{'data':data})
        except Workshop.DoesNotExist:
            raise Http404('Data does not exist')



def viewWorkshop(request):
    try:
        user=Person.objects.get(Email=request.session['Email'])

        my_workshop=Workshop.objects.filter(PIC=user)

        
        return render(request,'MyWorkshop.html',{'data':my_workshop})
    except Workshop.DoesNotExist:
        raise Http404('Data does not exist')


def WorkshopParticipant(request, id):
    try:
        workshop = Workshop.objects.get(id=id)
        participantList=Booking.objects.filter(BookWorkshop=workshop)
        participant_count = Booking.objects.filter(BookWorkshop=workshop).count()

        return render(request,'WorkshopParticipant.html',{'data':participantList,'participant_count':participant_count})
    except Workshop.DoesNotExist:
        raise Http404('Data does not exist')


def Workshop_GeneralSoilTag(request):
    try:
        person=Person.objects.get(Email=request.session['Email'])
        data=Workshop.objects.all()
        # for setdata in dataWorkshopFilter:
        #     data=Workshop.objects.filter(id=setdata.SoilTagWorkshop.id)
            # Workshop.objects.get
            # data=Workshop.objects.filter(id=dataWorkshopFilter.SoilTagWorkshop.id)

        context = {
            "Clay": "Clay",
            "Sandy": "Sandy",
            "Silty": "Silty",
            "Peaty": "Peaty",
            "Chalky": "Chalky",
            "Loamy": "Loamy"
        }
            
            # return render(request,'WorkshopSoilTag.html', {'person':person,'data':data})
        return render(request,'workshop_soilTags.html', {'person':person,'data':data, 'context':context})

    except Workshop.DoesNotExist:
        raise Http404('Data does not exist')


def Workshop_SoilTag(request):
    
    data=Workshop.objects.all()
    person=Person.objects.get(Email=request.session['Email'])

    if request.method=='POST':
        
        soilTagsID = request.POST.get('SoilTag')
        soilTagging = SoilTag.objects.get(id=soilTagsID)

        filteredWorkshop = WorkshopSoilTagging.objects.filter(soilTag=soilTagging)

        return render(request,'SoilFilteredWorkshop.html', {'person':person, 'filteredWorkshop':filteredWorkshop, 'chosen_soilTag':soilTagging, 'ori_workshop':data})

    else:
        
        context = {
            'SoilTags': SoilTag.objects.all(), 
        }

        return render(request,'workshop.html', {'person':person,'data':data, 'context_SoilTags':context})


def Workshop_PlantTag(request):
    
    data=Workshop.objects.all()
    person=Person.objects.get(Email=request.session['Email'])

    if request.method=='POST':
        
        plantTagsID = request.POST.get('PlantTag')
        plantTagging = PlantTag.objects.get(id=plantTagsID)

        filteredWorkshop = WorkshopPlantTagging.objects.filter(plantTag=plantTagging)

        return render(request,'PlantFilteredWorkshop.html', {'person':person,'filteredWorkshop':filteredWorkshop, 'chosen_PlantTag':plantTagging, 'ori_workshop':data})

    else:
        
        context = {
            'PlantTags' : PlantTag.objects.all(),
        }

        return render(request,'workshop.html', {'person':person,'data':data, 'context_PlantTags':context})