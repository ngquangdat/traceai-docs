#!/usr/bin/env python3
"""Assemble traceai-slides.html from the deck sources and the Archify diagrams.

Each delivered diagram is gzipped and base64-encoded into a <script type="text/plain">
block; at runtime the deck inflates it and hands it to an iframe via srcdoc, so the
whole presentation stays a single self-contained file with no network access.
"""
import base64
import gzip
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DIAGRAMS = os.path.join(ROOT, 'diagrams')
PARTS = ['deck_head.html', 'deck_s1.html', 'deck_s2.html', 'deck_s3.html', 'deck_tail.html']
EMBEDDED = ['manual', 'architecture', 'sequence', 'dataflow']

html = ''.join(open(os.path.join(HERE, p), encoding='utf-8').read() for p in PARTS)

for name in EMBEDDED:
    raw = open(os.path.join(DIAGRAMS, name + '.html'), 'rb').read()
    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode='wb', compresslevel=9, mtime=0) as gz:
        gz.write(raw)
    payload = base64.b64encode(buf.getvalue()).decode('ascii')
    assert '</script' not in payload
    token = '__PAYLOAD_' + name.upper() + '__'
    assert token in html, 'missing slot for ' + name
    html = html.replace(token, payload)

assert '__PAYLOAD_' not in html, 'an unfilled payload slot remains'
out = os.path.join(ROOT, 'traceai-slides.html')
open(out, 'w', encoding='utf-8').write(html)
print('built %s (%d KB)' % (out, len(html) // 1024))
