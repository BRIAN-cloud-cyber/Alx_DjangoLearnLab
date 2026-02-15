from django.shortcuts import render,redirect
from . forms import UserRegisterForm ,UserUpdateForm
from django.contrib import messages
from . models import User
from django.contrib.auth import authenticate , login


def register(request):
    if request.method=='POST':
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()

        messages.success(request,"Account Created Successfully! You can now log in.")
        return redirect('login')
    else:
        form=UserRegisterForm ()

    return render(request,'blog/register.html',{'form':form})


def login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

#checks if a user with the provided username exists

        if not User.objects.filter(username==username).exists():
            #display an error message if the username does not exist
            messages.error(request,"Invalid Username")
            return redirect('/login/')
        
        user=authenticate(username=username,password=password)

        if user is None:
            #display an error message if authentication fails (invalid password)
            messages.error(request,"Invalid password")
            return redirect ('/login/')
        
        else:
            login(request,user)
            return redirect ('/home/')
        
    
    return render(request, 'login.html')