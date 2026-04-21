#!/usr/bin/env python3
"""Simple HTTP server that properly handles special characters in filenames."""

import http.server
import socketserver
import os
import sys
from urllib.parse import unquote

PORT = 8000

class BetterHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP请求处理器，正确处理URL中的特殊字符。"""
    
    def translate_path(self, path):
        """将URL路径转换为文件系统路径。"""
        # 解码URL编码的字符
        path = unquote(path)
        # 调用父类方法转换路径
        return super().translate_path(path)
    
    def end_headers(self):
        """添加CORS头以允许本地开发。"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

if __name__ == '__main__':
    # 切换到脚本所在目录
    os.chdir(os.path.dirname(os.path.abspath(__file__)) or '.')
    
    with socketserver.TCPServer(("", PORT), BetterHTTPRequestHandler) as httpd:
        print(f"Server running at http://localhost:{PORT}")
        print(f"Serving files from: {os.getcwd()}")
        print("Press Ctrl+C to stop")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")
            httpd.server_close()
