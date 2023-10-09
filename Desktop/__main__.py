#!/usr/bin/env python3


#------------------------------------------------------------
# REQUIREMENTS:
#
# Python3
# guizero
# PIL
#------------------------------------------------------------

from guizero import App, Text, Box, TextBox, PushButton, TitleBox, Picture, Drawing, CheckBox
import tkinter
from tkinter import Spinbox
from guizero import App
import gui

#Config = eval(open("Config.txt").read())

#------------------------------------------------------------
#default settings parameters for the gui
#do not change it unless you have strong reasons for that!
#------------------------------------------------------------
guiWidth = 860
guiHeight = 540
innerWidth = (guiWidth-92)
innerHeight = 400
#------------------------------------------------------------
#global variables for storing details...

Steps = 3


#------------------------------------------------------------
# positioning window function
# repositioning the window to the center of the active screen
#------------------------------------------------------------
def positioning_window(window_width, window_height, app): 
    app.tk.geometry('%dx%d+%d+%d' % (window_width, window_height, ((app.tk.winfo_screenwidth() // 2) - (window_width // 2)), (app.tk.winfo_screenheight() // 2) - (window_height // 2)))
#------------------------------------------------------------

#------------------------------------------------------------
# creating gui elements
#------------------------------------------------------------
mygui = gui.GUI()
mygui.CreateWindow("OnnxStream GUI", guiWidth, guiHeight,True)
main_window = mygui.GetMainWindow()
main_window.bg = "#F4F4F4"

#disable resizing of the window
main_window.tk.resizable(False,False)
#------------------------------------------------------------

#------------------------------------------------------------
#main box for holding controls
#------------------------------------------------------------
rootbox = Box(main_window, layout="grid", grid=[0,0], width=guiWidth, height="fill", align="left", border=0)
#------------------------------------------------------------


#------------------------------------------------------------
#header controls, like settings, help buttons, etc...
#some kind of a top menu, but in a custom way, because I like this more
#------------------------------------------------------------
HeaderControls = Box(rootbox, layout="grid", grid=[0,0], width=guiWidth, height=35, align="top", border=0)

#spacer left
Box(HeaderControls, layout="grid", grid=[0,0], width=46, height=35, align="right", border=0)
HeaderText_box = Box(HeaderControls, layout="grid", grid=[1,0], width=(innerWidth-120), height=35, align="left", border=0)
HeaderControls_inner = Box(HeaderControls, layout="grid", grid=[2,0], width=120, height=35, align="right", border=0)
#spacer right
Box(HeaderControls, layout="grid", grid=[3,0], width=46, height=35, align="left", border=0)

#header text, info text, etc...
#under implementation...
HeaderText_box_inner = Box(HeaderText_box, layout="grid", grid=[0,0], width=(innerWidth-120)-46, height=35, align="left", border=0)
HeaderText = Text(HeaderText_box_inner, text="OnnxStream", grid=[0,0], align="left")
HeaderText.font = "Arial Black"
HeaderText.text_color = "#000000"
HeaderText.size = 16

PushButton(HeaderControls_inner, grid=[0,0],text="Settings", padx=6, pady=2, align="right")
Box(HeaderControls_inner, layout="auto", grid=[1,0], border=0, align="right", width=20, height=20)
PushButton(HeaderControls_inner, grid=[2,0],text="Open Github", align="right", padx=6, pady=2)
#------------------------------------------------------------


#------------------------------------------------------------
#outer box for holding visual elements in perfect shape and dimmensions
#------------------------------------------------------------
outerbox = Box(rootbox, layout="grid", grid=[0,1], width="fill", height="fill", align="left", border=0)
outerbox.bg="#FFFFFF"

Drawing(outerbox, width=46, height=46, grid=[0,0], align="right").image(0,0, image="images/corner-top-left.png", width=46, height=46)
Drawing(outerbox, width=innerWidth, height=46, grid=[1,0], align="left").image(0,0, image="images/top.png", width=800, height=46)
Drawing(outerbox, width=46, height=46, grid=[2,0], align="left").image(0,0, image="images/corner-top-right.png", width=46, height=46)

Drawing(outerbox, width=46, height=innerHeight, grid=[0,1], align="right").image(0,0, image="images/side-left.png", width=46, height=800)
#inside part of the whole window to hold control related boxes
innerbox = Box(outerbox, layout="grid", grid=[1,1], width=innerWidth, height=innerHeight, align="top", border=0)
innerbox.bg="#FFFFFF"
Drawing(outerbox, width=46, height=innerHeight, grid=[2,1], align="left").image(0,0, image="images/side-right.png", width=46, height=800)

Drawing(outerbox, width=46, height=46, grid=[0,2], align="right").image(0,0, image="images/corner-bottom-left.png", width=46, height=46)
Drawing(outerbox, width=innerWidth, height=46, grid=[1,2], align="left").image(0,0, image="images/bottom.png", width=800, height=46)
Drawing(outerbox, width=46, height=46, grid=[2,2], align="left").image(0,0, image="images/corner-bottom-right.png", width=46, height=46)
#------------------------------------------------------------


#------------------------------------------------------------
#input box outer for holding the inner boxes
#it is required to avoid graphical glitches and possible alignment issues on different screens
#this also helping to keep the content aligned to top-left
#------------------------------------------------------------
inputbox_outer = Box(innerbox, layout="grid", grid=[0,0], width=innerWidth-320, height=innerHeight, border=0, align="top")
#------------------------------------------------------------

#------------------------------------------------------------
# input box
# this holds all the elements like project name input, push buttons, etc...
#------------------------------------------------------------
inputbox = Box(inputbox_outer, layout="grid", grid=[0,0], width=innerWidth-330, height=innerHeight, border=0, align="left")
#------------------------------------------------------------

#------------------------------------------------------------
# + Box (ProjectActionBox)
#   + Text (Project Actions)
#   + Box [spacer]
#   + PushButton (Save Project)
#   + Box [spacer]
#   + PushButton (Load Project)
#   + Box [spacer]
#   + PushButton (New Project)
#------------------------------------------------------------
ProjectActionBox = Box(inputbox, layout="grid", grid=[0,0], border=0, align="left")
Text(ProjectActionBox, grid=[0,0], text="Project Actions", align="left", size=10)
Box(ProjectActionBox, layout="auto", grid=[1,0], border=0, align="left", width=20, height=20)
PushButton(ProjectActionBox, grid=[2,0],text="Save Project", padx=6, pady=2)
Box(ProjectActionBox, layout="auto", grid=[3,0], border=0, align="left", width=20, height=20)
PushButton(ProjectActionBox, grid=[4,0],text="Load Project", padx=6, pady=2)
Box(ProjectActionBox, layout="auto", grid=[5,0], border=0, align="left", width=20, height=20)
PushButton(ProjectActionBox, grid=[6,0],text="New Project", padx=6, pady=2)
#------------------------------------------------------------


#------------------------------------------------------------
# project input box
# Outer box for holding sub-boxes and objects / widgets
#------------------------------------------------------------
ProjectInputBox = Box(inputbox, layout="grid", grid=[0,1], border=0, align="left")
#------------------------------------------------------------

#------------------------------------------------------------
# Text (Project Name)
# + TextBox (ProjectName)
#------------------------------------------------------------
Text(ProjectInputBox, grid=[0,0], text="Project Name", align="left", size=10)
ProjectName = TextBox(ProjectInputBox, grid=[0,1], text="Project Name", align="left", width=69, multiline=False)
#------------------------------------------------------------

#------------------------------------------------------------
# Text (Positive Prompt)
# + TextBox (PositivePrompt)
#------------------------------------------------------------
Text(ProjectInputBox, grid=[0,2], text="Positive Prompt", align="left", size=10)
PositivePrompt = TextBox(ProjectInputBox, grid=[0,3], text="Positive Prompt", align="left", width=52, height=4, multiline=True, scrollbar=True)
PositivePrompt.wrap=True
#------------------------------------------------------------

#------------------------------------------------------------
# Text (Negative Prompt)
# + TextBox (NegativePrompt)
#------------------------------------------------------------
Text(ProjectInputBox, grid=[0,4], text="Negative Prompt", align="left", size=10)
NegativePrompt = TextBox(ProjectInputBox, grid=[0,5], text="Negative Prompt", align="left", width=52, height=3, multiline=True, scrollbar=True)
NegativePrompt.wrap=True
#------------------------------------------------------------

#------------------------------------------------------------
# Text (Image name)
# + TextBox (TargetImage)
#------------------------------------------------------------
Text(ProjectInputBox, grid=[0,6], text="Image name", align="left", size=10)
TargetImage = TextBox(ProjectInputBox, grid=[0,7], text="output.png", align="left", width=69, multiline=False)
#------------------------------------------------------------


#------------------------------------------------------------
# Text (Steps)
# + Box (SliderBox)
#   + Box (SpinBox)
#     + Box (SpinBox_text)
#       + TextBox (Steps_TextBox)
#   + Box (SpinBox_buttons)
#     + PushButton (up)
#     + PushButton (down)
#
# Additionals:
# function (steps_text_changed)
# function (increase_steps)
# function (decrease_steps)
# function (getTextBoxValue)
# function (getTextBoxObj)
#------------------------------------------------------------
Text(ProjectInputBox, grid=[0,8], text="Steps", align="left", size=10)

#------------------------------------------------------------
def steps_text_changed(textbox_value):
    global Steps
    
    if getTextBoxValue().isnumeric() == False:
        if (getTextBoxValue()[:-1].isnumeric() == True):
            getTextBoxObj().value = getTextBoxValue()[:-1]
        else:
            Steps = 3
            getTextBoxObj().value = "3"
            return

    if (int(getTextBoxValue()) > 100):
        Steps = 100
        getTextBoxObj().value = "100"
        return

    if (int(getTextBoxValue()) < 3):
        Steps = 3
        getTextBoxObj().value = "3"
        return

    Steps = int(getTextBoxValue())
#------------------------------------------------------------
    
#------------------------------------------------------------
def increase_steps():
    global Steps    
        
    if Steps >= 100:
        return
    
    Steps += 1
    Steps_TextBox.value = str(Steps)
#------------------------------------------------------------

#------------------------------------------------------------
def decrease_steps():
    global Steps    
        
    if Steps <= 3:
        return
    
    Steps -= 1
    Steps_TextBox.value = str(Steps)
#------------------------------------------------------------

SpinBox = Box(ProjectInputBox, grid=[0,9],layout="grid",align="left", width="fill", height="fill", border=0)
SpinBox_text = Box(SpinBox, grid=[0,0],align="left", width="fill", height="fill")
Steps_TextBox = TextBox(SpinBox_text, text="3", align="left", width="4",command=steps_text_changed)

#------------------------------------------------------------
def getTextBoxValue():
    return Steps_TextBox.value
#------------------------------------------------------------

#------------------------------------------------------------
def getTextBoxObj():
    return Steps_TextBox
#------------------------------------------------------------

SpinBox_buttons = Box(SpinBox, grid=[1,0], layout="grid",align="left", width="fill", height="fill")
PushButton(SpinBox_buttons, grid=[0,0],text="+", padx=6, pady=0, image="images/button_up.png", width=10, height=5, command=increase_steps)
PushButton(SpinBox_buttons, grid=[0,1],text="-", padx=6, pady=0, image="images/button_down.png", width=10, height=5, command=decrease_steps)
#------------------------------------------------------------

CheckBox(ProjectInputBox,grid=[0,10], align="left", text="Use Stable Diffusion XL 1.0 instead of Stable Diffusion 1.5")

#horizontal line
Box(ProjectInputBox, grid=[0,11],layout="grid",align="left", width=innerWidth-320, height=2, border=0).bg = "#EFEFEF"
#spacer
Box(ProjectInputBox, grid=[0,12],layout="grid",align="left", width=320, height=20, border=0)

PushButton(ProjectInputBox, grid=[0,13],text="Start", padx=6, pady=2, align="left", width=40)


#------------------------------------------------------------





#------------------------------------------------------------
#horizontal spacer
#------------------------------------------------------------
Box(innerbox, layout="auto", grid=[1,0], width=10, height=400, align="top", border=0)
#------------------------------------------------------------


#------------------------------------------------------------
#image and related controls holder box
#------------------------------------------------------------
imageBox = Box(innerbox, layout="grid", grid=[2,0], width=320, height=400, align="top", border=0)

#image
picture = Picture(imageBox, image="images/main.png", grid=[0,0], width=320, height=320)

#vertical spacer
Box(imageBox, layout="auto", grid=[0,1], width=320, height=10, align="top", border=0)

StatusBox = Box(imageBox, layout="grid", grid=[0,2], border=0, align="left")
Text(StatusBox, grid=[0,0], text="Status:", align="left", size=10)
StatusMSG = Text(StatusBox, grid=[1,0], text="Completed...", align="left", size=10)

#horizontal line
Box(imageBox, grid=[0,3],layout="grid",align="left", width=320, height=2, border=0).bg = "#EFEFEF"
#spacer
Box(imageBox, grid=[0,4],layout="grid",align="left", width=60, height=10, border=0)

#image controls
ImageActionBox = Box(imageBox, layout="grid", grid=[0,5], border=0, align="left")

Text(ImageActionBox, grid=[0,0], text="Actions ", align="left", size=10)
Box(ImageActionBox, layout="auto", grid=[1,0], border=0, align="left", width=20, height=20)
PushButton(ImageActionBox, grid=[2,0],text="Save", padx=6, pady=2)
Box(ImageActionBox, layout="auto", grid=[3,0], border=0, align="left", width=20, height=20)
PushButton(ImageActionBox, grid=[4,0],text="Refine", padx=6, pady=2)
Box(ImageActionBox, layout="auto", grid=[5,0], border=0, align="left", width=20, height=20)
PushButton(ImageActionBox, grid=[6,0],text="Delete", padx=6, pady=2)
#------------------------------------------------------------

#positioning the window...
positioning_window(guiWidth, guiHeight, main_window)

#showing the gui
mygui.Show()
