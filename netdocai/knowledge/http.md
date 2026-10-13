# HTTP Troubleshooting

HTTP operates above the transport layer and is used by web applications and APIs.

## HTTP Status Codes

### 2xx

Successful request.

### 4xx

Client-side request error.

### 5xx

Server-side error.

## Response Time

HTTP response time measures how long the client waits for the server response.

High response time can result from:

- Slow application processing
- Slow upstream services
- Server overload
- Network latency
- Backend database delays

## Time To First Byte

TTFB measures the time until the first byte of the response is received.

High TTFB can indicate that the server or an upstream dependency is taking a long time to begin generating the response.

## Troubleshooting

When investigating HTTP slowness:

1. Check the HTTP status code.
2. Measure total response time.
3. Measure TTFB when available.
4. Compare multiple requests.
5. Compare HTTP and HTTPS behavior.
6. Determine whether the issue is persistent or intermittent.