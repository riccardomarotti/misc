import socket

target_host = "localhost"
target_port = 9995

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((target_host, target_port))
request_string = "GET / HTTP/1.1\r\nHost:%s\r\n\r\n" % target_host
print(request_string)
client.send(request_string.encode())

print(client.recv(4096).decode())
