import os
import subprocess
import signal
import threading
import time
from subprocess import Popen, PIPE
import SD

class Diffusion:
    def __init__(self):
        self.is_running = False
        self.thread_done = False
        self.thread = threading.Thread()
        self.sd = ""
        self.args = ""
        self.pid = -1
        self.cwd = os.getcwd()

    def GetStatus(self):
        #return self.thread.is_alive()
        return self.is_running

    def GetProcessingResult(self):
        return self.thread_done

    def DiffuseThread(self):
        if (self.is_running == True):
            return
        
        self.is_running = True
        self.thread_done = False
        
        os.chdir(self.dir)        
        self.proc = os.popen(self.command).read()
        
        #changing back dir
        os.chdir(self.cwd)

        self.is_running = False
        self.thread_done = True


    def Stop(self):        
        if (self.is_running == True): 
            self.thread_done = False
            self.is_running = False
            
            os.popen("Taskkill /PID %d /F" % int(self.GetProcessID())).read()

            if self.thread.is_alive() == True:
                print("Thread is still alive :(")

    def GetStableDiffusion(self):
        #returns the stable diffusion path as OS requirements
        #later on it will be replaced with configuration editor.
        if os.name == 'nt':
            return "D:\\SD\\sd.exe"
        else:
            #use shell execute
            return "./sd"

    def GetProcessID(self):
        if os.name == 'nt':
            return self.WindowsGetProcessID()
        else:
            #use shell execute
            #some other commands for getting the right data...
            return "./sd"

    def WindowsGetProcessID(self):
        proc_path = self.GetStableDiffusion()
        
        Processes = str(subprocess.check_output(['wmic', 'process', 'list', 'full'])).split("\\r\\r\\n")

        i = 0
        for p in Processes:
            if (p.replace("\\\\", "\\").strip().endswith("=" + proc_path)):
                return Processes[i+2].split("=")[1].strip()

            i += 1
        
        return "-1"

    def GetWorkingDirectory(self):
        return "D:\\SD\\"
        
    def Diffuse(self):
        if (self.is_running == True):
            return False

        sd = SD.SD()
        
        if not sd.Load():
            return False
        
        self.sd = self.GetStableDiffusion()
        self.args = ""
        
        if (sd.GetXL()):
            self.args += " --xl "

        self.args += " --prompt \"" + sd.GetPosPrompt() + "\" "
        self.args += " --neg-prompt \"" + sd.GetNegPrompt() + "\" "
        self.args += " --output \"" + sd.GetImage() + "\" "
        self.args += " --steps \"" + sd.GetSteps() + "\" "
        #"--xl --prompt \"" + sd.GetPosPrompt() + "\" --neg-prompt \"blurry\" --output \"testfile.png\" --steps 3 "

        self.command = self.sd + " " + self.args
        self.dir = self.GetWorkingDirectory()

        self.thread = threading.Thread(target=self.DiffuseThread)
        self.thread.start()

