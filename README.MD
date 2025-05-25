# VoiceEmoji

A project for analyzing the emotional state based on audio recordings and generating psycho-emotional maps.  
**Supported formats**: MP3, OGG, WAV.

<img src="https://img.shields.io/badge/Python-3.8.10-blue" alt="Python Version"> <img alt="Hugging Face" src="https://img.shields.io/badge/Hugging-Face-yellow?style=plastic">

## Features
- Audio analysis using the * * Whisper-large-v3 * * model for emotion recognition.
- Visualization of results:
- * * Emotional map** (t-SNE) — shows the distribution of emotions in space.
  - **Mental Map** (PCA) — displays psychological characteristics.
- Intuitive graphical interface (GUI) based on Tkinter.

## How it works
1. Audio is divided into segments of 10 seconds each.
2. For each segment, an emotion is determined using a pre-trained model.
3. Based on the received emotions, we build:
- 2D visualization using t-SNE to group similar states.
   - PCA analysis for interpreting psychological patterns.

## Screenshots
| Emotional map | Mental Map |
|----------------------|--------------------|
| <img src="emotion_card.png" width="300"> | <img src="mental_map.png" width="300"> |


## Models used
[speech-emotion-recognition-with-openai-whisper-large-v3](https://huggingface.co/firdhokk/speech-emotion-recognition-with-openai-whisper-large-v3) — классификация эмоций.<br/>
[bert-base-uncased](https://huggingface.co/google-bert/bert-base-uncased) — vector representation of the text.

## Possible errors
- Error when processing audio: Make sure that the file is not corrupted and corresponds to the supported formats.
- Dependency issues on Windows: Install Microsoft Visual C++ Build Tools.

## Requirements
- Python 3.8.10
- Dependencies:  
```bash
  pip install -r requirements.txt
```

## Usage
```bash
git clone https://github.com/leksik-phew/VoiceEmoji.git
cd VoiceEmoji
pip install -r requirements.txt
python main.py
```

## Feedback: tg @bez_organov
