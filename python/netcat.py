import sys
import socket
import getopt
import threading
import subprocess

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

def setOption(all_options, option_to_set, value):
    all_options[option_to_set] = value

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


    actions = {
        '-h': lambda unused: usage(),
        '--help': lambda unused: usage(),
        '-l': lambda unused: setOption(options, 'listen', True),
        '--listen': lambda unused: setOption(options, 'listen', True),
        '-e': lambda argument: setOption(options, 'execute', argument),
        '--execute': lambda argument: setOption(options, 'execute', argument),
        '-c': lambda unused: setOption(options, 'command', True),
        '--commandshell': lambda unused: setOption(options, 'command', True),
        '-u': lambda argument: setOption(options, 'upload_destination', argument),
        '--upload': lambda argument: setOption(options, 'upload_destination', argument),
        '-t': lambda argument: setOption(options, 'target', argument),
        '--target': lambda argument: setOption(options, 'target', argument),
        '-p': lambda argument: setOption(options, 'port', int(argument)),
        '--port': lambda argument: setOption(options, 'port', int(argument)),
    }

    for option, argument in opts:
        actions.get(option, lambda argument: option_error(option, argument))(argument)


main()
