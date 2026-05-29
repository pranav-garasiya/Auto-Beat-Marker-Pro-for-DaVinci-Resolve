# 🎵 Auto Beat Marker Pro for DaVinci Resolve

### 📌 What does it do?
[cite_start]This is an advanced tool that automatically finds beats in your music or video files and applies color-coded markers on the DaVinci Resolve timeline[cite: 250]. [cite_start]The tool works smoothly in the background and places 5 different colors of markers once the process is complete[cite: 251].

### 🎯 What is it used for?
[cite_start]It is used for awesome "Beat Sync" video editing (cutting video according to the music beats)[cite: 252]. [cite_start]You can avoid the hassle of placing markers manually[cite: 253]. [cite_start]This tool automatically catches high peaks and drops, providing different color markers (Red, Yellow, Green, Cyan, Blue) based on the beat's strength[cite: 254].

### 📚 Which Libraries are used?
This tool uses 3 main Python libraries to work:
1. [cite_start]**`librosa`**: Used to detect beats and frequencies from the music[cite: 255].
2. [cite_start]**`numpy`**: A math/array processor required to perform beat calculations with librosa[cite: 256].
3. [cite_start]**`moviepy`**: If you place an `.mp4` or `.mov` video file on the timeline, this library is used to extract the audio automatically in the background[cite: 257].

## ⚙️ Prerequisites
You need the following two things to run this tool:
* [cite_start]**DaVinci Resolve Studio**: The Studio (Paid) version of DaVinci Resolve is required[cite: 258]. [cite_start](The Free version does not support external scripting [cite: 259]).
* [cite_start]**Python**: Python 3.10.11 must be installed on your PC[cite: 260].

## 🛠️ Installation Guide

### Step 1: Install Python
* [cite_start]Download and install Python 3.10.11 from python.org[cite: 261].
* [cite_start]⚠️ **IMPORTANT:** During installation, you MUST check the box that says **"Add Python 3.10 to PATH"** on the very first screen[cite: 262].

### Step 2: Install Libraries
* [cite_start]Open Command Prompt (CMD) on your computer[cite: 263].
* [cite_start]Type the following command and press Enter:
  ```bash
  pip install librosa numpy moviepy
