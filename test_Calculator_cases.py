import sys, os, types
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '{repo_basename}')))


# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', f'{safe_repo_name}')))
# Auto-mock tkinter for headless environments
try:
    import tkinter as tk
except ImportError:
    import sys, types
    class _WidgetMock:
        def __init__(self, *a, **k): self._text = ""
        def config(self, **kwargs): 
            if "text" in kwargs: self._text = kwargs["text"]
        def cget(self, key): return self._text if key == "text" else None
        def get(self): return self._text
        def grid(self, *a, **k): return []
        def pack(self, *a, **k): return []
        def place(self, *a, **k): return []
        def destroy(self): return None
        def __getattr__(self, item): return lambda *a, **k: None
    tk = types.ModuleType("tkinter")
    for widget in ["Tk","Label","Button","Entry","Frame","Canvas","Text","Scrollbar","Checkbutton",
                "Radiobutton","Spinbox","Menu","Toplevel","Listbox"]:
        setattr(tk, widget, _WidgetMock)
    for const in ["N","S","E","W","NE","NW","SE","SW","CENTER","NS","EW","NSEW"]:
        setattr(tk, const, const)
    sys.modules["tkinter"] = tk

import sys
import pytest
from unittest.mock import MagicMock, patch

sys.path.insert(0, r'/home/vvdn/projects/sfit_unitest_19_9_2025/cloned_repos/Calculator')

from calculator import Calculator, tk, LARGE_FONT_STYLE, SMALL_FONT_STYLE, DIGITS_FONT_STYLE, DEFAULT_FONT_STYLE, OFF_WHITE, WHITE, LIGHT_BLUE, LIGHT_GRAY, LABEL_COLOR

class _WidgetMock:
    def __init__(self, *args, **kwargs):
        self.config = MagicMock()
        self.pack = MagicMock()
        self.grid = MagicMock()
        self.bind = MagicMock()

class _TkMock(_WidgetMock):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry = MagicMock()
        self.resizable = MagicMock()
        self.title = MagicMock()
        self.mainloop = MagicMock()

@pytest.fixture
def mock_tkinter():
    with patch('tkinter.Tk', new=_TkMock), \
         patch('tkinter.Frame', new=_WidgetMock), \
         patch('tkinter.Label', new=_WidgetMock), \
         patch('tkinter.Button', new=_WidgetMock):
        yield

@pytest.fixture
def calculator(mock_tkinter):
    calc = Calculator()
    return calc

def test_calculator_initialization(calculator):
    assert calculator.window is not None
    assert calculator.total_expression == ""
    assert calculator.current_expression == ""
    assert calculator.display_frame is not None
    assert calculator.total_label is not None
    assert calculator.label is not None
    assert calculator.buttons_frame is not None

def test_add_to_expression(calculator):
    calculator.add_to_expression(5)
    assert calculator.current_expression == "5"
    calculator.add_to_expression("+")
    assert calculator.current_expression == "5+"
    calculator.update_label()
    calculator.label.config.assert_called_once_with(text="5+")

def test_append_operator(calculator):
    calculator.current_expression = "12"
    calculator.append_operator("+")
    assert calculator.current_expression == ""
    assert calculator.total_expression == "12+"
    calculator.update_total_label()
    calculator.total_label.config.assert_called_once_with(text=" 12 + ")
    calculator.update_label()
    calculator.label.config.assert_called_once_with(text="")

def test_clear(calculator):
    calculator.current_expression = "12+3"
    calculator.total_expression = "15"
    calculator.clear()
    assert calculator.current_expression == ""
    assert calculator.total_expression == ""
    calculator.update_label()
    calculator.label.config.assert_called_once_with(text="")
    calculator.update_total_label()
    calculator.total_label.config.assert_called_once_with(text="")

def test_square(calculator):
    calculator.current_expression = "5"
    calculator.square()
    assert calculator.current_expression == "25"
    calculator.update_label()
    calculator.label.config.assert_called_once_with(text="25")

def test_sqrt(calculator):
    calculator.current_expression = "25"
    calculator.sqrt()
    assert calculator.current_expression == "5.0"
    calculator.update_label()
    calculator.label.config.assert_called_once_with(text="5.0")

def test_evaluate_valid_expression(calculator):
    calculator.current_expression = "5"
    calculator.total_expression = "10+"
    calculator.evaluate()
    assert calculator.current_expression == "15.0"
    assert calculator.total_expression == ""
    calculator.update_total_label()
    calculator.total_label.config.assert_called_once_with(text="10 + ")
    calculator.update_label()
    calculator.label.config.assert_called_once_with(text="15.0")

def test_evaluate_error_expression(calculator):
    calculator.current_expression = "abc"
    calculator.total_expression = "10+"
    calculator.evaluate()
    assert calculator.current_expression == "Error"
    assert calculator.total_expression == ""
    calculator.update_total_label()
    calculator.total_label.config.assert_called_once_with(text="10 + ")
    calculator.update_label()
    calculator.label.config.assert_called_once_with(text="Error")

def test_update_total_label(calculator):
    calculator.total_expression = "10*5"
    calculator.update_total_label()
    calculator.total_label.config.assert_called_once_with(text="10 × 5")

def test_update_label_short_expression(calculator):
    calculator.current_expression = "12345"
    calculator.update_label()
    calculator.label.config.assert_called_once_with(text="12345")

def test_update_label_long_expression(calculator):
    calculator.current_expression = "1234567890123"
    calculator.update_label()
    calculator.label.config.assert_called_once_with(text="12345678901")

def test_bind_keys_return(calculator):
    calculator.window.bind.assert_any_call("<Return>", pytest.raises(TypeError)) # Mocked bind returns None, so we check for the lambda call

def test_bind_keys_digits(calculator):
    for digit in calculator.digits:
        calculator.window.bind.assert_any_call(str(digit), pytest.raises(TypeError))

def test_bind_keys_operators(calculator):
    for operator in calculator.operations:
        calculator.window.bind.assert_any_call(operator, pytest.raises(TypeError))

def test_create_digit_buttons(calculator):
    assert len(calculator.digits) == len(calculator.buttons_frame.grid.call_args_list) - 5 # Subtract special buttons

def test_create_operator_buttons(calculator):
    assert len(calculator.operations) == calculator.buttons_frame.grid.call_count - len(calculator.digits) - 5 # Subtract digit and special buttons

def test_create_special_buttons(calculator):
    calculator.create_special_buttons()
    assert calculator.buttons_frame.grid.call_count >= 4 # C, =, x^2, sqrt

if __name__ == "__main__":
    import pytest, sys
    sys.exit(pytest.main([__file__, "-v"]))