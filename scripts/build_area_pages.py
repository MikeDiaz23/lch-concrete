"""Build static area pages and synchronize their shared navigation. Standard library only."""
import argparse
import html
import json
import math
import re
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site'
DATA = json.loads((ROOT / 'content/areas.json').read_text())
CITIES = DATA['cities']
BASE = 'https://www.lchconcrete.com'
assert 0 < len(CITIES) <= 14, 'Keep the requested limit of at most 14 city pages.'
assert len({c['slug'] for c in CITIES}) == len(CITIES)
assert all(re.fullmatch(r'[a-z]+(?:-[a-z]+)*', c['slug']) for c in CITIES)
assert all(c['radius_miles'] <= DATA['radius_miles'] for c in CITIES)
CHECK = argparse.ArgumentParser()
CHECK.add_argument('--check', action='store_true', help='Report stale generated pages without writing.')
CHECK = CHECK.parse_args().check
STALE = []

def esc(value):
    return html.escape(str(value), quote=True)

def save(path, content):
    if path.exists() and path.read_text() == content:
        return
    if CHECK:
        STALE.append(str(path.relative_to(ROOT)))
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)

def city_url(city):
    return '/areas/' + city['slug'] + '/'

def city_links(current=None):
    return '\n'.join(
        '<a href="' + city_url(c) + '"' + (' aria-current="page"' if c['slug'] == current else '') + '>' + esc(c['name']) + '</a>'
        for c in CITIES)

def sync_shared(page, path):
    relative = path.relative_to(SITE)
    current = relative.parts[1] if len(relative.parts) == 3 and relative.parts[0] == 'areas' else None
    hub = relative.as_posix() == 'areas/index.html'
    menu = (
        '<details class="nav-drop area-nav-drop">\n'
        '<summary' + (' class="is-current"' if current or hub else '') + '>Areas</summary>\n'
        '<div class="nav-panel area-nav-panel">\n'
        '<a class="area-nav-overview" href="/areas/"' + (' aria-current="page"' if hub else '') + '>All service areas</a>\n'
        '<div class="area-nav-cities">\n' + city_links(current) + '\n</div>\n</div>\n</details>'
    )
    def update_nav(match):
        nav = re.sub(r'\n?<details class="nav-drop area-nav-drop">.*?</details>', '', match.group(), flags=re.S)
        first_end = nav.index('</details>') + len('</details>')
        return nav[:first_end] + '\n' + menu + nav[first_end:]
    page, count = re.subn(r'<nav class="site-nav"[^>]*>.*?</nav>', update_nav, page, count=1, flags=re.S)
    assert count == 1, path
    page = re.sub(r'<div class="cities-list">.*?</div>', '<div class="cities-list">\n' + city_links(current) + '\n</div>', page, flags=re.S)
    if '<a href="/areas/">Service areas</a>' not in page:
        page = page.replace('<a href="/contact.html">Contact us</a>', '<a href="/areas/">Service areas</a>\n<a href="/contact.html">Contact us</a>')
    page = re.sub(r'/js/modern.js(?:\?[^"]*)?', '/js/modern.js?v=areas-nav-1', page)
    page = re.sub(r'/css/responsive.css(?:\?[^"]*)?', '/css/responsive.css?v=areas-nav-1', page)
    if '/css/navigation.css' not in page:
        page = page.replace('</head>', '<link rel="stylesheet" href="/css/navigation.css?v=areas-1">\n</head>')
    return page

contact = (SITE / 'contact.html').read_text()
PREFIX = contact[:contact.index('<main id="main">')]
PREFIX = re.sub(r' aria-current="page"', '', PREFIX)
SUFFIX = contact[contact.index('</main>') + len('</main>'):]
FORM = re.search(r'<form id="wf-form-Message-Form".*?</form>', contact, re.S).group()

def start_page(title, description, path, body_class, schema):
    page = re.sub(r'<title>.*?</title>', '<title>' + esc(title) + '</title>', PREFIX, flags=re.S)
    values = {'description': description, 'og:title': title, 'twitter:title': title,
              'og:description': description, 'twitter:description': description}
    def meta(match):
        tag = match.group()
        key = re.search(r'(?:name|property)="([^"]+)"', tag)
        if key and key.group(1) in values:
            tag = re.sub(r'content="[^"]*"', 'content="' + esc(values[key.group(1)]) + '"', tag)
        return tag
    page = re.sub(r'<meta\b[^>]+>', meta, page)
    page = re.sub(r'<link rel="canonical"[^>]*>', '<link rel="canonical" href="' + BASE + path + '">', page)
    page = page.replace('<body class="modern">', '<body class="modern ' + body_class + '">')
    extra = '<meta property="og:url" content="' + BASE + path + '">\n'
    extra += '<link rel="stylesheet" href="/css/areas.css?v=area-guides-1">\n'
    extra += '<script type="application/ld+json">' + json.dumps(schema, ensure_ascii=False).replace('<', '\\u003c') + '</script>\n'
    return page.replace('</head>', extra + '</head>')

