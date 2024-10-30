# PyPlay

## Descripción

**PyPlay** es una aplicación de escritorio que permite a los usuarios controlar su música de Spotify directamente desde su computadora, sin necesidad de abrir la aplicación completa de Spotify. Diseñado para ofrecer una interfaz minimalista y funcional, PyPlay facilita la reproducción, pausa, cambio de pistas y ajustes básicos, mejorando la experiencia de quienes buscan un acceso rápido a su música mientras trabajan o realizan otras actividades.

## Funcionalidades

- **Control de Reproducción**: Reproduce, pausa, cambia a la siguiente o anterior canción en tu lista.
- **Control de Volumen y Tiempo**: Ajusta el volumen y navega entre las partes de una canción.
- **Modos Aleatorio y Repetición**: Activa o desactiva el modo aleatorio y elige si deseas repetir una canción o lista.
- **Interfaz Simple y Personalizable**: Un diseño de ventana flotante para acceder a tu música sin interrupciones.

## Instalación

### Requisitos previos

- **Python 3.7+**: PyPlay se desarrolla en Python, por lo que necesitas tener Python instalado.
- **Spotify Premium**: Requiere una cuenta de Spotify Premium para controlar la música.

### Paso a Paso de Instalación

1. **Clona el repositorio**:
   ```bash
   git clone https://github.com/tu-usuario/PyPlay.git
   cd PyPlay
   ```

2. **Crea un entorno virtual** (opcional pero recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate    # En macOS o Linux
   venv\Scripts\activate       # En Windows
   ```

3. **Instala las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configura las credenciales de Spotify**:
   - Regístrate y crea una aplicación en el [Panel de desarrolladores de Spotify](https://developer.spotify.com/dashboard).
   - Obtén tu **Client ID** y **Client Secret** y colócalos en un archivo `.env` en el directorio de PyPlay:
     ```
     SPOTIPY_CLIENT_ID='tu_client_id'
     SPOTIPY_CLIENT_SECRET='tu_client_secret'
     SPOTIPY_REDIRECT_URI='http://localhost:8888/callback'
     ```

5. **Ejecuta PyPlay**:
   ```bash
   python pyplay.py
   ```

## Uso

Una vez que la aplicación esté en ejecución, podrás controlar tu música desde la interfaz flotante de PyPlay. Al iniciar sesión en Spotify, PyPlay mostrará la canción en reproducción, permitiéndote controlar fácilmente la lista de reproducción, el volumen y más.
