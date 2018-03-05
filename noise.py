import cmath
import math
import numpy as np
import matplotlib.pyplot as plt
import random
import itertools

def getPhasor(A, phi):
    return A * (math.cos(phi) + math.sin(phi) * 1j)

class Wave:
    def __init__(self, phasors):
        self.phasors = phasors

    def __mul__(self, scalar):
        return Wave([p * scalar for p in self.phasors])

    def __div__(self, scalar):
        return Wave([p / scalar for p in self.phasors])

    def __add__(self, other):
        zipped = itertools.zip_longest(self.phasors, other.phasors)
        return Wave([(x or 0) + (y or 0) for x, y in zipped])

    def __sub__(self, other):
        return self + (other * -1)

    def harmonics(self):
        for idx, phasor in enumerate(self.phasors):
            amplitude = abs(phasor)
            phase = cmath.phase(phasor)
            frequency = idx + 1
            yield amplitude, frequency, phase
 
    def evaluate(self, x):
        return sum([A / w * math.sin(w * x + phi) for A, w, phi in self.harmonics()])

class WaveGenerator:
    def __init__(self, harmonics):
       self.harmonics = harmonics

    def generate(self):
        for i in range(self.harmonics):
            phase = random.random() * 2 * math.pi
            amplitude = random.random()
            yield getPhasor(amplitude, phase)

    def wave(self):
        return Wave(list(self.generate()))


class ImpulseGenerator:
    def __init__(self, amplitude, phase, harmonics):
        self.amplitude = amplitude
        self.phase = math.pi / 2 - phase
        self.harmonics = harmonics

    def generate(self):
        for i in range(self.harmonics):
            sign = math.pow(-1, i + 1)
            p = getPhasor(self.amplitude * (i + 1), self.phase)
            yield sign * p

    def wave(self):
        return Wave(list(self.generate()))

class SquareWaveGenerator:
    def __init__(self, amplitude, phase, harmonics):
        self.amplitude = amplitude
        self.phase = phase
        self.harmonics = harmonics

    def generate(self):
        for i in range(self.harmonics):
            yield ((i + 1) % 2) * getPhasor(self.amplitude, self.phase)

    def wave(self):
        return Wave(list(self.generate()))
            
if __name__ == '__main__':
    harmonics = 7
    #wave_gen = WaveGenerator(harmonics)
    imp_gen = ImpulseGenerator(1, 0, harmonics)
    wave = WaveGenerator(harmonics).wave()
    impulse = imp_gen.wave() * (1.0 / 5)
    #i2 = ImpulseGenerator(1, math.pi / 2, harmonics).wave()
    #wave = SquareWaveGenerator(1, 0, harmonics).wave()
    x = np.linspace(0, 2 * math.pi, 100)
    f = np.vectorize((wave - impulse).evaluate)
    plt.plot(x, f(x))
    plt.show()
    
