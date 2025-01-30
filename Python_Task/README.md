# Function Plotter

A Python GUI application built with **PySide6** and **Matplotlib** that allows users to input two mathematical functions of `x`, plot them, and find their intersection points.

---

## Features

- **Input Validation**: Ensures that the user inputs valid mathematical functions.
- **Supported Operators**: `+`, `-`, `/`, `*`, `^` (exponentiation), `log10()`, and `sqrt()`.
- **Plotting**: Plots the two functions on a graph.
- **Intersection Points**: Finds and annotates the intersection points of the two functions.
- **Automated Tests**: Includes `pytest` and `pytest-qt` tests for input validation and plotting functionality.

---

## Requirements

- Python 3.6 or later
- PySide6
- Matplotlib
- SymPy
- pytest
- pytest-qt

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/function-plotter.git
   cd function-plotter
2. **Install Dependencies**:
   ```bash
   pip install PySide6 matplotlib sympy pytest pytest-qt
## Usage
1. **Run the Program**:
   ```bash
   python function_plotter.py
2. **Enter Functions**:
   In the GUI, enter two functions of x in the input fields (e.g., 5*x^3 + 2*x and x^2 - 4).
3. **Plot Functions**:
   Click the "Plot Functions" button to plot the functions and display their intersection points.
   
## Running Tests
   ```bash
   pytest test_function_plotter.py -v

![2](https://github.com/user-attachments/assets/70cd7813-6aa3-4aac-aa34-0b1ad0ededb7)
![1](https://github.com/user-attachments/assets/ee6d8285-2ff2-4d69-944c-0e5674d55952)

   
