# Use Tkinter for python 2, tkinter for python 3
from tkinter import E, Tk, LEFT
from tkinter import Tk, Label, StringVar, W
from tkinter import Frame, Button
from tkinter.ttk import Combobox
import sys
import glob
import serial

class ConnectionPort(Frame):
    def __init__(self, parent, arduino):
        super().__init__()
        self.parent = parent
        self.arduino = arduino
        self.portsComboboxValue = StringVar()
        self.rateComoboboxValue = StringVar()
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
        self.rate = ['9600']
        self.portNameLabel = Label(self.parent, text = "Port name: ")
        self.portNameLabel.grid(row = 0, column = 0, sticky = W)

        try:
            self.portsComboboxValue = StringVar()
            portsCombobox = Combobox(self.parent, height=4, textvariable=self.portsComboboxValue)
            portsCombobox.grid(row=0, column=1)
            portsCombobox['values'] = self.ports
            portsCombobox.bind("<<ComboboxSelected>>", self.onSelectPortName)
        except TypeError:
            print("Something is wrong with select port")

        self.outputPortNameLabel = Label(self.parent, foreground='red')
        self.outputPortNameLabel.grid(row = 1, column = 1, sticky = W)

        self.bauteRateLabel = Label(self.parent, text="Baound Rate: ")
        self.bauteRateLabel.grid(row = 2, column = 0, sticky = W)
        
        try:
            self.rateComoboboxValue = StringVar()
            rateComobobox = Combobox(self.parent, height=4, textvariable=self.rateComoboboxValue)
            rateComobobox.grid(row = 2, column = 1)
            rateComobobox['values'] = self.rate
            rateComobobox.bind("<<ComboboxSelected>>", self.onSelectRate)
        except TypeError:
            print("Something is wrong with select rate")

        self.outputBauteRateLabel = Label(self.parent, foreground='red')
        self.outputBauteRateLabel.grid(row = 3, column = 1, sticky = W)

        self.buttonConnection = Button(self.parent, text="Connect", command=self.connectArduino)
        self.buttonConnection.grid(row = 0, column = 2, padx=5)

        self.buttonConnection = Button(self.parent, text="Disconnect", command=self.disconnectArduino)
        self.buttonConnection.grid(row = 0, column = 3, padx=5)

        self.outputConnectedLabel = Label(self.parent, foreground='green')
        self.outputConnectedLabel.grid(row = 2, column = 2, columnspan=2, rowspan=1)

    def disconnectArduino(self):
        try:
            self.outputConnectedLabel['text'] = f'You are disconnected!!'
            self.outputConnectedLabel['foreground'] = 'red'
            self.arduino.closeConnection()
        except:
            print("some is wrong when disconnect arduino")

    def connectArduino(self):
        try:
            self.arduino.connectArduino(self.PORT, self.RATE)
            self.outputConnectedLabel['text'] = f'You are connected!!'
            self.outputConnectedLabel['foreground'] = 'green'
        except:
            print("some is wrong when connect arduino")

    def onSelectPortName(self, event):
        self.PORT= event.widget.get()
        self.outputPortNameLabel['text'] = f'You selected: {event.widget.get()}'
        
    def onSelectRate(self, event):
        self.RATE = event.widget.get()
        self.outputBauteRateLabel['text'] = f'You selected: {event.widget.get()}'

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
