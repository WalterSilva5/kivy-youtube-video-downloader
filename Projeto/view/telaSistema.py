from pytube import YouTube
from sys import path
from os import sep
import os
from kivy.clock import Clock, mainthread
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.config import Config
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar

# desabilita o multi touch que cria bolas vermelhas na tela
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
# define the size of the window
# define as configurações da tela
Config.set('graphics', 'width', '300')
Config.set('graphics', 'height', '500')  # Disables window resizing
Config.set('graphics', 'resizable', False)
Config.write()

class GerenciadorDeTelas(ScreenManager):
    pass
class TelaPrincipal(Screen):
    pass

class TelaSistemaApp(App):
    def build(self):
        self.title = "Baixar Videos do youtube"
        return GerenciadorDeTelas()

    @mainthread
    def downloadYouTubeVideo(self, videourl, syspath):
        yt = YouTube(videourl, on_progress_callback=self.verificaProgresso)
        yt = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        self.file_size = yt.filesize
        if not os.path.exists(syspath):
            os.makedirs(syspath)
        yt.download(syspath)

    @mainthread
    def verificaProgresso(self, stream = None, chunk = None, file_handle = None, remaining = None):
        self.restante=0
        self.percent = (100 * (self.file_size - remaining)) // self.file_size
        self.restante = (100 * (self.file_size - remaining)) // self.file_size

        if self.percent == self.restante:
            self.root.get_screen("TelaPrincipal").ids.labelMensagem.text = "[b]{}%[/b]".format(self.restante)
            self.root.get_screen("TelaPrincipal").ids.labelMensagem.text = "[b]Feito[/b]"
            print(self.restante)

    def baixarVideo(self, url):
        self.downloadYouTubeVideo(url, str(path[1]+sep+'downloads'))

