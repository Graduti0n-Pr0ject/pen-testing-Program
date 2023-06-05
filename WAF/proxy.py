from mitmproxy import http
from mitmproxy.tools.main import mitmdump
import html

ip = ""
port = ""


def request(flow: http.HTTPFlow) -> None:
    """
    This method is called when a client makes a request to the server.
    """

    # Define a list of whitelisted IP addresses
    whitelist = ["10.0.0.1", "192.168.1.4"]

    # Get the client IP address from various headers or the connection itself
    client_ip = flow.request.headers.get("Client-IP", "")
    if not client_ip:
        client_ip = flow.request.headers.get("X-Real-IP", "")
    if not client_ip:
        client_ip = flow.client_conn.peername[0]

    # Check if the requested URL is /admin and if the client's IP address is in the whitelist
    if flow.request.path.startswith("/admin"):
        if client_ip not in whitelist:
            # If the client's IP address is not in the whitelist, create a new response object with status code 401
            # and change the response content to show an "Unauthorized" message
            headers = {"content-type": "text/plain"}
            content = b"Unauthorized"
            flow.response = http.Response.make(401, content, headers)
            return

    # Check if there are any GET parameters in the request
    if flow.request.method == "GET" and flow.request.query:
        # Define a list of blacklisted strings
        blacklist = ["<script>", "alert(", "document.cookie", "eval(", "javascript"]
        # Loop through each GET parameter to check for possible XSS
        for key, value in flow.request.query.items():
            # Check if the value contains any blacklisted strings
            if any(s in value for s in blacklist):
                # If a blacklisted string is detected, create a new response object with status code 404
                # and change the response content to show a "Hack detected" message
                headers = {"content-type": "text/html"}
                content = b"Hack detected"
                flow.response = http.Response.make(404, content, headers)
                return

    # Pass the request to the next layer
    flow.resume()


def response(flow: http.HTTPFlow) -> None:
    """
    This method is called when the server sends a response back to the client.
    """

    # Sanitize any GET parameters in the response HTML
    if "text/html" in flow.response.headers["content-type"]:
        content_bytes = flow.response.content
        content_str = content_bytes.decode("utf-8")
        sanitized_content_str = html.escape(content_str)
        flow.response.content = sanitized_content_str.encode("utf-8")

    # Add security headers if they don't already exist
    security_headers = {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "X-XSS-Protection": "1; mode=block",
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
        "Content-Security-Policy": "default-src 'self'; script-src 'self' https://example.com; object-src 'none'",
        "Referrer-Policy": "strict-origin-when-cross-origin",
        "Feature-Policy": "geolocation 'none'; camera 'none'"
    }

    for header_name, header_value in security_headers.items():
        if header_name not in flow.response.headers:
            flow.response.headers[header_name] = header_value


if __name__ == "__main__":
    # Configure mitmproxy to act as a reverse proxy for any app running on localhost:5000
    mitmdump(["-s", __file__, "-p", "5000", "--listen-host", ip, "--mode", "reverse:http://{ip}:{port}}"])
