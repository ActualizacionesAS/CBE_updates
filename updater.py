import requests
import subprocess
import os

# URL del archivo que contiene la última versión
LATEST_VERSION_URL = 'https://raw.githubusercontent.com/tu_usuario/mi_aplicacion/main/latest_version.txt'

# URL base para descargar las versiones
BASE_DOWNLOAD_URL = 'https://raw.githubusercontent.com/tu_usuario/mi_aplicacion/main/versions/'

def get_current_version():
    with open('version.txt', 'r') as file:
        return file.read().strip()

def check_for_update(current_version):
    response = requests.get(LATEST_VERSION_URL)
    latest_version = response.text.strip()
    return latest_version > current_version, latest_version

def download_update(latest_version):
    download_url = f"{BASE_DOWNLOAD_URL}{latest_version}/installer.exe"
    download_path = f"installer_{latest_version}.exe"

    response = requests.get(download_url, stream=True)
    with open(download_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

    return download_path

def install_update(installer_path):
    subprocess.run([installer_path], check=True)

def run_application():
    subprocess.run(['python', 'app.py'])

if __name__ == "__main__":
    current_version = get_current_version()
    update_available, latest_version = check_for_update(current_version)

    if update_available:
        print(f"Nueva versión disponible: {latest_version}")
        installer_path = download_update(latest_version)
        install_update(installer_path)
    else:
        print("No hay actualizaciones disponibles. Ejecutando la aplicación...")
        run_application()
