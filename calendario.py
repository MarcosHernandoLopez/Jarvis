from datetime import datetime, timedelta
from setupCalendario import obtenerServicioCalendario

service = obtenerServicioCalendario()


def crearEvento(titulo : str, desc : str, inicio : str, final : str) -> str:
    """
    Comprueba que la fecha de inicio sea anterior a la de final y si es correcto crea un evento.
    """
    if inicio > final:
        return 'La fecha de inicio no puede ser más lejana que la de fin.'
    
    else:
        try:
            # Crea el evento
            event = service.events().insert(calendarId='primary', body={
                "summary": titulo.capitalize(),
                "description": desc,
                "start": {"dateTime": inicio, "timeZone": "Europe/Madrid"},
                "end": {"dateTime": final, "timeZone": "Europe/Madrid"}
            }).execute()

            print ('Event created: %s' % (event.get('htmlLink'))) # Solo para debug
            return 'Evento creado'
        except Exception as ex:
            print('Error: ' + str(ex)) # Solo para debug
            return 'Hubo un error al crear el evento, inténtelo de nuevo.'

def obtenerEventos() -> list | None:
    """
    Obtiene todos los eventos y los separa en:
        - Eventos de hoy [0].
        - Eventos de esta semana [1].
        - Todos los eventos [2].
    """
    eventosHoy = []
    eventosEstaSemana = []
    eventosTodos = []
    page_token = None

    try:
        while True:
            events = service.events().list(calendarId = 'primary', pageToken = page_token).execute()
            for event in events['items']:
                eventosTodos.append(event)
                inicioEvento = datetime.strptime(event['start']['dateTime'].split('T')[0], '%Y-%m-%d').date()

                if inicioEvento == datetime.today().date():
                    eventosHoy.append(event)

                if inicioEvento >= datetime.today().date() and inicioEvento <= datetime.today().date() + timedelta(days = 6 - datetime.today().weekday()):
                    eventosEstaSemana.append(event)

            if not page_token:
                break
        return eventosHoy, eventosEstaSemana, eventosTodos
    except Exception as ex:
        print('Error: ' + str(ex))
        return None

def eliminarEvento(idEvento : str) -> str:
    """
    Borra el evento cuyo ID coincide con el pasado como parámetro.
    """
    try:
        service.events().delete(calendarId = 'primary', eventId = idEvento).execute()
        return 'Evento eliminado correctamente'

    except Exception as ex:
        print('Error: ' + str(ex))
        return 'Hubo un problema al eliminar el evento.'

def eventoExiste(listaEventos : list, tituloEvento : str) -> str:
    """
    Comprueba que en la lista de eventos pasada haya alguno con el título pasado como parámetro
    """
    for evento in listaEventos:
        if evento['summary'].lower() == tituloEvento.lower():
            return evento

def extraerTiemposEvento(evento) -> str:
    """
    Obtiene la hora y minuto de inicio y final del evento pasado por parámetro.
    - Inicio [0]
    - Final  [1]
    """
    # Tiempo de inicio
    tiempoInicio = evento['start']['dateTime'].split('T')[1].split(':')
    if tiempoInicio[1] == '15':
        inicio = tiempoInicio[0] + " y cuarto"
    elif tiempoInicio[1] == '30':
        inicio = tiempoInicio[0] + " y media"
    elif tiempoInicio[1] == '45':
        inicio = tiempoInicio[0] + " y tres cuartos"
    else:
        inicio = tiempoInicio[0] + ":" + tiempoInicio[1]
    # Tiempo de final
    tiempoFinal = evento['end']['dateTime'].split('T')[1].split(':')
    if tiempoFinal[1] == '15':
        final = tiempoFinal[0] + " y cuarto"
    elif tiempoFinal[1] == '30':
        final = tiempoFinal[0] + " y media"
    elif tiempoFinal[1] == '45':
        final = tiempoFinal[0] + " y tres cuartos"
    else:
        final = tiempoFinal[0] + ":" + tiempoFinal[1]

    return inicio, final

def extraerFechaEvento(evento) -> str:
    """
    Extrae el mes y el día del evento pasado como parámetro.
    - Inicio [0]
    - Final  [1]
    """
    # Dia de inicio
    diaInicio = evento['start']['dateTime'].split('T')[0].split('-')
    listaMeses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
    mes = listaMeses[int(diaInicio[1]) - 1]
    inicio = diaInicio[2] + " de " + mes
    # Dia de fin
    diaFinal = evento['end']['dateTime'].split('T')[0].split('-')
    listaMeses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
    mes = listaMeses[int(diaFinal[1]) - 1]
    final = diaFinal[2] + " de " + mes

    return inicio, final
