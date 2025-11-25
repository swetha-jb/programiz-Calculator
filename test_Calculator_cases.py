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

import pytest
import sys
from unittest.mock import MagicMock

sys.path.insert(0, r'/home/vvdn/projects/sfit_unitest_19_9_2025/cloned_repos/Calculator')
from calculator import Calculator

class MockTkinterWindow:
    def __init__(self):
        self.bind = MagicMock()
        self.mainloop = MagicMock()

class MockTkinterWidget:
    def __init__(self):
        self.config = MagicMock()
        self.pack = MagicMock()
        self.grid = MagicMock()
        self.rowconfigure = MagicMock()
        self.columnconfigure = MagicMock()

    def __getitem__(self, key):
        return self

    def __setitem__(self, key, value):
        pass

@pytest.fixture
def mock_tkinter():
    mock_tk = MagicMock()
    mock_tk.Tk.return_value = MockTkinterWindow()
    mock_tk.Frame.return_value = MockTkinterWidget()
    mock_tk.Label.return_value = MockTkinterWidget()
    mock_tk.Button.return_value = MockTkinterWidget()
    return mock_tk

@pytest.fixture
def calculator_instance(mock_tkinter):
    tk.Tk = mock_tkinter.Tk
    tk.Frame = mock_tkinter.Frame
    tk.Label = mock_tkinter.Label
    tk.Button = mock_tkinter.Button
    calc = Calculator()
    calc.update_label = MagicMock()
    calc.update_total_label = MagicMock()
    return calc

def test_calculator_initialization(calculator_instance):
    assert calculator_instance.window is not None
    assert calculator_instance.total_expression == ""
    assert calculator_instance.current_expression == ""
    assert calculator_instance.display_frame is not None
    assert calculator_instance.total_label is not None
    assert calculator_instance.label is not None
    assert calculator_instance.buttons_frame is not None

def test_add_to_expression(calculator_instance):
    calculator_instance.add_to_expression(5)
    assert calculator_instance.current_expression == "5"
    calculator_instance.update_label.assert_called_once()

    calculator_instance.add_to_expression("+")
    assert calculator_instance.current_expression == "5+"
    assert calculator_instance.update_label.call_count == 2

def test_append_operator(calculator_instance):
    calculator_instance.current_expression = "123"
    calculator_instance.append_operator("+")

    assert calculator_instance.total_expression == "123+"
    assert calculator_instance.current_expression == ""
    calculator_instance.update_total_label.assert_called_once()
    calculator_instance.update_label.assert_called_once()

def test_clear(calculator_instance):
    calculator_instance.total_expression = "1+2"
    calculator_instance.current_expression = "3"
    calculator_instance.clear()

    assert calculator_instance.total_expression == ""
    assert calculator_instance.current_expression == ""
    calculator_instance.update_label.assert_called_once()
    calculator_instance.update_total_label.assert_called_once()

def test_square(calculator_instance):
    calculator_instance.current_expression = "5"
    calculator_instance.square()
    assert calculator_instance.current_expression == "25"
    calculator_instance.update_label.assert_called_once()

    calculator_instance.current_expression = "-3"
    calculator_instance.square()
    assert calculator_instance.current_expression == "9"
    assert calculator_instance.update_label.call_count == 2

def test_sqrt(calculator_instance):
    calculator_instance.current_expression = "25"
    calculator_instance.sqrt()
    assert calculator_instance.current_expression == "5.0"
    calculator_instance.update_label.assert_called_once()

    calculator_instance.current_expression = "2"
    calculator_instance.sqrt()
    assert calculator_instance.current_expression == "1.4142135623730951"
    assert calculator_instance.update_label.call_count == 2

def test_evaluate_valid_expression(calculator_instance):
    calculator_instance.total_expression = "2+3"
    calculator_instance.current_expression = ""
    calculator_instance.evaluate()

    assert calculator_instance.total_expression == ""
    assert calculator_instance.current_expression == "5"
    calculator_instance.update_total_label.assert_called_once()
    calculator_instance.update_label.assert_called_once()

def test_evaluate_expression_with_current(calculator_instance):
    calculator_instance.total_expression = "10"
    calculator_instance.current_expression = "*2"
    calculator_instance.evaluate()

    assert calculator_instance.total_expression == ""
    assert calculator_instance.current_expression == "20"
    calculator_instance.update_total_label.assert_called_once()
    calculator_instance.update_label.assert_called_once()

def test_evaluate_error_expression(calculator_instance):
    calculator_instance.total_expression = "2+"
    calculator_instance.current_expression = ""
    calculator_instance.evaluate()

    assert calculator_instance.total_expression == "2+"
    assert calculator_instance.current_expression == "Error"
    calculator_instance.update_total_label.assert_called_once()
    calculator_instance.update_label.assert_called_once()

def test_update_total_label(calculator_instance):
    calculator_instance.total_expression = "1+2*3"
    calculator_instance.update_total_label()
    calculator_instance.total_label.config.assert_called_with(text='1 + 2 * 3')

def test_update_label(calculator_instance):
    calculator_instance.current_expression = "1234567890123"
    calculator_instance.update_label()
    calculator_instance.label.config.assert_called_with(text='12345678901')

def test_bind_keys_return(calculator_instance):
    calculator_instance.evaluate = MagicMock()
    calculator_instance.window.bind.assert_any_call("<Return>", MagicMock())

def test_bind_keys_digits(calculator_instance):
    calculator_instance.add_to_expression = MagicMock()
    for digit in calculator_instance.digits:
        calculator_instance.window.bind.assert_any_call(str(digit), MagicMock())

def test_bind_keys_operators(calculator_instance):
    calculator_instance.append_operator = MagicMock()
    for operator in calculator_instance.operations:
        calculator_instance.window.bind.assert_any_call(operator, MagicMock())

def test_create_digit_buttons(calculator_instance):
    calculator_instance.create_digit_buttons()
    assert calculator_instance.buttons_frame.grid.call_count == len(calculator_instance.digits)

def test_create_operator_buttons(calculator_instance):
    calculator_instance.create_operator_buttons()
    assert calculator_instance.buttons_frame.grid.call_count == len(calculator_instance.operations)

def test_create_special_buttons(calculator_instance):
    calculator_instance.create_special_buttons()
    assert calculator_instance.buttons_frame.grid.call_count == 4

def test_run(calculator_instance):
    calculator_instance.run()
    calculator_instance.window.mainloop.assert_called_once()

if __name__ == "__main__":
    import pytest, sys
    sys.exit(pytest.main([__file__, "-v"]))