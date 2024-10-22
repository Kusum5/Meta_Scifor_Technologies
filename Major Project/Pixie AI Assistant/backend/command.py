import time
import pyttsx3
import speech_recognition as sr
import eel

def speak(text):
    text = str(text)
    engine = pyttsx3.init('sapi5')

    # Get available voices
    voices = engine.getProperty('voices')
    
    # Set female voice (index 1 is female)
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate',174)
    eel.DisplayMessage(text)
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()

def takecommand():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('Listening ...')
        eel.DisplayMessage('Listening ...')
        r.pause_threshold = 1  # Pause before finalizing the recognition
        r.adjust_for_ambient_noise(source)  # Adjust to background noise
        
        # Listen for the user's voice
        audio = r.listen(source, timeout=10, phrase_time_limit=4)
        
    try:
        print('Recognizing ...')
        eel.DisplayMessage('Recognizing ...')
        query = r.recognize_google(audio,language='en-IN')
        print(f'User said: {query}')
        eel.DisplayMessage(query)
        time.sleep(2)

    except Exception as e:
        return ""
    return query.lower()
    
@eel.expose
def allCommands(message=1):
    if message == 1:
        query = takecommand()
        print(query) 
        eel.senderText(query)  
    else:
        query = message 
        eel.senderText(query)      
    try:

        if "open" in query:
            from backend.features import openCommand
            openCommand(query)
        elif "on youtube" in query:
            from backend.features import playYoutube 
            playYoutube(query)
        elif "send message" in query or "phone call" in query or "video call" in query:
            from backend.features import findContact, whatsApp
            contact_no,name = findContact(query)
            if(contact_no != 0):

                if "send message" in query:
                    message = 'message'
                    speak("what message to send")
                    query = takecommand()
                elif "phone call" in query:
                    message = 'call'
                else:
                    message = 'video call'
                    
                whatsApp(contact_no, query, message, name)    
        else:
            from backend.features import chatBot
            chatBot(query)
    except:
        print("error")

    eel.ShowHood()