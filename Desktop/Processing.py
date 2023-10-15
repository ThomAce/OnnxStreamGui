import os
import subprocess
import signal
import threading
import time
from subprocess import Popen, PIPE
import SD
import Settings
import io

#------------------------------------------------------------
# Diffusion Class for handling Stable Diffusion processing thread and data
#------------------------------------------------------------

class Diffusion:
    def __init__(self):
        self.is_running = False
        self.thread_done = False
        self.thread = threading.Thread()
        self.sd_exe = ""
        self.args = ""
        self.pid = -1
        self.cwd = os.getcwd()
        self.sd = SD.SD()
        self.settings = Settings.Settings()        

        self.settings.Load()
        self.sd.Load()

    def GetStatus(self):
        return self.is_running

    def GetProcessingResult(self):
        return self.thread_done

    def DiffuseThread(self):
        if (self.is_running == True):
            return
        
        self.is_running = True
        self.thread_done = False

        os.chdir(self.GetWorkingDirectory())
        
        self.proc = os.popen(self.command).read()
        
        #changing back dir
        os.chdir(self.cwd)

        self.is_running = False
        self.thread_done = True


    def Stop(self):        
        if (self.is_running == True):
            pid = int(self.GetProcessID())

            #debug:
            #print("processid: %d" % pid)

            if (pid < 1):
                print("Process could not be found!")
                return
            
            if os.name == 'nt':
                os.popen("Taskkill /PID %d /F" % pid).read()
            else:
                os.popen("kill %d" % pid).read()

            self.thread_done = False
            self.is_running = False

    def GetStableDiffusion(self):
        self.sd.Load()
        
        if (self.sd.GetXL()):
            return self.settings.GetSDXLFile()
        else:
            return self.settings.GetSDFile()

    def GetProcessID(self):
        if os.name == 'nt':
            return self.WindowsGetProcessID()
        else:
            return self.LinuxGetProcessID()
        
    def LinuxGetProcessID(self):
        path, executable = os.path.split(self.GetStableDiffusion())
        return os.popen("pidof " + executable).read().strip()

    def WindowsGetProcessID(self):
        #fix path issues
        proc_path = self.GetStableDiffusion().replace("/", "\\")

        pid = os.popen("wmic process get ProcessID,ExecutablePath | findstr /c:\"" + proc_path + "\"").read().strip()
        pid = str(pid.replace(pid.split("   ")[0].strip(), "").strip())
        
        if pid == "":
            return "-1"
        
        return pid
        
    def GetWorkingDirectory(self):
        if (self.sd.GetXL()):
            return self.settings.GetSDXLDir()
        else:
            return self.settings.GetSDDir()

    def is_raspberrypi(self):
        try:
            with io.open('/sys/firmware/devicetree/base/model', 'r') as m:
                if 'raspberry pi' in m.read().lower():
                    return " --rpi "
        except:
            pass
        
        return ""


    def Diffuse(self):
        self.settings.Load()
        
        if (self.is_running == True):
            return False        
        
        if not self.sd.Load():
            return False
        
        self.sd_exe = self.GetStableDiffusion()
        self.args = ""
        
        if (self.sd.GetXL()):
            self.args += " --xl "

        if (self.settings.GetRam()):
            self.args += " --ram "

        self.args += " --prompt \"" + self.sd.GetPosPrompt() + "\" "
        self.args += " --neg-prompt \"" + self.sd.GetNegPrompt() + "\" "
        self.args += " --output \"" + self.sd.GetImage() + "\" "
        self.args += " --steps " + self.sd.GetSteps() + " "
        self.args += " --seed " + str(self.sd.GetSeed()) + " "
        self.args += self.is_raspberrypi()

        self.command = self.sd_exe + " " + self.args
        self.dir = self.GetWorkingDirectory()
    
        self.thread = threading.Thread(target=self.DiffuseThread)
        self.thread.start()

