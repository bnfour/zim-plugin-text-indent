#!/usr/bin/env python

# A plugin to enable vscode-like indentation hotkeys ctrl-[ and ctrl-]
# https://github.com/bnfour/zim-plugin-text-indent for more details
# MIT license

from typing import Callable

from zim.actions import action
from zim.gui.pageview import PageViewExtension, TextBuffer
from zim.plugins import PluginClass

# we don't care what it is returning though, let it silently fail if it's unable
# to indent a given line (like a header)
type Action = Callable[[TextBuffer, int], bool]

class BnIndentPlugin(PluginClass):
    plugin_info = {
        'name': _('Indent'),
        'description': _('VS Code-like indentation with Ctrl-[ and Ctrl-]'),
        'author': 'bnfour'
    }

class BnIndentExtension(PageViewExtension):

    def __init__(self, plugin, pageview):
        super().__init__(plugin, pageview)

        self._indent_action : Action = lambda buf, line :\
            buf.set_indent(line, buf.get_indent(line) + 1, False)
        self._outdent_action : Action = lambda buf, line :\
            buf.set_indent(line, max(0, buf.get_indent(line) - 1), False)

    # see https://gitlab.gnome.org/GNOME/gtk/-/blob/main/gdk/gdkkeysyms.h
    # for the key names for accelerators

    @action(_('Indent Line(s)'), accelerator='<ctrl>bracketright', menuhints='edit')
    def indent(self):
        self._dent(self._indent_action)

    @action(_('Outdent Line(s)'), accelerator='<ctrl>bracketleft', menuhints='edit')
    def outdent(self):
        self._dent(self._outdent_action)

    def _dent(self, action: Action):
        """
        Common method that applies the appropriate action to a range of lines.
        """
        buf = self.pageview.textview.get_buffer()
        for line in self._get_affected_lines(buf):
            action(buf, line)

    @staticmethod
    def _get_affected_lines(buf: TextBuffer) -> range:
        """
        Returns the range of line indices to be affected. If text selection is
        present, all lines touched by it are included. Without selection, only
        the line with the cursor in it is included.
        """
        if buf.get_has_selection():
            selection_start, selection_end = buf.get_selection_bounds()
            start, end = selection_start.get_line(), selection_end.get_line()
            # unless the last line is a trailing newline, extend the range
            # to include it
            if not selection_end.starts_line():
                end += 1
            return range(start, end)
        else:
            line = buf.get_insert_iter().get_line()
            return range(line, line + 1)
