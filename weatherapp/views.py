from django.shortcuts import render
from django.contrib import messages
import requests
import datetime

def home(request):

    if 'city' in request.POST:
        city = request.POST['city']
    else:
        city = 'Bengaluru'

    # OpenWeather API
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=0ee21de2424d17200507af7ed4df5b60'
    PARAMS = {'units': 'metric'}

    # Google Image API
    API_KEY = 'AIzaSyDPbCnP5DggtUkSQrZbkN6pLhaC1EdvEyI'
    SEARCH_ENGINE_ID = '41ed4c0029ce5407a'

    query = city + " 1920x1080"
    page = 1
    start = (page - 1) * 10 + 1
    searchType = 'image'

    city_url = f'https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}&searchType={searchType}&imgSize=xlarge'

    data = requests.get(city_url).json()
    search_items = data.get("items")

    image_url = search_items[1]['link']

    try:

        data = requests.get(url, PARAMS).json()

        description = data['weather'][0]['description']
        icon = data['weather'][0]['icon']
        temp = data['main']['temp']
        pressure = data['main']['pressure']
        humidity = data['main']['humidity']
        wind = data['wind']['speed']

        # NEW FEATURES (safe additions)

        feels_like = data['main']['feels_like']
        wind_direction = data['wind']['deg']

        sunrise = datetime.datetime.fromtimestamp(
            data['sys']['sunrise']
        ).strftime('%H:%M')

        sunset = datetime.datetime.fromtimestamp(
            data['sys']['sunset']
        ).strftime('%H:%M')

        day = datetime.date.today()

        # 5 day forecast API
        forecast_url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid=0ee21de2424d17200507af7ed4df5b60&units=metric'
        forecast_data = requests.get(forecast_url).json()

        forecast_list = []

        for i in forecast_data['list'][0:5]:
            forecast = {
                'temp': i['main']['temp'],
                'icon': i['weather'][0]['icon'],
                'day': datetime.datetime.fromtimestamp(
                    i['dt']
                ).strftime('%A')
            }
            forecast_list.append(forecast)

        return render(request, 'index.html', {
            'description': description,
            'icon': icon,
            'temp': temp,
            'day': day,
            'city': city,
            'humidity': humidity,
            'pressure': pressure,
            'wind': wind,
            'feels_like': feels_like,
            'wind_direction': wind_direction,
            'sunrise': sunrise,
            'sunset': sunset,
            'forecast': forecast_list,
            'exception_occured': False,
            'image_url': image_url
        })

    except:

        exception_occured = True
        messages.error(request, 'Entered city is incorrect')
        day = datetime.date.today()

        return render(request, 'index.html', {
            'description': 'clear sky',
            'icon': '01d',
            'temp': 25,
            'day': day,
            'city': 'Bengaluru',
            'humidity': 50,
            'pressure': 1005,
            'wind': 2.5,
            'feels_like': 25,
            'wind_direction': 0,
            'sunrise': '06:00',
            'sunset': '18:30',
            'forecast': [],
            'exception_occured': True
        })