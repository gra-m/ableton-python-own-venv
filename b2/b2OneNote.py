import rtmidi2
import time
# Create a virtual midi port and map it to in/track in ableton, add an instrument to channel1 arm and choose midi
# this plays a middle 3 for half a second


midiOut = rtmidi2.MidiOut()
ports = rtmidi2.get_out_ports()
print(ports)

midiOut.open_port(2)

midiOut.send_noteon(0x90, 60, 100)
time.sleep(0.5)
midiOut.send_noteoff(0x90, 60)








