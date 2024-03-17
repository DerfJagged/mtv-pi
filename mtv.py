import os
import random
import subprocess
import time

def select_random_video(directory):
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
    debug = True
    video_directory = "/home/pi/Videos"
    selected_video = select_random_video(video_directory)

    if selected_video:
        if debug:
            video_path = "/home/pi/Videos/test.mp4"
        else:
            video_path = os.path.join(video_directory, selected_video)

        # Get video duration using ffprobe
        ffprobe_command = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", video_path]
        duration = float(subprocess.check_output(ffprobe_command).decode("utf-8").strip())

        # Calculate a random start time before the 80% mark
        start_time = calculate_random_start_time(duration)

        print(f"Selected video: {selected_video}")
        print(f"Random start time: {start_time} seconds")

        # Play the video
        process = play_video(video_path, start_time)
        
        if debug:
            time.sleep(60*60)
        else:
            time.sleep(60*30) #30 minutes

        # Stop the video playback
        process.terminate()
        subprocess.run(["sudo", "killall", "vlc"])

if __name__ == "__main__":
    main()

