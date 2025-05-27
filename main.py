from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk
import soundfile as sf
from pydub import AudioSegment
import librosa
import tempfile
import os
import numpy as np

from scripts.voice_analys import predict_emotion as emotion
from scripts.create_card import create
from scripts.psychology_help import transcribe_audio, get_psychological_help
from scripts.help import show_help

class EmotionAnalyzerApp:
    def __init__(self, master):
        self.master = master
        master.title("Emotion Analyzer")
        self.bg_color = "#f0f0f0"
        self.btn_color = "#e1e1e1"
        master.configure(bg=self.bg_color)
        self.audio_path = ""
        self.emotion_window = None
        self.mental_window = None
        self.create_widgets()

    def create_widgets(self):
        self.load_btn = Button(
            self.master,
            text="Upload Audio",
            command=self.load_file,
            bg=self.btn_color,
            padx=10,
            pady=5
        )
        self.load_btn.pack(pady=10)
        
        
        self.analyze_btn = Button(
            self.master,
            text="Analyze",
            command=self.analyze_emotion,
            bg=self.btn_color,
            padx=10,
            pady=5,
            state=DISABLED
        )
        self.analyze_btn.pack(pady=5)
        
        
        self.result_container = Frame(self.master, bg=self.bg_color)
        self.result_container.pack(pady=10, fill=BOTH, expand=True)
        

        self.progress_frame = Frame(self.master, bg=self.bg_color)
        self.progress_frame.pack(pady=5, fill=X, padx=10)
        
        self.progress_label = Label(
            self.progress_frame,
            text="Progress: 0%",
            bg=self.bg_color,
            font=("Arial", 9)
        )
        self.progress_label.pack(side=LEFT)
        
        self.progress = ttk.Progressbar(
            self.progress_frame,
            orient=HORIZONTAL,
            length=200,
            mode='determinate'
        )
        self.progress.pack(side=LEFT, padx=5, expand=True, fill=X)

        self.help_btn = Button(
            self.progress_frame,
            text="Help",
            command=self.show_help,
            bg=self.btn_color,
            padx=10,
            pady=2
        )
        self.help_btn.pack(side=RIGHT)

    def show_help(self):  
        help_window = Toplevel(self.master)  
        help_window.title("Справка / Help")  
        notebook = ttk.Notebook(help_window)  
        notebook.pack(fill=BOTH, expand=True)  
        ru_frame = Frame(notebook, bg=self.bg_color)  
        self.populate_help(ru_frame, "ru")  
        notebook.add(ru_frame, text="Русский")  
        en_frame = Frame(notebook, bg=self.bg_color)  
        self.populate_help(en_frame, "en")  
        notebook.add(en_frame, text="English") 

    def populate_help(self, parent, lang):  
        content = show_help(lang)  
        Label(parent, text=content["title"], font=("Arial", 12, "bold"), bg=self.bg_color).pack(pady=10)  
        for section in content["sections"]:  
            frame = Frame(parent, bg=self.bg_color)  
            frame.pack(fill=X, padx=10, pady=5)  
            Label(frame, text=section["title"], font=("Arial", 10, "bold"), bg=self.bg_color, anchor="w").pack(fill=X)  
            Label(frame, text=section["content"], justify=LEFT, bg=self.bg_color, wraplength=400).pack(fill=X)  
        Label(parent, text=content["tips"], font=("Arial", 10), bg=self.bg_color, wraplength=400).pack(pady=10)  

    def load_file(self):
        filetypes = (("Audio files", "*.wav *.mp3 *.ogg"),)
        self.audio_path = filedialog.askopenfilename(filetypes=filetypes)
        if self.audio_path:
            self.analyze_btn.config(state=NORMAL)
            self.clear_results()

    def analyze_emotion(self):
        if not self.audio_path:
            return
        
        try:
            self.analyze_btn.config(state=DISABLED)
            self.clear_results()

            y, sr = librosa.load(self.audio_path, sr=None)
            text = transcribe_audio(self.audio_path)

            segment_length = 10 * sr  
            segments = [
                y[i:i+segment_length] 
                for i in range(0, len(y), segment_length) 
                if len(y[i:i+segment_length]) >= segment_length
            ]

            print(f"Create {len(segments)} segments")
            
            self.progress['maximum'] = len(segments)
            self.progress['value'] = 0
            self.progress_label.config(text="Progress: 0%")
            self.master.update_idletasks()
            
            emotions = []
            for i, segment in enumerate(segments):
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
                    tmp_path = tmpfile.name
                
                sf.write(tmp_path, segment, sr, subtype='PCM_16')
                emotion_result = emotion(tmp_path)
                os.unlink(tmp_path) 
                
                emotions.append(emotion_result)

                print(f"Segment {i + 1}: {emotion_result}")
                
                
                self.progress['value'] = i + 1
                percent = int((i+1)/len(segments)*100)
                self.progress_label.config(text=f"Progress: {percent}%")
                self.master.update_idletasks()

            # print(emotions)
            create(emotions)
            self.show_results()
            
            answer = get_psychological_help(text)
            self.show_psychologist_answer(text, answer)
            

        except Exception as e:
            self.show_error(f"Error: {str(e)}")
            print("Error", e)
        finally:
            self.analyze_btn.config(state=DISABLED)
            self.progress['value'] = 0
            self.progress_label.config(text="Progress: 0%")

    def show_results(self):
        
        if self.emotion_window:
            self.emotion_window.destroy()
        if self.mental_window:
            self.mental_window.destroy()

        try:
            
            self.emotion_window = Toplevel(self.master)
            self.emotion_window.title("Emotion Card")
            img = Image.open("cards/emotion_card.png")
            img = ImageTk.PhotoImage(img)
            Label(self.emotion_window, image=img).pack()
            self.emotion_window.image = img  
            self.center_window(self.emotion_window)

            
            self.mental_window = Toplevel(self.master)
            self.mental_window.title("Mental Map")
            img = Image.open("cards/mental_map.png")
            img = ImageTk.PhotoImage(img)
            Label(self.mental_window, image=img).pack()
            self.mental_window.image = img  
            self.center_window(self.mental_window)

            self.temporal_window = Toplevel(self.master)
            self.temporal_window.title("Temporal chart")
            img = Image.open("cards/temporal_chart.png")
            img = ImageTk.PhotoImage(img)
            Label(self.temporal_window, image=img).pack()
            self.temporal_window.image = img
            self.center_window(self.temporal_window)
            
            self.umap_window = Toplevel(self.master)
            self.umap_window.title("UMAP Projection")
            img = Image.open("cards/umap_map.png")
            img = ImageTk.PhotoImage(img)
            Label(self.umap_window, image=img).pack()
            self.umap_window.image = img
            self.center_window(self.umap_window)
            
            self.heatmap_window = Toplevel(self.master)
            self.heatmap_window.title("Heatmap")
            img = Image.open("cards/heatmap.png")
            img = ImageTk.PhotoImage(img)
            Label(self.heatmap_window, image=img).pack()
            self.heatmap_window.image = img
            self.center_window(self.heatmap_window)

        except Exception as e:
            self.show_error(f"Failed to load images: {str(e)}")

    def center_window(self, window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f'+{x}+{y}')

    def show_error(self, message):
        for widget in self.result_container.winfo_children():
            widget.destroy()
        Label(
            self.result_container,
            text=message,
            fg="red",
            bg=self.bg_color,
            wraplength=400
        ).pack()

    def clear_results(self):
        for widget in self.result_container.winfo_children():
            widget.destroy()
    
    def show_psychologist_answer(self, text, answer):
        for widget in self.result_container.winfo_children():
            widget.destroy()
        
        answer_frame = Frame(self.result_container, bg=self.bg_color)
        answer_frame.pack(pady=10, fill=BOTH, expand=True)
        
        Label(
            answer_frame,
            text="Распознанный текст:",
            font=("Arial", 10, "bold"),
            bg=self.bg_color
        ).pack(anchor="w")
        
        text_box = Text(
            answer_frame,
            wrap=WORD,
            height=4,
            width=50,
            font=("Arial", 9),
            bg="white"
        )
        text_box.insert(END, text)
        text_box.config(state=DISABLED)
        text_box.pack(fill=BOTH, pady=5)
        
        Label(
            answer_frame,
            text="Рекомендация психолога:",
            font=("Arial", 10, "bold"),
            bg=self.bg_color
        ).pack(anchor="w", pady=(10,0))
        
        answer_box = Text(
            answer_frame,
            wrap=WORD,
            height=6,
            width=50,
            font=("Arial", 9),
            bg="white"
        )
        answer_box.insert(END, answer)
        answer_box.config(state=DISABLED)
        answer_box.pack(fill=BOTH, expand=True)


if __name__ == "__main__":
    root = Tk()
    app = EmotionAnalyzerApp(root)
    root.geometry("500x500") 
    root.mainloop()