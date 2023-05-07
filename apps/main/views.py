from django.shortcuts import render
# from django
# Create your views here.

def index(request):
    return render(request, 'main_app/index.html')