import sys
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QSizePolicy
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# Generate dummy data
x = [1, 2, 3, 4, 5]
y = [10, 8, 12, 7, 9]

# Create a figure and axis
fig, ax = plt.subplots()

# Create a line chart with the dummy data
ax.plot(x, y)

# Set the title and axis labels
ax.set_title('My Trend Report')
ax.set_xlabel('X Axis')
ax.set_ylabel('Y Axis')

# Create a canvas widget for the chart
canvas = FigureCanvas(fig)
canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
canvas.updateGeometry()

# Create a main window for the application
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the title and size of the window
        self.setWindowTitle('My Trend Report')
        self.setGeometry(100, 100, 800, 600)

        # Add the canvas widget to the main window
        self.setCentralWidget(canvas)

# Create an application instance and show the window
app = QApplication(sys.argv)
window = MainWindow()
window.show()

# Run the application
sys.exit(app.exec_())
