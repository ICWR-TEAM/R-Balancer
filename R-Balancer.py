#!/usr/bin/python3

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

import os, json, socket, ssl, re
import threading
from argparse import ArgumentParser

class RBalancer:

    def __init__(self, servers, ssl_backend=False, host_header=None):
        self.servers = self.listServer(servers)
        self.current_server = 0
        self.ssl_backend = ssl_backend
        self.host_header = host_header

    def listServer(self, servers):
        try:
            server_list = []

            for entry in servers.split(","):
                host, port = entry.split(":")
                server_list.append((host, int(port)))

            return server_list
        
        except Exception as E:
            print(f"[!] [Error: {E}]")

    def modify_http_request(self, data):
        if not self.host_header:
            return data
        # Simple HTTP request modification: replace Host header
        lines = data.decode('utf-8', errors='ignore').split('\r\n')
        modified_lines = []
        for line in lines:
            if line.lower().startswith('host:'):
                modified_lines.append(f'Host: {self.host_header}')
            else:
                modified_lines.append(line)
        return '\r\n'.join(modified_lines).encode('utf-8')

    def handle_client(self, client_socket):
        try:
            server = self.servers[self.current_server]
            self.current_server = (self.current_server + 1) % len(self.servers)

            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.connect(server)

            if self.ssl_backend:
                context = ssl.create_default_context()
                server_socket = context.wrap_socket(server_socket, server_hostname=server[0])

            modify_func = self.modify_http_request if self.host_header else None
            threading.Thread(target=self.forward_data_modify, args=(client_socket, server_socket, modify_func)).start()
            threading.Thread(target=self.forward_data, args=(server_socket, client_socket)).start()

        except Exception as E:
            print(f"[!] [Error: {E}]")

    def forward_data_modify(self, source, destination, modify_func=None):
        try:
            while True:
                try:
                    data = source.recv(4096)
                    if not data:
                        break
                    if modify_func:
                        data = modify_func(data)
                    destination.sendall(data)
                except:
                    break
            source.close()
            destination.close()
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

    configFile = "R-Balancer.conf"

    if os.path.isfile(configFile):

        opt = json.loads(open(configFile, "r").read())

    else:

        parser = ArgumentParser()
        parser.add_argument("-s", "--server", help="Host Server Balancer", required=True, type=str)
        parser.add_argument("-p", "--port", help="PORT Server Balancer", required=True, type=int)
        parser.add_argument("-l", "--list", help="List Backend Server", required=True, type=str)
        parser.add_argument("--ssl-backend", help="Use SSL for backend server connections", action="store_true")
        parser.add_argument("--host-header", help="Override Host header for requests", type=str)
        args = parser.parse_args()

        opt = {
            "server": args.server,
            "port": args.port,
            "list_server": args.list,
            "ssl_backend": args.ssl_backend,
            "host_header": args.host_header
        }
    
    run = RBalancer(opt["list_server"], opt.get("ssl_backend", False), opt.get("host_header"))
    run.start(opt["server"], int(opt["port"]))
