# mkdocs-pug

This MkDocs plugin is based on [pypugjs](https://github.com/kakulukia/pypugjs).

To install:

```
pip install mkdocs_pug
```

To use, add this to your `mkdocs.yml`:


```
plugins:
  - mkdocs_pug
```

Then, this plugin will watch for `*.pug` files in your template directories and build the corresponding `*.html` files in the same location.

To do this automatically with the server during development, you should run with

```
mkdocs serve --watch-theme
```

This repo contains an example of how to use this plugin inside an MkDocs project.
