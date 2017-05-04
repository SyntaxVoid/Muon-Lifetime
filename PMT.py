from copy import deepcopy
import matplotlib as mpl
import matplotlib.pyplot as plt


def midp(x):
    # Returns the midpoint between the maximum value of x and the minimum value of x
    return 0.5 * (max(x) + min(x))

class PMT:
    def __init__(self, hv, cts):
        self.hv = deepcopy(hv)
        self.cts = deepcopy(cts)
        assert len(self.hv) == len(self.cts), \
            "# of elements in hv is not equal to # of elements in cts!\n\thv:{}\n\tcts:{}".format(self.hv,self.cts)
        return

    def find_plateau(self):
        # Returns the index of the plateau voltage
        start = True
        mindfdx = 999999
        minind = 0
        for n in range(5, len(self.hv)-1):
            if start:
                start = False
                continue
            df = self.cts[n+1] - self.cts[n-1]
            dx = self.hv[n+1] - self.hv[n-1]
            dfdx = abs(df/dx)
            if dfdx < mindfdx:
                mindfdx = dfdx
                minind = n
        return minind

    def plot_plateau(self, title):
        plateau = self.find_plateau()
        plat_hv = self.hv[plateau]
        plat_cts = self.cts[plateau]
        mpl.rcParams.update({"font.size": 34})
        plt.plot(self.hv, self.cts,"bo", markersize=6)
        plt.plot([self.hv[0],self.hv[-1]], [plat_cts, plat_cts], linewidth = 5)
        plt.plot([plat_hv, plat_hv],[self.cts[0], self.cts[-1]], linewidth = 5)
        plt.grid()
        plt.legend(["Counts vs. Voltage","Plateau","Plateau Voltage"])
        plt.text(0.05 + plat_hv, midp(self.cts), "Plateau Voltage = {} kV\nPlateau Counts = {}"\
                 .format(plat_hv, plat_cts), size=50)
        plt.xlabel("PMT Voltage (kV)")
        plt.ylabel("Counts per 60 seconds")
        plt.title(title)
        plt.show()
        return

