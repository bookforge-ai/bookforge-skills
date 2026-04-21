# View Pattern Decision Matrix

Source: Patterns of Enterprise Application Architecture, Ch 14 (Fowler 2002)

## Three View Patterns at a Glance

| Dimension | Template View | Transform View | Two Step View |
|---|---|---|---|
| Organizing principle | Output (page structure) | Input (domain element types) | Two stages: logical then physical |
| Designer-editable | Yes (HTML skeleton visible) | No (code/rules structure) | Partially (stage 1 is code; stage 2 can be designed) |
| Testability | Medium (requires rendered HTML) | High (pure function: input XML → output) | High (stage 1 + stage 2 testable separately) |
| Multi-format output | Poor (one template per format) | Good (swap the transform per format) | Good (one second stage per output format) |
| Site-wide redesign cost | High (many templates to update) | Medium (many XSLT files) | Low (change only the second stage) |
| Scriptlet risk | High — the primary anti-pattern | Low (logic is in transform rules) | Low |
| Framework support | Universal (JSP, ERB, Jinja, Razor, Blade) | Moderate (XSLT engines; React SSR; serializers) | Limited (requires deliberate two-stage setup) |
| Complexity | Low | Medium | Medium-High |
| Modern equivalents | ERB, Jinja2, Razor, Thymeleaf, Blade, Handlebars | XSLT, React render(), Vue render(), JSON serializers | Next.js layouts, Rails application.html.erb + components, design-system libraries |

## Decision Criteria

### Choose Template View when:
- Non-programmers (designers, content editors) edit the templates
- The framework ships a server-page technology (virtually all do)
- Output is HTML and each screen has a distinct layout
- Team discipline can enforce the helper-object rule (no scriptlets)

### Choose Transform View when:
- Domain data is already in XML or easily converted
- The same data must be rendered in multiple formats (HTML + JSON + PDF + email)
- You want fully testable, side-effect-free rendering
- Team is comfortable with functional/transformation programming style
- Modern context: designing a JSON API response layer (serializer is a Transform View)

### Choose Two Step View when:
- Many screens share the same layout structure
- Global site-wide HTML changes must touch ONE place
- Supporting multiple "themes" or output styles from the same logical structure
- Modern context: building a design system where all pages compose from a single component library

## Combining Patterns

Two Step View is a modifier, not a replacement. You can have:
- Two Step Template View: stage 1 produces logical structure (code); stage 2 is a Template View
- Two Step Transform View: two XSLT stylesheets; stage 1 transforms domain XML to logical XML; stage 2 transforms logical XML to HTML

## Helper Object Pattern for Template View

To prevent scriptlet accumulation:
1. Controller creates a **View Model** (a plain data object with only the fields the template needs, pre-formatted)
2. Controller assigns view model to request scope
3. Template renders only: `${viewModel.albumTitle}`, no logic

The view model acts as the "helper object" Fowler describes — it absorbs all template-side logic (formatting, conditionals about what to show) and keeps the template clean.
