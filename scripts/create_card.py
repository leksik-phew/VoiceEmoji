import matplotlib.pyplot as plt
import numpy as np
from sklearn.manifold import TSNE
from umap import UMAP
from sklearn.decomposition import PCA
from transformers import BertTokenizer, BertModel
import torch
from matplotlib.colors import LinearSegmentedColormap
import os

def generate_emotion_card(emotions, output="cards/emotion_card.png"):
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

def generate_mental_map(emotions, output="cards/mental_map.png"):
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

def generate_temporal_emotion_chart(emotions, output="cards/temporal_chart.png"):
    time_points = np.arange(10, 10 * (len(emotions) + 1), 10)
    
    plt.figure(figsize=(10, 4))
    ax = plt.gca()
    
    unique_emotions = list(set(emotions))
    cmap = plt.get_cmap('tab20', len(unique_emotions))
    
    for i, em in enumerate(emotions):
        color = cmap(unique_emotions.index(em))
        plt.fill_betweenx(
            y=[i-0.4, i+0.4],
            x1=time_points[i]-10,
            x2=time_points[i],
            color=color,
            alpha=0.7
        )
    
    plt.title("The dynamics of emotions over time")
    plt.xlabel("Time (seconds)", fontsize=10)
    plt.yticks([])
    plt.xlim(0, max(time_points))
    plt.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    plt.savefig(output, dpi=100)
    plt.close()

def generate_umap_projection(emotions, output="cards/umap_map.png"):
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained('bert-base-uncased')
    inputs = tokenizer(emotions, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
    embeddings = outputs.last_hidden_state[:, 0, :].numpy()
    
    reducer = UMAP(n_components=2, random_state=42)
    coords = reducer.fit_transform(embeddings)
    
    plt.figure(figsize=(8, 6))
    unique_emotions = list(set(emotions))
    colors = plt.cm.tab20(np.linspace(0, 1, len(unique_emotions)))
    
    for i, (x, y) in enumerate(coords):
        plt.scatter(x, y, c=[colors[unique_emotions.index(emotions[i])]], s=100, edgecolor='w')
        plt.text(x, y+0.1, emotions[i], ha='center', fontsize=8)
    
    plt.title("UMAP Projection of Emotions")
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(output, dpi=100)
    plt.close()

def generate_heatmap(emotions, output="cards/heatmap.png"):
    unique_emotions, counts = np.unique(emotions, return_counts=True)
    intensity = counts / counts.sum()
    
    fig, ax = plt.subplots(figsize=(8, 2))
    cmap = LinearSegmentedColormap.from_list("emotion_cmap", ['#e0f3f8', '#0868ac'])
    
    bars = ax.barh(unique_emotions, intensity, color=cmap(intensity))
    
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 0.01, bar.get_y() + bar.get_height()/2,
                f'{width:.0%}', ha='left', va='center')
    
    plt.title("Intensity of emotions")
    plt.xlim(0, 1)
    plt.gca().invert_yaxis()
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(output, dpi=100, bbox_inches='tight')
    plt.close()


def create(emotions):    
    os.makedirs("cards", exist_ok=True)  
    generate_emotion_card(emotions, "cards/emotion_card.png")
    generate_mental_map(emotions, "cards/mental_map.png")
    generate_temporal_emotion_chart(emotions, "cards/temporal_chart.png")    
    generate_umap_projection(emotions, "cards/umap_map.png")          
    generate_heatmap(emotions, "cards/heatmap.png")
