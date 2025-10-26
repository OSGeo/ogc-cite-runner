# foss4g 2025 slides

These are to be built with [mkslides](https://github.com/MartenBE/mkslides), which can be installed using pipx:

```shell
pipx install mkslides
```

Or alternatively, creating a virtualenv and installing it there:

```shell
python3 -m venv .venv
source .venv/bin/activate
pip install mkslides
```

Start the dev server for mkslides:

```mkslides serve slides.md```

The slides shall now be available at <http://localhost:8000>

Author the slides at will and enjoy the live reloading


### Export slides to pdf

PDF export instructions are detailed at [revealjs website](https://revealjs.com/pdf-export/). Succinctly, add 
the `print-pdf` query parameter to the browser URL bar (_i.e._ visit <http://localhost:8000?print-pdf>) then open
the print settings (ctrl + p), remove the margins and add the background and print to PDF.


