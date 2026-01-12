from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def home(request):
    return HttpResponse('welcome to the')

def contact(request):
    return HttpResponse('welcome to the contact page')

def dashboard(request):
    return render(request, 'dashboard.html')


