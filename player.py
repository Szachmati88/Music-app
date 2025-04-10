import os
import random
from pygame import mixer

class MusicPlayer:
    def __init__(self, music_dir):
        mixer.init()
        self.music_dir = music_dir
        self.playlist = [f for f in os.listdir(music_dir) if f.endswith(".mp3")]
        self.current_index = 0
        self.loop = False
        self.shuffle = False
        self.paused = False

    def load_song(self):
        if not self.playlist:
            return ""
        path = os.path.join(self.music_dir, self.playlist[self.current_index])
        mixer.music.load(path)
        mixer.music.play()
        self.is_loaded = True
        self.paused = False
        return self.playlist[self.current_index]

    def play(self):
        if self.paused:
            mixer.music.unpause()
            self.paused = False
        elif not mixer.music.get_busy():
            return self.load_song()
        else:
            return ""

    def pause(self):
        if mixer.music.get_busy():
            mixer.music.pause()
            self.paused = True

    def stop(self):
        mixer.music.stop()

    def rewind(self):
        mixer.music.rewind()

    def next(self):
        self.paused = False
        if self.shuffle:
            self.current_index = random.randint(0, len(self.playlist) - 1)
        else:
            self.current_index = (self.current_index + 1) % len(self.playlist)
        return self.load_song()

    def previous(self):
        self.paused = False
        self.current_index = (self.current_index - 1) % len(self.playlist)
        return self.load_song()

    def set_volume(self, value):
        mixer.music.set_volume(value / 100)

    def get_position(self):
        return mixer.music.get_pos() // 1000

    def is_playing(self):
        return mixer.music.get_busy() and not self.paused

    def toggle_shuffle(self):
        self.shuffle = not self.shuffle

    def toggle_loop(self):
        self.loop = not self.loop
