from __future__ import absolute_import

from fanstatic import Group
from fanstatic import Library
from fanstatic import Resource

library = Library("kotti_agora", "static")
kotti_agora_css = Resource(library, "style.css")
kotti_agora_group = Group([kotti_agora_css])
