import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
from transformers import AutoProcessor, BarkModel
import scipy
from pydub import AudioSegment
import numpy as np
from datetime import datetime
import threading

processor = AutoProcessor.from_pretrained("suno/bark")
model = BarkModel.from_pretrained("suno/bark")
model.to("cuda")

def generate_audio(text, history_prompt, output):
    inputs = processor(text, voice_preset=history_prompt)
    for k, v in inputs.items():
        inputs[k] = v.to("cuda")
    audio_array = model.generate(**inputs)
    audio_array = audio_array.cpu().numpy().squeeze()
    sample_rate = model.generation_config.sample_rate
    scipy.io.wavfile.write(output, rate=sample_rate, data=audio_array)

def split_text(text):
    segments = text.rstrip('.').split('.')
    return segments

def browse_output_directory():
    directory = filedialog.askdirectory()
    output_dir.set(directory)

def start_process():
    text = text_input.get("1.0", ctk.END).strip()
    history_prompt = speaker_var.get()
    output_path = output_dir.get()

    if not text:
        messagebox.showerror("Error", "Please enter text to process.")
        return

    if not output_path:
        messagebox.showerror("Error", "Please select an output directory.")
        return

    show_progress_bar()

    threading.Thread(target=process_text, args=(text, history_prompt, output_path)).start()

def process_text(text, history_prompt, output_path):
    segments = split_text(text)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    output_segment_path = os.path.join(output_path, "segments")
    os.makedirs(output_segment_path, exist_ok=True)
    combined_audio = AudioSegment.empty()

    for i, segment in enumerate(segments):
        generate_audio(
            text="[reading quickly] " + segment.rstrip('.') + "...",
            history_prompt=history_prompt,
            output=f"{output_segment_path}/story{i+1}.wav"
        )

    wav_files = [file for file in os.listdir(output_segment_path) if file.endswith(".wav")]
    wav_files.sort()
    for wav_file in wav_files:
        audio_segment = AudioSegment.from_file(os.path.join(output_segment_path, wav_file))
        combined_audio += audio_segment

    output_file_path = os.path.join(output_path, f"merged_audio_{timestamp}.wav")
    combined_audio.export(output_file_path, format="wav")

    hide_progress_bar()

    messagebox.showinfo("Success", f"Audio files generated and merged successfully.\nSaved to: {output_file_path}")

def show_progress_bar():
    progress_bar.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="we")
    progress_bar.start()

def hide_progress_bar():
    progress_bar.stop()
    progress_bar.set(0)
    progress_bar.grid_remove()

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
root.title("Bark TTS")
root.geometry("700x400")

text_label = ctk.CTkLabel(root, text="Enter Text:", font=("Lexend", 12, "bold"))
text_label.grid(row=0, column=0, padx=10, pady=10, sticky="nw")
text_input = ctk.CTkTextbox(root, height=50)
text_input.grid(row=1, column=0, rowspan = 4, padx=10, pady=0, sticky="nswe")

speaker_label = ctk.CTkLabel(root, text="Select Speaker Voice Preset:", font=("Lexend", 12, "bold"))
speaker_label.grid(row=0, column=1, padx=10, pady=10, sticky="nw")

speaker_var = ctk.StringVar(root)
speaker_var.set("v2/en_speaker_0")
speaker_menu = ctk.CTkOptionMenu(root, variable=speaker_var, width=200, height=30,
                             values=[
                                 "v2/en_speaker_0",
                                 "v2/en_speaker_1",
                                 "v2/en_speaker_2",
                                 "v2/en_speaker_3",
                                 "v2/en_speaker_4",
                                 "v2/en_speaker_5",
                                 "v2/en_speaker_6",
                                 "v2/en_speaker_7",
                                 "v2/en_speaker_8",
                                 "v2/en_speaker_9"
                             ])
speaker_menu.grid(row=1, column=1, padx=10, pady=0, sticky="nwe")

output_label = ctk.CTkLabel(root, text="Select Output Directory:", font=("Lexend", 12, "bold"))
output_label.grid(row=2, column=1, padx=10, pady=10, sticky="nw")

output_dir = ctk.StringVar()

output_entry = ctk.CTkEntry(root, textvariable=output_dir, width=200, height=30)
output_entry.grid(row=3, column=1, padx=10, pady=0, sticky="nwe")

browse_button = ctk.CTkButton(root, text="Browse", width=200, height=30, command=browse_output_directory)
browse_button.grid(row=4, column=1, padx=10, pady=10, sticky="nwe")

progress_bar = ctk.CTkProgressBar(root, orientation="horizontal", mode="indeterminate")

start_button = ctk.CTkButton(root, text="Start", command=start_process)
start_button.grid(row=6, column=0, columnspan=2, padx=200, pady=10, sticky="we")

root.grid_columnconfigure(0, weight=6)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_rowconfigure(4, weight=1)
root.grid_rowconfigure(5, weight=1)
root.grid_rowconfigure(6, weight=1)

root.mainloop()
