## DESCRIPTION: This is a virtual assistant program that gets the date, current time, responds back with a random generator and returns 
##              information on a person

#### REQUIREMENTS ####
# pip install PyAudio
# pip install SpeechRecognition
# pip install gTTS
# pip install wikipedia


## Import the libraries
import speech_recognition as sr
import os
from gtts import gTTS
import datetime
import warnings
import calendar
import random
import wikipedia

# Ignore any warning messages
warnings.filterwarnings('ignore')

# Record audio and return it as a string 
def recordAudio():

    # Record audio
    r = sr.Recognizer() # create recognizer objet

    # Open the microphone and start recording
    with sr.Microphone() as source:
        print('Say something!')
        audio = r.listen(source)

    # Use Google's speech recognition 
    data = ''
    try:
        data = r.recognize_google(audio)
        print('You said: ' + data)
    except sr.UnknownValueError: # Check for unknown errors
        print('Google Speech Recognition could not understand the audio, unknown error')
    except sr.RequestError as e:
        print('Request results from Google Speech Recognition service error ' + e)
    
    return data
##recordAudio()

# A function to get virtual assistant response
def assistantResponse(text):
    print(text)

    ## Convert text to speech
    myObj = gTTS(text = text, lang='en', slow=False)

    ## Save the converted audio to a file
    myObj.save('assistant_response.mp3')

    ## Play the converted file
    os.system('start assistant_response.mp3')

#text = "This is a test"
#assistantResponse(text)

## A function for wake word(s) or phrase
def wakeWord(text):
    WAKE_WORDS = ['hey computer', 'okay computer'] # a list of wake words

    text = text.lower() # convert the input to all lower case to match the wake words

    ## check if the user input contains word(s) or phrase
    for phrase in WAKE_WORDS:
        if phrase in text:
            return True
    
    ## If the wake word(s) or phrase is not found in the user input
    return False

## A function to get current date
def getDate():
    now = datetime.datetime.now()
    myDate = datetime.datetime.today()
    weekday = calendar.day_name[myDate.weekday()] #e.g. Saturday
    monthNum = now.month
    dayNum = now.day

    ## A list of months
    month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    
    ## A list of of ordinal numbers
    ordinalNumbers = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th', '11th', '12th', '13th', '14th', '15th', '16th',
                        '17th', '18th', '19th', '20th', '21st', '22nd', '23rd', '24th', '25th', '26th', '27th', '28th', '29th', '30th',
                        '31st']

    return 'Today is ' + weekday + ', ' + month_names[monthNum - 1] + ' the ' + ordinalNumbers[dayNum - 1] + '. '
#print(getDate())

## A function to create random greeting 
def greeting(text):

    # Greeting inputs
    GREETING_INPUTS = ['hi', 'hey', 'hello', 'hola', 'greetings', 'wassup', 'que onda puto']

    # Greeting responses
    GREETING_RESPONSES = ['howdy', 'whats good', 'hello', 'hey there']

    # If user's response is a greeting then return a randomly chosen greeting response
    for word in text.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES) + '.'
    # If no greeting detected, return empty string
    return ''

## A function to get a poerson's first and last name from the text
def getPerson(text):
    wordList = text.split() # Splitting the text into a list of words

    for i in range(0, len(wordList)):
        if i + 3 <= len(wordList) - 1 and wordList[i].lower() == 'who' and wordList[i+1].lower() == 'is':
            return wordList[i+2] + ' ' + wordList[i+3]


## Keep listening to audio
while True:
    ## Record the audio
    text = recordAudio()
    response = ''

    ## Check for wake word(s) or phrase
    if (wakeWord(text) == True):
        #print('You said the Wake Word(s) or pharse.')

        ## Check for greetings by the user
        response = response + greeting(text)

        ## Check to see if the user said anything having to do with date
        if('date' in text):
            get_date = getDate()
            response = response + ' ' + get_date
        
        ## Check to see if the user said anything having to do with time 
        if('time' in text):
            now = datetime.datetime.now()
            meridiem = ''
            if now.hour >= 12:
                meridiem = 'P.M.' # Post Meridiem (P.M.) after midday
                hour = now.hour - 12
            else:
                meridiem = 'A.M.' # Ante Meridiem (A.M.) before midday
                hour = now.hour

            ## Convert minutes into proper string
            if now.minute < 10: 
                minute = '0' + str(now.minute)
            else:
                minute = str(now.minute)
            response = response + ' ' + 'It is ' + str(hour) + ':' + minute + ' ' + meridiem + ' .'
        
        ## Check if the user said 'who is'
        if('who is' in text):
            person = getPerson(text)
            wiki = wikipedia.summary(person, sentences = 2)
            response = response + ' ' + wiki

        ## Have the assistant respond back using audio and the text from response
        assistantResponse(response) 