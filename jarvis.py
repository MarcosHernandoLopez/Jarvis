from datetime import datetime
import pyttsx3
import speech_recognition as sr
import pywhatkit
import wikipedia
import random

# Configuración
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[2].id)
nombre = "jarvis"

def talk(texto : str):
    """
    Dice el mensaje pasado como parámetro
    """
    engine.say(texto)
    engine.runAndWait()


listener = sr.Recognizer()
def listen():
    try:
        # with sr.Microphone() as source:
            print("Escuchando...")
            # voice = listener.listen(source)
            # talk("Dime")
            # rec = listener.recognize_google(voice, language = 'es-ES')
            rec = "Jarvis cuentame un chiste" # Pruebas sin micro
            rec = rec.lower()
            if nombre in rec:
                rec = rec.replace(nombre, '')
                return rec  
    except Exception as ex:
        print("Error: " + str(ex))

def run():
    rec = listen()
    if "cuentame un chiste" in rec:
        chistes = ["Mamá, mamá, los spaghetti se están pegando. Déjalos que se maten",
                    "Soy Rosa. Ah, perdóname, es que soy daltónico.",
                    "Mi ordenador me gana al ajedrez, pero yo le gano boxeando.",
                    "Pues sí, el viaje a la India me cambió la vida. ¿Más langosta señor?. Pero ponle curry.",
                    "Doctor, un ciego quiere verlo. Dígale que yo no hago milagros.",
                    "¿Por qué Jaimito va con traje y corbata al oculista? Porque va a la graduación de sus gafas."]
        talk(random.choice(chistes))
    elif 'reproduce' in rec:
        music = rec.replace('reproduce', '')
        talk('Reproduciendo ' + music)
        pywhatkit.playonyt(music)
    elif 'que hora es' in rec:
        hora = datetime.now().strftime('%H:%M')
        talk("Son las " + hora)
    elif 'busca en wikipedia' in rec:
        order = rec.replace('busca en wikipedia', '')
        resultado = wikipedia.summary(order, 1)
        talk(resultado)
    elif 'busca en google' in rec:
        order = rec.replace('busca en google', '')
        resultado = pywhatkit.search(order)
        talk(resultado)
    elif 'captura de pantalla' in rec:
        pywhatkit.take_screenshot("Captura Jarvis")
    elif 'control remoto' in rec:
        talk('Iniciando el control remoto')
        pywhatkit.start_server()
    else: 
        talk('Lo siento, no tengo esa funcionalidad')

run()
