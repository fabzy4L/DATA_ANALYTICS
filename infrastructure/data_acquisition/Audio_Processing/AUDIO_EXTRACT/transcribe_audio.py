import requests
import time
import os

def transcribe_audio_assemblyai(audio_path, api_key):
    # Verify if the file exists before uploading
    if not os.path.isfile(audio_path):
        print(f"File not found: {audio_path}")
        return

    # Upload the audio file to AssemblyAI
    upload_url = "https://api.assemblyai.com/v2/upload"
    headers = {"authorization": api_key}

    with open(audio_path, 'rb') as f:
        response = requests.post(upload_url, headers=headers, files={'file': f})

    if response.status_code != 200:
        print("Failed to upload audio file:", response.json())
        return

    audio_url = response.json()['upload_url']
    print("Audio file uploaded successfully, audio_url:", audio_url)

    # Request transcription
    transcription_url = "https://api.assemblyai.com/v2/transcript"
    json_data = {'audio_url': audio_url}
    transcription_response = requests.post(transcription_url, json=json_data, headers=headers)

    if transcription_response.status_code != 200:
        print("Failed to request transcription:", transcription_response.json())
        return

    transcript_id = transcription_response.json()['id']
    print("Transcription job started successfully, transcript_id:", transcript_id)

    # Wait for transcription to complete
    while True:
        response = requests.get(f"https://api.assemblyai.com/v2/transcript/{transcript_id}", headers=headers)
        status = response.json()['status']

        if status == 'completed':
            print("Transcription completed: ")
            print(response.json()['text'])
            break
        elif status == 'failed':
            print("Transcription failed.")
            break

        time.sleep(5)  # Wait for 5 seconds before checking again

# Call the function with the audio file path and API key
audio_file_path = r"C:\Users\Fabian Alvarez-Primo\TLATOANI.mp3" # Correct path to your audio file
api_key = "c0ec01cedcec4fb794d536a24111336a"  # Your AssemblyAI API key
transcribe_audio_assemblyai(audio_file_path, api_key)