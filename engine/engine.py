"""Shared generator for Brik mini-sites.

Each site script builds a Site with its own theme, language, labels and nav,
then calls site.page(...) per page and site.finish(). Internal links in page
bodies are written as "@/<path>/" and resolved per page depth.
"""
import html, json, os, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
ROBOTS = '<meta name="robots" content="noindex, nofollow">'  # remove at launch


def fmt(n, sep=' '):
    return f'{n:,}'.replace(',', sep)


class Site:
    def __init__(self, *, domain, lang, out, utm, theme_css, fonts_href, logo, nav, labels,
                 footer_cols, footer_blurb, dir='ltr', updated='', date_iso='2026-11-24', sources=None):
        self.domain, self.lang, self.dir, self.out, self.utm = domain, lang, dir, out, utm
        self.theme_css, self.fonts_href, self.logo, self.nav = theme_css, fonts_href, logo, nav
        self.L, self.footer_cols, self.footer_blurb = labels, footer_cols, footer_blurb
        self.updated, self.date_iso, self.SRC = updated, date_iso, sources or {}
        if os.path.isdir(out):
            shutil.rmtree(out)
        os.makedirs(os.path.join(out, 'assets'))
        self.pages = []

    # ---------- helpers usable in bodies ----------
    def brik(self, content):
        return (f'https://real-estate-georgia.com/?utm_source={self.utm}'
                f'&amp;utm_medium=referral&amp;utm_campaign=minisite&amp;utm_content={content}')

    def a(self, target, text, cls=''):
        c = f' class="{cls}"' if cls else ''
        return f'<a{c} href="@/{target}index.html">{text}</a>'

    def related(self, items):
        return '<div class="related">' + ''.join(self.a(t, n) for t, n in items) + '</div>'

    def cta(self, content, title, text, button):
        return (f'<section class="band" style="padding-top:0"><div class="wrap"><div class="cta"><div><h2>{title}</h2><p>{text}</p></div>'
                f'<a class="btn" href="{self.brik(content)}">{button}</a></div></div></section>')

    def facts(self, items, three=False):
        cls = 'facts three band' if three else 'facts band'
        inner = ''.join(f'<div class="fact"><b>{b}</b><span>{s}</span><small>{m}</small></div>' for b, s, m in items)
        return f'<section class="{cls}" aria-label="{self.L["facts_label"]}"><div class="wrap">{inner}</div></section>'

    def rows(self, items, mx, highlight=None):
        """items: (name, sub, value, label, link_target_or_None)"""
        out = []
        for name, sub, v, label, target in items:
            cls = 'row hl' if highlight and name == highlight else 'row'
            inner = (f'<div class="nm"><b>{name}</b><span>{sub}</span></div>'
                     f'<div class="bar" aria-hidden="true"><i data-w="{min(v / mx * 100, 100):.1f}"></i></div><div class="v">{label}</div>')
            out.append(f'<a class="{cls}" href="@/{target}index.html">{inner}</a>' if target else f'<div class="{cls}">{inner}</div>')
        return '<div class="rows">' + ''.join(out) + '</div>'

    def lead_form(self, fields_html):
        return (f'<form data-draft novalidate>{fields_html}<button class="btn" type="submit">{self.L["submit"]}</button>'
                f'<div class="ok" role="status">{self.L["form_draft"]}</div></form>')

    def sources(self, keys):
        items = ''.join(f'<li><a href="{self.SRC[k][1]}">{self.SRC[k][0]}</a></li>' for k in keys)
        return (f'<section class="band" style="padding-top:0"><div class="wrap"><h2 style="font-size:20px">{self.L["sources"]}</h2>'
                f'<ul class="sources">{items}</ul><p class="sub">{self.L["sources_note"]}</p></div></section>')

    # ---------- page ----------
    def page(self, path, title, desc, crumbs, body, h1=None, lede=None, srcs=None, head_extra=''):
        depth = path.count('/')
        up = '../' * depth
        Lk = lambda t: up + t + 'index.html'
        nav = ''.join(
            f'<a href="{Lk(t)}"' + (' aria-current="page"' if (t == path or (t and path.startswith(t))) and (t or not path) else '') + f'>{n}</a>'
            for t, n in self.nav)
        crumb_html = ''
        ld_items = [{'@type': 'ListItem', 'position': 1, 'name': self.L['home'], 'item': self.domain + '/'}]
        if crumbs:
            parts = [f'<a href="{Lk("")}">{self.L["home"]}</a>']
            for i, (t, n) in enumerate(crumbs):
                ld_items.append({'@type': 'ListItem', 'position': i + 2, 'name': n, 'item': f'{self.domain}/{t}'})
                parts.append(f'<a href="{Lk(t)}">{n}</a>' if t != path else f'<span aria-current="page">{n}</span>')
            crumb_html = f'<nav class="crumbs" aria-label="{self.L["crumbs"]}">' + ' / '.join(parts) + '</nav>'
        ld = json.dumps([
            {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': ld_items},
            {'@context': 'https://schema.org', '@type': 'Article', 'headline': h1 or title, 'inLanguage': self.lang,
             'dateModified': self.date_iso, 'publisher': {'@type': 'Organization', 'name': 'Brik', 'url': 'https://real-estate-georgia.com'}}
        ], ensure_ascii=False)
        head_band = ''
        if h1:
            head_band = (f'<section class="band pagehead"><div class="wrap">{crumb_html}<h1>{h1}</h1>'
                         + (f'<p class="lede">{lede}</p>' if lede else '')
                         + f'<p class="updated">{self.L["updated"]}: {self.updated}</p></div></section>')
        cols = ''.join(f'<div><p><b>{t}</b></p><ul>' + ''.join(f'<li><a href="{Lk(x)}">{n}</a></li>' for x, n in items) + '</ul></div>'
                       for t, items in self.footer_cols)
        doc = f'''<!DOCTYPE html>
<html lang="{self.lang}" dir="{self.dir}">
<head>
<meta charset="utf-8">
{ROBOTS}
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{self.domain}/{path}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{self.fonts_href}" rel="stylesheet">
<link rel="stylesheet" href="{up}assets/site.css">
<script type="application/ld+json">{ld}</script>{head_extra}
</head>
<body>
<div class="draft">{self.L["draft"]}</div>
<header class="top"><div class="wrap"><a class="logo" href="{Lk("")}">{self.logo}</a><nav class="scroll" aria-label="{self.L["nav"]}">{nav}</nav></div></header>
<main>
{head_band}
{body}
{self.sources(srcs) if srcs else ''}
</main>
<footer class="band"><div class="wrap"><div class="cols">
<div><p>{self.footer_blurb.replace("{BRIK}", self.brik("footer"))}</p><p>{self.L["disclaimer"]}</p></div>
{cols}
</div></div></footer>
<script src="{up}assets/site.js"></script>
</body>
</html>
'''.replace('@/', up)
        dest = os.path.join(self.out, path, 'index.html')
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, 'w', encoding='utf-8') as f:
            f.write(doc)
        self.pages.append(path)

    def finish(self):
        with open(os.path.join(HERE, 'base.css'), encoding='utf-8') as f:
            base = f.read()
        with open(os.path.join(self.out, 'assets', 'site.css'), 'w', encoding='utf-8') as f:
            f.write(self.theme_css.strip() + '\n' + base)
        shutil.copy(os.path.join(HERE, 'site.js'), os.path.join(self.out, 'assets', 'site.js'))
        print(self.domain, 'pages:', len(self.pages))
