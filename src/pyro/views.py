from django.http import StreamingHttpResponse
from django.shortcuts import render
from .models import Camera, Location
from .features.video.CameraFeed import CameraFeed


def home(request):
    cams = Camera.objects.all()
    return render(request, 'pages/home.html', {
        'cams': cams,
    })

def archive(request):
    cams = Camera.objects.all()
    locs = Location.objects.all()
    return render(request, 'pages/archive.html', {
        'cams': cams,
        'locs': locs,
    })

def settings(request):
    return render(request, 'pages/settings.html')

def video(request, id):
    cam = Camera.objects.get(pk=id)
    vid = CameraFeed(cam.address)
    return StreamingHttpResponse(
        vid.stream(),
        content_type='multipart/x-mixed-replace; boundary=frame'
    )
