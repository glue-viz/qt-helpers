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

    app = qt_helpers.get_qapp()

    widget = qt_helpers.QtGui.QComboBox()
    widget.addItem('a', data1)
    widget.insertItem(0, 'b', data2)
    widget.addItem('c', data1)
    widget.setItemData(2, data3)
    widget.show()

    assert widget.findData(data1) == 1
    assert widget.findData(data2) == 0
    assert widget.findData(data3) == 2
    assert widget.findData(data4) == -1

    assert widget.itemData(0) == data2
    assert widget.itemData(1) == data1
    assert widget.itemData(2) == data3