PHONE_ICON = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.12.96.35 1.9.69 2.79a2 2 0 0 1-.45 2.11L8.08 9.89a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.89.34 1.83.57 2.79.69A2 2 0 0 1 22 16.92z"/></svg>'
PHONE = '<a class="btn btn-outline area-phone" href="tel:770-946-1697">' + PHONE_ICON + '<span>Call 770-946-1697</span></a>'
SERVICES = [
    ('Driveways', '/services/driveways.html', 'New driveways, extensions, and replacement concrete planned around parking, access, and the connection to your property.'),
    ('Patios', '/services/patios.html', 'Outdoor concrete spaces planned around seating, everyday use, and the way your patio connects to the house and yard.'),
    ('Sidewalks & pathways', '/services/sidewalks.html', 'Private-property walks and concrete repairs that connect entrances, parking areas, and outdoor spaces.'),
    ('Decorative concrete', '/services/concrete-stamping.html', 'Stamped and decorative options for projects where the finish is part of the design. Discuss the setting and intended use.')
]
IMAGES = {
    'driveways': ('AdobeStock_63714628-Optimized.jpg', 'Concrete driveway and garage approach', 900, 600, 'Driveway service example'),
    'patios': ('Screen-Shot-2020-11-27-at-1.24.23-PM.jpg', 'Concrete patio beside a brick home', 1774, 900, 'Patio service example'),
    'sidewalks': ('AdobeStock_377241561-optimized-1.jpg', 'Concrete walkway beside landscaping', 900, 600, 'Walkway service example'),
    'decorative': ('AdobeStock_75067836-Optimized.jpg', 'Decorative concrete surface', 900, 600, 'Decorative concrete service example')
}

def quote_form(city):
    form = FORM.replace('contact-contact', 'contact-area-' + city['slug'])
    form = form.replace('wf-form-Message-Form', 'wf-form-Area-Quote')
    form = form.replace('<input type="hidden" name="form-name" value="contact-area-' + city['slug'] + '">',
        '<input type="hidden" name="form-name" value="contact-area-' + city['slug'] + '">\n'
        '<input type="hidden" name="Area" value="' + esc(city['name']) + '">\n'
        '<input type="hidden" name="Page-URL" value="' + BASE + city_url(city) + '">')
    form = form.replace('name="City" type="text"', 'name="City" value="' + esc(city['name']) + '" type="text"')
    form = form.replace('<option>Other</option>', '<option>Decorative concrete</option>\n<option>Other</option>')
    form = form.replace('placeholder="What would you like to repair, build, or improve?"',
                        'placeholder="Project address, approximate size, and what you would like to build or repair."')
    return ('<aside class="area-quote quote-form w-form" id="area-quote" aria-labelledby="area-quote-title" tabindex="-1">\n'
        '<h2 id="area-quote-title" tabindex="-1">Request a free quote</h2>\n'
        '<p>Tell us about your ' + esc(city['name']) + ' project.</p>\n' + form +
        '\n<div class="w-form-done" role="status">Thank you! Your submission has been received.</div>\n'
        '<div class="w-form-fail" role="alert">Your message could not be sent. Please try again or call 770-946-1697.</div>\n'
        '</aside>')

def distance(a, b):
    x, y = math.radians(a['latitude']), math.radians(b['latitude'])
    dl = math.radians(b['longitude'] - a['longitude'])
    return math.sin((y-x)/2)**2 + math.cos(x)*math.cos(y)*math.sin(dl/2)**2

def breadcrumb(items):
    return {'@type':'BreadcrumbList','itemListElement':[
        {'@type':'ListItem','position':i+1,'name':name,'item':BASE+url}
        for i,(name,url) in enumerate(items)]}

