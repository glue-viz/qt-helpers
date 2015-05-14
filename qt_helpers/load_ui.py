from .core import is_pyside

__all__ = ['load_ui']

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
