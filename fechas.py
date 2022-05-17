from datetime import date, timedelta
import locale

locale.setlocale(locale.LC_ALL, 'es_ES')

def obtenerFechaHoy():
    hoy = date.today().strftime("%A, %d de %B del %Y").capitalize()
    return hoy

def obtenerFechaPasada(rec):
    cuandoTxt = ""
    if 'anteayer' in rec or 'antes de ayer' in rec:
        dias = 2
        cuandoTxt = 'anteayer'
    elif 'ayer' in rec:
        dias = 1
        cuandoTxt = 'ayer'
    else:
        rec = rec.replace("que","").replace("dias","").replace("fue","").replace("hace","").replace('cual', '').replace('la', '').replace('fecha', '')\
            .replace('de', '').replace("dia","").strip()
        dias = int(rec)
    
    if dias != 0:
        try:
            fecha = (date.today() - timedelta(days = dias)).strftime("%A, %d de %B del %Y")

            if cuandoTxt != "":
                return f'{cuandoTxt} fue {fecha}'
            else:
                return f'Hace {dias} días fue {fecha}'
        except Exception as ex:
            return 'No tengo datos de un tiempo tan lejano'
    else:
        return 'No entendí'

def obtenerFechaFutura(rec):
    cuandoTxt = ""
    if 'pasado mañana' in rec:
        cuandoTxt = "pasado mañana"
        dias = 2
    elif 'mañana' in rec:
        cuandoTxt = "mañana"
        dias = 1
    else:
        rec = rec.replace('que', '').replace('dias', '').replace('dia', '').replace('sera', '').replace('dentro de', '').replace('en', '')\
            .replace('es', '').replace('de', '').replace('cual', '').replace('la', '').replace('fecha', '').strip()
        dias = int(rec)

    if dias != 0:
        try:
            fecha = (date.today() + timedelta(days = dias)).strftime("%A, %d de %B del %Y")
            if cuandoTxt != "":
                return f'{cuandoTxt} será {fecha}'
            else:
                return f'Dentro de {dias} días será {fecha}'
        except Exception as ex:
            return 'No sé si en ese futuro seguirá igual el calendario'
    else:
        return 'No entendí'

def obtenerProximoDiaSemana(rec):
    dia = date.today() + timedelta(days = 1)
    buscado = ""
    rec = rec.replace('que', '').replace('el', '').replace('dia', '').replace('sera', '').replace('cuando', '').replace('en', '')\
        .replace(' es ', '').replace('cae', '').replace('proximo', '').strip()
    diasSemana = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo']
    
    if rec in diasSemana:
        buscado = diasSemana.index(rec)

        if buscado == 2:
            rec = 'miércoles'
        elif buscado == 5:
            rec = 'sábado'

        if dia.weekday() == buscado:
            return f'El próximo {rec} es mañana'
        else:
            while dia.weekday() != buscado:

                dia = dia + timedelta(days= 1)
        
            diaStr = dia.strftime("%d de %B del %Y")
            return f'El próximo {rec} será el día {diaStr}'
    else:
        return 'No entendí qué día quieres saber'

print(obtenerProximoDiaSemana('cuando es el proximo sabado'))