#!/usr/bin/env python3
import socket
import struct
import time

# ===========================================================
# SET YOUR FAKE DATE HERE (any string you want)
# Example for your test:
FAKE = "Thu Mar 19 11:01:53 2021"
# ===========================================================

# Convert fake date to UNIX timestamp
unix_ts = int(time.mktime(time.strptime(FAKE, "%a %b %d %H:%M:%S %Y")))

# Convert UNIX to NTP epoch (starts 1900)
ntp_ts = unix_ts + 2208988800

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", 123))

print("Fake NTP server running on UDP/123...")
print("Serving:", FAKE)

while True:
    data, addr = sock.recvfrom(48)
    if data:
        # LI=0, Version=4, Mode=4 (server)
        LI = 0
        VN = 4
        MODE = 4
        first_byte = (LI << 6) | (VN << 3) | MODE

        pkt = struct.pack(
            "!B B B b 11I",
            first_byte,     # Flags
            1,              # Stratum
            0,              # Poll
            0,              # Precision
            0, 0, 0,        # Root delays & dispersion
            ntp_ts, 0,      # Reference timestamp
            ntp_ts, 0,      # Originate timestamp
            ntp_ts, 0,      # Receive timestamp
            ntp_ts, 0       # Transmit timestamp
        )

        sock.sendto(pkt, addr)
