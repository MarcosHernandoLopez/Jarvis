


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

