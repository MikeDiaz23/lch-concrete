"""Check portable assets, internal routes, gallery images, and contact contracts."""
import json
import subprocess
import sys
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1] / 'site'
errors = []
forms = []


def check_ref(page, value):
    url = urlsplit(value)
    if url.scheme or url.netloc or not url.path:
        return
    path = (ROOT / unquote(url.path).lstrip('/') if url.path.startswith('/')
            else page.parent / unquote(url.path)).resolve()
    if not path.is_relative_to(ROOT.resolve()):
        errors.append(f'{page.name}: reference outside site: {value}')
    elif not any(p.is_file() for p in [path, path.with_suffix('.html'), path / 'index.html']):
        errors.append(f'{page.relative_to(ROOT)}: missing {value}')


class PageParser(HTMLParser):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.gallery = False
        self.data = ''
        self.form = None
        self.ids = set()
        self.labels = []
        self.headings = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('id'):
            if attrs['id'] in self.ids:
                errors.append(f'{self.page.relative_to(ROOT)}: duplicate ID {attrs["id"]}')
            self.ids.add(attrs['id'])
        if tag == 'label' and attrs.get('for'):
            self.labels.append(attrs['for'])
        if tag == 'h1':
            self.headings += 1
        for key in ('href', 'src', 'action'):
            if key in attrs and attrs[key] != '/.wf_auth':
                check_ref(self.page, attrs[key])
        for item in attrs.get('srcset', '').split(','):
            if item.strip():
                check_ref(self.page, item.strip().split()[0])
        if tag == 'form' and attrs.get('data-contact-form'):
            self.form = {'attrs': attrs, 'fields': set(), 'captcha': False}
            forms.append(self.form)
        if self.form:
            if tag in ('input', 'select', 'textarea'):
                self.form['fields'].add(attrs.get('name'))
            if tag == 'div' and attrs.get('data-netlify-recaptcha') == 'true':
                self.form['captcha'] = True
        if tag == 'script' and attrs.get('class') == 'w-json':
            self.gallery = True
            self.data = ''

    def handle_data(self, data):
        if self.gallery:
            self.data += data

    def handle_endtag(self, tag):
        if tag == 'form':
            self.form = None
        if tag == 'script' and self.gallery:
            for item in json.loads(self.data).get('items', []):
                check_ref(self.page, item['url'])
            self.gallery = False


pages = list(ROOT.rglob('*.html'))
for page in pages:
    parser = PageParser(page)
    parser.feed(page.read_text())
    if parser.headings != 1:
        errors.append(f'{page.relative_to(ROOT)}: expected one main heading')
    for target in parser.labels:
        if target not in parser.ids:
            errors.append(f'{page.relative_to(ROOT)}: missing label target {target}')
for css in ROOT.glob('css/*.css'):
    for value in re.findall(r'url\([\s\'"]*([^\)\'"\s]+)', css.read_text()):
        check_ref(css, value)
names = [form['attrs']['name'] for form in forms]
area_data = json.loads((ROOT.parent / 'content/areas.json').read_text())
cities = area_data['cities']
assert 0 < len(cities) <= 14, 'Area pages must remain within the requested 14-city limit.'
assert len(forms) == 11 + len(cities), f'Expected original forms plus one per city, got {len(forms)}'
expected_area_forms = {'contact-area-' + city['slug'] for city in cities}
assert {f['attrs']['name'] for f in forms if f['attrs']['name'].startswith('contact-area-')} == expected_area_forms
assert {p.parent.name for p in (ROOT / 'areas').glob('*/index.html')} == {c['slug'] for c in cities}
canonical_urls = set()
for page in pages:
    source = page.read_text()
    nav = re.search(r'<div class="area-nav-cities">(.*?)</div>', source, re.S)
    assert nav, f'{page}: missing Areas menu'
    assert set(re.findall(r'href="([^"]+)"', nav.group(1))) == {'/areas/' + c['slug'] + '/' for c in cities}
    if page.name not in {'401.html', '404.html', 'thank-you.html'}:
        canonical = re.search(r'<link rel="canonical" href="([^"]+)"', source)
        assert canonical, f'{page}: missing canonical'
        assert canonical.group(1) not in canonical_urls, f'{page}: duplicate canonical'
        canonical_urls.add(canonical.group(1))
for city in cities:
    page = ROOT / 'areas' / city['slug'] / 'index.html'
    source = page.read_text()
    assert chr(0x2014) not in source, f'{page}: em dash in new content'
    assert city['radius_miles'] <= area_data['radius_miles']
    assert 'name="Area" value="' + city['name'] + '"' in source
    assert 'name="City" value="' + city['name'] + '"' in source
    assert 'name="description"' in source
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', source, re.S)
    graph = json.loads(blocks[0])['@graph']
    assert {'Service', 'BreadcrumbList'} <= {node['@type'] for node in graph}
    service = next(node for node in graph if node['@type'] == 'Service')
    assert service['areaServed']['name'] == city['name']
    assert service['provider']['@id'] == 'https://www.lchconcrete.com/#business'
sitemap = ET.parse(ROOT / 'sitemap.xml')
locations = {node.text for node in sitemap.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')}
assert locations == canonical_urls, 'Sitemap does not match indexable page canonicals.'
assert 'Sitemap: https://www.lchconcrete.com/sitemap.xml' in (ROOT / 'robots.txt').read_text()
assert len(set(names)) == len(names), 'Contact form names must be unique'
for form in forms:
    assert form['attrs']['method'] == 'post'
    assert form['attrs']['action'] == '/thank-you.html'
    assert form['captcha']
    assert {'Name', 'Phone', 'Email', 'City', 'Message', 'Budget', 'form-name', 'bot-field'} <= form['fields']
    assert form['fields'] & {'Service-Type', 'Service-Type-2'}
if errors:
    raise SystemExit('\n'.join(errors))
generated = subprocess.run([sys.executable, str(ROOT.parent / 'scripts/build_area_pages.py'), '--check'], capture_output=True, text=True)
if generated.returncode:
    raise SystemExit(generated.stdout + generated.stderr)
print(f'PASS: {len(pages)} pages, local assets, routes, gallery images, and {len(forms)} contact forms')
