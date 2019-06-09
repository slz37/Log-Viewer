from libs import *
from fit_functions import *

def create_trendline(self):
    '''
    Add a selected trendline to the desired
    dataset.
    '''
    
    #Select Y-Variable Before Fitting
    if self.yvarfit.get() == "Choose a Y-Variable to Fit":
        print("Select a y-variable to fit first.")
        return
    elif self.yvarfit.get() == "":
        print("Cannot fit to empty dataset.")
        return

    #Selected X Variable
    xvar = self.xvarsel.get()

    #Selected Y Variable
    yvarunsplit = self.yvarfit.get()
    yvar = yvarunsplit.split(" ", 1)[0]
    yvarrun = yvarunsplit.split(" ", 2)[2]

    #Currently Selected Log
    chosen_log = self.logvarsel.get()

    #Find Index in Tracker Array
    for row in self.fitlines:
        try:
            column_index = row.index(yvarunsplit)
            row_index = self.fitlines.index(row)
        except:
            pass

    #Load Data From Log File If Necessary
    if chosen_log != yvarrun:
            temp_x_headers, temp_data = self.temp_log_data(yvarrun)

            #Get Indices
            if self.text_box_first.get() == "" or self.text_box_first.get() == "0":
                first_index = 0
            else:
                try:
                    first_index = int(self.text_box_first.get())
                except:
                    print("First index is invalid (not an integer or blank).\n")
                    return
            if self.text_box_last.get() == "" or self.text_box_last.get() == "0":
                last_index = len(temp_data.iloc[:, 0])
            else:
                try:
                    last_index = int(self.text_box_last.get()) + 1
                except:
                    print("Last index is invalid (not an integer or blank).\n")
                    return

            #If Fitting Variable Already Fit, Delete Plot
            if yvarunsplit in [row[0] for row in self.fitlines]:
                delete_fit(self, "no", [])

                #Rescale Axes
                self.ax.relim()
                self.ax.autoscale_view()
                draw()

            #Get X Data
            xindex = temp_x_headers.index(xvar)
            xdata = temp_data.iloc[:, xindex].values

            #Trim X Data
            xdata = xdata[first_index:last_index]

            #Get Location of Header in Original File
            yindex = temp_x_headers.index(yvar)

            #Store Column Data
            ydata = temp_data.iloc[:, yindex].values

            #Trim Y Data
            ydata = ydata[first_index:last_index]
    else:
        #Get Indices
        if self.text_box_first.get() == "" or self.text_box_first.get() == "0":
            first_index = 0
        else:
            try:
                first_index = int(self.text_box_first.get())
            except:
                print("First index is invalid (not an integer or blank).\n")
                return
        if self.text_box_last.get() == "" or self.text_box_last.get() == "0":
            last_index = len(self.data.iloc[:, 0])
        else:
            try:
                last_index = int(self.text_box_last.get()) + 1
            except:
                print("Last index is invalid (not an integer or blank).\n")
                return

        #If Fitting Variable Already Fit, Delete Plot
        if yvarunsplit in [row[0] for row in self.fitlines]:
            delete_fit(self, "no", [])

        #Get X Data
        xindex = self.x_headers.index(xvar)
        xdata = self.data.iloc[:, xindex].values

        #Trim X Data
        xdata = xdata[first_index:last_index]

        #Get Location of Header in Original File
        yindex = self.x_headers.index(yvar)

        #Store Column Data
        ydata = self.data.iloc[:, yindex].values

        #Trim Y Data6
        ydata = ydata[first_index:last_index]

    #Get Type of Fit
    fit_type = self.trendlines.get()

    #Fit Line
    if fit_type == "Linear":
        #Get Fit Coefficients
        fit = np.polyfit(xdata, ydata, deg = 1)

        #Plot
        self.ax.plot(xdata, fit[0] * xdata + fit[1], label = "Linear Fit {0:s}\n {1:.4g}x + {2:.4g}".format(yvarunsplit, fit[0], fit[1]))
    elif fit_type == "Quadratic":
        #Get Fit Coefficients
        fit = np.polyfit(xdata, ydata, deg = 2)

        #Plot
        self.ax.plot(xdata, fit[0] * xdata**2 + fit[1] * xdata + fit[2], label = "Quadratic Fit {0:s}\n {1:.4g}x$^2$ + {2:.4g}x + {3:.4g}".format(yvarunsplit, fit[0], fit[1], fit[2]))
    elif fit_type == "Gaussian":
        #Calculate Statistical Variables Needed
        mean = sum(xdata * ydata) / sum(ydata)
        sigma = np.sqrt(sum(ydata * (xdata - mean)**2) / sum(ydata))

        #Get Fit Coefficients
        popt, pcov = curve_fit(gaussian, xdata, ydata, p0 = [max(ydata), mean, sigma])

        #Plot
        self.ax.plot(xdata, gaussian(xdata, *popt), label = "Gaussian Fit {}".format(yvarunsplit))
    elif fit_type == "Exponential":
        #Get Fit Coefficients - low guess for b
        popt, pcov = curve_fit(ex, xdata, ydata, p0 = (1, 1E-5))

        #Plot
        self.ax.plot(xdata, ex(xdata, *popt), label = "Exponential Fit {0:s}\n ({1:.4g})e$^{{({2:.4g})x}}$".format(yvarunsplit, popt[0], popt[1]))
    elif fit_type == "Logarithmic":
        #Store X-Data to be Modified For Calculations
        xdata_calc = xdata

        #Initial Shift
        c = 0

        #Shift Data if Negative
        try:
            #Shift By Most Negative Number
            c = abs(min([n for n in xdata if n < 0]))
            xdata_calc = [n + c for n in xdata]
        except:
            pass

        #Convert Back to Numpy Array
        xdata_calc = np.asarray(xdata_calc, dtype = float)

        #Set Indices With Zero Values to Small Numbers
        xdata_calc[xdata_calc == 0] = 1E-10

        #Get Fit Coefficients
        popt, pcov = curve_fit(ln, xdata_calc, ydata)

        #Plot
        self.ax.plot(xdata, ln(xdata_calc, *popt), label = "Logarithmic Fit {0:s}\n ({1:.4g})ln(x + {2:.4g}) + {3:.4g}".format(yvarunsplit, popt[0], c, popt[1]))
    else:
        print("Select a fit type.\n")
        return

    #Keep Track of Which Fit Lines Goes With Which Variable
    self.fitlines.append(["{} - {}".format(yvar, yvarrun), len(self.ax.lines) - 1, self.ax.lines[len(self.ax.lines) - 1], first_index, last_index, fit_type, yvarrun])

    #Destroy Navigation If Exists
    try:
        self.nav.destroy()
    except:
        pass

    #Legend
    self.leg = self.ax.legend(loc = "upper left", bbox_to_anchor = (1, 1))

    #Lock to Tight View
    self.fig.set_tight_layout(True)

    #Update Canvas
    self.canvas = FigureCanvasTkAgg(self.fig, self.graph)
    self.canvas.draw()
    self.canvas.get_tk_widget().grid(row = 0, column = 1)

    #Unlock Layout
    self.fig.set_tight_layout(False)

    #Width of Legend
    leg_width = self.leg.get_frame().get_width()

    #Location of Legend as Fraction of Total Width
    buffer = 0.01
    leg_loc = ((self.fig_width - leg_width) / self.fig_width) - buffer

    #Adjust Right Side to Fit Legend
    self.fig.subplots_adjust(right = leg_loc)

    #Plot Toolbar
    self.nav = NavigationToolbar2Tk(self.canvas, self.bottom_frame)
    self.nav.pack(side = "top")

