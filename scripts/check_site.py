"""Check portable assets, internal routes, gallery images, and contact contracts."""
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

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

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
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
    PageParser(page).feed(page.read_text())
for css in ROOT.glob('css/*.css'):
    for value in re.findall(r'url\([\s\'"]*([^\)\'"\s]+)', css.read_text()):
        check_ref(css, value)
names = [form['attrs']['name'] for form in forms]
assert len(forms) == 11, f'Expected 11 inquiry forms, got {len(forms)}'
assert len(set(names)) == len(names), 'Contact form names must be unique'
for form in forms:
    assert form['attrs']['method'] == 'post'
    assert form['attrs']['action'] == '/thank-you.html'
    assert form['captcha']
    assert {'Name', 'Phone', 'Email', 'City', 'Message', 'Budget', 'form-name', 'bot-field'} <= form['fields']
    assert form['fields'] & {'Service-Type', 'Service-Type-2'}
if errors:
    raise SystemExit('\n'.join(errors))
print(f'PASS: {len(pages)} pages, local assets, routes, gallery images, and {len(forms)} contact forms')
