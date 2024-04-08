# Phase Vocoder

method based on https://www.guitarpitchshifter.com/algorithm.html

Algorithm is used to scale a digital signal over the time domain by a factor of $s$ without changing the pitch.

Take note of the following parameters:

- $hop_a = \frac{N}{4}$ (for overlap of $75\%$), the number of samples between two successive windows for analysis stage
- $hop_s = s\times hop_a$ the number of samples between two successive windows for synthesis stage
- $\Delta t_a = \dfrac{hop_a}{f_s}$ time interval of analysis stage
- $\Delta t_s = \dfrac{hop_s}{f_s}$ time interval of synthesis stage
- $L$ number of frames
- TODO: calculate number of steps


## Analysis

Analysis stage equation

- $$(X_a[k])_i = \sum_{n=0}^{N-1} {x[n + i\times (hop_a)]w[n]e^{-j(\frac{2\pi k n}{N})}}$$
- $k = 0,1,2,...,N-1$
- $N$ number of samples in the frame $i$
- $x[n]$ sample signal
- $w[n]$ Hanning window
- $(X_a[k])_i$ discrete spectrum of the frame $i$

## Processing

Frequency bins 

- Applying a FFT of length $N$ results into $N$ frequency bins starting from $0$ up to $\frac{N-1}{N}f_s$
- $f_s$ sampling rate frequency
- $\frac{f_s}{N}$ interval 

Phase shift

- The phase difference between the two frames is referred to as the phase shift $(\Delta \phi_a[k])_i$
- The phase shift can be used to determine the __true frequency__ associated with a bin


### True frequency

True frequency when the phase shift is unwrapped

- $(\omega_{true}[k])_i = \dfrac{(\Delta \phi_a[k])_i}{\Delta t_a}$
- However, the phase information provided by the FFT is wrapped, which implies that $(\Delta \phi_a[k])_i$ lies between $–\pi$ and $\pi$

frequency deviation

- $(\Delta \omega[k])_i = \dfrac{(\phi_a[k])_i - (\phi_a[k])_{i-1}}{\Delta t_a} - \omega_{bin}[k]$ 
- $\omega_{bin}[k]$ bin frequency


Wrapped frequency deviation

- $(\Delta \omega_{wrapped}[k])_i = \text{mod}[((\Delta \omega[k])_i + \pi), 2\pi] - \pi$ 

True frequency

- $(\omega_{true}[k])_i = \omega_{bin}[k] + (\Delta \omega_{wrapped}[k])_i$

### Phase adjustment

Phase adjustment for the synthesis stage

- $(\phi_s[k])_i = (\phi_s[k])_{i-1} +\Delta t_s \times (\omega_{true}[k])_i$ 

Amplitude and phase of the spectrum of the synthesis stage

- $\vert (X_s[k])_i \vert = \vert (X_a[k])_i \vert$
- $\angle (X_s[k])_i = (\phi_s[k])_i$

## Synthesis

Synthesis stage equation

- $$q_i[n] = \left\{ \frac{1}{N} \sum_{k=0}^{N-1}{(X_s[k])_ie^{-j(\frac{2\pi k n}{N})}} \right\} w[n]$$
- $n = 0,1,2,...,N-1$

Overlap-add of the synthesis frames

- $$y[n] = \sum_{i=0}^{L-1}{q_i[n - i\times hop_s]\{u[n - i\times hop_s] - u[n - i\times hop_s - N]\} }$$
- $L$ number of frames
- $u[n]$ unit step function