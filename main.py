
import sys
import os
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QSlider, QMainWindow, QScrollArea
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap, QIcon
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# Cargar las variables de entorno
load_dotenv()

class AlbumWindow(QWidget):
    def __init__(self, albums):
        super().__init__()
        self.setWindowTitle("Álbumes")
        self.setGeometry(300, 300, 300, 400)
        
        # Layout de la ventana de álbumes
        layout = QVBoxLayout()
        
        # Scroll area para la lista de álbumes
        scroll_area = QScrollArea(self)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        # Mostrar cada álbum con su carátula
        for album in albums:
            album_layout = QHBoxLayout()
            
            album_cover = QLabel()
            pixmap = QPixmap()
            try:
                pixmap.loadFromData(requests.get(album['cover']).content)
                album_cover.setPixmap(pixmap.scaled(50, 50, Qt.KeepAspectRatio))
            except Exception as e:
                print(f"Error al cargar la carátula del álbum: {e}")
                album_cover.setText("No Image")
            
            album_layout.addWidget(album_cover)
            
            album_name = QLabel(album['name'])
            album_layout.addWidget(album_name)
            
            scroll_layout.addLayout(album_layout)
        
        scroll_area.setWidget(scroll_widget)
        layout.addWidget(scroll_area)
        self.setLayout(layout)

class PyPlay(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyPlay")
        self.setGeometry(100, 100, 500, 150)  # Ajustar el tamaño de la ventana

        # Autenticación de Spotify
        self.sp = Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv("SPOTIPY_CLIENT_ID"),
                                                     client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
                                                     redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
                                                     scope="user-read-playback-state,user-modify-playback-state,user-read-currently-playing,user-library-read"))

        # Configuración de UI
        self.initUI()

        # Temporizador para actualizar la información de la canción
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_song_info)
        self.timer.start(1000)

    def initUI(self):
        main_layout = QHBoxLayout()

        # Carátula del álbum
        self.album_cover = QLabel()
        pixmap = QPixmap("assets/icons/album-placeholder.jpg")  # Imagen por defecto
        self.album_cover.setPixmap(pixmap.scaled(80, 80, Qt.KeepAspectRatio))
        main_layout.addWidget(self.album_cover)

        # Contenedor de información de la canción y barra de progreso
        info_layout = QVBoxLayout()

        # Título de la canción y artista
        self.song_title = QLabel("Nombre de la Canción - Artista")
        info_layout.addWidget(self.song_title)

        # Barra de progreso
        progress_layout = QHBoxLayout()
        self.current_time = QLabel("0:00")
        progress_layout.addWidget(self.current_time)

        self.progress_bar = QSlider(Qt.Horizontal)
        progress_layout.addWidget(self.progress_bar)

        self.total_time = QLabel("0:00")
        progress_layout.addWidget(self.total_time)
        info_layout.addLayout(progress_layout)

        main_layout.addLayout(info_layout)

        # Controles de reproducción
        controls_layout = QHBoxLayout()

        # Botones de control de reproducción
        prev_button = QPushButton()
        prev_button.setIcon(QIcon("assets/icons/Anterior.png"))
        prev_button.clicked.connect(self.previous_track)
        controls_layout.addWidget(prev_button)

        self.play_pause_button = QPushButton()
        self.play_pause_button.setIcon(QIcon("assets/icons/Reproducir.png"))
        self.play_pause_button.clicked.connect(self.toggle_play_pause)
        controls_layout.addWidget(self.play_pause_button)

        next_button = QPushButton()
        next_button.setIcon(QIcon("assets/icons/Siguiente.png"))
        next_button.clicked.connect(self.next_track)
        controls_layout.addWidget(next_button)

        shuffle_button = QPushButton()
        shuffle_button.setIcon(QIcon("assets/icons/Aleatorio.png"))
        controls_layout.addWidget(shuffle_button)

        repeat_button = QPushButton()
        repeat_button.setIcon(QIcon("assets/icons/Repetir.png"))
        controls_layout.addWidget(repeat_button)

        volume_button = QPushButton()
        volume_button.setIcon(QIcon("assets/icons/Volumen.png"))
        controls_layout.addWidget(volume_button)

        settings_button = QPushButton()
        settings_button.setIcon(QIcon("assets/icons/Opciones.png"))
        controls_layout.addWidget(settings_button)

        main_layout.addLayout(controls_layout)

        # Botón de álbumes
        album_button = QPushButton()
        album_button.setIcon(QIcon("assets/icons/Album.png"))  # Usa un icono adecuado
        album_button.clicked.connect(self.show_albums)
        main_layout.addWidget(album_button)

        # Agregar el layout principal al widget central
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

    def update_song_info(self):
        # Obtener la canción en reproducción
        track = self.sp.current_playback()
        if track and track["is_playing"]:
            item = track["item"]
            self.song_title.setText(f"{item['name']} - {item['artists'][0]['name']}")
            self.progress_bar.setMaximum(item["duration_ms"])
            self.progress_bar.setValue(track["progress_ms"])
            self.current_time.setText(self.format_time(track["progress_ms"]))
            self.total_time.setText(self.format_time(item["duration_ms"]))

            # Actualizar la carátula del álbum
            album_url = item["album"]["images"][0]["url"]
            try:
                pixmap = QPixmap()
                pixmap.loadFromData(requests.get(album_url).content)
                self.album_cover.setPixmap(pixmap.scaled(80, 80, Qt.KeepAspectRatio))
            except Exception as e:
                print(f"Error al cargar la carátula del álbum: {e}")
                self.album_cover.setText("No Image")

    def show_albums(self):
        # Obtener álbumes del usuario
        albums = []
        try:
            results = self.sp.current_user_saved_albums(limit=10)
            for item in results['items']:
                album = item['album']
                albums.append({
                    'name': album['name'],
                    'cover': album['images'][0]['url']
                })
        except Exception as e:
            print(f"Error al obtener los álbumes: {e}")
        
        # Mostrar ventana de álbumes
        self.album_window = AlbumWindow(albums)
        self.album_window.show()

    def toggle_play_pause(self):
        playback_state = self.sp.current_playback()
        if playback_state["is_playing"]:
            self.sp.pause_playback()
            self.play_pause_button.setIcon(QIcon("assets/icons/Reproducir.png"))
        else:
            self.sp.start_playback()
            self.play_pause_button.setIcon(QIcon("assets/icons/Pausar.png"))

    def next_track(self):
        self.sp.next_track()
        self.update_song_info()

    def previous_track(self):
        self.sp.previous_track()
        self.update_song_info()

    def format_time(self, ms):
        seconds = (ms // 1000) % 60
        minutes = (ms // (1000 * 60)) % 60
        return f"{minutes}:{seconds:02}"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PyPlay()
    window.show()
    sys.exit(app.exec_())
