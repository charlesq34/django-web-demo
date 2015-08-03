import os
import random
import string
import time

from django.shortcuts import render
from django.template import RequestContext, loader
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Create your views here.
def index(request):
    return render(request, 'visiondemo/demo.html')  

def handle_uploaded_file(f):
    with open(os.path.join(BASE_DIR, 'media/tmp.jpg'), 'wb+') as dst:
        for chunk in f.chunks():
            dst.write(chunk)

@csrf_exempt
def fileupload(request):
    if request.method == 'POST':
        handle_uploaded_file(request.FILES['file'])
    return HttpResponse('ok')


def loadFromExternalApp(filepath):
    while not os.path.exists(filepath+'.done'):
        time.sleep(1)
        pass
    return 1 #json.load(open(filepath))

def result(request):
    #return HttpResponse("Hello, world. You've succeeded in uploading the image.")

    N = 10
    tag = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))
    open(os.path.join(BASE_DIR, 'media/', tag+'.query.done'), 'w').close()

    result = loadFromExternalApp(os.path.join(BASE_DIR, 'media/', tag+'.result'))
    return render(request, 'visiondemo/result.html')
