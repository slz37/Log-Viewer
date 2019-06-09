from libs import *
from plot import *

def populate_logs(self):
    '''
    Obtain all log files and list them for user selection.
    '''
    
    #Get List of Logs
    self.list_logs = glob(os.path.join(self.log_directory, "2*\\"))

    #Clean Up String For Visibility
    convention = re.compile("\d+_\d+")
    self.list_logs = [convention.findall(folder) for folder in self.list_logs]

    #Reformat to Single List of Strings
    for i in range(0, len(self.list_logs)):
       self.list_logs[i] = self.list_logs[i][0]

def load_log_data(self, ROOT, error_reset):
    '''
    Load data from the user selected log file.
    '''
    
    #Get Currently Selected Log
    chosen_log = self.logvarsel.get()

    if chosen_log != "Choose a Log File":
        if error_reset == "no":
            #File Path
            file = os.path.join(self.log_directory, chosen_log, "{}.txt".format(chosen_log))

            #Load Header and Data
            self.x_headers = list(pd.read_csv(file, skiprows = 1, delimiter = "  ", engine = "python"))
            self.data = pd.read_csv(file, skiprows = 4, header = None, delim_whitespace = True)

            #Don"t Reset If Already Chosen
            if  self.xvarsel.get() == "Choose an X-Variable":
                #Destroy Old Dropdown
                self.x_select.destroy()

                #Select X Variable
                self.xvarsel = tk.StringVar(ROOT)
                self.xvarsel.set("Choose an X-Variable")
                self.x_select = tk.OptionMenu(self.fra3, self.xvarsel, *self.x_headers, command = update_graph(self))
                self.x_select.pack(side = "top")

        #Load Y Headers
        self.y_headers_left = self.x_headers[:]

        #Remove Session_ID From List - Not Needed and Causes Errors
        try:
            index = self.y_headers_left.index("sessionID")
            del self.y_headers_left[index]
        except:
            pass

        try:
            #Remove Any Element Already Plotted
            for item in self.y_headers_right:
                #Find Index in Tracker Array
                for row in self.datalines:
                    try:
                        column_index = row.index(item)
                        rowindex = self.datalines.index(row)
                    except:
                        pass

                #Remove If Same Log File
                if self.logvarsel.get() == self.datalines[rowindex][2]:
                    #Split to Y-Variable Name
                    itemsplit = item.split(" ", 1)[0]

                    #Remove From Left Side
                    self.y_headers_left.remove(itemsplit)
        except Exception as e:
            print(e,  "Line: ", sys.exc_info()[2].tb_lineno)

        #Clear Old Y Listbox
        self.listbox_not_sel.delete(0, tk.END)

        #Populate Y Listbox
        for element in self.y_headers_left:
            self.listbox_not_sel.insert(tk.END, element)

def temp_log_data(self, log):
    '''
    Load temporary log data to refill the headers in the
    appropriate order.
    '''
    
    #File Path
    file = os.path.join(self.log_directory, log, "{}.txt".format(log))

    #Load Header and Data
    new_x_headers = list(pd.read_csv(file, skiprows = 1, delimiter = "  ", engine = "python"))
    new_data = pd.read_csv(file, skiprows = 4, header = None, delim_whitespace = True)

    return new_x_headers, new_data
