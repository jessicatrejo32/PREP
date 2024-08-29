# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 15:29:20 2024

@author: jessica.trejo
"""

import requests
import zipfile
import os


url = 'https://prep2024.ine.mx/publicacion/nacional/assets/20240603_2005_PREP.zip'
nombre_archivo = '20240603_2005_PREP.zip'
directorio_destino = '/var/jenkins_home/workspace/Publicacion/Archivos'  # Carpeta donde se van a extraer los archivos
ruta_completa = os.path.join(directorio_destino, nombre_archivo)

# Crear la carpeta de destino si no existe
if not os.path.exists(directorio_destino):
    os.makedirs(directorio_destino)

# Realizar la petición GET al servidor
respuesta = requests.get(url)

# Verificar si la descarga fue exitosa (código 200)
if respuesta.status_code == 200:
    # Guardar el contenido descargado en un archivo local
    with open(ruta_completa, 'wb') as archivo:
        archivo.write(respuesta.content)
    print(f'Descarga exitosa: {ruta_completa}')
else:
    print(f'Error al descargar: {respuesta.status_code}')
    

archivo_zip1 = os.path.join(f"{directorio_destino}/20240603_2005_PREP.zip")  # Nombre del archivo ZIP a descomprimir
# Descomprimir el archivo ZIP
with zipfile.ZipFile(archivo_zip1, 'r') as zip_ref:
    zip_ref.extractall(directorio_destino)

print(f'Archivo ZIP "{archivo_zip1}" descomprimido exitosamente en "{directorio_destino}"')

archivo_zip2 = os.path.join(f"{directorio_destino}/20240603_2005_PREP_DIP_FED.zip")  # Nombre del archivo ZIP a descomprimir
# Descomprimir el archivo ZIP
with zipfile.ZipFile(archivo_zip2, 'r') as zip_ref:
    zip_ref.extractall(directorio_destino)

print(f'Archivo ZIP "{archivo_zip2}" descomprimido exitosamente en "{directorio_destino}"')

archivo_zip3 = os.path.join(f"{directorio_destino}/20240603_2005_PREP_PRES.zip")  # Nombre del archivo ZIP a descomprimir
# Descomprimir el archivo ZIP
with zipfile.ZipFile(archivo_zip3, 'r') as zip_ref:
    zip_ref.extractall(directorio_destino)

print(f'Archivo ZIP "{archivo_zip3}" descomprimido exitosamente en "{directorio_destino}"')

archivo_zip4 = os.path.join(f"{directorio_destino}/20240603_2005_PREP_SEN.zip")  # Nombre del archivo ZIP a descomprimir
# Descomprimir el archivo ZIP
with zipfile.ZipFile(archivo_zip4, 'r') as zip_ref:
    zip_ref.extractall(directorio_destino)

print(f'Archivo ZIP "{archivo_zip4}" descomprimido exitosamente en "{directorio_destino}"')

# Mostrar los archivos extraídos
for root, dirs, files in os.walk(directorio_destino):
    for file in files:
        print(os.path.join(root, file))

