import requests
import urllib

api_url = "http://www.mapquestapi.com/directions/v2/route?"
key = "CfVOIJ6Jj0VOt1rCWxrgRdgw4KRv3qCj"
origen = "Fuenlabrada"
destino = "Braga"
# fastest = Más rápida en coche | shortest = Más corta en coche
# pedestrian = Caminando (evita carreteras y solo está disponible para - 320km) | bicycle = Bicicleta 
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