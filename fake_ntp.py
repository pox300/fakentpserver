#!/usr/bin/env python
import socket, struct, time
from datetime import datetime

# Your exact fake date here:
FAKE = "Thu Mar 19 09:40:53 2021"
fake_ts = int(time.mktime(time.strptime(FAKE, "%a %b %d %H:%M:%S %Y")))

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", 123))

while True:
    data, addr = sock.recvfrom(1024)
    if data:
        transmit = fake_ts + 2208988800  # Convert Unix → NTP epoch
        response = struct.pack("!BBBBIII4sQQQQ",
            0x1C, 0, 0, 0,  # LI/VN/Mode
            0, 0, 0, b"\0"*4,
            transmit << 32, 0, transmit << 32, 0
        )
        sock.sendto(response, addr)
