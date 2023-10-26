import os
from guizero import Window, App, Text, Box, TextBox, PushButton, TitleBox, CheckBox

#------------------------------------------------------------
# Settings Class for handling SDGUI configuration data
#------------------------------------------------------------

class Settings:
    def __init__(self):
        self.status = False
        self.sd_file = ""
        self.sdxl_file = ""
        self.ram = False
        self.configfile = "Settings.txt"        
        self.cwd = os.getcwd()


    #setters

    def SetSDFile(self, file):
        self.sd_file = file

    def SetSDXLFile(self, file):
        self.sdxl_file = file

    def SetRam(self, ram):
        self.ram = ram

    #getters

    def GetSDXLDir(self):
        return os.path.dirname(self.sdxl_file)

    def GetSDXLFile(self):
        return self.sdxl_file

    def GetSDDir(self):
        return os.path.dirname(self.sd_file)

    def GetSDFile(self):
        return self.sd_file

    def GetRam(self):
        return self.ram
    

    def Load(self):
        try:
            data = eval(open(self.cwd + "/" + self.configfile).read())
            self.SetSDFile(data["SD"])
            self.SetSDXLFile(data["SDXL"])
            self.SetRam(False)

            if data["RAM"] == "1":
                self.SetRam(True)
            
            return True
        except:
            return False
            pass

    def Save(self):
        try:              
            f = open(self.cwd + "/" + self.configfile, "w")
                
            f.write("""{
    \"SD\": \"""" + self.GetSDFile().strip() + """\",
    \"SDXL\": \"""" + self.GetSDXLFile().strip() + """\",
    \"RAM\": \"""" + str(self.GetRam()).strip() + """\"
}""")
            f.close()
            return True
        except:
            return False
            pass

    def Show(self, master):
        app = Window(master, visible=False, title="Settings", layout="grid", width=380, height=180)
        app.tk.resizable(False,False)

        def positioning_window(window_width, window_height, app): 
            app.tk.geometry('%dx%d+%d+%d' % (window_width, window_height, ((app.tk.winfo_screenwidth() // 2) - (window_width // 2)), (app.tk.winfo_screenheight() // 2) - (window_height // 2)))

        if (not self.Load()):
            app.warn("ERROR", "No settings loaded!")

        #spacer for better visuals on all platforms
        Box(app, grid=[0,0], width=20, height=20) #spacer left
        Box(app, grid=[1,0], width=60, height=20) #holding predefined space for middle section
        Box(app, grid=[2,0], width=20, height=20) #spacer right

        def select_sd():
            selected_file = app.select_file(title="Select SD 1.5 ", folder=".", filetypes=[["All files", "*.*"]], save=False, filename="")
            if (selected_file != ""):
                SD_Path.value = selected_file
            return

        Box(app, grid=[0,1], width=20, height=20) #spacer left
        SDPath = TitleBox(app, "Path to Stable Diffusion 1.5 executable", grid=[1,1], layout="grid")
        SDPath.font="Arial"
        SD_Path = TextBox(SDPath, grid=[0,0], width=40, text=self.GetSDFile())
        PushButton(SDPath, grid=[1,0], text="Open",padx=6, pady=1, command=select_sd).font="Arial"
        Box(app, grid=[2,1], width=20, height=20) #spacer right

        def select_xl():
            selected_file = app.select_file(title="Select SDXL 1.0 ", folder=".", filetypes=[["All files", "*.*"]], save=False, filename="")
            if (selected_file != ""):
                SDXL_Path.value = selected_file
            return

        Box(app, grid=[0,2], width=10, height=20) #spacer left
        SDXLPath = TitleBox(app, "Path to Stable Diffusion XL1.0 executable", grid=[1,2], layout="grid")
        SDXLPath.font="Arial"
        SDXL_Path = TextBox(SDXLPath, grid=[0,0], width=40, text=self.GetSDXLFile())
        PushButton(SDXLPath, grid=[1,0], text="Open",padx=6, pady=1, command=select_xl).font="Arial"
        Box(app, grid=[2,2], width=20, height=20) #spacer right

        Box(app, grid=[0,3], width=10, height=20) #spacer left

        Ram_CheckBox = CheckBox(app, grid=[1,3],align="left", text="Use Ram instead of disk cache")
        Ram_CheckBox.font = "Arial"
        Box(app, grid=[2,3], width=20, height=20) #spacer right

        Ram_CheckBox.value = self.GetRam()

        def save():
            self.SetSDFile(SD_Path.value)
            self.SetSDXLFile(SDXL_Path.value)
            self.SetRam(Ram_CheckBox.value)
            self.Save()
            app.destroy()
            

        Box(app, grid=[0,4], width=20, height=20) #spacer left
        ButtonBox = Box(app, grid=[1,4], width=60, height=25)        
        PushButton(ButtonBox, text="Save", width=20, padx=6, pady=4, command=save).font="Arial"
        Box(app, grid=[2,4], width=20, height=20) #spacer right

        positioning_window(380, 180, app)

        app.show()

#------------------------------------------------------------
