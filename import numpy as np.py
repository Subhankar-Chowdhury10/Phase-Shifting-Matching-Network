import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import tkinter as tk
from tkinter import ttk
from schemdraw import Drawing
from schemdraw.elements import Resistor
from skrf import Network

class PhaseShiftingMatchingNetworkDesigner:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Phase Shifting Matching Network Designer")
        self.create_widgets()
        self.root.mainloop()

    def create_widgets(self):
        self.label1 = ttk.Label(self.root, text="Load Impedance:")
        self.label1.grid(row=0, column=0)
        self.r_load_entry = ttk.Entry(self.root)
        self.r_load_entry.grid(row=0, column=1)
        self.x_load_entry = ttk.Entry(self.root)
        self.x_load_entry.grid(row=0, column=2)

        self.label2 = ttk.Label(self.root, text="Source Impedance:")
        self.label2.grid(row=1, column=0)
        self.r_source_entry = ttk.Entry(self.root)
        self.r_source_entry.grid(row=1, column=1)
        self.x_source_entry = ttk.Entry(self.root)
        self.x_source_entry.grid(row=1, column=2)

        self.compute_button = ttk.Button(self.root, text="Compute Matching Network", command=self.compute_matching_network)
        self.compute_button.grid(row=2, columnspan=3)

    def compute_matching_network(self):
        r_load = float(self.r_load_entry.get())
        x_load = float(self.x_load_entry.get())
        r_source = float(self.r_source_entry.get())
        x_source = float(self.x_source_entry.get())

        load_impedance = r_load + 1j * x_load
        source_impedance = r_source + 1j * x_source

        def phase_shift_network_loss(params):
            # The phase shift network is represented by two capacitors
            c1, c2 = params
            z1 = -1j / (2 * np.pi * c1 * 1e6)
            z2 = -1j / (2 * np.pi * c2 * 1e6)
            total_impedance = source_impedance + z1 + z2
            return np.abs((total_impedance - load_impedance) / total_impedance)

        initial_guess = [10e-12, 10e-12]  # Initial guess for capacitor values in Farads
        result = minimize(phase_shift_network_loss, initial_guess, method='Nelder-Mead')
        best_c1, best_c2 = result.x

        self.plot_matching_network(best_c1, best_c2)

    def plot_matching_network(self, c1, c2):
        d = Drawing()
        d += Resistor(label='R1')
        d += Resistor(label='R2')
        d += Resistor(label='R3')
        d += Resistor(label='R4')
        d += Resistor(label='R5')
        d += Resistor(label='R6')

        d += Resistor(d='right', xy=d.R6.end, label='RL')
        d += Resistor(d='up', label='Rs')
        d += Resistor(d='up', label='Z1', start=d.Rs.start)
        d += Resistor(d='up', label='Z2', start=d.Z1.start)

        d.draw()
        plt.show()

if __name__ == "__main__":
    PhaseShiftingMatchingNetworkDesigner()
