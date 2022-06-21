import cv2 as cv
import speech_recognition as sr
import os
import datetime
import webbrowser
import pyttsx3
import random

print("\n")
print("---------------------------------")
print("Try using the following commands:- ")
print("---------------------------------")
print("What's the time/date")
print("Open the mirror")
print("Tell me a joke")
print("What's the news")
print("Start video recording")
print("Open the camera. (Used to click pictures)")
print("Restaurants near me")
print("Gas stations near me / Petrol stations near me")


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

#greeting 
time = int(datetime.datetime.now().hour)
if time>= 0 and time<12:
    speak("Good Morning!")
elif time>= 12 and time<18:
    speak("Good Afternoon!")  
else:
    speak("Good Evening!") 


speak("I am your Assistant for today. Try using the commands on your screen")


img = cv.imread(r"C:\Users\Public\Pictures\up.png")

end_commands = ["stop", "end", "quit", "finish", "close"]

Time = ["what's the time","what's the date"] 

jokes = ["Did you hear they arrested the devil? Yeah, they got him on possession", "What did one DNA say to the other DNA? Do these genes make me look fat?", "My IQ test results came back. They were negative", "What do you get when you cross a polar bear with a seal? A polar bear", "Why can’t you trust an atom? Because they make up literally everything", "Why was six afraid of seven? Because seven eight nine", "What do you call a hippie’s wife? Mississippi", "What’s the difference between an outlaw and an in-law? Outlaws are wanted", "Before you marry a person, you should first make them use a computer with a slow Internet connection to see who they really are", "I never knew what happiness was until I got married—and then it was too late."]

while True:
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source: # microphone
            print("\nListening... \n")
            audio = r.listen(source)
            text = r.recognize_google(audio)
            print("You said: {}".format(text))

        for i in Time:
            if text == i:
                x = datetime.datetime.now()
                print("The date and time is ",x)
        
        for i in end_commands:
            if text == i: 
                quit()

        if text == "hello":
            speak("Hi.")

        elif text == "open the camera":
            speak("Activating camera. Hit space to click a picture. Hit escape to close the camera.")
            cam = cv.VideoCapture(0)
            cv.namedWindow("Camera")
            img_counter = 0
            while True:
                ret, frame = cam.read()
                if not ret:
                    speak("failed to grab frame")
                    break
                cv.imshow("Camera", frame)

                k = cv.waitKey(1)
                if k%256 == 27:
                    # ESC pressed
                    speak("Closing the camera")
                    break
                elif k%256 == 32:
                    # SPACE pressed
                    img_name = "camera{}.png".format(img_counter)
                    cv.imwrite(img_name, frame)
                    img_counter += 1

            cam.release()
            cv.destroyAllWindows()

        elif text == "tell me a joke":
            x = random.choice(jokes)
            speak(x)

        elif text == "open picture":
            cv.imshow("Up",img)
            cv.waitKey(0)
        
        elif text == "open the mirror":
            speak("Opening mirror.")
            cap = cv.VideoCapture(0)
            speak("Once your done, Press Q to close the mirror.")
            while True:
                ret, frame= cap.read()
                cv.imshow("Mirror", frame)
                
                if cv.waitKey(1) == ord ("q"):
                    speak("Closing Mirror")
                    break
            cap.release()
            cv.destroyAllWindows()

        elif text == "what's the news":
            webbrowser.open("https://www.bbc.co.uk")
            speak("Here's the latest news on BBC")

        elif text == "restaurants near me":
            webbrowser.open("https://www.google.com/maps/search/restaurant")
            speak("Here are some restaurants in your vicinity.")

        elif text == "gas stations near me" or text == "petrol stations near me":
            webbrowser.open("https://www.google.com/maps/search/Gas")
            speak("Here are some petrol stations in your vicinity.")
        
        elif text == "start video recording":
            
            speak("Starting video recording")
            filename = 'video.avi'
            frames_per_second = 24.0
            res = '720p'

            # Set resolution for the video capture
            # Function adapted from https://kirr.co/0l6qmh
            def change_res(cap, width, height):
                cap.set(3, width)
                cap.set(4, height)

            # Standard Video Dimensions Sizes
            STD_DIMENSIONS =  {
                "480p": (640, 480),
                "720p": (1280, 720),
                "1080p": (1920, 1080),
                "4k": (3840, 2160),
            }

            # grab resolution dimensions and set video capture to it.
            def get_dims(cap, res='1080p'):
                width, height = STD_DIMENSIONS["480p"]
                if res in STD_DIMENSIONS:
                    width,height = STD_DIMENSIONS[res]
                ## change the current caputre device
                ## to the resulting resolution
                change_res(cap, width, height)
                return width, height

            # Video Encoding, might require additional installs
            # Types of Codes: http://www.fourcc.org/codecs.php
            VIDEO_TYPE = {
                'avi': cv.VideoWriter_fourcc(*'XVID'),
                #'mp4': cv2.VideoWriter_fourcc(*'H264'),
                'mp4': cv.VideoWriter_fourcc(*'XVID'),
            }

            def get_video_type(filename):
                filename, ext = os.path.splitext(filename)
                if ext in VIDEO_TYPE:
                    return  VIDEO_TYPE[ext]
                return VIDEO_TYPE['avi']

            cap = cv.VideoCapture(0)
            out = cv.VideoWriter(filename, get_video_type(filename), 25, get_dims(cap, res))

            while True:
                ret, frame = cap.read()
                out.write(frame)
                cv.imshow('frame',frame)
                if cv.waitKey(1) & 0xFF == ord('q'):
                    speak("Ending video recording")
                    break

            cap.release()
            out.release()
            cv.destroyAllWindows()
    except:
        print("Sorry couldnt recognize what you said. Please repeat.")