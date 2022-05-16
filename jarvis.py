from datetime import datetime
import socket
import webbrowser
import pyttsx3
import speech_recognition as sr
import pywhatkit
import wikipedia
import random
import os
import json
from clima import *

# Métodos

def talk(texto : str):
    """
    Dice el mensaje pasado como parámetro
    """
    engine.say(texto)
    engine.runAndWait()

def eliminarNotasWikipedia(texto : str):
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

def config():
    f = open('config.json')
    data = json.load(f)
    f.close()
    return data

def eliminarTildes(texto : str):
    return texto.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")

def escucha():
    listener = sr.Recognizer()
    estado = False

    with sr.Microphone() as source:
        print("Escuchando...")
        listener.adjust_for_ambient_noise(source, duration=1)
        audio = listener.listen(source)
        rec = ""

        try:
            rec = listener.recognize_google(audio, language='es-ES').lower()
            rec = rec.replace('yarbiss', 'jarvis').replace('yarbis', 'jarvis')

            if nombre in rec:
                rec = eliminarTildes(rec.replace(nombre, "")).strip()
                estado = True

        except:
            pass
    
    return rec, estado

def cambiarNombre(nombre : str, data : json):
    with open('config.json', 'w') as f:
        data['lord'] = nombre
        json.dump(data, f)

def obtenerCiudad(texto: str):
    split1 = texto.split('en ')
    split2 = split1[1].split(' de ')
    return split2[0]


def run():
        valores = escucha()
        rec = valores[0]
        estado = valores[1]
        print("-----------------DEBUG-----------------")
        print("Comando: " + rec + "          Estado: " + str(estado))
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
                    else:
                        talk('Necesito que me digas dónde buscar')

                # Cambiar nombre de saludo
                elif 'llamame' in rec:
                    nombre = rec.replace('llamame', '').lstrip()
                    cambiarNombre(nombre.capitalize(), data)
                    talk('Vale, a partir de ahora te llamaré ' + nombre.capitalize())

                #Te dice el nombre registrado en la configuración
                elif 'cual es mi nombre' in rec:
                    nombre = data['lord']
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
                elif 'clima' or 'tiempo' in rec:
                    ciudad = obtenerCiudad(rec).title()
                    
                    if "hoy" in rec:
                        talk('Este es el clima de hoy en ' + ciudad + ':')
                        talk(obtenerClima(ciudad, 'hoy'))
                    elif "mañana" in rec:
                        talk('Este es el clima de mañana en ' + ciudad + ':')
                        talk(obtenerClima(ciudad, 'mañana'))
                    elif "pasado mañana" in rec:
                        talk('Este es el clima de pasado mañana en ' + ciudad + ':')
                        talk(obtenerClima(ciudad, "pasado mañana"))
                    else:
                        talk('Lo siento, sólo tengo los datos de hoy, mañana y pasado.')

                #Lanza una moneda
                elif 'lanza una moneda' in rec:
                    resultado = random.choice(["cara", "cruz"])
                    talk("Y el resultado es... " + resultado)

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
engine.setProperty('rate', 175)
data = config()
nombre = "jarvis"



talk("Hola "+ data["lord"] +", soy Jarvis y estoy a tu servicio")
while True:
    run()
