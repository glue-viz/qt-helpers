from __future__ import absolute_import, division, print_function

import os
import sys

import qt_helpers as qt

import pytest
from mock import MagicMock

from imp import reload


class TestQT(object):

    def teardown_class(cls):
        for m in sys.modules.keys():
            if m.startswith('PyQt4') or m.startswith('PySide'):
                sys.modules.pop(m)

    def setup_method(self, method):
        qt.deny_module(None)
        if 'QT_API' in os.environ:
            os.environ.pop('QT_API')

    def test_defaults_to_qt4(self):
        reload(qt)
        assert qt.QT_API == qt.QT_API_PYQT

    def _load_qt4(self):
        os.environ['QT_API'] = qt.QT_API_PYQT
        reload(qt)

    def _load_pyside(self):
        os.environ['QT_API'] = qt.QT_API_PYSIDE
        reload(qt)

    def test_overridden_with_env(self):
        os.environ['QT_API'] = qt.QT_API_PYSIDE
        reload(qt)
        assert qt.QT_API == qt.QT_API_PYSIDE

    def test_main_import(self):
        self._load_qt4()
        from qt_helpers import QtCore
        from qt_helpers import QtGui

        from PyQt4 import QtCore as core, QtGui as gui
        assert QtCore is core
        assert QtGui is gui

        self._load_pyside()
        from qt_helpers import QtCore
        from qt_helpers import QtGui

        from PySide import QtCore as core, QtGui as gui
        assert QtCore is core
        assert QtGui is gui

    def test_submodule_import(self):
        self._load_qt4()
        from qt_helpers.QtGui import QMessageBox
        from qt_helpers.QtCore import Qt
        from PyQt4.QtGui import QMessageBox as qmb
        from PyQt4.QtCore import Qt as _qt
        assert qmb is QMessageBox
        assert _qt is Qt

        self._load_pyside()
        from qt_helpers.QtGui import QMessageBox
        from qt_helpers.QtCore import Qt

        from PySide.QtGui import QMessageBox as qmb
        from PySide.QtCore import Qt as _qt
        assert qmb is QMessageBox
        assert _qt is Qt

    def test_signal_slot_property(self):
        self._load_qt4()
        from qt_helpers.QtCore import Signal, Slot, Property

    def test_qt4_unavailable(self):
        import PyQt4
        try:
            sys.modules['PyQt4'] = None
            self._load_qt4()
            assert qt.QT_API == qt.QT_API_PYSIDE
        finally:
            sys.modules['PyQt4'] = PyQt4

    def test_pyside_unavailable(self):
        import PySide
        try:
            sys.modules['PySide'] = None
            self._load_pyside()
            assert qt.QT_API == qt.QT_API_PYQT
        finally:
            sys.modules['PySide'] = PySide

    def test_both_unavailable(self):
        import PySide
        import PyQt4
        try:
            sys.modules['PySide'] = None
            sys.modules['PyQt4'] = None
            with pytest.raises(ImportError) as e:
                reload(qt)
        finally:
            sys.modules['PySide'] = PySide
            sys.modules['PyQt4'] = PyQt4
