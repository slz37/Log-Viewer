from libs import *

def update_graph(self):
    '''
    Update the plot to reflect data and trendlines
    while scaling to appropriate view.
    '''
    
    #Destroy Navigation If Exists
    try:
        self.nav.destroy()
    except:
        pass

    #Update Lines If Plotted, Else Create Blank Plot
    try:
        #Current Selected Log
        chosen_log = self.logvarsel.get()

        #Update Lines to New X-Data
        for lines in self.ax.lines:
            #Update Fitlines
            if lines in (row[2] for row in self.fitlines):
                #Find Index in Tracker Array
                for row in self.fitlines:
                    try:
                        column_index = row.index(lines)
                        row_index = self.fitlines.index(row)
                    except:
                        pass

                #Load Data From Log File If Necessary
                if chosen_log != self.fitlines[row_index][6]:
                    temp_x_headers, temp_data = self.temp_log_data(self.fitlines[row_index][6])

                    #New Selected X-Variable
                    xvar = self.xvarsel.get()

                    #Relabel X-Axis
                    self.ax.set_xlabel(xvar)

                    #New Data
                    xindex = temp_x_headers.index(xvar)
                    xdata = temp_data.iloc[:, xindex].values

                    #Get Y-Variable
                    yvarunsplit = self.fitlines[row_index][0]
                    yvar = yvarunsplit.split(" ", 1)[0]

                    #Get Location of Header in Original File
                    yindex = temp_x_headers.index(yvar)

                    #Store Column Data
                    ydata = temp_data.iloc[:, yindex]
                else:
                    #New Selected X-Variable
                    xvar = self.xvarsel.get()

                    #Relabel X-Axis
                    self.ax.set_xlabel(xvar)

                    #New Data
                    xindex = self.x_headers.index(xvar)
                    xdata = self.data.iloc[:, xindex].values

                    #Get Y-Variable
                    yvarunsplit = self.fitlines[row_index][0]
                    yvar = yvarunsplit.split(" ", 1)[0]

                    #Get Location of Header in Original File
                    yindex = self.x_headers.index(yvar)

                    #Store Column Data
                    ydata = self.data.iloc[:, yindex]

                #Get Indices
                first_index = self.fitlines[row_index][3]
                last_index = self.fitlines[row_index][4]

                #Trim X-Data
                fitxdata = xdata[first_index:last_index]

                #Trim Y Data
                ydata = ydata[first_index:last_index]

                #Get Type of Fit
                fit_type = self.fitlines[row_index][5]

                #Update Fit Line
                if fit_type == "Linear":
                    #Get Fit Coefficients
                    fit = np.polyfit(fitxdata, ydata, deg = 1)

                    #Calculate New Y-Data
                    newydata = fit[0] * fitxdata + fit[1]

                    #Set New Arrays to Plot
                    lines.set_xdata(fitxdata)
                    lines.set_ydata(newydata)

                    #Update Legend
                    lines.set_label("Linear Fit {0:s}\n {1:.4g}x + {2:.4g}".format(yvarunsplit, fit[0], fit[1]))
                elif fit_type == "Quadratic":
                    #Get Fit Coefficients
                    fit = np.polyfit(fitxdata, ydata, deg = 2)

                    #Calculate New Y-Data
                    newydata = fit[0] * fitxdata**2 + fit[1] * xdata + fit[2]

                    #Set New Arrays to Plot
                    lines.set_xdata(fitxdata)
                    lines.set_ydata(newydata)

                    #Update Legend
                    lines.set_label("Quadratic Fit {0:s}\n {1:.4g}x$^2$ + {2:.4g}x + {3:.4g}".format(yvarunsplit, fit[0], fit[1], fit[2]))
                elif fit_type == "Gaussian":
                    #Calculate Statistical Variables Needed
                    mean = sum(fitxdata * ydata) / sum(ydata)
                    sigma = np.sqrt(sum(ydata * (fitxdata - mean)**2) / sum(ydata))

                    #Get Fit Coefficients
                    popt, pcov = curve_fit(gaussian, fitxdata, ydata, p0 = [max(ydata), mean, sigma])

                    #Set New Arrays to Plot
                    lines.set_xdata(fitxdata)
                    lines.set_ydata(gaussian(fitxdata, *popt))

                    #Update Legend
                    lines.set_label("Gaussian Fit {}".format(yvarunsplit))
                elif fit_type == "Exponential":
                    #Get Fit Coefficients
                    popt, pcov = curve_fit(ex, xdata, ydata)

                    #Calculate New Y-Data
                    newydata = ex(fitxdata, *popt)

                    #Set New Arrays to Plot
                    lines.set_xdata(fitxdata)
                    lines.set_ydata(newydata)

                    #Update Legend
                    lines.set_label("Exponential Fit {0:s}\n ({1:.4g})e$^{{({2:.4g})x}}$".format(yvarunsplit, popt[0], popt[1]))
                elif fit_type == "Logarithmic":
                    #Store X-Data to be Modified For Calculations
                    xdata_calc = fitxdata

                    #Initial Shift
                    c = 0

                    #Shift Data if Negative
                    try:
                        #Shift By Most Negative Number
                        c = abs(min([n for n in fitxdata if n < 0]))
                        xdata_calc = [n + c for n in fitxdata]
                    except:
                        pass

                    #Convert Back to Numpy Array
                    xdata_calc = np.asarray(xdata_calc, dtype = float)

                    #Set Indices With Zero Values to Small Numbers
                    xdata_calc[xdata_calc == 0] = 1E-10

                    #Get Fit Coefficients
                    popt, pcov = curve_fit(ln, xdata_calc, ydata)

                    #Calculate New Y-Data
                    newydata = ln(xdata_calc, *popt)

                    #Set New Arrays to Plot
                    lines.set_xdata(fitxdata)
                    lines.set_ydata(newydata)

                    #Update Legend
                    lines.set_label("Logarithmic Fit {0:s}\n ({1:.4g})ln(x + {2:.4g}) + {3:.4g}".format(yvarunsplit, popt[0], c, popt[1]))
                else:
                    print("Unknown fit type: {}\n".format(fit_type))
            #Update Datalines
            else:
                #Find Index in Tracker Array
                for row in self.datalines:
                    try:
                        column_index = row.index(lines)
                        row_index = self.datalines.index(row)
                    except:
                        pass

                #Load Data From Log File If Necessary
                if chosen_log != self.datalines[row_index][2]:
                    temp_x_headers, temp_data = self.temp_log_data(self.datalines[row_index][2])

                    #New Selected X-Variable
                    xvar = self.xvarsel.get()

                    #Relabel X-Axis
                    self.ax.set_xlabel(xvar)

                    #New Data
                    xindex = temp_x_headers.index(xvar)
                    xdata = temp_data.iloc[:, xindex].values

                    lines.set_xdata(xdata)
                else:
                    #New Selected X-Variable
                    xvar = self.xvarsel.get()

                    #Relabel X-Axis
                    self.ax.set_xlabel(xvar)

                    #New Data
                    xindex = self.x_headers.index(xvar)
                    xdata = self.data.iloc[:, xindex].values

                    lines.set_xdata(xdata)

        #Rescale Axes
        self.ax.relim()
        self.ax.autoscale_view()
        draw()

        #Legend
        if len(self.datalines) == 0:
            self.ax.legend_.remove()
        else:
            self.leg = self.ax.legend(loc = "upper left", bbox_to_anchor = (1, 1))

        #Update Canvas
        self.canvas = FigureCanvasTkAgg(self.fig, self.graph)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row = 0, column = 1)

        #Plot Toolbar
        self.nav = NavigationToolbar2Tk(self.canvas, self.bottom_frame)
        self.nav.pack(side = "top")
    except Exception as e:
        if len(self.y_headers_right) > 0:
            #Reset Variables
            self.fitlines = []
            self.datalines = []
            self.y_headers_right = []
            load_log_data(self, ROOT, "yes")

            #Print Error
            print(e,  "Line: ", sys.exc_info()[2].tb_lineno)

        #Reset Plot
        plt.close("all")
        self.fig = Figure(figsize = (13, 5), dpi = 100)
        self.fig_width = self.fig.get_size_inches()[0] * self.fig.dpi
        self.ax = self.fig.add_subplot(111)

        #Adjust Margins
        self.fig.subplots_adjust(left = 0.03, right = 0.98, top = 0.96, bottom = 0.1)

        #Update Canvas
        self.canvas = FigureCanvasTkAgg(self.fig, self.graph)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row = 0, column = 1)

        #Plot Toolbar
        self.nav = NavigationToolbar2Tk(self.canvas, self.bottom_frame)
        self.nav.pack(side = "top")

