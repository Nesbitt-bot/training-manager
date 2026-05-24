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
]

templates_path = ['_templates'] if (DOCS / '_templates').exists() else []
source_suffix = '.rst'
master_doc = 'index'
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
pygments_style = 'sphinx'

html_theme = 'classic'
html_static_path = ['_static'] if (DOCS / '_static').exists() else []
html_last_updated_fmt = '%b %d, %Y'
html_show_sphinx = False
html_show_copyright = True
html_copy_source = True
html_use_index = True
html_domain_indices = True
html_short_title = 'training-manager'

autodoc_member_order = 'bysource'
