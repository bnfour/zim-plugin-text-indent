from zim.plugins import PluginClass

class BnIndentPlugin(PluginClass):
    plugin_info = {
        'name': _('Indent'),
        'description': _('VS Code-like indentation with Ctrl-[ and Ctrl-]'),
        'author': 'bnfour'
    }

# TODO pageviewext that actually indents
