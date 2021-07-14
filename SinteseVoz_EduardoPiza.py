#!/usr/bin/env python
# coding: utf-8

# In[1]:


# POS GRADUACAO - IESB
# Disciplina: Computacao Cognitiva II - Sintese de voz
# Aluno: Eduardo Gomes Piza
# Turma: A


# In[2]:


from tkinter import *

from ibm_watson import TextToSpeechV1
from ibm_watson.websocket import SynthesizeCallback
import pyaudio
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
from threading import Thread
from queue import Queue, Full

import pyaudio
import wave
import speech_recognition as sr
import base64
import time

authenticator = IAMAuthenticator('Cv3uJ8s1jrpufyTIpJbQ7CMgwj2in-QUEHcQtVxOeCdI')
authenticator2 = IAMAuthenticator('B-ahWVChPrd17mv-SEytAJaWYzJreO9I1trx_pKuxg4r')    
service = TextToSpeechV1(authenticator=authenticator)
speech_to_text = SpeechToTextV1(authenticator=authenticator2)


# In[3]:


class Application:
    def __init__(self, master=None):
        self.fontePadrao = ("Arial", "10")
        # No primeiro container vamos informar o título
        self.primeiroContainer = Frame(master)
        self.primeiroContainer["pady"] = 10
        self.primeiroContainer.pack()

        # No segundo e terceiro container vamos acrescentar o campo
        # para que o usuário digite o texto que deseja "processar"
        self.segundoContainer = Frame(master)
        self.segundoContainer["padx"] = 20
        self.segundoContainer.pack()

        self.terceiroContainer = Frame(master)
        self.terceiroContainer["padx"] = 20
        self.terceiroContainer.pack()

        self.quartoContainer = Frame(master)
        self.quartoContainer["pady"] = 20
        self.quartoContainer.pack()

        self.quintoContainer = Frame(master)
        self.quintoContainer["pady"] = 20
        self.quintoContainer.pack()

        self.sextoContainer = Frame(master)
        self.sextoContainer["pady"] = 20
        self.sextoContainer.pack()

        self.setimoContainer = Frame(master)
        self.setimoContainer["pady"] = 20
        self.setimoContainer.pack()

        self.oitavoContainer = Frame(master)
        self.oitavoContainer["pady"] = 20
        self.oitavoContainer.pack()        
 
        self.nonoContainer = Frame(master)
        self.nonoContainer["pady"] = 20
        self.nonoContainer.pack()

        self.titulo = Label(self.primeiroContainer, text="Sintese de Voz")
        self.titulo["font"] = ("Arial", "12", "bold")
        self.titulo.pack()

        self.nomeLabel = Label(self.segundoContainer,text="Insira o texto para processamento e clique no botao 'Processar':", font=self.fontePadrao)
        self.nomeLabel.pack(side=LEFT)

        self.campoTexto = Entry(self.terceiroContainer)
        self.campoTexto["width"] = 100
        self.campoTexto["font"] = self.fontePadrao
        self.campoTexto.focus()
        self.campoTexto.pack(side=LEFT)

        self.processarTexto = Button(self.quartoContainer)
        self.processarTexto["text"] = "Processar"
        self.processarTexto["font"] = ("Calibri", "10")
        self.processarTexto["width"] = 12
        self.processarTexto["command"] = self.processaTexto
        self.processarTexto.pack()

        self.mensagem = Label(self.quintoContainer, text="", font=self.fontePadrao)
        self.mensagem.pack()
        
        self.vozLabel1 = Label(self.sextoContainer, text="Pressione o botão 'Gravar Voz' para iniciar a gravação!", font=self.fontePadrao)
        self.vozLabel1.pack(side=LEFT)

        self.vozLabel2 = Label(self.sextoContainer, text="Serão gravados 5 segundos de voz para processamento!", font=self.fontePadrao)
        self.vozLabel2.pack(side=LEFT)        
        
        self.gravarVoz = Button(self.oitavoContainer)
        self.gravarVoz["text"] = "Gravar Voz"
        self.gravarVoz["font"] = ("Calibri", "10")
        self.gravarVoz["width"] = 20
        self.gravarVoz["command"] = self.gravacaoVoz
        self.gravarVoz.pack()        
 
        self.gravarVoz = Button(self.oitavoContainer)
        self.gravarVoz["text"] = "Processar gravação"
        self.gravarVoz["font"] = ("Calibri", "10")
        self.gravarVoz["width"] = 20
        self.gravarVoz["command"] = self.processaGravacao
        self.gravarVoz.pack()
        
        self.textoResultado = Label(self.nonoContainer, text='', font=self.fontePadrao)
        self.textoResultado.pack(side=LEFT)

    #Método para processar o texto digitado
    def processaTexto(self):
        
        text = self.campoTexto.get()
        test_callback = MySynthesizeCallback()
        
        service.synthesize_using_websocket(text,
                                           test_callback,
                                           accept='audio/wav',
                                           voice="pt-BR_IsabelaVoice"
                                           #voice="pt-BR_IsabelaV3Voice"
                                           )
    
    #Método para gravar a voz/audio
    def gravacaoVoz(self):

        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        RECORD_SECONDS = 5
        
        WAVE_OUTPUT_FILENAME = "output.wav"

        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        print("==> Iniciando gravação")

        frames = []

        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        print("==> Gravação finalizada")

        stream.stop_stream()
        stream.close()
        p.terminate()

        global wf
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        

    #Método para processar a voz e retornar o texto
    def processaGravacao(self):        
        with open('output.wav','rb') as audio_file:
            speech_recognition_results = speech_to_text.recognize(
            audio=audio_file,
            model='pt-BR_BroadbandModel',
            content_type='audio/wav'       
            ).get_result()
        resultado = speech_recognition_results['results']
        resultado = resultado[0]
        resultado = resultado['alternatives']
        resultado = resultado[0]
        resultado = resultado['transcript']
        self.textoResultado.destroy()
        self.textoResultado = Label(self.nonoContainer, text=resultado, font=self.fontePadrao)
        self.textoResultado.pack(side=LEFT)

        
