import riocore

from PyQt5 import QtGui, QtSvg
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QStandardItem
from PyQt5.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QLineEdit,
    QSpinBox,
)

STYLESHEET = """
    background-color: #444444;
    color: white;
"""
STYLESHEET_CHECKBOX = """
    QCheckBox::indicator::unchecked {
        background-color: lightgray;
    }
"""
STYLESHEET_BUTTON = """
    QPushButton::disabled {
        background-color: black;
    }
"""
STYLESHEET_CHECKBOX_GREEN_RED = """
    QCheckBox::indicator::checked {
        background-color: green;
    }
    QCheckBox::indicator::unchecked {
        background-color: red;
    }
"""


class MyQSvgWidget(QtSvg.QSvgWidget):
    def mousePressEvent(self, event):
        self.old_x = event.pos().x()
        self.old_y = event.pos().y()

    def mouseMoveEvent(self, event):
        mp_x = event.pos().x()
        mp_y = event.pos().y()
        diff_x = self.old_x - mp_x
        diff_y = self.old_y - mp_y
        self.old_x = mp_x
        self.old_y = mp_y
        viewbox = self.renderer().viewBox()
        x = int(viewbox.x()) + diff_x
        y = int(viewbox.y()) + diff_y
        width = int(viewbox.width())
        height = int(viewbox.height())
        self.renderer().setViewBox(QRect(int(x), int(y), int(width), int(height)))
        self.repaint()

    def wheelEvent(self, event: QtGui.QWheelEvent) -> None:
        delta = event.angleDelta()
        mp_x = event.pos().x()
        mp_y = event.pos().y()
        if delta.y() < 0:
            scale = 1.1
            diff_x = -mp_x / 10
            diff_y = -mp_y / 10
        else:
            scale = 0.9
            diff_x = mp_x / 10
            diff_y = mp_y / 10
        viewbox = self.renderer().viewBox()
        x = int(viewbox.x()) + diff_x
        y = int(viewbox.y()) + diff_y
        width = int(viewbox.width()) * scale
        height = int(viewbox.height()) * scale
        self.renderer().setViewBox(QRect(int(x), int(y), int(width), int(height)))
        self.repaint()


class MyStandardItem(QStandardItem):
    def __init__(self, txt="", font_size=12, set_bold=False, key=None, help_text=None):
        super().__init__()
        self.key = key
        if help_text:
            self.setToolTip(help_text)
        else:
            self.setToolTip(txt)
        self.setEditable(False)
        self.setText(txt)


class edit_float(QDoubleSpinBox):
    def __init__(self, win, obj, key, vmin=None, vmax=None, cb=None, help_text=None, default=None, decimals=None):
        super().__init__()
        self.win = win
        self.cb = cb
        self.obj = obj
        self.key = key
        self.default = default
        if help_text:
            self.setToolTip(help_text)
        if decimals is None:
            decimals = 3
        self.setDecimals(decimals)
        steps = 1.0
        if decimals > 1:
            for dn in range(decimals - 1):
                steps /= 10.0
            self.setSingleStep(steps)
        if vmin:
            self.setMinimum(vmin)
        else:
            self.setMinimum(-99999999)
        if vmax:
            self.setMaximum(vmax)
        else:
            self.setMaximum(99999999)
        if key in obj:
            self.setValue(float(obj[key]))
        elif default is not None:
            self.setValue(float(default))
        self.valueChanged.connect(self.change)
        self.editingFinished.connect(self.change)
        self.setFocusPolicy(Qt.StrongFocus)

    def wheelEvent(self, *args, **kwargs):
        if self.hasFocus():
            return QSpinBox.wheelEvent(self, *args, **kwargs)

    def change(self):
        if self.value() != self.default:
            self.obj[self.key] = self.value()
        elif self.key in self.obj:
            del self.obj[self.key]
        if self.cb:
            self.cb(self.value())
        else:
            self.win.display()


class edit_int(QSpinBox):
    def __init__(self, win, obj, key, vmin=None, vmax=None, cb=None, help_text=None, default=None):
        super().__init__()
        self.win = win
        self.cb = cb
        self.obj = obj
        self.key = key
        self.default = default
        if help_text:
            self.setToolTip(help_text)
        if vmin:
            self.setMinimum(vmin)
        else:
            self.setMinimum(-99999999)
        if vmax:
            self.setMaximum(vmax)
        else:
            self.setMaximum(99999999)
        if key in obj:
            self.setValue(int(obj[key]))
        elif default is not None:
            self.setValue(int(default))
        self.valueChanged.connect(self.change)
        self.editingFinished.connect(self.change)
        self.setFocusPolicy(Qt.StrongFocus)

    def wheelEvent(self, *args, **kwargs):
        if self.hasFocus():
            return QSpinBox.wheelEvent(self, *args, **kwargs)

    def change(self):
        if self.value() != self.default:
            self.obj[self.key] = self.value()
        elif self.key in self.obj:
            del self.obj[self.key]
        if self.cb:
            self.cb(self.value())
        else:
            self.win.display()


