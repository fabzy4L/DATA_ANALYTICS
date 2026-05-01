import subprocess
import os


##DOWNLOAD https://ffmpeg.org/download.html#build-windows

def extract_audio(video_path, audio_path):
    """
    Extracts audio from a video file and saves it as an audio file.
    
    :param video_path: Path to the video file.
    :param audio_path: Path to save the extracted audio file.
    """
    # Ensure the video file exists
    if not os.path.exists(video_path):
        print(f"Error: The video file '{video_path}' does not exist.")
        return
    
    try:
        # Run the ffmpeg command to extract audio
        command = [
            r"C:\Users\Fabian Alvarez-Primo\Downloads\ffmpeg\bin\ffmpeg",  # Path to ffmpeg executable
            "-i", video_path,  # Input video file
            "-vn",  # No video
            "-acodec", "libmp3lame",  # Audio codec for mp3
            "-ac", "2",  # Stereo audio
            "-ab", "192k",  # Audio bitrate
            "-ar", "44100",  # Audio sample rate
            audio_path  # Output audio file path
        ]
        
        # Run the command
        subprocess.run(command, check=True)
        print(f"Audio extracted and saved as {audio_path}")
        
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print(f"Could not extract audio from '{video_path}'.")

# Example usage
video_path = r"C:\Users\Fabian Alvarez-Primo\Downloads\MÁS DE TLATOANI STAND UP.mp4"  # Path to your video file
audio_path = "extracted_audio.mp3"  # Path where the audio will be saved

extract_audio(video_path, audio_path)
