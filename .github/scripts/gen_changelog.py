#!/usr/bin/env python3
"""
If version already exists in change_log.md, exit 0 without modification.
Usage: python .github/scripts/gen_changelog.py v4.10.9
"""
from __future__ import annotations
import sys, json, re, html, urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path

API_URL = "https://community.fit2cloud.com/v1/products/jumpserver/releases"
CHANGELOG = Path('docs/change_log.md')
MARKER = '# 更新日志'
TZ = timezone(timedelta(hours=8))

TITLE_MAP = {
    '功能': ('info', '新增功能 🌱', 'feat'),
    '优化': ('summary', '功能优化 🚀', 'perf'),
    '修复': ('success', '问题修复 🐛', 'fix'),
    "What's new": ('info', '新增功能 🌱', 'feat'),
    'Improvements': ('summary', '功能优化 🚀', 'perf'),
    'Bug fixes': ('success', '问题修复 🐛', 'fix'),
}
H2_UL = re.compile(r'<h2><a[^>]*></a>([^<]+)</h2>\n?(<ul>.*?</ul>)', re.S)
LI = re.compile(r'<li>(.*?)</li>', re.S)


def fetch():
    with urllib.request.urlopen(API_URL, timeout=30) as r:
        return json.loads(r.read().decode())


def normalize(v: str) -> str:
    return v.replace('-lts','')


def find_release(target: str, data):
    for rel in data:
        if normalize(rel.get('version','')) == target:
            return rel
    return None


def build_block(rel: dict):
    version = normalize(rel['version'])
    ts = rel.get('publishTime')
    dt = datetime.fromtimestamp(ts/1000, tz=TZ) if ts else datetime.now(tz=TZ)
    date_str = f"{dt.year}年{dt.month}月{dt.day}日"
    html_content = rel.get('releaseNoteH', '')
    sections = []
    for title, ul_html in H2_UL.findall(html_content):
        items = LI.findall(ul_html)
        cleaned = [html.unescape(re.sub(r'\s+',' ', re.sub(r'<[^>]+>','', it)).strip()) for it in items if it.strip()]
        if not cleaned:
            continue
        admon, nice, tag = TITLE_MAP.get(title, ('info', title, 'note'))
        lines = '\n'.join(f"    - {tag}: {i}" for i in cleaned)
        sections.append(f"!!! {admon} \"{nice}\"\n{lines}\n")
    if not sections:
        clean = html.unescape(re.sub(r'<[^>]+>','', html_content)).strip()
        if clean:
            sections.append(f"!!! info \"发布说明\"\n    - note: {clean}\n")
    block = '\n'.join([version, '------------------------', date_str, ''] + sections).rstrip() + '\n\n'
    return block


def main():
    if len(sys.argv) < 2:
        print('Version arg required, e.g. v4.10.9 or v4.10.9-lts or 4.10.9', file=sys.stderr)
        return 1
    raw = sys.argv[1].strip()
    # Accept forms: v4.10.9, v4.10.9-lts, 4.10.9, 4.10.9-lts
    if not raw.startswith('v'):
        raw = 'v' + raw
    target = normalize(raw)  # remove -lts suffix if present
    data = fetch()
    rel = find_release(target, data)
    if not rel:
        print(f'Target version {raw} (normalized {target}) not found in API list', file=sys.stderr)
        return 1
    if not CHANGELOG.exists():
        print('Changelog file missing.')
        return 1
    content = CHANGELOG.read_text(encoding='utf-8')
    if f"\n{target}\n" in content or content.startswith(target+'\n'):
        print('Version already exists, skip.')
        return 0
    block = build_block(rel)
    if MARKER in content:
        new_content = content.replace(MARKER, MARKER + '\n\n' + block, 1)
    else:
        new_content = MARKER + '\n\n' + block + content
    CHANGELOG.write_text(new_content, encoding='utf-8')
    print('Inserted changelog for', target)
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
