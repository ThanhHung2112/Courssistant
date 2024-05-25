import pygame
from gtts import gTTS

def Text2Speech(pandasResponse):
    language = "en"
    text_to_speak = "Vu has a banana that is exceptionally large, much to everyone's amazement. This banana stands out not only because of its impressive size but also because of its sweet and delicious flavor. Vu takes great pride in showing off this remarkable fruit to his friends and neighbors. The large banana has become a bit of a local legend, drawing attention from everyone who sees it. Vu's dedication to growing such an extraordinary banana has certainly paid off, making him quite popular in his community."

    gtts_object = gTTS(text=text_to_speak, lang=language, slow=False)
    gtts_object.save("speech.wav")

    # pygame.mixer.init()
    # pygame.mixer.music.load("speech.wav")
    # pygame.mixer.music.play()
    # while pygame.mixer.music.get_busy():
    #     pygame.time.Clock().tick(10)

Text2Speech("")