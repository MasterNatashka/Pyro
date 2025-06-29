from django.shortcuts import render

def home(request):
    return render(request, 'pages/home.html')

def archive(request):
    return render(request, 'pages/archive.html')

def settings_page(request):
    return render(request, 'pages/settings.html')
