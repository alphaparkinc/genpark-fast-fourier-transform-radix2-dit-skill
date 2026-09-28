"""Radix-2 Cooley-Tukey FFT & IFFT Engine.
100% Python Standard Library.
"""

import math

class FastFourierTransform:
    @staticmethod
    def _bit_reverse(x):
        n = len(x)
        j = 0
        y = list(x)
        for i in range(n - 1):
            if i < j:
                y[i], y[j] = y[j], y[i]
            k = n // 2
            while k <= j:
                j -= k
                k //= 2
            j += k
        return y

    @staticmethod
    def fft(signal):
        n = len(signal)
        assert (n & (n - 1)) == 0, "Signal length must be a power of 2"
        a = FastFourierTransform._bit_reverse([complex(s) for s in signal])
        length = 2
        while length <= n:
            angle = -2.0 * math.pi / length
            wlen = complex(math.cos(angle), math.sin(angle))
            for i in range(0, n, length):
                w = 1.0 + 0.0j
                for j in range(length // 2):
                    u = a[i + j]
                    v = a[i + j + length // 2] * w
                    a[i + j] = u + v
                    a[i + j + length // 2] = u - v
                    w *= wlen
            length *= 2
        return a

    @staticmethod
    def ifft(spectrum):
        n = len(spectrum)
        conjugates = [s.conjugate() for s in spectrum]
        transformed = FastFourierTransform.fft(conjugates)
        return [round(t.conjugate().real / n, 5) for t in transformed]
