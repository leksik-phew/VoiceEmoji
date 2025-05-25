# VoiceEmoji

Проект для анализа эмоционального состояния по аудиозаписи и генерации психоэмоциональных карт.  
**Поддерживаемые форматы**: MP3, OGG, WAV.

<img src="https://img.shields.io/badge/Python-3.8.10-blue" alt="Python Version"> <img alt="Hugging Face" src="https://img.shields.io/badge/Hugging-Face-yellow?style=plastic">

## Особенности
- Анализ аудио с использованием модели **Whisper-large-v3** для распознавания эмоций.
- Визуализация результатов:
  - **Эмоциональная карта** (t-SNE) — показывает распределение эмоций в пространстве.
  - **Психическая карта** (PCA) — отображает психологические характеристики.
- Интуитивный графический интерфейс (GUI) на базе Tkinter.

## Как это работает
1. Аудио разбивается на сегменты по 10 секунд.
2. Для каждого сегмента определяется эмоция с помощью предобученной модели.
3. На основе полученных эмоций строятся:
   - 2D-визуализация с использованием t-SNE для группировки схожих состояний.
   - PCA-анализ для интерпретации психологических паттернов.

## Скриншоты
| Эмоциональная карта | Психическая карта |
|----------------------|--------------------|
| <img src="emotion_card.png" width="300"> | <img src="mental_map.png" width="300"> |


## Используемые модели
[speech-emotion-recognition-with-openai-whisper-large-v3](https://huggingface.co/firdhokk/speech-emotion-recognition-with-openai-whisper-large-v3) — классификация эмоций.<br/>
[bert-base-uncased](https://huggingface.co/google-bert/bert-base-uncased) — векторное представление текста.

## Возможные ошибки
- Ошибка при обработке аудио: Убедитесь, что файл не поврежден и соответствует поддерживаемым форматам.
- Проблемы с зависимостями на Windows: Установите Microsoft Visual C++ Build Tools.

## Требования
- Python 3.8.10
- Зависимости:  
```bash
  pip install -r requirements.txt
```

## Использование
```bash
git clone https://github.com/leksik-phew/VoiceEmoji.git
cd VoiceEmoji
pip install -r requirements.txt
python main.py
```

## Обратная связь: tg @bez_organov