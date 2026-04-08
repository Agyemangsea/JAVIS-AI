import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import speech_recognition as sr
import pyttsx3
import datetime
import os
import json

class JavisAI:
    def __init__(self):
        """Initialize Javis AI with NLP capabilities"""
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)  # Speed of speech
        self.model = self.build_model()
        self.intents = self.load_intents()
        
    def build_model(self):
        """Build TensorFlow neural network model"""
        model = keras.Sequential([
            layers.Dense(128, activation='relu', input_shape=(10,)),
            layers.Dropout(0.5),
            layers.Dense(64, activation='relu'),
            layers.Dropout(0.5),
            layers.Dense(32, activation='relu'),
            layers.Dense(5, activation='softmax')  # 5 intent categories
        ])
        model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        return model
    
    def load_intents(self):
        """Load intent patterns"""
        return {
            'greeting': ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening'],
            'time': ['what time', 'current time', 'tell me time'],
            'date': ['what date', 'today date', 'tell me date'],
            'help': ['help', 'what can you do', 'commands'],
            'exit': ['exit', 'quit', 'goodbye', 'bye']
        }
    
    def get_time_greeting(self):
        """Return greeting based on time of day"""
        current_hour = datetime.datetime.now().hour
        
        if 5 <= current_hour < 12:
            return "Good morning! I hope you slept well. How can I assist you today?"
        elif 12 <= current_hour < 17:
            return "Good noon! I hope your day is going great. What do you need?"
        else:
            return "Good evening! It's time to wind down. How can I help you?"
    
    def speak(self, text):
        """Convert text to speech"""
        print(f"Javis: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
    
    def listen(self):
        """Listen to microphone input"""
        try:
            with sr.Microphone() as source:
                print("Listening...")
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source, timeout=5)
                text = self.recognizer.recognize_google(audio)
                print(f"You said: {text}")
                return text.lower()
        except sr.UnknownValueError:
            self.speak("Sorry, I didn't catch that. Please try again.")
            return ""
        except sr.RequestError:
            self.speak("Sorry, I'm having trouble connecting to the internet.")
            return ""
    
    def process_command(self, command):
        """Process user command and return response"""
        if any(word in command for word in self.intents['greeting']):
            return self.get_time_greeting()
        elif any(word in command for word in self.intents['time']):
            current_time = datetime.datetime.now().strftime("%H:%M")
            return f"The current time is {current_time}"
        elif any(word in command for word in self.intents['date']):
            current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
            return f"Today is {current_date}"
        elif any(word in command for word in self.intents['help']):
            return "I can help you with time, date, greetings, and more. Just ask!"
        else:
            return "I'm not sure how to help with that. Try asking for time, date, or greeting."
    
    def run(self):
        """Main AI loop"""
        self.speak(self.get_time_greeting())
        
        while True:
            command = self.listen()
            
            if not command:
                continue
            
            if any(word in command for word in self.intents['exit']):
                self.speak("Goodbye! See you later.")
                break
            
            response = self.process_command(command)
            self.speak(response)

def main():
    """Start Javis AI"""
    print("🚀 Starting Javis AI...")
    javis = JavisAI()
    javis.run()

if __name__ == "__main__":
    main()
