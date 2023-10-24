import time
import rtmidi2
import numpy as np
from scipy import signal as sig
import matplotlib.pyplot as plt
import threading

# NEW only draws these for now period 1 max duration 1.00001 = 1 cycle
PERIOD = 1
# Originally got rid of flicker on repeat (B8) it was a way of returning modulation shape to start, here is just used
# for experimentation
MAX_DURATION_ADDITIONAL = 0
# start for wave ranges
START = 0
SAW = "SAW"
SINE = "SINE"
SQUARE = "SQUARE"
# TRIANGLE = "TRIANGLE" not available in
MODULATION_SHAPE = SAW

# MELODY
# 4/4 4bpb
REPEAT_BAR = 4
BPM = 60

# OLD
# send only the slice as you have made it to the channel and cc num below, alt will be list based on entire time list
send_slice_to_mod = True
# if sending a slice repeats need to be higher, otherwise effect can be very short
REPEAT = 8
# the required values for mapping this to I think the single byte available to cc 0-127 = 128 bits
IN_MIN = -1
IN_MAX = 1
OUT_MIN = 0
OUT_MAX = 127

CHANNEL = 0
CC_NUM = 75
BETWEEN_MESSAGE_SLEEP = 0.001
portList = rtmidi2.get_out_ports()
midiOut = rtmidi2.MidiOut()
timeUnit = .5
midiOut.open_port(1)

TIME_LIST_START = 0
TIME_LIST_END = 80.1
# Increment size in created list
GRANULARITY = 0.01

SLICE_START = 0
SLICE_END = 1258
print_modulation_param_report = True
print_send_report = True
show_full_plot = False
show_slice_plot = False


def play_melody(melody, bpm):
    """Loops over melody list"""
    for pitch, duration in melody:
        sleep_duration_to_fill_beat = duration_to_time_delay(duration, bpm)
        midiOut.send_noteon(0x90, pitch, 112)
        print("-------------------------------------------------------------")
        print("-------------------------------------------------------------")
        print(f"\nsleep_duration_to_fill_beat {sleep_duration_to_fill_beat}")
        time.sleep(sleep_duration_to_fill_beat)
        midiOut.send_noteoff(0x80, pitch)


def play_modulation(y, max_duration):
    max_duration += MAX_DURATION_ADDITIONAL
    pause_duration = max_duration / y.size
    printValues = False
    # Sending slices of modulation pattern
    for v in y:
        v = convert_range(v, -1.0, 1.0, 0, 127)
        if printValues:
            print(f"Sending modulation value {v}")
        midiOut.send_cc(CHANNEL, CC_NUM, v)
        if printValues:
            print(f"pausing for {pause_duration} before next modulation v in y")
        time.sleep(pause_duration)


def print_modulation_curve_params(time_list_size, amplitude_size, time_list_slice_size, amplitude_list_slice_size):
    print(f"MIDI_PORTS_rtmidi2_SEES {rtmidi2.get_out_ports()}")
    print(f"TIME_LIST_START/END/SPACING {TIME_LIST_START} {TIME_LIST_END} {GRANULARITY}")
    print(f"time_list_size/amplitude(list)_size {time_list_size} / {amplitude_size}")
    print(
        f"SLICE_START/END/timeSliceSize/ampSliceSize {SLICE_START} / {SLICE_END} / {time_list_slice_size} / {amplitude_list_slice_size}")


# Comments == current level of understanding
def convert_range(value, in_min, in_max, out_min, out_max):
    """for convert_range value 5 , in_min -1, in_max 1, out_min 0, out_max 127
    left_span = 1 - -1  == 2
    right_span = 127 - 0 = 127
    left_scaled =  5 - -1 == 6 / 2 == 3
    scaled_value = 0 + 3 * 127 = 0 + 381 == 381
    """
    left_span = in_max - in_min
    right_span = out_max - out_min
    left_scaled = (value - in_min) / left_span
    scaled_value = out_min + (left_scaled * right_span)
    # possibility of getting better rounding if in_min -10 in_max 10? then np.float_something etc. to int? d/k if
    # even useful
    return np.round(scaled_value)


def send_mod(amplitude, repeat):
    """A function that will send CC data to a MIDI driver"""
    scaled = []
    not_printed = True
    for amp_a in amplitude:
        val = convert_range(amp_a, IN_MIN, IN_MAX, OUT_MIN, OUT_MAX)
        scaled.append(val)
    for _ in range(repeat):
        if print_send_report & not_printed:
            print(
                f"scaled list put through convert range inmin {IN_MIN} / max {IN_MAX} / outmin {OUT_MIN} / max {OUT_MAX} "
                f"of size: {len(scaled)} ")
            not_printed = False
        for value in scaled:
            # rtmidi way mod = ([CONTROL_CHANGE | CHANNEL, CC_NUM, value])
            midiOut.send_cc(CHANNEL, CC_NUM, value)
            time.sleep(BETWEEN_MESSAGE_SLEEP)


