import pytest
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from function_plotter import FunctionPlotterApp


@pytest.fixture
def app(qtbot):
    """Fixture to initialize the application."""
    test_app = QApplication.instance()
    if test_app is None:
        test_app = QApplication([])
    window = FunctionPlotterApp()
    qtbot.addWidget(window)
    return window


def test_input_validation(app, qtbot):
    """Test input validation for invalid functions."""
    # Test empty input
    app.function1_input.setText("")
    app.function2_input.setText("")
    qtbot.mouseClick(app.plot_button, Qt.LeftButton)
    valid1, msg1 = app.validate_function(app.function1_input.text())
    valid2, msg2 = app.validate_function(app.function2_input.text())
    assert not valid1 and "Function cannot be empty" in msg1
    assert not valid2 and "Function cannot be empty" in msg2

    # Test unsupported operator
    app.function1_input.setText("5*x^3 + 2*x")
    app.function2_input.setText("sin(x)")
    qtbot.mouseClick(app.plot_button, Qt.LeftButton)
    valid1, msg1 = app.validate_function(app.function1_input.text())
    valid2, msg2 = app.validate_function(app.function2_input.text())
    assert valid1
    assert not valid2 and "Unsupported operator or function" in msg2


def test_plotting(app, qtbot):
    """Test plotting valid functions."""
    # Input valid functions
    app.function1_input.setText("x^2")
    app.function2_input.setText("2*x")
    qtbot.mouseClick(app.plot_button, Qt.LeftButton)

    # Check that there are 2 lines for the functions
    function_lines = [line for line in app.ax.lines if line.get_label() in ["Function 1", "Function 2"]]
    assert len(function_lines) == 2  # Two lines should be plotted for the functions

    # Check that the intersection point is plotted
    intersection_points = [line for line in app.ax.lines if line.get_label() not in ["Function 1", "Function 2"]]
    assert len(intersection_points) >= 1  # At least one intersection point should be plotted