print(
r'''
$$$$$$$\          $$$$$$$\            $$\                                                   
$$  __$$\         $$  __$$\           $$ |                                                  
$$ |  $$ |        $$ |  $$ | $$$$$$\  $$ | $$$$$$\  $$$$$$$\   $$$$$$$\  $$$$$$\   $$$$$$\  
$$$$$$$  |$$$$$$\ $$$$$$$\ | \____$$\ $$ | \____$$\ $$  __$$\ $$  _____|$$  __$$\ $$  __$$\ 
$$  __$$< \______|$$  __$$\  $$$$$$$ |$$ | $$$$$$$ |$$ |  $$ |$$ /      $$$$$$$$ |$$ |  \__|
$$ |  $$ |        $$ |  $$ |$$  __$$ |$$ |$$  __$$ |$$ |  $$ |$$ |      $$   ____|$$ |      
$$ |  $$ |        $$$$$$$  |\$$$$$$$ |$$ |\$$$$$$$ |$$ |  $$ |\$$$$$$$\ \$$$$$$$\ $$ |      
\__|  \__|        \_______/  \_______|\__| \_______|\__|  \__| \_______| \_______|\__|      
============================================================================================
[*] R-Balancer - Load Balancer ( Round-Robin ) | R&D incrustwerush.org - Afrizal F.A
============================================================================================
''')

import socket
import threading
from argparse import ArgumentParser

class RBalancer:

    def __init__(self, servers):
        self.servers = self.listServer(servers)
        self.current_server = 0

    def listServer(self, servers):
        try:
            server_list = []

            for entry in servers.split(","):
                host, port = entry.split(":")
                server_list.append((host, int(port)))

            return server_list
        
        except Exception as E:
            print(f"[!] [Error: {E}]")

    def handle_client(self, client_socket):
        try:
            server = self.servers[self.current_server]
            self.current_server = (self.current_server + 1) % len(self.servers)

            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.connect(server)

            threading.Thread(target=self.forward_data, args=(client_socket, server_socket)).start()
            threading.Thread(target=self.forward_data, args=(server_socket, client_socket)).start()

        except Exception as E:
            print(f"[!] [Error: {E}]")

    def forward_data(self, source, destination):
        try:
            while True:
                
                try:
                    data = source.recv(4096)
                    
                    if not data:
                        break
                    
                    destination.sendall(data)
                    
                except:
                    break

            source.close()
            destination.close()

        except Exception as E:
            print(f"[!] [Error: {E}]")

    def start(self, bind_ip, bind_port):
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind((bind_ip, bind_port))
            server.listen(5)

            print(f"[*] Listening on {bind_ip}:{bind_port}")

            while True:
                try:
                    client_socket, addr = server.accept()
                    print(f"[*] Accepted connection from {addr}")

                    client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
                    client_handler.start()
                
                except Exception as E:
                    print(f"[!] [Error: {E}]")

        except Exception as E:
            print(f"[!] [Error: {E}]")

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-s", "--server", help="Host Server Balancer", required=True, type=str)
    parser.add_argument("-p", "--port", help="PORT Server Balancer", required=True, type=int)
    parser.add_argument("-l", "--list", help="List Backend Server", required=True, type=str)
    args = parser.parse_args()
    
    run = RBalancer(args.list)
    run.start(args.server, args.port)
