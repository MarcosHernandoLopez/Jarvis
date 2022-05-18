from datetime import datetime


listaMeses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
texto = "28 del 10 de 2002 a las 12:00"

for mes in listaMeses:
    if mes in texto:
        texto = texto.replace(mes, str(listaMeses.index(mes) + 1))

texto = texto.replace(" a las ", " de ").replace(" del ", " de ").split(" de ")

if len(texto[1]) ==0:
    texto[1] = "0" + texto[1]

fechaStr = texto[2] + "-" + texto[1] + "-" + texto[0] + " " + texto[3]
fecha = datetime.fromisoformat(fechaStr).replace(microsecond=0).isoformat()
print("Fecha str: " + fechaStr)
print('Fecha: ' + str(fecha))
