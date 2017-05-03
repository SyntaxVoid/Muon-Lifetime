import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from copy import deepcopy

def read_SPE(f, data_start=12, data_end=None, stepping=2):
    histx = []
    histy = []
    with open(f,"r") as histo:
        for line_num,data in enumerate(histo.readlines()):
           if line_num < 12:
               # Skip the header information

               continue

    return




def midp(x):
    return 0.5 * (max(x) + min(x))

class PMT:
    def __init__(self, hv, cts):
        self.hv = deepcopy(hv)
        self.cts = deepcopy(cts)
        assert len(self.hv) == len(self.cts), \
            "# of elements in hv is not equal to # of elements in cts!\n\thv:{}\n\tcts:{}".format(self.hv,self.cts)
        return

    def find_plateau(self):
        # Returns the voltage of a plateau
        start = 1
        mindfdx = 999999
        minind = 0
        for n in range(5, len(self.hv)-1):
            if start:
                start = 0
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
        matplotlib.rcParams.update({"font.size": 34})
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


if __name__ == '__main__':
    # All counts (cts) are per 60 seconds.
    # PMT 1
    # Discriminator 1 voltage is 1.508 V
    hv1 =  [1.168, 1.173, 1.183, 1.188, 1.197, 1.225, 1.235, 1.242, 1.251, 1.260, 1.272, 1.292,
          1.311, 1.322, 1.334, 1.344, 1.357, 1.364, 1.377, 1.385, 1.401, 1.421, 1.442, 1.465]
    cts1 = [12, 13, 14, 19, 19, 22, 27, 41, 53, 46, 41, 93, 115,
           137, 155, 173, 220, 233, 281, 325, 380, 534, 733, 915]
    PMT1 = PMT(hv1,cts1)

    # PMT 2
    # Discriminator 2 voltage is 1.505 V
    hv2 = [1.163, 1.172, 1.181, 1.191, 1.200, 1.217, 1.248,
          1.277, 1.312, 1.343, 1.351, 1.361, 1.371, 1.380]
    cts2 = [751, 834, 935, 1109, 1263, 1679, 2595, 3540, 4812, 7157, 10612, 14285, 32415, 92540]
    PMT2 = PMT(hv2,cts2)
    # PMT 3

    hv3 = [1.152, 1.164, 1.172, 1.182, 1.193, 1.207, 1.213, 1.223, 1.233, 1.243, 1.254, 1.267, 1.273, 1.282,
           1.295, 1.303, 1.314, 1.323, 1.333, 1.343, 1.352, 1.364, 1.374, 1.383, 1.394, 1.406, 1.416, 1.424,
           1.433, 1.443, 1.453, 1.463, 1.474, 1.488, 1.500, 1.512, 1.523, 1.533, 1.543, 1.554, 1.566, 1.578,
           1.589, 1.600]
    cts3 = [306, 360, 375, 521, 565, 652, 697, 861, 918, 1112, 1203, 1316, 1491, 1591, 1758, 1824, 2081, 2240,
            2438, 2645, 2817, 3036, 3354, 3505, 3725, 4045, 4359, 4565, 4735, 4954, 5226, 5489, 5714, 6174,
            6677, 7137, 7539, 8137, 8825, 9948, 11488, 13889, 15846, 21504]
    PMT3 = PMT(hv3,cts3)


    ## Second attempt at discriminator 1. v_dis = 1.508 V
    hv1 = [1.178, 1.188, 1.200, 1.212, 1.221, 1.237, 1.247, 1.257, 1.267, 1.277, 1.287,
           1.300, 1.312, 1.322, 1.351, 1.400, 1.451, 1.500, 1.550, 1.665, 1.700]
    cts1 = [3,2,3,3,8,11, 3,9,8,11,13,12,14,21,37,54,124,181,328,572,869]

    #PMTxx = PMT(hv1,cts1)
    #PMTxx.plot_plateau(title=r"$PMT_1 --- v_{dis} = 1.508 V$")
    ### Analysis
    #PMT1.plot_plateau(title=r"$PMT 1 -- v_{dis} = 1.508 V")
    #PMT2.plot_plateau(title=r"$PMT 2 -- v_{dis} = 1.505 V")
    #PMT3.plot_plateau(title=r"$PMT 3 -- v_{dis} = 1.509 V")

    read_SPE("muon_data.spe")