#!/usr/bin/env python3
"""Index supplied PDF pages; preserve page numbers and record limited scope."""
import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import unicodedata
from pathlib import Path


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def flatten(text):
    text = unicodedata.normalize('NFKC', text).replace('\u00ad', '')
    text = re.sub(r'(?<=\w)-\s*\n\s*(?=\w)', '', text)
    return re.sub(r'\s+', ' ', text).strip()


def extract(pdf):
    if shutil.which('pdftotext'):
        r = subprocess.run(['pdftotext', '-enc', 'UTF-8', str(pdf), '-'],
                           capture_output=True, text=True, timeout=60)
        if r.returncode:
            raise ValueError('PDF extraction failed: '+r.stderr[:300])
        pages = r.stdout.split('\f')
        if r.stdout.endswith('\f'):
            pages.pop()  # delimiter; do not discard genuine blank PDF pages
        return pages, 'pdftotext'
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise ValueError('Install poppler/pdftotext or pypdf') from exc
    return [p.extract_text() or '' for p in PdfReader(str(pdf)).pages], 'pypdf'


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('pdf')
    ap.add_argument('--out', required=True)
    ap.add_argument('--scope', choices=['provided_document', 'excerpt'], default='provided_document')
    ap.add_argument('--expected-pages', type=int)
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    pdf = Path(a.pdf)
    meta = {'schema_version':'2.0', 'source':pdf.name, 'scope':a.scope, 'status':'invalid_input',
            'scope_warning':'Only supplied pages are indexed; supplements and completeness are not assumed.'}
    try:
        if not pdf.is_file() or not pdf.read_bytes().startswith(b'%PDF-'):
            raise ValueError('Missing input or invalid PDF header')
        meta['sha256'] = digest(pdf)
        raw, engine = extract(pdf)
        if not raw:
            raise ValueError('No PDF pages')
        pages = [{'page':i, 'flat':flatten(s), 'chars':len(flatten(s))} for i,s in enumerate(raw,1)]
        (out/'pages.jsonl').write_text(''.join(json.dumps(p,ensure_ascii=False)+'\n' for p in pages))
        (out/'flat.txt').write_text('\n\f\n'.join(p['flat'] for p in pages))
        meta.update(engine=engine, pages=len(pages), chars=sum(p['chars'] for p in pages),
                    pages_with_little_text=[p['page'] for p in pages if p['chars']<40],
                    pages_sha256=digest(out/'pages.jsonl'), status='ok')
        if meta['chars']<40:
            meta.update(status='insufficient_text', reason='No usable text layer; request OCR or readable source')
        if a.expected_pages and a.expected_pages!=len(pages):
            meta.update(scope='excerpt', scope_warning='Page count differs from expectation; material is incomplete')
    except (ValueError,OSError,subprocess.SubprocessError) as exc:
        meta['reason']=str(exc)
    (out/'index.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(meta,ensure_ascii=False))
    return 0 if meta['status']=='ok' else 2


if __name__=='__main__':
    sys.exit(main())
