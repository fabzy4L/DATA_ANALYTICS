import ffmpeg

def extract_audio(video_path, audio_path):
    ffmpeg.input(video_path).output(audio_path).run()
    print(f"Audio extracted and saved as {audio_path}")

# Specify the paths for video and audio
video_path = r"C:\Users\Fabian Alvarez-Primo\Downloads\MÁS DE TLATOANI STAND UP.mp4"  # Path to your video file
audio_path = "extracted_audio.wav"  # Path where audio will be saved

# Extract audio from video
extract_audio(video_path, audio_path)
