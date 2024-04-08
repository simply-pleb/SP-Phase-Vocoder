import sys

import numpy as np
from scipy.io import wavfile

sys.path.append('.')
from phase_vocoder import constants
from phase_vocoder import perform_analysis
from phase_vocoder import perform_processing
from phase_vocoder import perform_synthesis

def main(input_wav:str, output_wav:str, time_stretch_ratio:float):
    # Load the WAV file
    fs, signal = wavfile.read(input_wav)
    
    # Calculate parameters for synthesis
    hop_s = int(time_stretch_ratio * constants.HOP_A)
    output_signal_length = int(len(signal) * time_stretch_ratio)
    
    # Perform phase vocoder 
    frame_spectra = perform_analysis(signal)
    frame_spectra_s = perform_processing(frame_spectra, fs, hop_s)
    y = perform_synthesis(frame_spectra_s, hop_s, output_signal_length)
    
    # Write y to WAV file
    wavfile.write(output_wav, fs, y.astype(np.int16))

if __name__ == '__main__':
    # Check if correct number of command-line arguments is provided
    if len(sys.argv) != 4:
        print("Usage: python main.py <input.wav> <output.wav> <time_stretch_ratio>")
        sys.exit(1)
    
    # Assign command-line arguments to variables
    input_wav = sys.argv[1]
    output_wav = sys.argv[2]
    time_stretch_ratio = float(sys.argv[3])  # Convert time_stretch_ratio to float
    
    # Call the main function with the provided arguments
    main(input_wav, output_wav, time_stretch_ratio)