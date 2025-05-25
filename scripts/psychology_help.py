from transformers import pipeline
from pydub import AudioSegment
import tempfile
import os

# Явное указание пути к FFmpeg (если нужно)
# AudioSegment.ffmpeg = "C:/ffmpeg/bin/ffmpeg.exe"

def transcribe_audio(audio_path: str) -> str:
    try:
        # Конвертация в WAV
        audio = AudioSegment.from_file(audio_path)
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
            wav_path = tmpfile.name
            audio.export(wav_path, format="wav", codec="pcm_s16le")  # Явное указание кодека

        # Транскрибация
        transcriber = pipeline(
            task="automatic-speech-recognition",
            model="facebook/wav2vec2-base-960h"
        )
        result = transcriber(wav_path)
        os.remove(wav_path)
        return result["text"]

    except Exception as e:
        if os.path.exists(wav_path):
            os.remove(wav_path)
        raise RuntimeError(f"Ошибка: {str(e)}")

def get_psychological_help(text):
    psychologist = pipeline(
        task="text-generation",
        model="microsoft/DialoGPT-medium",
        tokenizer="microsoft/DialoGPT-medium"
    )
    
    prompt = f"""Ты психолог. Ответь на русском.
    Пользователь: {text}
    Психолог:"""
    
    response = psychologist(
        prompt,
        max_new_tokens=500,
        do_sample=True,
        temperature=0.7,
        truncation=True,
        pad_token_id=psychologist.tokenizer.eos_token_id
    )
    
    return response[0]["generated_text"].split("Психолог:")[-1].strip()