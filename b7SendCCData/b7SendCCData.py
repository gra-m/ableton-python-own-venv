import time
# from rtmidi.midiconstants import (CONTROL_CHANGE) not needed with rtmidi2
import rtmidi2
import numpy as np
import matplotlib.pyplot as plt
CHANNEL = 0
CC_NUM = 75
SPEED = 0.01
portList = rtmidi2.get_out_ports()
midiOut = rtmidi2.MidiOut()
timeUnit = .5
print(rtmidi2.get_out_ports())
midiOut.open_port(1)


# our range is not something that midi/ableton could understand, it is not 0->127


def convert_range(value, in_min, in_max, out_min, out_max):
    """for convert_range value 5, in_min 0, in_max 10, out_min 0, out_max 100
    left_span = 10 - 0 == 10
    right_span = 100 - 0 = 100
    left_scaled = 5 - 0 == 5 / 10 == .5
    scaled_value = 0 + .5 * 100 = 0 + 50 == 50
    """
    left_span = in_max - in_min
    right_span = out_max - out_min
    left_scaled = (value - in_min) / left_span
    scaled_value = out_min + (left_scaled * right_span)
    return np.round(scaled_value)


def send_mod(amplitude, repeat):
    """A function that will send CC data to a MIDI driver"""
    scaled = []
    for amp_a in amplitude:
        val = convert_range(amp_a, -1.0, 1.0, 0, 127)
        scaled.append(val)
    for _ in range(repeat):
        for value in scaled:
            # rtmidi way mod = ([CONTROL_CHANGE | CHANNEL, CC_NUM, value])
            midiOut.send_cc(CHANNEL, CC_NUM, value)
            time.sleep(SPEED)


def modulation_shape(repeat=10):
    """plot no longer showing in this version is set to 62 as this looked more perfect when np.cos it still creates 801
    length list, I am just going with this quick as want to get to the good stuff"""
    time_list = np.arange(0, 80.1, 0.1)
    amplitude = np.sin(time_list)
    time_list_cycle_slice = time_list[1:62]
    amplitude_list_cycle_slice = amplitude[1:62]
    plt.title("Modulation Shape")
    plt.plot(time_list_cycle_slice, amplitude_list_cycle_slice)
    plt.xlabel("Time")
    plt.ylabel("Amplitude == sin(time)")
    plt.grid(True, "both", "both")
    plt.axhline(y=0, color="k")
    # plt.show()
    send_mod(amplitude, repeat)
    return amplitude


amp = modulation_shape(1)

count = 1
converted_amplitude = []
for sin_of_time_list_slice in amp:
    converted = convert_range(sin_of_time_list_slice, -1.0, 1, 0, 127)
    print(count, " ", converted)
    converted_amplitude.append(converted)
    count = count + 1

converted_amplitude_size = len(converted_amplitude)
print("Size of list ", converted_amplitude_size)
