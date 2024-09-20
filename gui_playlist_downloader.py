import os
import re
import tkinter as tk
from tkinter import messagebox, filedialog
import yt_dlp

def limpiar_nombre(nombre):
    # Eliminar caracteres inválidos en nombres de directorio en Windows
    return re.sub(r'[\/:*?"<>|]', '_', nombre)

def mostrar_titulos_canciones(url_playlist):
    # Usar yt-dlp para obtener los títulos de los videos
    ydl_opts = {
        'extract_flat': True,  # Extraer solo la lista de reproducción, no los videos
        'quiet': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url_playlist, download=False)
        return [f"{i+1}. {entry['title']}" for i, entry in enumerate(info['entries'])]

def descargar_playlist_youtube(url_playlist, directorio_destino, genero, ventana, lista_titulos):
    try:
        # Mostrar los títulos de las canciones en la lista de reproducción
        canciones = mostrar_titulos_canciones(url_playlist)
        lista_titulos.delete(0, tk.END)
        for cancion in canciones:
            lista_titulos.insert(tk.END, cancion)

        # Obtener el título de la lista de reproducción y limpiarlo
        nombre_lista = limpiar_nombre(canciones[0])  # Usa el nombre del primer video

        # Crear un directorio para la lista de reproducción
        directorio_destino_playlist = os.path.join(directorio_destino, nombre_lista)
        if not os.path.exists(directorio_destino_playlist):
            os.makedirs(directorio_destino_playlist)

        # Opciones de yt-dlp para descargar solo el audio
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(directorio_destino_playlist, f'{genero} - %(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        # Descargar el audio de la lista de reproducción
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url_playlist])

        messagebox.showinfo("Completado", "Descarga de la lista de reproducción completada.")

    except Exception as e:
        messagebox.showerror("Error", f"Error al descargar la lista de reproducción: {e}")

def seleccionar_directorio():
    directorio = filedialog.askdirectory()
    if directorio:
        directorio_destino_entry.delete(0, tk.END)
        directorio_destino_entry.insert(0, directorio)

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Descargar Playlist de YouTube con yt-dlp")
ventana.geometry("600x400")

# Etiqueta y campo para la URL de la playlist
tk.Label(ventana, text="URL de la Playlist de YouTube:").pack(pady=5)
url_playlist_entry = tk.Entry(ventana, width=50)
url_playlist_entry.pack(pady=5)

# Etiqueta y campo para el género
tk.Label(ventana, text="Género de las canciones:").pack(pady=5)
genero_entry = tk.Entry(ventana, width=50)
genero_entry.pack(pady=5)

# Botón para seleccionar el directorio de destino
tk.Button(ventana, text="Seleccionar directorio de destino", command=seleccionar_directorio).pack(pady=5)

# Campo de texto para mostrar el directorio seleccionado
directorio_destino_entry = tk.Entry(ventana, width=50)
directorio_destino_entry.pack(pady=5)

# Lista de títulos de canciones
lista_titulos = tk.Listbox(ventana, width=70, height=10)
lista_titulos.pack(pady=5)

# Función para iniciar la descarga
def iniciar_descarga():
    url_playlist = url_playlist_entry.get()
    genero = genero_entry.get()
    directorio_destino = directorio_destino_entry.get()
    
    if not url_playlist or not genero or not directorio_destino:
        messagebox.showwarning("Campos incompletos", "Por favor, completa todos los campos antes de descargar.")
    else:
        descargar_playlist_youtube(url_playlist, directorio_destino, genero, ventana, lista_titulos)

# Botón para iniciar la descarga
tk.Button(ventana, text="Iniciar Descarga", command=iniciar_descarga).pack(pady=5)

# Ejecutar la ventana
ventana.mainloop()
