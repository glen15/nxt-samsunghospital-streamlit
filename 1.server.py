from http.server import HTTPServer, BaseHTTPRequestHandler
import subprocess

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

def get_public_ip():
    try:
        result = subprocess.run(
            ['curl', '-s', 'ifconfig.me'],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.stdout.strip()
    except:
        return "Public IP를 가져올 수 없음"

public_ip = get_public_ip()

print(f"서버가 시작되었습니다! 아래 링크를 클릭해주세요.")
print(f"접속 URL: http://{public_ip}:{port}")

HTTPServer(("", port), Handler).serve_forever()
