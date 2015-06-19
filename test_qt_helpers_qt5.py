from __future__ import absolute_import, division, print_function

import os
import sys

import pytest
from mock import MagicMock


# At the moment it is not possible to have PyQt5 and PyQt4 installed
# simultaneously because one requires the Qt4 libraries while the other
# requires the Qt5 libraries

class TestQT5(object):

    def setup_class(cls):
        os.environ['QT_API'] = 'pyqt5'
        import qt_helpers as qt

    def _load_qt5(self):
        import qt_helpers as qt

    def test_main_import_qt5(self):

        self._load_qt5()

        from qt_helpers import QtCore
        from qt_helpers import QtGui

        from PyQt5 import QtCore as core, QtGui as gui
        assert QtCore is core
        assert QtGui is gui

    # At the moment, PyQt5 does not run correctly on Travis so we can't run
    # this without causing an Abort Trap.
    # def test_load_ui_qt5(self):
    #     self._load_qt5()
    #     from qt_helpers import load_ui, get_qapp
    #     qpp = get_qapp()
    #     load_ui('test.ui')

    def test_submodule_import_qt5(self):

        self._load_qt5()

        from qt_helpers.QtGui import QMessageBox
        from qt_helpers.QtCore import Qt

        from PyQt5.QtWidgets import QMessageBox as qmb
        from PyQt5.QtCore import Qt as _qt
        assert qmb is QMessageBox
        assert _qt is Qt
