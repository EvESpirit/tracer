import numpy as np
import scipy.io.wavfile as wavfile
import sys
import os
from concurrent.futures import ThreadPoolExecutor


def generate_tone(bit, durat, frq0, frq1, sample):
    """
    Generate a sinusoidal wave with the specified frequency and duration.

    Args:
        bit (str): The bit value, '0' or '1'.
        durat (float): The duration of the generated wave in seconds.
        frq0 (int): The frequency of the generated wave for bit '0'.
        frq1 (int): The frequency of the generated wave for bit '1'.
        sample (int): The audio sample rate in Hz.

    Returns:
        ndarray: An array of floating-point values representing the generated audio wave.
    """
    if bit == '0':
        freq = frq0
    elif bit == '1':
        freq = frq1
    else:
        raise ValueError("Invalid bit value")

    t = np.linspace(0, durat, int(sample * durat), False)
    tone = np.sin(freq * 2 * np.pi * t)
    return tone


def generate_tone_byte(byte, durat, freqs, sample):
    """
    Generate a sinusoidal wave with the frequency specified by the given byte value.

    Args:
        byte (int): The byte value.
        durat (float): The duration of the generated wave in seconds.
        freqs (ndarray): An array of frequencies corresponding to the possible byte values.
        sample (int): The audio sample rate in Hz.

    Returns:
        ndarray: An array of floating-point values representing the generated audio wave.
    """
    freq = freqs[byte]

    t = np.linspace(0, durat, int(sample * durat), False)
    tone = np.sin(freq * 2 * np.pi * t)
    return tone


def process_chunk(chunk, dur, fq0, fq1, samplerate, mode):
    """
    Generate an audio wave for a chunk of binary data.

    Args:
        chunk (str or bytes): The binary data chunk to process.
        dur (float): The duration of each bit or byte in seconds.
        fq0 (int): The frequency of the generated wave for bit '0' or the minimum frequency for byte mode.
        fq1 (int): The frequency of the generated wave for bit '1' or the maximum frequency for byte mode.
        samplerate (int): The audio sample rate in Hz.
        mode (str): The encoding mode, either 'bit' or 'byte'.

    Returns:
        ndarray: An array of floating-point values representing the generated audio wave.
    """
    audio_data = np.array([], dtype=np.float32)

    if mode == 'bit':
        for bit in chunk:
            tone = generate_tone(bit, dur, fq0, fq1, samplerate)
            audio_data = np.concatenate((audio_data, tone))
    elif mode == 'byte':
        for byte in chunk:
            tone = generate_tone_byte(byte, dur, np.linspace(fq0, fq1, 256), samplerate)
            audio_data = np.concatenate((audio_data, tone))
    else:
        raise ValueError("Invalid encoding mode")

    return audio_data


def binary_to_audio(ifile, ofile, fq0, fq1, dur, samplerate, mode):
    """
    Convert a binary file to an audio wave.

    Args:
        ifile (str): The path to the input binary file.
        ofile (str): The path to the output audio file.
        fq0 (int): The frequency of the generated wave for bit '
    Returns:
        None
    """
    with open(ifile, 'rb') as file:
        binary_data = file.read()

    if mode == 'bit':
        bit_string = ''.join(format(byte, '08b') for byte in binary_data)
        num_threads = os.cpu_count()
        chunk_size = len(bit_string) // num_threads
        bit_chunks = [bit_string[i:i + chunk_size] for i in range(0, len(bit_string), chunk_size)]
        data_chunks = bit_chunks
    elif mode == 'byte':
        num_threads = os.cpu_count()
        chunk_size = len(binary_data) // num_threads
        byte_chunks = [binary_data[i:i + chunk_size] for i in range(0, len(binary_data), chunk_size)]
        data_chunks = byte_chunks
    else:
        raise ValueError("Invalid encoding mode")

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        audio_chunks = list(executor.map(process_chunk, data_chunks, [dur] * num_threads, [fq0] * num_threads, [fq1] * num_threads, [samplerate] * num_threads, [mode] * num_threads))

    audio_data = np.concatenate(audio_chunks)
    wavfile.write(ofile, samplerate, audio_data)


if __name__ == "__main__":

    if len(sys.argv) != 4:
        print("Usage: python binary_to_audio.py <input_file> <output_file> <mode>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    mode = sys.argv[3]

    freq0 = 1000  # Frequency for binary '0' or the minimum frequency for byte mode
    freq1 = 2000  # Frequency for binary '1' or the maximum frequency for byte mode
    duration = 0.01  # Duration of each bit or byte in seconds
    sample_rate = 44100  # Audio sample rate

    binary_to_audio(input_file, output_file, freq0, freq1, duration, sample_rate, mode)
    print("Binary-to-audio conversion complete.")
