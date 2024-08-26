# R-Balancer

![Python Logo](https://camo.githubusercontent.com/3c55df0eaf0804dba65a57bfd09fd26419a1bec537962d966ace4e4959b51f5a/687474703a2f2f466f7254686542616467652e636f6d2f696d616765732f6261646765732f6d6164652d776974682d707974686f6e2e737667)

R-Balancer is a simple load balancer implementation using the Round-Robin algorithm. It distributes incoming client requests across multiple backend servers to balance the load. This script is designed for use in Python 3.x.

## Features

- **Round-Robin Load Balancing**: Distributes incoming requests evenly across a list of backend servers.
- **Multithreading**: Handles multiple client connections simultaneously using threads.
- **Configurable**: Allows customization of server addresses and ports via command-line arguments.

## Requirements

- Python 3.x
- `socket` and `threading` modules (built-in Python libraries)

## Installation

Clone the repository or download the script:

```bash
git clone <repository-url>
cd <repository-directory>
```

## Usage

Run the script using the following command format:

```bash
python R-Balancer.py -s <host> -p <port> -l "<server1>:<port1>,<server2>:<port2>,..."
```

### Arguments

- `-s` or `--server`: The IP address or hostname where the load balancer will listen for incoming connections.
- `-p` or `--port`: The port on which the load balancer will listen.
- `-l` or `--list`: A comma-separated list of backend servers in the format `host:port`.

### Example

To start the load balancer on `0.0.0.0` port `8080` and distribute requests to backend servers `127.0.0.1:8081`, `127.0.0.1:8082`, and `127.0.0.1:8083`:

```bash
python R-Balancer.py -s 0.0.0.0 -p 8080 -l "127.0.0.1:8081,127.0.0.1:8082,127.0.0.1:8083"
```

### Or Using Config file

Create config file in same directory with name `R-Balancer.conf`.

Example config:

```json
{
    "server": "0.0.0.0",
    "port": 80,
    "list_server": "192.168.1.3:80,192.168.1.4:8080,192.168.1.5:8000"
}
```

## Script Overview

- **Initialization**: `RBalancer` class is initialized with a list of backend servers.
- **Server List**: The `listServer` method parses the backend server list from a string.
- **Client Handling**: The `handle_client` method handles incoming client connections and forwards them to backend servers in a round-robin manner.
- **Data Forwarding**: The `forward_data` method transfers data between client and server.
- **Starting**: The `start` method binds the load balancer to the specified IP and port and begins listening for incoming connections.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
