from faster_whisper import WhisperModel
import multiprocessing
import concurrent.futures
import subprocess
import os

model_size = "tiny.en"
max_processes = 30
path = ""

def transcribe(audio_file, model):
# Run on GPU with FP16
    segments, _ = model.transcribe(audio_file)
    data = " ".join([segment.text for segment in segments])
    #write to textfile

    with open(audio_file.replace(".mp3", "") + ".txt", "w", encoding="utf-8") as txt:
        txt.write(data)

def transcribe_audio(model, max_processes = 0):
    if max_processes > multiprocessing.cpu_count() or max_processes == 0:
        max_processes = multiprocessing.cpu_count()

    mp3s = [f for f in os.listdir('.') if os.path.isfile(f)]
    print(mp3s)
    # Submit each file to the thread pool and store the corresponding future object
    with concurrent.futures.ThreadPoolExecutor(max_processes) as executor:
        for file_path in mp3s:
            executor.submit(transcribe, file_path, model)

if __name__ == "__main__":
    # load model
    model = WhisperModel(model_size, device="cuda", compute_type="float16")
    transcribe_audio(model, max_processes = max_processes)