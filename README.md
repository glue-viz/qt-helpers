
[![Build Status](https://travis-ci.org/glue-viz/glue.png)](https://travis-ci.org/glue-viz/qt-helpers?branch=master)
[![Build status](https://ci.appveyor.com/api/projects/status/lmh99ih9rkmq6vf4/branch/master?svg=true)](https://ci.appveyor.com/project/astrofrog/qt-helpers/branch/master)

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

If you want to know which backend is being used, you can use the ``is_pyqt()``
and ``is_pyside()`` functions.

Finally, a convenience ``load_ui(filename)`` function is provided to load Qt
``.ui`` files, e.g.:

    from qt_helpers import load_ui
    ui = load_ui('mywidget.ui')

If you define any custom widgets that are used in the ``.ui`` file, you
should pass them as a list or tuple to ``load_ui`` using the
``custom_widgets=`` argument.
