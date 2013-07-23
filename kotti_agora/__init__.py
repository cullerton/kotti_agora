from pyramid.i18n import TranslationStringFactory

_ = TranslationStringFactory('kotti_agora')


def kotti_configure(settings):
    settings['kotti.fanstatic.view_needed'] += ' kotti_agora.fanstatic.kotti_agora_group'
