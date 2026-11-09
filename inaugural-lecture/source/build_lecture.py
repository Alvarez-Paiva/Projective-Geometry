#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
# © 2001, 2026 Juan Carlos Álvarez Paiva
"""Assemble the inaugural lecture in English, French and Spanish.

frame.html holds styles and scripts; body_{en,fr,es}.html hold the text, with
<!--APPLET name|caption--> placeholders.  The French and Spanish bodies take
the formula (<!--FORMULA-->) and the reference list (<!--REFS-->) from English.
"""
import json, re, sys, os

SRC = os.path.dirname(os.path.abspath(__file__)) if len(sys.argv) < 2 else sys.argv[1]
OUT = SRC if len(sys.argv) < 3 else sys.argv[2]
rd = lambda f: open(os.path.join(SRC, f), encoding='utf-8').read()

spec0 = json.load(open(os.path.join(SRC, 'spec.json')))
frame = rd('frame.html')
en = rd('body_en.html')
FORMULA = re.search(r'<math display="block">.*?</math>', en, re.S).group(0)
REFS = re.search(r'<ol class="refs">.*?</ol>', en, re.S).group(0)

FLAGS = {
 'en': '<svg viewBox="0 0 60 30" aria-hidden="true"><clipPath id="ukc"><path d="M0,0v30h60V0z"/></clipPath>'
       '<clipPath id="ukt"><path d="M30,15h30v15zv15H0zH0V0zV0h30z"/></clipPath><g clip-path="url(#ukc)">'
       '<path d="M0,0v30h60V0z" fill="#012169"/><path d="M0,0L60,30M60,0L0,30" stroke="#fff" stroke-width="6"/>'
       '<path d="M0,0L60,30M60,0L0,30" clip-path="url(#ukt)" stroke="#C8102E" stroke-width="4"/>'
       '<path d="M30,0v30M0,15h60" stroke="#fff" stroke-width="10"/>'
       '<path d="M30,0v30M0,15h60" stroke="#C8102E" stroke-width="6"/></g></svg>',
 'fr': '<svg viewBox="0 0 3 2" aria-hidden="true"><path fill="#002654" d="M0 0h1v2H0z"/>'
       '<path fill="#fff" d="M1 0h1v2H1z"/><path fill="#CE1126" d="M2 0h1v2H2z"/></svg>',
 'es': '<svg viewBox="0 0 3 2" aria-hidden="true"><path fill="#AA151B" d="M0 0h3v2H0z"/>'
       '<path fill="#F1BF00" d="M0 .5h3v1H0z"/></svg>',
}
NAMES = {'en': 'English', 'fr': 'Français', 'es': 'Español'}
FILES = {'en': 'index.html', 'fr': 'index-fr.html', 'es': 'index-es.html'}
# public address of the lecture folder (GitHub Pages)
BASE = 'https://alvarez-paiva.github.io/Projective-Geometry/inaugural-lecture/'
HOME = {'en': '← Projective geometry course', 'fr': '← Cours de géométrie projective',
        'es': '← Curso de geometría proyectiva'}

L = {
 'en': dict(title='Introduction to Projective Geometry',
            desc='Inaugural lecture of an interactive course on projective geometry, with live constructions.',
            reset='Reset', nav='Language',
            fail='The interactive figure could not load (CindyJS was not reached).', tr={}),
 'fr': dict(title='Introduction à la géométrie projective',
            desc='Leçon inaugurale d’un cours interactif de géométrie projective, avec des constructions animées.',
            reset='Réinitialiser', nav='Langue',
            fail='La figure interactive n’a pas pu se charger (CindyJS est inaccessible).',
            tr={'polar of P': 'polaire de P'}),
 'es': dict(title='Introducción a la geometría proyectiva',
            desc='Lección inaugural de un curso interactivo de geometría proyectiva, con construcciones animadas.',
            reset='Reiniciar', nav='Idioma',
            fail='La figura interactiva no pudo cargarse (no se pudo acceder a CindyJS).',
            tr={'polar of P': 'polar de P'}),
}

LANG_CSS = """
.langs { display: flex; gap: 14px; justify-content: flex-end; flex-wrap: wrap; font: 0.82rem/1 var(--ui); margin-bottom: 8px; }
.langs a, .langs span { display: inline-flex; align-items: center; gap: 6px; color: var(--muted); text-decoration: none; }
.langs a:hover { color: var(--ink, #222); text-decoration: underline; }
.langs span[aria-current] { color: var(--ink, #222); font-weight: 600; }
.langs a.home { margin-right: auto; }
.langs svg { width: 21px; height: 14px; border-radius: 2px; box-shadow: 0 0 0 1px rgba(0,0,0,.15); }
"""

