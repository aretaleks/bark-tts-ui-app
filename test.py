from transformers import AutoProcessor, BarkModel
import scipy
from pydub import AudioSegment
import numpy as np
import os
from datetime import datetime

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


input_folder = "C:\\Users\\areta\\workspace\\TTS\\"
wav_files = []
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

def main():
    text = "Sample text here."
    segments = split_text(text)
    separator = os.path.sep
    output_segment_path = os.path.join("segments")
    combined_audio = AudioSegment.empty()
    for i, segment in enumerate(segments):
        generate_audio(
            text="[reading quickly] "+segment.rstrip('.')+"...",
            history_prompt="v2/en_speaker_5",
            output=f"{output_segment_path}/story{i+1}.wav"
        )
    wav_files = [file for file in os.listdir(input_folder+"segments") if file.endswith(".wav")]   
    wav_files.sort()
    print("List of WAV files found:", wav_files)
    for wav_file in wav_files:
        audio_segment = AudioSegment.from_file(output_segment_path + separator + wav_file)
        combined_audio += audio_segment
    output_file_path = os.path.join("merged", f"merged_audio_{timestamp}.wav")
    combined_audio.export(output_file_path, format="wav")


main()
