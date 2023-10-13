from guizero import App, Text, Box, TextBox, PushButton, TitleBox, Picture, Drawing
import tkinter
import os

class GUI:    
    def __init__(self):
        self.cwd = os.getcwd()
        self.app_start = "1"
        self.app = None
        self.header = None
        self.main = None
        self.width = 0
        self.height = 0

    def CreateWindow(self, title, width, height):
        self.width = width
        self.height = height
        container = App(visible=False, title=title, layout="grid", width=width, height=height)        
        self.app = container
        #disable resizing of the window
        self.app.tk.resizable(False,False)
        self.app.tk.geometry('%dx%d+%d+%d' % (self.width, self.height, ((self.app.tk.winfo_screenwidth() // 2) - (self.width // 2)), (self.app.tk.winfo_screenheight() // 2) - (self.height // 2)))
        return container
    
#------------------------------------------------------------
#main box for holding controls
#------------------------------------------------------------
    def DrawWindow(self):
        self.rootbox = Box(self.app, layout="grid", grid=[0,0], width=self.width, height="fill", align="left", border=0)
        return self.rootbox
#------------------------------------------------------------

#------------------------------------------------------------
#outer box for holding visual elements in perfect shape and dimensions
#------------------------------------------------------------
    def DrawMain(self, inner_width, inner_height):
        outerbox = Box(self.rootbox, layout="grid", grid=[0,1], width="fill", height="fill", align="left", border=0)
        outerbox.bg="#FFFFFF"

        Drawing(outerbox, width=46, height=46, grid=[0,0], align="right").image(0,0, image=self.cwd + "/images/corner-top-left.png", width=46, height=46)
        Drawing(outerbox, width=inner_width, height=46, grid=[1,0], align="left").image(0,0, image=self.cwd + "/images/top.png", width=800, height=46)
        Drawing(outerbox, width=46, height=46, grid=[2,0], align="left").image(0,0, image=self.cwd + "/images/corner-top-right.png", width=46, height=46)

        Drawing(outerbox, width=46, height=inner_height, grid=[0,1], align="right").image(0,0, image=self.cwd + "/images/side-left.png", width=46, height=800)
        #inside part of the whole window to hold control related boxes
        innerbox = Box(outerbox, layout="grid", grid=[1,1], width=inner_width, height=inner_height, align="top", border=0)
        innerbox.bg="#FFFFFF"
        Drawing(outerbox, width=46, height=inner_height, grid=[2,1], align="left").image(0,0, image=self.cwd + "/images/side-right.png", width=46, height=800)

        Drawing(outerbox, width=46, height=46, grid=[0,2], align="right").image(0,0, image=self.cwd + "/images/corner-bottom-left.png", width=46, height=46)
        Drawing(outerbox, width=inner_width, height=46, grid=[1,2], align="left").image(0,0, image=self.cwd + "/images/bottom.png", width=800, height=46)
        Drawing(outerbox, width=46, height=46, grid=[2,2], align="left").image(0,0, image=self.cwd + "/images/corner-bottom-right.png", width=46, height=46)

        return innerbox
#------------------------------------------------------------
    
    def Show(self):
        #disable resizing of the window
        self.app.tk.resizable(False,False)
        self.app.tk.geometry('%dx%d+%d+%d' % (self.width, self.height, ((self.app.tk.winfo_screenwidth() // 2) - (self.width // 2)), (self.app.tk.winfo_screenheight() // 2) - (self.height // 2)))
        self.app.visible = True
        self.app.display()

    def GetMainWindow(self):
        return self.app

    
