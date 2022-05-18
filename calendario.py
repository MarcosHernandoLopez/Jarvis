from datetime import datetime, timedelta
from setupCalendario import obtenerServicioCalendario

service = obtenerServicioCalendario()


def crearEvento(titulo, desc, inicio, final):
    try:
        event = service.events().insert(calendarId='primary', body={
            "summary": titulo,
            "description": desc,
            "start": {"dateTime": inicio, "timeZone": "Europe/Madrid"},
            "end": {"dateTime": final, "timeZone": "Europe/Madrid"}
        }).execute()
        print ('Event created: %s' % (event.get('htmlLink')))
        return('Evento creado')
    except Exception as ex:
        print('Error: ' + str(ex))
        return('Hubo un error al crear el evento, inténtelo de nuevo.')