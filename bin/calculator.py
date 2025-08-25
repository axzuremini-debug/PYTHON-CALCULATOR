import sys
import math
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QGridLayout, QPushButton, QLineEdit, QTabWidget, 
    QVBoxLayout, QTableWidget, QTableWidgetItem, QFileDialog, QHBoxLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from geometry_widget import GeometryWidget
from coin_flip_widget import CoinFlipWidget

class CalculatorWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.create_display()
        self.create_buttons()
        self.apply_stylesheet()

    def create_display(self):
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setFixedHeight(70)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setFont(QFont('Arial', 24))
        self.layout.addWidget(self.display, 0, 0, 1, 4)

    def create_buttons(self):
        self.buttons = {}
        buttons_layout = {
            'sin': (1, 0), 'cos': (1, 1), 'tan': (1, 2), 'log': (1, 3),
            'ln': (2, 0), 'sqrt': (2, 1), '(': (2, 2), ')': (2, 3),
            'C': (3, 0), '%': (3, 1), '<': (3, 2), '/': (3, 3),
            '7': (4, 0), '8': (4, 1), '9': (4, 2), '*': (4, 3),
            '4': (5, 0), '5': (5, 1), '6': (5, 2), '-': (5, 3),
            '1': (6, 0), '2': (6, 1), '3': (6, 2), '+': (6, 3),
            '0': (7, 0, 1, 2), '.': (7, 2), '=': (7, 3)
        }

        for text, pos in buttons_layout.items():
            self.buttons[text] = QPushButton(text)
            self.buttons[text].setFont(QFont('Arial', 18))
            self.buttons[text].clicked.connect(self.on_button_click)
            if len(pos) == 4:
                self.layout.addWidget(self.buttons[text], *pos)
            else:
                self.layout.addWidget(self.buttons[text], pos[0], pos[1])

    def on_button_click(self):
        button = self.sender()
        text = button.text()

        if text == '=':
            try:
                expression = self.display.text().replace('%', '/100')
                safe_dict = {
                    'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
                    'log': math.log10, 'ln': math.log, 'sqrt': math.sqrt,
                    'pi': math.pi, 'e': math.e
                }
                result = str(eval(expression, {"__builtins__": {}}, safe_dict))
                self.display.setText(result)
            except Exception as e:
                self.display.setText('Error')
        elif text == 'C':
            self.display.clear()
        elif text == '<':
            self.display.setText(self.display.text()[:-1])
        else:
            current_text = self.display.text()
            if current_text == 'Error':
                self.display.setText(text)
            else:
                self.display.setText(current_text + text)

    def apply_stylesheet(self):
        # Stylesheet will be applied at the main window level
        pass

class PyxxellWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Button layout
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save")
        self.load_button = QPushButton("Load")
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.load_button)
        self.layout.addLayout(button_layout)

        # Table Widget
        self.table = QTableWidget(100, 26)  # 100 rows, 26 columns (A-Z)
        self.table.setHorizontalHeaderLabels([chr(ord('A') + i) for i in range(26)])
        self.layout.addWidget(self.table)

        # Connect buttons
        self.save_button.clicked.connect(self.save_data)
        self.load_button.clicked.connect(self.load_data)

    def save_data(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Pyxxell files (*.pyxxell)")
        if not file_path:
            return

        data = []
        for row in range(self.table.rowCount()):
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item and item.text():
                    data.append({'row': row, 'col': col, 'text': item.text()})
        
        with open(file_path, 'w') as f:
            json.dump(data, f)

    def load_data(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Pyxxell files (*.pyxxell)")
        if not file_path:
            return

        self.table.clearContents()

        with open(file_path, 'r') as f:
            data = json.load(f)

        for item_data in data:
            item = QTableWidgetItem(item_data['text'])
            self.table.setItem(item_data['row'], item_data['col'], item)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Calculator, Pyxxell, Geometry & Coin Flip')
        self.setFixedSize(400, 600)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.tabs = QTabWidget()
        self.tabs.addTab(CalculatorWidget(), 'Calculator')
        self.tabs.addTab(PyxxellWidget(), 'Pyxxell')
        self.tabs.addTab(GeometryWidget(), 'Geometry')
        self.tabs.addTab(CoinFlipWidget(), 'Coin Flip')
        self.layout.addWidget(self.tabs)

        self.apply_stylesheet()

    def apply_stylesheet(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #2E3440;
                color: #ECEFF4;
            }
            QTabWidget::pane {
                border: 1px solid #4C566A;
            }
            QTabBar::tab {
                background: #3B4252;
                color: #ECEFF4;
                padding: 10px;
            }
            QTabBar::tab:selected {
                background: #4C566A;
            }
            QLineEdit {
                background-color: #3B4252;
                border: none;
                padding: 10px;
                color: #ECEFF4;
            }
            QPushButton {
                background-color: #4C566A;
                border: none;
                padding: 15px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #5E81AC;
            }
            QTableWidget {
                background-color: #3B4252;
                gridline-color: #4C566A;
            }
            QHeaderView::section {
                background-color: #4C566A;
                color: #ECEFF4;
                padding: 5px;
                border: 1px solid #2E3440;
            }
        """)
        # Apply specific button styles to calculator tab
        calculator_widget = self.tabs.widget(0)
        for text, button in calculator_widget.buttons.items():
            if text in ['/', '*', '-', '+']:
                button.setStyleSheet("background-color: #88C0D0; color: #2E3440;")
            if text in ['C', '<', '%', 'sin', 'cos', 'tan', 'log', 'ln', 'sqrt', '(', ')']:
                button.setStyleSheet("background-color: #A3BE8C; color: #2E3440;")
            if text == '=':
                 button.setStyleSheet("background-color: #BF616A; color: #ECEFF4;")

        # Apply specific button styles to Pyxxell tab
        pyxxell_widget = self.tabs.widget(1)
        pyxxell_widget.save_button.setStyleSheet("background-color: #A3BE8C; color: #2E3440;")
        pyxxell_widget.load_button.setStyleSheet("background-color: #A3BE8C; color: #2E3440;")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())