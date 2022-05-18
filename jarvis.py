from datetime import datetime
from googletrans import Translator
from googlesearch import search
from clima import *
from fechas import *
from setupCalendario import obtenerServicioCalendario
from calendario import *
import socket, os, webbrowser,pyttsx3, speech_recognition as sr, pywhatkit, wikipedia, random, json, geocoder, time


# Métodos

def talk(texto : str):
    """
    Dice el mensaje pasado como parámetro
    """
    engine.say(texto)
    engine.runAndWait()
    if engine._inLoop:
        engine.endLoop()

def listen() -> str:
    """
    Escucha el audio y retorna el texto de este
    """

    listener = sr.Recognizer()
    with sr.Microphone() as source:
        print("Escuchando...")
        listener.adjust_for_ambient_noise(source, duration=1)
        listener.pause_threshold = 0.8
        audio = listener.listen(source, timeout=1)
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
    Crea la escucha de los comandos de voz. Retorna el comando y si se ha dicho la palabra de activación
    """
    estado = False
    rec = listen()
    try:
        rec = rec.replace('yarbiss', 'jarvis').replace('yarbis', 'jarvis')
        if nombre in rec:
            rec = eliminarTildes(rec.replace(nombre, "")).strip()
            estado = True
    except:
        pass
    return rec, estado

def eliminarNotasWikipedia(texto : str) -> str:
    """
    Elimina los [Nota N] del texto pasado por parámetro por el asistente
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

def config() -> dict:
    """
    Lee el fichero JSON y guarda su contenido en un diccionario que será retornado
    """
    f = open('config.json')
    data = json.load(f)
    f.close()
    return data

def eliminarTildes(texto : str) -> str:
    """
    Elimina las tildes del texto
    """
    return texto.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u").replace("à", "a").replace("è", "e").replace("ì", "i").replace("ò", "o").replace("ù", "u")

def cambiarNombre(nombre : str, data : json):
    """
    Cambia el apartado 'master' de config.json al nombre dicho.
    """
    with open('config.json', 'w') as f:
        
        data['master'] = nombre
        json.dump(data, f)

def obtenerCiudad(texto: str, cuando : str) -> str:
    """
    Obtiene la ciudad del texto para ver el clima, pone la primera letra en mayúsculas y la retorna.
    """
    traductor = Translator()
    ciudad = texto.replace('dime el clima de ', '').replace('dime el clima en ', '').replace('dime el clima de ' , '')
    ciudad = texto.replace('dime el tiempo de ', '').replace('dime el tiempo en ', '').replace('dime el tiempo de ' , '')
    ciudad = ciudad.replace(' de ', '').replace(' en ', '')
    ciudad = ciudad.replace(cuando, '')
    if ciudad == "":
        ciudad = geocoder.ip('me').city
    ciudad = ciudad.title()
    ciudadEs = traductor.translate(ciudad, dest='es').text

    if ciudadEs == 'Puerto':
        ciudadEs = 'O Porto'

    return ciudadEs

def URLBusquedaAmazon(texto: str) -> str:
    urls = []
    busqueda = texto + " amazon"
    resultados = search(busqueda, lang="es", num_results=1)
    for r in resultados:
        urls.append(r)
    return urls[0]

def obtenerTitulo():
    talk('Dime el título del evento')
    time.sleep(0.5)
    return listen()

def obtenerDesc():
    talk('Dime la descripción del evento')
    time.sleep(0.5)
    return listen()

def obtenerFecha():
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

def obtenerInicio():
    talk('Dime cuándo empieza el evento')
    time.sleep(0.5)
    texto = listen()
    return obtenerFecha(texto)

def obtenerFinal():
    talk('Dime cuándo termina el evento')
    time.sleep(0.5)
    texto = listen()
    return obtenerFecha(texto)



def run():
    """
    Llama al método 'escucha()' y dependiendo de los valores retornados ejecuta un comando de voz (ninguno si estado == False o si no se tiene ese comando).
    """
    valores = comando()
    rec = valores[0]
    estado = valores[1]
    print("-----------------DEBUG-----------------")
    print("Comando: " + rec + " Estado: " + str(estado))
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

                # Busca en Google o en Wikipedia
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
                
                # El clima de hoy, mañana o pasado
                elif 'clima' in rec or 'tiempo' in rec:
       
                    if "hoy" in rec:
                        ciudad = obtenerCiudad(rec, 'hoy')
                        talk('Este es el clima de hoy en ' + ciudad + ':')
                        talk(obtenerClima(ciudad, 'hoy'))

                    elif "pasado mañana" in rec:
                        ciudad = obtenerCiudad(rec, 'pasado mañana')
                        talk('Este es el clima de pasado mañana en ' + ciudad + ':')
                        talk(obtenerClima(ciudad, "pasado mañana"))

                    elif "mañana" in rec:
                        ciudad = obtenerCiudad(rec, 'mañana')
                        talk('Este es el clima de mañana en ' + ciudad + ':')
                        talk(obtenerClima(ciudad, 'mañana'))


                    else:
                        talk('Lo siento, sólo tengo los datos de hoy, mañana y pasado.')

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
                    talk('Lo siento, no reconozco: ' + rec)
            
            except Exception as ex:
                pass


# Configuración

wikipedia.set_lang('es')
engine = pyttsx3.init()
voices = engine.getProperty('voices')
volumen = engine.getProperty('volume')
engine.setProperty('voice', voices[2].id)
engine.setProperty('rate', 160)
data = config()
nombre = "jarvis"


if __name__ == "__main__":
    talk("Hola "+ data["master"] +", soy Yarvis.")
    # Mientras no se apague el asistente seguirá ejecutándose siempre.
    while True:
        run()
