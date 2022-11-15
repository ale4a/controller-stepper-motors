# Use Tkinter for python 2, tkinter for python 3
from tkinter import E, Tk, LEFT
from tkinter import Tk, Label, StringVar, W
from tkinter import Frame, Button, PhotoImage
from tkinter.ttk import Combobox
import sys
import glob
import serial

class ConnectionPort(Frame):
    def __init__(self, parent, arduino):
        super().__init__()
        self.parent = parent
        self.arduino = arduino
        self.RATE = 9600
        self.isConnected = False
        self.onImage = PhotoImage(file = "img/on.png")
        self.offImage = PhotoImage(file = "img/off.png")
        self.portsComboboxValue = StringVar()
        self.createWidgets()

    def createWidgets(self):
        self.ports = self.connectPorts()
        if(len(self.ports) != 0):
            self.showConnection()
        else:
            self.showEmptyConnection()

    def showConnection(self, *args):
        self.selectPort()
    
    def searchPorts(self):
        self.ports = self.connectPorts()
        if (len(self.ports) != 0):
            self.schaltf1.destroy()
            self.label1.destroy()
            self.showConnection()

    def showEmptyConnection(self):
        self.label1 = Label(self.parent, text="Devices not detected ...")
        self.label1.grid(row = 0, column = 0, padx= 70, pady = 30)
        
        self.schaltf1 = Button(self.parent, text="Reload", command=self.searchPorts)
        self.schaltf1.grid(row = 0, column = 1, padx=10)

    def selectPort(self):
        padding = {"padx": 5, "pady": 10}
        self.portNameLabel = Label(self.parent, text = "Port name: ")
        self.portNameLabel.grid(row = 0, column = 0, sticky = W, **padding)

        try:
            self.portsComboboxValue = StringVar()
            portsCombobox = Combobox(self.parent, height=4, textvariable=self.portsComboboxValue)
            portsCombobox.grid(row=0, column=1, **padding)
            portsCombobox['values'] = self.ports
            portsCombobox.bind("<<ComboboxSelected>>", self.onSelectPortName)
        except TypeError:
            print("Something is wrong with select port")

        self.switchConnection = Button(self.parent, image = self.offImage, bd = 0, command = self.switchConnectionFuntion)
        self.switchConnection.grid(row = 0, column = 3, **padding)

    def switchConnectionFuntion(self):
        if self.isConnected:
            self.disconnectArduino()
        else:
            self.connectArduino()
            
    def disconnectArduino(self):
        try:
            self.arduino.closeConnection()
            self.isConnected = False
            self.switchConnection.config(image = self.offImage)
        except:
            print("some is wrong when disconnect arduino")

    def connectArduino(self):
        try:
            self.arduino.connectArduino(self.PORT, self.RATE)
            self.isConnected = True
            self.switchConnection.config(image = self.onImage)
        except:
            print("some is wrong when connect arduino")

    def onSelectPortName(self, event):
        self.PORT= event.widget.get()
        
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

class GUI(Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent)
        self.parent = parent
        self.parent.geometry("500x300")
        self.parent.title('Software to scanner')
        self.connectionPort = ConnectionPort(self, '*ARDUINO*')
        self.connectionPort.pack(side = LEFT)


if __name__ == "__main__":
    root = Tk()
    GUI(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
