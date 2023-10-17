import sys
import speech_recognition as sr
from pydub import AudioSegment

def transcribe_audio(audio_data, recognizer):
    transcriptions = []
    total_length = len(audio_data)
    
    for i in range(0, total_length, 10000):
        progress = (i / total_length) * 100
        print(f"Progress: {progress:.2f}%")
        
        audio_chunk = audio_data[i:i+10000]
        
        with sr.AudioFile(audio_chunk.export("temp_chunk.wav", format="wav")) as source:
            audio_data_chunk = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data_chunk)
                transcriptions.append(text)
            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results; {e}")

    print("Progress: 100%")
    return " ".join(transcriptions)

if __name__ == "__main__":
    # Get audio file path from command line arguments
    if len(sys.argv) < 2:
        print("Usage: python script.py <audio_file_path>")
        sys.exit(1)

    audio_file_path = sys.argv[1]
    file_extension = audio_file_path.split(".")[-1]

    recognizer = sr.Recognizer()

    if file_extension == "mp3":
        audio_data = AudioSegment.from_mp3(audio_file_path)
    elif file_extension == "wav":
        audio_data = AudioSegment.from_wav(audio_file_path)
    else:
        print("Unsupported file format. Only mp3 and wav are supported.")
        sys.exit(1)

    # Generate output filename based on input filename
    output_text_file = f"{audio_file_path.split('.')[0]}_transcription.txt"

    # Perform transcription
    result = transcribe_audio(audio_data, recognizer)

    # Save the transcription to a text file
    with open(output_text_file, 'w') as f:
        f.write(result)
        
    print(f"Transcription saved to {output_text_file}")
