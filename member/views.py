from django.http.response import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
# from .forms import CreateInDiscussion, PersonForm, UserUpdateForm
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.db.models.signals import post_save
from django.db import IntegrityError
from django.dispatch import receiver
from cryptography.fernet import Fernet
from .models import Person, MemberRequest,Memberlist, Room, Message, SensorData, SoilTag, PlantTag
from django.http import HttpResponse, JsonResponse
from igrowKMS import encryption_util

# def encryptPassword(Pwd):
#         key = Fernet.generate_key()
#         fernet = Fernet(key)
#         encrypted = fernet.encrypt(Pwd.encode())
#         return encrypted

# def deryptPassword(Pwd):
#         key = Fernet.generate_key()
#         fernet = Fernet(key)
#         decrypted = fernet.decrypt(Pwd).decode()
#         return decrypted

def Indexpage(request):
    return render(request, 'index.html')

def homepage(request):
    person = Person.objects.filter(Email=request.session['Email'])
    return render(request, 'homepage.html',{'person': person })


def OurServices(request):
    return render(request, 'OurServices.html')


def About(request):
    return render(request, 'About.html')


def ContactUs(request):
    return render(request, 'ContactUs.html')


#user registration
def UserReg(request):
    if request.method=='POST':
        Email=request.POST['Email']
        Pwd=encryption_util.encrypt(request.POST['Pwd']) 
        Username=request.POST.get('Username')
        Name=request.POST.get('Name')
        DateOfBirth=request.POST.get('DateOfBirth')
        Age=request.POST['Age']
        District=request.POST['District']
        State=request.POST['State']
        Occupation=request.POST['Occupation']
        About=request.POST['About']
        Gen=request.POST.get('Gender')
        MaritalStatus=request.POST.get('MaritalStatus')
        UserLevel=request.POST.get('UserLevel')
        Person(Email=Email,Password=Pwd,Username=Username,Name=Name,DateOfBirth=DateOfBirth,Age=Age,District=District,State=State,
            Occupation=Occupation,About=About,Gender=Gen,MaritalStatus=MaritalStatus,UserLevel=UserLevel).save(),
        messages.success(request,'The new user ' + request.POST['Username'] + " is save succesfully..!")
        return render(request,'registration.html')
    else :
        return render(request,'registration.html')

def loginpage(request):
    if request.method == "POST":
        try:
            Userdetails = Person.objects.get(Email = request.POST['Email'])
            print("Username", Userdetails)
            request.session['Email'] = Userdetails.Email
            person = Person.objects.filter(Email = request.POST['Email'])
            if encryption_util.decrypt(Userdetails.Password)== request.POST['Pwd']:
             return render(request,'homepage.html',{'person' : person})
            else:
             messages.success(request,'Pasword is incorrect')
        except Person.DoesNotExist as e:
            messages.success(request,'Username is not available')
    return render(request,'login.html')


def logout(request):
    try:
        del request.session['Email']
    except:
        return render(request,'index.html')
    return render(request,'index.html')

#profile
def view(request):
    person = Person.objects.get(Email=request.session['Email'])
    if request.method=='POST':
       t = Person.objects.get(Email=person.Email)
       t.Email=request.POST['Email']
       request.session['Email'] = t.Email
       t.Password=encryption_util.encrypt(request.POST['Password'])
    #    t.Password=request.POST['Password']
       t.Username=request.POST.get('Username')
       t.Name=request.POST.get('Name')
       t.DateOfBirth=request.POST.get('DateOfBirth')
       t.Age=request.POST['Age']
       t.District=request.POST['District']
       t.State=request.POST['State']
       t.Occupation=request.POST['Occupation']
       t.About=request.POST['About']
       t.Gen=request.POST.get('Gender')
       t.MaritalStatus=request.POST.get('MaritalStatus')
       t.save()
       return render(request,'homepage.html')
    else:
        decryptPass = encryption_util.decrypt(person.Password)
        return render(request, 'profile.html',{'person': person,'password':decryptPass})


def viewProfile(request, id):
    participantProfile=Person.objects.get(id=id)
    return render(request, 'ViewProfile.html',{'participantProfile':participantProfile})


#member
def mainMember(request):
    return render(request,'MainMember.html')

