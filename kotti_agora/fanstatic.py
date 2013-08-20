from __future__ import absolute_import

from fanstatic import Group
from fanstatic import Library
from fanstatic import Resource

from js.jquery_infinite_ajax_scroll import jquery_infinite_ajax_scroll
from js.jquery_infinite_ajax_scroll import jquery_infinite_ajax_scroll_css

from kotti.fanstatic import view_needed

library = Library("kotti_agora", "static")
kotti_agora_css = Resource(library, 
    "style.css",
    depends=[jquery_infinite_ajax_scroll_css, ],
    minified='style.min.css',
    bottom=True)
kotti_agora_js = Resource(library, 
    "kotti_agora.js",
    depends=[jquery_infinite_ajax_scroll, ],
    minified='kotti_agora.min.js',
    bottom=True)
kotti_agora_group = Group([kotti_agora_css,kotti_agora_js])
