from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFrame, QHBoxLayout
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import Qt

class DrawingCanvas(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        self.setMinimumSize(200, 200)
        self.objects = []
        self.current_tool = 'point'
        self.line_start_point = None

    def set_tool(self, tool):
        self.current_tool = tool
        self.line_start_point = None # Reset when tool changes

    def mousePressEvent(self, event):
        if self.current_tool == 'point':
            point = event.pos()
            self.objects.append(('point', point))
            self.update() # Trigger a repaint
        elif self.current_tool == 'line':
            if self.line_start_point is None:
                self.line_start_point = event.pos()
            else:
                self.objects.append(('line', self.line_start_point, event.pos()))
                self.line_start_point = None
                self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        
        self.draw_grid(painter)

        pen = QPen(Qt.white, 2, Qt.SolidLine)
        painter.setPen(pen)

        for obj_type, *data in self.objects:
            if obj_type == 'point':
                painter.drawEllipse(data[0], 3, 3) # Draw a small circle for the point
            elif obj_type == 'line':
                painter.drawLine(data[0], data[1])

    def draw_grid(self, painter):
        grid_spacing = 20
        pen = QPen(QColor(76, 86, 106), 1, Qt.SolidLine) # Using a color from the theme
        painter.setPen(pen)

        width = self.width()
        height = self.height()

        # Draw vertical lines
        for x in range(0, width, grid_spacing):
            painter.drawLine(x, 0, x, height)

        # Draw horizontal lines
        for y in range(0, height, grid_spacing):
            painter.drawLine(0, y, width, y)

class GeometryWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        # Main layout for the geometry tab
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        # Toolbar layout
        toolbar_layout = QHBoxLayout()
        
        # Tool buttons
        self.point_button = QPushButton("Point")
        self.line_button = QPushButton("Line")
        toolbar_layout.addWidget(self.point_button)
        toolbar_layout.addWidget(self.line_button)
        self.layout.addLayout(toolbar_layout)
        
        # Drawing Canvas
        self.canvas = DrawingCanvas()
        self.layout.addWidget(self.canvas)

        # Connect buttons to set tool
        self.point_button.clicked.connect(lambda: self.canvas.set_tool('point'))
        self.line_button.clicked.connect(lambda: self.canvas.set_tool('line'))
