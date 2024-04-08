# SP-Phase-Vocoder

This repository contains a python implementation of Phase Vocoder based on [Guitar Pitch Shifter](https://www.guitarpitchshifter.com/algorithm.html). A summary of the method is provided in the _report_ directory.

The Algorithm is used to scale a digital signal over the time domain by a factor of $s$ without changing the pitch.

Sample outputs are provided in the _samples_ directory.

## Installation

Clone this repository to your local machine using:
```
git clone https://github.com/simply-pleb/SP-Phase-Vocoder.git
```

## Usage

0. Make sure to have python installed (my version was 3.10).
1. Install the required dependencies by running:
```
pip install numpy scipy
```
2. Run the Phase Vocoder bash script 'run.sh' with the following command-line arguments:
```
./run.sh <input.wav> <output.wav> <time_stretch_ratio>
``` 
- <input.wav>: path to the input WAV file.
- <output.wav>: path to save the output WAV file.
- <time_stretch_ratio>: Time stretch ratio to apply to the input audio (e.g., 0.5 for half the original duration, 2.0 for double the original duration).

Example usage:
```
./run.sh samples/test_mono.wav samples/output.wav 1.3
```
