from django.http import StreamingHttpResponse, HttpResponse
from django.shortcuts import render
import json
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
    if request.method == 'GET':
        return StreamingHttpResponse(
            vid.stream(),
            content_type='multipart/x-mixed-replace; boundary=frame'
        )
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            action = data.get('action')
            if action == 'pan-tilt':
                pan = data.get('pan')
                tilt = data.get('tilt')
                vid.ptz_move(pan=pan, tilt=tilt)
            # elif action == 'zoom':
            #     zoom = data.get('zoom')
            #     vid.ptz_zoom(zoom)
            elif action == 'stop':
                vid.ptz_stop()
            return HttpResponse(status=200)
        except Exception as err:
            return HttpResponseBadRequest(str(err))
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])
