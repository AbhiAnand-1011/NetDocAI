# DNS Troubleshooting

DNS translates domain names into IP addresses.

## Common Outcomes

### Successful Resolution

A hostname resolves when the DNS resolver returns one or more valid IP addresses.

Check both IPv4 and IPv6 when troubleshooting connectivity:

- A record -> IPv4 address
- AAAA record -> IPv6 address

### NXDOMAIN

NXDOMAIN means the queried domain name does not exist according to the DNS server.

Possible causes:
- Typo in hostname
- Missing DNS record
- Incorrect domain configuration

### SERVFAIL

SERVFAIL means the DNS server failed to provide a valid answer.

Possible causes:
- Upstream DNS failure
- DNSSEC validation failure
- Authoritative nameserver problems
- Temporary resolver problems

### DNS Timeouts

A timeout means the DNS query did not receive a response within the expected period.

Possible causes:
- Network connectivity problems
- Unreachable resolver
- Firewall filtering
- Resolver overload

### Troubleshooting

When investigating DNS problems:

1. Check whether the hostname resolves.
2. Check both A and AAAA records.
3. Measure DNS response time.
4. Compare results using another resolver.
5. Check whether the problem is intermittent or persistent.

DNS problems can appear as application failures even when TCP and HTTP connectivity are otherwise healthy.