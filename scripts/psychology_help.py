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
        model="microsoft/DialoGPT-medium"
    )
    
    prompt = f"""Person: {text} Psychologist:"""
    
    response = psychologist(
        prompt,
        max_length=200,
        pad_token_id=psychologist.tokenizer.eos_token_id
    )
    
    return response[0]["generated_text"].split("Psychologist:")[-1].strip()

get_psychological_help("i really love to suck some big black dicks")