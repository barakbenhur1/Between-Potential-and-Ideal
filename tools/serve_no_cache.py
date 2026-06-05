#!/usr/bin/env python3
"""Serve the repository locally without browser caching.

Run from the repository root:
    python3 tools/serve_no_cache.py

Then open:
    http://localhost:8000/site/en.html
    http://localhost:8000/site/index.html
"""

from __future__ import annotations

import argparse
import http.server
import socketserver
from pathlib import Path


class NoCacheRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Simple static-file handler that disables all browser/proxy caching."""

    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()


def main() -> None:
    parser = argparse.ArgumentParser(description="Serve the BPI repository with caching disabled.")
    parser.add_argument("--port", type=int, default=8000, help="Port to use (default: 8000)")
    parser.add_argument(
        "--directory",
        default=".",
        help="Directory to serve (default: repository root / current directory)",
    )
    args = parser.parse_args()

    directory = Path(args.directory).resolve()
    if not directory.is_dir():
        raise SystemExit(f"Directory does not exist: {directory}")

    handler = lambda *handler_args, **handler_kwargs: NoCacheRequestHandler(
        *handler_args,
        directory=str(directory),
        **handler_kwargs,
    )

    with socketserver.ThreadingTCPServer(("", args.port), handler) as server:
        server.allow_reuse_address = True
        print(f"Serving {directory} at http://localhost:{args.port} with cache disabled")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped")


if __name__ == "__main__":
    main()
