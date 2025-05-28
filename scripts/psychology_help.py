from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from transformers import pipeline
from pydub import AudioSegment
import tempfile
import os


def transcribe_audio(audio_path: str, flag=False) -> str:
    if flag: return "Would be some text"
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

# model_name = "openchat/openchat-3.6-8b-20240522"
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = None

# # Инициализируем модель при первом вызове
# def init_model():
#     global model
#     if model is None:
#         model = AutoModelForCausalLM.from_pretrained(
#             model_name,
#             device_map="cpu",  # Автоматический выбор GPU/CPU
#             torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
#             low_cpu_mem_usage=True
#         ).eval()
#         print("Model loaded on device:", model.device)

# init_model()  # Предзагрузка модели

def get_psychological_help(text: str) -> str:
    return "Would be advice"
    try:
        # Форматирование промпта
        formatted_text = (
            "GPT4 Correct User: You are a professional psychologist. "
            f"Respond in English to this message:<|end_of_turn|>\n"
            f"Client: {text}<|end_of_turn|>\n"
            "GPT4 Correct Assistant:"
        )
        
        # Токенизация
        inputs = tokenizer(
            formatted_text,
            return_tensors="pt",
            max_length=1024,
            truncation=True
        ).to(model.device)

        # Генерация с оптимизированными параметрами
        with torch.no_grad():  # Отключаем вычисление градиентов
            outputs = model.generate(
                **inputs,
                max_new_tokens=200,  # Уменьшили длину ответа
                do_sample=True,
                temperature=0.7,     # Более детерминированные ответы
                top_k=50,
                top_p=0.9,
                repetition_penalty=1.1,
                num_return_sequences=1,
                pad_token_id=tokenizer.eos_token_id,
                eos_token_id=tokenizer.eos_token_id
            )
        
        # Декодирование ответа
        full_response = tokenizer.decode(
            outputs[0], 
            skip_special_tokens=True
        )

        return full_response.split("GPT4 Correct Assistant:")[-1].strip()

    except Exception as e:
        print(f"Error: {e}")
        return "Could not generate response. Please try again."

# text = transcribe_audio("temp.ogg", True)
# print(get_psychological_help(text))

# from ollama_api import OllamaClient

# client = OllamaClient()
# response = client.generate_completion(model="deepseek-r1:1.5b", prompt="Why is the sky blue?")
# print(response)