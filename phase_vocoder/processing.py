import numpy as np

import phase_vocoder.constants as constants


def _frequency_deviation(frame_spectra_phase: list, bin_frequencies: np.array, dt_a: float) -> list:
    d_omegas = []
    
    d_omegas.append(frame_spectra_phase[0]/dt_a - bin_frequencies)
    for i in range(1, len(frame_spectra_phase)):
        phase_dif = frame_spectra_phase[i] - frame_spectra_phase[i-1]
        d_omegas.append(phase_dif/dt_a - bin_frequencies)
    
    return d_omegas

def _wrapped_frequency_deviation(d_omegas: list) -> list:
    wrapped_delta_omegas = [np.mod(d_omega + np.pi, 2*np.pi) - np.pi for d_omega in d_omegas]
    return wrapped_delta_omegas

def _true_frequency(wrapped_delta_omegas: list, bin_frequencies: np.array) -> list:
    true_omegas = [bin_frequencies + wrapped_delta_omega for wrapped_delta_omega in wrapped_delta_omegas]
    return true_omegas 
 
def calc_true_frequencies(frame_spectra: list, bin_frequencies: np.array, dt_a: float) -> list:
    frame_spectra_phase = []
    for frame_spectrum in frame_spectra:
        frame_spectra_phase.append(np.angle(frame_spectrum))
    
    d_omegas = _frequency_deviation(frame_spectra_phase, bin_frequencies, dt_a)
    wrapped_delta_omegas = _wrapped_frequency_deviation(d_omegas)
    true_omegas = _true_frequency(wrapped_delta_omegas, bin_frequencies)
    
    return true_omegas

def calc_phase_adjustment(true_omegas: list, dt_s: float) -> list:
    phases_s = []
    phases_s.append(dt_s * true_omegas[0])
    
    for i in range(1, len(true_omegas)):
        phases_s.append(phases_s[i-1] + dt_s * true_omegas[i])
    
    return phases_s

def perform_processing(frame_spectra: list, fs: int, hop_s: int) -> list: 
    dt_a = constants.HOP_A/fs
    dt_s = hop_s/fs
    bin_frequencies = np.fft.fftfreq(constants.N)
    
    true_omegas = calc_true_frequencies(frame_spectra, bin_frequencies, dt_a)
    phases_s = calc_phase_adjustment(true_omegas, dt_s)
    
    # change the phase of the frame spectra to phase_s
    frame_spectra_s = []
    for i, phase_s in enumerate(phases_s):
        new_spectrum = np.abs(frame_spectra[i]) * np.exp(1j * phase_s)
        frame_spectra_s.append(new_spectrum)
    
    return frame_spectra_s