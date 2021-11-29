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
from .models import Workshop, Booking, SoilTag
from member.models import Person
from django.db import IntegrityError



# Create your views here.

#workshop
def workshop(request):
        try:
            data=Workshop.objects.all()
            # cuba
            person=Person.objects.get(Email=request.session['Email'])
            # context = {
            #     "Clay": "Clay",
            #     "Sandy": "Sandy",
            #     "Silty": "Silty",
            #     "Peaty": "Peaty",
            #     "Chalky": "Chalky",
            #     "Loamy": "Loamy"
            # }
            return render(request,'workshop.html', {'person':person,'data':data})
        except Workshop.DoesNotExist:
            raise Http404('Data does not exist')
            
def createWorkshop(request):
    if request.method=='POST':
        pic=Person.objects.get(Email=request.session['Email'])
        ProgrammeName=request.POST.get('ProgrammeName')
        Speaker=request.POST.get('Speaker')
        Description=request.POST.get('Description')
        Date=request.POST.get('Date')
        # Session=request.POST.get('Session')
        StartTime=request.POST.get('StartTime')
        EndTime=request.POST.get('EndTime')

        workshop_id = Workshop(ProgrammeName=ProgrammeName,Speaker=Speaker,Description=Description,Date=Date,StartTime=StartTime,EndTime=EndTime,PIC=pic).save()
        workshop = Workshop.objects.get(id=workshop_id)

        soilTags = request.POST.getlist('SoilTag')
        # i=0
        # numOfTag=soilTags.count
        # for i in range(numOfTag):
        #     SoilTag(workshopSoilTag=workshop, soilTag = soilTags[i]).save()
            # i=i+1
        for soilTag in soilTags:
            SoilTag(SoilTagWorkshop=workshop, soilTag = soilTag).save()

        
        messages.success(request,'The ' + request.POST['ProgrammeName'] + " is save succesfully..!")   

        return render(request,'CreateWorkshop.html')
    else :
        return render(request,'CreateWorkshop.html')


def updateWorkshop(request, pk):
    workshop=Workshop.objects.get(id=pk)
    workshop_farming = Workshop.objects.get(id=pk)
    soilTag=SoilTag.objects.filter(SoilTagWorkshop=workshop)
    if request.method=='POST':
        workshop.ProgrammeName=request.POST.get('ProgrammeName')
        workshop.Speaker=request.POST.get('Speaker')
        workshop.Description=request.POST.get('Description')
        workshop.Date=request.POST.get('Date')
        workshop.StartTime=request.POST.get('StartTime')
        workshop.EndTime=request.POST.get('EndTime')
        workshop_id=workshop.save()
        workshop_obj = Workshop.objects.get(id=workshop_id)
        # workshop_farming = Workshop.objects.get(id=workshop_id)

        # soilTags = request.POST.getlist('SoilTag')
        currentSoilTag=SoilTag.objects.filter(SoilTagWorkshop=workshop)
        farmingSoilTag2=SoilTag.objects.filter(SoilTagWorkshop=workshop_farming)

        # if soilTag:
        #     for currentSoilTag in currentSoilTag:
        #         currentSoilTag.deleteRecordFarming()
        #     for farmingSoilTag2 in farmingSoilTag2:
        #         farmingSoilTag2.deleteRecordIgrow()
       
        newSoilTags = request.POST.getlist('SoilTag')

        try:
            if soilTag:
                for currentSoilTag in currentSoilTag:
                    currentSoilTag.deleteRecordFarming()
                for farmingSoilTag2 in farmingSoilTag2:
                    farmingSoilTag2.deleteRecordIgrow()

            for newSoilTag in newSoilTags:
                SoilTag(SoilTagWorkshop=workshop_obj, soilTag = newSoilTag).save()

        # sebenarnya tak yah dah exception IntegrityError ni, sebab mmg takkan sampai sini sebab kita dah delete dulu baru save
        except IntegrityError:
            messages.error(request,'The workshop is already been tagged with the chosen tag(s)!')
            # messages.success(request,'The ' + request.POST['ProgrammeName'] + " is updated succesfully..!")
            # return render(request,'UpdateWorkshop.html')

        messages.success(request,'The ' + request.POST['ProgrammeName'] + " is updated succesfully..!")
        return render(request,'UpdateWorkshop.html')
    else :
        return render(request,'UpdateWorkshop.html', {'data':workshop, 'soilTag':soilTag})


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
    except Group.DoesNotExist:
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


def Workshop_SoilTag(request, soilTag):
        try:
            person=Person.objects.get(Email=request.session['Email'])
            dataWorkshopFilter=SoilTag.objects.filter(soilTag=soilTag)
            if dataWorkshopFilter:
                for setdata in dataWorkshopFilter:
                    data=Workshop.objects.filter(id=setdata.SoilTagWorkshop.id)
            else:
                data = ''
            
            context = {
                "Clay": "Clay",
                "Sandy": "Sandy",
                "Silty": "Silty",
                "Peaty": "Peaty",
                "Chalky": "Chalky",
                "Loamy": "Loamy"
            }
            
            # return render(request,'WorkshopSoilTag.html', {'person':person,'data':data})
            return render(request,'workshop_soilTags.html', {'person':person,'data':data, 'context':context, 'soilTag':soilTag})
        except Workshop.DoesNotExist:
            raise Http404('Data does not exist')


def Workshop_PlantTag(request):
        try:
            data=Workshop.objects.all()
            # cuba
            person=Person.objects.get(Email=request.session['Email'])
            # person = Person.objects.filter(Email=request.session['Email'])
            # return render(request,'workshop.html',{'data':data})
            # return render(request,'workshop.html',{'data':data},{'person':person})
            return render(request,'workshop.html', {'person':person,'data':data})
        except Workshop.DoesNotExist:
            raise Http404('Data does not exist')


def Workshop_LocationTag(request):
        try:
            data=Workshop.objects.all()
            # cuba
            person=Person.objects.get(Email=request.session['Email'])
            # person = Person.objects.filter(Email=request.session['Email'])
            # return render(request,'workshop.html',{'data':data})
            # return render(request,'workshop.html',{'data':data},{'person':person})
            return render(request,'workshop.html', {'person':person,'data':data})
        except Workshop.DoesNotExist:
            raise Http404('Data does not exist')


def Workshop_DemographicTag(request):
        try:
            data=Workshop.objects.all()
            # cuba
            person=Person.objects.get(Email=request.session['Email'])
            # person = Person.objects.filter(Email=request.session['Email'])
            # return render(request,'workshop.html',{'data':data})
            # return render(request,'workshop.html',{'data':data},{'person':person})
            return render(request,'workshop.html', {'person':person,'data':data})
        except Workshop.DoesNotExist:
            raise Http404('Data does not exist')