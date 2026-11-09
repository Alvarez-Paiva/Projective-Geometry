#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
# © 2001, 2026 Juan Carlos Álvarez Paiva
"""Translate Cinderella 1 constructions (.cdy, gzip-compressed "Cindy-1.0" scripts)
into CindyJS geometry specifications.  Usage: cdy2cindyjs.py APPLETDIR OUT.json"""
import gzip, json, re, sys, os

src, out = sys.argv[1], sys.argv[2]

# Cinderella 1 colour indices -> palette names used by the page
COLORS = {0: 'ink', 1: 'ink', 2: 'red', 3: 'blue', 4: 'green', 5: 'gold'}
OPS = {'FreePoint': 'Free', 'PointOnLine': 'PointOnLine', 'Join': 'Join', 'Meet': 'Meet',
       'ConicBy5': 'ConicBy5', 'PolarPoint': 'PolarOfPoint', 'PolarLine': 'PolarOfLine'}

def homog(s):
    """'[1.8+i*0.0,4.0+i*0.0,-0.95+i*-0.0]' -> real homogeneous coordinates"""
    parts = re.findall(r'(-?[\d.E-]+)\+i\*-?[\d.E-]+', s)
    x, y, z = [float(p) for p in parts]
    return [x, -y, z]          # Cinderella's y-axis points down

def params(html):
    p = dict(re.findall(r'name=(\w+)\s+value\s*=\s*"([^"]*)"', html))
    return {k: float(p[k]) for k in ('scale', 'originx', 'originy', 'width', 'height')}

applets = {}
for f in sorted(os.listdir(src)):
    if not f.endswith('.cdy'):
        continue
    name = f[:-4]
    text = gzip.open(os.path.join(src, f)).read().decode('latin-1')
    htmlname = 'pappus_applet.html' if name == 'pappus' else name + '.html'
    vp = params(open(os.path.join(src, htmlname), encoding='latin-1').read())
    els, app = [], {}
    for line in text.replace('\r\n', '\n').replace('\r', '\n').split('\n'):
        m = re.match(r'\("([^"]+)"\):=(\w+)\((.*)\);$', line)
        if m:
            nm, op, args = m.groups()
            el = {'name': nm}
            if op == 'LocusConic':           # locus of a point: use the conic it traces
                el.update(type='ConicBy5', args=['A', 'B', 'C', 'D', 'E'], locus=True)
            else:
                el['type'] = OPS[op]
                pos = re.search(r'\[.*\]', args)
                names = re.findall(r'"([^"]+)"', args)
                if pos:
                    el['pos'] = homog(pos.group(0))
                if names:
                    el['args'] = names
            els.append(el)
            continue
        m = re.match(r'"([^"]+)"\.setAppearance\((.*)\);', line)
        if m:
            a = m.group(2).split(',')
            app[m.group(1)] = {'color': COLORS.get(int(a[0]), 'ink'), 'size': int(a[1]),
                               'labeled': a[6].strip() == 'true'}
    for el in els:
        el.update(app.get(el['name'], {}))
    s, ox, oy, w, h = vp['scale'], vp['originx'], vp['originy'], vp['width'], vp['height']
    applets[name] = {'rect': [-ox/s, oy/s, (w-ox)/s, -(h-oy)/s], 'aspect': w/h,
                     'geometry': els}
json.dump(applets, open(out, 'w'), indent=1)
for k, v in applets.items():
    print(k, len(v['geometry']), [round(x, 2) for x in v['rect']])
