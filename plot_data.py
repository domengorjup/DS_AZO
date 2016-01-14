import numpy as np
import matplotlib.pyplot as plt
import tkinter
from tkinter import filedialog

def main():
    tkinter.Tk().withdraw()
    in_path = filedialog.askopenfilename(title="Choose data file!")

    return in_path


if __name__ == "__main__":
    filepath = main()
    print(filepath)

    xf,yf,zf,freq = np.loadtxt(filepath)



izbor = freq >= 0

plt.plot(freq[izbor], np.abs((zf))[izbor], 'g')
plt.plot(freq[izbor], np.abs((xf))[izbor], 'b')
plt.plot(freq[izbor], np.abs((yf))[izbor], 'r')
plt.xlabel(r'$f$ [Hz]')
plt.grid()
frame = plt.gca()
#frame.axes.get_yaxis().set_ticks([])

plt.show()
