"""Example demonstrating FFT computation and inversion."""
from client import FastFourierTransform

def main():
    sig = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
    spec = FastFourierTransform.fft(sig)
    print("FFT Magnitudes:", [round(abs(c), 2) for c in spec])
    recon = FastFourierTransform.ifft(spec)
    print("Reconstructed Signal:", recon)

if __name__ == "__main__":
    main()
