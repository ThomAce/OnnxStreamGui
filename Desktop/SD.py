import os
from PIL import Image
import time
import random

#------------------------------------------------------------
# SD Class for handling Stable Diffusion project data
#------------------------------------------------------------
class SD:
#------------------------------------------------------------
# generate random number
#------------------------------------------------------------
    def get_random_number(self):
        return random.randint(3, int(time.time()))
#------------------------------------------------------------
    
#------------------------------------------------------------
# initialize
#------------------------------------------------------------
    def __init__(self):
        self.name = ""
        self.posprompt = ""
        self.negprompt = ""
        self.image = ""
        self.steps = "3"
        self.seed = self.get_random_number()
        self.xl = False
        self.project_file = "Project.txt" #default project file
        self.cwd = os.getcwd()
        self.status = False
        self.thumb_created = False
#------------------------------------------------------------
        
#------------------------------------------------------------
    def SetName(self, name):
        self.name = name
#------------------------------------------------------------
    def SetPosPrompt(self, prompt):
        self.posprompt = prompt
#------------------------------------------------------------
    def SetNegPrompt(self, prompt):
        self.negprompt = prompt
#------------------------------------------------------------
    def SetImage(self, image):
        self.image = image
#------------------------------------------------------------        
    def SetSteps(self, steps):
        self.steps = steps
#------------------------------------------------------------
    def SetXL(self, xl):
        self.xl = xl
#------------------------------------------------------------
    def SetSeed(self, seed):
        if (seed == -1):
            seed = self.get_random_number()
            
        self.seed = seed
#------------------------------------------------------------
    def ResetThumb(self):
        self.thumb_created = False

#------------------------------------------------------------
    def GetName(self):
        return self.name
#------------------------------------------------------------
    def GetPosPrompt(self):
        return self.posprompt
#------------------------------------------------------------
    def GetNegPrompt(self):
        return self.negprompt
#------------------------------------------------------------
    def GetImage(self):
        return self.image
#------------------------------------------------------------

#------------------------------------------------------------
# create thumbnail if the image generated
#------------------------------------------------------------
    def GetImageThumb(self):
        if self.image == "":
            return ""
        
        if not self.thumb_created:
            image = Image.open(self.image)
            new_image = image.resize((320, 320))
            new_image.save(self.cwd + '/thumb.png')
            self.thumb_created = True
        
        return (self.cwd + '/thumb.png')
#------------------------------------------------------------
    
#------------------------------------------------------------
# Get steps
#------------------------------------------------------------
    def GetSteps(self):
        if (self.steps == ""):
            self.steps = "3"
            
        return self.steps
#------------------------------------------------------------
    
#------------------------------------------------------------
# get xl
#------------------------------------------------------------
    def GetXL(self):
        return self.xl
#------------------------------------------------------------
    
#------------------------------------------------------------
# Get status
#------------------------------------------------------------
    def GetStatus(self):
        return self.status
#------------------------------------------------------------
    
#------------------------------------------------------------
# get seed number
#------------------------------------------------------------
    def GetSeed(self, seed = 0):
        if (int(seed) < 0):
            self.SetSeed(-1)
        elif (int(seed) == 0):
           return self.seed
        else:
            self.SetSeed(int(seed))

        return self.seed
#------------------------------------------------------------

#------------------------------------------------------------
# reset project -> clean up all details
#------------------------------------------------------------
    def Reset(self):
        self.SetName("")
        self.SetPosPrompt("")
        self.SetNegPrompt("")
        self.SetImage("")
        self.SetSteps("")
        self.SetXL(False)
        self.status = False
        self.thumb_created = False
#------------------------------------------------------------

#------------------------------------------------------------
# load project file and process content
#------------------------------------------------------------
    def LoadProjectFile(self, project_file):
        if (len(project_file.strip()) < 3):
            return False
        
        try:
            data = eval(open(project_file).read())

            self.SetName(data["name"])
            self.SetPosPrompt(data["posprompt"])
            self.SetNegPrompt(data["negprompt"])
            self.SetImage(data["image"])
            self.SetSteps(data["steps"])
            self.SetXL(data["xl"])

            if (data["seed"] < 0):
                self.SetSeed(-1)
            else:
                self.SetSeed(data["seed"])
                
            self.status = True
            
            self.Save()
            
            return True
        except:
            return False
            pass
#------------------------------------------------------------

#------------------------------------------------------------
# load project data
#------------------------------------------------------------
    def Load(self):
        try:
            data = eval(open(self.cwd + "/" + self.project_file).read())

            self.SetName(data["name"].strip())
            self.SetPosPrompt(data["posprompt"].strip())
            self.SetNegPrompt(data["negprompt"].strip())
            self.SetImage(data["image"].strip())
            self.SetSteps(data["steps"].strip())
            self.SetXL(data["xl"])

            try:
                if (data["seed"] < 0):
                    self.SetSeed(-1)
                else:
                    self.SetSeed(data["seed"])
            except:
                self.SetSeed(-1)

            if (self.GetName() != "" and self.GetPosPrompt() != ""):
                self.status = True
            else:
                self.status = False
            
            return True
        except:
            self.SetName("")
            self.SetPosPrompt("")
            self.SetNegPrompt("")
            self.SetImage("")
            self.SetSteps("")
            self.SetXL(False)
            self.SetSeed(-1)
            self.status = False
            
            return False

            pass
#------------------------------------------------------------
        
#------------------------------------------------------------
# save project data to file
#------------------------------------------------------------
    def Save(self, save_as = ""):
        try:
            if (save_as != ""):
                f = open(save_as, "w")
            else:  
                f = open(self.cwd + "/" + self.project_file, "w")
                
            f.write("""{
    \"name\": \"""" + self.GetName().replace("\n", " ").replace("\r", "").strip() + """\",
    \"posprompt\": \"""" + self.GetPosPrompt().replace("\n", " ").replace("\r", "").strip() + """\",
    \"negprompt\": \"""" + self.GetNegPrompt().replace("\n", " ").replace("\r", "").strip() + """\",
    \"image\": \"""" + self.GetImage().replace("\n", " ").replace("\r", "").replace("\\", "\\\\").strip() + """\",
    \"steps\": \"""" + self.GetSteps().replace("\n", " ").replace("\r", "").strip() + """\",
    \"xl\": """ + str(self.GetXL()) + """,
    \"seed\":""" + str(self.GetSeed()) + """
}""")
            f.close()
            return True
        except:
            return False
            pass
        
#------------------------------------------------------------

#------------------------------------------------------------
# end of the script
#------------------------------------------------------------
