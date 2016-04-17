from django.conf import settings
from travelpart.views import search_id
if not settings.configured:
    settings.configure()
import json
import urllib
import simplejson
import googlemaps
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
import requests
from lxml import html
from BeautifulSoup import BeautifulSoup
GOOGLE_API_KEY='AIzaSyCbx8G_jSaL_xs1nHdOPvefocqV7KDQKHo'
#from busutil import *
googleGeocodeUrl = 'http://maps.googleapis.com/maps/api/geocode/json?'
#def calcuatefare(n):
#    if n<=4:
#        return '100'
#    else:
#        return str(100+(13*(n-4)))

def cab(request,lat,lng):
    print("strin1",search_id)
    startlat,startlong=get_coordinates(str(search_id),from_sensor=False)
    print("string",startlat,startlong)
    dstlat,dstlong=float(lat),float(lng)
    url = 'https://api.uber.com/v1/estimates/price'
    parameters = {
        'server_token': 'SYcSQ4z0VKulQ3gXthdbDSw8f1O2qsza7FQrv7kI',
        'start_latitude': startlat,
        'start_longitude': startlong,
        'end_latitude': dstlat,
        'end_longitude':dstlong,
    }
    response = requests.get(url, params=parameters)
    print(response)
    data = response.json()
    print(data)
    return render(request,'cab.html',{'data':data['prices']})


def get_coordinates(query, from_sensor=False):
    query = query.encode('utf-8')
    url = 'https://api.uber.com/v1/estimates/price'
    params = {
        'address': query,
        'sensor': "true" if from_sensor else "false"
    }
    url = googleGeocodeUrl + urllib.urlencode(params)
    json_response = urllib.urlopen(url)
    response = simplejson.loads(json_response.read())
    if response['results']:
        location = response['results'][0]['geometry']['location']
        latitude, longitude = location['lat'], location['lng']
    else:
        latitude, longitude = None, None
        print query, "<no results>"
    return latitude, longitude
