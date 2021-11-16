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
from django.dispatch import receiver
from cryptography.fernet import Fernet
from .models import Person, Member, SensorData, Plants, Users

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




#user registration
def UserReg(request):
    if request.method=='POST':
        Email=request.POST['Email']
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
        #cuba
        # FarmingPerson(Email=Email,Password=Pwd,Username=Username,Name=Name,DateOfBirth=DateOfBirth,Age=Age,District=District,State=State,
        #     Occupation=Occupation,About=About,Gender=Gen,MaritalStatus=MaritalStatus).save(),
        # FarmingPerson(Email=Email,Password=Pwd,Username=Username,Name=Name,DateOfBirth=DateOfBirth,Age=Age,District=District,State=State,
            # Occupation=Occupation,About=About,Gender=Gen,MaritalStatus=MaritalStatus),
        messages.success(request,'The new user ' + request.POST['Username'] + " is save succesfully..!")
        return render(request,'registration.html')
    else :
        return render(request,'registration.html')


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
        return render(request, 'profile.html',{'person': person})  


#member
def mainMember(request):
    try:
        member = Member.objects.all()
        return render(request,'MainMember.html',{'member':member})
    except Member.DoesNotExist:
        raise Http404('Data does not exist')

def member(request):
    if request.method=='POST':
        Name=request.POST.get('Name')
        Study=request.POST.get('Study')
        Lives=request.POST.get('Lives')
        Member(Name=Name,Study=Study,Lives=Lives).save(),
        messages.success(request,'The new member ' + request.POST['Name'] + " is create succesfully..!")
        return render(request,'member.html')
    else :
        return render(request,'member.html')
def friendlist(request):
    #try:
    #    member=Member.objects.filter(Name=request.session['Name'])
        return render(request,'friendlist.html')#{'member':member})
    #except Member.DoesNotExist:
     #   raise Http404('Data does not exist')


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
