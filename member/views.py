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
from .models import Person, MemberRequest,Memberlist, Room, Message, SensorData, Plants
from django.http import HttpResponse, JsonResponse

# def encryptPassword(password):
#         key = Fernet.generate_key()
#         fernet = Fernet(key)
#         # pk = bytes(password, encoding)
#         encryptedpass = fernet.encrypt(password.encode('ascii'))
#         return encryptedpass

# def decryptPassword(password):
#         key = Fernet.generate_key()
#         fernet = Fernet(key)
#         decryptedpass = fernet.decrypt(password).decode('ascii')
#         return decryptedpass

def Indexpage(request):
    return render(request, 'index.html')

def homepage(request):
    person = Person.objects.filter(Email=request.session['Email'])
    return render(request, 'homepage.html',{'person': person })




#user registration
def UserReg(request):
    try:
        if request.method=='POST':
            Email=request.POST['Email']
            # Pwd=encryptPassword(request.POST['Pwd'])
            Pwd=request.POST['Pwd']
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

    except IntegrityError:
        messages.error(request,'You email address has already registered!')
        return render(request,'registration.html')

# def loginpage(request):
#     if request.method == "POST":
#         try:
#             User = Person.objects.filter(Email = request.POST['Email'])
            
#             if (User.exists()):
#                 UserExist = Person.objects.get(Email = request.POST['Email'])
#                 password=decryptPassword(UserExist.Password)
#             else:
#                 messages.success(request,'Username/Password Invalid..!')
#                 return render(request,'login.html')
#             Userdetails = Person.objects.get(Email = request.POST['Email'], Password = password)
#             print("Username", Userdetails)
#             request.session['Email'] = Userdetails.Email
#             person = Person.objects.filter(Email = request.POST['Email'])
#             return render(request,'homepage.html',{'person' : person})
#         except Person.DoesNotExist as e:
#             messages.success(request,'Username/Password Invalid..!')
#     return render(request,'login.html')

def loginpage(request):
    if request.method == "POST":
        try:
            Userdetails = Person.objects.get(Email = request.POST['Email'], Password = (request.POST['Pwd']))
            print("Username", Userdetails)
            request.session['Email'] = Userdetails.Email
            person = Person.objects.filter(Email = request.POST['Email'])
            return render(request,'homepage.html',{'person' : person})
        except Person.DoesNotExist as e:
            messages.success(request,'Username/Password Invalid..!')
    return render(request,'login.html')

def logout(request):
    try:
        del request.session['Email']
    except:
        return render(request,'index.html')
    return render(request,'index.html')

#profile
def view(request):
    person = Person.objects.filter(Email=request.session['Email'])
    if request.method=='POST':
       t = Person.objects.get(Email=request.session['Email'])
    #    Pwd=encryptPassword(request.POST.get['Pwd'])
    #    t.Password=encryptPassword(request.POST['Password'])
       t.Password=request.POST['Password']
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
        # decryptPass = deryptPassword(person.Password)
        return render(request, 'profile.html',{'person': person})  


#member
def mainMember(request):
    return render(request,'MainMember.html')


# def member(request):
#     if request.method=='POST':
#         Name=request.POST.get('Name')
#         Study=request.POST.get('Study')
#         Lives=request.POST.get('Lives')
#         Member(Name=Name,Study=Study,Lives=Lives).save(),
#         messages.success(request,'The new member ' + request.POST['Name'] + " is create succesfully..!")
#         return render(request,'member.html')
#     else :
#         return render(request,'member.html')


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
    member1 = Memberlist.objects.get(to_person=user, from_person=user2)
    member2 = Memberlist.objects.get(from_person=user, to_person=user2)

    if request.method=='POST':
        member1.deleteRecordIgrow()
        member2.deleteRecordFarming()
        messages.success(request, "You have unfriended " + user2.Name +" ..!")
        return render(request, 'friendlist.html')
    else:
        return render(request, 'friendlist.html')


def myMember(request):
    #try:
    #    member=Member.objects.filter(Name=request.session['Name'])
        return render(request,'MyMember.html')#{'member':member})
    #except Member.DoesNotExist:
     #   raise Http404('Data does not exist')

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


        
