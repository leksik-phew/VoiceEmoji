import matplotlib.pyplot as plt
import numpy as np
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from transformers import BertTokenizer, BertModel
import torch

def generate_emotion_card(emotions, output="emotion_card.png"):
    if len(emotions) < 2:
        raise ValueError("Для анализа нужно минимум 2 эмоции")
    
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained('bert-base-uncased')
    
    inputs = tokenizer(emotions, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
    embeddings = outputs.last_hidden_state[:, 0, :].numpy()
    
    perplexity = min(30, len(emotions)-1)
    tsne = TSNE(n_components=2, perplexity=perplexity, random_state=42)
    coords = tsne.fit_transform(embeddings)
    
    unique_emotions = list(set(emotions))
    color_map = plt.cm.get_cmap('rainbow', len(unique_emotions))
    emotion_colors = {em: color_map(i) for i, em in enumerate(unique_emotions)}
    
    plt.figure(figsize=(12, 8))
    for i, (x, y) in enumerate(coords):
        plt.scatter(x, y, c=[emotion_colors[emotions[i]]], s=200, edgecolors='black')
        plt.text(x, y, emotions[i], fontsize=10, ha='center', va='bottom')
        
        if i > 0:
            plt.plot([coords[i-1, 0]], [coords[i, 0]],
                     [coords[i-1, 1]], [coords[i, 1]],
                     'grey', linestyle='--', alpha=0.4)
    
    plt.title("Эмоциональная карта", fontsize=14)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(output)
    plt.close()

def generate_mental_map(emotions, output="mental_map.png"):
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained('bert-base-uncased')
    
    inputs = tokenizer(emotions, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
    embeddings = outputs.last_hidden_state[:, 0, :].numpy()
    
    pca = PCA(n_components=2)
    components = pca.fit_transform(embeddings)
    
    plt.figure(figsize=(10, 10))
    plt.scatter(components[:, 0], components[:, 1], c='purple', s=150, alpha=0.6)
    
    for i, (x, y) in enumerate(components):
        plt.text(x, y, emotions[i], fontsize=9, 
                ha='center', va='center', 
                bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))
    
    plt.xlabel("Интроверсия ↔ Экстраверсия", fontsize=12)
    plt.ylabel("Стабильность ↔ Невротизм", fontsize=12)
    plt.title("Психическая карта", fontsize=14)
    plt.grid(color='lightgray', linestyle='--')
    plt.savefig(output)
    plt.close()

def create(emotions):    
    generate_emotion_card(emotions, "emotion_card.png")
    generate_mental_map(emotions, "mental_map.png")