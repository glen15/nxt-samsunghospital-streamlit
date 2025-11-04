from http.server import HTTPServer, BaseHTTPRequestHandler

username = "User"
port = 8080


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(f"{username}의 서버 {port} 포트에서 실행중 !!".encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write("Not Found".encode())


HTTPServer(("", port), Handler).serve_forever()
