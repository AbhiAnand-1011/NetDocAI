import socket
import subprocess
import time
from urllib.error import HTTPError
from urllib.request import Request, urlopen


def ping_host(host: str, count: int = 1) -> str:
    try:
        result = subprocess.run(
            ["ping", "-c", str(count), "-W", "2", host],
            capture_output=True,
            text=True,
            timeout=5,
        )

        if result.returncode == 0:
            return f"Ping successful for {host}.\n{result.stdout.strip()}"

        return f"Ping failed for {host}.\n{result.stderr.strip()}"

    except subprocess.TimeoutExpired:
        return f"Ping timed out for {host}."


def dns_lookup(host: str) -> str:
    try:
        addresses = socket.getaddrinfo(host, None)
        ips = sorted({address[4][0] for address in addresses})

        if not ips:
            return f"No IP addresses found for {host}."

        return f"DNS resolution successful for {host}:\n" + "\n".join(ips)

    except socket.gaierror as exc:
        return f"DNS resolution failed for {host}: {exc}"


def tcp_connect(host: str, port: int, timeout: float = 3.0) -> str:
    start = time.perf_counter()

    try:
        with socket.create_connection((host, port), timeout=timeout):
            latency_ms = (time.perf_counter() - start) * 1000

        return (
            f"TCP connection successful: {host}:{port}\n"
            f"Connection time: {latency_ms:.2f} ms"
        )

    except (socket.timeout, OSError) as exc:
        return f"TCP connection failed: {host}:{port}\nError: {exc}"


def http_request(url: str, timeout: float = 5.0) -> str:
    try:
        start = time.perf_counter()

        request = Request(
            url,
            headers={"User-Agent": "NetDocAI/1.0"},
        )

        with urlopen(request, timeout=timeout) as response:
            elapsed_ms = (time.perf_counter() - start) * 1000

            return (
                f"HTTP request successful\n"
                f"URL: {url}\n"
                f"Status: {response.status}\n"
                f"Content-Type: {response.headers.get('Content-Type')}\n"
                f"Response time: {elapsed_ms:.2f} ms"
            )

    except Exception as exc:
        return f"HTTP request failed for {url}\nError: {exc}"
