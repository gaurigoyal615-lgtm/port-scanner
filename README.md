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

The next goal is to understand whether concurrency can significantly improve scans involving slow connections and timeouts.

## Project Structure

```text
port_scanner/
├── client.py
└── server.py
```

## Next

* Learn `ThreadPoolExecutor`
* Build a concurrent version
* Compare sequential vs concurrent performance
* Improve result handling and scanner design
