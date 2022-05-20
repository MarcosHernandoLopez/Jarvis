import requests
import urllib

api_url = "http://www.mapquestapi.com/directions/v2/route?"
key = "CfVOIJ6Jj0VOt1rCWxrgRdgw4KRv3qCj"
origen = "Fuenlabrada"
destino = "Braga"
# fastest = Más rápida en coche | shortest = Más corta en coche
# pedestrian = Caminando (evita carreteras y solo está disponible para - 320km) statuscode = 607 | bicycle = Bicicleta 
tipoRuta = "fastest"

distanciaRecorrida = 0

def obtenerCiudadesMapa(texto : str) -> list:
    """
    Retorna una lista con las 2 ciudades dentro del texto pasado como parámetro.
        - Origen  [0]
        - Destino [1]
    """
    ciudades = texto.replace('distancia ', '').replace('kilometros ', '').replace('cuantos ', '').replace('cuanto ', '').replace('entre ', '')\
                        .replace('cual ', '').replace('hay ', '').replace('que ', '').replace('desde ', '').replace('es la ', '').replace(' y ', '@').replace(' a ', '@').replace(' e ', '@')\
                        .replace('tiempo ', '').replace('se ', '').replace('tarda ', '').replace('de ', '')\
                        .replace('ir ', '').replace('en ', '').split('@')
    return ciudades

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
    # print('Indicaciones: ')
    # for maniobra in data['route']['legs'][0]['maneuvers']:
    #     distanciaRecorrida = distanciaRecorrida + round(maniobra['distance'], 2)
    #     distanciaRestante = distanciaTotal - distanciaRecorrida

    #     if distanciaRestante < 0:
    #         distanciaRestante = 0

    #     print(maniobra['narrative'] + f'    ({round(distanciaRestante, 2)} Km restantes)')

print(obtenerCiudadesMapa('cual tiempo se tarda de ir desde ciudad de buenos aires a entrepinos'))