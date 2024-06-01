from gtts import gTTS
from pydub import AudioSegment
import pygame
import os

def text2speech(pandasResponse):
    language = "en"
    text_to_speak = pandasResponse

    # Create a cache sound file to execute TTS
    gtts_object = gTTS(text=text_to_speak, lang=language, slow=False)
    gtts_object.save("cache_sound.mp3")

    # Convert mp3 to wav AudioSegment
    audio = AudioSegment.from_mp3("cache_sound.mp3")
    audio.export("cache_sound.wav", format="wav")

    # Just load wav file converted from mp3 cache
    pygame.mixer.init()
    pygame.mixer.music.load("cache_sound.wav")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    # Remove cache mp3 file
    os.remove("cache_sound.mp3")
