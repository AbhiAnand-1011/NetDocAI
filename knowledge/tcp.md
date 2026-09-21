# TCP Troubleshooting

TCP provides reliable, connection-oriented communication between applications.

## TCP Connection

A successful TCP connection indicates that a client was able to establish a connection to the destination host and port.

For HTTPS, the usual destination port is 443.

## Connection Failures

Common causes include:

- Destination service is not listening
- Firewall filtering
- Network routing problems
- Server unavailable
- Incorrect port

## Connection Latency

Measure the time required to establish a TCP connection.

High TCP connection latency can indicate:

- Network congestion
- Routing problems
- High server load
- Packet loss and retransmissions

## Troubleshooting

When investigating TCP problems:

1. Confirm the destination hostname resolves.
2. Attempt a TCP connection to the expected port.
3. Measure connection latency.
4. Compare results across repeated attempts.
5. Check whether failures are intermittent or persistent.

A successful TCP connection does not prove that the application itself is healthy.