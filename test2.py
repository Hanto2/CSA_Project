# import pygame
# import numpy as np
# from scipy.fftpack import fft

# # Initialize Pygame
# pygame.init()
# pygame.mixer.init()

# # Screen settings
# WIDTH, HEIGHT = 800, 400
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("Audio Visualizer")

# # Colors
# BACKGROUND_COLOR = (20, 20, 50)  # Dark blue
# BAR_COLOR = (0, 255, 255)       # Cyan

# # Audio settings
# MUSIC_FILE = "C:/Users/Hanto/OneDrive/Desktop/Assignment Stuff/Codes/downloads/Ricky Montgomery - Line Without a Hook (Official Lyric Video).mp3"
# pygame.mixer.music.load(MUSIC_FILE)
# pygame.mixer.music.play(-1)  # Play on loop

# # Visualization settings
# NUM_BARS = 50
# BAR_WIDTH = WIDTH // NUM_BARS

# def draw_visualizer(audio_data):
#     screen.fill(BACKGROUND_COLOR)

#     # Apply FFT to audio data to get frequencies
#     fft_values = np.abs(fft(audio_data))[:NUM_BARS]
#     max_height = max(fft_values) if max(fft_values) > 0 else 1
#     normalized_values = fft_values / max_height

#     for i, bar_height in enumerate(normalized_values):
#         bar_h = int(bar_height * HEIGHT)  # Scale bar height
#         x = i * BAR_WIDTH
#         pygame.draw.rect(screen, BAR_COLOR, (x, HEIGHT - bar_h, BAR_WIDTH - 2, bar_h))

#     pygame.display.flip()

# # Generate dummy audio data for testing (replace with real-time audio data)
# def generate_audio_data():
#     # Simulate a sine wave for testing
#     t = np.linspace(0, 1, 1024)
#     wave = 0.5 * (np.sin(2 * np.pi * 440 * t) + np.sin(2 * np.pi * 880 * t))
#     return wave

# # Main loop
# running = True
# clock = pygame.time.Clock()

# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     # Generate or fetch real-time audio data
#     audio_data = generate_audio_data()  # Replace with actual audio stream

#     # Draw the visualizer
#     draw_visualizer(audio_data)

#     clock.tick(30)  # Limit to 30 FPS

# pygame.quit()
import pygame
from tkinter import *
import tkinter.ttk as ttk
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Initialize pygame
pygame.init()
pygame.mixer.init()
pygame.display.set_mode((1, 1))

class MediaPlayer:
    def __init__(self, window):
        self.window = window
        self.window.title("Media Player with Visualizer")
        self.window.geometry("900x600")
        ctk.set_appearance_mode("Light")
        ctk.set_default_color_theme("blue")

        self.is_playing = False
        self.current_file = None
        self.playlist = []
        self.current_index = -1
        
        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        self.window.after(100, self.check_music_end)
        self.create_widgets()
        self.init_visualizer()

    def create_widgets(self):
        self.file_label = ctk.CTkLabel(self.window, text="No file loaded")
        self.file_label.pack(pady=10)
        
        self.playlist_box = Listbox(self.window, bg="black", fg="light blue", width=60)
        self.playlist_box.pack(pady=10)

        self.play_button = ctk.CTkButton(self.window, text="Play", command=self.play_song)
        self.play_button.pack(pady=5)

        self.stop_button = ctk.CTkButton(self.window, text="Stop", command=self.stop_song)
        self.stop_button.pack(pady=5)

        self.add_button = ctk.CTkButton(self.window, text="Add Music", command=self.add_music)
        self.add_button.pack(pady=5)

    def add_music(self):
        files = filedialog.askopenfilenames(
            title="Select Media File",
            filetypes=(("Audio Files", "*.mp3 *.wav *.ogg"), ("All Files", "*.*"))
        )
        for file in files:
            if file not in self.playlist:
                self.playlist.append(file)
                self.playlist_box.insert(END, os.path.basename(file))

    def play_song(self):
        selected = self.playlist_box.curselection()
        if not selected:
            self.file_label.configure(text="Please select a file to play!")
            return

        self.current_file = self.playlist[selected[0]]
        self.file_label.configure(text=f"Playing: {os.path.basename(self.current_file)}")
        pygame.mixer.music.load(self.current_file)
        pygame.mixer.music.play()

        self.is_playing = True
        self.start_visualizer()

    def stop_song(self):
        pygame.mixer.music.stop()
        self.is_playing = False
        self.stop_visualizer()

    def check_music_end(self):
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                self.stop_song()
        self.window.after(100, self.check_music_end)

    def init_visualizer(self):
        self.fig, self.ax = plt.subplots(figsize=(8, 3))
        self.ax.set_xlim(0, 100)
        self.ax.set_ylim(-1, 1)
        self.bar_plot = self.ax.bar(range(100), np.zeros(100), color="blue")
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.window)
        self.canvas.get_tk_widget().pack(pady=10)

    def start_visualizer(self):
        self.anim = FuncAnimation(self.fig, self.update_visualizer, interval=50)
        self.canvas.draw()

    def stop_visualizer(self):
        if hasattr(self, 'anim'):
            self.anim.event_source.stop()

    def update_visualizer(self, frame):
        if self.is_playing:
            try:
                # Simulate audio data (Replace with actual audio data if possible)
                audio_data = np.random.rand(100) - 0.5  # Replace this with actual audio sample data
                for bar, value in zip(self.bar_plot, audio_data):
                    bar.set_height(value)
                self.canvas.draw()
            except Exception as e:
                print(f"Visualizer error: {e}")

if __name__ == "__main__":
    root = ctk.CTk()
    app = MediaPlayer(root)
    root.mainloop()