def sendMemberRequest(request, userID):
    
    try:
        from_user=Person.objects.get(Email=request.session['Email'])
        to_user=Person.objects.get(id=userID)
        to_user_id = to_user.id
        
        MemberRequest(from_user=from_user, to_user=to_user).save()
        messages.success(request,'Member request to ' + to_user.Name + " is sent succesfully..!")

        return redirect('v2MainSearchbar', to_user_id)

    except MemberRequest.DoesNotExist:
        raise Http404('Data does not exist')

    except IntegrityError:
        messages.error(request,'You already sent friend request to ' + to_user.Name + '!')
        return redirect('v2MainSearchbar', to_user_id)


def acceptMemberRequest(request, requestID):
    user=Person.objects.get(Email=request.session['Email'])
    
    member_request = MemberRequest.objects.get(id=requestID)
    member_request2 = MemberRequest.objects.get(id=requestID)

    from_person = member_request.from_user
    room_id = Room(member1 = user, member2 = from_person).save()
    room = Room.objects.get(id=room_id)

    try:

        if member_request.to_user == user:
            
            
            Memberlist(from_person=from_person, to_person=user, chatRoom=room).save()
            Memberlist(from_person=user, to_person=from_person, chatRoom=room).save()
            
            member_request.deleteRecordIgrow()
            member_request2.deleteRecordFarming()
            
            messages.success(request,'Member request accepted ')
            return redirect('PendingMemberRequest')
            
        else:
            messages.success(request,'Member request does not accepted ')
            return redirect('PendingMemberRequest')
    
    except IntegrityError:
        messages.error(request,'You already membered with ' + from_person.Name + '!')
        return redirect('PendingMemberRequest')



def pendingMemberRequest(request):
    
    user=Person.objects.get(Email=request.session['Email'])

    try:        
        userRequestList = MemberRequest.objects.all().filter(to_user=user)
        # messages.success(request,'There are request..!')
        return render(request,'FriendRequest.html', {'userRequestList':userRequestList})
    
    except MemberRequest.DoesNotExist:
        messages.success(request,'No Request..!')
        return render(request,'FriendRequest.html')
        

def friendlist(request):
    
    user=Person.objects.get(Email=request.session['Email'])

    try:
        memberList = Memberlist.objects.all().filter(to_person=user)
        return render(request,'friendlist.html', {'memberList':memberList})

    except Memberlist.DoesNotExist:
        messages.success(request,'You have no friends yet..!')
        return render(request,'friendlist.html')


def unfriend(request, pk):
    
    user=Person.objects.get(Email=request.session['Email'])
    user2=Person.objects.get(id=pk)

    member1_igrow = Memberlist.objects.get(to_person=user, from_person=user2)
    member2_igrow = Memberlist.objects.get(from_person=user, to_person=user2)

    member1_farming = Memberlist.objects.get(to_person=user, from_person=user2)
    member2_farming = Memberlist.objects.get(from_person=user, to_person=user2)

    # if request.method=='POST':
    member1_igrow.deleteRecordIgrow()
    member2_igrow.deleteRecordIgrow()

    member1_farming.deleteRecordFarming() 
    member2_farming.deleteRecordFarming()

    messages.success(request, "You have unfriended " + user2.Name +" ..!")
    return render(request, 'friendlist.html')
    # else:
    #     return render(request, 'friendlist.html')

def MainSearchbar(request):
    if request.method == 'GET':
        search = request.GET.get('search')
        Name = Person.objects.all().filter(Name=search)
        # cuba
        Name2 = Name.exclude(Email=request.session['Email'])
        return render(request, 'MainSearchbar.html', {'Name': Name2})
    # else:
    #     person = from_user
    #     return render(request, 'MainSearchbar.html', {'sentRequestUser': person})

def v2MainSearchbar(request, pk):
    
    person = Person.objects.get(id=pk)
    return render(request, 'MainSearchbar.html', {'sentRequestUser': person})


def chatRoom(request, room):

    room = Room.objects.get(id = room)
    user=Person.objects.get(Email=request.session['Email'])

    return render(request, 'ChatRoom.html', {'room':room, 'user':user})


