import os
import random
import subprocess
import time

video_directory = "/home/pi/Videos"
duration_to_play = 60 # minutes

debug = True
debug_video_path = "/home/pi/Videos/test.mp4"

#############################################

def select_random_video(directory):
    # Select a video from the specified directory
    video_files = [file for file in os.listdir(directory) if file.endswith(".mp4")]
    if not video_files:
        print("No .mp4 files found in the specified directory.")
        return None
    return random.choice(video_files)

def calculate_random_start_time(duration):
    # Choose a random time before the 80% mark
    return random.uniform(0, 0.8 * duration)

def play_video(video_path, start_time):
    command = [
        "cvlc",
        "--no-video-title-show",
        "--no-osd",
        "--fullscreen",
        "--video-on-top",
        #"--height=480",
        "--width=640",
        "--aspect-ratio=3:2",
        "--deinterlace=0",
        "--start-time=" + str(start_time),
        video_path,
    ]
    process = subprocess.Popen(command)
    return process

def main():
    if debug:
        selected_video = debug_video_path.split('/')[-1]
        video_path = debug_video_path
    else:
        selected_video = select_random_video(video_directory)
        if not selected_video:
            return
        video_path = os.path.join(video_directory, selected_video)

    # Get video duration using ffprobe
    ffprobe_command = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", video_path]
    duration = float(subprocess.check_output(ffprobe_command).decode("utf-8").strip())

    # Calculate a random start time before the 80% mark
    start_time = calculate_random_start_time(duration)

    print(f"Selected video: {selected_video}")

    if debug:
        print(f"Starting from beginning of video")
        process = play_video(video_path, 0)
        time.sleep(60*5) #5 minutes
    else:
        print(f"Random start time: {start_time} seconds")
        process = play_video(video_path, start_time)
        time.sleep(60 * duration_to_play)

    # Stop the video playback
    process.terminate()
    subprocess.run(["sudo", "killall", "vlc"])
    subprocess.Popen('kill $(ps aux | grep mtv.py | grep -v grep | awk \'{ print $2 }\')', shell=True)

if __name__ == "__main__":
    main()
