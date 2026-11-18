"""Entry program for make.fun news-image-20261117 (Python 3.13, stdlib only).

The entry image is the entry.png beside this file: a front page drawn for
Tuesday 17 November 2026 by frontpage.py (the second edition: seventeen
stories, eight of them illustrated, with a map and the day in figures).
The program copies it, byte for byte, to the output directory the grader
provides, so both runs write identical bytes.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import hashlib
import os

HERE = os.path.dirname(os.path.abspath(__file__))


PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1048576
MAX_SIDE = 1024


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    with open(src, "rb") as fh:
        data = fh.read()
    if data[:8] != PNG_MAGIC:
        raise SystemExit("entry.png is not a PNG")
    if len(data) > MAX_BYTES:
        raise SystemExit("entry.png exceeds 1 MiB")
    width = int.from_bytes(data[16:20], "big")
    height = int.from_bytes(data[20:24], "big")
    if width > MAX_SIDE or height > MAX_SIDE:
        raise SystemExit("entry.png exceeds 1024x1024")
    dst = os.path.join(out_dir, "entry.png")
    with open(dst, "wb") as fh:
        fh.write(data)
    digest = hashlib.sha256(data).hexdigest()
    print("wrote", dst, len(data), "bytes", f"({width}x{height})",
          "sha256", digest)


if __name__ == "__main__":
    main()
