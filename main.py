import customtkinter as ctk
from tkinter import filedialog
import pygame
from pathlib import Path

pygame.mixer.init()

class MusicPlayer(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("SpotiPy Music Player")
        self.iconbitmap("logo.ico")
        self.geometry("600x700")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")
        
        # variables
        self.playlist = []
        self.current_index = 0
        self.is_paused = False
        
        self.create_ui()
        
    def create_ui(self):
        self.main_frame = ctk.CTkFrame(self, corner_radius=15)
        self.main_frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        self.title_label = ctk.CTkLabel(self.main_frame, text="SpotiPy", font=("Arial", 28, "bold"))
        self.title_label.pack(pady=(20, 10))
        
        self.song_label = ctk.CTkLabel(self.main_frame, text="No song selected", font=("Arial", 16), wraplength=500)
        self.song_label.pack(pady=10)
        
        # Controls
        self.controls_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.controls_frame.pack(pady=30)
        
        self.prev_btn = ctk.CTkButton(self.controls_frame, text="⏮", width=60, height=60, font=("Arial", 24), command=self.previous_song, corner_radius=30)
        self.prev_btn.pack(side="left", padx=10)
        
        self.play_btn = ctk.CTkButton(self.controls_frame, text="▶", width=80, height=80, font=("Arial", 30), command=self.play_pause, corner_radius=40)
        self.play_btn.pack(side="left", padx=10)
        
        self.next_btn = ctk.CTkButton(self.controls_frame, text="⏭", width=60, height=60, font=("Arial", 24), command=self.next_song, corner_radius=30)
        self.next_btn.pack(side="left", padx=10)
        
        # --- Volume ---
        self.volume_label = ctk.CTkLabel(self.main_frame, text="Volume", font=("Arial", 14))
        self.volume_label.pack(pady=(10, 0))

        self.volume_slider = ctk.CTkSlider(
            self.main_frame, 
            from_=0, 
            to=1, 
            width=400, 
            command=self.update_volume
        )
        self.volume_slider.pack(pady=5)
        self.volume_slider.set(0.7)

        self.volume_percent_label = ctk.CTkLabel(self.main_frame, text="70%", font=("Arial", 12))
        self.volume_percent_label.pack(pady=(0, 10))
        
        # Playlist
        self.playlist_frame = ctk.CTkScrollableFrame(self.main_frame, width=500, height=200)
        self.playlist_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        self.add_btn = ctk.CTkButton(self.main_frame, text="➕ Add Songs", command=self.add_songs)
        self.add_btn.pack(pady=10)

    def update_volume(self, value):
        """Updates the mixer volume and the text label percentage"""
        pygame.mixer.music.set_volume(value)
        percent = int(value * 100)
        self.volume_percent_label.configure(text=f"{percent}%")

    def add_songs(self):
        files = filedialog.askopenfilenames(filetypes=[("Audio Files", "*.mp3 *.wav *.ogg *.flac")])
        for file in files:
            if file not in self.playlist:
                self.playlist.append(file)
                ctk.CTkButton(self.playlist_frame, text=Path(file).stem, 
                            command=lambda f=file: self.play_selected(f), 
                            anchor="w", height=35).pack(pady=2, padx=5, fill="x")
    
    def play_selected(self, file):
        self.current_index = self.playlist.index(file)
        self.start_music()

    def play_pause(self):
        if not self.playlist: return
        
        if not pygame.mixer.music.get_busy() and not self.is_paused:
            self.start_music()
        elif self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False
            self.play_btn.configure(text="⏸")
        else:
            pygame.mixer.music.pause()
            self.is_paused = True
            self.play_btn.configure(text="▶")

    def start_music(self):
        pygame.mixer.music.load(self.playlist[self.current_index])
        pygame.mixer.music.play()
        self.song_label.configure(text=f"Now Playing: {Path(self.playlist[self.current_index]).stem}")
        self.play_btn.configure(text="⏸")
        self.is_paused = False
        self.check_playback()

    def next_song(self):
        if self.playlist:
            self.current_index = (self.current_index + 1) % len(self.playlist)
            self.start_music()

    def previous_song(self):
        if self.playlist:
            self.current_index = (self.current_index - 1) % len(self.playlist)
            self.start_music()

    def check_playback(self):
        if not pygame.mixer.music.get_busy() and not self.is_paused:
            self.next_song()
        else:
            self.after(1000, self.check_playback)

if __name__ == "__main__":
    app = MusicPlayer()
    app.mainloop()