from django.shortcuts import render, get_object_or_404, redirect

from .forms import InfoForm
from .models import Person

# Create your views here.
def user_list(request):
    users = Person.objects.all()
    return render(request,'InfoApp/user_list.html',{'users':users})

def user_detail(request,pk):
    user = get_object_or_404(Person,pk=pk)
    return render(request,'InfoApp/user_detail.html',{'user':user})

def user_create(request):
    if request.method == 'POST':
        form = InfoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
        else:
            form = InfoForm()
        return render(request,'InfoApp/user_form.html',{'form':form})

def user_update(request,pk):
    user = get_object_or_404(Person,pk=pk)
    if request.method == 'POST':
        form = InfoForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_detail',pk=pk)
        else:
            form = InfoForm(instance=user)
    return render(request,'InfoApp/user_form.html',{'form':form})

def user_delete(request,pk):
    user = get_object_or_404(Person,pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('user_list')
    return render(request,'InfoApp/user_confirm_delete.html',{'user':user})
