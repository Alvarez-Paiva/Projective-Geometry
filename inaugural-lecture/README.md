# Introduction to Projective Geometry (inaugural lecture, 2026 edition)

Online: https://alvarez-paiva.github.io/Projective-Geometry/inaugural-lecture/

Open `index.html` (English), `index-fr.html` (français) or `index-es.html` (español) in a browser, or copy this folder to any web server (it is a static site).

- The 12 interactive figures run on CindyJS, loaded from the jsDelivr CDN; `Cindy.js` is a
  local copy used when the CDN cannot be reached (e.g. offline).
- The constructions were translated from the original Cinderella files
  (`web_projective-geometry/Inaugural-Lecture/applets/*.cdy`) by `source/cdy2cindyjs.py`.
- `source/lecture_spec.py` adds labels, colors and highlighting; `source/frame.html` holds
  the styles and scripts, `source/body_en.html`, `body_fr.html`, `body_es.html` hold the text
  in each language; `source/build_lecture.py` assembles the three pages, each with a
  language switcher (flags) linking to the others.
- The diagrams in `svg/` were converted from the original XFig files to MetaPost
  (with `book/fig2mp.py`) and output as SVG by `mpost`.

Rebuild after editing the text or the overrides (run inside `source/`, with the original
applets folder path as argument):

    python3 cdy2cindyjs.py <path>/Inaugural-Lecture/applets applets.json
    python3 lecture_spec.py
    python3 build_lecture.py . ..

## License

© 2001, 2026 Juan Carlos Álvarez Paiva. Text and figures: CC BY-SA 4.0; scripts: GNU GPL v3 or later;
CindyJS: Apache 2.0; paintings: public domain. See `../LICENSE.md` and `../LICENSES/`.
