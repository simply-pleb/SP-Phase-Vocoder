import numpy as np

import phase_vocoder.constants as constants

def calc_synthesis_stage(frame_spectra_s:list) -> list:
    q_signals = []
    w = np.hanning(constants.N)
    
    for frame_spectrum in frame_spectra_s:
        signal = np.fft.ifft(frame_spectrum)
        signal = signal * w
        q_signals.append(signal)
        
    return q_signals


# def overlap_add_synthesis_frames(q_signals, output_signal_length, hop_s):
    
#     y = []
#     N = output_signal_length
        
#     for n in range(output_signal_length):
#         sum_synth = 0        
#         for i, q_signal in enumerate(q_signals):
#             frame_val = 0
#             # unit_step_overlap = np.heaviside(n - i*hop_s, 0) - np.heaviside(n - i*hop_s - constants.N, 0)
#             if n >= i*hop_s and n < i*hop_s+constants.N:
#                 frame_val = q_signal[n - i*hop_s]
#             sum_synth += frame_val
#         y.append(sum_synth)
    
#     return np.array(y)


def overlap_add_synthesis_frames(q_signals:list, hop_s:int, output_signal_length:int) -> np.array:
    y = np.zeros(output_signal_length, dtype=complex)

    for i, q_signal in enumerate(q_signals):
        start_index = i * hop_s
        end_index = start_index + constants.N
        segment_len = min(constants.N, output_signal_length - start_index)
        y[start_index:end_index] += q_signal[:segment_len]
    
    return y

            
def perform_synthesis(frame_spectra_s:list, hop_s:int, output_signal_length:int) -> np.array:
    q_signals = calc_synthesis_stage(frame_spectra_s)
    y = overlap_add_synthesis_frames(q_signals, hop_s, output_signal_length)
    
    return y