def delete_fit(self, button, item):
    '''
    Remove the trendline from a desired
    dataset.
    '''
    
    #Select Y-Variable Before Deleting
    if self.yvarfit.get() == "Choose a Y-Variable to Fit" and button == "yes":
        print("Select a y-variable to delete first.")
        return

    #Get Fit Variable
    if not item:
        yvar = self.yvarfit.get()
    else:
        yvar = item

    #Plot Fitline Before Deleting
    if yvar not in [row[0] for row in self.fitlines] and button == "yes":
        print("Fitline is not currently plotted.")
        return

    #Get Index Where Variable Fit is Stored
    rowind = [row[0] for row in self.fitlines].index(yvar)

    #Get Index of Line in ax.lines
    fitindex = self.fitlines[rowind][1]

    #No Longer Plotted, Remove From Tracker
    del self.fitlines[rowind]

    #Delete Line
    del self.ax.lines[fitindex]

    #Shift Stored Indices Down 1
    for row in self.datalines:
        if row[1] > fitindex:
            row[1] -= 1
    for row in self.fitlines:
        if row[1] > fitindex:
            row[1] -= 1

    #Update Canvas If Button Was Clicked
    if button == "yes":
        #Rescale Axes
        self.ax.relim()
        self.ax.autoscale_view()
        draw()

        #Destroy Navigation If Exists
        try:
            self.nav.destroy()
        except:
            pass

        #Legend
        if len(self.datalines) == 0:
            self.ax.legend_.remove()
        else:
            self.leg = self.ax.legend(loc = "upper left", bbox_to_anchor = (1, 1))

        #Lock to Tight View
        self.fig.set_tight_layout(True)

        #Update Canvas
        self.canvas = FigureCanvasTkAgg(self.fig, self.graph)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row = 0, column = 1)

        #Unlock Margins
        self.fig.set_tight_layout(False)

        #Width of Legend
        leg_width = self.leg.get_frame().get_width()

        #Location of Legend as Fraction of Total Width
        buffer = 0.01
        leg_loc = ((self.fig_width - leg_width) / self.fig_width) - buffer

        #Adjust to Fit Legend
        self.fig.subplots_adjust(right = leg_loc)

        #Plot Toolbar
        self.nav = NavigationToolbar2Tk(self.canvas, self.bottom_frame)
        self.nav.pack(side = "top")
