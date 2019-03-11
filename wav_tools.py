import scipy.io.wavfile as siw

def play(a, rate=44100, filename='tmp.wav'):
    siw.write(filename, rate, a)
    print("playing sound...("+filename+")")
    os.system('aplay ' + filename)
    print("...sound was played!")


def read(path):
    rate, a = siw.read(path)
    return rate, a
