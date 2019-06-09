from libs import *
from move import *
from log import *
from trendline import *
from plot import *

def create_widgets(self, ROOT):
    '''
    Creates and initializes all widgets
    for the tkinter window.
    '''
    
    #Notebook
    self.notebook = ttk.Notebook(self, padding = [0, 0, 0, 0])
    self.notebook.grid(row = 0, column = 0, columnspan = 5)

    #Graph
    self.graph = tk.Frame(self.notebook, bd = 5, relief = tk.SUNKEN)
    self.graph.pack(side = "top")

    #Bottom Frame - All Buttons, Boxes, Etc.
    self.fra2 = tk.Frame(self.notebook)
    self.fra2.pack(side = "top")

    #Subframe For Listboxes, Pulldown Menus
    self.fra3 = tk.Frame(self.fra2, bd = 5, relief = tk.SUNKEN)
    self.fra3.pack(fill = "y", side = "left")

    #Subframe For Listboxes and Listbox Text
    self.fra4 = tk.Frame(self.fra2, bd = 5, relief = tk.SUNKEN)
    self.fra4.pack(fill = "y", side = "left")

    #Subframe For Only Listbox Text
    self.fra5 = tk.Frame(self.fra4)
    self.fra5.pack(side = "top")

    #Subframe For Only Listboxes
    self.fra6 = tk.Frame(self.fra4)
    self.fra6.pack(side = "top")

    #Subframe For Applying Trends
    self.fra7 = tk.Frame(self.fra2, bd = 5, relief = tk.SUNKEN)
    self.fra7.pack(fill = "y", side = "left")

    #Subframe for Selecting Y Variable to Fit
    self.fra8 = tk.Frame(self.fra7)
    self.fra8.pack(side = "top")

    #Subframe For First Index
    self.fra9 = tk.Frame(self.fra7)
    self.fra9.pack(side = "top")

    #Subframe For End Index
    self.fra10 = tk.Frame(self.fra7)
    self.fra10.pack(side = "top")

    #Subframe For Trendline Dropdown
    self.fra11 = tk.Frame(self.fra7)
    self.fra11.pack(side = "top")

    #Subframe For Delete/Apply Trendline
    self.fra12 = tk.Frame(self.fra7)
    self.fra12.pack(side = "top")

    #Subframe For Horizontal Scrollbars
    self.fra13 = tk.Frame(self.fra4)
    self.fra13.pack(fill = "x", side = "top")

    #Y-Fit Label
    self.y_fit_label = tk.Label(self.fra8, text = "Select Y-Variable to Fit:")
    self.y_fit_label.pack(side = "top")

    #Selecting Y Variable to Fit Dropdown
    self.yvarfit = tk.StringVar(ROOT)
    self.yvarfit.set("Choose a Y-Variable to Fit")
    self.yvarfit_box = tk.OptionMenu(self.fra8, self.yvarfit, [])
    self.yvarfit_box.pack(side = "top")

    #Trim Label
    self.Trim = tk.Label(self.fra9, text = "Trim Data:")
    self.Trim.pack(side = "top")

    #First Index Text
    self.list_label = tk.Label(self.fra9, text = "Select First Index:")
    self.list_label.pack(side = "left")

    #First Index Box
    self.text_box_first = tk.Entry(self.fra9)
    self.text_box_first.pack(side = "left")

    #End Index Text
    self.list_label = tk.Label(self.fra10, text = "Select End Index:")
    self.list_label.pack(side = "left")

    #End Index Box
    self.text_box_last = tk.Entry(self.fra10)
    self.text_box_last.pack(side = "left")

    #Fit Type Label
    self.fit_type_label = tk.Label(self.fra11, text = "Select Fit Type:")
    self.fit_type_label.pack(side = "top")

    #Trendline Dropdown
    self.trendlines = tk.StringVar(ROOT)
    self.trendlines.set("Choose a Fit Type")
    self.trendlines_sel = tk.OptionMenu(self.fra11, self.trendlines, *self.log_fits)
    self.trendlines_sel.pack(side = "top")

    #Delete Trendline
    self.delete_trendline = tk.Button(self.fra12, text = "Delete Trendline", \
                                      command = lambda: delete_fit(self, "yes", []))
    self.delete_trendline.pack(side = "left")

    #Apply Trendline
    self.apply_trendline = tk.Button(self.fra12, text = "Apply Trendline", \
                                     command = lambda: create_trendline(self))
    self.apply_trendline.pack(side = "left")

    #Log Files Label
    self.log_label = tk.Label(self.fra3, text = "Select Log File:")
    self.log_label.pack(side = "top")

    #Select Log Files
    self.logvarsel = tk.StringVar(ROOT)
    self.logvarsel.set("Choose a Log File")
    self.log_select = tk.OptionMenu(self.fra3, self.logvarsel, *self.list_logs, \
                                    command = lambda _: load_log_data(self, ROOT, "no"))
    self.log_select.pack(side = "top")

    #X-Variables Label
    self.x_label = tk.Label(self.fra3, text = "Select X-Variable:")
    self.x_label.pack(side = "top")

    #Select X-Variables
    self.xvarsel = tk.StringVar(ROOT)
    self.xvarsel.set("Choose an X-Variable")
    self.x_select = tk.OptionMenu(self.fra3, self.xvarsel, "", command = lambda _: update_graph(self))
    self.x_select.pack(side = "top")

    #Listbox Labels
    self.list_label1 = tk.Label(self.fra5, text = "Select Y-Variables:")
    self.list_label1.pack(side = "left")
    self.list_label2 = tk.Label(self.fra5, text = "              ")
    self.list_label2.pack(side = "left")
    self.list_label3 = tk.Label(self.fra5, text = "Y-Variables Plotted:")
    self.list_label3.pack(side = "left")

    #Listbox Y-Variable - Not Selected
    self.scrollbar_left_vert = tk.Scrollbar(self.fra6, orient = "vertical")
    self.scrollbar_left_hori = tk.Scrollbar(self.fra13, orient = "horizontal")
    self.listbox_not_sel = tk.Listbox(self.fra6, xscrollcommand = self.scrollbar_left_hori.set, \
                                      yscrollcommand = self.scrollbar_left_vert.set)
    self.scrollbar_left_vert.config(command = self.listbox_not_sel.yview)
    self.scrollbar_left_hori.config(command = self.listbox_not_sel.xview)
    self.listbox_not_sel.pack(side = "left")
    self.scrollbar_left_vert.pack(side = "left", fill = "y")
    self.scrollbar_left_hori.grid(row = 0, column = 0, sticky = tk.N + tk.S + tk.W + tk.E)
    self.listbox_not_sel.bind("<<ListboxSelect>>", lambda _: move_right(self, ROOT))

    #Listbox Y-Variable - Selected
    self.scrollbar_right_vert = tk.Scrollbar(self.fra6, orient = "vertical")
    self.scrollbar_right_hori = tk.Scrollbar(self.fra13, orient = "horizontal")
    self.listbox_sel = tk.Listbox(self.fra6, xscrollcommand = self.scrollbar_right_hori.set, \
                                  yscrollcommand = self.scrollbar_right_vert.set)
    self.scrollbar_right_vert.config(command = self.listbox_sel.yview)
    self.scrollbar_right_hori.config(command = self.listbox_sel.xview)
    self.listbox_sel.pack(side = "left")
    self.scrollbar_right_vert.pack(side = "left", fill = "y")
    self.scrollbar_right_hori.grid(row = 0, column = 1, sticky = tk.N + tk.S + tk.W + tk.E)
    self.listbox_sel.bind("<<ListboxSelect>>", lambda _: move_left(self, ROOT))

    #Horizontal Scrollbars Fill Frame Evenly
    for i in range(2):
        tk.Grid.columnconfigure(self.fra13, i, weight = 1)

    #Navigation Frame
    self.bottom_frame = tk.Frame(self, bd=5, relief=tk.SUNKEN)
    self.bottom_frame.grid(row=1, column=0, sticky="NW")
