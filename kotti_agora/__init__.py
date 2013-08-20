from kotti.resources import get_root
from kotti.util import extract_from_settings
from kotti_agora.models import Forum
from pyramid.i18n import TranslationStringFactory

_ = TranslationStringFactory('kotti_agora')

import logging
logger = logging.getLogger("%s: " % str(__name__))

def kotti_configure(settings):
    settings['kotti.fanstatic.view_needed'] += (
        ' kotti_agora.fanstatic.kotti_agora_group')
    settings['kotti.available_types'] += (
        ' kotti_agora.models.Idea kotti_agora.models.Forum')
    settings['pyramid.includes'] += ' kotti_agora kotti_agora.views'

def populate():

    logger.info("populate: ")
    root = get_root()
    root.default_view = 'agora_front_page_view'
    if 'forum' not in root.keys():
        forum = Forum(title=u'Forum')
        root['forum'] = forum
        logger.info("populate: forum: %s" % str(forum))

def check_true(value):
    if value == u'true':
        return True
    return False

AGORA_DEFAULTS = {
    'use_batching': 'true',
    'pagesize': '5',
    'use_auto_batching': 'true',
    'link_headline_overview': 'true',
    }

def agora_settings(name=''):
    prefix = 'kotti_agora.agora_settings.'
    if name:
        prefix += name + '.' # pragma: no cover
    settings = AGORA_DEFAULTS.copy()
    settings.update(extract_from_settings(prefix))
    settings['use_batching'] = check_true(settings['use_batching'])
    try:
        settings['pagesize'] = int(settings['pagesize'])
    except ValueError:
        settings['pagesize'] = 5
    settings['use_auto_batching'] = check_true(settings['use_auto_batching'])
    settings['link_headline_overview'] = check_true(settings['link_headline_overview'])

    return settings

def includeme(config):
    """"""
    logger.info("includeme: ")
