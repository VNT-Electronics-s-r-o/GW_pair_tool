import datetime
import os
import platform
import sys

import openpyxl
from data_saver import DataSaver, DataViewer
from dotenv import load_dotenv
from PyQt6.QtCore import (
    QObject,
    QRunnable,
    QSize,
    Qt,
    QThreadPool,
    pyqtSignal,
    pyqtSlot,
)
from PyQt6.QtGui import QAction, QColor, QFont, QIcon, QPalette
from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QTextEdit,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

from settings import DEVICE_MAP, ENV_PATH, ICONS_PATH, ROLE
from styles import Styles

load_dotenv(ENV_PATH)


class Signals(QObject):
    result = pyqtSignal(object)
    progress = pyqtSignal(str, str)
    def __init__(self):
        super().__init__()


class Worker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = Signals()

    @pyqtSlot()
    def run(self):
        fn_result = self.fn(*self.args, **self.kwargs)
        self.signals.result.emit(fn_result)


class DatabaseSelector(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.selected_device = None

        self.setWindowTitle('Vybrat databázi')
        self.setWindowIcon(QIcon(ICONS_PATH + 'database.png'))
        self.resize(350, 200)
        Styles.dialog(self)

        layout = QVBoxLayout()

        title = QLabel('Vyberte databázi, kterou chcete zobrazit:')
        Styles.heading(title, size='dialog')
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        button_layout = QVBoxLayout()
        button_layout.setSpacing(10)

        gw100_btn = QPushButton('GW100')
        fm20_btn = QPushButton('FM20')
        zebu_btn = QPushButton('ZEBU')
        agrifence_btn = QPushButton('AGRIFENCE')
        for button in (gw100_btn, fm20_btn, zebu_btn, agrifence_btn):
            Styles.database_option_button(button)

        close_btn = QPushButton('Zavřít')
        Styles.close_button(close_btn)

        button_layout.addWidget(gw100_btn)
        button_layout.addWidget(fm20_btn)
        button_layout.addWidget(zebu_btn)
        button_layout.addWidget(agrifence_btn)
        button_layout.addSpacing(12)
        button_layout.addWidget(close_btn)

        layout.addLayout(button_layout)
        self.setLayout(layout)

        gw100_btn.clicked.connect(lambda: self.select_device('GW100'))
        fm20_btn.clicked.connect(lambda: self.select_device('FM20'))
        zebu_btn.clicked.connect(lambda: self.select_device('ZEBU'))
        agrifence_btn.clicked.connect(lambda: self.select_device('AGRIFENCE'))

        close_btn.clicked.connect(self.reject)

    def select_device(self, device_type):
        self.selected_device = device_type
        self.accept()

    def get_selected_device(self):
        return self.selected_device


class MainWindow(QMainWindow):
    log_signal = pyqtSignal(str, str)
    def __init__(self):
        super().__init__()

        self.database = None
        self.device = None

        device_type_label = QLabel('Typ zařízení:')


        device_id_label = QLabel('Číslo desky:')

        self.device_id_input = QInputDialog()

    def log_msg(self, msg: str, msg_type: str = 'info'):
        try:
            color_map = {
                'info': 'black',
                'ok': 'green',
                'warn': 'orange',
                'error': 'red',
                'debug': 'purple',
                '': 'black',
                'empty': 'none'
            }

            time = self.get_timestamp()
            color = color_map.get(msg_type, 'black')

            match msg_type:
                case 'info':
                    self.log.append(f'<font color="{color}">[INFO] {time} | {msg}</font>')
                case 'warn':
                    self.log.append(f'<font color="{color}"><b>[WARNING]</b> {time} | {msg}</font>')
                case 'error':
                    self.log.append(f'<font color="{color}"><b>[ERROR]</b> {time} | <b>{msg}</b></font>')
                case 'debug':
                    self.log.append(f'<font color="{color}">[DEBUG] {time} | {msg}</font>')
                case 'ok':
                    self.log.append(f'<font color="{color}"><b>[OK]<b> {time} | {msg}</font>')
                case '':
                    self.log.append(f'<font color="{color}">[INFO] {time} | {msg}')
                case 'empty':
                    self.log.append('')
        except Exception as e:
            print('Error in log_msg: ', e)
            return False
    
    def get_timestamp(self):
        return datetime.now().strftime('%d.%m.%Y %H:%M')

    def open_db(self):
        db_selector = DatabaseSelector(self)
        if db_selector.exec() == QDialog.DialogCode.Accepted:
            selected_database = db_selector.get_selected_device()
            db_viewer = DataViewer(device=selected_database, database=selected_database)
            db_viewer.exec()

def confirmation_msg(title, msg):
    """Improved confirmation dialog with better styling"""
    msg_box = QMessageBox()
    msg_box.setWindowTitle(title)
    msg_box.setText(msg)
    msg_box.setIcon(QMessageBox.Icon.Question)
    msg_box.setWindowIcon(QIcon(ICONS_PATH + 'question.png'))
    Styles.message_dialog(msg_box)

    font = QFont()
    font.setPointSize(11)
    msg_box.setFont(font)

    yes_btn = msg_box.addButton('Ano', QMessageBox.ButtonRole.YesRole)
    Styles.confirm_button(yes_btn)
    no_btn = msg_box.addButton('Ne', QMessageBox.ButtonRole.NoRole)
    Styles.cancel_button(no_btn)

    msg_box.exec()

    result = msg_box.clickedButton() == yes_btn
    print(f'User clicked {"Yes" if result else "No"}')
    return result

def input_dialog(label, text, items = None):
    """Improved input dialog - kept for compatibility but now uses better styling"""
    dialog = QInputDialog()
    dialog.setWindowTitle(label)
    dialog.setLabelText(text)
    if items:
        dialog.setComboBoxItems(items)

    dialog.setWindowIcon(QIcon(ICONS_PATH + 'input.png'))
    Styles.input_dialog(dialog)

    dialog.resize(450, 200)
    dialog.setOkButtonText('OK')
    dialog.setCancelButtonText('Zrušit')

    buttons = dialog.findChildren(QPushButton)

    for button in buttons:
        if button.text() == 'OK':
            Styles.confirm_button(button)
        elif button.text() == 'Zrušit':
            Styles.cancel_button(button)
    dialog.exec()
    if dialog.result() == QDialog.DialogCode.Accepted:
        return dialog.textValue()
    else:
        return None

def alert_dialog(label, text):
    msg = QMessageBox()
    msg.setWindowTitle(label)
    msg.setText(text)
    msg.setWindowIcon(QIcon(ICONS_PATH + 'alert-active.png'))
    Styles.message_dialog(msg)

    result = msg.exec()
    return result


if __name__ == '__main__':
    app = QApplication(sys.argv)

    if platform.system() == "Windows":
        app.setStyle("windowsvista")
    else:
        app.setStyle("Fusion")

    Styles.apply_theme(app)

    window = MainWindow()
    window.showMaximized()

    sys.exit(app.exec())

