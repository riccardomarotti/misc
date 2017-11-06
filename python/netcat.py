import sys
import socket
import getopt
import threading
import subprocess


def client_sender(options):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((options['target'], options['port']))

        buffer = sys.stdin.read()

        while True:
            if len(buffer):
                client.send(buffer.encode())

            recv_len = 4096
            response = ""

            while recv_len >= 4096:
                data = client.recv(4096)
                recv_len = len(data)
                response += data.decode()

            print(response),
            buffer = raw_input()
    except:
        print(sys.exc_info())
        print("[*] Exiting.")
        client.close()


def run_command(command):
    command = command.rstrip()

    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except:
        output = "Failed to execute command.\r\n"

    return output


def client_handler(client_socket, options):
    upload_destination = options['upload_destination']
    if len(upload_destination):
        file_buffer = ""

        for data in iter(client_socket.recv(4096)):
            file_buffer += data

        try:
            file_descriptor = open(upload_destination, "wb")
            file_descriptor.write(file_buffer)
            file_descriptor.close()
            client_socket.send("Successfully saved file to %s\r\n" % upload_destination)
        except:
            client_socket.send("Failed to save file to %s\r\n" % upload_destination)

    if len(options['execute']):
        output = run_command(options['execute'])
        client_socket.send(output)

    if options['command']:
        while True:
            client_socket.send(">".encode())

            cmd_buffer = ""
            for data in iter(client_socket.recv(1024)):
                cmd_buffer += data.encode()

            response = run_command(cmd_buffer)
            client_socket.send(response)




def server_loop(options):
    if not len(options['target']):
        options['target'] = "0.0.0.0"

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((options['target'], options['port']))
    server.listen(5)

    while True:
        client_socket, addr = server.accept()
        print("Accepted connection from %s" % str(addr))
        client_thread = threading.Thread(target=client_handler, args=(client_socket, options))
        client_thread.start()



def usage():
    print("Net Tool")
    print()
    print( "Usage: netcat.py -t target_host -p port")
    print("-l --listen              - listen on [host]:[port] for incoming connections")
    print("-e --execute=file_to_run - execute the given file upon receiving a connection")
    print("-c --command             - initialize a command shell")
    print("-u --upload=destination  - upon receiving connection upload a file and write to [destination]")
    print()
    print()
    print("Examples: ")
    print("netcat.py -t 192.168.0.1 -p 5555 -l -c")
    print("netcat.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe")
    print("netcat.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\"")
    print("echo 'ABCDEFGHI' | ./netcat.py -t 192.168.11.12 -p 135")
    sys.exit(0)

def option_error(option, value):
    print("Unhandled option '%s'" % option)
    sys.exit(-1);


def main():
    options = {
        'listen': False,
        'command': False,
        'upload': False,
        'execute': "",
        'target': "",
        'upload_destination': "",
        'port': 0,
    }

    if not len(sys.argv[1:]):
        usage()

    try:
        opts, args = getopt.getopt(sys.argv[1:],"hle:t:p:cu:",
        ["help","listen","execute","target","port","command","upload"])

    except getopt.GetoptError as err:
        print(str(err))
        usage()

    actions = {}
    actions.update(dict.fromkeys(['-h', '--help'], lambda unused: usage()))
    actions.update(dict.fromkeys(['-l', '--listen'], lambda unused: options.update({'listen': True})))
    actions.update(dict.fromkeys(['-e', '--execute'], lambda argument: options.update({'execute': argument})))
    actions.update(dict.fromkeys(['-c', '--commandshell'], lambda unused: options.update({'command': True})))
    actions.update(dict.fromkeys(['-u', '--upload'], lambda argument: options.update({'upload_destination': argument})))
    actions.update(dict.fromkeys(['-t', '--target'], lambda argument: options.update({'target': argument})))
    actions.update(dict.fromkeys(['-p', '--port'], lambda argument: options.update({'port': int(argument)})))


    for option, argument in opts:
        actions.get(option, lambda argument: option_error(option, argument))(argument)

    if not options['listen'] and len(options['target']) and options['port'] > 0:
        client_sender(options)

    if options['listen']:
        server_loop(options)


main()
