from __future__ import annotations

from pathlib import Path
import sys

DOCS = Path(__file__).resolve().parent
ROOT = DOCS.parent
sys.path.insert(0, str(ROOT))

project = 'training-manager'
author = 'Nesbitt'
copyright = '2026, Nesbitt'
release = '0.1.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx_rtd_theme',
]

templates_path = ['_templates'] if (DOCS / '_templates').exists() else []
source_suffix = '.rst'
master_doc = 'index'
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
pygments_style = 'sphinx'

html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'collapse_navigation': False,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    'flyout_display': 'hidden',
    'version_selector': False,
    'language_selector': False,
}
html_static_path = ['_static'] if (DOCS / '_static').exists() else []
html_last_updated_fmt = '%b %d, %Y'
html_show_sphinx = True
html_show_copyright = True
html_copy_source = True
html_show_sourcelink = True
html_use_index = True
html_domain_indices = True
html_short_title = 'training-manager'
html_context = {
    'display_github': True,
    'github_user': 'Nesbitt-bot',
    'github_repo': 'training-manager',
    'github_version': 'main',
    'conf_py_path': '/docs/',
}

autodoc_member_order = 'bysource'
