# Tests common to all Qt packages

import qt_helpers


def test_patched_qcombobox():

    # This test ensures that patch_qcombobox works correctly. See the comments
    # in that function to understand the issue.

    # The __getitem__ is needed in order to reproduce the Segmentation Fault
    class Data(object):
        def __getitem__(self, item):
            raise ValueError("Failing")

    data1 = Data()
    data2 = Data()
    data3 = Data()
    data4 = Data()
    data5 = Data()
    data6 = Data()

    icon1 = qt_helpers.QtGui.QIcon()
    icon2 = qt_helpers.QtGui.QIcon()

    app = qt_helpers.get_qapp()

    widget = qt_helpers.QtGui.QComboBox()
    widget.addItem('a', data1)
    widget.insertItem(0, 'b', data2)
    widget.addItem('c', data1)
    widget.setItemData(2, data3)
    widget.addItem(icon1, 'd', data4)
    widget.insertItem(3, icon2, 'e', data5)

    widget.show()

    assert widget.findData(data1) == 1
    assert widget.findData(data2) == 0
    assert widget.findData(data3) == 2
    assert widget.findData(data4) == 4
    assert widget.findData(data5) == 3
    assert widget.findData(data6) == -1

    assert widget.itemData(0) == data2
    assert widget.itemData(1) == data1
    assert widget.itemData(2) == data3
    assert widget.itemData(3) == data5
    assert widget.itemData(4) == data4

    assert widget.itemText(0) == 'b'
    assert widget.itemText(1) == 'a'
    assert widget.itemText(2) == 'c'
    assert widget.itemText(3) == 'e'
    assert widget.itemText(4) == 'd'


def test_main_import():
    from qt_helpers import QtCore
    from qt_helpers import QtGui


def test_submodule_import():
    from qt_helpers.QtGui import QMessageBox
    from qt_helpers.QtCore import Qt


def test_load_ui():
    from qt_helpers import load_ui, get_qapp
    qpp = get_qapp()
    load_ui('test.ui')
