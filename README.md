# TCP Port Scanner

A TCP port scanner written in Python, built incrementally to understand how TCP connections actually behave rather than just relying on a library to do the work.

## Current Features

* Scan a custom range of TCP ports
* Command-line arguments using `argparse`
* Port validation (`1–65535`)
* Connection timeout handling
* Detects:

  * `OPEN`
  * `CLOSED`
  * `TIMEOUT`
  * `ERROR`
* Measures scan time
* Uses `tcpdump` to observe TCP packets during experiments

## How It Works

For each port, the scanner creates a TCP socket and attempts:

```text
connect()
   |
   +-- success             → OPEN
   +-- ConnectionRefused   → CLOSED
   +-- Timeout             → TIMEOUT
   +-- other error         → ERROR
```

Sockets are closed using `finally` to make sure resources are cleaned up.

## Experiments

I used an Ubuntu VM in UTM as a controlled target to understand the difference between an open, closed, and filtered port.

### OPEN

A server is listening on the port.

```text
SYN → SYN-ACK → ACK
          ↓
        OPEN
```

### CLOSED

Nothing is listening on the port, so the host responds with a TCP reset.

```text
SYN → RST
       ↓
     CLOSED
```

### TIMEOUT

Traffic is silently dropped, so the scanner receives no response before its timeout.

```text
SYN → DROP
       ↓
   wait 2 seconds
       ↓
    TIMEOUT
```

I used `tcpdump` to verify that the timeout was actually caused by SYN packets being retransmitted without a response.

## Performance

Initial sequential scan on localhost:

| Ports   |    Time |
| ------- | ------: |
| 1–100   | 0.004 s |
| 1–1,000 | 0.034 s |
| 1–5,000 | 0.107 s |

Concurrency
The initial scanner checked ports sequentially. This becomes inefficient when connections take time to timeout.
I introduced ThreadPoolExecutor so multiple TCP connection attempts can happen concurrently.
Sequential:

port 1 → wait → port 2 → wait → port 3 → ...

Concurrent:

port 1 ─┐
port 2 ─┤
port 3 ─┤ → running at the same time
port 4 ─┘
Results are collected using as_completed(), so completed scans can be reported without waiting for earlier ports to finish.
I also experimented with different worker counts. Increasing the number of workers helps with I/O-bound scans, but using an unnecessarily large number of workers does not provide proportional speedup.
DNS Resolution
The scanner can accept a hostname instead of requiring an IP address.
DNS resolution happens once before the thread pool starts:
hostname
   ↓
DNS resolution
   ↓
IP address
   ↓
concurrent port scanning
DNS resolution time is measured separately from the actual port scan.
This keeps check_port() focused on one job: attempting a TCP connection to a specific IP address and port.
Performance
Initial sequential scan on localhost:
Ports	Time
1–100	0.004 s
1–1,000	0.034 s
1–5,000	0.107 s
The main reason for introducing concurrency was not fast localhost connections, but slow connections where each port may spend time waiting for a timeout.
Project Structure
port_scanner/

├── client.py
└── server.py
server.py is used as a controlled test server while developing and experimenting with the scanner.
Next
The next step is to investigate what happens after a TCP connection succeeds.
Currently the scanner can tell me:
Port 5000: OPEN
The next question is:
What service is actually running on that port?
The next experiment will be to send and receive application data using the test server and investigate how banner grabbing works.

