"""Minimal Chrome DevTools Protocol client (stdlib only): screenshot / evaluate on the page whose URL contains a substring.
usage: python cdp_shot.py <port> <url-substring> <out.png> [js-to-evaluate-first] [width height]"""
import sys, json, socket, base64, os, struct, urllib.request
port, sub, out = int(sys.argv[1]), sys.argv[2], sys.argv[3]
js = sys.argv[4] if len(sys.argv) > 4 else ''
W, H = (int(sys.argv[5]), int(sys.argv[6])) if len(sys.argv) > 6 else (1600, 900)
pages = json.loads(urllib.request.urlopen(f'http://127.0.0.1:{port}/json/list').read())
ws = next(p['webSocketDebuggerUrl'] for p in pages if sub in p['url'])
path = ws.split(str(port), 1)[1]
s = socket.create_connection(('127.0.0.1', port)); key = base64.b64encode(os.urandom(16)).decode()
s.send(f'GET {path} HTTP/1.1\r\nHost: 127.0.0.1:{port}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n'.encode())
buf = b''
while b'\r\n\r\n' not in buf: buf += s.recv(4096)
buf = buf.split(b'\r\n\r\n', 1)[1]
def send(obj):
    data = json.dumps(obj).encode(); mask = os.urandom(4); n = len(data)
    hdr = bytes([0x81]) + (bytes([0x80 | n]) if n < 126 else bytes([0x80 | 126]) + struct.pack('>H', n) if n < 65536 else bytes([0x80 | 127]) + struct.pack('>Q', n))
    s.send(hdr + mask + bytes(b ^ mask[i % 4] for i, b in enumerate(data)))
def recv_exact(n):
    global buf
    while len(buf) < n: buf += s.recv(1 << 20)
    d, buf = buf[:n], buf[n:]; return d
def recv():
    msg = b''
    while True:
        b0, b1 = recv_exact(2); n = b1 & 0x7f
        if n == 126: n = struct.unpack('>H', recv_exact(2))[0]
        elif n == 127: n = struct.unpack('>Q', recv_exact(8))[0]
        msg += recv_exact(n)
        if b0 & 0x80: return json.loads(msg)
i = 0
def call(method, **params):
    global i; i += 1; send({'id': i, 'method': method, 'params': params})
    while True:
        r = recv()
        if r.get('id') == i: return r
call('Emulation.setDeviceMetricsOverride', width=W, height=H, deviceScaleFactor=1, mobile=False)
if js:
    r = call('Runtime.evaluate', expression=js, awaitPromise=True, returnByValue=True); print('eval:', json.dumps(r.get('result', {}).get('result', {}).get('value'))[:2000])
r = call('Page.captureScreenshot', format='png')
open(out, 'wb').write(base64.b64decode(r['result']['data'])); print('saved', out)
