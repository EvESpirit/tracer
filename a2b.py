# audio_to_binary.py
import numpy as np
import scipy.io.wavfile as wavfile


def bit_string_to_bytes(bit_string):
    byte_array = bytearray()
    for i in range(0, len(bit_string), 8):
        byte = bit_string[i:i + 8]
        byte_array.append(int(byte, 2))

    return bytes(byte_array)


class AudioToBinary:
    def __init__(self, freq0, freq1, duration, sample_rate):
        self.freq0 = freq0
        self.freq1 = freq1
        self.duration = duration
        self.sample_rate = sample_rate

    def load_audio(self, input_file):
        try:
            sample_rate, audio_data = wavfile.read(input_file)
            return sample_rate, audio_data
        except FileNotFoundError:
            raise Exception(f"Error: file {input_file} not found")
        except Exception as e:
            raise Exception(f"Error reading file {input_file}: {str(e)}")

    def decode_bit(self, tone):
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
        def bit_generator():
            bit_duration = int(self.sample_rate * self.duration)
            bit_count = len(audio_data) // bit_duration

            for i in range(bit_count):
                start = i * bit_duration
                end = start + bit_duration
                tone = audio_data[start:end]
                yield self.decode_bit(tone)

        return ''.join(bit_generator())

    def process(self, input_file, output_file):
        sample_rate, audio_data = self.load_audio(input_file)
        bit_string = self.demodulate(audio_data)
        binary_data = bit_string_to_bytes(bit_string)

        try:
            with open(output_file, 'wb') as file:
                file.write(binary_data)
        except Exception as e:
            raise Exception(f"Error writing file {output_file}: {str(e)}")