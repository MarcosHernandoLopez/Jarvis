import json,requests,urllib


with open('config.json', 'r') as f:
    data = json.load(f)

base_url = "http://www.mapquestapi.com/directions/v2/route?"
key = data['API_map']


def obtenerCiudadesMapa(texto : str) -> list:
    """
    Retorna una lista con las 2 ciudades dentro del texto pasado como parámetro.
        - Origen  [0]
        - Destino [1]
    """
    ciudades = texto.replace('distancia ', '').replace('kilometros ', '').replace('cuantos ', '').replace('cuanto ', '').replace('entre ', '').replace('dime ', '').replace('como ', '').replace('ruta ', '').replace('camino ', '')\
                        .replace('caminando ', '').replace('andando ', '').replace('a pie ', '')\
                        .replace('bici ', '').replace('bicicleta ', '').replace('pedaleando ', '')\
                        .replace('en coche ', '').replace('conduciendo ', '')\
                        .replace('mas corta ', '').replace('mas corto ', '').replace('mas rapida ', '').replace('mas rapido ', '')\
                        .replace('cual ', '').replace('hay ', '').replace('para ', '').replace('que ', '').replace('desde ', '').replace('es la ', '').replace(' y ', '@').replace(' a ', '@').replace(' e ', '@')\
                        .replace('tiempo ', '').replace('se ', '').replace('tarda ', '').replace('de ', '').replace('es el ', '')\
                        .replace('ir ', '').replace('en ', '').strip().split('@')
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
    elif 'coche' in texto or 'conduciendo' in texto or 'mas rapida' in texto or 'mas rapido' in texto:
        return 'fastest'
    elif 'mas corta' in texto or 'mas corto' in texto:
        return 'shortest'
    else:
        return 'fastest'

def obtenerDatosMapa(ciudades : list, tipoRuta : str) -> str:
    """
    Obtiene el resultado de la búsqueda de las dos direcciones en el mapa.
    """
    origen = ciudades[0]
    destino = ciudades[1]
    url = base_url + urllib.parse.urlencode({"key": key, "from": origen, "to": destino, "locale": 'es_ES', "unit": 'k', "routeType": tipoRuta})
    data = requests.get(url).json()
    print('Url de la búsqueda: ' + url)
    status_code = data['info']['statuscode']
    
    if status_code == 402:
        return 'No es posible localizar una ruta entre esos puntos.'
    elif status_code == 500:
        return 'Error al localizar uno de los puntos.'
    elif status_code == 601:
        if '#1' in data['info']['messages']:
            return 'No es posible trabajar con la segunda localización.'
        elif '#0' in data['info']['messages']:
            return 'No es posible trabajar con la primera localización.'
    elif status_code == 607:
        return 'La distancia a pie es superior a 320 kilómetros.'
    elif status_code == 611:
        return 'Se necesitan dos localizaciones.'
    elif status_code == 0:
        distancia = round(data['route']['distance'], 2)
        tiempoTemp = data['route']['formattedTime'].split(':')

        if int(tiempoTemp[0]) == 0:
            tiempo = tiempoTemp[1] + " minutos"
        else:
            tiempo = tiempoTemp[0] + " horas y " + tiempoTemp[1] + " minutos"

        if tipoRuta == 'fastest':
            return f'Para ir de {origen} a {destino} en coche hay que recorrer una distancia de {distancia} kilómetros y se tarda {tiempo}.'
        elif tipoRuta == 'shortest':
            return f'Para ir de {origen} a {destino} usando la ruta más corta hay que recorrer una distancia de {distancia} kilómetros y se tarda {tiempo}.'
        elif tipoRuta == 'pedestrian':
            return f'Para ir de {origen} a {destino} andando hay que recorrer una distancia de {distancia} kilómetros y se tarda {tiempo}.'
        else:
            return f'Para ir de {origen} a {destino} en bicicleta hay que recorrer una distancia de {distancia} kilómetros y se tarda {tiempo}.'
