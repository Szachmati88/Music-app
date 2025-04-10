from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QSlider
)
from PyQt6.QtCore import Qt, QTimer
from player import MusicPlayer

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Muzyczny Winamp")
        self.setFixedSize(400, 200)

        self.player = MusicPlayer("music")

        self.init_ui()
        self.init_timer()

    def init_ui(self):
        self.song_label = QLabel("SONG: ")
        self.time_label = QLabel("00:00")
        self.bitrate_label = QLabel("BITRATE: 128 kbps")
        self.mixrate_label = QLabel("MIXRATE: 44 kHz")

        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setValue(50)
        self.volume_slider.valueChanged.connect(self.player.set_volume)

        # Buttons
        self.play_btn = QPushButton("▶")
        self.pause_btn = QPushButton("⏸")
        self.next_btn = QPushButton("⏭")
        self.prev_btn = QPushButton("⏮")
        self.restart_btn = QPushButton("⟲")
        self.shuffle_btn = QPushButton("Shuffle")
        self.loop_btn = QPushButton("Loop")

        self.play_btn.clicked.connect(self.play_song)
        self.pause_btn.clicked.connect(self.pause_song)
        self.next_btn.clicked.connect(self.next_song)
        self.prev_btn.clicked.connect(self.prev_song)
        self.restart_btn.clicked.connect(self.restart_song)
        self.shuffle_btn.clicked.connect(self.toggle_shuffle)
        self.loop_btn.clicked.connect(self.toggle_loop)

        info_layout = QVBoxLayout()
        info_layout.addWidget(self.song_label)
        info_layout.addWidget(self.time_label)
        info_layout.addWidget(self.bitrate_label)
        info_layout.addWidget(self.mixrate_label)

        control_layout = QHBoxLayout()
        for btn in [self.prev_btn, self.play_btn, self.pause_btn, self.next_btn, self.restart_btn]:
            control_layout.addWidget(btn)

        options_layout = QHBoxLayout()
        options_layout.addWidget(self.shuffle_btn)
        options_layout.addWidget(self.loop_btn)

        main_layout = QVBoxLayout()
        main_layout.addLayout(info_layout)
        main_layout.addWidget(self.volume_slider)
        main_layout.addLayout(control_layout)
        main_layout.addLayout(options_layout)

        self.setLayout(main_layout)

    def init_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

    def play_song(self):
        self.player.play()
        self.song_label.setText(
            f"SONG: {self.player.playlist[self.player.current_index]}")

    def pause_song(self):
        self.player.pause()

    def next_song(self):
        song = self.player.next()
        self.song_label.setText(f"SONG: {song}")

    def prev_song(self):
        song = self.player.previous()
        self.song_label.setText(f"SONG: {song}")

    def restart_song(self):
        self.player.rewind()

    def toggle_shuffle(self):
        self.player.toggle_shuffle()
        self.shuffle_btn.setStyleSheet("background-color: lightgreen;" if self.player.shuffle else "")

    def toggle_loop(self):
        self.player.toggle_loop()
        self.loop_btn.setStyleSheet("background-color: lightgreen;" if self.player.loop else "")

    def update_time(self):
        if self.player.is_playing():
            pos = self.player.get_position()
            self.time_label.setText(f"{pos // 60:02}:{pos % 60:02}")
        elif not self.player.paused:
            if self.player.loop:
                self.player.rewind()
            else:
                self.next_song()

