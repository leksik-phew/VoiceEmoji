from transformers import pipeline
from pydub import AudioSegment
import tempfile
import os

def transcribe_audio(audio_path: str) -> str:
    try:
        print("Transcribing audio: ")

        audio = AudioSegment.from_file(audio_path)
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
            wav_path = tmpfile.name
            audio.export(wav_path, format="wav", codec="pcm_s16le")

        print("Convertation: SUCCESS")

        transcriber = pipeline(
            task="automatic-speech-recognition",
            model="openai/whisper-medium",
            generate_kwargs={"return_timestamps": True}  
        )

        print("Model initialization: SUCCESS")

        result = transcriber(wav_path)
        os.remove(wav_path)

        print("Getting result: SUCCESS")

        return result["text"]

    except Exception as e:
        if os.path.exists(wav_path):
            os.remove(wav_path)
        raise RuntimeError(f"Transcribing error: {str(e)}")

def get_psychological_help(text):
    try: 
        print("Get psychological help: ")

        psychologist = pipeline(
            task="text-generation",
            model="microsoft/DialoGPT-medium",
            tokenizer="microsoft/DialoGPT-medium"
        )

        print("Model initialization: SUCCESS")
        
        prompt = f"""Ты психолог. Ответь на русском.
        Пользователь: {text}
        Психолог:"""
        
        response = psychologist(
            prompt,
            max_new_tokens=8000,
            do_sample=True,
            temperature=0.7,
            truncation=True,
            pad_token_id=psychologist.tokenizer.eos_token_id
        )

        print("Getting response: SUCCESS")
        
        return response[0]["generated_text"]
    #.split("Психолог:")[-1].strip()
    except Exception as e:
        print(f"Get psychological help error: {e}")

# text = transcribe_audio("temp.ogg")
# print(get_psychological_help(text))