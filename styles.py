"""Reusable PyQt6 theme colors and component styling helpers."""

from typing import Literal, Union

from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QDialog,
    QInputDialog,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QTableWidget,
    QTextEdit,
    QToolBar,
)


class Styles:
    """Shared colors and reusable component styles; no instance is required."""

    # Change these values to recolor the theme and all component helpers.
    COLOR_PRIMARY = "#2f8f63"
    COLOR_PRIMARY_HOVER = "#287d57"
    COLOR_PRIMARY_PRESSED = "#216b4a"
    COLOR_PRIMARY_DISABLED = "#cbd6cf"
    COLOR_PRIMARY_DISABLED_TEXT = "#f7f9f8"
    COLOR_SECONDARY = "#e8edf0"
    COLOR_SECONDARY_HOVER = "#dce4e9"
    COLOR_SECONDARY_PRESSED = "#cdd8df"
    COLOR_SECONDARY_TEXT = "#465866"
    COLOR_HIGHLIGHT = "#4a90c2"
    COLOR_BACKGROUND = "#f4f6f8"
    COLOR_SURFACE = "#ffffff"
    COLOR_TEXT = "#2c3e50"
    COLOR_FIELD_TEXT = "#34495e"
    COLOR_READ_ONLY_TEXT = "#526574"
    COLOR_MUTED_TEXT = "#788692"
    COLOR_BORDER = "#cbd4dc"
    COLOR_BORDER_HOVER = "#9aaab7"
    COLOR_BORDER_SUBTLE = "#dfe5ea"
    COLOR_CLOSE_BORDER_HOVER = "#aebbc4"
    COLOR_DISABLED = "#edf0f2"
    COLOR_DISABLED_BORDER = "#d8dee3"
    COLOR_DISABLED_TEXT = "#9aa4ad"
    COLOR_SUCCESS = "#77b895"
    COLOR_SUCCESS_BACKGROUND = "#e4f3eb"
    COLOR_SELECTION = "#d9ebf7"
    COLOR_INPUT_HOVER = "#edf2f5"
    COLOR_INPUT_PRESSED = "#dfe7ec"
    COLOR_READ_ONLY_BACKGROUND = "#edf1f4"
    COLOR_TABLE_GRID = "#e3e8ec"
    COLOR_TABLE_ROW_BORDER = "#e8edf0"
    COLOR_TABLE_HEADER_BACKGROUND = "#edf1f4"

    @classmethod
    def _app_stylesheet(cls) -> str:
        return f"""
        QWidget {{
            color: {cls.COLOR_TEXT};
        }}
        QMainWindow, QDialog, QMessageBox, QInputDialog {{
            background-color: {cls.COLOR_BACKGROUND};
        }}
        QLabel {{
            background-color: transparent;
        }}
        QPushButton {{
            background-color: {cls.COLOR_SURFACE};
            border: 1px solid {cls.COLOR_BORDER};
            border-radius: 6px;
            color: {cls.COLOR_TEXT};
            padding: 7px 14px;
        }}
        QPushButton:hover {{
            background-color: {cls.COLOR_INPUT_HOVER};
            border-color: {cls.COLOR_BORDER_HOVER};
        }}
        QPushButton:pressed {{
            background-color: {cls.COLOR_INPUT_PRESSED};
        }}
        QPushButton:disabled {{
            background-color: {cls.COLOR_DISABLED};
            border-color: {cls.COLOR_DISABLED_BORDER};
            color: {cls.COLOR_DISABLED_TEXT};
        }}
        QLineEdit, QComboBox, QTextEdit, QPlainTextEdit, QTableWidget {{
            background-color: {cls.COLOR_SURFACE};
            border: 1px solid {cls.COLOR_BORDER};
            border-radius: 6px;
            selection-background-color: {cls.COLOR_SELECTION};
            selection-color: {cls.COLOR_TEXT};
        }}
        QLineEdit:focus, QComboBox:focus, QTextEdit:focus, QPlainTextEdit:focus {{
            border: 2px solid {cls.COLOR_HIGHLIGHT};
        }}
    """


    @classmethod
    def apply_theme(
        cls,
        app: QApplication,
        font_family: str = "Calibri",
        font_size: int = 11,
    ) -> None:
        """Apply the shared palette and base styles to a PyQt application."""
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(cls.COLOR_BACKGROUND))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(cls.COLOR_TEXT))
        palette.setColor(QPalette.ColorRole.Base, QColor(cls.COLOR_SURFACE))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(cls.COLOR_READ_ONLY_BACKGROUND))
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(cls.COLOR_SURFACE))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor(cls.COLOR_TEXT))
        palette.setColor(QPalette.ColorRole.Text, QColor(cls.COLOR_TEXT))
        palette.setColor(QPalette.ColorRole.Button, QColor(cls.COLOR_SURFACE))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(cls.COLOR_TEXT))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(cls.COLOR_HIGHLIGHT))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(cls.COLOR_SURFACE))
        app.setPalette(palette)
        app.setStyleSheet(
            f'* {{ font-family: "{font_family}"; font-size: {font_size}pt; }}\n'
            + cls._app_stylesheet()
        )


    @classmethod
    def main_window(cls, window: QMainWindow) -> None:
        """Apply the shared background style to a main window."""
        window.setStyleSheet(
            f"QMainWindow {{ background-color: {cls.COLOR_BACKGROUND}; }}"
        )


    @classmethod
    def dialog(cls, dialog: QDialog) -> None:
        """Apply the shared background style to a dialog."""
        dialog.setStyleSheet(f"QDialog {{ background-color: {cls.COLOR_BACKGROUND}; }}")


    @classmethod
    def primary_button(cls, button: QPushButton) -> None:
        """Style a main, call-to-action button."""
        button.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {cls.COLOR_PRIMARY};
                border: 1px solid {cls.COLOR_PRIMARY};
                border-radius: 8px;
                color: {cls.COLOR_SURFACE};
                font-weight: 600;
                padding: 12px 16px;
            }}
            QPushButton:hover {{
                background-color: {cls.COLOR_PRIMARY_HOVER};
                border-color: {cls.COLOR_PRIMARY_HOVER};
            }}
            QPushButton:pressed {{
                background-color: {cls.COLOR_PRIMARY_PRESSED};
                border-color: {cls.COLOR_PRIMARY_PRESSED};
            }}
            QPushButton:disabled {{
                background-color: {cls.COLOR_PRIMARY_DISABLED};
                border-color: {cls.COLOR_PRIMARY_DISABLED};
                color: {cls.COLOR_PRIMARY_DISABLED_TEXT};
            }}
            """
        )


    @classmethod
    def secondary_button(cls, button: QPushButton) -> None:
        """Style a regular secondary action button."""
        button.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {cls.COLOR_SECONDARY};
                border: 1px solid {cls.COLOR_BORDER};
                border-radius: 6px;
                color: {cls.COLOR_SECONDARY_TEXT};
                padding: 7px 14px;
            }}
            QPushButton:hover {{
                background-color: {cls.COLOR_SECONDARY_HOVER};
                border-color: {cls.COLOR_CLOSE_BORDER_HOVER};
            }}
            QPushButton:pressed {{
                background-color: {cls.COLOR_SECONDARY_PRESSED};
            }}
            QPushButton:disabled {{
                background-color: {cls.COLOR_DISABLED};
                border-color: {cls.COLOR_DISABLED_BORDER};
                color: {cls.COLOR_DISABLED_TEXT};
            }}
            """
        )


    @classmethod
    def close_button(cls, button: QPushButton) -> None:
        """Style a less prominent close or dismiss action."""
        button.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {cls.COLOR_SECONDARY};
                border: 1px solid {cls.COLOR_BORDER};
                border-radius: 6px;
                color: {cls.COLOR_SECONDARY_TEXT};
                font-size: 10pt;
                padding: 7px 14px;
            }}
            QPushButton:hover {{
                background-color: {cls.COLOR_SECONDARY_HOVER};
                border-color: {cls.COLOR_CLOSE_BORDER_HOVER};
            }}
            QPushButton:pressed {{
                background-color: {cls.COLOR_SECONDARY_PRESSED};
            }}
            """
        )


    @classmethod
    def database_option_button(cls, button: QPushButton) -> None:
        """Style a selectable database or category option."""
        button.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {cls.COLOR_SURFACE};
                border: 1px solid {cls.COLOR_BORDER};
                border-radius: 6px;
                color: {cls.COLOR_TEXT};
                font-size: 13pt;
                min-width: 100px;
                padding: 8px 12px;
            }}
            QPushButton:hover {{
                background-color: {cls.COLOR_INPUT_HOVER};
                border-color: {cls.COLOR_BORDER_HOVER};
            }}
            QPushButton:pressed {{
                background-color: {cls.COLOR_INPUT_PRESSED};
            }}
            QPushButton:disabled {{
                background-color: {cls.COLOR_DISABLED};
                border-color: {cls.COLOR_DISABLED_BORDER};
                color: {cls.COLOR_DISABLED_TEXT};
            }}
            """
        )


    @classmethod
    def confirm_button(cls, button: QPushButton) -> None:
        """Style an affirmative confirmation action."""
        button.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {cls.COLOR_SURFACE};
                border: 1px solid {cls.COLOR_SUCCESS};
                border-radius: 6px;
                color: {cls.COLOR_TEXT};
                padding: 7px 14px;
            }}
            QPushButton:hover {{
                background-color: {cls.COLOR_SUCCESS_BACKGROUND};
                border-color: {cls.COLOR_PRIMARY};
            }}
            QPushButton:pressed {{
                background-color: {cls.COLOR_INPUT_PRESSED};
            }}
            QPushButton:disabled {{
                background-color: {cls.COLOR_DISABLED};
                border-color: {cls.COLOR_DISABLED_BORDER};
                color: {cls.COLOR_DISABLED_TEXT};
            }}
            """
        )


    @classmethod
    def cancel_button(cls, button: QPushButton) -> None:
        """Style a cancel or negative confirmation action."""
        cls.close_button(button)


    @classmethod
    def heading(
        cls,
        label: QLabel,
        size: Literal["main", "section", "dialog"] = "main",
    ) -> None:
        """Style a heading label; size may be 'main', 'section', or 'dialog'."""
        sizes = {"main": "20pt", "section": "18pt", "dialog": "14pt"}
        label.setStyleSheet(
            f"""
            QLabel {{
                background-color: {cls.COLOR_SURFACE};
                border: 1px solid {cls.COLOR_BORDER_SUBTLE};
                border-radius: 10px;
                color: {cls.COLOR_TEXT};
                font-size: {sizes[size]};
                font-weight: 600;
                padding: 12px;
            }}
            """
        )


    @classmethod
    def field_label(cls, label: QLabel) -> None:
        """Style a label used to identify an input field."""
        label.setStyleSheet(
            f"QLabel {{ color: {cls.COLOR_FIELD_TEXT}; font-size: 13pt; font-weight: 600; padding: 4px; }}"
        )


    @classmethod
    def muted_label(cls, label: QLabel) -> None:
        """Style supporting or secondary text."""
        label.setStyleSheet(
            f"QLabel {{ color: {cls.COLOR_MUTED_TEXT}; font-size: 10pt; font-style: italic; padding: 2px 5px; }}"
        )


    @classmethod
    def text_input(cls, widget: Union[QLineEdit, QComboBox]) -> None:
        """Style an editable line input or combo box."""
        widget.setStyleSheet(
            f"""
            QLineEdit, QComboBox {{
                background-color: {cls.COLOR_SURFACE};
                border: 1px solid {cls.COLOR_BORDER};
                border-radius: 6px;
                color: {cls.COLOR_TEXT};
                padding: 7px 9px;
            }}
            QLineEdit:focus, QComboBox:focus {{
                border: 2px solid {cls.COLOR_HIGHLIGHT};
            }}
            """
        )


    @classmethod
    def read_only_input(cls, widget: QLineEdit) -> None:
        """Style a read-only line input."""
        cls.text_input(widget)
        widget.setStyleSheet(
            widget.styleSheet()
            + f"""
            QLineEdit:read-only {{
                background-color: {cls.COLOR_READ_ONLY_BACKGROUND};
                color: {cls.COLOR_READ_ONLY_TEXT};
            }}
            """
        )


    @classmethod
    def label_preview(cls, widget: QTextEdit) -> None:
        """Style the label preview text area."""
        widget.setStyleSheet(
            f"""
            QTextEdit {{
                background-color: {cls.COLOR_SURFACE};
                border: 2px solid {cls.COLOR_HIGHLIGHT};
                border-radius: 6px;
                color: {cls.COLOR_TEXT};
                font-size: 12pt;
                padding: 6px;
            }}
            """
        )


    @classmethod
    def log_output(cls, widget: Union[QTextEdit, QPlainTextEdit]) -> None:
        """Style a read-only log or console text area."""
        widget.setStyleSheet(
            f"""
            QTextEdit, QPlainTextEdit {{
                background-color: {cls.COLOR_SURFACE};
                border: 1px solid {cls.COLOR_BORDER};
                border-radius: 6px;
                color: {cls.COLOR_TEXT};
                font-family: Consolas, monospace;
                font-size: 10pt;
                padding: 6px;
            }}
            """
        )


    @classmethod
    def database_table(cls, table: QTableWidget) -> None:
        """Style a data table and its headers."""
        table.setStyleSheet(
            f"""
            QTableWidget {{
                background-color: {cls.COLOR_SURFACE};
                border: 1px solid {cls.COLOR_BORDER};
                border-radius: 6px;
                gridline-color: {cls.COLOR_TABLE_GRID};
                selection-background-color: {cls.COLOR_SELECTION};
                selection-color: {cls.COLOR_TEXT};
            }}
            QTableWidget::item {{
                padding: 6px;
                border-bottom: 1px solid {cls.COLOR_TABLE_ROW_BORDER};
            }}
            QHeaderView::section {{
                background-color: {cls.COLOR_TABLE_HEADER_BACKGROUND};
                border: 1px solid {cls.COLOR_BORDER_SUBTLE};
                color: {cls.COLOR_FIELD_TEXT};
                font-weight: 600;
                padding: 8px;
            }}
            """
        )


    @classmethod
    def toolbar(cls, toolbar: QToolBar) -> None:
        """Style the application's navigation toolbar."""
        toolbar.setStyleSheet(
            f"""
            QToolBar {{
                background-color: {cls.COLOR_SURFACE};
                border: 1px solid {cls.COLOR_BORDER_SUBTLE};
                border-radius: 8px;
                padding: 4px;
                spacing: 6px;
            }}
            QToolBar QToolButton {{
                background-color: transparent;
                border: 1px solid transparent;
                border-radius: 5px;
                color: {cls.COLOR_TEXT};
                padding: 6px 10px;
            }}
            QToolBar QToolButton:hover {{
                background-color: {cls.COLOR_INPUT_HOVER};
                border-color: {cls.COLOR_BORDER_SUBTLE};
            }}
            QToolBar QToolButton:pressed {{
                background-color: {cls.COLOR_INPUT_PRESSED};
            }}
            """
        )


    @classmethod
    def message_dialog(cls, dialog: QMessageBox) -> None:
        """Style a message dialog and its standard buttons."""
        dialog.setStyleSheet(
            f"""
            QMessageBox {{
                background-color: {cls.COLOR_BACKGROUND};
                color: {cls.COLOR_TEXT};
            }}
            QMessageBox QLabel {{
                background-color: transparent;
                color: {cls.COLOR_TEXT};
                padding: 4px;
            }}
            QMessageBox QPushButton {{
                background-color: {cls.COLOR_SURFACE};
                border: 1px solid {cls.COLOR_BORDER};
                border-radius: 6px;
                color: {cls.COLOR_TEXT};
                min-width: 80px;
                padding: 7px 14px;
            }}
            QMessageBox QPushButton:hover {{
                background-color: {cls.COLOR_INPUT_HOVER};
                border-color: {cls.COLOR_BORDER_HOVER};
            }}
            """
        )


    @classmethod
    def input_dialog(cls, dialog: QInputDialog) -> None:
        """Style a text or selection input dialog."""
        dialog.setStyleSheet(
            f"""
            QInputDialog {{
                background-color: {cls.COLOR_BACKGROUND};
            }}
            QInputDialog QLabel {{
                background-color: transparent;
                color: {cls.COLOR_TEXT};
                font-weight: 600;
                padding: 4px;
            }}
            QInputDialog QLineEdit, QInputDialog QComboBox {{
                background-color: {cls.COLOR_SURFACE};
                border: 1px solid {cls.COLOR_BORDER};
                border-radius: 6px;
                color: {cls.COLOR_TEXT};
                padding: 7px 9px;
            }}
            QInputDialog QLineEdit:focus, QInputDialog QComboBox:focus {{
                border: 2px solid {cls.COLOR_HIGHLIGHT};
            }}
            QInputDialog QPushButton {{
                background-color: {cls.COLOR_SURFACE};
                border: 1px solid {cls.COLOR_BORDER};
                border-radius: 6px;
                color: {cls.COLOR_TEXT};
                min-width: 80px;
                padding: 7px 14px;
            }}
            QInputDialog QPushButton:hover {{
                background-color: {cls.COLOR_INPUT_HOVER};
            }}
            """
        )
