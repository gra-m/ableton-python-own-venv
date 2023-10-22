import rtmidi2
import time

midiOut = rtmidi2.MidiOut()
print(midiOut.ports)
portSetInAbleton = 3
midiOut.open_port(portSetInAbleton)


def send_notes(pitch=60, repeat=4):
    for note in range(repeat):
        midiOut.send_noteon(0x90, pitch, 80)
        time.sleep(.1)
        #midiOut.send_pitchbend(0x90,4000)
        time.sleep(.2)
        midiOut.send_noteoff(0x80, pitch)
        time.sleep(.03)


def return_sum(arg1, arg2):
    """returns the sum of two numbers"""
    result = arg1 + arg2
    return result

for i in range(4):
    send_notes(40, 2)
    send_notes(60)
    send_notes(40, 2)
    send_notes(80)
    send_notes(40, 2)
    send_notes(54)
    returnSum = return_sum(5, 8)
    time.sleep(2.0)

midiOut.close_port()
print(returnSum)
