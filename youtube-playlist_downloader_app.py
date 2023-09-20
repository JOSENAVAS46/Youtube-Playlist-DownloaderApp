from pytube import Playlist
import os
import re

def limpiar_nombre(nombre):
    # Eliminar caracteres inválidos en nombres de directorio en Windows
    return re.sub(r'[\/:*?"<>|]', '_', nombre)

def mostrar_titulos_canciones(playlist):
    print("Canciones en la lista de reproducción:")
    for i, video in enumerate(playlist.videos, 1):
        print(f"{i}. {video.title}")

def descargar_playlist_youtube(url_playlist, directorio_destino, genero):
    try:
        # Crear un objeto Playlist
        playlist = Playlist(url_playlist)

        # Mostrar los títulos de las canciones en la lista de reproducción
        mostrar_titulos_canciones(playlist)

        # Obtener el título de la lista de reproducción y limpiarlo
        nombre_lista = limpiar_nombre(playlist.title)

        # Crear un directorio para la lista de reproducción
        directorio_destino_playlist = os.path.join(directorio_destino, nombre_lista)
        if not os.path.exists(directorio_destino_playlist):
            os.makedirs(directorio_destino_playlist)

        # Descargar cada video de la lista de reproducción con el género y el nombre de la canción
        for video in playlist.videos:
            try:
                # Obtener la mejor calidad de audio disponible
                audio_stream = video.streams.filter(only_audio=True).order_by("abr").desc().first()

                if audio_stream:
                    # Generar un nombre de archivo con el género y el nombre de la canción
                    nombre_archivo = f"{genero} - {video.title}.mp3"

                    # Descargar el audio al directorio de destino con el nuevo nombre de archivo
                    audio_stream.download(output_path=directorio_destino_playlist, filename=nombre_archivo)
                    print(f"+ Descarga de audio para '{video.title}'. Guardado en {directorio_destino_playlist}/{nombre_archivo}")
                else:
                    print(f"El video '{video.title}' no tiene formato de audio disponible y no se pudo descargar.")
            except Exception as e:
                print(f"- Error al descargar el audio del video '{video.title}': {e}")

        print("+ Descarga de la lista de reproducción completada. +")

    except Exception as e:
        print(f"Error al descargar la lista de reproducción: {e}")

if __name__ == "__main__":
    # Solicitar al usuario que ingrese el género una sola vez
    genero = input("Ingresa el género de las canciones en la lista de reproducción: ")

    # Solicitar al usuario que ingrese la URL de la lista de reproducción de YouTube
    url_playlist_youtube = input("Ingresa la URL de la lista de reproducción de YouTube que deseas descargar: ")

    # Directorio donde deseas guardar todas las listas de reproducción
    directorio_destino = "playlists_youtube"
    if not os.path.exists(directorio_destino):
        os.makedirs(directorio_destino)

    # Llamar a la función para descargar la lista de reproducción de YouTube
    descargar_playlist_youtube(url_playlist_youtube, directorio_destino, genero)
