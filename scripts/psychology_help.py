from transformers import pipeline

def transcribe_audio(audio_path):
    transcriber = pipeline(
        task="automatic-speech-recognition",
        model="facebook/wav2vec2-base-960h"
    )
    result = transcriber(audio_path)
    return result["text"]

def get_psychological_help(text):
    psychologist = pipeline(
        task="text-generation",
        model="microsoft/DialoGPT-medium",
        tokenizer="microsoft/DialoGPT-medium"
    )
    
    prompt = f"""Ты профессиональный психолог. Ответь на русском языке. 
    Пользователь: {text}
    Психолог:"""
    
    response = psychologist(
        prompt,
        max_length=300,
        min_length=50,
        temperature=0.7,  # Контроль креативности
        top_p=0.9,
        repetition_penalty=1.2,
        truncation=True,
        num_return_sequences=1,
        pad_token_id=psychologist.tokenizer.eos_token_id
    )
    
    full_response = response[0]["generated_text"]
    psychologist_part = full_response.split("Психолог:")[-1].strip()
    
    # Фильтрация нежелательных фраз
    unwanted_phrases = ["I'm not a psychologist", "I'm an AI assistant"]
    for phrase in unwanted_phrases:
        psychologist_part = psychologist_part.replace(phrase, "")
    
    return psychologist_part

print(get_psychological_help("i really love to suck some big black dicks"))