import datetime
import socket
from dnslib import DNSRecord, DNSHeader, RR, A

DEFAULT_IP = "192.0.2.1"
PORT = 53
BUFFER_SIZE = 512
LOG_FILE = "/tmp/lookups.txt"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('0.0.0.0', PORT))

print("Listening for DNS requests")

while True:
    try:
        data, addr = sock.recvfrom(BUFFER_SIZE)
        print(f"Request from {addr}")
        try:
            dns_record = DNSRecord.parse(data)
            qname = dns_record.q.qname
            qtype = dns_record.q.qtype
            timestamp = datetime.datetime.now(datetime.UTC)
            log_entry = f"[{timestamp}] {addr[0]} -> {qname}"

            print(log_entry)
            with open(LOG_FILE, "a") as f:
                f.write(f"{qname}\n")

            # Create a DNS response
            reply = DNSRecord(DNSHeader(id=dns_record.header.id, qr=1, aa=1, ra=1), q=dns_record.q)
            reply.add_answer(RR(qname, rtype=qtype, rclass=1, ttl=300, rdata=A(DEFAULT_IP)))

            sock.sendto(reply.pack(), addr)

        except Exception as e:
            print(f"Failed to parse DNS request: {e}")
            continue
    except KeyboardInterrupt:
        print("\nShutting down.")
        break
    except Exception as e:
        print(f"Error: {e}")
