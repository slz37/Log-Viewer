from libs import *
from log import *
from trendline import *

def move_right(self, ROOT):
    '''
    Move selected item to plot to the right listbox.
    '''
    
    #Prevent From Running With Empty Selection
    if not self.listbox_not_sel.curselection():
        return
    
    #Prevent Moving If No X-Value
    if self.xvarsel.get() == "Choose an X-Variable":
        print("Choose an x-variable before plotting.")
        return

    #Get Selected Item
    item = self.listbox_not_sel.get(self.listbox_not_sel.curselection())

    #Add to Graph
    populate_plot(self, item)

    #Delete From Left Side
    index = self.y_headers_left.index(item)
    del self.y_headers_left[index]
    self.listbox_not_sel.delete(index)

    #Rescale Axes
    self.ax.relim()
    self.ax.autoscale_view()
    draw()

    #Add to Right Side
    self.y_headers_right.append("{} - {}".format(item, self.logvarsel.get()))
    self.listbox_sel.insert(tk.END, "{} - {}".format(item, self.logvarsel.get()))

    #Destroy Old OptionMenus
    self.yvarfit_box.destroy()

    #Update Fit Dropdown
    self.yvarfit = tk.StringVar(ROOT)
    self.yvarfit.set("Choose a Y-Variable to Fit")
    self.yvarfit_box = tk.OptionMenu(self.fra8, self.yvarfit, *self.y_headers_right)
    self.yvarfit_box.pack(side = "top")

def move_left(self, ROOT):
    '''
    Move selected item to remove from plot to the left listbox.
    '''
    
    #Prevent From Running With Empty Selection
    if not self.listbox_sel.curselection():
        return
    
    #Get Selected Item
    item = self.listbox_sel.get(self.listbox_sel.curselection())

    #Find Index in Tracker Array
    for row in self.datalines:
        try:
            column_index = row.index(item)
            rowindex = self.datalines.index(row)
        except:
            pass

    #Remove Fit Line if Exists
    try:
        delete_fit(self, "no", item)
    except Exception as e:
        pass

    #Delete From Right Side
    index = self.y_headers_right.index(item)
    del self.y_headers_right[index]
    self.listbox_sel.delete(index)

    #Add to Left Side
    if self.logvarsel.get() == self.datalines[rowindex][2]:
        load_log_data(self, ROOT, "yes")

    #Remove From Graph
    delete_data(self, item)

    #Destroy Old OptionMenus
    self.yvarfit_box.destroy()

    #Update Fit Dropdown - Glitches if y_headers_right is empty and use asterisk to fill
    if self.y_headers_right:
        self.yvarfit = tk.StringVar(ROOT)
        self.yvarfit.set("Choose a Y-Variable to Fit")
        self.yvarfit_box = tk.OptionMenu(self.fra8, self.yvarfit, *self.y_headers_right)
        self.yvarfit_box.pack(side = "top")
    else:
        self.yvarfit = tk.StringVar(ROOT)
        self.yvarfit.set("Choose a Y-Variable to Fit")
        self.yvarfit_box = tk.OptionMenu(self.fra8, self.yvarfit, [])
        self.yvarfit_box.pack(side = "top")
