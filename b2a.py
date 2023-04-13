import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np
import scipy.io.wavfile as wavfile
import sys


class BinaryToAudioGUI:
    def __init__(self, master):
        self.master = master
        master.title("Binary to Audio Converter")

        # Set window size to 16:9 aspect ratio
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        width = int(screen_width * 0.5)
        height = int(width / 1.7777778)
        x = int((screen_width - width) / 2)
        y = int((screen_height - height) / 2)
        master.geometry(f"{width}x{height}+{x}+{y}")

        # Create input file selection button and label
        self.input_file_label = tk.Label(master, text="Input file:")
        self.input_file_label.pack(anchor="w")
        self.input_file_button = tk.Button(master, text="Select file", command=self.select_input_file)
        self.input_file_button.pack(fill="x", pady=10)

        # Create output file selection button and label
        self.output_file_label = tk.Label(master, text="Output file:")
        self.output_file_label.pack(anchor="w")
        self.output_file_button = tk.Button(master, text="Select file", command=self.select_output_file)
        self.output_file_button.pack(fill="x", pady=10)

        # Create bit duration field and label
        self.bit_duration_label = tk.Label(master, text="Bit duration (s):")
        self.bit_duration_label.pack(anchor="w")
        self.bit_duration_entry = tk.Entry(master)
        self.bit_duration_entry.pack(fill="x", pady=10)
        self.bit_duration_entry.insert(0, "0.01")

        # Create frequency fields and labels
        self.freq0_label = tk.Label(master, text="Frequency for bit '0' (Hz):")
        self.freq0_label.pack(anchor="w")
        self.freq0_entry = tk.Entry(master)
        self.freq0_entry.pack(fill="x", pady=10)
        self.freq0_entry.insert(0, "1000")
        self.freq1_label = tk.Label(master, text="Frequency for bit '1' (Hz):")
        self.freq1_label.pack(anchor="w")
        self.freq1_entry = tk.Entry(master)
        self.freq1_entry.pack(fill="x", pady=10)
        self.freq1_entry.insert(0, "2000")

        # Create start conversion button
        self.convert_button = tk.Button(master, text="Convert", command=self.convert)
        self.convert_button.pack(fill="x", pady=20)

        # Initialize instance variables
        self.input_file = None
        self.output_file = None
        self.freq0 = None
        self.freq1 = None
        self.duration = None
        self.sample_rate = 44100

    def select_input_file(self):
        self.input_file = filedialog.askopenfilename()
        self.input_file_label.config(text=f"Input file: {self.input_file}")

    def select_output_file(self):
        self.output_file = filedialog.asksaveasfilename(defaultextension=".wav")
        self.output_file_label.config(text=f"Output file: {self.output_file}")

    def generate_tone(self, bit):
        if bit == '0':
            freq = self.freq0
        elif bit == '1':
            freq = self.freq1
        else:
            raise ValueError("Invalid bit value")

        t = np.linspace(0, self.duration, int(self.sample_rate * self.duration), False)
        tone = np.sin(freq * 2 * np.pi * t)
        return tone

    def binary_to_audio(self):
        with open(self.input_file, 'rb') as file:
            binary_data = file.read()

        bit_string = ''.join(format(byte, '08b') for byte in binary_data)
        audio_data = np.array([], dtype=np.float32)

        for bit in bit_string:
            tone = self.generate_tone(bit)
            audio_data = np.concatenate((audio_data, tone))

        wavfile.write(self.output_file, self.sample_rate, audio_data)

    def convert(self):
        if not self.input_file:
            messagebox.showerror("Error", "Please select an input file.")
            return

        if not self.output_file:
            messagebox.showerror("Error", "Please select an output file.")
            return

        try:
            self.duration = float(self.bit_duration_entry.get())
            self.freq0 = float(self.freq0_entry.get())
            self.freq1 = float(self.freq1_entry.get())

            self.binary_to_audio()
            messagebox.showinfo("Success", "Conversion complete.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", str(e))



root = tk.Tk()
gui = BinaryToAudioGUI(root)
root.mainloop()
