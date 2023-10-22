import numpy as np
import matplotlib.pyplot as plt


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


print("------------------------------------------------------------")
print(convert_range(5, 0, 10, 0, 100))


def modulation_shape(repeat=1):
    time_list = np.arange(0, 80.1, 0.1)
    amplitude = np.sin(time_list)
    #print("------------------------time_list = numpy.arange 0->80 resolution .1--------------------")
    #print(time_list)
    #print("------------------------np.cos(time_list)--------------------")
    #print(amplitude)
    time_list_cycle_slice = time_list[1:62]
    amplitude_list_cycle_slice = amplitude[1:62]
    plt.title("Modulation Shape")
    plt.plot(time_list_cycle_slice, amplitude_list_cycle_slice)
    plt.xlabel("Time")
    plt.ylabel("Amplitude == sin(time)")
    plt.grid(True, "both", "both")
    plt.axhline(y=0, color="k")
    plt.show()
    return amplitude


amp = modulation_shape(1)

# print("amp = ", amp)

count = 1
converted_amplitude = []
for sin_of_time_list_slice in amp:
    # print(sin_of_time_list_slice, " -> original sin_of_time_slice")
    converted = convert_range(sin_of_time_list_slice, -1.0, 1, 0, 127)
    print(count, " ", converted)
    converted_amplitude.append(converted)
    count = count + 1

converted_amplitude_size = len(converted_amplitude)
print(converted_amplitude_size)

