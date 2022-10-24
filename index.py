



# Use Tkinter for python 2, tkinter for python 3
from tkinter import Tk, RIGHT, BOTH, RAISED, LEFT
from tkinter import Tk, LabelFrame, Label, StringVar, W
from tkinter import Frame, OptionMenu, Button

import sys
import glob
import serial

class ConectionPort(Frame):
    def __init__(self, parent = None):
        super().__init__()
        self.parent = parent
        self.createWidgets()

    def createWidgets(self):
        self.connectionContainer = LabelFrame(self)
        self.connectionContainer["text"] = " Container "
        self.connectionContainer.grid(row = 0, column = 0, columnspan = 3, pady = 10, padx = 10)

        # initialize data
        
        self.selectPort()
        

    def selectPort(self):
        paddings = {'padx': 15, 'pady': 10}
        self.languages = self.connectPorts() or ['empty']
        self.rate = ['9600', '10000', '1200']

        # portNameLabel
        self.portNameLabel = Label(self.connectionContainer)
        self.portNameLabel["text"] = "Port name:"
        self.portNameLabel.grid(row = 0, column = 0)
        self.portName = StringVar(self.connectionContainer)

        # selectPortName
        self.selectPortName = OptionMenu(
            self.connectionContainer,
            self.portName,
            *self.languages,
            command=self.onSelectPortName)
        self.selectPortName.config(width = 10)
        self.selectPortName.config(bg='light blue')
        self.selectPortName.grid(row = 0, column = 1, sticky=W, **paddings)

        # bauteRateLabel
        self.bauteRateLabel = Label(self.connectionContainer)
        self.bauteRateLabel["text"] = "Baoud Rate:"
        self.bauteRateLabel.grid(row = 2, column = 0)
        self.bauteRate = StringVar(self.connectionContainer)

        # selectBauteRate
        self.selectBauteRate = OptionMenu(
            self.connectionContainer,
            self.bauteRate,
            *self.rate,
            command=self.onSelectBauteRate)
        self.selectBauteRate.config(width = 10)
        self.selectBauteRate.config(bg='green')
        self.selectBauteRate.grid(row = 2, column = 1, sticky=W, **paddings)

        # connect
        self.outputPortNameLabel = Label(self.connectionContainer, foreground='red')
        self.outputPortNameLabel.grid(row = 1, column = 0, sticky = W, **paddings)


    def onSelectPortName(self, *args):
        self.outputPortNameLabel['text'] = f'You selected: {self.portName.get()}'

    def onSelectBauteRate(self, *args):
        print(self.bauteRate.get())

        
    def connectPorts(self):
        """ Lists serial port names
            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result

    def showDropDown(self):
        pass
    
    def showEmptyConnect(self):
        pass


        
class GUI(Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent)
        self.parent = parent
        self.parent.geometry("900x500")
        self.parent.title('Software to scanner')

        self.connectionPort = ConectionPort(self)
        self.connectionPort.pack(side = LEFT)


if __name__ == "__main__":
    root = Tk()
    GUI(root).pack(side="top", fill="both", expand=True)
    root.mainloop()


# https://stackoverflow.com/questions/17466561/best-way-to-structure-a-tkinter-application

