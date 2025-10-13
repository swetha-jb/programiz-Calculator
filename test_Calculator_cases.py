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
        self.children = {}
        self.config = MagicMock()
        self.pack = MagicMock()
        self.grid = MagicMock()
        self.bind = MagicMock()
        self.destroy = MagicMock()
        self.configure = MagicMock()

    def __setitem__(self, key, value):
        pass

    def __getitem__(self, key):
        return self

    def add_child(self, name, widget):
        self.children[name] = widget

class _TkMock(_WidgetMock):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry = MagicMock()
        self.resizable = MagicMock()
        self.title = MagicMock()
        self.mainloop = MagicMock()

    def bind(self, event, handler):
        pass

class _FrameMock(_WidgetMock):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rowconfigure = MagicMock()
        self.columnconfigure = MagicMock()

class _LabelMock(_WidgetMock):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = MagicMock()

class _ButtonMock(_WidgetMock):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.command = kwargs.get('command')

@pytest.fixture
def mock_tkinter():
    with patch('tkinter.Tk', _TkMock), \
         patch('tkinter.Frame', _FrameMock), \
         patch('tkinter.Label', _LabelMock), \
         patch('tkinter.Button', _ButtonMock):
        yield

@pytest.fixture
def calculator(mock_tkinter):
    return Calculator()

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

def test_append_operator(calculator):
    calculator.current_expression = "5"
    calculator.append_operator("+")
    assert calculator.total_expression == "5+"
    assert calculator.current_expression == ""

def test_clear(calculator):
    calculator.current_expression = "123"
    calculator.total_expression = "456"
    calculator.clear()
    assert calculator.current_expression == ""
    assert calculator.total_expression == ""

def test_square(calculator):
    calculator.current_expression = "5"
    calculator.square()
    assert calculator.current_expression == "25"

def test_sqrt(calculator):
    calculator.current_expression = "25"
    calculator.sqrt()
    assert calculator.current_expression == "5.0"

def test_evaluate_valid_expression(calculator):
    calculator.current_expression = "5"
    calculator.total_expression = "2+"
    calculator.evaluate()
    assert calculator.current_expression == "7.0"
    assert calculator.total_expression == ""

def test_evaluate_division_by_zero(calculator):
    calculator.current_expression = "0"
    calculator.total_expression = "5/"
    calculator.evaluate()
    assert calculator.current_expression == "Error"
    assert calculator.total_expression == "5/0"

def test_update_label(calculator):
    calculator.current_expression = "12345678901"
    calculator.update_label()
    assert calculator.label.config.call_args[1]['text'] == "1234567890"

def test_update_total_label(calculator):
    calculator.total_expression = "5+3"
    calculator.update_total_label()
    assert calculator.total_label.config.call_args[1]['text'] == "5 + 3"

def test_bind_keys_digits(calculator):
    calculator.window.bind.assert_any_call('7', pytest.raises(TypeError))
    calculator.window.bind.assert_any_call('0', pytest.raises(TypeError))
    calculator.window.bind.assert_any_call('.', pytest.raises(TypeError))

def test_bind_keys_operators(calculator):
    calculator.window.bind.assert_any_call('+', pytest.raises(TypeError))
    calculator.window.bind.assert_any_call('-', pytest.raises(TypeError))

def test_create_digit_buttons(calculator):
    for digit, grid_value in calculator.digits.items():
        calculator.buttons_frame.add_child(str(digit), _ButtonMock(command=lambda x=digit: calculator.add_to_expression(x)))
    calculator.create_digit_buttons()
    assert len(calculator.buttons_frame.children) == len(calculator.digits)

def test_create_operator_buttons(calculator):
    calculator.create_operator_buttons()
    assert len(calculator.buttons_frame.children) == len(calculator.operations)

def test_create_special_buttons(calculator):
    calculator.create_special_buttons()
    assert "C" in calculator.buttons_frame.children
    assert "=" in calculator.buttons_frame.children
    assert "x\u00b2" in calculator.buttons_frame.children
    assert "\u221ax" in calculator.buttons_frame.children

if __name__ == "__main__":
    import pytest, sys
    sys.exit(pytest.main([__file__, "-v"]))