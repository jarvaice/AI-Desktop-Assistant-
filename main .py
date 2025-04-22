import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os
    
    

recognizer = sr.Recognizer()
engine  = pyttsx3.init()
newsapi = "1582b0102d1b405cb3df2eacddd6438f"

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')

    # Initialize pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load("temp.mp3")

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running untill the music stop playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3")     



# def aiProcess(command):
   
#     client = OpenAI(api_key="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")  # Replace with your actual API key

#     completion = client.chat.completions.create(
#     model="gpt-4o",
#     messages=[
#         {"role": "system", "content": "You are a virtual assistant named Jarvis skilled in general tasks like Alexa and Google Cloud.Give short response please."},
#         {"role": "user", "content": command}
#     ]
# )

#     return(completion.choices[0].message.content)    

def aiProcess(command):

    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",
    )

    completion = client.chat.completions.create(
    model="deepseek/deepseek-r1:free",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named Jarvis skilled in general tasks like Alexa and Google Cloud.Give short response please"},
        {"role": "user", "content": command},
    ]
)

    return(completion.choices[0].message.content)

def processCommand(c):
     if  "open google" in c.lower():
         webbrowser.open("https://google.com")
     elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")     
     elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")     
     elif "open Linkdin" in c.lower():
        webbrowser.open("https://Linkdin.com")
     elif c.lower().startswith("play"):
         song = c.lower().split(" ")[1]
         link = musiclibrary.music[song]
         webbrowser.open(link)


     elif "news" in c.lower():
         r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
         if r.status_code == 200:
            # Parse the JSON response
            data = r.json()

            # Extract the articles
            articles = data.get('articles', [])

            # Print the headlines
            for article in articles:
                speak(article['title'])

     else:
        #Let ai handle the process
        output = aiProcess(c)
        speak(output)



if __name__ == "__main__":
    speak("Initializing jarvis...")
    while True:
        # listen for the wake word "jarvis"
        # obtain audio from the microphone
        r = sr.Recognizer()
       
        print("recognizing...")
        try:
             with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)
             word = r.recognize_google(audio)
             
             if (word.lower() =="jarvis"):
                speak("ya")

                # Listen for command
                with sr.Microphone() as source:
                    print("jarvis activate...")
                    audio = r.listen(source, timeout=2, phrase_time_limit=1)
                    command = r.recognize_google(audio)

                    processCommand(command)




        except Exception as e:
            print("error; {0}".format(e))
            
