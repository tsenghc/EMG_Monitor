import socket
import binascii
import time
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

PORT = 1234

s.bind(('0.0.0.0', PORT))
print('Listening for broadcast at ', s.getsockname())
tt = ""
count = 0
start_time = time.time()
while True:
    data, address = s.recvfrom(1024)
    count += 1
    now = time.time()
    
    print(count/(now-start_time))
    # print(data.decode().split(" "))

    # val = data.hex()
    # print('Server received from {}:{}'.format(address, val))
