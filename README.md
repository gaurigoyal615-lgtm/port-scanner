# TCP Port Scanner

A TCP port scanner written in Python to understand TCP connection behavior, timeouts, concurrency, and basic application-layer communication.

## Features

* Scan a custom TCP port range
* Hostname resolution using DNS
* Detect:

  * `OPEN`
  * `CLOSED`
  * `TIMEOUT`
  * `ERROR`
* Configurable connection timeout
* Concurrent scanning using `ThreadPoolExecutor`
* Measures DNS resolution and scan time separately
* Collects application-layer responses from open ports
* Input validation for ports, timeout, and worker count

## Implementation

For each port, the scanner:

```text
Create socket
      ↓
Set timeout
      ↓
TCP connect()
      ↓
┌───────────────┬──────────────────┬──────────────┐
│ Connection    │ Connection       │ No response  │
│ succeeds      │ refused         │ before timeout│
│ → OPEN        │ → CLOSED        │ → TIMEOUT     │
└───────────────┴──────────────────┴──────────────┘
```

Sockets are closed using `finally` to ensure resources are released.

## Concurrency

`ThreadPoolExecutor` is used because port scanning is primarily I/O-bound.

* Each port scan is submitted as a separate task.
* `max_workers` controls the number of concurrent scans.
* `as_completed()` reports results as individual scans finish.
* Increasing workers improves performance for slow/timeout-heavy scans, but excessive concurrency does not provide proportional gains.

## DNS Resolution

Hostnames are resolved once before scanning:

```text
Hostname → DNS resolution → IP address → Port scanning
```

DNS resolution time is measured separately from the actual scan.

## Network Experiments

An Ubuntu VM was used as a controlled target.

### Open port

A listening service produces a successful TCP connection:

```text
SYN → SYN-ACK → ACK
```

### Closed port

A port with no listening service returns a TCP reset:

```text
SYN → RST
```

### Timeout

When packets are silently dropped, no response is received before the configured timeout:

```text
SYN → no response → TIMEOUT
```

`tcpdump` was used to verify SYN packets and retransmissions during timeout experiments.

## Application-Layer Experiment

A simple test server was used to understand data transfer after a TCP connection.

```text
connect()
   ↓
send()
   ↓
recv()
   ↓
raw bytes
```

The scanner can collect responses such as:

```text
b'HELLO FROM THE TEST SERVER'
```

An HTTP probe was also tested against Nginx to demonstrate that an open TCP port may require an application-layer request before returning data.

Comprehensive service/version detection is intentionally outside the scope of this project.

## Performance

Initial localhost measurements:

| Port Range |    Time |
| ---------- | ------: |
| 1–100      | 0.004 s |
| 1–1,000    | 0.034 s |
| 1–5,000    | 0.107 s |

## Project Structure

```text
port_scanner/
├── client.py
└── server.py
```

`server.py` is used as a controlled test server during development.
