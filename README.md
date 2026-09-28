# Radix-2 Cooley-Tukey Fast Fourier Transform Skill

In-place decimation-in-time (DIT) Fast Fourier Transform with bit-reversal sorting and butterfly twiddle factor recombination.

```mermaid
flowchart LR
    Time["Time Domain Signal x[n]"] --> BitRev["Bit-Reversal Permutation"]
    BitRev --> Butterfly["Log2(N) Butterfly Stages (Twiddle W_N^k)"]
    Butterfly --> Freq["Frequency Spectrum X[k]"]
    Freq --> IFFT["Conjugate Reversal IFFT"]
    IFFT --> Time
```

## Features
- **100% Python Standard Library**: Pure standard complex math.
- **O(N log N) Efficiency**: High-performance discrete Fourier transform.
- **Round-Trip Precision**: Exact analytical inversion.
