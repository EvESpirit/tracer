import tkinter as tk
from tkinter import filedialog
from a2b import AudioToBinary


class AudioToBinaryGUI(tk.Tk, AudioToBinary):
    """
    A graphical user interface for converting audio files to binary using AudioToBinary class.

    Attributes:
    freq0 (int): The frequency for binary '0'
    freq1 (int): The frequency for binary '1'
    duration (float): The duration of each bit
    sample_rate (int): The sampling rate of the audio file
    """

    def __init__(self, freq0, freq1, duration, sample_rate):
        """
        Initializes the AudioToBinaryGUI with the given parameters.

        Args:
        freq0 (int): The frequency for binary '0'
        freq1 (int): The frequency for binary '1'
        duration (float): The duration of each bit
        sample_rate (int): The sampling rate of the audio file
        """
        tk.Tk.__init__(self)
        AudioToBinary.__init__(self, freq0, freq1, duration, sample_rate)
        self.title("Audio to Binary Converter")
        self.build_gui()

    def build_gui(self):
        """
        Builds the graphical user interface for the audio to binary converter.
        """
        self.status_label = tk.Label(self, text="", fg="green")
        self.status_label.grid(row=3, column=1, pady=(5, 20))

        input_label = tk.Label(self, text="Input File:")
        input_label.grid(row=0, column=0, padx=(20, 5), pady=(20, 5), sticky="w")

        self.input_entry = tk.Entry(self, width=50)
        self.input_entry.grid(row=0, column=1, padx=(5, 20), pady=(20, 5))

        input_button = tk.Button(self, text="Browse", command=self.browse_input)
        input_button.grid(row=0, column=2, padx=(5, 20), pady=(20, 5))

        output_label = tk.Label(self, text="Output File:")
        output_label.grid(row=1, column=0, padx=(20, 5), pady=(5, 20), sticky="w")

        self.output_entry = tk.Entry(self, width=50)
        self.output_entry.grid(row=1, column=1, padx=(5, 20), pady=(5, 20))

        output_button = tk.Button(self, text="Browse", command=self.browse_output)
        output_button.grid(row=1, column=2, padx=(5, 20), pady=(5, 20))

        convert_button = tk.Button(self, text="Convert", command=self.convert)
        convert_button.grid(row=2, column=1, pady=(5, 20))

    def browse_input(self):
        """
        Opens a file dialog box to select the input audio file and displays the selected file path in the input entry.
        """
        file_path = filedialog.askopenfilename()
        self.input_entry.delete(0, tk.END)
        self.input_entry.insert(0, file_path)

    def browse_output(self):
        """
        Opens a file dialog box to select the output binary file and displays the selected file path in the output entry.
        """
        file_path = filedialog.asksaveasfilename()
        self.output_entry.delete(0, tk.END)
        self.output_entry.insert(0, file_path)

    def convert(self):
        """
        Converts the selected audio file to binary and saves the binary data to the selected output file.
        Displays appropriate status messages in the status label.
        """
        input_file = self.input_entry.get()
