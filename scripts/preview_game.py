#!/usr/bin/env python3
"""Serve a static game locally, avoid busy ports, and open it in the browser."""

from __future__ import annotations

import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import webbrowser


DEFAULT_PORTS = (5173, 3000, 8080, 8000)
HOST = "127.0.0.1"


class QuietHandler(SimpleHTTPRequestHandler):
    """Suppress ordinary successful-request logging during a manual preview."""

    def log_message(self, format: str, *args: object) -> None:
        return


def start_preview_server(
    project: Path,
    preferred_ports: tuple[int, ...] = DEFAULT_PORTS,
) -> tuple[ThreadingHTTPServer, list[int]]:
    """Bind the first free loopback port, recording all occupied candidates."""
    if not (project / "index.html").is_file():
        raise FileNotFoundError(f"missing game entry point: {project / 'index.html'}")

    handler = partial(QuietHandler, directory=str(project))
    skipped_ports: list[int] = []
    for port in (*preferred_ports, 0):
        try:
            server = ThreadingHTTPServer((HOST, port), handler)
        except OSError:
            if port != 0:
                skipped_ports.append(port)
            continue
        return server, skipped_ports

    raise OSError("unable to bind a local preview port")


def preview_url(server: ThreadingHTTPServer) -> str:
    """Return the local URL for a bound preview server."""
    return f"http://{HOST}:{server.server_port}/"


def open_default_browser(url: str) -> bool:
    """Open the preview in the operating system's default browser."""
    return webbrowser.open(url, new=2, autoraise=True)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Open a static Web game with automatic port-conflict avoidance."
    )
    parser.add_argument(
        "--project",
        type=Path,
        required=True,
        help="directory containing game/index.html or another static game index.html",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=DEFAULT_PORTS[0],
        help="preferred port; busy ports automatically fall back to standard alternatives",
    )
    parser.add_argument(
        "--no-open",
        action="store_true",
        help="start the server but do not open a browser",
    )
    arguments = parser.parse_args()

    ports = (arguments.port,) + tuple(
        port for port in DEFAULT_PORTS if port != arguments.port
    )
    try:
        server, skipped_ports = start_preview_server(arguments.project, ports)
    except (FileNotFoundError, OSError) as exc:
        parser.error(str(exc))

    url = preview_url(server)
    if skipped_ports:
        print(f"Port conflict detected: skipped {', '.join(map(str, skipped_ports))}.")
    print(f"Preview ready: {url}")
    if not arguments.no_open:
        opened = open_default_browser(url)
        print("Opened the default browser." if opened else "Open the preview URL manually.")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Preview stopped.")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
