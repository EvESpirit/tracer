import numpy as np
import scipy.io.wavfile as wavfile


def bit_string_to_bytes(bit_string):
    """
    Converts a binary string into a byte array.

    Args:
    - bit_string (str): The binary string to be converted.

    Returns:
    - bytes: The byte array converted from the binary string.
    """
    byte_array = bytearray()
    for i in range(0, len(bit_string), 8):
        byte = bit_string[i:i + 8]
        byte_array.append(int(byte, 2))

    return bytes(byte_array)


class AudioToBinary:
    """
    A class for converting audio files to binary data.

    Attributes:
    - freq0 (int): The frequency for a binary 0.
    - freq1 (int): The frequency for a binary 1.
    - duration (float): The duration of each bit in seconds.
    - sample_rate (int): The sample rate of the audio file.
    - mode (str): The encoding mode. Can be "bit" or "byte".

    Methods:
    - load_audio(input_file)
    - decode_bit(tone)
    - demodulate(audio_data)
    - process(input_file, output_file)
    """
    def __init__(self, freq0, freq1, duration, sample_rate, mode):
        """
        Initializes an AudioToBinary object.

        Args:
        - freq0 (int): The frequency for a binary 0.
        - freq1 (int): The frequency for a binary 1.
        - duration (float): The duration of each bit in seconds.
        - sample_rate (int): The sample rate of the audio file.
        - mode (str): The encoding mode. Can be "bit" or "byte".
        """
        self.freq0 = freq0
        self.freq1 = freq1
        self.duration = duration
        self.sample_rate = sample_rate
        self.mode = mode

    def load_audio(self, input_file):
        """
        Loads an audio file and returns the sample rate and audio data.

        Args:
        - input_file (str): The path to the input audio file.

        Returns:
        - tuple: A tuple containing the sample rate and audio data as a numpy array.
        """
        try:
            if not input_file.endswith(".wav"):
                raise Exception("Error: Only WAV files are supported")
            sample_rate, audio_data = wavfile.read(input_file)
            return sample_rate, audio_data
        except FileNotFoundError:
            raise Exception(f"Error: file {input_file} not found")
        except Exception as e:
            raise Exception(f"Error reading file {input_file}: {str(e)}")

    def decode_bit(self, tone):
        """
        Decodes a binary value from a tone.

        Args:
        - tone (numpy array): The audio data for a single bit.

        Returns:
        - str: The binary value decoded from the tone.
        """
        tone_length = len(tone)
        freqs = np.fft.fftfreq(tone_length, 1 / self.sample_rate)
        spectrum = np.fft.fft(tone)

        idx0 = np.argmax(np.abs(freqs - self.freq0) < 10)
        idx1 = np.argmax(np.abs(freqs - self.freq1) < 10)

        if np.abs(spectrum[idx0]) > np.abs(spectrum[idx1]):
            return '0'
        else:
            return '1'

    def demodulate(self, audio_data):
        """
        Demodulates audio data into binary data.

        Args:
        - audio_data (numpy array): The audio data to be demodulated.

        Raises:
        - ValueError: If an invalid encoding mode is specified.

        Returns:
        - str: The binary data demodulated from the audio data.
        """

        def bit_generator():
            bit_duration = int(self.sample_rate * self.duration)
            bit_count = len(audio_data) // bit_duration

            for i in range(bit_count):
                start = i * bit_duration
                end = start + bit_duration
                tone = audio_data[start:end]
                yield self.decode_bit(tone)

        if self.mode == "bit":
            return ''.join(bit_generator())
        elif self.mode == "byte":
            byte_generator = ("".join(bits) for bits in zip(*([bit_generator()] * 8)))
            return ''.join(byte_generator)
        else:
            raise ValueError("Invalid encoding mode")

    def process(self, input_file, output_file):
        """
        Processes an audio file and writes the resulting binary data to an output file.

        Args:
        - input_file (str): The path to the input audio file.
        - output_file (str): The path to the output file.

        Raises:
        - Exception: If there is an error reading or writing the file.

        Returns:
        - None [file output]
        """
        sample_rate, audio_data = self.load_audio(input_file)
        bit_string = self.demodulate(audio_data)
        binary_data = bit_string_to_bytes(bit_string)

        try:
            with open(output_file, 'wb') as file:
                file.write(binary_data)
        except Exception as e:
            raise Exception(f"Error writing file {output_file}: {str(e)}")
