import loops
import rtmidi2
import time
import mediapipe

midiOut = rtmidi2.MidiOut()
print(midiOut.ports)
portSetInAbleton = 3
midiOut.open_port(portSetInAbleton)

# def send_notes(pitch, repeat):
# for note in range(repeat):


loops.play_it_on_port(portSetInAbleton)


def return_sum(arg1, arg2):
    """returns the sum of two numbers"""
    result = arg1 + arg2
    return result


returnSum = return_sum(5, 8)

print(returnSum)
