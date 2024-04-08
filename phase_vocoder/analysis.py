import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

def hanning_window(N):
    """
    Generate Hanning window of length N.
    """
    return 0.5 - 0.5 * np.cos(2 * np.pi * np.arange(N) / (N - 1))

# Read audio data from WAV file
filename = 'samples/test_mono.wav'  # Provide the path to your WAV file
fs, x = wavfile.read(filename)

# Define parameters for spectrogram
N = 256  # Length of the windowed segments
overlap = 128  # Overlap between segments
w = hanning_window(N)  # Hanning window

# Compute spectrogram manually using DFT
spectrogram = []
for i in range(0, len(x) - N, overlap):
    segment = x[i:i + N] * w
    X = np.fft.fft(segment, n=N)
    spectrogram.append(np.abs(X))

# Convert to numpy array
spectrogram = np.array(spectrogram).T

# Plot the spectrogram
plt.imshow(spectrogram, aspect='auto', origin='lower', extent=[0, len(x) / fs, 0, fs / 2])
plt.xlabel('Time [s]')
plt.ylabel('Frequency [Hz]')
plt.title('Spectrogram')
plt.colorbar(label='Intensity [dB]')
plt.show()