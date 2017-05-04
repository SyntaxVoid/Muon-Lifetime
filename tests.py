import numpy as np
import matplotlib.pyplot as plt

KEVIN = True

###################### TESTING ZONE ##########################
# Kevins data
if KEVIN:
    ## Approximated from his paper...
    t = np.array(np.linspace(1.5, 19.5, 19))
    y1 = [90, 60, 58, 30, 24, 17, 5, 4, 5, 3, 1, 3, 4, 1, 3, 1, 1, 1, 0]
    y2 = max(y1) * np.exp((t[0] - t) / 2.6)
    plt.plot(t, y1, "r*")
    plt.plot(t, y2, "g-")
    plt.show()
'''
assert which_bin([1,2,3,4,5], 1.3) == 0
assert which_bin([1,2,3,4,5], 4.2) == 3
assert which_bin([1,2,3,4,5], 5) == 3
assert which_bin([1,2,3,4,5], 10) == -1
'''

def xy_to_mathematica(x,y,out):
    with open(out,"w") as o:
        o.write("{")
        for a,b in zip(x,y):
            o.write("{{{},{}}},".format(a,b))
        o.write("}")
    return
xy_to_mathematica(t,y1,"kevin.txt")