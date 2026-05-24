from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

project = 'training-manager'
author = 'Nesbitt'
release = '0.1.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'alabaster'
html_static_path = ['_static']
html_title = 'training-manager documentation'
html_theme_options = {
    'description': 'Host-native web UI for long-running Python and notebook jobs',
    'fixed_sidebar': True,
    'show_relbars': True,
}

autodoc_member_order = 'bysource'
