import tkinter as tk
from tkinter import filedialog, ttk
from ttkthemes import ThemedTk
from a2b import AudioToBinary


class AudioToBinaryGUI(ThemedTk, AudioToBinary):
    """
    GUI frontend for a2b.py
    """
    def __init__(self, freq0, freq1, duration, sample_rate):

        ThemedTk.__init__(self)
        AudioToBinary.__init__(self, freq0, freq1, duration, sample_rate, None)
        self.title("Audio to Binary Converter")
        self.set_theme("arc")
        self.build_gui()

    def build_gui(self):

        mainframe = ttk.Frame(self)
        mainframe.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.status_label = ttk.Label(mainframe, text="")
        self.status_label.grid(row=5, column=1, pady=(5, 20))

        input_label = ttk.Label(mainframe, text="Input File:")
        input_label.grid(row=0, column=0, padx=(20, 5), pady=(20, 5), sticky="w")

        self.input_entry = ttk.Entry(mainframe, width=50)
        self.input_entry.grid(row=0, column=1, padx=(5, 20), pady=(20, 5))

        input_button = ttk.Button(mainframe, text="Browse", command=self.browse_input)
        input_button.grid(row=0, column=2, padx=(5, 20), pady=(20, 5))

        output_label = ttk.Label(mainframe, text="Output File:")
        output_label.grid(row=1, column=0, padx=(20, 5), pady=(5, 20), sticky="w")

        self.output_entry = ttk.Entry(mainframe, width=50)
        self.output_entry.grid(row=1, column=1, padx=(5, 20), pady=(5, 20))

        output_button = ttk.Button(mainframe, text="Browse", command=self.browse_output)
        output_button.grid(row=1, column=2, padx=(5, 20), pady=(5, 20))

        mode_label = ttk.Label(mainframe, text="Encoding Mode:")
        mode_label.grid(row=2, column=0, padx=(20, 5), pady=(5, 20), sticky="w")

        self.mode_var = tk.StringVar()
        self.mode_var.set("bit")

        bit_mode = ttk.Radiobutton(mainframe, text="Bit", variable=self.mode_var, value="bit")
        bit_mode.grid(row=2, column=1, padx=(5, 20), pady=(5, 20), sticky="w")

        byte_mode = ttk.Radiobutton(mainframe, text="Byte", variable=self.mode_var, value="byte")
        byte_mode.grid(row=2, column=1, padx=(5, 20), pady=(5, 20), sticky="e")

        convert_button = ttk.Button(mainframe, text="Convert", command=self.convert)
        convert_button.grid(row=3, column=1, pady=(5, 20))

    def browse_input(self):

        file_path = filedialog.askopenfilename()
        self.input_entry.delete(0, tk.END)
        self.input_entry.insert(0, file_path)

    def browse_output(self):

        file_path = filedialog.asksaveasfilename()
        self.output_entry.delete(0, tk.END)
        self.output_entry.insert(0, file_path)

    def convert(self):

        input_file = self.input_entry.get()
        output_file = self.output_entry.get()

        try:
            self.set_mode()  # Set the encoding mode
            self.process(input_file, output_file)
            self.status_label.config(text="Conversion complete")
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}")

    def set_mode(self):
        self.mode = self.mode_var.get()


if __name__ == "__main__":
    freq0 = 1000  # Frequency for binary '0'
    freq1 = 2000  # Frequency for binary '1'
    duration = 0.01  # Duration of each bit in seconds
    sample_rate = 44100  # Audio sample rate
    gui = AudioToBinaryGUI(freq0, freq1, duration, sample_rate)
    gui.mainloop()
