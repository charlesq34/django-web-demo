import os
import random
import string
import time

from django.shortcuts import render, render_to_response
from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from .forms import URLForm, UploadFileForm

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Create your views here.
def index(request):
    return render(request, 'visiondemo/demo.html')  

def handle_uploaded_file(f):
    with open(os.path.join(BASE_DIR, 'media/tmp.jpg'), 'wb+') as dst:
        for chunk in f.chunks():
            dst.write(chunk)

def loadFromExternalApp(filepath):
    while not os.path.exists(filepath+'.done'):
        time.sleep(1)
        pass
    return 1 #json.load(open(filepath))

# TODO: make sure there is a valid image before submit. retrieve result with request session id.
#@csrf_exempt
def result(request):
    #return HttpResponse("Hello, world. You've succeeded in uploading the image.")
    N = 10
    tag = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))
    open(os.path.join(BASE_DIR, 'media/', tag+'.query.done'), 'w').close()

    result = loadFromExternalApp(os.path.join(BASE_DIR, 'media/', tag+'.result'))
    return render(request, 'visiondemo/result.html')

@csrf_exempt
def fileupload(request):
    if request.method == 'POST':
        #try:
        #    handle_uploaded_file(request.FILES['file'])
        #    HttpResponse('ok')
        #except:
        #    pass
        try:
            print('try UploadFileForm ...')
            form = UploadFileForm(request.POST, request.FILES)
            print(form.is_valid())
            if form.is_valid():
                handle_uploaded_file(request.FILES['file'])
                time.sleep(3)
                return HttpResponseRedirect(reverse('visiondemo:result'))
        except:
            pass

        try:
            print('URL form...')
            form = URLForm(request.POST)
            print(form)
            if form.is_valid():
                print(form.cleaned_data['myinput'])
                os.system('wget %s -O %s' % (form.cleaned_data['myinput'], os.path.join(BASE_DIR, 'media/tmp.jpg')))
                time.sleep(3)
                return HttpResponseRedirect(reverse('visiondemo:result'))
        except:
            pass

    return HttpResponse('error')