def populate_plot(self, y_header):
    '''
    Add selected data to plot.
    '''
    
    #Destroy Navigation If Exists
    try:
        self.nav.destroy()
    except:
        pass

    #Selected Variables
    xvar = self.xvarsel.get()
    
    #Label X-Axis
    self.ax.set_xlabel(xvar)

    #Collect Data Only if X Variable and Y Variable Are Chosen
    if xvar in self.x_headers and y_header:
        #Get X Data
        xindex = self.x_headers.index(xvar)
        xdata = self.data.iloc[:, xindex].values

        #Get Location of Header in Original File
        yindex = self.x_headers.index(y_header)

        #Store Column Data
        ydata = self.data.iloc[:, yindex]

        #Plot
        self.ax.plot(xdata, ydata, label = "{} - {}".format(y_header, self.logvarsel.get()))

        #Keep Track of Which Data Lines Goes With Which Variable
        self.datalines.append(["{} - {}".format(y_header, self.logvarsel.get()), len(self.ax.lines) - 1, self.logvarsel.get(), self.ax.lines[len(self.ax.lines) - 1]])

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

def delete_data(self, item):
    '''
    Remove data from plot if the user deselects the
    corresponding value in the right listbox.
    '''
    
    #Get Fit Variable
    yvar = item

    #Get Index Where Variable Fit is Stored
    rowind = [row[0] for row in self.datalines].index(yvar)

    #Get Index of Line in ax.lines
    fitindex = self.datalines[rowind][1]

    #No Longer Plotted, Remove From Tracker
    del self.datalines[rowind]

    #Delete Line
    del self.ax.lines[fitindex]

    #Shift Stored Indices Down 1
    for row in self.datalines:
        if row[1] > fitindex:
            row[1] -= 1
    for row in self.fitlines:
        if row[1] > fitindex:
            row[1] -= 1

    #Destroy Navigation If Exists
    try:
        self.nav.destroy()
    except:
        pass

    #Legend
    if len(self.datalines) == 0:
        self.ax.legend_.remove()

        #Lock to Tight View
        self.fig.set_tight_layout(True)

        #Update Canvas
        self.canvas = FigureCanvasTkAgg(self.fig, self.graph)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row = 0, column = 1)

        #Unlock Margins
        self.fig.set_tight_layout(False)

        #Plot Toolbar
        self.nav = NavigationToolbar2Tk(self.canvas, self.bottom_frame)
        self.nav.pack(side = "top")
    else:
        self.leg = self.ax.legend(loc = "upper left", bbox_to_anchor = (1, 1))

        #Rescale Axes
        self.ax.relim()
        self.ax.autoscale_view()
        draw()

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
