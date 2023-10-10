import os

import ez
import ymd

import tkinter as tk
from tkinter import filedialog

class GUI:
    def __init__(self, master):
        # Initialize the GUI
        self.master = master
        master.title("YKWPPModelConverter")

        # GroupBox "Files/Folders"
        self.groupBoxFiles = tk.LabelFrame(master, text="Files/Folders")
        self.groupBoxFiles.grid(row=0, column=0, padx=10, pady=10, rowspan=2, sticky="nsew")

        # Listbox
        self.listBoxFiles = tk.Listbox(self.groupBoxFiles, selectmode=tk.MULTIPLE)
        self.listBoxFiles.pack(expand=True, fill="both")

        # Add and Remove buttons
        self.btnAdd = tk.Button(master, text="Add", command=self.add_files)
        self.btnAdd.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        self.btnRemove = tk.Button(master, text="Remove", command=self.remove_files)
        self.btnRemove.grid(row=2, column=0, padx=10, pady=5, sticky="e")

        # GroupBox "Log"
        self.groupBoxLog = tk.LabelFrame(master, text="Log")
        self.groupBoxLog.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Log Textbox
        self.logTextbox = tk.Text(self.groupBoxLog, state="disabled", height=10, width=40)
        self.logTextbox.pack(expand=True, fill="both")

        # GroupBox "Output Folder"
        self.groupBoxOutput = tk.LabelFrame(master, text="Output Folder")
        self.groupBoxOutput.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        # Output Folder Textbox
        self.outputTextbox = tk.Entry(self.groupBoxOutput, state="readonly", width=30)
        self.outputTextbox.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # Open Folder Button
        self.btnOpenFolder = tk.Button(self.groupBoxOutput, text="Open", command=self.open_folder)
        self.btnOpenFolder.grid(row=0, column=1, padx=5, pady=5, sticky="e")

        # Convert Button
        self.btnConvert = tk.Button(master, text="Convert", command=self.convert, state="disabled")
        self.btnConvert.grid(row=3, column=1, pady=10, sticky="e")

    def add_files(self):
        # Add files to the listbox
        files = filedialog.askopenfilenames()
        for file in files:
            self.listBoxFiles.insert(tk.END, file)
        self.log("Added {} file(s)".format(len(files)))
        self.update_convert_button_state()

    def remove_files(self):
        # Remove selected files from the listbox
        selected_indices = self.listBoxFiles.curselection()
        for index in reversed(selected_indices):
            self.listBoxFiles.delete(index)
        self.log("Removed {} file(s)".format(len(selected_indices)))
        self.update_convert_button_state()

    def open_folder(self):
        # Open a folder and set it as the output folder
        folder = filedialog.askdirectory()
        self.outputTextbox.config(state="normal")
        self.outputTextbox.delete(0, tk.END)
        self.outputTextbox.insert(0, folder)
        self.outputTextbox.config(state="readonly")
        self.log("Selected output folder: {}".format(folder))
        self.update_convert_button_state()

    def convert(self):
        # Convert selected files
        output_folder = self.outputTextbox.get()
        if not output_folder:
            self.log("Error: Output folder not selected.")
            return

        selected_files = self.listBoxFiles.get(0, tk.END)
        for file in selected_files:
            _, extension = os.path.splitext(file)
            if extension == ".ez":
                self.log("Processing .ez file: {}".format(file))
                ez.ToZip(file, output_folder)
                
                filename = os.path.splitext(os.path.basename(file))[0]
                
                new_output_folder = output_folder + '/' + filename
                new_input_file = new_output_folder + '/' + filename + '.ymd'
                
                if ymd.to_obj(new_input_file, new_output_folder):
                    self.log("Conversion of {} to obj succeeded".format(file))
                else:
                    self.log("Can't convert {} to obj".format(file))
            elif extension == ".ymd":
                self.log("Processing .ymd file: {}".format(file))
                if ymd.to_obj(file, output_folder):
                    self.log("Conversion of {} to obj succeeded".format(file))
                else:
                    self.log("Can't convert {} to obj".format(file))
            else:
                self.log("Unsupported file extension: {}".format(file))

        self.log("Conversion completed")

    def update_convert_button_state(self):
        # Update the state of the Convert button based on the selected files and output folder
        output_folder = self.outputTextbox.get()
        files_selected = self.listBoxFiles.size() > 0
        convert_button_state = tk.NORMAL if output_folder and files_selected else tk.DISABLED
        self.btnConvert.config(state=convert_button_state)

    def log(self, message):
        # Log a message to the log textbox
        self.logTextbox.config(state="normal")
        self.logTextbox.insert(tk.END, message + "\n")
        self.logTextbox.config(state="disabled")

if __name__ == "__main__":
    # Run the GUI
    root = tk.Tk()
    gui = GUI(root)
    root.mainloop()
