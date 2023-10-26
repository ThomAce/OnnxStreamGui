import os
import subprocess
import signal
import threading
import time
from subprocess import Popen, PIPE
import subprocess
import SD
import Settings
import io
import math

#------------------------------------------------------------
# Diffusion Class for handling Stable Diffusion processing thread and data
#------------------------------------------------------------

class Diffusion:
    #------------------------------------------------------------
    # initialize 
    #------------------------------------------------------------
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
        self.progress = "0%"
        self.command = ""

        self.proc = None

        self.settings.Load()
        self.sd.Load()
    #------------------------------------------------------------

    #------------------------------------------------------------
    # Getting status 
    #------------------------------------------------------------
    def GetStatus(self):
        return self.is_running
    #------------------------------------------------------------

    #------------------------------------------------------------
    # Getting progress percentage
    #------------------------------------------------------------
    def GetProgress(self):
        if not self.is_running:
            return "0%"

        return self.progress        
    #------------------------------------------------------------
        
    #------------------------------------------------------------
    # Get processing result (true or false)
    #------------------------------------------------------------
    def GetProcessingResult(self):
        return self.thread_done
    #------------------------------------------------------------

    #------------------------------------------------------------
    # Thread to handling the diffusion executable as process
    # reading output here to update the percentage and monitoring status
    #------------------------------------------------------------
    def DiffuseThread(self):
        if (self.is_running == True):
            return
        
        self.is_running = True
        self.thread_done = False

        os.chdir(self.GetWorkingDirectory())

        #good working one:
        #obsolete, will be removed. Keeping here for reference
        #self.proc = os.popen(self.command).read()

        startupinfo = None

        #pass as list of arguments if the system is linux
        cmd = self.args

        if os.name == 'nt':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            #pass as string of command
            cmd = self.command

        self.proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,cwd=self.GetWorkingDirectory(),shell=False,startupinfo=startupinfo)
        self.progress = "0%"

        time.sleep(100/1000)

        #needed for linux / rpi when the process is being started a bit slower
        nolines = 0
        
        while True:
            time.sleep(100/1000)
            
            try:
                line = str(self.proc.stdout.readline().decode("utf-8")).strip()
                
                if line.startswith("step:"):
                    line = line.split("\t")[0].replace("step:", "").strip()
                    self.progress = str(math.floor(((int(line)+1) / int(self.sd.GetSteps())) * 100 )) + "%"
                    noline = 0

                if not line or line == "b''" or line == "":
                    noline += 1
                    if noline > 5:
                        break
            except:
                break
                pass
        
        #changing back dir
        os.chdir(self.cwd)

        self.is_running = False
        self.thread_done = True
    #------------------------------------------------------------

    #------------------------------------------------------------
    # stop processing.
    # killing the process by pid and terminating the subprocess
    #------------------------------------------------------------
    def Stop(self):        
        if (self.is_running == True):
            subprocess.Popen.kill(self.proc)
            self.proc.terminate()
            self.thread_done = False
            self.is_running = False
            return

            #old code section below:
            #soon it will be removed
            
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
    #------------------------------------------------------------

    #------------------------------------------------------------
    # Get actually used stable diffusion: SD1.5 or SDXL1.0
    #------------------------------------------------------------
    def GetStableDiffusion(self):
        self.sd.Load()
        
        if (self.sd.GetXL()):
            return self.settings.GetSDXLFile()
        else:
            return self.settings.GetSDFile()
    #------------------------------------------------------------

    #------------------------------------------------------------
    # Getting process id. OBSOLETE! WILL BE REMOVED
    #------------------------------------------------------------
    def GetProcessID(self):
        if os.name == 'nt':
            return self.WindowsGetProcessID()
        else:
            return self.LinuxGetProcessID()
    #------------------------------------------------------------
        
    #------------------------------------------------------------
    # Getting process id for linux. OBSOLETE! WILL BE REMOVED
    #------------------------------------------------------------        
    def LinuxGetProcessID(self):
        path, executable = os.path.split(self.GetStableDiffusion())
        return os.popen("pidof " + executable).read().strip()
    #------------------------------------------------------------
        
    #------------------------------------------------------------
    # Getting process id for windows. OBSOLETE! WILL BE REMOVED
    #------------------------------------------------------------  
    def WindowsGetProcessID(self):
        #fix path issues
        proc_path = self.GetStableDiffusion().replace("/", "\\")

        pid = os.popen("wmic process get ProcessID,ExecutablePath | findstr /c:\"" + proc_path + "\"").read().strip()
        pid = str(pid.replace(pid.split("   ")[0].strip(), "").strip())
        
        if pid == "":
            return "-1"
        
        return pid
    #------------------------------------------------------------

    #------------------------------------------------------------
    # Getting working directory for actual SD
    #------------------------------------------------------------
    def GetWorkingDirectory(self):
        if (self.sd.GetXL()):
            return self.settings.GetSDXLDir()
        else:
            return self.settings.GetSDDir()
    #------------------------------------------------------------

    #------------------------------------------------------------
    # Automatically checking if it is a Raspberry Pi or not.
    #------------------------------------------------------------
    def is_raspberrypi(self):
        try:
            with io.open('/sys/firmware/devicetree/base/model', 'r') as m:
                if 'raspberry pi' in m.read().lower():
                    return " --rpi "
        except:
            pass
        
        return ""
    #------------------------------------------------------------
    
    #------------------------------------------------------------
    # Assemble the command line / argument list and start the thread
    #------------------------------------------------------------
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

        self.steps = self.sd.GetSteps()

        self.args += " --prompt \"" + self.sd.GetPosPrompt() + "\" "
        self.args += " --neg-prompt \"" + self.sd.GetNegPrompt() + "\" "
        self.args += " --output \"" + self.sd.GetImage() + "\" "
        self.args += " --steps " + self.sd.GetSteps() + " "
        self.args += " --seed " + str(self.sd.GetSeed()) + " "
        self.args += self.is_raspberrypi()

        #command string for windows
        self.command = self.sd_exe + " " + self.args

        #command list for linux
        self.args = [self.sd_exe]
        self.args.append("--prompt")
        self.args.append("\"" + self.sd.GetPosPrompt() + "\"")
        self.args.append("--neg-prompt")
        self.args.append("\"" + self.sd.GetNegPrompt() + "\"")
        self.args.append("--output")
        self.args.append("\"" + self.sd.GetImage() + "\"")
        self.args.append("--steps")
        self.args.append("" + self.sd.GetSteps() + "")
        self.args.append("--seed")
        self.args.append(str(self.sd.GetSeed()))
        self.args.append(self.is_raspberrypi().strip())
        
        if (self.sd.GetXL()):
            self.args.append("--xl")

        if (self.settings.GetRam()):
            self.args.append("--ram")
        
        self.dir = self.GetWorkingDirectory()
    
        self.thread = threading.Thread(target=self.DiffuseThread)
        self.thread.start()
    #------------------------------------------------------------
