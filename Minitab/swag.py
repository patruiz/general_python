import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QListWidget

class MinitabClone(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Minitab Clone')
        self.setGeometry(100, 100, 400, 300)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create layout
        layout = QVBoxLayout()

        # Welcome label
        welcome_label = QLabel('Welcome to Minitab Clone!')
        welcome_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(welcome_label)

        # Instructions label
        instructions_label = QLabel('Select a function below:')
        instructions_label.setStyleSheet("font-size: 14px;")
        layout.addWidget(instructions_label)

        # List of available functions
        function_list = QListWidget()
        functions = [
            'Descriptive Statistics',
            'ANOVA',
            'Regression Analysis',
            'Control Charts',
            'Pareto Chart',
            'Hypothesis Testing',
            'Scatter Plot',
            'Time Series Analysis'
        ]
        
        function_list.addItems(functions)
        layout.addWidget(function_list)

        # Set layout to central widget
        central_widget.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MinitabClone()
    window.show()
    sys.exit(app.exec_())
