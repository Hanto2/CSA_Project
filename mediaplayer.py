import pygame
from tkinter import *
import tkinter.ttk as ttk
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os




pygame.init()
pygame.mixer.init()
pygame.display.set_mode((1, 1))


class MediaPlayer:
    def __init__(self, window):
        self.window = window
        self.window.title("Simple Media Player")
        self.window.geometry("800x500")
        self.set_icon('Ahdesign91-Media-Player-Adobe-Media-Player.ico')
        ctk.set_appearance_mode("Light")   
        ctk.set_default_color_theme("blue") 

        forward_button_image = "forward50.png"
        backward_button_image = "back50.png"
        add_button_image = "pngtree-music-icon-tune-png-image_10541108.png"
        stop_button_image = "stop50.png"
        play_button_image = "play50.png"
        pause_button_image = "pause50.png"

        self.forward_image = ctk.CTkImage(Image.open(forward_button_image), size=(60,60))
        self.backward_image = ctk.CTkImage(Image.open(backward_button_image), size=(60,60))
        self.stop_image = ctk.CTkImage(Image.open(stop_button_image), size=(60,60))
        self.play_image = ctk.CTkImage(Image.open(play_button_image), size=(60,60))
        self.pause_image = ctk.CTkImage(Image.open(pause_button_image), size=(60,60))
        self.add_image = ctk.CTkImage(Image.open(add_button_image), size=(60,60))


        
        self.is_dragging = False
        self.is_playing = False
        self.current_file = None
        self.playlist = []
        self.current_index = -1 

        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        self.window.after(100, self.check_music_end)
        self.create_widgets()

    def set_icon(self, icon_path):
        try:
            self.window.iconbitmap(icon_path)
        except Exception as e:
            print(f"Error setting icon: {e}")

    def create_widgets(self):
        

        self.file_label = ctk.CTkLabel(self.window, text="No file loaded", wraplength=350)
        self.file_label.pack(pady=10) 

        self.main_frame = ctk.CTkFrame(self.window, fg_color="white")
        self.main_frame.pack(pady=20)

        self.playlist_box = Listbox(self.main_frame, bg="black", fg="light blue", width=60, selectbackground="light blue", selectforeground="black")
        self.playlist_box.grid(row=0, column=0, padx=(20, 10), pady=10, sticky="n")

        self.volume_frame = LabelFrame(self.main_frame, text="Volume")
        self.volume_frame.grid(row=0, column=1, pady=10, padx=(5, 20), sticky="n")
        
        self.volume_slider = ttk.Scale(self.volume_frame, from_=1, to=0, orient=VERTICAL, value=1, command=self.volume, length=125)
        self.volume_slider.pack(pady=10)

        self.mymenu = Menu(self.window)
        self.window.config(menu=self.mymenu)

        self.addsong = Menu(self.mymenu)
        self.mymenu.add_cascade(label="Add Songs", menu=self.addsong)
        self.addsong.add_command(label="Add music to the playlist", command=self.add_music)

        self.removesong = Menu(self.mymenu)
        self.mymenu.add_cascade(label="Remove music", menu=self.removesong)
        self.removesong.add_command(label="remove songs from the playlist", command=self.remove_music)

        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="white")
        self.button_frame.grid(row=1, column=0, pady=20, columnspan=2)

        self.play_button = ctk.CTkButton(self.button_frame, text="", fg_color="white",
                                        hover_color="white", corner_radius=30, width=60, height=60, image=self.play_image, command=self.play_song)
        self.play_button.grid(row=0, column=0, padx=15)

        self.pause_button = ctk.CTkButton(self.button_frame, image=self.pause_image, text="", fg_color="white",
                                        hover_color="white", corner_radius=30, width=60, height=60, command=self.pause_song)
        self.pause_button.grid(row=0, column=1, padx=15)

        self.stop_button = ctk.CTkButton(self.button_frame, text="", image=self.stop_image, fg_color="white",
                                        hover_color="white", corner_radius=30, width=60, height=60, command=self.stop_song)
        self.stop_button.grid(row=0, column=2, padx=15)

        self.backward_button = ctk.CTkButton(self.button_frame, image=self.backward_image, fg_color="white",
                                            hover_color="white", corner_radius=30, width=60, height=60, text="", command=self.backward)
        self.backward_button.grid(row=0, column=3, padx=15)

        self.forward_button = ctk.CTkButton(self.button_frame, image=self.forward_image, text="", fg_color="white",
                                            hover_color="white", corner_radius=30, width=60, height=60, command=self.forward)
        self.forward_button.grid(row=0, column=4, padx=15)

        self.position_bar = ctk.CTkSlider(self.main_frame, from_=0, to=100, command=self.positioning, number_of_steps=1000)
        self.position_bar.grid(row=2, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

        self.time_label = ctk.CTkLabel(self.main_frame, text="00:00 / 00:00")
        self.time_label.grid(row=3, column=0, columnspan=2, pady=5)

        self.window.bind("<space>", lambda e: self.pause_song())
        self.window.bind("<Right>", lambda e: self.forward())
        self.window.bind("<Left>", lambda e: self.backward())
        self.window.bind("<Return>", lambda e: self.play_song())


    def add_music(self):
        files = filedialog.askopenfilenames(
        title="Select Media File",
        filetypes=(("Audio Files", "*.mp3 *.wav *.ogg"), ("All Files", "*.*"))
        )
        for file in files:
            if file not in self.playlist:
                self.playlist.append(file)
                self.playlist_box.insert(END, file.split("/")[-1])

    def remove_music(self):
        selected = self.playlist_box.curselection()
        if not selected:
            self.file_label.configure(text='Please select a song to remove!')
            return
        selected_song = self.playlist[selected[0]]
        self.playlist.remove(selected_song)
        self.playlist_box.delete(selected[0])

        if selected_song == self.current_file:
            self.stop_song()
            self.file_label.configure(text='No file loaded!')
        
        if not self.playlist:
            self.current_index = -1
            self.file_label.configure(text="No file loaded")
        else:
            if self.current_index >= len(self.playlist):
                self.current_index = len(self.playlist) - 1
            self.current_file = self.playlist[self.current_index]
            self.file_label.configure(text=f"Playing: {os.path.basename(self.current_file)}")
 
    def play_song(self):
        selected = self.playlist_box.curselection()

        if not selected:
            self.file_label.configure(text="Please select a file to play!")
            return

        selected_file = self.playlist[selected[0]]
        self.current_file = selected_file
        self.file_label.configure(text=f"Playing: {os.path.basename(selected_file)}")
        
        pygame.mixer.music.load(selected_file)
        pygame.mixer.music.play(loops=0, start=int(self.position_bar.get()))

        self.total_length = self.time_length(selected_file)
        self.position_bar.configure(to=self.total_length)
        self.time_label.configure(text=f"00:00 / {self.time_format(self.total_length)}")
        self.position_bar.set(0)
        self.update_positionbar()

        self.is_playing = True
        self.is_paused = False

    def pause_song(self):
        if self.is_playing and not self.is_paused:
            pygame.mixer.music.pause()
            self.pause_button.configure(text="")
            self.is_paused = True
        elif self.is_paused:
            pygame.mixer.music.unpause()
            self.pause_button.configure(text="")
            self.is_paused = False

    def stop_song(self):
        pygame.mixer.music.stop()
        self.is_playing = False
        self.is_paused = False
        self.position_bar.set(0)
        self.time_label.configure(text="00:00 / 00:00")

    def forward(self):
        if not self.playlist:
            self.file_label.configure(text="Playlist is empty!")
            return
        self.current_index += 1
        if self.current_index >= len(self.playlist):
            self.current_index = 0
        
        self.current_file = self.playlist[self.current_index]
        self.file_label.configure(text=f"Playing: {os.path.basename(self.current_file)}")

        pygame.mixer.music.load(self.current_file)
        pygame.mixer.music.play()
        self.is_playing = True
        self.is_paused = False

    def backward(self):
        if not self.playlist:
            self.file_label.configure(text="Playlist is empty!")
            return
        self.current_index -= 1
        if self.current_index < 0:
            self.current_index = len(self.playlist) - 1
        
        self.current_file = self.playlist[self.current_index]
        self.file_label.configure(text=f"Playing: {os.path.basename(self.current_file)}")

        pygame.mixer.music.load(self.current_file)
        pygame.mixer.music.play()
        self.is_playing = True
        self.is_paused = False

    def play_next(self):
        if self.playlist:
            self.current_index = (self.current_index + 1) % len(self.playlist)
            self.current_file = self.playlist[self.current_index]
            self.file_label.configure(text=f"Playing: {os.path.basename(self.current_file)}")

            pygame.mixer.music.load(self.current_file)
            pygame.mixer.music.play()

            self.total_length = self.time_length(self.current_file)
            self.position_bar.configure(to=self.total_length)
            self.time_label.configure(text=f"00:00 / {self.time_format(self.total_length)}")
            self.position_bar.set(0)
            self.update_positionbar()
        
    def check_music_end(self):
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                self.play_next()
        
        if not self.playlist or self.current_index < 0 or self.current_index >= len(self.playlist):
            return

        self.window.after(100, self.check_music_end)

        self.is_playing = True
        self.is_paused = False

    def time_length(self, file):
        try:
            return int(pygame.mixer.Sound(file).get_length())
        except Exception as e:
            print(f"Error getting the length of the song: {e}")
            return 0

    def time_format(self, seconds):
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02}:{seconds:02}"

    def update_positionbar(self):
            if self.is_playing and not self.is_dragging:
                try:
                    current_playtime = pygame.mixer.music.get_pos() / 1000
                    if self.current_file:
                        self.position_bar.set(current_playtime)
                        self.time_label.configure(
                            text=f"{self.time_format(int(current_playtime))} / {self.time_format(self.total_length)}"
                            )
                        self.window.after(1000, self.update_positionbar)
                except Exception as e:
                    print(f"Error updating the position bar: {e}")

    def positioning(self, value):
        if self.is_playing:
            try:
                pygame.mixer.music.set_pos(float(value))
                self.position_bar.set(value)
                
            except Exception as e:
                print(f"Error seeking to position: {e}")

    def seek_position(self):
        if self.is_playing:
            pos = self.position_bar.get()
            pygame.mixer.music.get_pos(pos)

    def volume(self, value, event=None):
        volume_level = self.volume_slider.get()
        pygame.mixer.music.set_volume(volume_level)
        try:
            pygame.mixer.music.set_volume(float(value))
        except Exception as e:
            print(f"Error setting volume: {e}")

    def slider_dragging(self):
        self.position_bar.bind("<ButtonPress-1>", lambda e: self.start_dragging)
        self.position_bar.bind("<ButtonRelease-1>", lambda e: self.end_dragging)

    def start_dragging(self, event):
        self.is_dragging = True

    def end_dragging(self, event):
        self.is_dragging = False
        selected_position = self.position_bar.get()
        self.positioning(selected_position)
        self.window.after(1000, self.update_positionbar)



if __name__ == "__main__":
    window = ctk.CTk()
    player = MediaPlayer(window)
    window.mainloop()