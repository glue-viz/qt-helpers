# qt-helpers

A common front-end to PySide, PyQt4, and PyQt5 (experimental)

With this module, you can import the ``QtGui`` and ``QtCore`` submodules from
``qt_helpers``, and it will automatically pick one between PyQt4 and PySide:

    from qt_helpers import QtGui, QtCore

By default, ``qt_helpers`` will first try and import from PyQt4, then PySide.
To explicitly force which backend package to use, you can set the ``QT_API``
environment variable to ``'pyqt'`` or ``'pyside'``.

Note that when using ``qt_helpers``, the QString API is always set to version
2.

If you want to know which backend is being used, you can use the ``is_pyqt``
and ``is_pyside`` functions.
