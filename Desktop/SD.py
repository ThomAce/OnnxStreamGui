import os

#------------------------------------------------------------
# SD Class for handling Stable Diffusion project data
#------------------------------------------------------------
class SD:
    def __init__(self):
        self.name = ""
        self.posprompt = ""
        self.negprompt = ""
        self.image = ""
        self.steps = ""
        self.xl = False
        self.project_file = "Project.txt"
        self.cwd = os.getcwd()

    def SetName(self, name):
        self.name = name

    def SetPosPrompt(self, prompt):
        self.posprompt = prompt

    def SetNegPrompt(self, prompt):
        self.negprompt = prompt

    def SetImage(self, image):
        self.image = image
        
    def SetSteps(self, steps):
        self.steps = steps

    def SetXL(self, xl):
        self.xl = xl


    def GetName(self):
        return self.name

    def GetPosPrompt(self):
        return self.posprompt

    def GetNegPrompt(self):
        return self.negprompt

    def GetImage(self):
        return self.image

    def GetSteps(self):
        return self.steps

    def GetXL(self):
        return self.xl

    def Load(self):
        try:
            data = eval(open(self.cwd + "/" + self.project_file).read())

            self.SetName(data["name"])
            self.SetPosPrompt(data["posprompt"])
            self.SetNegPrompt(data["negprompt"])
            self.SetImage(data["image"])
            self.SetSteps(data["steps"])
            self.SetXL(data["xl"])

            return True
        except:
            return False
            pass
        
    def Save(self):
        f = open(self.cwd + "/" + self.project_file, "w")
        f.write("""{
\"name\": \"""" + self.GetName().replace("\n", " ").replace("\r", "").strip() + """\",
\"posprompt\": \"""" + self.GetPosPrompt().replace("\n", " ").replace("\r", "").strip() + """\",
\"negprompt\": \"""" + self.GetNegPrompt().replace("\n", " ").replace("\r", "").strip() + """\",
\"image\": \"""" + self.GetImage().replace("\n", " ").replace("\r", "").replace("\\", "\\\\").strip() + """\",
\"steps\": \"""" + self.GetSteps().replace("\n", " ").replace("\r", "").strip() + """\",
\"xl\": """ + str(self.GetXL()) + """
}""")
        f.close()
        
#------------------------------------------------------------        

##sd = SD()
##sd.Load()
##
##print(sd.GetName())
##
##sd.SetName("NEW PROJECT")
##
##print(sd.GetName())
##
##sd.Save()
##
##sd.Load()
