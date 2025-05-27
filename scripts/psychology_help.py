from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from transformers import pipeline
from pydub import AudioSegment
import tempfile
import os

def transcribe_audio(audio_path: str) -> str:
    return "Would be some text"
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

def get_psychological_help(text: str) -> str:
    return "Would be advice"
    try:
        print("Generating psychological advice...")
        
        # Используем многоязычную модель OpenChat
        model_name = "openchat/openchat-3.6-8b-20240522"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map="cpu",
            torch_dtype=torch.bfloat16
        )

        # Форматирование запроса согласно спецификации модели
        formatted_text = (
            "GPT4 Correct User: You are a professional psychologist. "
            f"Respond in English to this message:<|end_of_turn|>\n"
            f"Client: {text}<|end_of_turn|>\n"
            "GPT4 Correct Assistant:"
        )
        
        # Токенизация с учетом формата чата
        inputs = tokenizer(
            formatted_text,
            return_tensors="pt",
            max_length=2048,
            truncation=True
        ).to(model.device)

        # Генерация ответа с оптимизированными параметрами
        outputs = model.generate(
            **inputs,
            max_new_tokens=400,
            do_sample=True,
            temperature=0.8,
            top_p=0.95,
            repetition_penalty=1.15,
            num_return_sequences=1,
            pad_token_id=tokenizer.eos_token_id,
            eos_token_id=tokenizer.eos_token_id
        )
        
        # Декодирование и очистка ответа
        full_response = tokenizer.decode(
            outputs[0], 
            skip_special_tokens=True
        )
        
        # Извлекаем только ответ ассистента
        return full_response.split("GPT4 Correct Assistant:")[-1].strip()

    except Exception as e:
        print(f"Generation error: {e}")
        return "Could not generate response. Please rephrase your request."

# text = transcribe_audio("temp.ogg")
# print(get_psychological_help(text))