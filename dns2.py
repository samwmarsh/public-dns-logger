import datetime
import socket
from dnslib import DNSRecord, DNSHeader, RR, A, QTYPE, RCODE

DEFAULT_IP = "192.0.2.1"
ALLOWED_DOMAIN = ".blah.blah.net"
PORT = 53
BUFFER_SIZE = 512
LOG_FILE = "/tmp/lookups.txt"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('0.0.0.0', PORT))

print(f"DNS server listening on port {PORT}, responding to *{ALLOWED_DOMAIN} with {DEFAULT_IP}")

while True:
    try:
        data, addr = sock.recvfrom(BUFFER_SIZE)
        try:
            request = DNSRecord.parse(data)
            qname = str(request.q.qname).rstrip('.')
            qtype = QTYPE[request.q.qtype]

            timestamp = datetime.datetime.now().astimezone().isoformat()
            log_entry = f"[{timestamp}] {addr[0]} asked for {qname} ({qtype})"

            response = DNSRecord(DNSHeader(id=request.header.id, qr=1, aa=1, ra=1), q=request.q)

            if qtype == "A" and qname.endswith(ALLOWED_DOMAIN):
                response.add_answer(RR(qname, QTYPE.A, rclass=1, ttl=300, rdata=A(DEFAULT_IP)))
                print(f"{log_entry} -> {DEFAULT_IP}")
            else:
                response.header.rcode = RCODE.NXDOMAIN
                print(f"{log_entry} -> NXDOMAIN")

            with open(LOG_FILE, "a") as f:
                f.write(f"{log_entry}\n")

            sock.sendto(response.pack(), addr)

        except Exception as e:
            print(f"Failed to process DNS request from {addr}: {e}")
            continue

    except KeyboardInterrupt:
        print("\nShutting down DNS server.")
        break
    except Exception as e:
        print(f"Unexpected error: {e}")
