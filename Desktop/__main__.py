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
import gui
import os
import Processing
import SD

sd = SD.SD()
sd.Load()

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

WorkingDirectory = os.getcwd()

Steps = 3


#------------------------------------------------------------
# positioning window function
# repositioning the window to the center of the active screen
#------------------------------------------------------------
def positioning_window(window_width, window_height, app): 
    app.tk.geometry('%dx%d+%d+%d' % (window_width, window_height, ((app.tk.winfo_screenwidth() // 2) - (window_width // 2)), (app.tk.winfo_screenheight() // 2) - (window_height // 2)))
#------------------------------------------------------------

Diffusion = Processing.Diffusion()

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
HeaderText = Text(HeaderText_box_inner, text="OnnxStream GUI", grid=[0,0], align="left")
HeaderText.font = "Arial Black"
HeaderText.text_color = "#000000"
HeaderText.size = 16

PushButton(HeaderControls_inner, grid=[0,0],text="Settings", padx=6, pady=2, align="right").font = "Arial"
Box(HeaderControls_inner, layout="auto", grid=[1,0], border=0, align="right", width=20, height=20)
PushButton(HeaderControls_inner, grid=[2,0],text="Open Github", align="right", padx=6, pady=2).font = "Arial"
#------------------------------------------------------------


#------------------------------------------------------------
#outer box for holding visual elements in perfect shape and dimmensions
#------------------------------------------------------------
outerbox = Box(rootbox, layout="grid", grid=[0,1], width="fill", height="fill", align="left", border=0)
outerbox.bg="#FFFFFF"

Drawing(outerbox, width=46, height=46, grid=[0,0], align="right").image(0,0, image=WorkingDirectory + "/images/corner-top-left.png", width=46, height=46)
Drawing(outerbox, width=innerWidth, height=46, grid=[1,0], align="left").image(0,0, image=WorkingDirectory + "/images/top.png", width=800, height=46)
Drawing(outerbox, width=46, height=46, grid=[2,0], align="left").image(0,0, image=WorkingDirectory + "/images/corner-top-right.png", width=46, height=46)

Drawing(outerbox, width=46, height=innerHeight, grid=[0,1], align="right").image(0,0, image=WorkingDirectory + "/images/side-left.png", width=46, height=800)
#inside part of the whole window to hold control related boxes
innerbox = Box(outerbox, layout="grid", grid=[1,1], width=innerWidth, height=innerHeight, align="top", border=0)
innerbox.bg="#FFFFFF"
Drawing(outerbox, width=46, height=innerHeight, grid=[2,1], align="left").image(0,0, image=WorkingDirectory + "/images/side-right.png", width=46, height=800)

Drawing(outerbox, width=46, height=46, grid=[0,2], align="right").image(0,0, image=WorkingDirectory + "/images/corner-bottom-left.png", width=46, height=46)
Drawing(outerbox, width=innerWidth, height=46, grid=[1,2], align="left").image(0,0, image=WorkingDirectory + "/images/bottom.png", width=800, height=46)
Drawing(outerbox, width=46, height=46, grid=[2,2], align="left").image(0,0, image=WorkingDirectory + "/images/corner-bottom-right.png", width=46, height=46)
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

#save_project function
#Save_Project_PushButton action
#referencing to a later defined function. Python trick...
def save_project():
    save_project_data()

ProjectActionBox = Box(inputbox, layout="grid", grid=[0,0], border=0, align="left")
Text(ProjectActionBox, grid=[0,0], text="Project Actions", align="left", size=9, font="Arial Black")
Box(ProjectActionBox, layout="auto", grid=[1,0], border=0, align="left", width=20, height=20)
SaveProject_PushButton = PushButton(ProjectActionBox, grid=[2,0],text="Save Project", padx=6, pady=1, command=save_project)
SaveProject_PushButton.font = "Arial"
Box(ProjectActionBox, layout="auto", grid=[3,0], border=0, align="left", width=20, height=20)
LoadProject_PushButton = PushButton(ProjectActionBox, grid=[4,0],text="Load Project", padx=6, pady=1)
LoadProject_PushButton.font = "Arial"
Box(ProjectActionBox, layout="auto", grid=[5,0], border=0, align="left", width=20, height=20)
NewProject_PushButton = PushButton(ProjectActionBox, grid=[6,0],text="New Project", padx=6, pady=1)
NewProject_PushButton.font = "Arial"
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
Text(ProjectInputBox, grid=[0,0], text="Project Name", align="left", size=9, font="Arial Black")
ProjectName = TextBox(ProjectInputBox, grid=[0,1], text=sd.GetName(), align="left", width=60, multiline=False)
ProjectName.font = "Arial"
#------------------------------------------------------------

#------------------------------------------------------------
# Text (Positive Prompt)
# + TextBox (PositivePrompt)
#------------------------------------------------------------
Text(ProjectInputBox, grid=[0,2], text="Positive Prompt", align="left", size=9, font="Arial Black")
PositivePrompt = TextBox(ProjectInputBox, grid=[0,3], text=sd.GetPosPrompt(), align="left", width=58, height=4, multiline=True, scrollbar=True)
PositivePrompt.wrap = True
PositivePrompt.font = "Arial"
#------------------------------------------------------------

#------------------------------------------------------------
# Text (Negative Prompt)
# + TextBox (NegativePrompt)
#------------------------------------------------------------
Text(ProjectInputBox, grid=[0,4], text="Negative Prompt", align="left", size=9, font="Arial Black")
NegativePrompt = TextBox(ProjectInputBox, grid=[0,5], text=sd.GetNegPrompt(), align="left", width=58, height=3, multiline=True, scrollbar=True)
NegativePrompt.wrap = True
NegativePrompt.font = "Arial"
#------------------------------------------------------------

#------------------------------------------------------------
# Text (Image name)
# + TextBox (TargetImage)
#------------------------------------------------------------
Text(ProjectInputBox, grid=[0,6], text="Image name", align="left", size=9, font="Arial Black")
TargetImage_Box = Box(ProjectInputBox, grid=[0,7], layout="grid", width="fill", align="left")
TargetImage = TextBox(TargetImage_Box, grid=[0,0], text=sd.GetImage(), align="left", width=54, multiline=False)
TargetImage.font = "Arial"
#spacer
Box(TargetImage_Box, grid=[1,0],layout="grid",align="left", width=10, height=10, border=0)

def open_target_image():
    TargetImage_Box.select_file(title="Select file", folder=".", filetypes=[["All files", "*.*"]], save=False, filename="")

OpenTargetImage_PushButton = PushButton(TargetImage_Box, grid=[2,0], width=18, height=18, align="right", image=WorkingDirectory + "/images/save_icon.png")
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
Text(ProjectInputBox, grid=[0,8], text="Steps", align="left", size=9, font="Arial Black")

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
Steps_TextBox = TextBox(SpinBox_text, text=sd.GetSteps(), align="left", width="4",command=steps_text_changed)
Steps_TextBox.font = "Arial"

#------------------------------------------------------------
def getTextBoxValue():
    return Steps_TextBox.value
#------------------------------------------------------------

#------------------------------------------------------------
def getTextBoxObj():
    return Steps_TextBox
#------------------------------------------------------------

SpinBox_buttons = Box(SpinBox, grid=[1,0], layout="grid",align="left", width="fill", height="fill")
SpinBox_UP = PushButton(SpinBox_buttons, grid=[0,0],text="+", padx=6, pady=0, image=WorkingDirectory + "/images/button_up.png", width=10, height=5, command=increase_steps)
SpinBox_UP.font = "Arial"
SpinBox_Down = PushButton(SpinBox_buttons, grid=[0,1],text="-", padx=6, pady=0, image=WorkingDirectory + "/images/button_down.png", width=10, height=5, command=decrease_steps)
SpinBox_Down.font = "Arial"
#------------------------------------------------------------

UseXL_CheckBox = CheckBox(ProjectInputBox,grid=[0,10], align="left", text="Use Stable Diffusion XL 1.0 instead of Stable Diffusion 1.5")
UseXL_CheckBox.font = "Arial"

if (sd.GetXL() == True):
    UseXL_CheckBox.toggle()

#horizontal line
Box(ProjectInputBox, grid=[0,11],layout="grid",align="left", width=innerWidth-320, height=2, border=0).bg = "#EFEFEF"
#spacer
Box(ProjectInputBox, grid=[0,12],layout="grid",align="left", width=320, height=15, border=0)

def start_diffusing():
    if (not Diffusion.GetStatus()):
        save_project_data()
        
    Diffusion.Diffuse()

def stop_diffusing():
    Diffusion.Stop()

StartBox = Box(ProjectInputBox, grid=[0,13],layout="grid",align="left", width="fill", height=30, border=0)
Start_Button = PushButton(StartBox, grid=[0,0],text="Start", padx=6, pady=2, align="left", width=30, command=start_diffusing)
Start_Button.font = "Arial"
#StatusText = Text(StartBox, grid=[1,0], text="Waiting...", align="right", width=10, font="Arial")
#StatusText.visible = False
Box(StartBox, grid=[1,0],layout="grid",align="left", width=50, height=20, border=0)
Stop_Button = PushButton(StartBox, grid=[2,0],text="Stop", padx=6, pady=2, align="right", width=5, command=stop_diffusing)
Stop_Button.font = "Arial"
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
picture = Picture(imageBox, image=WorkingDirectory + "/images/main.png", grid=[0,0], width=320, height=320)

#vertical spacer
Box(imageBox, layout="auto", grid=[0,1], width=320, height=10, align="top", border=0)

StatusBox = Box(imageBox, layout="grid", grid=[0,2], border=0, align="left")
Text(StatusBox, grid=[0,0], text="Status:", align="left", size=9, font="Arial Black")
StatusMSG = Text(StatusBox, grid=[1,0], text="Completed...", align="left", size=10)
StatusMSG.font = "Arial"

#horizontal line
Box(imageBox, grid=[0,3],layout="grid",align="left", width=320, height=2, border=0).bg = "#EFEFEF"
#spacer
Box(imageBox, grid=[0,4],layout="grid",align="left", width=60, height=10, border=0)

#image controls
ImageActionBox = Box(imageBox, layout="grid", grid=[0,5], border=0, align="left")

Text(ImageActionBox, grid=[0,0], text="Actions ", align="left", size=9, font="Arial Black")
Box(ImageActionBox, layout="auto", grid=[1,0], border=0, align="left", width=20, height=20)
Save_Image_PushButton = PushButton(ImageActionBox, grid=[2,0],text="Save", padx=6, pady=2)
Save_Image_PushButton.font = "Arial"
Box(ImageActionBox, layout="auto", grid=[3,0], border=0, align="left", width=20, height=20)
Refine_Image_PushButton = PushButton(ImageActionBox, grid=[4,0],text="Refine", padx=6, pady=2)
Refine_Image_PushButton.font = "Arial"
Box(ImageActionBox, layout="auto", grid=[5,0], border=0, align="left", width=20, height=20)
Delete_Image_PushButton = PushButton(ImageActionBox, grid=[6,0],text="Delete", padx=6, pady=2)
Delete_Image_PushButton.font = "Arial"
#------------------------------------------------------------

#positioning the window...
positioning_window(guiWidth, guiHeight, main_window)

def save_project_data():
    sd.SetName(ProjectName.value)
    sd.SetPosPrompt(PositivePrompt.value)
    sd.SetNegPrompt(NegativePrompt.value)
    sd.SetImage(TargetImage.value)
    sd.SetSteps(Steps_TextBox.value)
    sd.SetXL(UseXL_CheckBox.value)
    sd.Save()

def DisableVisuals():
    ProjectName.enabled = False
    PositivePrompt.enabled = False
    NegativePrompt.enabled = False
    TargetImage.enabled = False
    Steps_TextBox.enabled = False
    UseXL_CheckBox.enabled = False
    SpinBox_UP.enabled = False
    SpinBox_Down.enabled = False
    Start_Button.enabled = False
    picture.image = WorkingDirectory + "/images/loading.png"

def EnableVisuals():
    ProjectName.enabled = True
    PositivePrompt.enabled = True
    NegativePrompt.enabled = True
    TargetImage.enabled = True
    Steps_TextBox.enabled = True
    UseXL_CheckBox.enabled = True
    SpinBox_UP.enabled = True
    SpinBox_Down.enabled = True
    Start_Button.enabled = True
    picture.image = WorkingDirectory + "/images/main.png"

    

def GetThreadStatus():
    if (Diffusion.GetStatus() == True):
        StatusMSG.value = "Processing..."
        DisableVisuals()
    else:
        StatusMSG.value = "Ready"

    if (Diffusion.GetProcessingResult() == True):
        StatusMSG.value = "Finished!"
        EnableVisuals()

        if os.path.isfile(sd.GetImage()):
            picture.image = sd.GetImage()    


mygui.GetMainWindow().repeat(1000, GetThreadStatus)


#showing the gui
mygui.Show()
