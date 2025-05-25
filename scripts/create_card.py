import matplotlib.pyplot as plt
import numpy as np
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from transformers import BertTokenizer, BertModel
import torch

def generate_emotion_card(emotions, output="emotion_card.png"):
    if len(emotions) < 2:
        raise ValueError("At least 2 emotions required for analysis")
    
    
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained('bert-base-uncased')
    inputs = tokenizer(emotions, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
    embeddings = outputs.last_hidden_state[:, 0, :].numpy()
    
    
    perplexity = min(30, len(emotions)-1)
    tsne = TSNE(n_components=2, perplexity=perplexity, random_state=42)
    coords = tsne.fit_transform(embeddings)
    
    
    plt.figure(figsize=(8, 6))  
    ax = plt.gca()
    
    
    unique_emotions = list(set(emotions))
    colors = plt.cm.tab20(np.linspace(0, 1, len(unique_emotions)))
    emotion_colors = {em: colors[i] for i, em in enumerate(unique_emotions)}
    
    
    for i, (x, y) in enumerate(coords):
        plt.scatter(x, y, c=[emotion_colors[emotions[i]]], s=200,  
                   edgecolors='w', linewidth=1, alpha=0.9)
        plt.text(x, y+0.08, emotions[i],  
                fontsize=9, ha='center', va='bottom',  
                fontweight='bold', color='black')
    
    
    legend_elements = [plt.Line2D([0], [0], marker='o', color='w', 
                      markerfacecolor=emotion_colors[em], 
                      markersize=10, label=em)  
                   for em in unique_emotions]
    ax.legend(handles=legend_elements, loc='upper left', 
             bbox_to_anchor=(1, 1), fontsize=8)  
    
   
    plt.title("Emotion Map\n(t-SNE Projection)", fontsize=12, pad=12)  
    plt.axis('off')
    plt.grid(True, alpha=0.2)
    plt.tight_layout()
    plt.savefig(output, bbox_inches='tight', dpi=100) 
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
    
    plt.figure(figsize=(7, 7)) 
    ax = plt.gca()
    
    for i, (x, y) in enumerate(components):
        plt.scatter(x, y, s=120, c='#4B0082', alpha=0.7, edgecolors='w')  
        plt.text(x, y, emotions[i], 
                fontsize=8, 
                ha='center', va='center',
                bbox=dict(boxstyle='round', 
                        facecolor='w', 
                        alpha=0.8, 
                        edgecolor='#DDDDDD'))
    

    plt.title("Mental State Map\n(PCA Projection)", fontsize=12, pad=12)  
    plt.xlabel("Principal Component 1", fontsize=10, labelpad=8)  
    plt.ylabel("Principal Component 2", fontsize=10, labelpad=8)
    plt.grid(True, color='#EEEEEE')
    ax.set_facecolor('#FAFAFA')
    

    plt.text(0.5, -0.12, "*Axes represent principal components from PCA", 
            transform=ax.transAxes,
            ha='center', va='center', 
            fontsize=7, color='#666666')  
    
    plt.tight_layout()
    plt.savefig(output, dpi=100)  
    plt.close()

def create(emotions):    
    generate_emotion_card(emotions, "emotion_card.png")
    generate_mental_map(emotions, "mental_map.png")