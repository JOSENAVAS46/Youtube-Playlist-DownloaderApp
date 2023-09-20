from pytube import YouTube
import os

def descargar_video_youtube(url, directorio_destino):
    try:
        # Crear un objeto YouTube
        yt = YouTube(url)

        # Obtener la mejor calidad de video disponible
        video = yt.streams.get_highest_resolution()

        # Descargar el video al directorio de destino
        video.download(output_path=directorio_destino)

        print(f"Descarga del video completada. Archivo guardado en {directorio_destino}")
    except Exception as e:
        print(f"Error al descargar el video: {e}")

if __name__ == "__main__":
    # Solicitar al usuario que ingrese la URL del video de YouTube
    url_video_youtube = input("Ingresa la URL del video de YouTube que deseas descargar: ")

    # Directorio donde deseas guardar el video
    directorio_destino = "video_youtube"
    if not os.path.exists(directorio_destino):
        os.makedirs(directorio_destino)

    # Llamar a la función para descargar el video de YouTube
    descargar_video_youtube(url_video_youtube, directorio_destino)
