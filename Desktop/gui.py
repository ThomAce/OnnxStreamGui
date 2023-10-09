from guizero import App, Text, Box, TextBox, PushButton, TitleBox, Picture
import tkinter

class GUI:
    app_start = ""
    app = None
    
    def __init__(self):
        self.app_start = "1"
        self.app = None

    def CreateWindow(self, title, width, height, main_window = False):
        container = App(visible=False, title=title, layout="grid", width=width, height=height)
        if main_window == True:
            self.app = container
        else:
            return container

    def Show(self):
        self.app.visible = True
        self.app.display()

    def GetMainWindow(self):
        return self.app

    
