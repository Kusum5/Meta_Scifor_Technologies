import os
import eel
from backend.features import *
from backend.command import *
from backend.auth import recoganize

def start():
    eel.init("frontend")

    playAssistantSound()

    @eel.expose
    def init():
        eel.hideLoader()
        speak("Please Authenticate your face first.")
        flag = recoganize.AuthenticateFace()
        if flag == 1:
            eel.hideFaceAuth()
            speak("Face authenticated successful.")
            eel.hideFaceAuthSuccess()
            speak("Welcome. How can I help you?")
            eel.hideStart()
            playAssistantSound()
        else:
            speak("Face authentication failed!")    
    os.system('start msedge.exe --app="http://localhost:8000/index.html"')
    eel.start('index.html',mode=None,host="localhost",block=True)