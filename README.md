# public-dns-logger
Python server to accept and log DNS requests, useful for C2 exfil via DNS.

## Usage
```
$ python3 -m venv venv
$ source venv/bin/activate

$ python3 dns-logger.py
Listening for DNS requests
Request from ('X.X.X.X', 57120)
[2025-03-26 11:29:47.996554+00:00] X.X.X.X -> example.com.

$ tail -f /tmp/lookups.txt
[2025-03-26 11:29:47.996554+00:00] X.X.X.X -> example.com.
```
