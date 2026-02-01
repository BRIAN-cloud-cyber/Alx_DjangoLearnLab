from django.shortcuts import render

from django .http import HttpResponse
from .models import student, course 

from django .views.generic import ListView,TemplateView,DetailView, UpdateView

def student_list(request):
    students=student.objects.all()
    return render (request, 'student_list.html', {'students': students})    

class courseListView(ListView):
    model=course
    template_name='course_list.html'
    context_object_name='courses'

class courseDetailView(DetailView):
    model=course
    template_name='course_detail.html'
    context_object_name='course'

    def __str__(self):
        return HttpResponse("Hello, world. You're at the ALX index.")
    
class studentUpdateView(UpdateView):
    model=student
    fields=['first_name', 'last_name', 'region']
    template_name='student_update.html'
    success_url='/students/'