"""Network Connection"""
import socket

"""
COMMANDS
---------

=> md dir_name          | make directory
=> mf file_name         | make file
=> cd full_path         | change directory to new path
=> wd file_name size    | write data to file



"""


# "192.168.1.106"
class NetworkInterface:

    def __init__(self, host_ip: str):
        self._HOST_IP = host_ip
        self._PORT = 5000
        self._CONNECTION = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._TRANSFER_SIZE = 1024
        self._ENCODING_TYPE = "UTF-8"
        self._connected = False
    
    @property
    def is_connected(self) -> bool: 
        return self._connected

    # @property
    # def encoding_type(self) -> str:
    #     return self._ENCODING_TYPE
    
    def disconnect(self):
        """Ends the connection between the server and the host"""
        self._CONNECTION.close()

class NetworkCommands:
    MAKE_FILE = 1
    MAKE_DIRECTORY = 2
    CHANGE_DIRECTORY = 3
    WRITE_DATA = 4

    paramLengths = {
        MAKE_FILE: 1, 
        MAKE_DIRECTORY: 1, 
        CHANGE_DIRECTORY: 1, 
        WRITE_DATA: 2
    }

class NetworkHost(NetworkInterface):

    def __init__(self, host_ip: str):
        super().__init__(host_ip)
        self._CLIENT = None
        self._CLIENT_ADDR = None
        self._setup_server()
    
    def _setup_server(self):
        """Sets up the server and waits for the client to connect"""
        try:
            self._start_sever()
            self._listen_for_client()
            if (self._CLIENT != None):
                self._connected = True
        except:
            print("Failed to connect to client")
    
    def _start_sever(self):
        """Starts sever"""
        self._CONNECTION.bind((self._HOST_IP, self._PORT))
        self._CONNECTION.listen(1)
        
    def _listen_for_client(self):
        """Waits for a client to connect"""
        self._CLIENT, self._CLIENT_ADDR = self._CONNECTION.accept()
    
    def _send_data(self, data: bytes) -> bool:
        """Sends data to client"""
        data_sent = False
        try:
            self._CLIENT.send(data)
            data_sent = True
        except:
            print("Failed to send data to client")
        return data_sent
    
    def retrieve_data(self) -> str:
        """Gets data retrieved from client. Note the client can only send string messages."""
        data = self._CLIENT.recv(self._TRANSFER_SIZE)
        return data.decode("utf-8")
    
    def send_command(self, command: int, params: list, should_encode=True) -> bool:
        """Sends a command to the client"""
        is_data_sent = False
        correct_number_of_params = len(params) == NetworkCommands.paramLengths[command]
        if correct_number_of_params:
            data = (str(command) + " " + ' '.join(map(str, params)))
            if should_encode:
                data = data.encode(self._ENCODING_TYPE)
            is_data_sent = self._send_data(data)
        else:
            print("Invalid number of parameters")
        return is_data_sent
    
    def send_file_bytes(self, data: bytes) -> bool:
        """Sends the bytes for a file"""
        return self._send_data(data)

class NetworkClient(NetworkInterface):

    def __init__(self, host_ip: str):
        super().__init__(host_ip)
        self._connect_to_host()
        
    def _connect_to_host(self):
        """Used to connect to the host"""
        try:
            self._CONNECTION.connect((self._HOST_IP, self._PORT))
            self._connected = True
        except:
            print("Failed to connect to host")

    def send_data(self, data: bytes) -> bool:
        """Sends data to the host"""
        is_data_sent = False
        try:
            self._CONNECTION.send(data)
            is_data_sent = True
        except:
            print("Failed to send data to host")
        return is_data_sent
    
    def retrieve_data(self, should_decode=False) -> bytes:
        """Returns the data recieved from the host as bytes"""
        data = self._CONNECTION.recv(self._TRANSFER_SIZE)
        if should_decode:
            data = data.decode(self._ENCODING_TYPE)
        return data
    

# Host To Client
ip = input("Enter ip of host: ")
server = NetworkHost(ip)
print("waiting for client to connect")
if server.is_connected:
    print("connected")
    server.send_command(NetworkCommands.MAKE_FILE, ["Adnan.txt"])
    print("sent")
    server.disconnect()
    print("closed connection")
else:
    print("Failed to connect to client")


# Client to Host

# client = NetworkClient(ip)
# if client.is_connected:
#     x = client.retrieve_data(True)
#     print(x)
#     client.disconnect()
#     print("closed connection")

