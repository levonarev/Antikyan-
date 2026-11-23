# Antikyan Gallery

The website of Antikyan Gallery, Yerevan, served at [antikyan.com](https://antikyan.com)
through GitHub Pages.

The site is one page in four languages: English (`/`), Armenian (`/hy/`), Italian (`/it/`)
and Russian (`/ru/`).

## Editing

The four `index.html` files are generated. Do not edit them by hand.

- Text in every language: `src/i18n.json`
- Layout: `src/template.html`
- Styles: `style.css`
- Images: `img/`

After a change, rebuild the pages:

```
python3 src/build.py
```
