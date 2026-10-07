"""Build the Elementor template JSON for the F&A Hospitality Calculators page.

Run:  python3 tools/build_template.py
Output: elementor-template/fa-hospitality-calculators.json
"""
import json, random, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
random.seed(42)


def uid():
    return "%07x" % random.getrandbits(28)


def px(t, r=None, b=None, l=None):
    r = t if r is None else r
    b = t if b is None else b
    l = r if l is None else l
    return {"unit": "px", "top": str(t), "right": str(r), "bottom": str(b), "left": str(l), "isLinked": False}


def typo(family, size, weight, lh=None, ls=None, size_m=None):
    d = {"typography_typography": "custom", "typography_font_family": family,
         "typography_font_size": {"unit": "px", "size": size}, "typography_font_weight": str(weight)}
    if lh: d["typography_line_height"] = {"unit": "em", "size": lh}
    if ls is not None: d["typography_letter_spacing"] = {"unit": "px", "size": ls}
    if size_m: d["typography_font_size_mobile"] = {"unit": "px", "size": size_m}
    return d


def container(name, children, inner=False, **s):
    base = {"_title": name, "content_width": "boxed" if not inner else "full",
            "flex_direction": "column", "flex_gap": {"unit": "px", "size": 16, "column": "16", "row": "16", "isLinked": True}}
    if not inner:
        base["boxed_width"] = {"unit": "px", "size": 1172}
    base.update(s)
    return {"id": uid(), "elType": "container", "isInner": inner, "settings": base, "elements": children}


def widget(kind, settings):
    return {"id": uid(), "elType": "widget", "widgetType": kind, "isInner": False, "settings": settings, "elements": []}


def heading(text, tag, size, color, size_m=None, align="left", ls=-1.3):
    return widget("heading", {"title": text, "header_size": tag, "align": align, "title_color": color,
                              **typo("Plus Jakarta Sans", size, 800, 1.15, ls, size_m)})


def eyebrow(text, color="#E96C20", align="left"):
    return widget("heading", {"title": text, "header_size": "div", "align": align, "title_color": color,
                              "typography_text_transform": "uppercase",
                              **typo("Inter", 12.5, 700, 1.4, 1.5)})


def text(html, color="#475569", size=16.8, align="left"):
    return widget("text-editor", {"editor": html, "text_color": color, "align": align,
                                  **typo("Inter", size, 400, 1.7)})


def button(label, url, cls="fa-btn"):
    return widget("button", {"text": label, "link": {"url": url, "is_external": "on", "nofollow": ""},
                             "background_color": "#E96C20", "button_text_color": "#FFFFFF",
                             "button_background_hover_color": "#D55D15", "hover_color": "#FFFFFF",
                             "border_radius": px(10), "text_padding": {"unit": "px", "top": "13.6", "right": "28.8", "bottom": "13.6", "left": "28.8", "isLinked": False},
                             "_css_classes": cls, **typo("Inter", 15.68, 600)})


FAQ = [
    ("Is VAT on restaurant food 20%?",
     "Food eaten on your premises is standard-rated at 20%. Hot takeaway food is also 20%. Most cold takeaway food, such as a sandwich to go, is zero-rated. Alcohol and soft drinks are 20% whether eaten in or taken away."),
    ("What is a good GP% for a restaurant?",
     "Many UK restaurants aim for a food gross profit of around 65–70% and a drinks gross profit of 70% or more. The right target depends on your menu, pricing and concept."),
    ("What is prime cost?",
     "Prime cost is your food and drink costs plus your labour costs. Many hospitality businesses aim to keep it under 60–65% of sales, so there is enough left for rent, bills and profit."),
    ("How much does it cost to employ someone in the UK in 2026/27?",
     "On top of gross pay, you pay employer National Insurance at 15% on earnings over £5,000 a year, plus at least 3% employer pension on qualifying earnings. Many small employers can claim Employment Allowance of up to £10,500 a year against their employer NI."),
    ("Are these calculators tax advice?",
     "No. They give estimates for guidance. Speak to an F&amp;A hospitality accountant for advice on your own figures."),
]

faq_schema = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a.replace("&amp;", "&")}} for q, a in FAQ]}

