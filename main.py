
import numpy as np
import operator

from PMT import *

def ty_to_mathematica(x,y,out):
    with open(out,"w") as o:
        for a,b in zip(x,y):
            o.write("{} {}\n".format(a,b))
    return
    # with open(out,"w") as o:
    #     o.write("{")
    #     start = 1
    #     for a,b in zip(x,y):
    #         if start:
    #             o.write("{{{},{}}}".format(a,b))
    #             start = 0
    #         else:
    #             o.write(",{{{},{}}}".format(a, b))
    #     o.write("}")
    # return


def find_max(arr):
    ## Returns a tuple containing the index of the maximum, and the maximum itself. (index, val)
    ## Will only return index of the FIRST maximum.
    return max(enumerate(arr), key=operator.itemgetter(1))


def keV_to_mus(n, factor = 1/420):
    ## Converts the number, n, from keV to microseconds.
    ## Maestro provides a histogram with the x-axis in keV, but we would
    ## prefer a histogram of microseconds. We found that a 2 microsecond
    ## delay corresponds to 840 keV. Then 1 keV = 1/420 microseconds.
    return n*factor


def which_bin(bins, val):
    ## Returns the index of the val that bins is in. If -1 is returned, val is not within any bin.
    ## Bin numbering starts at ZERO.

    ## Take care of edge case immediately.
    if val == bins[-1]:
        return len(bins)-2
    for b in range(len(bins)-1):
        if val >= bins[b] and val < bins[b+1]:
            return b
    return -1


def bin_rough(t, y, n_bins=100):
    ## We would like to have the bins: { [t0,t0+i), [t0+i,t0+2i), ... [t0+(n-1)i, t0+n*i] }
    bins = np.array(np.linspace(start = t[0], stop = t[-1], num = n_bins))
    vals = np.array(np.zeros(len(bins)-1), dtype=int)
    for n, (tt, yy) in enumerate(zip(t,y)):
        ## What bin are we currently in? Take our current t value and find which bin we are in.
        b = which_bin(bins, tt)
        ## Add value to our bin
        vals[b] += yy
    return bins, vals

def midpoint(a,b):
    return 0.5 * (a+b)


def bins_to_midp(bins):
    out = np.array(np.zeros(len(bins)-1), dtype=np.float64)
    for b in range(len(bins)-1):
        out[b] = midpoint(bins[b+1],bins[b])
    return out

def plot_histogram(t,y,title="Histogram Title"):
    #plt.plot(t,y,"b*")
    #plt.hist(y, bins=[0,1,2,3,4,5,6,7,8,9,10])

    plt.bar(b,v, width=0.6)
    plt.xlabel(r"Decay Time ($\mu$s)")
    plt.ylabel("Counts")
    plt.title(title)
    plt.xlim([1.1, 5])
    plt.ylim([0,2000])
    #plt.ylim([min(y),max(y)*1.05])
    return plt.gca()

def read_SPE(f):
    ## Reads in data from a Maestro .spe text file and returns arrays of
    ## the t and y values from the histogram. Converts t values from keV
    ## to microseconds with the keV_to_mus function.
    data = False
    start = True
    index = 0
    t = [ ]
    y = [ ]
    with open(f,"r") as histo:
        data_lines = histo.readlines()
        for line_num, data_line in enumerate(data_lines):
            if data_line.startswith("$DATA:"):
                data = True
                continue # This everything below it and moves to the next iteration of the for loop
            if data and start:
                ## The line after $DATA: will contain the minimum t value and maximum t value
                tmin = int(data_line.split()[0]) # This is our starting value
                tmax = int(data_line.split()[1]) # This is our ending value
                ## All save files should be incremented by 1 keV
                n_pts = tmax-tmin
                t = np.array(np.linspace(start=keV_to_mus(tmin), stop=keV_to_mus(tmax), num=n_pts+1), dtype=np.float64)
                y = np.array(np.zeros(n_pts+1), dtype=int)
                ## t is now an array from tmin to tmax in units of microseconds.
                start = False
                continue
            if data and not start:
                # We are reading the real data now.
                if data_line.startswith("$"):
                    break ## End of data
                y[index] = int(data_line.strip())
                index += 1
    return t,y

def fit_exponential2(t, y, ax):
    ind,ymax = find_max(y)
    tmax = t[ind]
    ymax = 1000
    def lifetime(tau):
        return lambda t: ymax * np.exp( (tmax-t) / tau )

    lifetime1 = lifetime(0.022)
    lifetime2 = lifetime(0.10)
    lifetime3 = lifetime(2.20)

    #ax.plot(x,lifetime1(x), "r-", linewidth=15)
    ax.plot(x,lifetime3(x), "g-", linewidth=10)
    return



