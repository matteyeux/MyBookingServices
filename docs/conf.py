# Config file for Sphinx Doc
import sys
import os
import subprocess
from recommonmark.parser import CommonMarkParser

project = "MyBookingServices"
copyright = "2021, Bombarman Gang"
author = "Bombarman Gang"


# add 
sys.path.append("../APIs/booking")
current_path = os.getcwd()

# module to add to path for autodoc
modules = [
    "booking",
    #"users",
    #"management",
]

for module in modules:
    # add to PATH to generate autodoc
    sys.path.append(f"../APIs/{module}")

    # cd to dir and run poetry install
    os.chdir(f"../APIs/{module}")
    subprocess.Popen(['poetry', 'install']).wait()

    # cd back to current dir
    os.chdir(current_path)


version = "1.0"

# -- General configuration ---------------------------------------------------
needs_sphinx = "3.0"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx_click.ext",
    "sphinxcontrib.contentui",
    "sphinx_copybutton",
]


templates_path = ["_templates" "."]
source_suffix = {
    ".rst": "restructuredtext",
    ".txt": "markdown",
    ".md": "markdown",
}

master_doc = "index"
language = "en"
exclude_patterns = [
    "_build",
    "build",
    "Thumbs.db",
    ".DS_Store",
    "env",
    ".gitignore",
    "Makefile",
    "requirements.txt",
    "README.md",
]
pygments_style = "colorful"

# -- Options for HTML output -------------------------------------------------

html_theme = "pydata_sphinx_theme"
html_theme_options = {
    "show_prev_next": False,
    "github_url": "https://github.com/matteyeux/netmon",
    "twitter_url": "https://twitter.com/big_ben_clock",  # idk pretty cool bot
}

html_sidebars = {"**": ["globaltoc.html"]}


# workaround to remove multiple build warnings caused by upstream bug.
class CustomCommonMarkParser(CommonMarkParser):
    def visit_document(self, node):
        pass


def setup(app) -> None:
    app.add_source_parser(CustomCommonMarkParser)
