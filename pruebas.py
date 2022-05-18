from datetime import datetime

def obtenerFecha(texto):
    try:
        listaMeses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
        for mes in listaMeses:
            if mes in texto:
                texto = texto.replace(mes, str(listaMeses.index(mes) + 1))

        texto = texto.replace(" a las ", " de ").replace(" del ", " de ").split(" de ")

        if len(texto[1]) == 1:
            texto[1] = "0" + texto[1]

        if len(texto) < 4:
            texto.append("00:00")
        elif len(texto) > 4:
            for i in range(4, len(texto) - 1, 1):
                texto.remove(texto[i])

        fechaStr = texto[2] + "-" + texto[1] + "-" + texto[0] + " " + texto[3]
        fecha = datetime.fromisoformat(fechaStr).isoformat(timespec='minutes')
        return fecha
    except Exception as ex:
        print('Error: ' + str(ex))
        return None



f1 = obtenerFecha('28 de octubre de 2002 a las 19:00')
f2 = obtenerFecha('18 de enero del 2022 a las 13:00 a las qwe a las asd')

print(f1)
print(f2)

