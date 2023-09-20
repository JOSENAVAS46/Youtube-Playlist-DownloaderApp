import os
import subprocess

def convertir_a_mp3(input_dir, output_dir):
    for root, _, files in os.walk(input_dir):
        for filename in files:
            input_path = os.path.join(root, filename)
            output_filename = os.path.splitext(filename)[0] + ".mp3"
            output_path = os.path.join(output_dir, output_filename)

            try:
                # Utilizamos subprocess para llamar a FFmpeg y realizar la conversión
                subprocess.run(['ffmpeg', '-i', input_path, '-vn', '-ar', '44100', '-ac', '2', '-ab', '192k', '-f', 'mp3', output_path], capture_output=True, text=True, check=True)
                print(f"Convertido '{filename}' a 'mp3'")
            except subprocess.CalledProcessError as e:
                print(f"Error al convertir '{filename}': {e.stderr}")

if __name__ == "__main__":
    input_directory = input("Ingresa la ubicación completa del directorio de entrada: ")
    output_directory = os.path.join("mp3_output", os.path.basename(input_directory))  # Directorio de salida personalizado

    # Asegúrate de que el directorio de salida exista
    os.makedirs(output_directory, exist_ok=True)

    # Convertir todos los archivos a mp3
    convertir_a_mp3(input_directory, output_directory)

    print("La conversión ha finalizado. Los archivos mp3 se han guardado en:", output_directory)
