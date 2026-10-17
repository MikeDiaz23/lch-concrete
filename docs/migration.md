# Migration record

Source: `lch-concrete.webflow.zip`, supplied by the user, exported October 17, 2026. Source documents are reference data; only the user's request authorizes migration work.

Connected Webflow site: `618f1e77756c4c6c2adc700b`, domains `www.lchconcrete.com` and `lchconcrete.com`. The page API lists the same 12 pages present in the export. Ten are public content pages; the other two are Webflow's password and not-found templates. No CMS collection markup occurs in the exported pages. A CMS collection API query failed schema validation, so CMS account inventory has not been verified.

## Preserved and adapted

All exported page HTML, CSS, responsive images, logos, and interaction scripts are retained. Existing titles, descriptions, phone/email links, Google Analytics (`G-GLE8JW4T57`), Google Fonts, and external map/review links remain. Canonical URLs retain the existing public extensionless paths. jQuery 3.5.1 is vendored and its SHA-256 matches the original SRI attribute. Open Graph images use the local image on the production domain. The 404 template uses root-relative assets so nested missing paths can display correctly.

The gallery contains 26 lightbox elements. Original lightbox JSON and local full-size images are retained, including any pre-existing duplicate images/groups.

Webflow's hosted form backend is replaced by an optional Netlify adapter on all 10 inquiry forms. Every original business field remains. Each page has a unique form name, a honeypot, and a Netlify-managed CAPTCHA placeholder. A capture-phase handler avoids the Webflow runtime's duplicate submission handler and retains inline success/error messages. Notifications, form detection, and real delivery require host setup. Never treat a local preview as a submission test.

`401.html` is retained for fidelity, but Webflow's `/.wf_auth` endpoint does not transfer. It is not access control on a static host. No protected content was identified in the export; verify any intended protection in Webflow before cutover and implement host-side authentication if needed.

## Still required before live cutover

- Choose hosting and configure form delivery and notifications.
- Verify live redirect rules, custom code, and any protected routes in Webflow settings; these settings are not fully represented in the export.
- Browser comparison on desktop/mobile: navigation, dropdowns, gallery keyboard behavior, animation visibility, anchor links, form validation, and success/error states.
- Deploy-time CAPTCHA and real inquiry delivery tests on every form variant; do not send test inquiries without the user's authorization.
- Verify external maps/review links, analytics, production social preview URLs, extensionless routes, HTTPS, and 404 response status.
- Connect the repository to the deployment host and move the domain only after verification. Retire Webflow after cutover succeeds.

The Python check validates local asset references (including CSS, responsive variants, and lightbox JSON), route files, and inquiry form contracts. It cannot establish rendered or backend parity.
