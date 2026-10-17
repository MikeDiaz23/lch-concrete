# Modern redesign preview

Branch: `redesign/modern-site`. The original Webflow migration remains on `main`. Hosting and domain changes remain deferred.

The current direction draws on https://libraries.dev/: a charcoal background, compact Inter typography, centered hero, rounded frames, subtle borders, and restrained hover effects. LCH's existing white logo variant sits on the dark header, with red accents carrying the business branding. The homepage surrounds its service-focused message with linked project-photo cards rather than software demos. Existing project photos lead the homepage and gallery. Business name, logo, contact details, operations manager, service areas, service descriptions, customer quotes, analytics ID, routes, gallery images, and inquiry fields remain available.

All 13 pages share the new header, navigation, footer, typography, and spacing. The homepage is rebuilt around services, local experience, completed projects, customer quotes, and the quote request. Service and community pages retain their original descriptive content in readable article layouts. The gallery retains its 26 exported lightboxes and runtime. The new navigation uses keyboard-accessible native dropdowns and a mobile menu with Escape dismissal. Reduced-motion settings disable entrance effects.

Edit page HTML directly. Base layout styles are in `site/css/modern.css`; the current visual direction is in `site/css/studio.css`, navigation behavior in `site/js/modern.js`, and form transport in `site/js/contact-forms.js`. The original exported stylesheet is retained for comparison but is no longer loaded by the redesigned pages.

## Validation

- Python site validation passes for all 13 pages, local assets, responsive references, lightbox image data, and all 10 inquiry forms.
- Browser layout checks pass at 390px, 768px, and 1440px for the homepage, contact, gallery, patio service, and community pages, with no document overflow or broken eager-loaded images.
- Browser interaction checks pass for mobile menu toggle, Escape dismissal, outside-click dropdown dismissal, gallery opening and Escape closing, and the inquiry form's missing-CAPTCHA error.
- Every page has one main heading, unique IDs, and valid label targets.
- No real inquiries were sent. Hosting-dependent CAPTCHA, backend delivery, notifications, and server authentication remain unverified until hosting is configured.

Preview the checked-out branch at http://127.0.0.1:8000/ using the existing Python server. Refresh if an older design is cached.

The earlier light editorial direction is preserved in commit `c0f5421`. No reference-site code or proprietary assets were copied. The four primary services are visible on the homepage; existing business information and inquiry fields remain.
