# Typography and wide-screen layout

The redesign uses `site/css/readability.css` and `site/css/responsive.css`, loaded last on all 13 pages. Base font sizes in modern.css, studio.css, theme.css, and hero-quote.css use rem units so browser font preferences can enlarge them. The exported gallery runtime and its component stylesheet remain intact.

## Reading sizes

The previous typography audit found visible text at 9–13px on every page, including form labels, footer links, fine print, card descriptions, navigation, and paragraphs.

| Content | Normal desktop and phone | At a 5120px CSS viewport |
| --- | --- | --- |
| Paragraphs, inputs, buttons, project card labels | At least 16px | 24px |
| Secondary labels, captions, footer, fine print | At least 14px | 20px |
| Desktop navigation | At least 15px | About 23px |

These are project readability targets, not minimum font sizes prescribed by WCAG. Body text uses a 1.7 line height. Long reading passages are limited to roughly 70 characters per line. Text and controls can wrap, and form submit inputs have been replaced by buttons so their labels can wrap when enlarged. The transport still supports both control types and restores the correct label after success or failure.

## Fluid content area

The previous studio layout capped the content width at 1080px. The shared content area now grows with the viewport while retaining proportional side gutters and an upper limit of 196rem. At the default 16px root size:

| Viewport width | Content width |
| --- | --- |
| 1440px | About 1325px |
| 1920px | About 1766px |
| 2560px | 2112px |
| 3840px | 2624px |
| 5120px | 3136px |

At 1800px and wider, headings, photos, section spacing, and card titles scale progressively. Services and galleries use four columns. The hero keeps equal content and form columns, with three form columns at 3000px and wider. The article and lower inquiry sections retain separate width caps to keep long text and forms comfortable to use. The hero heading uses its full column instead of retaining the earlier 640px cap.

The mobile navigation breakpoint is 1000px, allowing larger links to fit cleanly before the full menu opens. The hero measures the actual header height to maintain the opening viewport strip placement as header sizes change.

A high-resolution display can report a smaller CSS viewport because of operating system scaling. Both 2560px and 5120px widths were tested rather than inferring layout from the display's physical resolution alone.

## Verification

- All 13 pages checked at 390px and 1440px: no visible reading text below 14px and no horizontal document overflow.
- All 13 pages checked at 320px and 5120px in both themes, including open navigation and service-area disclosures: no horizontal document overflow or clipped text controls.
- Homepage, services overview, sidewalk detail, and gallery checked at 1024px, 1920px, 2560px, and 3840px in both themes.
- A 200% root font-size check on the homepage, contact page, sidewalk detail, and gallery at 1440px found no horizontal overflow or clipped text controls. This checks enlarged font preferences; it is not a full native browser zoom or assistive-technology audit.
- Desktop hover navigation, mobile menu, Escape dismissal, carousel next/previous, and gallery open/close checked in Chromium. All 26 gallery lightboxes remain available.
- Mocked form transport checked for pending state, duplicate-submit prevention, success, failure, focus, and restored button labels. The localhost form still refuses transport and shows the preview notice. No real inquiries were sent.
- `python3 scripts/check_site.py` and `git diff --check` pass.

This review addresses typography and responsive layout. It does not establish full WCAG conformance. WCAG also requires text enlargement without loss of content or functionality and reflow at narrow viewports. See the W3C guidance for [Resize Text](https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html) and [Reflow](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html).