embed = (ROOT / "elementor-embed.html").read_text()

SECTION_PAD = dict(padding=px(96, 24), padding_tablet=px(96, 24), padding_mobile=px(72, 18))

content = [
    # Hero
    container("Hero – Main", [
        container("Hero – Header", [
            eyebrow("Free tools for hospitality"),
            heading("Hospitality calculators for UK restaurants, pubs and cafés", "h1", 51.2, "#FFFFFF", 34),
            text("<p>Work out VAT, gross profit and prime cost, or the real cost of a new hire in seconds. Built by specialist hospitality accountants, using 2026/27 UK tax rates.</p>", "#B9C6D8"),
        ], inner=True, flex_gap={"unit": "px", "size": 14, "column": "14", "row": "14", "isLinked": True},
            width={"unit": "%", "size": 70}, width_tablet={"unit": "%", "size": 100}),
    ], background_background="gradient", background_color="#091F3C", background_color_b="#0A1E38",
        background_gradient_angle={"unit": "deg", "size": 160},
        padding=px(88, 24, 92.8), padding_mobile=px(48, 18, 56)),

    # Calculators
    container("Calculators – Main", [
        container("Calculators – Header", [
            eyebrow("Calculators"),
            heading("Check your numbers", "h2", 44, "#123560", 30),
            text("<p>Pick a calculator below. Every figure updates as you type.</p>"),
        ], inner=True),
        container("Calculators – Content", [
            widget("html", {"html": embed, "_title": "F&A – Calculators embed"}),
        ], inner=True, _css_classes="fa-lp"),
    ], background_background="classic", background_color="#F8FAFD", **SECTION_PAD),

    # FAQ
    container("FAQ – Main", [
        container("FAQ – Header", [
            eyebrow("FAQ"),
            heading("Common questions", "h2", 44, "#123560", 30),
        ], inner=True),
        container("FAQ – Content", [
            widget("toggle", {"tabs": [{"_id": uid(), "tab_title": q, "tab_content": "<p>" + a + "</p>"} for q, a in FAQ],
                              "_css_classes": "fa-faq", "title_color": "#123560", "tab_active_color": "#E96C20",
                              "content_color": "#475569", "icon_align": "right",
                              "selected_icon": {"value": "fas fa-plus", "library": "fa-solid"},
                              "selected_active_icon": {"value": "fas fa-minus", "library": "fa-solid"},
                              "title_typography_typography": "custom", "title_typography_font_family": "Plus Jakarta Sans",
                              "title_typography_font_weight": "700"}),
            widget("html", {"html": '<script type="application/ld+json">' + json.dumps(faq_schema) + "</script>",
                            "_title": "F&A – FAQ schema (no content in here)"}),
        ], inner=True),
    ], background_background="classic", background_color="#FFFFFF", **SECTION_PAD),

    # CTA
    container("CTA – Main", [
        container("CTA – Card", [
            heading("Want these numbers to look better?", "h2", 32, "#123560", 26, align="center", ls=-0.8),
            text("<p>F&amp;A Accountants work with hospitality businesses on VAT, GP, payroll and tronc every week. Talk to a specialist about your figures.</p>", align="center"),
            button("Book a free consultation", "https://faaccountants.com/hospitality-accounting-services/"),
        ], inner=True, _css_classes="fa-cta-blob", align_items="center", flex_align_items="center",
            background_background="classic", background_color="#FFF5EE",
            border_border="solid", border_width=px(1), border_color="#FFD9C2", border_radius=px(24),
            padding=px(56, 32), padding_mobile=px(40, 20)),
    ], background_background="classic", background_color="#FFFFFF",
        padding=px(0, 24, 80), padding_mobile=px(0, 18, 56)),
]

template = {
    "content": content,
    "page_settings": {"hide_title": "yes"},
    "version": "0.4",
    "title": "F&A – Hospitality Calculators (Native Elementor)",
    "type": "page",
}

out = ROOT / "elementor-template" / "fa-hospitality-calculators.json"
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps(template, indent=2, ensure_ascii=False))
print("wrote", out, out.stat().st_size, "bytes")
