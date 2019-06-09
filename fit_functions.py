from libs import *

'''
Non standard functions available to fit to data.
Also available are linear and quadratic.
'''

def gaussian(x, a, x0, sigma):
    return a * np.exp(-(x - x0)**2 / (2 * sigma**2))

def ln(x, a, b):
    return a * np.log(x) + b

def ex(x, a, b):
    return a * np.exp(b * x)

#Generate random data for example
if __name__ == "__main__":
    headers = ["Time", "linear", "quadratic", "gaussian", "ln", "ex"]
    time = np.linspace(1, 100, 1000)
    file = open('20190609_0.txt', 'w+')

    #Header stuff
    file.write("Title - skipped when loaded\n")
    for i in headers:
        file.write(i + "  ")
    file.write("\n%.3f %.3f %.3f %.3f %.3f %.3f\n")
    for i in range(3):
        file.write(" \n")

    #Write data
    for t in time:
        lin = "%.3f" % (5 * t - 10 + 10 * np.random.normal())
        quad = "%.3f" % (6 * (t / 8)**2 - 5 * t - 10 + 10 * np.random.normal())
        gaus = "%.3f" % (gaussian(t, 300, 50, 10) + 10 * np.random.normal())
        nat = "%.3f" % (ln(t, 100, 5) + 10 * np.random.normal())
        test = np.random.normal()
        expon = "%.3f" % (ex(t, 3, 5E-2) + 10 * test)

        file.write("%.3f" % t + " " + lin + " " + quad + " " + \
                   gaus + " " + nat + " " + expon + "\n")

    file.close()
    