def render_city(city):
    name = city['name']
    path = city_url(city)
    title = 'Concrete Contractor in ' + name + ', GA | LCH Concrete'
    description = 'Driveways, patios, walkways, and concrete repairs in ' + name + ', GA. Hampton-based LCH Concrete & Restoration. Request a free project estimate.'
    schema = {'@context':'https://schema.org','@graph':[
        {'@type':'Service','@id':BASE+path+'#service','name':'Concrete services in '+name+', GA',
         'serviceType':['Concrete construction','Concrete restoration','Driveways','Patios','Sidewalks'],
         'url':BASE+path,'areaServed':{'@type':'City','name':name,'containedInPlace':{'@type':'State','name':'Georgia'}},
         'provider':{'@type':'Organization','@id':BASE+'/#business','name':'LCH Concrete & Restoration','url':BASE+'/',
                     'telephone':'+1-770-946-1697','email':'ConcreteLCH@gmail.com'}},
        breadcrumb([('Home','/'),('Service areas','/areas/'),(name+', GA',path)])
    ]}
    page = start_page(title, description, path, 'area-page', schema)
    page = page.replace('class="btn nav-cta" href="/contact.html"', 'class="btn nav-cta" href="#area-quote"')
    image, alt, iw, ih, caption = IMAGES[city['focus']]
    service_cards = '\n'.join(
        '<article class="area-service-card"><h3>' + esc(label) + '</h3><p>' + esc(copy) +
        '</p><a class="text-link" href="' + href + '">Explore ' + esc(label.lower()) + '</a></article>'
        for label,href,copy in SERVICES)
    planning = '\n'.join('<li><h3>'+esc(p['title'])+'</h3><p>'+esc(p['text'])+'</p></li>' for p in city['planning'])
    faqs = '\n'.join('<details class="area-faq-item"><summary>'+esc(f['question'])+'</summary><p>'+esc(f['answer'])+'</p></details>' for f in city['faqs'])
    neighbors = sorted([c for c in CITIES if c != city], key=lambda c:distance(city,c))[:3]
    nearby = '\n'.join('<a class="text-link" href="'+city_url(c)+'">'+esc(c['name'])+', GA</a>' for c in neighbors)
    page += f'''<main id="main">
<div class="wrap area-shell">
<nav class="crumb area-breadcrumb" aria-label="Breadcrumb"><a href="/index.html">Home</a><span aria-hidden="true">/</span><a href="/areas/">Areas</a><span aria-hidden="true">/</span><span aria-current="page">{esc(name)}, GA</span></nav>
<div class="area-layout">
<article class="area-article">
<header class="area-intro">
<div class="eyebrow">{esc(city['county'])} · Georgia</div>
<h1>Concrete services in {esc(name)},&nbsp;GA</h1>
<p>{esc(city['intro'])}</p>
<div class="actions"><a class="btn" href="#area-quote">Request a free quote</a>{PHONE}</div>
</header>
<figure class="area-photo"><img src="/images/{image}" alt="{esc(alt)}" width="{iw}" height="{ih}" fetchpriority="high" decoding="async"><figcaption>{caption} <a class="text-link" href="/gallery.html">View the project gallery</a></figcaption></figure>
<nav class="area-jump" aria-label="On this page"><a href="#area-services">Our services</a><a href="#area-planning">Plan your project</a><a href="#area-questions">Common questions</a></nav>
<section class="area-section"><h2>{esc(city['local_heading'])}</h2>{''.join('<p>'+esc(p)+'</p>' for p in city['local_copy'])}</section>
<section class="area-section" id="area-services"><h2>Concrete services for your property</h2><div class="area-services">{service_cards}</div></section>
<section class="area-section"><h2>Residential &amp; commercial</h2><div class="area-audiences"><section><h3>For your home</h3><p>{esc(city['residential'])}</p></section><section><h3>For your business or property</h3><p>{esc(city['commercial'])}</p></section></div></section>
<section class="area-section area-planning" id="area-planning"><h2>Before your {esc(name)} concrete estimate</h2><ul>{planning}</ul><a class="text-link" href="{esc(city['source'])}" target="_blank" rel="noopener noreferrer">Official {esc(name)} resources</a></section>
<section class="area-section"><h2>A clear next step</h2><ol class="area-steps"><li><strong>Share the project.</strong> Send the address, photos, approximate size, and the result you want.</li><li><strong>Discuss the property.</strong> We can talk about the existing concrete, access, intended use, and questions that need a closer look.</li><li><strong>Define the scope.</strong> Review the proposed work and estimate before making scheduling decisions.</li></ol></section>
<section class="area-section" id="area-questions"><h2>Questions about concrete work in {esc(name)}</h2><div class="area-faq">{faqs}</div></section>
<section class="area-section area-nearby"><h2>Looking nearby?</h2><p>Our service area starts in Hampton and extends to selected communities south of Atlanta.</p><div class="area-nearby-links">{nearby}</div><a class="text-link" href="/areas/">View all service areas</a></section>
</article>
{quote_form(city)}
</div>
</div>
<nav class="area-mobile-actions" aria-label="Project actions"><a class="area-mobile-call" href="tel:770-946-1697">{PHONE_ICON}<span>Call LCH</span></a><a class="btn" href="#area-quote">Request a free quote</a></nav>
</main>'''
    return sync_shared(page + SUFFIX, SITE / 'areas' / city['slug'] / 'index.html')