def print_plot(title, xlabel, ylabel, time_list, amplitude_list):
    plt.title(title)
    plt.plot(time_list, amplitude_list)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True, "both", "both")
    plt.axhline(y=0, color="k")
    plt.show()


def modulation_shape(REPEAT):
    """
    The shape of the modulation as decided by numpy -> cos, sin etc. The labels do not auto update just showing sin at
    the moment
    :param repeat:  default 1 == how many times the curve mapped amplitude steps will eventually be sent
    :return: void
    """
    # return evenly spaced values within a given interval
    time_list = np.arange(TIME_LIST_START, TIME_LIST_END, GRANULARITY)
    time_list_size = time_list.size

    # CHANGE MODULATION HERE  cos, sin
    amplitude = np.sin(time_list)
    amplitude_size = amplitude.size

    time_list_cycle_slice = time_list[SLICE_START:SLICE_END]
    # just used for plotting, calculated from scratch below
    amplitude_list_cycle_slice = amplitude[SLICE_START:SLICE_END]

    # CHANGE MODULATION HERE cos, sin
    amplitude_slice = np.sin(time_list_cycle_slice)

    # stops here until dismissed
    if show_full_plot:
        print_plot("Full Shape prior to slicing one modulation", "Time", "Amplitude == sin(time)", time_list, amplitude)
    if show_slice_plot:
        print_plot("Slice Shape", "Time", "Amplitude == sin(time)", time_list_cycle_slice, amplitude_list_cycle_slice)
    if print_modulation_param_report:
        time_list_slice_size = time_list_cycle_slice.size
        amplitude_list_slice_size = amplitude_list_cycle_slice.size
        print_modulation_curve_params(time_list_size, amplitude_size, time_list_slice_size, amplitude_list_slice_size)
    if send_slice_to_mod:
        send_mod(amplitude_slice, REPEAT)
    else:
        send_mod(amplitude, REPEAT)


def get_modulation_shape(shape: str, period: float, max_duration: float, granularity: float):
    x = np.arange(START, max_duration + MAX_DURATION_ADDITIONAL, granularity)
    if shape == "SINE":
        y = np.sin(2 * np.pi / period * x)
    elif shape == "SAW":
        y = sig.sawtooth(2 * np.pi / period * x)
    elif shape == "SQUARE":
        y = sig.square(2 * np.pi / period * x)
    else:
        raise ValueError(f"unknown shape {shape}")

    print_plot("Modulation Shape", "Time", f"Amplitude = {shape} (time)", x, y)
    return y


def duration_to_time_delay(note_duration, bpm):
    if note_duration == "w":
        factor = 4
    elif note_duration == "h":
        factor = 2
    elif note_duration == "q":
        factor = 1
    elif note_duration == "e":
        factor = 0.5
    elif note_duration == "s":
        factor = 0.25
    else:
        assert False
    bps = bpm / 60

    return factor * bps


# list comprehension
def duration_of_melody(melody, bpm):
    return sum(duration_to_time_delay(duration, bpm) for _, duration in melody)


def main():
    print(f"MIDI_PORTS_rtmidi2_SEES {rtmidi2.get_out_ports()}")
    melody = [(60, "e"), (62, "e"), (67, "q"), (62, "q"), (67, "q")] * REPEAT_BAR
    #melody = [(60, "w")]  * REPEAT_BAR
    melody_duration = duration_of_melody(melody, BPM)
    modulation_shape = get_modulation_shape(MODULATION_SHAPE, PERIOD, melody_duration + MAX_DURATION_ADDITIONAL,
                                            GRANULARITY)
    # melody = [(60, "w")]  * REPEAT_BAR
    # melody = [(60, "h"), (60, "h")]  * REPEAT_BAR
    # melody = [(60, "q"), (60, "q"), (60, "q"), (60, "q")]  * REPEAT_BAR
    # check_bar
    print(f"duration of melody: {melody_duration} seconds")
    modulation_thread = threading.Thread(target=play_modulation, args=(modulation_shape, melody_duration))
    melody_thread = threading.Thread(target=play_melody, args=(melody, BPM))
    modulation_thread.start()
    melody_thread.start()


main()
# New
# Old
# modulation_shape(REPEAT)
