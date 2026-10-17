# LCH Concrete & Restoration

Website source for [lchconcrete.com](https://www.lchconcrete.com), migrated from the October 17, 2026 Webflow export. Make future website edits in this repository using Codex. Hosting and domain cutover are deferred.

## Redesign preview

The `redesign/modern-site` branch contains a full visual redesign using the existing logo, business details, project photos, and inquiry fields. `main` retains the original migrated design. The preview server serves the currently checked-out branch.

New design styles are in `site/css/modern.css`; navigation behavior is in `site/js/modern.js`. Page HTML is edited directly. See [redesign notes](docs/redesign.md).

## Work locally

```sh
python3 scripts/check_site.py
python3 -m http.server 8000 --directory site
```

Open http://localhost:8000. No package installation or build framework is needed. Local previews do not send inquiries or render the hosting-provided CAPTCHA.

## Files to edit

- `site/index.html`: homepage.
- `site/contact.html`, `site/gallery.html`: contact and gallery pages.
- `site/about/` and `site/services/`: remaining content pages.
- `site/css/modern.css`: current redesign styles; `lch-concrete.css` retains the original export styles.
- `site/images/`: logos, photos, responsive variants, and gallery images.
- `site/js/lch-concrete.js`: exported runtime, now used on the gallery for its lightboxes.
- `site/js/contact-forms.js`: optional Netlify contact transport, separate from the exported runtime.

The HTML, responsive styles, gallery lightboxes, animations, phone/email links, maps links, Google Fonts, and Google Analytics ID are retained. jQuery is stored locally with its original integrity hash. Social preview images use the site's own domain. See [migration notes](docs/migration.md) for verification limits and hosting-dependent features.

## Hosting later

Namecheap remains the user's domain/provider choice; no DNS or Webflow hosting settings were changed. GitHub stores the source; a hosting provider must serve it and process inquiries.

An optional Netlify configuration is included because it offers a replacement for Webflow Forms. It is not deployed or connected. To use it later:

1. Import this GitHub repository into Netlify; publish directory is `site` and validation runs from `netlify.toml`.
2. Enable Forms detection and redeploy. Verify all 10 `contact-*` forms appear.
3. Configure submission email notifications to the confirmed business recipient. The address displayed on the site is `ConcreteLCH@gmail.com`; notifications are not configured by this repository.
4. Test CAPTCHA, successful submissions, inbox delivery, error handling, clean URLs, mobile navigation, gallery lightboxes, and animations on the preview domain.
5. Connect `www.lchconcrete.com` and `lchconcrete.com`, then update the applicable Namecheap DNS records according to the selected host. Keep existing email records.
6. Verify HTTPS and redirects before ending Webflow hosting.

For Namecheap web hosting or another provider, replace the Netlify form adapter with that host's secure backend and configure extensionless routes and the custom 404 page. Uploading these files to basic static hosting alone does not provide contact form delivery.

Official references: [Netlify form setup](https://docs.netlify.com/manage/forms/setup/) and [CAPTCHA setup](https://docs.netlify.com/manage/forms/spam-filters/).
