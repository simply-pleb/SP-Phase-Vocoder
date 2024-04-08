import numpy as np

import phase_vocoder.constants as constants

def frame_signal(signal: np.array) -> list:
    L = (len(signal) - constants.N) // constants.HOP_A + 1  # Number of frames
    frames = np.zeros((L, constants.N))  # Initialize array to store frames

    for l in range(L):
        start = l * constants.HOP_A  # Start index of the frame
        end = start + constants.N  # End index of the frame
        frames[l] = signal[start:end]  # Extract frame from signal

    return frames

def dft(signal: np.array) -> np.array:    
    w = np.hanning(constants.N)
    signal = signal * w
    
    spectrum = np.fft.fft(signal)

    return spectrum

def perform_analysis(signal: np.array) -> np.array:
    signal_frames = frame_signal(signal)
    
    # Perform DFT on each frame
    frame_spectra = []
    for frame in signal_frames:
        spectrum = dft(frame)
        # Apply magnitude thresholding
        spectrum[np.abs(spectrum) < constants.THRESHOLD_E] = 0
        frame_spectra.append(spectrum)
    
    return frame_spectra