def render_hub():
    title = 'Concrete Service Areas South of Atlanta | LCH Concrete'
    description = 'Explore 14 concrete service areas around Hampton, GA. Local driveway, patio, walkway, and restoration services for homes and businesses south of Atlanta.'
    schema = {'@context':'https://schema.org','@graph':[
        {'@type':'CollectionPage','name':'Concrete service areas south of Atlanta','url':BASE+'/areas/',
         'mainEntity':{'@type':'ItemList','itemListElement':[
             {'@type':'ListItem','position':i+1,'name':c['name']+', GA','url':BASE+city_url(c)}
             for i,c in enumerate(CITIES)]}},
        breadcrumb([('Home','/'),('Service areas','/areas/')])
    ]}
    page = start_page(title,description,'/areas/','areas-index',schema)
    cards = '\n'.join('<article class="area-city-card"><span class="area-card-label">'+
        ('Our home base' if c['slug']=='hampton' else esc(c['county']))+'</span><h2>'+esc(c['name'])+
        ', GA</h2><p>'+esc(c['summary'])+'</p><a class="text-link" href="'+city_url(c)+'">Explore '+esc(c['name'])+'</a></article>' for c in CITIES)
    page += f'''<main id="main">
<section class="page-hero"><div class="wrap"><nav class="crumb" aria-label="Breadcrumb"><a href="/index.html">Home</a><span aria-hidden="true">/</span><span aria-current="page">Areas</span></nav><div class="eyebrow">Based in Hampton, Georgia</div><h1>Concrete services south of Atlanta.</h1><p>Local project guidance for 14 communities within an approximately 40-mile radius of Hampton. Explore your area, find the services that fit your property, and start a conversation with LCH.</p><div class="actions"><a class="btn" href="/contact.html">Request a free quote</a>{PHONE}</div></div></section>
<section class="section-space"><div class="wrap"><div class="section-heading-row"><h2>Start close to home.</h2><p class="area-directory-intro">Starting with Hampton and expanding outward, these are the communities featured in our local service guides.</p></div><div class="areas-grid">{cards}</div></div></section>
<section class="section-space areas-coverage"><div class="wrap"><div class="area-coverage-copy"><div class="eyebrow">Plan with LCH</div><h2>Your address. Your project. A useful plan.</h2><p>A city name is only the starting point. Tell us about the concrete you want to build, repair, or replace, how the property is used, and the result you have in mind.</p><p>The service-area radius is geographic, not driving mileage. For properties near a city boundary or outside the places listed here, send the full address so we can confirm the location and discuss the work.</p><a class="text-link" href="/contact.html">Let's talk about your project</a></div></div></section>
</main>'''
    return sync_shared(page + SUFFIX, SITE / 'areas/index.html')

# Build area pages first, then synchronize the shared menu/footer on every route.
for city in CITIES:
    save(SITE / 'areas' / city['slug'] / 'index.html', render_city(city))
save(SITE / 'areas/index.html', render_hub())
for path in sorted(SITE.rglob('*.html')):
    save(path, sync_shared(path.read_text(), path))

# Keep one discoverable sitemap, using existing canonicals for the original routes.
ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')
urlset = ET.Element('{http://www.sitemaps.org/schemas/sitemap/0.9}urlset')
for path in sorted(SITE.rglob('*.html')):
    if path.name in {'401.html','404.html','thank-you.html'}:
        continue
    match = re.search(r'<link rel="canonical" href="([^"]+)"', path.read_text())
    assert match, path
    node = ET.SubElement(urlset, '{http://www.sitemaps.org/schemas/sitemap/0.9}url')
    ET.SubElement(node, '{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text = html.unescape(match.group(1))
ET.indent(urlset, space='  ')
save(SITE / 'sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(urlset,encoding='unicode') + '\n')
save(SITE / 'robots.txt', 'User-agent: *\nAllow: /\n\nSitemap: ' + BASE + '/sitemap.xml\n')
if STALE:
    raise SystemExit('Stale generated files:\n' + '\n'.join(STALE))
print(('Checked' if CHECK else 'Built') + f' {len(CITIES)} city pages, an area directory, shared navigation, and sitemap.')
