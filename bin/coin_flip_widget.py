import random
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QSlider, QHBoxLayout
from PyQt5.QtCore import Qt

class CoinFlipWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        # Probability Slider
        prob_layout = QHBoxLayout()
        self.prob_label = QLabel("Heads Probability: 50%")
        self.prob_slider = QSlider(Qt.Horizontal)
        self.prob_slider.setRange(0, 100)
        self.prob_slider.setValue(50)
        self.prob_slider.valueChanged.connect(self.update_prob_label)
        prob_layout.addWidget(self.prob_label)
        prob_layout.addWidget(self.prob_slider)
        self.layout.addLayout(prob_layout)

        self.result_label = QLabel("Click 'Flip Coin' to start")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.result_label)
        
        self.flip_button = QPushButton("Flip Coin")
        self.layout.addWidget(self.flip_button)
        
        self.flip_button.clicked.connect(self.flip_coin)

    def update_prob_label(self, value):
        self.prob_label.setText(f"Heads Probability: {value}%")

    def flip_coin(self):
        heads_prob = self.prob_slider.value() / 100.0
        if random.random() < heads_prob:
            result = 'Heads'
        else:
            result = 'Tails'
        self.result_label.setText(result)
