#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
# © 2001, 2026 Juan Carlos Álvarez Paiva
"""Build the CindyJS specifications for the inaugural lecture from applets.json
(translated from the original Cinderella files) plus a few presentation overrides."""
import json, copy

d = json.load(open('./applets.json'))

# palette shared with the page (Giotto's ultramarine and vermilion, ink, gold)
PAL = {'ink': [0.13, 0.15, 0.19], 'red': [0.78, 0.25, 0.15], 'blue': [0.15, 0.29, 0.58],
       'green': [0.16, 0.47, 0.30], 'gold': [0.70, 0.52, 0.06], 'grey': [0.55, 0.58, 0.62],
       'result': [0.15, 0.29, 0.58]}
POINTS = ('Free', 'PointOnLine', 'Meet', 'PolarOfLine')

# per applet: printname (label shown), forced labels, results (emphasized), hidden, dashed
OVR = {
 'pappus': dict(print={'D': "A'", 'E': "B'", 'F': "C'"}, label='ABCDEF',
                result=['k', 'G', 'H', 'K']),
 'desargues': dict(print={'A': 'O'}, label='A', result=['l', 'H', 'K', 'L']),
 'trans': dict(print={'C': 'P', 'D': 'Q', 'b': 'm'}, label=['C', 'D', 'X', 'T(X)', 'b'],
               result=['T(X)']),
 'harmonic': dict(label='ABCD', result=['D'], dashed=['b', 'c', 'd', 'e', 'f', 'g'], recolor={'b': 'grey', 'c': 'grey', 'd': 'grey', 'e': 'grey', 'f': 'grey', 'g': 'grey', 'F': 'red', 'G': 'red'}),
 'pappus_dual': dict(print={'d': "a'", 'e': "b'", 'f': "c'"}, label='abcdef',
                     result=['g', 'h', 'k', 'L']),
 'first': dict(),
 'conic': dict(),
 'pascal': dict(print={'H': 'X'}, label=['A', 'B', 'C', 'D', 'E', 'F', 'H'], result=['e', 'F']),
 'construct': dict(print={'H': 'X'}, label=['A', 'B', 'C', 'D', 'E', 'F', 'H'], result=['e', 'F'],
                   trace=['F'], dashed=['C0']),
 'polarity': dict(print={'F': 'P', 'a': 'polar of P'}, label=['F', 'a'], result=['a']),
 'delahire': dict(print={'a': 'ℓ', 'K': 'L', 'b': 'polar of P', 'H': 'P'},
                  label=['a', 'K', 'b', 'H'], result=['K', 'b']),
}

# a new applet: the point at infinity (page 2), drawn after the figure of the original lecture
d['infinity'] = {'rect': [-6.5, 4.2, 8.5, -3.2], 'aspect': 15 / 7.4, 'geometry': [
    {'name': 'U', 'type': 'Free', 'pos': [0, 3.6, 1], 'color': 'grey', 'size': 0},
    {'name': 'V', 'type': 'Free', 'pos': [0, -2.8, 1], 'color': 'grey', 'size': 0},
    {'name': 'l', 'type': 'Join', 'args': ['U', 'V'], 'color': 'ink', 'size': 4},
    {'name': 'W', 'type': 'Free', 'pos': [-5.5, -1.8, 1], 'color': 'grey', 'size': 0},
    {'name': 'Z', 'type': 'Free', 'pos': [7.5, -1.8, 1], 'color': 'grey', 'size': 0},
    {'name': 'm', 'type': 'Join', 'args': ['W', 'Z'], 'color': 'ink', 'size': 4},
    {'name': 'P', 'type': 'Free', 'pos': [-3.5, 2.2, 1], 'color': 'red', 'size': 5},
    {'name': 'A', 'type': 'PointOnLine', 'args': ['l'], 'pos': [0, 0.8, 1], 'color': 'red', 'size': 5},
    {'name': 'p', 'type': 'Join', 'args': ['P', 'A'], 'color': 'ink', 'size': 2},
    {'name': "A'", 'type': 'Meet', 'args': ['p', 'm'], 'color': 'ink', 'size': 5},
    {'name': 'q', 'type': 'Para', 'args': ['m', 'P'], 'color': 'grey', 'size': 2},
    {'name': 'B', 'type': 'Meet', 'args': ['l', 'q'], 'color': 'ink', 'size': 4},
]}
OVR['infinity'] = dict(label=['P', 'A', "A'", 'B', 'l', 'm'], dashed=['q'], result=["A'"])

# start the slider X of the five-point construction on the visible part of BC
for e in d['construct']['geometry']:
    if e['name'] == 'H':
        e['pos'] = [2.99, 3.94, 1]

out = {}
for name, app in d.items():
    o = OVR.get(name, {})
    geo = []
    for e in app['geometry']:
        g = {k: e[k] for k in ('name', 'type', 'args', 'pos') if k in e}
        n = e['name']
        is_pt = e['type'] in POINTS
        col = e.get('color', 'ink')
        if col == 'blue':
            col = 'green'          # blue is reserved for what the theorem predicts
        size = e.get('size', 3)
        if is_pt:
            g['size'] = 2.5 if size == 0 else min(5.5, 2 + 0.7 * size)
            if size == 0:
                col = 'grey'
        else:
            g['size'] = 1 if size <= 2 else (1.4 if size == 3 else (1.7 if size == 4 else 2.2))
        col = o.get('recolor', {}).get(n, col)
        if n in o.get('result', []):
            col = 'result'
            g['size'] = (g['size'] + 1.5) if is_pt else 2.8
        g['color'] = PAL[col]
        if n in o.get('print', {}):
            g['printname'] = o['print'][n]
        if n in o.get('label', []) or (e.get('labeled') and not o.get('label')):
            g['labeled'] = True
        if n in o.get('dashed', []):
            g['dashtype'] = 1
            g['alpha'] = 0.6
        if n in o.get('trace', []):
            g['drawtrace'] = True
            g['tracelength'] = 600
            g['tracedim'] = 0.35
        if e.get('locus'):
            g['alpha'] = 0.45
        geo.append(g)
    out[name] = {'rect': app['rect'], 'aspect': app['aspect'], 'geometry': geo}

json.dump(out, open('./spec.json', 'w'))
print({k: len(v['geometry']) for k, v in out.items()})
