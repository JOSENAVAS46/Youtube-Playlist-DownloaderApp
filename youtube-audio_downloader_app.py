from pytube import YouTube
import os

def seleccionar_calidad_audio(audio_streams):
    print("Elige la calidad del audio:")
    for i, audio_stream in enumerate(audio_streams, 1):
        print(f"{i}. Calidad: {audio_stream.abr} - Formato: {audio_stream.mime_type}")
    
    opcion = int(input("Ingresa el número de la opción deseada: ")) - 1

    if 0 <= opcion < len(audio_streams):
        return audio_streams[opcion]
    else:
        print("Opción inválida. Elige una opción válida.")
        return None

def descargar_audio_youtube(url, directorio_destino, genero):
    try:
        # Crear un objeto YouTube
        yt = YouTube(url)

        # Obtener todos los streams de audio disponibles
        audio_streams = yt.streams.filter(only_audio=True)
        
        # Permitir al usuario seleccionar la calidad del audio
        audio_stream = seleccionar_calidad_audio(audio_streams)
        
        if audio_stream:
            # Generar un nombre de archivo con el número incrementable, el género y el nombre de la canción
            numero_incrementable = len(os.listdir(directorio_destino)) + 1
            nombre_archivo = f"{numero_incrementable} - {genero} - {yt.title}.mp3"

            # Descargar el audio al directorio de destino con el nuevo nombre de archivo
            audio_stream.download(output_path=directorio_destino, filename=nombre_archivo)

            print(f"Descarga de audio completada. Archivo de audio guardado en {directorio_destino}/{nombre_archivo}")
        else:
            print("No se pudo seleccionar la calidad del audio.")

    except Exception as e:
        print(f"Error al descargar el audio: {e}")

if __name__ == "__main__":
    # Solicitar al usuario que ingrese el género una sola vez
    genero = input("Ingresa el género de la canción: ")

    # Solicitar al usuario que ingrese la URL del video de YouTube
    url_video_youtube = input("Ingresa la URL del video de YouTube del cual deseas extraer el audio: ")

    # Directorio donde deseas guardar el audio
    directorio_destino = "audio_youtube"
    if not os.path.exists(directorio_destino):
        os.makedirs(directorio_destino)

    # Llamar a la función para descargar el audio de YouTube
    descargar_audio_youtube(url_video_youtube, directorio_destino, genero)
