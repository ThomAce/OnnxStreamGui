import os
from guizero import Window, App, Text, Box, TextBox, PushButton, TitleBox, Picture

#------------------------------------------------------------
# Settings Class for handling SDGUI configuration data
#------------------------------------------------------------

class Settings:
    def __init__(self):
        self.status = False
        self.sd_file = ""
        self.sdxl_file = ""
        self.configfile = "Settings.txt"
        self.cwd = os.getcwd()

    def SetSDFile(self, file):
        self.sd_file = file

    def GetSDDir(self):
        return os.path.dirname(self.sd_file)

    def GetSDFile(self):
        return self.sd_file


    def SetSDXLFile(self, file):
        self.sdxl_file = file

    def GetSDXLDir(self):
        return os.path.dirname(self.sdxl_file)

    def GetSDXLFile(self):
        return self.sdxl_file
    

    def Load(self):
        try:
            data = eval(open(self.cwd + "/" + self.configfile).read())
            self.SetSDFile(data["SD"])
            self.SetSDXLFile(data["SDXL"])
            
            return True
        except:
            return False
            pass

    def Save(self):
        try:              
            f = open(self.cwd + "/" + self.configfile, "w")
                
            f.write("""{
    \"SD\": \"""" + self.GetSDFile().strip() + """\",
    \"SDXL\": \"""" + self.GetSDXLFile().strip() + """\"
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
        
        Box(app, grid=[0,0], width=20, height=20)
        Box(app, grid=[1,0], width=60, height=20)
        
        Box(app, grid=[0,1], width=20, height=20)

        def select_sd():
            selected_file = app.select_file(title="Select SD 1.5 ", folder=".", filetypes=[["All files", "*.*"]], save=False, filename="")
            if (selected_file != ""):
                SD_Path.value = selected_file
            return
        
        SDPath = TitleBox(app, "Path to Stable Diffusion 1.5 executable", grid=[1,1], layout="grid")
        SDPath.font="Arial"
        SD_Path = TextBox(SDPath, grid=[0,0], width=40, text=self.GetSDFile())
        PushButton(SDPath, grid=[1,0], text="Open",padx=6, pady=1, command=select_sd).font="Arial"

        def select_xl():
            selected_file = app.select_file(title="Select SDXL 1.0 ", folder=".", filetypes=[["All files", "*.*"]], save=False, filename="")
            if (selected_file != ""):
                SDXL_Path.value = selected_file
            return

        Box(app, grid=[0,2], width=10, height=20)
        SDXLPath = TitleBox(app, "Path to Stable Diffusion XL1.0 executable", grid=[1,2], layout="grid")
        SDXLPath.font="Arial"
        SDXL_Path = TextBox(SDXLPath, grid=[0,0], width=40, text=self.GetSDXLFile())
        PushButton(SDXLPath, grid=[1,0], text="Open",padx=6, pady=1, command=select_xl).font="Arial"

        Box(app, grid=[0,3], width=20, height=20)
        Box(app, grid=[1,3], width=60, height=20)

        def save():
            self.SetSDFile(SD_Path.value)
            self.SetSDXLFile(SDXL_Path.value)
            self.Save()
            app.destroy()

        Box(app, grid=[0,4], width=20, height=20)
        ButtsonBox = Box(app, grid=[1,4], width=60, height=40)
        PushButton(ButtsonBox, text="Save", width=20, height=20, padx=6, pady=4, command=save).font="Arial"

        positioning_window(380, 180, app)

        app.show()

#------------------------------------------------------------
