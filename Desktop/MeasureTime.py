import time


#------------------------------------------------------------
# Timer Class for measuring elapsed time
#------------------------------------------------------------
class Timer:
#------------------------------------------------------------
# initialize
#------------------------------------------------------------
    def __init__(self):
        self.start_time = time.time()
        self.stop_time = -1
        self.runtime = -1
#------------------------------------------------------------
        
#------------------------------------------------------------
# Start measuring
#------------------------------------------------------------
    def start(self):
        self.start_time = time.time()
        self.stop_time = -1
        self.runtime = -1
#------------------------------------------------------------

#------------------------------------------------------------
# Stop measuring
#------------------------------------------------------------
    def stop(self):
        if (self.stop_time > -1):
            return

        self.stop_time = time.time()
        self.runtime = (time.time() - self.start_time)
#------------------------------------------------------------

#------------------------------------------------------------
# Get values
#------------------------------------------------------------
    def get(self):
        if (self.runtime > -1):
            actual = int(self.runtime)
        else:
            actual = int(time.time() - self.start_time)
        
        if (actual < 60):
            return str(actual) + " sec"
        elif (actual <= 3600):
            if (str(actual % 60) == 0):
               return str(actual // 60) + " min "
            return str(actual // 60) + " min " + str(actual % 60) + " sec"
        elif (actual > 3600):
            actual = (actual // 60)
            return str(actual // 60) + " hr " + str(actual % 60) + " min"
#------------------------------------------------------------

#------------------------------------------------------------
# end of the script
#------------------------------------------------------------