class edit_text(QLineEdit):
    def __init__(self, win, obj, key, cb=None, help_text=None, default=None):
        super().__init__()
        self.win = win
        self.cb = cb
        self.obj = obj
        self.key = key
        self.default = default
        if help_text:
            self.setToolTip(help_text)
        if key in obj:
            self.setText(str(obj[key]))
        elif default is not None:
            self.setText(str(default))
        self.textChanged.connect(self.change)

    def change(self):
        if self.text() != self.default:
            self.obj[self.key] = self.text()
        elif self.key in self.obj:
            del self.obj[self.key]
        if self.cb:
            self.cb(self.text())
        else:
            self.win.display()


class edit_bool(QCheckBox):
    def __init__(self, win, obj, key, cb=None, help_text=None, default=None):
        super().__init__()
        self.win = win
        self.cb = cb
        self.obj = obj
        self.key = key
        self.default = default
        self.setStyleSheet(STYLESHEET_CHECKBOX)
        if help_text:
            self.setToolTip(help_text)
        if key in obj:
            self.setChecked(obj[key])
        elif default is not None:
            self.setChecked(default)
        self.stateChanged.connect(self.change)

    def change(self):
        if self.isChecked() != self.default:
            self.obj[self.key] = self.isChecked()
        elif self.key in self.obj:
            del self.obj[self.key]
        if self.cb:
            self.cb(self.text())
        else:
            self.win.display()


class edit_combobox(QComboBox):
    def __init__(self, win, obj, key, options, cb=None, help_text=None, default=None):
        super().__init__()
        self.win = win
        self.cb = cb
        self.obj = obj
        self.key = key
        self.default = default
        options = options.copy()
        if help_text:
            self.setToolTip(help_text)
        if key in obj:
            if obj[key] not in options:
                options.append(obj[key])
        else:
            options.append("")
        for option in options:
            self.addItem(option)
        self.setEditable(True)
        if key in obj:
            if obj[key] in options:
                self.setCurrentIndex(options.index(obj[key]))
            else:
                print(f"ERROR: {obj[key]} is not a option")
        elif default is not None:
            if default in options:
                self.setCurrentIndex(options.index(default))
            else:
                print(f"ERROR: {default} is not a option")
        else:
            self.setCurrentIndex(options.index(""))
        self.editTextChanged.connect(self.change)
        self.setFocusPolicy(Qt.StrongFocus)

    def wheelEvent(self, *args, **kwargs):
        if self.hasFocus():
            return QComboBox.wheelEvent(self, *args, **kwargs)

    def change(self):
        if self.currentText() != self.default:
            self.obj[self.key] = self.currentText()
        elif self.key in self.obj:
            del self.obj[self.key]
        if self.cb:
            self.cb(self.currentText())
        else:
            self.win.display()


class modifier_selector(QComboBox):
    def __init__(self, win, pin_setup, modifier_id, modifier_view, help_text=None):
        super().__init__()
        self.win = win
        self.pin_setup = pin_setup
        self.modifier_id = modifier_id
        self.modifier_view = modifier_view
        self.entrys = list(set(riocore.plugins.Modifiers().pin_modifier_list()))
        self.entrys.append("--delete--")
        if help_text:
            self.setToolTip(help_text)
        for entry in self.entrys:
            self.addItem(entry)
        active = pin_setup["modifier"][self.modifier_id]["type"]
        self.setCurrentIndex(self.entrys.index(active))
        self.setEditable(False)
        self.activated.connect(self.change)
        self.setFocusPolicy(Qt.StrongFocus)

    def wheelEvent(self, *args, **kwargs):
        if self.hasFocus():
            return QComboBox.wheelEvent(self, *args, **kwargs)

    def change(self):
        selected = self.currentText()
        if selected == "--delete--":
            del self.pin_setup["modifier"][self.modifier_id]
            parent = self.modifier_view.parent()
            while parent.rowCount() > 0:
                parent.removeRow(0)
            for modifier_id, modifier in enumerate(self.pin_setup.get("modifier", [])):
                self.win.tree_add_modifier(parent, self.pin_setup, modifier_id, modifier)
        else:
            self.pin_setup["modifier"][self.modifier_id]["type"] = selected
        self.win.display()
