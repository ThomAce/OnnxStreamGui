from guizero import Box, Drawing

class ProgressBar:
    def __init__(self, container):
        #set initial sizes, colors, etc...
        self.box = Box(container, width=10, height=10, border=0, align="left")
        self.box.visible = False
        self.box.width = 100
        self.box.height = 10
        self.box.align="left"
        
        self.drawing = Drawing(self.box, width=10, height=10)

        self.barWidth = 100
        self.barHeight = 10
        self.barColor = "#0000FF"
        self.barBgColor = "#EFEFEF"
        self.barHighValueSet = False
        self.barHighColor = "#FF0000"
        self.barHighValue = 75
    #------------------    


    def Width(self, w):
        self.box.width = w
        self.drawing.width = w
        self.barWidth = w
    #------------------

        
    def Height(self, h):
        self.box.height = h
        self.drawing.height = h
        self.barHeight = h
    #------------------


    def BGColor(self, color):
        self.barBgColor = color
        self.drawing.rectangle(0, 0, 100, 5, color=self.barBgColor)
    #------------------
        

    def BarColor(self, color, high_color="", high_value=-1):
        self.barColor = color

        if (high_color != "") and (high_value > 0):
            self.barHighColor = high_color
            self.barHighValue = high_value
            self.barHighValueSet = True
        else:
            self.barHighValueSet = False
    #------------------

    def Border(self, border):
        self.box.border = border
    #------------------


    def Progress(self, value):
        if value > 100:
            value = 100
        elif value < 0:
            value = 0

        self.drawing.clear()
        
        self.drawing.rectangle(0, 0, self.barWidth, self.barHeight, color=self.barBgColor)
        
        self.drawing.rectangle(0, 0, 0, self.barHeight, color=self.barColor)     
        
        if (self.barHighValueSet == True) and (value >= self.barHighValue):
            self.drawing.rectangle(0, 0, round((self.box.width / 100) * value), self.barHeight, color=self.barHighColor)
        else:
            self.drawing.rectangle(0, 0, round((self.box.width / 100) * value), self.barHeight, color=self.barColor)
        
    #------------------
        

    def Show(self):
        self.box.visible = True
    #------------------

#------------------





