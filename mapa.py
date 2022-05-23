import requests
import urllib

api_url = "http://www.mapquestapi.com/directions/v2/route?"
key = "CfVOIJ6Jj0VOt1rCWxrgRdgw4KRv3qCj"


def obtenerCiudadesMapa(texto : str) -> list:
    """
    Retorna una lista con las 2 ciudades dentro del texto pasado como parámetro.
        - Origen  [0]
        - Destino [1]
    """
    ciudades = texto.replace('distancia ', '').replace('kilometros ', '').replace('cuantos ', '').replace('cuanto ', '').replace('entre ', '').replace('dime ', '').replace('como ', '')\
                        .replace('cual ', '').replace('hay ', '').replace('que ', '').replace('desde ', '').replace('es la ', '').replace(' y ', '@').replace(' a ', '@').replace(' e ', '@')\
                        .replace('tiempo ', '').replace('se ', '').replace('tarda ', '').replace('de ', '')\
                        .replace('ir ', '').replace('en ', '').split('@')
    return ciudades

def obtenerTipoRuta(texto : str) -> str:
    """
    Obtiene el tipo de ruta del texto.
    - pedestrian = A pie
    - bicycle = En bicicleta
    - fastest = En coche
    - shortest = La ruta más corta
    """
    if 'caminando' in texto or 'andando' in texto or 'a pie' in texto:
        return 'pedestrian'
    elif 'bicicleta' in texto or 'bici' in texto or 'pedaleando' in texto:
        return 'bicycle'
    elif 'en coche' in texto or 'conduciendo' in texto:
        return 'fastest'
    elif 'mas corta' in texto:
        return 'shortest'
    else:
        return 'Necesito saber cómo quieres ir.'

def obtenerDatosMapa(ciudades : list, tipoRuta : str) -> str:
    """
    Obtiene el resultado de la búsqueda de las dos direcciones en el mapa.
    """
    origen = ciudades[0]
    destino = ciudades[1]
    url = api_url + urllib.parse.urlencode({"key": key, "from": origen, "to": destino, "locale": 'es_ES', "unit": 'k', "routeType": tipoRuta})
    data = requests.get(url).json
    print('Url de la búsqueda: ' + url)
    statuscode = data['info']['statuscode']
    
    if statuscode == 402:
        return 'No es posible localizar una ruta entre esos puntos.'
    elif statuscode == 500:
        return 'Error al localizar uno de los puntos.'
    elif statuscode == 601:
        if '#1' in data['info']['messages']:
            return 'No es posible trabajar con la segunda localización.'
        elif '#0' in data['info']['messages']:
            return 'No es posible trabajar con la primera localización.'
    elif statuscode == 607:
        return 'La distancia a pie es superior a 320 kilómetros.'
    elif statuscode == 611:
        return 'Se necesitan dos localizaciones.'
    elif statuscode == 0:
        distancia = data['route']['distance']
        tiempoTemp = data['route']['formattedTime'].split(':')
        tiempo = tiempoTemp[0] + " horas y " + tiempoTemp[1] + " minutos"
        if tipoRuta == 'fastest':
            return 'Para ir de {origen} a {destino} en coche hay que recorrer una distancia de {distancia} kilómetros y se tarda {tiempo}.'
        elif tipoRuta == 'shortest':
            return 'La ruta más corta para ir de {origen} a {destino} hay que recorrer una distancia de {distancia} kilómetros y se tarda {tiempo}.'
        elif tipoRuta == 'pedestrian':
            return 'Para ir de {origen} a {destino} andando hay que recorrer una distancia de {distancia} kilómetros y se tarda {tiempo}.'
        else:
            return 'Para ir de {origen} a {destino} en bicicleta hay que recorrer una distancia de {distancia} kilómetros y se tarda {tiempo}.'

def temp():
    #PARA EL MAPA
    texto = "cual es la distancia entre ciudad de buenos aires y entrepinos"
    texto2 = "cuanto tiempo se tarda de ir desde ciudad de buenos aires a entrepinos"

    # Mapa distancia
    texto2 = texto2.replace('distancia ', '').replace('kilometros ', '').replace('cuantos ', '').replace('cuanto ', '').replace('entre ', '')\
            .replace('cual ', '').replace('hay ', '').replace('que ', '').replace('desde ', '').replace('es la ', '').replace(' y ', '@').replace(' a ', '@').replace(' e ', '@')\
            .replace('tiempo ', '').replace('se ', '').replace('tarda ', '').replace('de ', '')\
            .replace('ir ', '').replace('en ', '')

    texto2 = texto2.split('@')

    print(texto2)




origen = "Braga"
destino = "Fuenlabrada"
# fastest = Más rápida en coche | shortest = Más corta en coche
# pedestrian = Caminando (evita carreteras y solo está disponible para - 320km) statuscode = 607 | bicycle = Bicicleta 
tipoRuta = "fastest"

distanciaRecorrida = 0

url = api_url + urllib.parse.urlencode({"key": key, "from": origen, "to": destino, 'locale': 'es_ES', 'unit': 'k', 'routeType': tipoRuta})
data = requests.get(url).json()
status_code = data['info']['statuscode']
print(url)

if status_code == 0:
    duracion = data['route']['formattedTime']
    distanciaTotal = round(data['route']['distance'], 2)

    print(f'---------- Viaje desde {origen} hasta {destino} ----------')
    print(f'Distancia recorrida: {str(distanciaTotal)}')
    print(f'Duración del viaje en coche: {duracion}')
    print('----------------------------------------------------------')
    print('Indicaciones: ')
    for maniobra in data['route']['legs'][0]['maneuvers']:
        distanciaRecorrida = distanciaRecorrida + round(maniobra['distance'], 2)
        distanciaRestante = distanciaTotal - distanciaRecorrida

        if distanciaRestante < 0:
            distanciaRestante = 0

        print(maniobra['narrative'] + f'    ({round(distanciaRestante, 2)} Km restantes)')

print(obtenerCiudadesMapa('cual tiempo se tarda de ir desde ciudad de buenos aires a entrepinos'))



