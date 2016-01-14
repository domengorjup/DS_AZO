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

    xf,yf,zf,freq = np.loadtxt(filepath)



    izbor = freq >= 0

    plt.plot(freq[izbor], np.abs((xf))[izbor], 'b', label='x')
    plt.plot(freq[izbor], np.abs((yf))[izbor], 'r', label='y')
    plt.plot(freq[izbor], np.abs((zf))[izbor], 'g', label='z')
    plt.xlabel(r'$f$ [Hz]')
    plt.legend()
    plt.title("AZO data plotter")
    plt.grid()

    plt.show()
