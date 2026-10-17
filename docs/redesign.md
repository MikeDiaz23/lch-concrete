# Modern redesign preview

Branch: `redesign/modern-site`. The original Webflow migration remains on `main`. Hosting and domain changes remain deferred.

The current direction draws on https://libraries.dev/: a charcoal background, compact Inter typography, centered hero, rounded frames, subtle borders, and restrained hover effects. LCH's red logo icon remains consistent in both themes, with white lettering on dark surfaces and dark lettering on light surfaces. The homepage surrounds its service-focused message with linked project-photo cards rather than software demos. Existing project photos lead the homepage and gallery. Business name, logo, contact details, operations manager, service areas, service descriptions, customer quotes, analytics ID, routes, gallery images, and inquiry fields remain available.

All 13 pages share the new header, navigation, footer, typography, and spacing. The homepage is rebuilt around services, local experience, completed projects, customer quotes, and the quote request. Service and community pages retain their original descriptive content in readable article layouts. The gallery retains its 26 exported lightboxes and runtime. The new navigation uses keyboard-accessible native dropdowns and a mobile menu with Escape dismissal. Reduced-motion settings disable entrance effects.

Edit page HTML directly. Base layout styles are in `site/css/modern.css`; the current visual direction is in `site/css/studio.css`, navigation behavior in `site/js/modern.js`, and form transport in `site/js/contact-forms.js`. The original exported stylesheet is retained for comparison but is no longer loaded by the redesigned pages.

## Featured concrete photography

The four service detail pages and About Us introduce their subject with a large photograph beside the title and primary actions. Photos retain their full proportions and original color, replacing the small cropped sidebar thumbnails. At tablet and phone widths, the photograph spans the content width below the introduction. Existing image variants provide responsive downloads, and explicit dimensions reserve the image space as it loads. Service descriptions and inquiry forms remain intact; the sidebar quote prompt follows the article on smaller screens.

## Light and dark appearance

Every header includes a sun/moon switch with a keyboard-accessible “Light mode” state. Dark remains the initial appearance. The visitor's selection is saved in browser storage and restored before styles render on subsequent pages; switching still works when storage is unavailable. The control remains beside the mobile menu, with the logo and controls sharing one row. The light palette uses warm concrete neutrals, matching card and header surfaces, and readable form and review colors. In both headers and footers, the logo icon uses the hero headline’s brighter red (#d64b45) with white lettering in dark mode, and the original red (#9f1d20) with dark lettering in light mode. Both variants share the original logo geometry. The homepage's aggregate, grid, and animated line accents adapt to the selected palette, including in reduced-motion mode. Appearance rules live in `site/css/theme.css`, with preference restoration in `site/js/theme.js`.

## Validation

- Python site validation passes for all 13 pages, local assets, responsive references, lightbox image data, and all 10 inquiry forms.
- Browser layout checks pass at 390px, 768px, and 1440px for the homepage, contact, gallery, patio service, and community pages, with no document overflow or broken eager-loaded images.
- Browser interaction checks pass for mobile menu toggle, Escape dismissal, outside-click dropdown dismissal, gallery opening and Escape closing, and the inquiry form's missing-CAPTCHA error.
- Every page has one main heading, unique IDs, and valid label targets.
- No real inquiries were sent. Hosting-dependent CAPTCHA, backend delivery, notifications, and server authentication remain unverified until hosting is configured.

Preview the checked-out branch at http://127.0.0.1:8000/ using the existing Python server. Refresh if an older design is cached.

The earlier light editorial direction is preserved in commit `c0f5421`. No reference-site code or proprietary assets were copied. The four primary services are visible on the homepage; existing business information and inquiry fields remain.

## Interactive hero surface

`site/js/hero-surface.js` draws a decorative canvas behind the homepage hero. Fine angular grains suggest concrete aggregate; offset perspective seams suggest poured slabs. A slow light sweep adds ambient movement. Pointer movement gently displaces nearby grains and leaves a short finishing stroke, referring to the pass of a trowel.

The canvas does not capture pointer input or block links. It caps resolution and particle count, draws at approximately 30 fps, and pauses offscreen or when the document is hidden. Reduced-motion mode draws a still surface and disables pointer animation. No dependencies or new external assets are required.

In light mode, darker warm mineral tones keep the grid and pointer sweep visible against the pale background. The pointer wash strengthens during interaction and the trail uses a darker tint; the surface mask fades more gradually toward the edges. Moving grid highlights have slightly more contrast in light mode, while reduced-motion mode retains only the static grid.

Browser checks passed for ambient and pointer animation, the quote/gallery CTA hit target, offscreen pause, reduced-motion stability, animation resume, mobile/tablet overflow, and absence of runtime errors. These checks sent no inquiries.

## Hero tile entrance

`site/js/hero-tiles.js` gives the four homepage tiles a staggered construction-sketch reveal on each page load. The outlines and slab joints draw first, followed by a soft photo fade, with 110ms between tiles. The sequence takes roughly two and a half seconds and preserves the settled positions, tilts, and hover styles. Decorative SVG sketches are removed afterward. Any pointer, keyboard, or focus interaction skips the intro immediately. Reduced-motion preferences bypass it, and a short fallback restores visibility if the script fails to load.

The sketch/photo handoff uses matching image bounds and a synchronized 850ms crossfade. Image decoding is attempted before the intro (with a short time limit), and the photo retains its normal sharpness and color throughout to avoid a snap at completion.

Persistent warm highlights begin immediately on page load, alongside the tile intro. They travel along the exact perspective rays and slanted cross-seams of the existing background grid, sharing normalized geometry with the canvas so the angles remain aligned at every viewport size. Slow 18–27 second loops and lower contrast behind the copy keep the motion understated. Motion pauses offscreen and in hidden tabs; reduced-motion mode retains the still canvas grid.

## Hero typography

The hero pairs a medium-weight Inter first line (Concrete services) with a warm Georgia italic second line (Residential & Commercial) to distinguish the offering from its audience. One supporting sentence combines the services and local-team message in a consistent, stronger text treatment, with a readable line length and the same typography throughout. Dark mode uses warm white text; light mode uses dark text. The experience badge emphasizes the number, and the action buttons remain legible. Georgia is a system font, so the contrasting headline adds no font download.

## Opening viewport strip

The hero uses a viewport-height flex layout so its full-width highlights strip sits at the bottom of the opening browser view. The strip remains a static element in document flow and scrolls away with the page. Compact height rules adjust spacing and photo crops on shorter screens while retaining readable tile labels and all four strip items. The narrow mobile header keeps the logo and menu on one row. Browser checks cover initial bottom alignment, natural scrolling, and layout fit across desktop, tablet, and phone viewports.
