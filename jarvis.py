from datetime import datetime
from googlesearch import search
from calendario import *
from clima import *
from fechas import *
from conversorDivisas import *
from mapa import *
import socket, os, webbrowser,pyttsx3, speech_recognition as sr, pywhatkit, wikipedia, random, json

# Configuración
def config() -> dict:
    """
    Lee el fichero JSON y guarda su contenido en un diccionario que será retornado.
    """
    f = open('config.json')
    data = json.load(f)
    f.close()
    return data

wikipedia.set_lang('es')
engine = pyttsx3.init()
voices = engine.getProperty('voices')
volumen = engine.getProperty('volume')
engine.setProperty('voice', voices[2].id)
engine.setProperty('rate', 160)
data = config()
nombre = "jarvis"

# Métodos
def talk(texto : str):
    """
    Dice el mensaje pasado como parámetro.
    """
    engine.say(texto)
    engine.runAndWait()
    if engine._inLoop:
        engine.endLoop()

def listen() -> str:
    """
    Escucha el audio y retorna el texto de este.
    """

    listener = sr.Recognizer()
    with sr.Microphone() as source:
        print("Escuchando...")
        listener.adjust_for_ambient_noise(source, duration=1)
        listener.pause_threshold = 0.8
        audio = listener.listen(source)
        rec = ""
        try:
            rec = listener.recognize_google(audio, language='es-ES').lower()
        except sr.UnknownValueError:
            pass
        except sr.RequestError as e:
            print(f'No se pudo obtener respuesta del servicio de Google Speech Recognition: {e}')

    return rec.lower()

def comando() -> list:
    """
    Crea la escucha de los comandos de voz. Retorna el comando y si se ha dicho la palabra de activación.
    """
    estado = False
    rec = listen()
    try:
        rec = rec.replace('yarbiss', 'jarvis').replace('yarbis', 'jarvis')
        if nombre in rec:
            rec = rec.replace(nombre, "")
            rec = eliminarTildes(rec).strip()
            estado = True
    except:
        pass
    return rec, estado

def eliminarNotasWikipedia(texto : str) -> str:
    """
    Elimina los [Nota N] del texto pasado por parámetro por el asistente.
    """
    sinNotas = ""
    corchete = False

    for i in range(len(texto)):
        if texto[i] == '[':
            corchete = True
        elif texto[i] == ']':
            corchete = False

        if not corchete:
            sinNotas = sinNotas + texto[i]

    sinNotas = sinNotas.replace(']', '')
    return sinNotas

def eliminarTildes(texto : str) -> str:
    """
    Elimina las tildes del texto.
    """
    return texto.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u").replace("à", "a").replace("è", "e").replace("ì", "i").replace("ò", "o").replace("ù", "u")

def cambiarNombre(nombre : str, data : json):
    """
    Cambia el apartado 'master' de config.json al nombre dicho.
    """
    with open('config.json', 'w') as f:
        
        data['master'] = nombre
        json.dump(data, f)

def URLBusquedaAmazon(texto: str) -> str:
    """
    Retorna la url de una búsqueda de Amazon.
    """
    urls = []
    busqueda = texto + " amazon"
    resultados = search(busqueda, lang="es", num_results=1)
    for r in resultados:
        urls.append(r)
    return urls[0]

def obtenerTitulo() -> str:
    """
    Obtiene el título del evento.
    """
    talk('Dime el título del evento')
    titulo = listen()
    return titulo

def obtenerDesc() -> str:
    """
    Obtiene la descripción de un evento.
    """
    talk('Dime la descripción del evento')
    desc = listen()
    print(desc)
    return desc

def obtenerFecha(rec) -> str | None:
    """
    Extrae la fecha del texto pasado como parámetro.
    """
    try:

        if 'hoy' in rec:
            hoy = datetime.today().isoformat(timespec='minutes')
            return hoy

        listaMeses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
        for mes in listaMeses:
            if mes in rec:
                rec = rec.replace(mes, str(listaMeses.index(mes) + 1))

        rec = rec.replace("a las", " de ").replace("del", " de ").replace("el", "").replace(" ", "").split("de")

        if len(rec[1]) == 1:
            rec[1] = "0" + rec[1]

        if len(rec) < 4:
            rec.append("00:00")
        elif len(rec) > 4:
            for i in range(4, len(rec) - 1, 1):
                rec.remove(rec[i])

        fechaStr = rec[2] + "-" + rec[1] + "-" + rec[0] + " " + rec[3]
        fecha = datetime.fromisoformat(fechaStr).isoformat(timespec='seconds')
        return fecha
    except Exception as ex:
        print('Error: ' + str(ex))
        return None

