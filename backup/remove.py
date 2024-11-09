#!/usr/bin/env python3

import os
import subprocess
import sys

def check_root():
    if os.geteuid() != 0:
        sys.exit("Este script debe ser ejecutado como root.")


def remove_service():
    service_name = 'important-system.service'
    service_path = f'/etc/systemd/system/{service_name}'

    # Detener el servicio si está en ejecución
    try:
        subprocess.run(['systemctl', 'stop', service_name], check=True)
        print(f"Servicio {service_name} detenido.")
    except subprocess.CalledProcessError:
        print(f"Error al detener el servicio {service_name}, puede que no esté en ejecución.")

    # Deshabilitar el servicio
    try:
        subprocess.run(['systemctl', 'disable', service_name], check=True)
        print(f"Servicio {service_name} deshabilitado.")
    except subprocess.CalledProcessError:
        print(f"Error al deshabilitar el servicio {service_name}, puede que no esté habilitado.")

    # Eliminar el archivo del servicio
    if os.path.exists(service_path):
        os.remove(service_path)
        print(f"Archivo de servicio {service_path} eliminado.")
    else:
        print(f"No se encontró el archivo de servicio {service_path}.")

def remove_script():
    script_path = '/var/tmp/.important-system.py'
    
    # Eliminar el script
    if os.path.exists(script_path):
        os.remove(script_path)
        print(f"Script {script_path} eliminado.")
    else:
        print(f"No se encontró el script {script_path}.")

if __name__ == '__main__':
    check_root()
    remove_service()
    remove_script()
    print("Configuración eliminada correctamente.")
