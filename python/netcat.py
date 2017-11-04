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
    print("Setting option %s to %s" % (option_to_set, value))
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
        '-h': lambda a: usage(),
        '--help': lambda a: usage(),
        '-l': lambda a: setOption(options, 'listen', True),
        '--listen': lambda a: setOption(options, 'listen', True),
        '-e': lambda a: setOption(options, 'execute', a),
        '--execute': lambda a: setOption(options, 'execute', a),
        '-c': lambda a: setOption(options, 'command', True),
        '--commandshell': lambda a: setOption(options, 'command', True),
        '-u': lambda a: setOption(options, 'upload_destination', a),
        '--upload': lambda a: setOption(options, 'upload_destination', a),
        '-t': lambda a: setOption(options, 'target', a),
        '--target': lambda a: setOption(options, 'target', a),
        '-p': lambda a: setOption(options, 'port', int(a)),
        '--port': lambda a: setOption(options, 'port', int(a)),
    }


    for o, a in opts:
        actions.get(o, lambda x: option_error(o, x))(a)

main()
