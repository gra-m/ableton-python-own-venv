import numpy as np
import matplotlib.pyplot as plt
# Create waveform from a time list with cos, slice it into a representation of one cycle
# ready to be sent as a cc message to an instrument that can modulate itself

def modulation_shape(repeat=1):
    """function that plots a modulation shape"""
    # 0 to 80 with a resolution of 0.1
    time_list = np.arange(0, 80.1, 0.1)
    amplitude = np.cos(time_list)
    print("------------------------numpy.arange()--------------------")
    print(time_list)
    print("------------------------Init list--------------------")
    print(amplitude)
    # plt.plot(amplitude)
    # plt.show()
    time_list_cycle_slice = time_list[1:62]
    amplitude_list_cycle_slice = amplitude[1:62]

    plt.plot(time_list_cycle_slice, amplitude_list_cycle_slice)
    plt.xlabel("Time")
    plt.ylabel("Amplitude == sin(time)")
    plt.grid(True, "both", "both")
    plt.axhline(y=0, color="k")
    plt.show()


modulation_shape(20)
