#!/usr/bin/env python3

from command_and_control import Listener
from termcolor import colored

if __name__ == '__main__':
    logo = """


   _____                   _____ .__            
  /  _  \_______   ____   /  |  ||  |__   ____  
 /  /_\  \_  __ \_/ ___\ /   |  ||  |  \_/ __ \ 
/    |    \  | \/\  \___/    ^   /   Y  \  ___/ 
\____|__  /__|    \___  >____   ||___|  /\___  >
        \/            \/     |__|     \/     \/ 


"""
    print(colored(logo, 'red')) 
    ip = input(colored("\n[+] Enter your IP Address >> ", 'green'))
    my_listener = Listener(ip, 4100)
    my_listener.run()
