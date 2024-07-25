import os
import ffmpeg
from concurrent.futures import ProcessPoolExecutor

def split_segment(input_file, start_time, segment_length, output_file):
    """
    Splits a segment from the input file starting from start_time with the given length.

    Args:
        input_file (str): Path to the input MP3 file.
        start_time (int): The start time of the segment in seconds.
        segment_length (int): Length of each segment in seconds.
        output_file (str): Path to save the output segment.
    """
    ffmpeg.input(input_file, ss=start_time, t=segment_length).output(output_file).run()

def split_mp3(input_file, output_dir='.', segment_length=600, num_workers=6):
    """
    Splits an MP3 file into segments of a specified length using ffmpeg-python.

    Args:
        input_file (str): Path to the input MP3 file.
        output_dir (str): Directory to save the output segments (default is current directory).
        segment_length (int): Length of each segment in seconds (default is 600 seconds, i.e., 10 minutes).
        num_workers (int): Number of worker processes to use for parallel processing (default is 6).
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Get the duration of the input file in seconds
    probe = ffmpeg.probe(input_file)
    duration = float(probe['format']['duration'])

    # Split the file into segments
    num_segments = int(duration // segment_length) + 1
    tasks = []

    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        for i in range(num_segments):
            start_time = i * segment_length
            output_file = os.path.join(output_dir, f"segment_{i + 1}.mp3")
            tasks.append(executor.submit(split_segment, input_file, start_time, segment_length, output_file))

    # Optionally, you can wait for all tasks to complete
    for task in tasks:
        task.result()

if __name__ == "__main__":
    input_mp3 = "test.mp3"
    split_mp3(input_mp3, "./10_m")
    split_mp3(input_mp3, "./15_m")
    split_mp3(input_mp3, "./20_m")
    split_mp3(input_mp3, "./30_m")
    split_mp3(input_mp3, "./60_m")