def switcher(cur):
    items = [f'<a class="home" href="../">{HOME[cur]}</a>']
    for k in ('en', 'fr', 'es'):
        inner = FLAGS[k] + NAMES[k]
        if k == cur:
            items.append(f'<span lang="{k}" aria-current="page">{inner}</span>')
        else:
            items.append(f'<a href="{FILES[k]}" lang="{k}" hreflang="{k}">{inner}</a>')
    return f'<nav class="langs" aria-label="{L[cur]["nav"]}">' + ''.join(items) + '</nav>'

def block(spec, name, caption, reset, inline=False):
    a = spec[name]['aspect']
    inner = (f'<div class="board" style="aspect-ratio:{a:.4f}"><div id="cs-{name}"></div></div>'
             f'<div class="bar"><figcaption>{caption}</figcaption>'
             f'<button type="button" data-reset="{name}">{reset}</button></div>')
    tag = 'div' if inline else 'figure'
    return f'<{tag} class="applet" data-applet="{name}">{inner}</{tag}>'

for lang in ('en', 'fr', 'es'):
    c = L[lang]
    body = rd(f'body_{lang}.html').replace('<!--FORMULA-->', FORMULA).replace('<!--REFS-->', REFS)
    body = body.replace('<!--LANGS-->', switcher(lang))
    sj = json.dumps(spec0, separators=(',', ':'), ensure_ascii=False)
    for k, v in c['tr'].items():
        sj = sj.replace(json.dumps(k, ensure_ascii=False), json.dumps(v, ensure_ascii=False))
    spec = json.loads(sj)
    body = re.sub(r'<!--APPLET-INLINE (\w+)\|(.*?)-->', lambda m: block(spec, m.group(1), m.group(2), c['reset'], True), body, flags=re.S)
    body = re.sub(r'<!--APPLET (\w+)\|(.*?)-->', lambda m: block(spec, m.group(1), m.group(2), c['reset']), body, flags=re.S)
    html = frame.replace('<!--BODY-->', body)
    html = html.replace('<html lang="en">', f'<html lang="{lang}">')
    html = html.replace('<title>Introduction to Projective Geometry</title>', f'<title>{c["title"]}</title>')
    html = html.replace('content="Inaugural lecture of an interactive course on projective geometry, with live constructions."',
                        f'content="{c["desc"]}"')
    html = html.replace('The interactive figure could not load (CindyJS was not reached).', c['fail'].replace("'", "\\'"))
    url = lambda k: BASE + ('' if FILES[k] == 'index.html' else FILES[k])
    alts = (f'<link rel="canonical" href="{url(lang)}">\n'
            + ''.join(f'<link rel="alternate" hreflang="{k}" href="{url(k)}">\n' for k in FILES)
            + f'<link rel="alternate" hreflang="x-default" href="{url("en")}">\n'
            + f'<meta property="og:type" content="website">\n<meta property="og:url" content="{url(lang)}">\n'
            + f'<meta property="og:title" content="{c["title"]}">\n<meta property="og:description" content="{c["desc"]}">\n'
            + f'<meta property="og:image" content="{BASE}images/raphael.jpg">\n'
            + '<meta property="og:locale" content="' + {'en':'en_GB','fr':'fr_FR','es':'es_ES'}[lang] + '">')
    html = html.replace('</title>', '</title>\n' + alts, 1)
    html = html.replace('</style>', LANG_CSS + '</style>', 1)
    html = html.replace('/*SPEC*/null', sj)
    html = html.replace('<script src="https://cdn.jsdelivr.net/npm/cindyjs@0.0.5/build/js/Cindy.js"></script>',
        '<script src="https://cdn.jsdelivr.net/npm/cindyjs@0.0.5/build/js/Cindy.js"></script>\n'
        '<script>if (typeof CindyJS !== "function") document.write(\'<script src="Cindy.js"><\\/script>\');</script>')
    used = set(re.findall(r'data-applet="(\w+)"', html))
    assert '<!--' not in body or True
    print(lang, 'applets:', len(used), 'unused:', sorted(set(spec) - used),
          'leftover placeholders:', re.findall(r'<!--(APPLET|LANGS|FORMULA|REFS)', html))
    open(os.path.join(OUT, FILES[lang]), 'w', encoding='utf-8').write(html)
