import os
import random
import string
import time
import uuid

from django.shortcuts import render, render_to_response
from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from .forms import URLForm, UploadFileForm

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# MAIN PAGE
def index(request):
    return render(request, 'visiondemo/demo.html')  

# RESULT PAGE
def result(request):
    if 'cookie_tag' in request.COOKIES:
        tag = request.COOKIES[ 'cookie_tag' ]
        print('cookie_tag: %s' % (tag))
        input_img_fname = '../media/%s_tmp.jpg' % (tag)
        output_img_fname = '../media/%s_tmp_out.jpg' % (tag)
        return render(request, 'visiondemo/demo.html', {'image_list': [input_img_fname,output_img_fname]})
    else:
        return Http404("Error")


def handle_uploaded_file(f, fname):
    with open(fname, 'wb+') as dst:
        for chunk in f.chunks():
            dst.write(chunk)

def loadFromExternalApp(filepath):
    while not os.path.exists(filepath+'.done'):
        time.sleep(1)
        pass
    print('found result...')
    return 1 #json.load(open(filepath))

def dispatch_job(tag):
    open(os.path.join(BASE_DIR, 'media/', tag+'.query.done'), 'w').close()
    return loadFromExternalApp(os.path.join(BASE_DIR, 'media/', tag+'.result'))

# HANDLE FILE UPLOAD
@csrf_exempt
def fileupload(request):

    #N = 10
    #tag = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))
    tag = str(uuid.uuid4())
    fname = os.path.join(BASE_DIR, 'media/%s_tmp.jpg' % (tag))
    print('fileupload tag: %s' % (tag))

    response = HttpResponseRedirect(reverse('visiondemo:result'))
    response.set_cookie( 'cookie_tag', tag )


    if request.method == 'POST':
        # FROM DROPZONE UPLOAD
        try:
            print('try UploadFileForm ...')
            form = UploadFileForm(request.POST, request.FILES)
            print(form.is_valid())
            if form.is_valid():
                handle_uploaded_file(request.FILES['file'], fname)
                print('Upload succeeded.')
                dispatch_job(tag)
                return response
        except:
            pass
        # FROM URL TEXT
        try:
            print('URL form...')
            form = URLForm(request.POST)
            print(form)
            if form.is_valid():
                print(form.cleaned_data['myinput'])
                os.system('wget %s -O %s' % (form.cleaned_data['myinput'], fname))
                print('Download succeeded.')
                dispatch_job(tag)
                return response
        except:
            pass

    return Http404("Error")
