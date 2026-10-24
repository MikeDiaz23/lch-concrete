# Local service-area guides

The Areas menu, directory, and 14 city guides are part of the redesign branch. The existing service pages, gallery, analytics, and original main-page content are preserved. Hosting, DNS, and Webflow cancellation remain deferred.

## Coverage and selection

The user selected an approximate 40-mile geographic radius centered on Hampton, not a driving-distance limit. The 14 featured places are prominent south Atlanta communities rather than an exhaustive list of municipalities. The directory and menu start at Hampton and expand outward by approximate radius. The footer area list now links to these guides instead of the exported list of external map links.

Distances were calculated from representative place coordinates in the [2025 U.S. Census Gazetteer place file](https://www2.census.gov/geo/docs/maps-data/data/gazetteer/2025_Gazetteer/2025_Gaz_place_national.zip), using great-circle distance and a 3958.7613-mile Earth radius. These are approximate distances between representative geographic points, not road mileage or a guarantee that every address within a municipality lies inside the radius. The selected coordinates, geographic IDs, source URL, and calculated distances are stored with the content. Pages ask visitors to provide the exact address where confirmation matters.

## Content and source of truth

Edit content/areas.json for city copy, selection, and source links. Run:

    python3 scripts/build_area_pages.py
    python3 scripts/build_area_pages.py --check
    python3 scripts/check_site.py

The generated HTML is committed under site/areas/. It is static, crawlable, and works with the standard Python preview server. No framework or dependency installation is required. The builder uses the contact page's shared shell and form contract, synchronizes navigation and footer area links across all pages, and maintains the sitemap. Do not hand-edit generated city HTML for content changes. An obsolete city directory must be removed intentionally when replacing a selection; the checker rejects extra city directories.

Each city has original introductory and local context copy, residential and commercial guidance, three planning points, two tailored FAQs, and nearby-city links. Local context is informed by the official sources listed below and in the data file. Property planning advice is original editorial guidance inferred from those settings, not a claim about a specific property's condition or a city-wide construction requirement. Existing service photos are labelled as service examples and do not claim to show projects completed in the named city.

## Layout and navigation

All pages share an Areas dropdown with 14 city links and an overview link. Desktop hover, native keyboard disclosure, Escape dismissal, and mobile menu behavior are retained. The navigation collapses at 1200px to make room for the added menu. The desktop area panel uses two columns and a viewport-limited scrolling area when necessary. Mobile links remain reachable inside the main menu's scrolling region.

City pages use a content column and a quote panel. At desktop widths the quote panel sticks below the measured header height. Its height is limited by the available viewport, with internal scrolling on shorter screens so every field and the submit button remains reachable. At 1200px and below, the form follows the content in normal flow and a fixed call/quote bar provides access without covering the reading area. The call action uses the existing business number. The quote action jumps to the form.

## Inquiry behavior

Each city has a unique form name, contact-area-<city>, with the same core fields, CAPTCHA declaration, and transport as the existing forms. Project city is prefilled and editable. Hidden Area and Page-URL fields preserve the inquiry's origin even if the visitor edits the city. There are 25 inquiry forms in total, including the original 11.

Local previews continue to refuse message delivery and show the existing phone/email notice. The forms remain prepared for optional Netlify hosting. Production CAPTCHA, storage, notifications, and delivery require configuration and end-to-end testing with the chosen backend. No real inquiries were sent during this work.

## Search structure

City pages have distinct titles, descriptions, headings, canonical directory URLs, and social metadata. They link to relevant service pages, the directory, and nearby city guides. Every city includes Service and BreadcrumbList structured data. A single provider identity is used throughout; no extra city offices, local addresses, reviews, project counts, credentials, or response-time claims were invented. The directory includes CollectionPage and ItemList structured data.

The sitemap lists the 25 indexable canonical URLs. Authentication/error utility pages and the thank-you page are excluded from it. robots.txt points to the sitemap. No search indexing, ranking, or rich-result outcome is promised. The content approach follows [Google's guidance on doorway abuse](https://developers.google.com/search/docs/essentials/spam-policies#doorway-abuse) by providing useful local guidance instead of swapping place names in repeated copy. Structured data does not imply an additional physical branch or eligibility for a specific search feature; see [Google's local business guidance](https://developers.google.com/search/docs/appearance/structured-data/local-business).

## Verification

The required site check validates all 28 pages, internal assets and links, gallery data, heading/label IDs, the 14-city cap, shared menu links, localized form context, structured data, and sitemap canonicals. The builder's check mode detects stale generated files. Browser layout checks passed across all 28 pages at 320px, 1440px, and 5120px in both themes, for 168 cases with no horizontal overflow, clipped text, broken loaded images, or runtime errors. Sticky positioning passed on all 14 city pages. Desktop hover and keyboard disclosure, short-screen menu and form scrolling, mobile quote-target focus, and the original gallery and hero controls passed their interaction checks. Form transport is tested with mocks only, alongside the localhost delivery guard.

## Local context sources

- [Hampton](https://hamptonga.gov/DocumentCenter/View/2701/Res-21-03-Main-Street-Boundaries): Henry County, approximately 0.0 straight-line miles from the Hampton representative point. Route: /areas/hampton/.
- [Griffin](https://www.cityofgriffin.com/government/departments/economic-development/downtown-griffin): Spalding County, approximately 9.4 straight-line miles from the Hampton representative point. Route: /areas/griffin/.
- [McDonough](https://www.mcdonoughga.org/181/Downtown-Development-Authority): Henry County, approximately 9.7 straight-line miles from the Hampton representative point. Route: /areas/mcdonough/.
- [Jonesboro](https://www.jonesboroga.com/m/JonesboroDowntownDevelopmentAuthority.aspx): Clayton County, approximately 10.4 straight-line miles from the Hampton representative point. Route: /areas/jonesboro/.
- [Stockbridge](https://stockbridgega.org/ed): Henry County, approximately 11.1 straight-line miles from the Hampton representative point. Route: /areas/stockbridge/.
- [Fayetteville](https://www.fayetteville-ga.gov/DocumentCenter/View/3906/Hello-Neighbor-Update-2025-09-29): Fayette County, approximately 11.2 straight-line miles from the Hampton representative point. Route: /areas/fayetteville/.
- [Locust Grove](https://www.locustgrove-ga.gov/living-here/parks): Henry County, approximately 11.7 straight-line miles from the Hampton representative point. Route: /areas/locust-grove/.
- [Riverdale](https://www.riverdalega.gov/505/Event-Information): Clayton County, approximately 14.4 straight-line miles from the Hampton representative point. Route: /areas/riverdale/.
- [Peachtree City](https://www.peachtree-city.org/1187/Shared-Use-Path-System): Fayette County, approximately 15.7 straight-line miles from the Hampton representative point. Route: /areas/peachtree-city/.
- [Forest Park](https://www.forestparkga.gov/sites/default/files/fileattachments/planning_building_and_zoning/page/3321/forest_park_2023_comprehensive_plan-final.pdf): Clayton County, approximately 17.1 straight-line miles from the Hampton representative point. Route: /areas/forest-park/.
- [Fairburn](https://www.fairburn.com/209/Main-Street-Program-Downtown-Development): Fulton County, approximately 20.4 straight-line miles from the Hampton representative point. Route: /areas/fairburn/.
- [Union City](https://www.unioncityga.org/home/showpublisheddocument/1836/636670508774130000): Fulton County, approximately 21.3 straight-line miles from the Hampton representative point. Route: /areas/union-city/.
- [South Fulton](https://www.cityofsouthfultonga.gov/3140/Development-Nodes): Fulton County, approximately 24.2 straight-line miles from the Hampton representative point. Route: /areas/south-fulton/.
- [Newnan](https://www.newnanga.gov/188/Historic-Districts): Coweta County, approximately 27.6 straight-line miles from the Hampton representative point. Route: /areas/newnan/.
