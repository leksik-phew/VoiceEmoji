from transformers import pipeline
from pydub import AudioSegment
import numpy as np
import tempfile
import os

def transcribe_audio(audio_path: str) -> str:
    try:
        # Конвертация в WAV через pydub
        audio = AudioSegment.from_file(audio_path)
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
            wav_path = tmpfile.name
            audio.export(wav_path, format="wav")

        transcriber = pipeline(
            task="automatic-speech-recognition",
            model="facebook/wav2vec2-base-960h"
        )

        result = transcriber(wav_path)
        os.unlink(wav_path)

        return result["text"]

    except Exception as e:
        raise RuntimeError(f"Ошибка транскрибации: {str(e)}")

def get_psychological_help(text):
    psychologist = pipeline(
        task="text-generation",
        model="microsoft/DialoGPT-medium",
        tokenizer="microsoft/DialoGPT-medium"
    )
    
    prompt = f"""Ты профессиональный психолог. Ответь на английском языке. 
    Пользователь: {text}
    Психолог:"""

    response = psychologist(
        prompt,
        max_length=300,
        min_length=50,
        do_sample=True,
        temperature=0.5,  # Контроль креативности
        top_p=0.9,
        repetition_penalty=1.2,
        truncation=True,
        num_return_sequences=1,
        pad_token_id=psychologist.tokenizer.eos_token_id
    )
    
    full_response = response[0]["generated_text"]
    psychologist_part = full_response.split("Психолог:")[-1].strip()
    
    
    return psychologist_part

print(get_psychological_help("i really love to suck some big black dicks"))