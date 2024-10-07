import speech_recognition as sr
import pyttsx3  # Convert text to speech
import pywhatkit  # Play YouTube videos, send WhatsApp messages
import wikipedia  # Retrieve information from Wikipedia
import datetime as dt  # Get the current date
import pyjokes  # Get programming-related jokes


def text_to_speech(text):
    """Convert text to speech and play it."""
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # Set to female voice
    engine.setProperty('rate', 150)  # Set speech rate
    engine.setProperty('volume', 1)  # Set volume level
    engine.say(text)
    engine.runAndWait()


def process_question(question):
    """Process the user's question and provide appropriate responses."""
    question = question.lower()  # Normalize question to lower case

    if 'what are you doing' in question:
        response = "I am waiting for your question."
    elif 'how are you' in question:
        response = "I am good, thank you. How can I help you?"
    elif 'play' in question:
        song = question.replace('play', '').strip()
        pywhatkit.playonyt(song)
        return "Playing " + song
    elif 'who is' in question or 'college' in question:
        topic = question.replace('who is', '').replace('college', '').strip()
        response = wikipedia.summary(topic, 1)
    elif 'date' in question:
        response = str(dt.date.today())
    elif 'joke' in question:
        response = pyjokes.get_joke()
    elif 'love you' in question:
        response = "I love you too!"
    elif 'bye' in question:
        response = "Bye bye, please take care. We will meet later."
        text_to_speech(response)
        return False
    else:
        response = "I didn't get your question. Can you say it again?"

    text_to_speech(response)
    return True


def get_question():
    """Listen for a question from the user and return it."""
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('Say "Alexa" to start speaking')
        audio = r.listen(source)
        try:
            question = r.recognize_google(audio)
            print(question)  # Print recognized question
            if 'alexa' in question.lower():
                return question.replace('alexa', '').strip()
            else:
                print("You are not talking with me. Please continue your work.")
                return ""
        except sr.UnknownValueError:
            print("Sorry, I can't get your question.")
            return ""
        except Exception as e:
            print(f"An error occurred: {e}")
            return ""


def main():
    """Main function to run the voice assistant."""
    can_ask_question = True
    while can_ask_question:
        question = get_question()

        if not question.strip():  # Check if the question is empty
            text_to_speech("I didn't hear anything, please repeat.")
            continue  # Go to the next iteration of the loop

        can_ask_question = process_question(question)


if __name__ == "__main__":
    main()
