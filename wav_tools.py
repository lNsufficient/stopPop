import scipy.io.wavfile as siw
import numpy as np

def play(a, rate=44100, filename='tmp.wav'):
    siw.write(filename, rate, a)
    print("playing sound...("+filename+")")
    os.system('aplay ' + filename)
    print("...sound was played!")


def read(path):
    rate, a = siw.read(path)
    dt = 1.0/rate
    t = np.array(range(len(a)))*dt
    return rate, a, t
