from dnserver import DNSServer, DNSHandler
import socket

# The IP address to return for all matching domains
TARGET_IP = "192.168.1.100"

# The wildcard domain you want to match
WILDCARD_DOMAIN = ".BLAH.HOST.NET"

def handle_query(request: DNSHandler):
    qname = str(request.q.qname).rstrip('.')
    qtype = request.q.qtype

    # Log incoming query
    print(f"Received query: {qname} (type {qtype})")

    # Only respond to A (IPv4) queries and match the wildcard domain
    if qtype == 1 and qname.endswith(WILDCARD_DOMAIN):
        return {
            "type": "A",
            "ttl": 60,
            "rdata": TARGET_IP
        }
    else:
        # Return empty (NXDOMAIN) for non-matching domains
        return None

if __name__ == "__main__":
    print(f"Starting DNS server to resolve *{WILDCARD_DOMAIN} → {TARGET_IP}")
    DNSServer(handlers={"A": handle_query}).start()