def obtenerInicio() -> str | None:
    """
    Retorna la fecha de inicio del evento
    """
    talk('Dime cuándo empieza el evento')
    texto = listen()
    print('Texto: ' + texto)
    fInicio = obtenerFecha(texto)
    print('fInicio: ' + str(fInicio))
    return fInicio

def obtenerFinal() -> str | None:
    """
    Retorna la fecha del final del evento.
    """
    talk('Dime cuándo termina el evento')
    texto = listen()
    print('Texto: ' + texto)
    fFinal = obtenerFecha(texto)
    print('fFinal: ' + str(fFinal))
    return fFinal

def main():
    """
    Llama al método 'escucha()' y dependiendo de los valores retornados ejecuta un comando de voz (ninguno si estado == False o si no se tiene ese comando).
    """
    valores = comando()
    rec = valores[0]
    estado = valores[1]
    print("-----------------DEBUG-----------------")
    print("Comando: " + rec + "     Palabra clave: " + str(estado))
    print("---------------------------------------")
    if estado:
            try:
                # Cuenta un chiste de la lista
                if "cuentame un chiste" in rec:
                    chistes = ["Mamá, mamá, los spaghetti se están pegando. Déjalos que se maten",
                                "Soy Rosa. Ah, perdóname, es que soy daltónico.",
                                "Mi ordenador me gana al ajedrez, pero yo le gano boxeando.",
                                "Pues sí, el viaje a la India me cambió la vida. ¿Más langosta señor?. Pero ponle curry.",
                                "Doctor, un ciego quiere verlo. Dígale que yo no hago milagros.",
                                "¿Por qué Jaimito va con traje y corbata al oculista? Porque va a la graduación de sus gafas."]
                    talk(random.choice(chistes))

                # Reproduce un video en YouTube
                elif 'reproduce' in rec:
                    music = rec.replace('reproduce', '')
                    talk('Reproduciendo ' + music)
                    pywhatkit.playonyt(music)

                # Dice la hora actual
                elif 'que hora es' in rec:
                    hora = datetime.now().strftime('%H:%M')
                    talk("Son las " + hora)

                # Busca en Google, en Wikipedia o en Amazon
                elif 'busca' in rec:
                    if 'en google' in rec:
                        order = rec.replace('en google', '').replace('busca', '')
                        resultado = pywhatkit.search(order)
                        talk('Buscando ' + order + " en Google")

                    elif 'en wikipedia' in rec:
                        order = rec.replace('en wikipedia', '').replace('busca', '')
                        resultado = wikipedia.summary(order, 2)
                        mensaje = eliminarNotasWikipedia(resultado)
                        talk(mensaje)
                    
                    elif 'en amazon' in rec:
                        order = rec.replace('en amazon', '').replace('busca', '')
                        resultado = URLBusquedaAmazon(order)
                        webbrowser.open(resultado)
                    else:
                        talk('Necesito que me digas dónde buscar')

                # Cambiar nombre de saludo
                elif 'llamame' in rec:
                    nombre = rec.replace('llamame', '').lstrip()
                    cambiarNombre(nombre.capitalize(), data)
                    talk('Vale, a partir de ahora te llamaré ' + nombre.capitalize())

                #Te dice el nombre registrado en la configuración
                elif 'cual es mi nombre' in rec:
                    nombre = data['master']
                    talk("Tu nombre es " + nombre)

                #Abre YouTube, la calculadora, el explorador de ficheros
                elif 'abre' in rec:
                    if 'youtube' in rec:
                        talk("Abriendo YouTube")
                        webbrowser.open("https://www.youtube.com/")
                    elif 'calculadora' in rec:
                        talk("Abriendo la calculadora")
                        os.system("calc")
                    elif 'explorador de ficheros' in rec or 'explorador de archivos' in rec:
                        talk("Abriendo el explorador de ficheros")
                        os.system("explorer")

                # Hace una captura de pantalla
                elif 'captura de pantalla' in rec:
                    pywhatkit.take_screenshot("Captura Jarvis")

                # Inicia el control remoto
                elif 'control remoto' in rec:
                    ip = socket.gethostbyname(socket.gethostname())
                    print('Conectarse en el móvil a: ' + str(ip) + ":8000")
                    talk('Iniciando el control remoto')
                    pywhatkit.start_server()
                
                # Trabajo sobre Google Calendar
                elif 'evento' in rec:
                    # Nuevo evento
                    if 'crea' in rec or 'nuevo' in rec or 'añade' in rec:
                        titulo, desc, inicio, final = obtenerTitulo(), obtenerDesc(), obtenerInicio(), obtenerFinal()
                        if inicio is None:
                            talk('No entendí la fecha de inicio del evento.')
                        elif final is None:
                            talk('No entendí la fecha de fin del evento.')
                        else:
                            talk(crearEvento(titulo, desc, inicio, final))
                    # Dice tus eventos 
                    elif 'cuales' in rec or 'dime' in rec or 'que eventos' in rec:
                        # Eventos de hoy
                        if 'hoy' in rec:
                            eventosHoy = obtenerEventos()[0]
                            if len(eventosHoy) == 0:
                                talk('No tienes ningún evento hoy.')
                            else: 
                                talk('Estos son tus eventos de hoy:')
                                for evento in eventosHoy:
                                    titulo = evento['summary']
                                    fInicio = extraerFechaEvento(evento)[0]
                                    fFinal = extraerFechaEvento(evento)[1]
                                    inicio = extraerTiemposEvento(evento)[0]
                                    final = extraerTiemposEvento(evento)[1]

                                    if fInicio == fFinal:
                                        talk(f'De {inicio} a {final}: {titulo}')
                                    else:
                                        talk(f'De {inicio} a las {final} del {fFinal}: {titulo}')
                        # Eventos de esta semana
                        elif 'semana' in rec:
                            eventosEstaSemana = obtenerEventos()[1]
                            if len(eventosEstaSemana) == 0:
                                talk('No tienes ningún evento en lo que queda de semana.')
                            else:
                                talk('Estos son tus eventos de lo que queda de semana:')
                                for evento in eventosEstaSemana:
                                    titulo = evento['summary']
                                    fInicio = extraerFechaEvento(evento)[0]
                                    fFinal = extraerFechaEvento(evento)[1]
                                    inicio = extraerTiemposEvento(evento)[0]
                                    final = extraerTiemposEvento(evento)[1]
                                    talk(f'De {inicio} del {fInicio} a las {final} del {fFinal}: {titulo}')
                        # Todos los eventos
                        else:
                            eventosTodos = obtenerEventos()[2]

                            if len(eventosTodos) == 0:
                                talk('No tienes ningún evento.')
                            else:
                                talk('Estos son todos tus eventos:')
                                for evento in eventosTodos:
                                    titulo = evento['summary']
                                    fInicio = extraerFechaEvento(evento)[0]
                                    fFinal = extraerFechaEvento(evento)[1]
                                    inicio = extraerTiemposEvento(evento)[0]
                                    final = extraerTiemposEvento(evento)[1]
                                    talk(f'De {inicio} del {fInicio} a las {final} del {fFinal}: {titulo}')
                    # Elimina un evento según su título
                    elif 'borra' in rec or 'elimina' in rec:
                        eventos = obtenerEventos()[2]
                        titulo = obtenerTitulo()
                        evento = eventoExiste(eventos, titulo)

                        if evento is None:
                            talk('No se ha encontrado ningún evento con título ' + titulo)
                        else:
                            talk(f'¿Seguro que quiere eliminar el evento {evento["summary"]}? Diga sí para confirmar')
                            confirmar = listen().replace('í', 'i').replace('ì', 'i')

                            if confirmar == 'si':
                                talk(eliminarEvento(evento['id']))
                            else:
                                talk('Evento no eliminado')

                # Trabajo sobre fechas
                elif 'que dia' in rec or 'cuando es' in rec:
                    if 'lunes' in rec or 'martes' in rec or 'miercoles' in rec or 'jueves' in rec or 'viernes' in rec or 'sabado' in rec or 'domingo' in rec:
                        talk(obtenerProximoDiaSemana(rec))
                    elif 'dentro de' in rec or 'sera' in rec:
                        talk(obtenerFechaFutura(rec))
                    elif 'era' in rec or 'fue' in rec:
                        talk(obtenerFechaPasada(rec))
                    elif 'es' in rec:
                        talk(obtenerFechaHoy())
                    else:
                        talk('No entendí: ' + rec)
                        talk("Pruebe con 'qué dia es hoy', 'que día será' o 'qué día fue'.")

                # El clima de hoy, mañana o pasado
                elif 'clima' in rec or 'tiempo' in rec:
       
                    if "hoy" in rec:
                        ciudad = obtenerCiudadClima(rec, 'hoy')
                        talk('Este es el clima de hoy en ' + ciudad + ':')
                        talk(obtenerClima(ciudad, 'hoy'))

                    elif "pasado mañana" in rec:
                        ciudad = obtenerCiudadClima(rec, 'pasado mañana')
                        talk('Este es el clima de pasado mañana en ' + ciudad + ':')
                        talk(obtenerClima(ciudad, "pasado mañana"))

                    elif "mañana" in rec:
                        ciudad = obtenerCiudadClima(rec, 'mañana')
                        talk('Este es el clima de mañana en ' + ciudad + ':')
                        talk(obtenerClima(ciudad, 'mañana'))

                    else:
                        talk('Lo siento, sólo tengo los datos de hoy, mañana y pasado.')

                # Dice la distancia y el tiempo que se recorre para ir de un punto X a un punto Y en una ruta Z
                if 'distancia' in rec or 'ruta' in rec or 'ir' in rec:
                    ciudades, tipoRuta = obtenerCiudadesMapa(rec), obtenerTipoRuta(rec)
                    talk(obtenerDatosMapa(ciudades, tipoRuta))

                # Hace una conversión de divisas
                elif 'cuanto son' in rec or 'cuanto equivale' in rec:
                    talk('Esta es la conversión: ')
                    talk(obtenerConversion(rec))

                #Lanza una moneda
                elif 'lanza una moneda' in rec:
                    resultado = random.choice(["cara", "cruz"])
                    talk("Y el resultado es... " + resultado)
                
                # Dice una frase de la lista
                elif 'como estas' in rec:
                    frases = [
                        '¡Estoy bien!',
                        'Pasando el rato',
                        'A mis cosas',
                        'Echando el día'
                    ]
                    talk(random.choice(frases))

                # Apaga a Jarvis
                elif 'descansa' in rec:
                    talk('Chao chao')
                    exit()
    
    # OPCIONES QUE AFECTAN AL ESTADO DEL ORDENADOR 
                # Cierra la sesión
                elif 'cierra sesion' in rec or 'cierra la sesion' in rec:
                    talk('Hasta luego')
                    os.system("shutdown -l")

                # Reinicia el ordenador
                elif 'reinicia el ordenador' in rec:
                    talk('Ahora nos vemos')
                    os.system("shutdown /r /t 1")

                # Suspende el ordenador
                elif 'suspende el ordenador' in rec:
                    import ctypes
                    ctypes.windll.user32.LockWorkStation()

                # Apaga el ordenador
                elif 'apaga el ordenador' in rec:
                    talk('Apagando en 3... 2... 1...')
                    os.system("shutdown /s /t 1")

                else: 
                    talk('Lo siento, no reconozco: ' + rec + '. Prueba con "Jarvis busca en Google"')
            
# TRABAJO DE ERRORES
            except Exception as ex:
                print('Error: ' + str(ex))


if __name__ == "__main__":
    talk("Hola "+ data["master"] +", soy Yarvis.")
    # Mientras no se apague el asistente seguirá ejecutándose siempre.
    while True:
        main()
