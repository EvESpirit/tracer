import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from ttkthemes import ThemedTk
from b2a import binary_to_audio

"""
GUI frontend for b2a.py
"""


def open_input_file():
    input_path.set(filedialog.askopenfilename(title="Select input file"))


def open_output_file():
    output_path.set(filedialog.asksaveasfilename(title="Select output file", defaultextension=".wav"))


def convert():
    input_file = input_path.get()
    output_file = output_path.get()
    freq0 = int(freq0_entry.get())
    freq1 = int(freq1_entry.get())
    duration = float(duration_entry.get())
    sample_rate = int(sample_rate_entry.get())
    mode = mode_var.get()

    binary_to_audio(input_file, output_file, freq0, freq1, duration, sample_rate, mode)
    status_label.config(text="Conversion complete")


root = ThemedTk(theme="arc")
root.title("Binary to Audio Converter")

input_path = tk.StringVar()
output_path = tk.StringVar()
mode_var = tk.StringVar()

mainframe = ttk.Frame(root, padding="12 12 12 12")
mainframe.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

input_label = ttk.Label(mainframe, text="Input file:")
input_label.grid(row=0, column=0, sticky="E", padx=(0, 5), pady=(5, 5))
input_entry = ttk.Entry(mainframe, textvariable=input_path)
input_entry.grid(row=0, column=1, padx=(0, 5), pady=(5, 5))
input_button = ttk.Button(mainframe, text="Browse", command=open_input_file)
input_button.grid(row=0, column=2, padx=(0, 5), pady=(5, 5))

output_label = ttk.Label(mainframe, text="Output file:")
output_label.grid(row=1, column=0, sticky="E", padx=(0, 5), pady=(5, 5))
output_entry = ttk.Entry(mainframe, textvariable=output_path)
output_entry.grid(row=1, column=1, padx=(0, 5), pady=(5, 5))
output_button = ttk.Button(mainframe, text="Browse", command=open_output_file)
output_button.grid(row=1, column=2, padx=(0, 5), pady=(5, 5))

freq0_label = ttk.Label(mainframe, text="Frequency for '0':")
freq0_label.grid(row=2, column=0, sticky="E", padx=(0, 5), pady=(5, 5))
freq0_entry = ttk.Entry(mainframe)
freq0_entry.grid(row=2, column=1, padx=(0, 5), pady=(5, 5))
freq0_entry.insert(0, "1000")

freq1_label = ttk.Label(mainframe, text="Frequency for '1':")
freq1_label.grid(row=3, column=0, sticky="E", padx=(0, 5), pady=(5, 5))
freq1_entry = ttk.Entry(mainframe)
freq1_entry.grid(row=3, column=1, padx=(0, 5), pady=(5, 5))
freq1_entry.insert(0, "2000")

duration_label = ttk.Label(mainframe, text="Duration of each bit/byte:")
duration_label.grid(row=4, column=0, sticky="E", padx=(0, 5), pady=(5, 5))
duration_entry = ttk.Entry(mainframe)
duration_entry.grid(row=4, column=1, padx=(0, 5), pady=(5, 5))
duration_entry.insert(0, "0.01")

sample_rate_label = ttk.Label(mainframe, text="Sample rate:")
sample_rate_label.grid(row=5, column=0, sticky="E", padx=(0, 5), pady=(5, 5))
sample_rate_entry = ttk.Entry(mainframe)
sample_rate_entry.grid(row=5, column=1, padx=(0, 5), pady=(5, 5))
sample_rate_entry.insert(0, "44100")

mode_label = ttk.Label(mainframe, text="Encoding mode:")
mode_label.grid(row=6, column=0, sticky="E", padx=(0, 5), pady=(5, 5))
mode_radiobutton1 = ttk.Radiobutton(mainframe, text="Bit", variable=mode_var, value="bit")
mode_radiobutton1.grid(row=6, column=1, sticky="W")
mode_radiobutton1.invoke()
mode_radiobutton2 = ttk.Radiobutton(mainframe, text="Byte", variable=mode_var, value="byte")
mode_radiobutton2.grid(row=6, column=1, sticky="E")

convert_button = ttk.Button(mainframe, text="Convert", command=convert)
convert_button.grid(row=7, column=1, pady=(10, 5))

status_label = ttk.Label(mainframe, text="")
status_label.grid(row=8, column=1, pady=(5, 5))

root.mainloop()
