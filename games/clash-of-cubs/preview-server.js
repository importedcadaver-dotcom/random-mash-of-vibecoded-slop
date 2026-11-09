const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const root = __dirname;
const server = http.createServer((req, res) => {
  const pathname = new URL(req.url, 'http://127.0.0.1').pathname;
  const target = path.resolve(root, `.${decodeURIComponent(pathname === '/' ? '/index.html' : pathname)}`);
  if (!target.startsWith(root + path.sep)) { res.writeHead(403).end('Forbidden'); return; }
  fs.readFile(target, (error, bytes) => {
    if (error) { res.writeHead(404).end('Not found'); return; }
    const type = target.endsWith('.html') ? 'text/html; charset=utf-8' : target.endsWith('.js') ? 'text/javascript; charset=utf-8' : target.endsWith('.css') ? 'text/css; charset=utf-8' : 'text/plain; charset=utf-8';
    res.writeHead(200, { 'Content-Type': type, 'Cache-Control': 'no-store' }).end(bytes);
  });
});
server.listen(4173, '127.0.0.1', () => console.log('Clash of Cubs preview: http://127.0.0.1:4173'));

