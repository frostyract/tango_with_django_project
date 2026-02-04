from django.shortcuts import render
from django.http import HttpResponse

# views go here
def index(request):
    return HttpResponse("Rango says hey there partner!")

def about(request):
    return HttpResponse("Rango says here is the about page.")
