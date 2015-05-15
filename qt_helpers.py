"""
This module provides a way to import from Python Qt wrappers in a uniform
way, regardless of whether PySide or PyQt is used.

This file lovingly borrows from the IPython and python_qt_binding project

https://github.com/ipython/ipython/blob/master/IPython/external/qt.py
https://github.com/ros-visualization/python_qt_binding/

See also this discussion

http://qt-project.org/wiki/Differences_Between_PySide_and_PyQt

Do not use this if you need PyQt with the old QString/QVariant API.
"""

from __future__ import absolute_import, division, print_function

import os
import sys

__all__ = ['QtCore', 'QtGui', 'is_pyside', 'is_pyqt', 'load_ui']

# Available APIs.
QT_API_PYQT = 'pyqt'
QT_API_PYSIDE = 'pyside'
QT_API = None


class ImportDenier(object):
    """
    Import hook to protect importing of both PySide and PyQt4.
    """
    
    __forbidden = set()

    def __init__(self):
        self.__forbidden = None

    def forbid(self, module_name):
        self.__forbidden = module_name

    def find_module(self, mod_name, pth):
        if pth:
            return
        if mod_name == self.__forbidden:
            return self

    def load_module(self, mod_name):
        raise ImportError("Importing %s forbidden by %s"
                          % (mod_name, __name__))


_import_hook = ImportDenier()
sys.meta_path.append(_import_hook)


def prepare_pyqt4():
    # For PySide compatibility, use the new-style string API that 
    # automatically converts QStrings to Unicode Python strings. Also, 
    # automatically unpack QVariants to their underlying objects.
    import sip
    sip.setapi('QString', 2)
    sip.setapi('QVariant', 2)


def register_module(module, modlabel):
    """
    Register an imported module into a submodule of qt_helpers.
    
    This enables syntax such as:
    
        >>> from qt_helpers.QtGui import QMessageBox
    """
    sys.modules[__name__ + '.' + modlabel] = module


def deny_module(mod_name):
    _import_hook.forbid(mod_name)


def _load_pyqt4():

    prepare_pyqt4()

    from PyQt4 import QtCore, QtGui, QtTest
    from distutils.version import LooseVersion

    if LooseVersion(QtCore.PYQT_VERSION_STR) < LooseVersion('4.8'):
        raise ImportError("Glue Requires PyQt4 >= 4.8")

    QtCore.Signal = QtCore.pyqtSignal
    QtCore.Slot = QtCore.pyqtSlot
    QtCore.Property = QtCore.pyqtProperty

    from PyQt4.QtGui import QFileDialog
    QFileDialog.getOpenFileName = QFileDialog.getOpenFileNameAndFilter
    QFileDialog.getSaveFileName = QFileDialog.getSaveFileNameAndFilter

    register_module(QtCore, 'QtCore')
    register_module(QtGui, 'QtGui')
    register_module(QtTest, 'QtTest')

    global QT_API
    QT_API = QT_API_PYQT

    deny_module('PySide')


def _load_pyside():

    from PySide import QtCore, QtGui, __version__, QtTest

    if __version__ < '1.0.3':
        # old PySide, fallback on PyQt
        raise ImportError("Glue requires PySide >= 1.0.3")

    register_module(QtCore, 'QtCore')
    register_module(QtGui, 'QtGui')
    register_module(QtTest, 'QtTest')

    def setMargin(self, x):
        self.setContentsMargins(x, x, x, x)
    QtGui.QLayout.setMargin = setMargin

    global QT_API
    QT_API = QT_API_PYSIDE

    deny_module('PyQt4')

loaders = [_load_pyqt4, _load_pyside]
if os.environ.get('QT_API') == QT_API_PYSIDE:
    loaders = loaders[::-1]

msgs = []

# acutally do the loading
for loader in loaders:
    try:
        loader()
        # we set this env var, since IPython also looks for it
        os.environ['QT_API'] = QT_API
        QtCore = sys.modules[__name__ + '.QtCore']
        QtGui = sys.modules[__name__ + '.QtGui']
        break
    except ImportError as e:
        msgs.append(str(e))
        pass
else:
    raise ImportError("Could not find a suitable QT installation."
                      " Encountered the following errors: %s" %
                      '\n'.join(msgs))


def is_pyside():
    return QT_API == QT_API_PYSIDE


def is_pyqt():
    return QT_API == QT_API_PYQT


def load_ui(path, parent=None, custom_widgets=None):
    if is_pyside():
        return _load_ui_pyside(path, parent, custom_widgets=custom_widgets)
    else:
        return _load_ui_pyqt4(path, parent)


def _load_ui_pyside(path, parent, custom_widgets=None):
    
    from PySide.QtUiTools import QUiLoader

    loader = QUiLoader()

    # must register custom widgets referenced in .ui files
    if custom_widgets is not None:
        for w in custom_widgets:
            loader.registerCustomWidget(w)

    widget = loader.load(path, parent)

    return widget


def _load_ui_pyqt4(path, parent):
    from PyQt4.uic import loadUi
    return loadUi(path, parent)
