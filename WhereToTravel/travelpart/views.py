
from settings import GOOGLE_API_KEY
from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
# Create your views here.
from googleplaces import GooglePlaces
lass NameForm(forms.Form):
    your_location = forms.CharField(label='Your name', max_length=100)
def getPlaces(location,keyWord,Radius):
	google_places = GooglePlaces(GOOGLE_API_KEY)
	# You may prefer to use the text_search API, instead.
	query_result = google_places.nearby_search(
		location=location, keyword="landmarks",
		radius=500, types=[types.TYPE_place_of_worship,types.TYPE_zoo,types.TYPE_,types.TYPE_natural_feature,types.TYPE_city_hall])

def TravelOutput(request) :
	if(request.method=='POST'):
		if form.is_valid():
			form = NameForm(request.POST)
            		getPlaces(form.your_location)
			
	return render(request, 'name.html', {'form': form})
