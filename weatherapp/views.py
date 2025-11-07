from django.shortcuts import render
from django.contrib import messages
import requests
import datetime

# Create your views here.
def home(request):

    if 'city' in request.POST:
        city = request.POST['city']
    else:
        city = 'Bengaluru'

    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=0ee21de2424d17200507af7ed4df5b60'
    PARAMS = {'units':'metric'}

    API_KEY =  'AIzaSyDPbCnP5DggtUkSQrZbkN6pLhaC1EdvEyI'
    SEARCH_ENGINE_ID = '41ed4c0029ce5407a'
     
    query = city + " 1920x1080"
    page = 1
    start = (page - 1) * 10 + 1
    searchType = 'image'
    city_url = f'https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}&searchType={searchType}&imgSize=xlarge'

    data = requests.get(city_url).json()
    count = 1
    search_items = data.get("items")
    image_url = search_items[1]['link']


    try :
        data = requests.get(url,PARAMS).json()
        description = data['weather'][0]['description']
        icon = data['weather'][0]['icon']
        temp = data['main']['temp']
        pressure = data['main']['pressure']
        humidity = data['main']['humidity']
        wind = data['wind']['speed']
        day = datetime.date.today()
        return render(request,'index.html',{'description':description,'icon':icon,'temp':temp,'day':day,'city':city,'humidity':humidity,'pressure':pressure,'wind':wind,'exception_occured':False,'image_url':image_url})
    
    except :
        exception_occured=True
        messages.error(request,'Entered city is incorrect')
        day=datetime.date.today()


        return render(request,'index.html',{'description':'clear sky','icon':'01d','temp':25,'day':day,'city':'Bengaluru','humidity':50,'pressure':1005,'wind':2.5,'exception_occured':True})


