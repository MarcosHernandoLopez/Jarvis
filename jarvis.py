import pyttsx3
import speech_recognition as sr

# Configuración
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[2].id)
nombre = "jarvis"

# Métodos

def talk(texto : str):
    """
    Dice el mensaje pasado como parámetro
    """
    engine.say(texto)
    engine.runAndWait()


# Main
listener = sr.Recognizer()

try:
    with sr.Microphone() as source:
        print("Escuchando...")
        voice = listener.listen(source)
        rec = listener.recognize_google(voice)
        rec = rec.lower()
        if nombre in rec:
            talk(rec)
except Exception as ex:
    print("Error: " + str(ex))

