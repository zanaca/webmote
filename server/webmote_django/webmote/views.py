from pprint import pprint
from django import forms
from django.forms.models import modelformset_factory
from django.template import RequestContext
from django.http import HttpResponse
from django.core.context_processors import csrf
from django.shortcuts import render_to_response, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import logout_then_login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from webmote_django.webmote.models import *
import serial, sys, os, signal
from django.utils import simplejson
import json


# This allows the javascript locater to find the server
def identification(request):
    if request.method == 'GET':
        response = HttpResponse('webmote model #12345')
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
        response['Access-Control-Max-Age'] = 1000
        response['Access-Control-Allow-Headers'] = '*'
        return response
    else:
        return render_to_response('fail.html')

def help(request):
    return render_to_response('help.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('/')

@login_required
def index(request):
    context = {}
    context['plugins'] = []
    for dirName in os.listdir(MODULES_DIR):
        try:
            json_data = open('/'.join([os.path.abspath(MODULES_DIR), dirName, 'info.json',]))
            data = json.load(json_data)
            context['plugins'].append({'url' : data['url'], 'name' : data['name']})
        except:
            print 'Failed to locate info file for ' + dirName + '!' 
    return render_to_response('index.html', context, context_instance=RequestContext(request))

@login_required
def help(request):
    return render_to_response('help.html', context_instance=RequestContext(request))

@login_required
def runAction(request, id):
    action = Actions.objects.filter(id=int(id))[0]
    action.runAction()
    return HttpResponse(simplejson.dumps(''), mimetype='application/javascript')

@login_required
def transceiverSearch(request, type, port):
    msg = False
    try:
        ser = serial.Serial('/dev/' + port, 9600)
        msg = str(ser.readline()).split('_')[0]
        if not msg in type:
            msg = ''
    except Exception, exc:
        print str(exc)
    return HttpResponse(simplejson.dumps({'deviceType' : msg}), mimetype='application/javascript')

##################
# Helper Functions 
##################

# This is going to be reworked eventually
#def resetAllTransceivers(port):
#    Transceivers.objects.all().delete()
#    try:
#        ser = serial.Serial(port, 9600)
#        ser.write('reset')
#    except Exception, exc:
#        print str(exc)

########################
# Load Modules views.py
########################
sys.path.append(os.path.abspath(MODULES_DIR))
for dirName in os.listdir(MODULES_DIR):
    try:
        __import__(dirName + '.views')
        print 'Loading ' + dirName + ' plugin (views).'
    except:
        print 'Failed to load ' + dirName + ' plugin (views).'
del sys.path[-1]
