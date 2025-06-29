from django.shortcuts import render
from .models import Camera, Location


def home(request):
    return render(request, 'pages/home.html')

def archive(request):
    cams = Camera.objects.all()
    locs = Location.objects.all()
    return render(request, 'pages/archive.html', {
        "cams": cams,
        "locs": locs,
    })

def settings_page(request):
    return render(request, 'pages/settings.html')
