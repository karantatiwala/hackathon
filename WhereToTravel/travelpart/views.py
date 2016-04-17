from django import forms
from django.shortcuts import render
import json
import urllib
import simplejson
import googlemaps

from django.http import HttpResponseRedirect
# Create your views here.
from googleplaces import GooglePlaces,types,lang
places={}
GOOGLE_API_KEY='AIzaSyCbx8G_jSaL_xs1nHdOPvefocqV7KDQKHo'

import urllib, json
googleGeocodeUrl = 'http://maps.googleapis.com/maps/api/geocode/json?'

#Grabbing and parsing the JSON data
def GoogPlac(lat,lng,radius,types,key):
  #making the url
  AUTH_KEY = key
  LOCATION = str(lat) + "," + str(lng)
  RADIUS = radius
  TYPES = types
  MyUrl = ('https://maps.googleapis.com/maps/api/place/nearbysearch/json'
           '?location=%s'
           '&radius=%s'
           '&types=%s'
           '&sensor=false&key=%s') % (LOCATION, RADIUS, TYPES, AUTH_KEY)
  #grabbing the JSON result
  print(MyUrl)
  response = urllib.urlopen(MyUrl)
  jsonRaw = response.read()
  jsonData = simplejson.loads(jsonRaw)
  return jsonData



def getPlaces(Location):
	
	google_places = GooglePlaces(GOOGLE_API_KEY)
	query_result = google_places.nearby_search(location=str(Location), keyword="landmarks",radius=20000, types=[types.TYPE_FOOD])#types.TYPE_zoo,types.TYPE_natural_feature,types.TYPE_city_hall])		
	return query_result
def TravelOutput(request) :
	if (request.method == 'POST'):
		context=[]
		search_id = request.POST.get('textfield', None)
		startlon,startlat=get_coordinates(search_id, from_sensor=False)
		
		places=GoogPlac(startlon,startlat, 20000,'landmarks',' AIzaSyCbx8G_jSaL_xs1nHdOPvefocqV7KDQKHo')		
		print(places['results'][1])
		for i in places['results']:
			context.append({'name':i[u'name'],'address':i[u'vicinity'],'geolat':i[u'geometry'][u'location'][u'lat'],'geolng':i[u'geometry'][u'location'][u'lng'],'search':search_id})	
			
		return render(request, 'detail.html', {'context':context})
def output(request):
	return render(request, 'index.html', {})

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
