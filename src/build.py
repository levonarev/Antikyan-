#!/usr/bin/env python3
"""Build the four language pages from src/template.html and src/i18n.json.

Run from anywhere:  python3 src/build.py
Writes index.html (English), hy/index.html, it/index.html and ru/index.html.
Edit the text in i18n.json and the layout in template.html, never the output.
"""
import json
import re
from pathlib import Path

SRC = Path(__file__).resolve().parent
SITE = SRC.parent
BASE = "https://antikyan.com/"

# code -> (folder, label in the switcher)
LANGS = {
    "hy": ("hy/", "ՀԱՅ"),
    "en": ("", "EN"),
    "it": ("it/", "IT"),
    "ru": ("ru/", "РУ"),
}
BRUNI_INDEX = 3  # position of Bruno Bruni in every artists list

template = (SRC / "template.html").read_text(encoding="utf-8")
strings = json.loads((SRC / "i18n.json").read_text(encoding="utf-8"))

keys = set(strings["en"])
for code in LANGS:
    if set(strings[code]) != keys:
        raise SystemExit(f"{code}: keys differ from en: {set(strings[code]) ^ keys}")

hreflang = "\n".join(
    f'<link rel="alternate" hreflang="{c}" href="{BASE}{folder}">'
    for c, (folder, _) in LANGS.items()
) + f'\n<link rel="alternate" hreflang="x-default" href="{BASE}">'

for code, (folder, _) in LANGS.items():
    s = dict(strings[code])
    root = "../" if folder else ""
    s["artists"] = "\n".join(
        f'      <li>{name}'
        + (f' <small>{s["italy"]}</small>' if i == BRUNI_INDEX else "")
        + "</li>"
        for i, name in enumerate(s["artists"])
    )
    s["langs"] = "\n".join(
        f'      <li><a href="{root}{f}" lang="{c}" hreflang="{c}"'
        + (' aria-current="page"' if c == code else "")
        + f">{label}</a></li>"
        for c, (f, label) in LANGS.items()
    )
    s.update(lang=code, root=root, url=BASE + folder, hreflang=hreflang)

    def fill(match):
        return s[match.group(1)]

    html = re.sub(r"\{\{(\w+)\}\}", fill, template)
    out = SITE / folder / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print("wrote", out.relative_to(SITE))
