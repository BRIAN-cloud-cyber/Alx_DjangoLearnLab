from django.shortcuts import render,redirect
from . forms import UserRegisterForm ,UserUpdateForm
from django.contrib import messages

def register(request):
    if request.method=='POST':
        form=UserRegisterForm(request.POST)
        if form.is_valid:
            form.save()

        messages.success(request,"Account Created Successfully! You can now log in.")
        return redirect('login')
    else:
        form=UserRegisterForm ()

    return render(request,'blog/register.html',{'form':form})
