# Final technical proof audit — ef98c03 / v0.9.0

Scope: files under `/tmp/bwt-appnote`; no manuscript, proof or release file changed. Actual three-page main PDF was rendered in memory and visually inspected (not merely its older `preview-main-*.png` files). Supplement checks combine all-page geometry/text/image inspection with visual checks of pages 8, 13, 19 and 29. DOCX inspection is ZIP/XML/media inspection, **not Word pagination**.

Policy basis: [official Bioinformatics author guidelines](https://academic.oup.com/bioinformatics/pages/author-guidelines), supplied `/tmp/bwt-final-check/author-guidelines.txt`, especially lines 760 (figures), 789–791 (LaTeX widths), and 688 (figure preparation). Four-page Application Note limit; 86 mm single/178 mm double widths; adjacent legends; initial inline low-resolution review figures permitted. Production guidance requests 1200 dpi line/350 dpi colour or halftone TIFF preparation.

## Findings

### W1 — Medium: journal-width mismatch, main PDF

`/tmp/bwt-appnote/submission/manuscript.pdf`, pages 1–3: body columns measure **82.680 mm**, gutter **6.328 mm**, total text/figure width **171.688 mm**, rather than the LaTeX-specific 86 mm column setting. The figure width itself fits within the 178 mm double-column format and is not, on its own, a violation. The page measures 594.710 × 781.910 pt (209.80 × 275.84 mm). Body font is 7.5 pt. The two figures both span the current text width; their approximate displayed heights are 53.5 and 59.4 mm.

Cause location: `/tmp/bwt-appnote/submission/build.py:30,34` uses `width=\textwidth` with the template’s `large` option without Bioinformatics-specific column dimensions. This is a concrete journal-style mismatch, not evidence of a failed four-page limit: the actual main PDF is **3 pages**. Format-free initial submission is allowed; rectify dimensions before claiming template compliance/revision readiness and recheck pagination afterward.

### W2 — Medium: small figure type and overlapping annotations

`/tmp/bwt-appnote/submission/manuscript.pdf`, page 3: main Figure 1 axis titles are **3.806 pt**, small notes **3.021 pt**, logarithmic superscripts **2.442 pt**; Figure 2 axis titles **4.294 pt**, ticks/legend approximately **3.936 pt**. Both captions are **6 pt**. These are substantially smaller than body text and difficult at physical print size. The linked `/tmp/bwt-final-check/figure-accessibility.pdf`, p10, recommends 12–14 pt **“if possible”**; p3 acknowledges project constraints. This is a readability recommendation, **not a mandatory 8 pt minimum or automatic rejection criterion**. Increasing only to 178 mm would enlarge them just 3.7%.

Figure 1A has a measurable actual collision: two `1.77×` annotations occupy PDF rectangles `(147.467,85.979,159.123,90.410)` and `(147.467,87.133,159.123,91.564)` pt: **3.277 pt vertical overlap**, visible in the rendering. Separate those labels and enlarge figure typography/reflow panels. This applies to the identical Supplementary Figure 2 artwork (`/tmp/bwt-appnote/submission/supplementary.pdf`, page 13) too.

**No current main-figure axis-label or caption clipping found.** In particular, Figure 2’s bottom axis titles are complete at y=688.784–693.783 pt, above its caption at y≈705.10 pt. Older local preview images are not authoritative for this result.

### W3 — Medium: supplemental figure numbering and detached legends

`/tmp/bwt-appnote/submission/supplementary.pdf` has Pandoc-generated secondary numbers: page 13 says **“Figure 1: Supplementary Figure 2”**; page 19 **“Figure 4: Supplementary Figure 1”**; page 29 **“Figure 6: Supplementary Figure S2.”** All seven images have this extra numbering scheme. The intended Supplementary identifiers remain present, so these are confusing labels, **not missing destinations**.

Full legends are separated from their images for Supplementary Figures 2 (**legend p12/image p13**), S1 (**p14/p15**), 4 (**p22/p23**), S2 (**p26/p29**), and 5 (**p31/p32**). Figures 3 and 1 retain adjacent full legends on pages 16 and 19. Relevant source image/legend pairs: `/tmp/bwt-appnote/supplementary.md:105–107,115–117,202–204,258–260,338–340`; conversion at `/tmp/bwt-appnote/submission/build.py:71–75`. Keep each intended label/full legend with its image and suppress the redundant automatic caption. Main figures, by contrast, are embedded on page 3 with adjacent correct captions; a figure-only page is not itself a broken inline image.

### W4 — Medium: supplemental headings render as literal Markdown

`/tmp/bwt-appnote/submission/supplementary.pdf`, page 8, visibly prints `## 2.2.2 Genome Assemblies` and `## 2.2.3 Evaluation Metrics` **inside prose**, rather than as headings. Sources: `/tmp/bwt-appnote/supplementary.md:79,81`; missing blank separation before headings under the current Pandoc Markdown reader causes this. There are **22 literal `##` occurrences across 14 pages**. Section text remains present, but cross-reference navigation/readability is impaired. The preservation validator does not certify correct heading rendering.

### W5 — Low/medium: accessibility recommendation, pale legend markers

`/tmp/bwt-appnote/submission/manuscript.pdf`, p3, Figure 2C: TRF/TRASH legend markers use RGB `#8C7BA8`/`#A9AFB8` with **0.30 opacity**. Composited against white, WCAG relative-luminance contrast is approximately **1.405:1 / 1.239:1**, below the linked guide’s **3:1 non-text recommendation** (accessibility PDF p7). Competitor legend markers are circles; distinct symbols or dash patterns would add redundancy beyond colour. This is a targeted accessibility finding, not a full colour-vision certification or submission-rejection rule. Reproduce with `get_drawings()` on main p3: marker rectangles x≈466.849–468.894, y≈578.197–580.241 (TRF) and 595.908–597.953 (TRASH); inspect `color` and `stroke_opacity`, composite RGB as `0.3*RGB+0.7`, then apply WCAG sRGB linearization and `(1.05)/(luminance+0.05)`.

### Production note — not an initial-submission blocker

Main figures are **mixed vector/raster PDFs**, not inherently “300 dpi.” Actual embedded image components on main page 3 are **794 ppi** (Figure 1) and **704 ppi** (Figure 2), while text and other elements remain vector. No main raster falls below the 350 dpi colour target. This does not certify 1200 dpi line-art preparation for rasterized components.

The seven supplemental images are embedded PNGs: widths **267.0 mm** except Figure 5 **219.44 mm**; effective resolutions respectively **510.9, 338.2, 339.7, 451.9, 513.5, 424.4, 521.6 ppi** in PDF order. Their landscape supplement sizing is not a main-column-width measurement. The two ~339 ppi images are a production consideration, not an initial-review failure. Supplied figure assets are PDF/PNG, not TIFF; prepare/confirm production deliverables when requested. PNG metadata often says 96 dpi, but that does not determine resolution after layout scaling.

## Passed checks and limits

- All text-span, drawing-path and image rectangles are within page bounds (0.5 pt tolerance), across **3 main + 45 supplementary pages**; no U+FFFD replacement characters. Main visual review found no off-page text. Page-1 grey square and near-edge coloured rules are template artwork, not broken image links. Cropped legacy figure text remains extractable in places but is not visibly printed; do not mistake it for caption overprinting.
- Main Figure 1 → Supplementary Figure 2 (image p13); main Figure 2 → Supplementary Figure 1 (p19). Main references to Supplementary Sections 2.1/2.2/3.2 resolve to text on pp3/6/21; Methods S1/S2 to pp36/39; Table 1b to p18 and Table 2 to p22. All cited supplemental figure/table/section identifiers were found. These references are plain text, not clickable internal PDF destinations; neither PDF has internal link annotations.
- All Markdown image paths exist: **2 main, 7 supplement, 1 archived full-source**. Both DOCX archives pass CRC checks; **2/7 embedded media files**, no missing internal relationship targets; supplemental DOCX contains **19 tables**. Main DOCX image extents are 148.167 mm, a separate format-free layout, not evidence of Word page count.
- Read-only conversion validator rerun passed: **19 table blocks**, complete supplemental prose replay, **2/7 figures** and receipt/hash checks.

## Rerunnable checks (read-only)

```sh
cd /tmp/bwt-appnote
python docs/2026-09-10-appnote/check_conversion.py
pdfinfo submission/manuscript.pdf
pdfimages -list submission/manuscript.pdf
pdfimages -list submission/supplementary.pdf
pdftotext -layout submission/supplementary.pdf -
```

For geometry/type, use PyMuPDF `page.get_text('dict')` spans (`size`, `bbox`), `page.get_image_info()` (`width`, `height`, `bbox`), `page.get_drawings()` and `page.get_links()`. Convert points to mm with `*25.4/72`; raster ppi is `pixel_width*72/bbox_width`. Main p2 full justified lines bound columns at x≈54.534–288.902 and 306.838–541.205 pt; p3 `get_xobjects()` plus content-stream transforms reproduce figure widths. Render current PDFs with `get_pixmap()` for visual confirmation. DOCX checks: Python `zipfile.ZipFile.testzip()`, verify each non-external `.rels` target exists, count `word/media/*` and `w:tbl` elements in `word/document.xml`.
