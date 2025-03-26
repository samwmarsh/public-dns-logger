import socket
from dnslib import DNSRecord
from datetime import datetime

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
         qname = str(dns_record.q.qname)
         timestamp = datetime.now(datetime.UTC)
         log_entry = f"[{timestamp}] {addr[0]} -> {qname}"

         print(log_entry)
         with open(LOG_FILE, "a") as f:
            f.write(f"{qname}\n")

      except Exception as e:
         print(f"Failed to parse DNS request: {e}")
         continue
      response = f"DNS response for {qname}: {DEFAULT_IP}"
      sock.sendto(response.encode(), addr)
   except KeyboardInterrupt:
      print("\nShutting down.")
      break
   except Exception as e:
      print(f"Error: {e}")
