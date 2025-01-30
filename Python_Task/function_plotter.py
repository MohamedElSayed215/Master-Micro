import sys
import numpy as np
import matplotlib.pyplot as plt
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from PySide6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from sympy import symbols, sympify, solve

# Supported operators and functions
SUPPORTED_OPERATORS = ["+", "-", "/", "*", "^", "log10", "sqrt"]


class FunctionPlotterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Function Plotter")
        self.setGeometry(100, 100, 800, 600)

        # Main widget and layout
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout(self.main_widget)

        # Input fields for functions
        self.function1_input = QLineEdit(self)
        self.function1_input.setPlaceholderText("Enter first function of x, e.g., 5*x^3 + 2*x")
        self.function2_input = QLineEdit(self)
        self.function2_input.setPlaceholderText("Enter second function of x, e.g., x^2 - 4")

        # Plot button
        self.plot_button = QPushButton("Plot Functions", self)
        self.plot_button.clicked.connect(self.plot_functions)

        # Matplotlib figure and canvas
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)

        # Add widgets to layout
        self.layout.addWidget(QLabel("Function 1:"))
        self.layout.addWidget(self.function1_input)
        self.layout.addWidget(QLabel("Function 2:"))
        self.layout.addWidget(self.function2_input)
        self.layout.addWidget(self.plot_button)
        self.layout.addWidget(self.canvas)

    def validate_function(self, func_str):
        """
        Validate the function input.
        """
        if not func_str:
            return False, "Function cannot be empty."
        try:
            # Replace ^ with ** for Python syntax
            func_str = func_str.replace("^", "**")
            # Check if the function contains only supported operators
            for op in SUPPORTED_OPERATORS:
                if op in func_str:
                    break
            else:
                return False, "Unsupported operator or function."
            # Test if the function can be parsed
            x = symbols("x")
            sympify(func_str)
            return True, ""
        except Exception as e:
            return False, f"Invalid function: {str(e)}"

    def plot_functions(self):
        """
        Plot the two functions and their intersection point.
        """
        # Get function inputs
        func1_str = self.function1_input.text().strip()
        func2_str = self.function2_input.text().strip()

        # Validate inputs
        valid1, msg1 = self.validate_function(func1_str)
        valid2, msg2 = self.validate_function(func2_str)
        if not valid1:
            QMessageBox.warning(self, "Invalid Input", f"Function 1: {msg1}")
            return
        if not valid2:
            QMessageBox.warning(self, "Invalid Input", f"Function 2: {msg2}")
            return

        # Parse functions
        x = symbols("x")
        func1 = sympify(func1_str.replace("^", "**"))
        func2 = sympify(func2_str.replace("^", "**"))

        # Solve for intersection points
        try:
            solution = solve(func1 - func2, x)
            if not solution:
                QMessageBox.warning(self, "No Solution", "The functions do not intersect.")
                return
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to solve equations: {str(e)}")
            return

        # Generate x values for plotting
        x_vals = np.linspace(-10, 10, 400)
        y1_vals = [func1.subs(x, val).evalf() for val in x_vals]
        y2_vals = [func2.subs(x, val).evalf() for val in x_vals]

        # Clear previous plot
        self.ax.clear()

        # Plot functions
        self.ax.plot(x_vals, y1_vals, label="Function 1")
        self.ax.plot(x_vals, y2_vals, label="Function 2")

        # Plot intersection points
        for sol in solution:
            if sol.is_real:
                sol_x = float(sol)
                sol_y = float(func1.subs(x, sol))
                self.ax.plot(sol_x, sol_y, "ro")  # Red dot for intersection
                self.ax.annotate(
                    f"({sol_x:.2f}, {sol_y:.2f})",
                    (sol_x, sol_y),
                    textcoords="offset points",
                    xytext=(10, 10),
                    ha="center",
                )

        # Add labels and legend
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.legend()
        self.ax.grid(True)

        # Refresh canvas
        self.canvas.draw()

    def closeEvent(self, event):
        """
        Handle window close event.
        """
        reply = QMessageBox.question(
            self, "Exit", "Are you sure you want to exit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FunctionPlotterApp()
    window.show()
    sys.exit(app.exec_())