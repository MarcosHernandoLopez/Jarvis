import json, requests, geocoder
from googletrans import Translator
from fechas import *

with open('config.json', 'r') as f:
    data = json.load(f)

API_key = data['API_weather']

def coordenadas(ciudad : str) -> list:
    """
    Obtiene la latitud y la longitud de la ciudad pasada como parámetro.
    """
    url = f'http://api.openweathermap.org/geo/1.0/direct?q={ciudad}&limit=1&appid={API_key}'

    response = requests.get(url)
    response.raise_for_status()

    location = json.loads(response.text)[0]
    
    lat = location['lat']
    lon = location['lon']
    return lat, lon

def obtenerCiudadClima(texto: str, cuando : str) -> str:
    """
    Obtiene la ciudad del texto para ver el clima, pone la primera letra en mayúsculas y la retorna.
    """
    traductor = Translator()
    ciudad = texto.replace('dime el clima de ', '').replace('dime el clima en ', '')
    ciudad = texto.replace('dime el tiempo de ', '').replace('dime el tiempo en ', '')
    ciudad = ciudad.replace(' de ', '').replace(' en ', '')
    ciudad = ciudad.replace(cuando, '')
    if ciudad == "":
        ciudad = geocoder.ip('me').city
    ciudad = ciudad.title()
    ciudadEs = traductor.translate(ciudad, dest='es').text

    if ciudadEs == 'Puerto':
        ciudadEs = 'O Porto'

    return ciudadEs

def climasDe(lat : float, lon : float) -> dict:
    """
    Obtiene el clima de los próximos 7 días de la localización con la longitud y latitud pasadas como parámetro.
    """
    url = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=hourly,alerts,minutely,current&appid={API_key}&units=metric&lang=es'

    response = requests.get(url)
    response.raise_for_status()

    weather = json.loads(response.text)

    return weather

def clima(cuando : str, climas : dict) -> str:
    """
    Retorna un texto con la temperatura mínima, máxima, el estado del cielo y la probabilidad de precipitaciones de hoy, mañana o pasado mañana. 
    """
    if cuando == "hoy":
        dia = climas['daily'][0]
        return('Hoy hay una mínima de ' + str(round(dia['temp']['min'], 1)) + ' grados y una máxima de ' + str(round(dia['temp']['max'], 1)) + ' grados, ' + str(dia['weather'][0]['description'])\
            + ' y una probabilidad de precipitaciones del ' + str(int((dia['pop'] * 100))) + '%')
    elif cuando == 'mañana':
        dia = climas['daily'][1]
        return('Mañana habrá una mínima de ' + str(round(dia['temp']['min'], 1)) + ' grados y una máxima de ' + str(round(dia['temp']['max'], 1)) + ' grados, ' + str(dia['weather'][0]['description'])\
            + ' y una probabilidad de precipitaciones del ' + str(int((dia['pop'] * 100))) + '%')
    elif cuando == 'pasado mañana':
        dia = climas['daily'][2]
        return('Pasado mañana habrá una mínima de ' + str(round(dia['temp']['min'], 1)) + ' grados y una máxima de ' + str(round(dia['temp']['max'], 1)) + ' grados, ' + str(dia['weather'][0]['description'])\
            + ' y una probabilidad de precipitaciones del ' + str(int((dia['pop'] * 100))) + '%')

def obtenerClima(ciudad : str, cuando : str) -> str :
    """
    Obtiene y retorna el clima de la ciudad pasada como parámetro en el momento pasado como parámetro (hoy, mañana o pasado mañana).
    """
    coords = coordenadas(ciudad)
    climas = climasDe(coords[0], coords[1])
    return clima(cuando, climas)