def send(request):
    message = request.POST['message']
    user = request.POST['sender']
    room_id = request.POST['room']
    room = Room.objects.get(id = room_id)
    # user = Person.objects.get(id = user_id)


    Message(value=message, sender=user, room=room).save()
    
    return HttpResponse('Message sent successfully')

def getMessages(request, room):
    room = Room.objects.get(id=room)

    messages = Message.objects.filter(room=room.id)
    return JsonResponse({"messages":list(messages.values())})


def TagSuggestion(request):
    person=Person.objects.get(Email=request.session['Email'])
    soilTagList=SoilTag.objects.all()
    plantTagList=PlantTag.objects.all()

    return render(request,'MainTaggingSuggestion.html', {'person':person, 'soilTag':soilTagList, 'plantTag':plantTagList})


def add_SoilTag(request):
    
    try:   
        if request.method=='POST':
            soilTag = request.POST.get("SoilTag")
            SoilTag(SoilTagName=soilTag).save()
            return render(request, "soilTag.html", {"msg":"soil Tag added!"})
        else:
            return render(request, "soilTag.html")

    except IntegrityError:
        return render(request, "soilTag.html", {"msg":"The " + soilTag +" Soil Tag has already been added before!"})        


def add_PlantTag(request):
    try:
        if request.method=='POST':
            plantTag = request.POST.get("PlantTag")
            PlantTag(PlantTagName=plantTag).save()
            return render(request, "plantTag.html", {"msg":"Plant Tag added!"})
        else:
            return render(request, "plantTag.html")
    except IntegrityError:
        return render(request, "plantTag.html", {"msg":"The " + plantTag + " Tag has already been added before added!"})


def UpdateSoilTag(request, id):
    try:
        soilTag=SoilTag.objects.get(id=id)

        if request.method=='POST':

            soilTag.SoilTagName= request.POST.get("SoilTag")       
            soilTag.save()
            return render(request, "UpdateSoilTag.html", {"msg":"Soil Tag has been updated!"})
        else:
            return render(request, "UpdateSoilTag.html", {'soilTag':soilTag})
    except IntegrityError:
        return render(request, "soilTag.html", {"msg":"The " + soilTag.SoilTagName + " tag is already in the record"})


def DeleteSoilTag(request, id):
    try:
        soilTagList=SoilTag.objects.all()
        plantTagList=PlantTag.objects.all()

        soilTag_igrow=SoilTag.objects.get(id=id)
        soilTag_farming=SoilTag.objects.get(id=id)

        if request.method=='POST':

            soilTag_igrow.deleteRecordIgrow()
            soilTag_farming.deleteRecordFarming()

            messages.success(request,'The ' + soilTag_igrow.SoilTagName + " is deleted succesfully..!")

            return redirect('TagSuggestion')
        else:
            return render(request, "DeleteSoilTag.html", {'soilTag':soilTag_igrow})
    except SoilTag.DoesNotExist:
            raise Http404('Data does not exist')


def UpdatePlantTag(request, id):
    try:
        plantTag=PlantTag.objects.get(id=id)

        if request.method=='POST':

            plantTag.PlantTagName= request.POST.get("PlantTag")       
            plantTag.save()
            return render(request, "UpdatePlantTag.html", {"msg":"Plant Tag has been updated!"})
        else:
            return render(request, "UpdatePlantTag.html", {'plantTag':plantTag})
    except IntegrityError:
        return render(request, "plantTag.html", {"msg":"The " + plantTag.PlantTagName + " tag is already in the record"})


def DeletePlantTag(request, id):
    try:
        soilTagList=SoilTag.objects.all()
        plantTagList=PlantTag.objects.all()

        plantTag_igrow=PlantTag.objects.get(id=id)
        plantTag_farming=PlantTag.objects.get(id=id)

        if request.method=='POST':

            plantTag_igrow.deleteRecordIgrow()
            plantTag_farming.deleteRecordFarming()

            messages.success(request,'The ' + plantTag_igrow.PlantTagName + " is deleted succesfully..!")

            return redirect('TagSuggestion')
        else:
            return render(request, "DeletePlantTag.html", {'plantTag':plantTag_igrow})
    except PlantTag.DoesNotExist:
            raise Http404('Data does not exist')

        
