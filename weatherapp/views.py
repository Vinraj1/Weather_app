from django.shortcuts import render
from django.contrib import messages
import requests
import datetime


def home(request):

    if 'city' in request.POST:
        city = request.POST['city']
    else:
        city = 'Bengaluru'

    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=0ee21de2424d17200507af7ed4df5b60'
    forecast_url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid=0ee21de2424d17200507af7ed4df5b60'

    PARAMS = {'units': 'metric'}

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
        feels_like = data['main']['feels_like']

        pressure = data['main']['pressure']
        humidity = data['main']['humidity']

        wind = data['wind']['speed']
        wind_direction = data['wind']['deg']

        sunrise = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset = datetime.datetime.fromtimestamp(data['sys']['sunset'])

        day = datetime.date.today()

        # ---------- 5 DAY FORECAST ----------

        forecast_data = requests.get(forecast_url, PARAMS).json()

        forecast_list = []

        for item in forecast_data['list'][::8]:
            forecast_list.append({
                "day": datetime.datetime.fromtimestamp(item['dt']).strftime('%A'),
                "temp": item['main']['temp'],
                "icon": item['weather'][0]['icon'],
                "description": item['weather'][0]['description']
            })

        return render(request, 'index.html', {
            'description': description,
            'icon': icon,
            'temp': temp,
            'feels_like': feels_like,
            'day': day,
            'city': city,
            'humidity': humidity,
            'pressure': pressure,
            'wind': wind,
            'wind_direction': wind_direction,
            'sunrise': sunrise.strftime("%H:%M"),
            'sunset': sunset.strftime("%H:%M"),
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
            'feels_like': 25,
            'day': day,
            'city': 'Bengaluru',
            'humidity': 50,
            'pressure': 1005,
            'wind': 2.5,
            'wind_direction': 0,
            'sunrise': '06:00',
            'sunset': '18:00',
            'forecast': [],
            'exception_occured': True
        })