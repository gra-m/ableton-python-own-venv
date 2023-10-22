import rtmidi2
import time

portList = rtmidi2.get_out_ports()
midiOut = rtmidi2.MidiOut()
timeUnit = .5

print(rtmidi2.get_out_ports())
print(midiOut.ports)


def play_it_on_port(port_num):
    midiOut.open_port(port_num)
    for note in range(8):
        midiOut.send_noteon(0x90, 60, 50)
        time.sleep(timeUnit / 2)
        midiOut.send_noteoff(0x90, 60)
        time.sleep(timeUnit / 2)
        for noteInner in range(3):
            midiOut.send_noteon(0x90, 50, 40)
            time.sleep(timeUnit / 10 * 4)
            midiOut.send_noteoff(0x90, 50)
            time.sleep(timeUnit / 10 * 6)


names = [1, 2, 3, 4, 5]
for name in names:
    print(name)
