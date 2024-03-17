# mtv-pi
Emulate the golden days of MTV!

This Python script is meant to be run on a Raspberry Pi and does the following:
1. Selects a random MP4 video in the specified directory (`/home/pi/Videos` by default).
2. Selects a random start time before the 80% mark in the video and starts playing it.
3. Turns off after a specified amount of time.

It's recommended to use archived videos of MTV footage (which are hours long), but any videos can be used.

[![MTV Alarm Clock](http://img.youtube.com/vi/jBcRUBrIyRI/0.jpg)](https://www.youtube.com/watch?v=jBcRUBrIyRI "MTV Alarm Clock Demo")

## Usage

1. Install VLC 3.0 or higher (`sudo apt-get install vlc`).
2. Open the VLC GUI, choose Tools > Preferences > Video, and in the "Output" dropdown menu, select "DRM vout plugin". This will enable hardware acceleration for video, allowing it to use much less CPU.
3. Run the script with the command `python mtv.py` on a local session or VNC. It will not let you run it as root or via SSH.
4. (Optional) Depending on the resolution of the vidoes, Pi model, and other factors; you may need to do some tuning to free up enough resources.
    * Close all other open programs. Avoid using VNC while the video is playing.
    * Set your Pi resolution to match the source content. For instance, 640x480i.
      Interlaced resolutions will be easier to render, but you will need to test if your display will work with it.
    * Set the script to match the source content. For instance, 640x480.
    * Use the command `htop` and click the CPU tab to monitor how much CPU the process takes. You want to avoid maxing out the CPU (100%) as it can cause crashes. For reference, my Pi Zero W runs at 720x480i and videos rendered at 640x480, and hovers around 65% CPU usage.

## Usage - Alarm Clock

If you'd like to use MTV-Pi as an alarm clock, first run through the usage instructions above to make sure everything works properly.

1. Find a way to turn your TV on at the desired time. I use a portable CRT with the power switch always set to "On", which is plugged into a smart outlet that I can set a schedule for on my phone. For example, I have it turn on at 9am and off at 9:30am daily. Modern TVs often have a setting to turn on and off at certain times.
2. On the Pi, open a terminal and enter the command `crontab -e`. At the bottom of this file, add the line: `0 9 * * 0-6 DISPLAY=:0 python /home/pi/mtv.py`. This will set it to start the MTV script at 9am everyday and display it on the primary screen. 
3. Open mtv.py and set the `duration_to_play` variable. By default, it is set to 30 minutes.
