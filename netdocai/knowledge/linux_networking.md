# Linux Networking Troubleshooting

Linux provides several tools for investigating network connectivity.

## Ping

Ping measures ICMP reachability and round-trip latency.

Useful metrics include:

- Packet loss
- Minimum latency
- Average latency
- Maximum latency
- Jitter

Ping does not prove that TCP or HTTP services are working.

## DNS

Common commands include:

- getent hosts
- dig
- nslookup

Use DNS tools to determine whether hostname resolution is working correctly.

## TCP

Useful tools include:

- nc
- curl
- ss

A TCP connection test checks whether a destination port can be reached.

## HTTP

curl can be used to test HTTP and HTTPS endpoints and inspect:

- Status code
- Response headers
- Response timing

## Traceroute

Traceroute can help identify routing paths and where latency or packet loss may occur.

A single failed or missing traceroute hop does not necessarily mean that the network path is broken because routers may filter or deprioritize diagnostic traffic.