#!/usr/bin/env python
import socket, struct, time

FAKE = "Thu Mar 19 10:52:53 2021"   # You can change this
fake_ts = int(time.mktime(time.strptime(FAKE, "%a %b %d %H:%M:%S %Y")))
ntp_ts = fake_ts + 2208988800  # Convert Unix NTP epoch

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", 123))

while True:
    data, addr = sock.recvfrom(48)
    if len(data) >= 48:
        # LI=0, Version=4, Mode=4
        first_byte = (0 << 6) | (4 << 3) | 4
        response = struct.pack(
            "!B B B b 11I",
            first_byte,     # LI/VN/Mode
            1,              # Stratum
            0,              # Poll
            0,              # Precision
            0,              # Root Delay
            0,              # Root Dispersion
            0,              # Reference ID
            ntp_ts,         # Reference Timestamp
            0,              # Reference Fraction
            ntp_ts,         # Originate Timestamp
            0,
            ntp_ts,         # Receive Timestamp
            0,
            ntp_ts,         # Transmit Timestamp
            0,
        )
        sock.sendto(response, addr)