def fit_exponential(x,y):
    #fit = np.polyfit(-x, np.log(y), 1)
    #def f(t):
    #    return fit[0]*np.log(t)+fit[1]
    #fity = []
    #for tmp in x:
    #    fity.append(f(tmp))
    def theory(t,tau):
        return y[0] * np.exp((-(t-48/420))/tau)
    xth = np.array(np.linspace(0,1,100))
    yth = theory(xth,0.02)
    print(y[0],max(y))
    y1 = []
    y2 = []
    y3 = []
    for i in x:
        y1.append(theory(i,2.2))
        y2.append(theory(i,1.0))
        y3.append(theory(i,3.5))
    plt.plot(x,y,"b*",xth,yth,"b-")
    plt.xlim([0,1])
    plt.ylim([0,6000])
    #plt.plot(x,y1,"r-")
    #plt.plot(x,y2,"g-")
    #plt.plot(x,y3,"k-")
    print(y1)
    print(x[0])
    plt.legend(["Data","1"])#,"2","3"])
    #plt.plot(x,fity,"r-")
    plt.show()
    #plt.plot(x,fit)
    #fitx,fity = optimize.curve_fit(lambda t,a,b: a*np.exp(b*t),x,y)
    #plt.plot(fitx,fity)
    #plt.grd
    return





if __name__ == '__main__':
    ###### CONTROLS ######
    ## Set values to either true or false to specify which
    ## parts of the analysis you would like to run.

    PLOT_PLATEAUS  = False
    PLOT_HISTOGRAM = True

    ######################### PMT CALIBRATION ####################
    ## All counts (cts) are per 60 seconds.
    ###### PMT 1 ######
    # Discriminator 1 voltage is 1.508 V
    hv1 =  [1.168, 1.173, 1.183, 1.188, 1.197, 1.225, 1.235, 1.242, 1.251, 1.260, 1.272, 1.292,
          1.311, 1.322, 1.334, 1.344, 1.357, 1.364, 1.377, 1.385, 1.401, 1.421, 1.442, 1.465]
    cts1 = [12, 13, 14, 19, 19, 22, 27, 41, 53, 46, 41, 93, 115,
           137, 155, 173, 220, 233, 281, 325, 380, 534, 733, 915]
    PMT1 = PMT(hv1,cts1)
    ###### ######

    ###### PMT 2 ######
    ## Discriminator 2 voltage is 1.505 V
    hv2 = [1.163, 1.172, 1.181, 1.191, 1.200, 1.217, 1.248,
          1.277, 1.312, 1.343, 1.351, 1.361, 1.371, 1.380]
    cts2 = [751, 834, 935, 1109, 1263, 1679, 2595, 3540, 4812, 7157, 10612, 14285, 32415, 92540]
    PMT2 = PMT(hv2,cts2)
    ###### ######

    ###### PMT 3 ######
    ## Discriminator 3 voltage is 1.509 V
    hv3 = [1.152, 1.164, 1.172, 1.182, 1.193, 1.207, 1.213, 1.223, 1.233, 1.243, 1.254, 1.267, 1.273, 1.282,
           1.295, 1.303, 1.314, 1.323, 1.333, 1.343, 1.352, 1.364, 1.374, 1.383, 1.394, 1.406, 1.416, 1.424,
           1.433, 1.443, 1.453, 1.463, 1.474, 1.488, 1.500, 1.512, 1.523, 1.533, 1.543, 1.554, 1.566, 1.578,
           1.589, 1.600]
    cts3 = [306, 360, 375, 521, 565, 652, 697, 861, 918, 1112, 1203, 1316, 1491, 1591, 1758, 1824, 2081, 2240,
            2438, 2645, 2817, 3036, 3354, 3505, 3725, 4045, 4359, 4565, 4735, 4954, 5226, 5489, 5714, 6174,
            6677, 7137, 7539, 8137, 8825, 9948, 11488, 13889, 15846, 21504]
    PMT3 = PMT(hv3,cts3)
    ###### ######

    ###### PMT1 - Attempt 2 ######
    ## Second attempt at discriminator 1. v_dis = 1.508 V
    hv1_2 = [1.178, 1.188, 1.200, 1.212, 1.221, 1.237, 1.247, 1.257, 1.267, 1.277, 1.287,
           1.300, 1.312, 1.322, 1.351, 1.400, 1.451, 1.500, 1.550, 1.665, 1.700]
    cts1_2 = [3,2,3,3,8,11, 3,9,8,11,13,12,14,21,37,54,124,181,328,572,869]
    PMT1_2 = PMT(hv1_2,cts1_2)
    ###### ######
    ##############################################################


    ##################### HISTOGRAMS #############################
    ## Gathered data for 595201 seconds or 6.889 days.
    hist_file = "muon_data.spe"
    ## First we read the data in.
    x,y = read_SPE(hist_file)

    ##############################################################
    if PLOT_PLATEAUS:
        PMT1.plot_plateau(  title=r"$PMT 1 -- v_{dis} = 1.508 V")
        PMT2.plot_plateau(  title=r"$PMT 2 -- v_{dis} = 1.505 V")
        PMT3.plot_plateau(  title=r"$PMT 3 -- v_{dis} = 1.509 V")
        PMT1_2.plot_plateau(title=r"$PMT 1 -- v_{dis} = 1.508 V")


    if PLOT_HISTOGRAM:
        t, y = read_SPE("muon_data.spe")

        b, v = bin_rough(t, y, n_bins=10)
        b = bins_to_midp(b)
        # Want to skip the first two bins.. Maybe theres an argument for this later...
        b,v = b[2:],v[2:]
        ty_to_mathematica(b, v, "Mathematica_format.txt")

        # ax = plot_histogram(t, y, title = "Muon decay time histogram")
        # fit_exponential2(t, y, ax)
        # plt.legend(["Data Points", "Theoretical"])
        # plt.show()

