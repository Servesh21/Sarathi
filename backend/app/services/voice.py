import speech_recognition as sr
from gtts import gTTS
import os
import uuid
from pydub import AudioSegment

# Directory to save temporary audio files
UPLOAD_DIR = "app/static/audio"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def transcribe_audio(file_path: str) -> str:
    """Convert User Audio -> Text"""
    recognizer = sr.Recognizer()
    
    # 1. Convert audio to WAV (SpeechRecognition prefers WAV)
    # Android/iOS usually send .m4a or .mp4, so we convert it.
    audio = AudioSegment.from_file(file_path)
    wav_path = file_path + ".wav"
    audio.export(wav_path, format="wav")

    # 2. Transcribe
    with sr.AudioFile(wav_path) as source:
        audio_data = recognizer.record(source)
        try:
            # Using Google's free Speech API
            text = recognizer.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            return "API Error"
        finally:
            # Cleanup temp files
            if os.path.exists(wav_path):
                os.remove(wav_path)

async def text_to_speech(text: str) -> str:
    """Convert Agent Text -> Audio File URL"""
    try:
        # Generate unique filename
        filename = f"{uuid.uuid4()}.mp3"
        file_path = os.path.join(UPLOAD_DIR, filename)
        
        # Convert text to speech
        tts = gTTS(text=text, lang='en', slow=False)
        tts.save(file_path)
        
        # Return the relative path for the frontend to play
        return f"/static/audio/{filename}"
    except Exception as e:
        print(f"TTS Error: {e}")
        return ""