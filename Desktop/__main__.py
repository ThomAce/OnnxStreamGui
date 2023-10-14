#!/usr/bin/env python3


#------------------------------------------------------------
# REQUIREMENTS:
#
# Python3
# guizero
# PIL (pillow)
#------------------------------------------------------------

from guizero import App, Text, Box, TextBox, PushButton, TitleBox, Picture, Drawing, CheckBox
import tkinter
import gui
import os
import Processing
import SD
import shutil
import Settings
import webbrowser
import time



start_time = time.time()
stop_time = -1

#------------------------------------------------------------
# start measuring processing time
#------------------------------------------------------------
def start_measure_processing():
    global start_time
    global stop_time

    start_time = time.time()
    stop_time = -1
#------------------------------------------------------------
    
#------------------------------------------------------------
# stop measure processing time
#------------------------------------------------------------
def stop_measure_processing():
    global stop_time
    
    if (stop_time > -1):
        return
    
    stop_time = (time.time() - start_time)
#------------------------------------------------------------

#------------------------------------------------------------
# calculating processing time... later on it will be moved to a class
#------------------------------------------------------------
def processing_time():
    global start_time
    global stop_time
    
    if (stop_time > -1):
        runtime = int(stop_time)
    else:
        runtime = (time.time() - start_time)
    
    if (runtime < 60):
        return str(runtime) + " sec"
    elif (runtime <= 3600):
        if (str(runtime % 60) == 0):
           return str(runtime // 60) + " min "
        
        return str(runtime // 60) + " min " + str(runtime % 60) + " sec"
    elif (runtime > 3600):
        runtime = (runtime // 60)
        return str(runtime // 60) + " hr " + str(runtime % 60) + " min"
#------------------------------------------------------------
    
sd = SD.SD()
sd.Load()

settings = Settings.Settings()
settings.Load()

#------------------------------------------------------------
#default settings parameters for the gui
#do not change it unless you have strong reasons for that!
#------------------------------------------------------------
guiWidth = 860
guiHeight = 540
innerWidth = (guiWidth-92)
innerHeight = 400
#------------------------------------------------------------

#------------------------------------------------------------
#global variables for storing details...
#------------------------------------------------------------

WorkingDirectory = os.getcwd()

Steps = int(sd.GetSteps())

Diffusion = Processing.Diffusion()
#------------------------------------------------------------

#------------------------------------------------------------
# creating gui elements
#------------------------------------------------------------
mygui = gui.GUI()
mygui.CreateWindow("OnnxStream GUI", guiWidth, guiHeight)
main_window = mygui.GetMainWindow()
app = main_window
main_window.bg = "#F4F4F4"

master = mygui.DrawWindow()
innerbox = mygui.DrawMain(innerWidth, innerHeight)
#------------------------------------------------------------


#------------------------------------------------------------
#header controls, like settings, help buttons, etc...
#some kind of a top menu, but in a custom way, because I like this more
#------------------------------------------------------------
HeaderControls = Box(master, layout="grid", grid=[0,0], width=guiWidth, height=35, align="top", border=0)

#spacer left
Box(HeaderControls, layout="grid", grid=[0,0], width=46, height=35, align="right", border=0)
HeaderText_box = Box(HeaderControls, layout="grid", grid=[1,0], width=(innerWidth-120), height=35, align="left", border=0)
HeaderControls_inner = Box(HeaderControls, layout="grid", grid=[2,0], width=120, height=35, align="right", border=0)
#spacer right
Box(HeaderControls, layout="grid", grid=[3,0], width=46, height=35, align="left", border=0)
#------------------------------------------------------------

#------------------------------------------------------------
#header text, info text, etc...
#------------------------------------------------------------
HeaderText_box_inner = Box(HeaderText_box, layout="grid", grid=[0,0], width=(innerWidth-300)-46, height=35, align="left", border=0)
HeaderText = Text(HeaderText_box_inner, text="OnnxStream GUI", grid=[0,0], align="left")
HeaderText.font = "Arial Black"
HeaderText.text_color = "#000000"
HeaderText.size = 16
#------------------------------------------------------------

#------------------------------------------------------------
# Open settings window function
#------------------------------------------------------------
def OpenSettings():
    settings.Show(main_window)
#------------------------------------------------------------

#------------------------------------------------------------
# Open github page to the GUI in default webbrowser
#------------------------------------------------------------
def OpenGithub():
    webbrowser.open("https://github.com/ThomAce/OnnxStreamGui")
#------------------------------------------------------------

#------------------------------------------------------------
# Open OnnxStream Github page.
#------------------------------------------------------------
def OpenOnnxGithub():
    webbrowser.open("https://github.com/vitoplantamura/OnnxStream")
#------------------------------------------------------------
    
PushButton(HeaderControls_inner, grid=[0,0],text="Settings", padx=6, pady=2, align="right", command=OpenSettings).font = "Arial"
Box(HeaderControls_inner, layout="auto", grid=[1,0], border=0, align="right", width=10, height=20)
PushButton(HeaderControls_inner, grid=[2,0],text="GUI on Github", align="right", padx=6, pady=2, command=OpenGithub).font = "Arial"
Box(HeaderControls_inner, layout="auto", grid=[3,0], border=0, align="right", width=10, height=20)
PushButton(HeaderControls_inner, grid=[4,0],text="OnnxStream on Github", align="right", padx=6, pady=2, command=OpenOnnxGithub).font = "Arial"
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

#project function
#referencing to a later defined functions. Python trick...
#------------------------------------------------------------
def save_project():
    save_project_data()
#------------------------------------------------------------
    
#------------------------------------------------------------
def export_project():
    save_project_data()

    if (sd.GetStatus()):
        selected_file = app.select_file(title="Save Project", folder=".", filetypes=[["All files", "*.txt"]], save=True, filename="")

        if(selected_file != ""):
            sd.Save(selected_file)
#------------------------------------------------------------
    
#------------------------------------------------------------
def load_project():
    if (sd.GetStatus()):
        if (not app.yesno("WARNING!", "There is a loaded project. Do you wish to overwrite it?")):
            return

    if (not sd.LoadProjectFile(app.select_file(title="Select Project", folder=".", filetypes=[["All files", "*.txt"]], save=False, filename=""))):
            app.warn("WARNING!", "Project file is not loaded!")
    else:
        load_project_data()
#------------------------------------------------------------
        
#------------------------------------------------------------
def new_project():
    if (not app.yesno("WARNING!", "Do you really wanted to reset all fields?")):        
        return

    reset_project_data()
    sd.Reset()
#------------------------------------------------------------    

ProjectActionBox = Box(inputbox, layout="grid", grid=[0,0], border=0, align="left")
Text(ProjectActionBox, grid=[0,0], text="Project Actions", align="left", size=9, font="Arial Black")
Box(ProjectActionBox, layout="auto", grid=[1,0], border=0, align="left", width=20, height=20)
SaveProject_PushButton = PushButton(ProjectActionBox, grid=[2,0],text="Save", padx=6, pady=1, command=save_project)
SaveProject_PushButton.font = "Arial"
Box(ProjectActionBox, layout="auto", grid=[3,0], border=0, align="left", width=20, height=20)
LoadProject_PushButton = PushButton(ProjectActionBox, grid=[4,0],text="Load", padx=6, pady=1, command=load_project)
LoadProject_PushButton.font = "Arial"
Box(ProjectActionBox, layout="auto", grid=[5,0], border=0, align="left", width=20, height=20)
LoadProject_PushButton = PushButton(ProjectActionBox, grid=[6,0],text="Export", padx=6, pady=1, command=export_project)
LoadProject_PushButton.font = "Arial"
Box(ProjectActionBox, layout="auto", grid=[7,0], border=0, align="left", width=20, height=20)
NewProject_PushButton = PushButton(ProjectActionBox, grid=[8,0],text="New", padx=6, pady=1, command=new_project)
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

#------------------------------------------------------------
# opening target image location... "where to save"
#------------------------------------------------------------
def open_target_image():
    save_path = app.select_file(title="Save generated image file", folder=".", filetypes=[["All files", "*.png"]], save=True, filename="")

    if os.path.isfile(save_path):
        if (not app.yesno("WARNING!", "The file already exists!\r\nDo you wish to overwrite?")):
            return

    TargetImage.value = save_path
#------------------------------------------------------------
    
OpenTargetImage_PushButton = PushButton(TargetImage_Box, command=open_target_image, grid=[2,0], width=18, height=18, align="right", image=WorkingDirectory + "/images/save_icon.png")
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
# and others...
#------------------------------------------------------------
Text(ProjectInputBox, grid=[0,8], text="Steps and Seed", align="left", size=9, font="Arial Black")

#------------------------------------------------------------
# this function is called uppon text changed
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

    Steps = int(getTextBoxValue(getTextBoxObj()))
#------------------------------------------------------------
    
#------------------------------------------------------------
# increase steps
#------------------------------------------------------------
def increase_steps():
    global Steps    
        
    if Steps >= 100:
        return
    
    Steps += 1
    Steps_TextBox.value = str(Steps)
#------------------------------------------------------------

#------------------------------------------------------------
# decrease steps
#------------------------------------------------------------
def decrease_steps():
    global Steps    
        
    if Steps <= 3:
        return
    
    Steps -= 1
    Steps_TextBox.value = str(Steps)
#------------------------------------------------------------

#------------------------------------------------------------
# Spinbox for holding steps and other controls
#------------------------------------------------------------
SpinBox = Box(ProjectInputBox, grid=[0,9],layout="grid",align="left", width="fill", height="fill", border=0)
Text(SpinBox, grid=[0,0], text="Steps:", align="left", size=9, font="Arial Black")
Box(SpinBox, grid=[1,0],layout="grid",align="left", width=10, height=10, border=0) #spacer
SpinBox_text = Box(SpinBox, grid=[2,0],align="left", width="fill", height="fill")
Steps_TextBox = TextBox(SpinBox_text, text=sd.GetSteps(), align="left", width="4",command=steps_text_changed)
Steps_TextBox.font = "Arial"
#------------------------------------------------------------

#------------------------------------------------------------
# getting textobx object for steps
#------------------------------------------------------------
def getTextBoxObj():
    return Steps_TextBox
#------------------------------------------------------------

#------------------------------------------------------------
# Spinbox imitation with up and down buttons
#------------------------------------------------------------
SpinBox_buttons = Box(SpinBox, grid=[3,0], layout="grid",align="left", width="fill", height="fill")
SpinBox_UP = PushButton(SpinBox_buttons, grid=[0,0],text="+", padx=6, pady=0, image=WorkingDirectory + "/images/button_up.png", width=10, height=5, command=increase_steps)
SpinBox_UP.font = "Arial"
SpinBox_Down = PushButton(SpinBox_buttons, grid=[0,1],text="-", padx=6, pady=0, image=WorkingDirectory + "/images/button_down.png", width=10, height=5, command=decrease_steps)
SpinBox_Down.font = "Arial"
#------------------------------------------------------------

#------------------------------------------------------------
# making a new random seed number
#------------------------------------------------------------
def random_seed():
    sd.SetSeed(-1)
    set_seed()
    return
#------------------------------------------------------------

#------------------------------------------------------------
# this function called uppon content of seed textbox changed
#------------------------------------------------------------
def seed_changed(text):
    if getTextBoxValue(getSeedBox()).isnumeric() == False:
        sd.SetSeed(-1)
        getSeedBox().value = str(sd.GetSeed())
        return

    sd.SetSeed(int(getSeedBox().value))
    getSeedBox().value = sd.GetSeed()
#------------------------------------------------------------

#------------------------------------------------------------
# Seed and the buttons for these controls
#------------------------------------------------------------
SeedBox = Box(SpinBox, grid=[4,0],align="left", width="fill", height="fill",layout="grid")
Box(SeedBox, grid=[0,0],layout="grid",align="left", width=10, height=10, border=0)  #spacer
Text(SeedBox, grid=[1,0], text="Seed:", align="left", size=9, font="Arial Black")
Box(SeedBox, grid=[2,0],layout="grid",align="left", width=10, height=10, border=0)  #spacer
SeedBox_TextBox = TextBox(SeedBox, grid=[3,0], text=sd.GetSeed(), align="left", width="12",command=seed_changed)
SeedBox_TextBox.font = "Arial"
Box(SeedBox, grid=[4,0],layout="grid",align="left", width=10, height=10, border=0)  #spacer
SeedBox_PushButton = PushButton(SeedBox, grid=[5,0],text=" ", padx=6, pady=0, width=18, height=18, image=WorkingDirectory + "/images/dice_icon.png", command=random_seed)
#------------------------------------------------------------

#------------------------------------------------------------
# return seedbox textbox widget object
#------------------------------------------------------------
def getSeedBox():
    return SeedBox_TextBox
#------------------------------------------------------------

#------------------------------------------------------------
# return textbox value
#------------------------------------------------------------
def getTextBoxValue(TextBoxObj):
    return TextBoxObj.value #Steps_TextBox.value
#------------------------------------------------------------

#------------------------------------------------------------
# set seed value from project file
#------------------------------------------------------------
def set_seed():
    SeedBox_TextBox.value = sd.GetSeed()
#------------------------------------------------------------

#------------------------------------------------------------
# Checkbox for switching between SD and SDXL
#------------------------------------------------------------
UseXL_CheckBox = CheckBox(ProjectInputBox,grid=[0,10], align="left", text="Use Stable Diffusion XL 1.0 instead of Stable Diffusion 1.5")
UseXL_CheckBox.font = "Arial"

if (sd.GetXL() == True):
    UseXL_CheckBox.toggle()
#------------------------------------------------------------

#------------------------------------------------------------
#horizontal line
#------------------------------------------------------------
Box(ProjectInputBox, grid=[0,11],layout="grid",align="left", width=innerWidth-320, height=2, border=0).bg = "#EFEFEF"
Box(ProjectInputBox, grid=[0,12],layout="grid",align="left", width=320, height=15, border=0) #horizontal spacer
#------------------------------------------------------------


#------------------------------------------------------------
# Start diffusing procedure...
#------------------------------------------------------------
def start_diffusing():
    global start_time
    
    if (not Diffusion.GetStatus()):
        save_project_data()

    if os.path.isfile(sd.GetImage()):
        if (not app.yesno("WARNING!", "The target image will be overwritten.\r\nAre you sure?")):
            return

    start_measure_processing()

    Diffusion.Diffuse()
#------------------------------------------------------------

#------------------------------------------------------------
# Stop diffusion by user request.
#------------------------------------------------------------
def stop_diffusing():
    Diffusion.Stop()
#------------------------------------------------------------

#------------------------------------------------------------
# Start and stop buttons
#------------------------------------------------------------
StartBox = Box(ProjectInputBox, grid=[0,13],layout="grid",align="left", width="fill", height=30, border=0)
Start_Button = PushButton(StartBox, grid=[0,0],text="Start", padx=6, pady=2, align="left", width=30, command=start_diffusing)
Start_Button.font = "Arial"
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
#------------------------------------------------------------

#------------------------------------------------------------
# Saving the image to user defined location.
#------------------------------------------------------------
def save_image():
    #app.info("Not implemented", "Not yet implemented")
    selected_file = app.select_file(title="Save to file", folder=".", filetypes=[["All files", "*.png"]], save=True, filename="")

    if (selected_file != ""):
        shutil.move(sd.GetImage(), selected_file)
        EnableVisuals()
        app.info("Info", "Done!")
#------------------------------------------------------------

#------------------------------------------------------------
# Refine image function. Basically the same as Start button.
#------------------------------------------------------------
def refine_image():
    if (not app.yesno("WARNING!", "The actual file will be overwritten.\r\nAre you sure?")):
        return

    #saving project
    save_project_data()
    
    start_measure_processing()
    #starting the diffusion
    start_diffusing()
    return
#------------------------------------------------------------

#------------------------------------------------------------
# Delete image function.
#------------------------------------------------------------
def delete_image():
    if (not app.yesno("WARNING!", "The actual file will be deleted.\r\nAre you sure?")):
        return

    try:
        os.remove(sd.GetImage())
        EnableVisuals()
        app.info("Info", "Done!")
    except:
        app.error("Error", "File could not be deleted!")
        pass
#------------------------------------------------------------

#------------------------------------------------------------
# Action buttons for save, refine, delete image.
#------------------------------------------------------------
Text(ImageActionBox, grid=[0,0], text="Actions ", align="left", size=9, font="Arial Black")
Box(ImageActionBox, layout="auto", grid=[1,0], border=0, align="left", width=20, height=20)
Save_Image_PushButton = PushButton(ImageActionBox, grid=[2,0],text="Save", padx=6, pady=2, command=save_image)
Save_Image_PushButton.font = "Arial"
Box(ImageActionBox, layout="auto", grid=[3,0], border=0, align="left", width=20, height=20)
Refine_Image_PushButton = PushButton(ImageActionBox, grid=[4,0],text="Refine", padx=6, pady=2, command=refine_image)
Refine_Image_PushButton.font = "Arial"
Box(ImageActionBox, layout="auto", grid=[5,0], border=0, align="left", width=20, height=20)
Delete_Image_PushButton = PushButton(ImageActionBox, grid=[6,0],text="Delete", padx=6, pady=2, command=delete_image)
Delete_Image_PushButton.font = "Arial"
#------------------------------------------------------------

#------------------------------------------------------------
# saving project data
#------------------------------------------------------------
def save_project_data():
    sd.SetName(ProjectName.value)
    sd.SetPosPrompt(PositivePrompt.value)
    sd.SetNegPrompt(NegativePrompt.value)
    sd.SetImage(TargetImage.value)
    sd.SetSteps(Steps_TextBox.value)
    sd.SetXL(UseXL_CheckBox.value)
    sd.SetSeed(SeedBox_TextBox.value)
    sd.Save()
#------------------------------------------------------------

#------------------------------------------------------------
# loading the project data file
#------------------------------------------------------------
def load_project_data():
    ProjectName.value = sd.GetName()
    PositivePrompt.value = sd.GetPosPrompt()
    NegativePrompt.value = sd.GetNegPrompt()
    TargetImage.value = sd.GetImage()
    Steps_TextBox.value = sd.GetSteps()
    SeedBox_TextBox.value = sd.GetSeed()
    UseXL_CheckBox.value = sd.GetXL()
#------------------------------------------------------------

#------------------------------------------------------------
# reset all project data to "empty"
#------------------------------------------------------------
def reset_project_data():
    ProjectName.value = ""
    PositivePrompt.value = ""
    NegativePrompt.value = ""
    TargetImage.value = ""
    Steps_TextBox.value = ""
    SeedBox_TextBox.value = sd.GetSeed(-1)
    UseXL_CheckBox.value = False
#------------------------------------------------------------

#------------------------------------------------------------
# disable most visual elements on main form to avoid unwanted user inputs during processing
#------------------------------------------------------------
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
    OpenTargetImage_PushButton.enabled = False
    ProjectActionBox.enabled = False
    SeedBox_TextBox.enabled = False
    SeedBox_PushButton.enabled = False
    
    picture.image = WorkingDirectory + "/images/loading.png"
#------------------------------------------------------------

#------------------------------------------------------------
# disable image action buttions below the generated image
#------------------------------------------------------------
def DisableImageActionButtons():
    Save_Image_PushButton.enabled = False
    Refine_Image_PushButton.enabled = False
    Delete_Image_PushButton.enabled = False
#------------------------------------------------------------

#------------------------------------------------------------
# enable image action buttions below the generated image
#------------------------------------------------------------
def EnableImageActionButtons():
    Save_Image_PushButton.enabled = True
    Refine_Image_PushButton.enabled = True
    Delete_Image_PushButton.enabled = True
#------------------------------------------------------------

#------------------------------------------------------------
# Enabling visual elemenets
#------------------------------------------------------------
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
    OpenTargetImage_PushButton.enabled = True
    ProjectActionBox.enabled = True
    SeedBox_TextBox.enabled = True
    SeedBox_PushButton.enabled = True
   
    picture.image = WorkingDirectory + "/images/main.png"
#------------------------------------------------------------

#------------------------------------------------------------
# this is responsible for a visual update during processing
# nothing more just some visual stuffs for entertaining purposes
#------------------------------------------------------------
proc_steps = 0

def get_proc_msg():
    global proc_steps

    proc_steps += 1

    if proc_steps > 3:
        proc_steps = 0
        return "Processing"
    elif proc_steps == 3:
        return "Processing..."
    elif proc_steps == 2:
        return "Processing.."
    elif proc_steps == 1:
        return "Processing."

    return "Processing"
#------------------------------------------------------------

#------------------------------------------------------------
# Get thread status every seconds
# it will control the visual elements accordingly.
#------------------------------------------------------------
def GetThreadStatus():
    if (Diffusion.GetStatus() == True):
        StatusMSG.value = get_proc_msg()#"Processing..."
        DisableVisuals()
        DisableImageActionButtons()
        Stop_Button.enabled = True
    else:
        StatusMSG.value = "Ready"
        DisableImageActionButtons()

        if os.path.isfile(sd.GetImage()):
            picture.image = sd.GetImageThumb()
            EnableImageActionButtons()

    if (Diffusion.GetProcessingResult() == True):
        StatusMSG.value = "Finished! "
        stop_measure_processing()
        StatusMSG.value += processing_time()
        EnableVisuals()
        Stop_Button.enabled = False

        if os.path.isfile(sd.GetImage()):
            picture.image = sd.GetImageThumb()
            EnableImageActionButtons()
#------------------------------------------------------------

            
DisableImageActionButtons()
    
Stop_Button.enabled = False

app.repeat(1000, GetThreadStatus)


#showing the gui
mygui.Show()

#------------------------------------------------------------
# end of the script
#------------------------------------------------------------
