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

    print(options)

main()
