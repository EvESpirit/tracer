import tkinter as tk
from tkinter import filedialog
from a2b import AudioToBinary


class AudioToBinaryGUI(tk.Tk, AudioToBinary):
    def __init__(self, freq0, freq1, duration, sample_rate):
        tk.Tk.__init__(self)
        AudioToBinary.__init__(self, freq0, freq1, duration, sample_rate)
        self.title("Audio to Binary Converter")
        self.build_gui()

    def build_gui(self):

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

        if not input_file:
            self.status_label.config(text="Error: Please select an input file.", fg="red")
            return

        if not output_file:
            self.status_label.config(text="Error: Please select an output file.", fg="red")
            return

        try:
            self.process(input_file, output_file)
            self.status_label.config(text="Finished", fg="green")
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}", fg="red")
            return


if __name__ == '__main__':
    freq0 = 1000
    freq1 = 2000
    duration = 0.01
    sample_rate = 44100

    app = AudioToBinaryGUI(freq0, freq1, duration, sample_rate)
    app.mainloop()
