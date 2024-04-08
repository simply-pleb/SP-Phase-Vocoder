#!/bin/bash

# Check if correct number of arguments is provided
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <input.wav> <output.wav> <time_stretch_ratio>"
    exit 1
fi

# Assigning arguments to variables
input_wav="$1"
output_wav="$2"
time_stretch_ratio="$3"

# Running the Python script with provided arguments
python src/main.py "$input_wav" "$output_wav" "$time_stretch_ratio"