class Play(object):
    """
    Wrapper to play the audio in a blocking mode
    """
    def __init__(self):
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 22050
        self.chunk = 1024
        self.pyaudio = None
        self.stream = None

    def start_streaming(self):
        self.pyaudio = pyaudio.PyAudio()
        self.stream = self._open_stream()
        self._start_stream()

    def _open_stream(self):
        stream = self.pyaudio.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            output=True,
            frames_per_buffer=self.chunk,
            start=False
        )
        return stream

    def _start_stream(self):
        self.stream.start_stream()

    def write_stream(self, audio_stream):
        self.stream.write(audio_stream)

    def complete_playing(self):
        self.stream.stop_stream()
        self.stream.close()
        self.pyaudio.terminate()

class MySynthesizeCallback(SynthesizeCallback):
    def __init__(self):
        SynthesizeCallback.__init__(self)
        self.play = Play()

    def on_connected(self):
        print('Opening stream to play')
        self.play.start_streaming()

    def on_error(self, error):
        print('1. Error received: {}'.format(error))

    def on_timing_information(self, timing_information):
        print(timing_information)

    def on_audio_stream(self, audio_stream):
        self.play.write_stream(audio_stream)
        return audio_stream
    
    def on_data(self, data):
        return data

    def on_close(self):
        print('Completed synthesizing')
        self.play.complete_playing()

# define callback for the speech to text service
class MyRecognizeCallback(RecognizeCallback):
    def __init__(self):
        RecognizeCallback.__init__(self)

    def on_transcription(self, transcript):
        print(transcript)

    def on_connected(self):
        print('Connection was successful')

    def on_error(self, error):
        print('2. Error received: {}'.format(error))

    def on_inactivity_timeout(self, error):
        print('Inactivity timeout: {}'.format(error))

    def on_listening(self):
        print('Service is listening')

    def on_hypothesis(self, hypothesis):
        print(hypothesis)

    def on_data(self, data):
        print(data)

    def on_close(self, ws):
        print('Connection closed')
        


# In[4]:


root = Tk()
Application(root)
root.mainloop()


# In[ ]:




