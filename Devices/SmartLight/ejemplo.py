import speech_recognition as sr
import pyttsx3, pywhatkit, wikipedia, datetime, keyboard
from pygame import mixer

name = "María"
listener = sr.Recognizer()
engine = pyttsx3.init()

voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)


def talk(text):
    engine.say(text)
    engine.runAndWait()


def micro_listen():
    try:
        with sr.Microphone() as source:
            print("Microfono está escuchando ...")
            pc = listener.listen(source)
            rec = listener.recognize_google(pc, language="es")
            rec = rec.lower()
            if name in rec:
                rec = rec.replace(name, "")
    except:
        pass
    return rec

def maria_listen():
    try: 
        with sr.Microphone() as source:
            print("Maria está escuchando")
            pc = listener.listen(source)
            grabacion = listener.recognize_google(pc, language="es")
            grabacion = grabacion.lower()
            if name in grabacion:
                grabacion = grabacion.replace(name "")
    except:
        pass
    return grabacion

def run_María():
    while True:
        rec = listen()
        if "reproduce" in rec:
            music = rec.replace("reproduce", "")
            print("Reproduciendo" + music)
            talk("Reproduciendo" + music)
            pywhatkit.playonyt(music)
        elif "busca" in rec:
            search = rec.replace("busca", "")
            wikipedia.set_lang("es")
            wiki = wikipedia.summary(search, 1)
            print(search + ": " + wiki)
            talk(wiki)
        elif "alarma" in rec:
            num = rec.replace("alarma", "")
            num = num.strip()
            talk("Alarma activada a las" + num + "horas")
            while True:
                if datetime.datetime.now().strftime("%H:%M") == num:
                    print("¡DESPIERTA!")
                    mixer.init()
                    mixer.music.load("alarm-clock.mp3")
                    mixer.music.play()
                    if keyboard.read_key() == "s":
                        mixer.music.stop()
                        break


if __name__ == "__main__":
    run_María()
