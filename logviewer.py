from libs import *
from log import *
from plot import *
from create_widgets import create_widgets

class Application(tk.Frame):
    def __init__(self, master = None):
        '''
        Set up the initial state of the tkinter
        window.
        '''
        
        tk.Frame.__init__(self, master)
        self.grid()

        #log_directory: where log files from the DAQ are stored
        self.log_directory = r"logs"

        #Log Viewer Variables
        self.fitlines = []
        self.datalines = []
        self.y_headers_right = []
        self.log_fits = ["Linear", "Quadratic", "Gaussian", "Exponential", "Logarithmic"]

        #Initial Functions
        populate_logs(self)
        create_widgets(self, ROOT)
        update_graph(self)

def on_closing():
    '''
    Function for closing the tkinter window
    and ending the script.
    '''
    
    ROOT.destroy()
    sys.exit()

if __name__ == "__main__":
    #Create Window and Set On Top
    ROOT = tk.Tk()
    ROOT.lift()
    ROOT.attributes("-topmost", True)
    ROOT.after_idle(ROOT.attributes, "-topmost", False)

    #Size and Position of Window
    WIDTH = 1350
    HEIGHT = 800
    X = 0
    Y = 0

    #Update Window and Run
    ROOT.geometry("%dx%d+%d+%d" % (WIDTH, HEIGHT, X, Y))
    ROOT.title("Log Viewer")
    APP = Application(ROOT)
    ROOT.protocol("WM_DELETE_WINDOW", on_closing)
    APP.mainloop()
