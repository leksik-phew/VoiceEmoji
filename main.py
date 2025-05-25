from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk
import soundfile as sf
import librosa
import tempfile
import os
import numpy as np

from scripts.voice_analys import predict_emotion as emotion
from scripts.create_card import create

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
        self.progress_frame.pack(pady=5, fill=X)
        
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
        self.progress.pack(side=LEFT, padx=5)

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
            
            y, sr = librosa.load(self.audio_path, sr=None)
            segment_length = 10 * sr  
            segments = [
                y[i:i+segment_length] 
                for i in range(0, len(y), segment_length) 
                if len(y[i:i+segment_length]) >= segment_length
            ]

            
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
                
                
                self.progress['value'] = i + 1
                percent = int((i+1)/len(segments)*100)
                self.progress_label.config(text=f"Progress: {percent}%")
                self.master.update_idletasks()

            
            create(emotions)
            self.show_results()

        except Exception as e:
            self.show_error(f"Error: {str(e)}")
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
            img = Image.open("emotion_card.png")
            img = ImageTk.PhotoImage(img)
            Label(self.emotion_window, image=img).pack()
            self.emotion_window.image = img  
            self.center_window(self.emotion_window)

            
            self.mental_window = Toplevel(self.master)
            self.mental_window.title("Mental Map")
            img = Image.open("mental_map.png")
            img = ImageTk.PhotoImage(img)
            Label(self.mental_window, image=img).pack()
            self.mental_window.image = img  
            self.center_window(self.mental_window)

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

if __name__ == "__main__":
    root = Tk()
    app = EmotionAnalyzerApp(root)
    root.geometry("500x250")
    root.mainloop()