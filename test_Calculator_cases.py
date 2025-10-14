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
from unittest.mock import MagicMock, _WIDGET_BASE

sys.path.insert(0, r'/home/vvdn/projects/sfit_unitest_19_9_2025/cloned_repos/Calculator')

from calculator import Calculator, LARGE_FONT_STYLE, SMALL_FONT_STYLE, DIGITS_FONT_STYLE, DEFAULT_FONT_STYLE, OFF_WHITE, WHITE, LIGHT_BLUE, LIGHT_GRAY, LABEL_COLOR

class _WidgetMock(_WIDGET_BASE):
    def __init__(self, master=None, **kw):
        self._mock_master = master
        self._mock_config = {}
        self._mock_pack = {}
        self._mock_grid = {}
        self._mock_place = {}

    def config(self, **kw):
        self._mock_config.update(kw)

    def pack(self, **kw):
        self._mock_pack.update(kw)

    def grid(self, **kw):
        self._mock_grid.update(kw)

    def place(self, **kw):
        self._mock_place.update(kw)

    def bind(self, sequence, func, add=None):
        pass

    def unbind(self, sequence, add=None):
        pass

    def destroy(self):
        pass

    def __setitem__(self, key, value):
        self.config(**{key: value})

    def __getitem__(self, key):
        return self._mock_config.get(key)

@pytest.fixture
def mock_tkinter(monkeypatch):
    mock_tk = MagicMock()
    mock_tk_instance = MagicMock()
    mock_tk.return_value = mock_tk_instance

    mock_frame = MagicMock(spec=_WidgetMock)
    mock_label = MagicMock(spec=_WidgetMock)
    mock_button = MagicMock(spec=_WidgetMock)

    monkeypatch.setattr(sys.modules['tkinter'], 'Tk', mock_tk)
    monkeypatch.setattr(sys.modules['tkinter'], 'Frame', mock_frame)
    monkeypatch.setattr(sys.modules['tkinter'], 'Label', mock_label)
    monkeypatch.setattr(sys.modules['tkinter'], 'Button', mock_button)

    mock_tk_instance.Frame.return_value = mock_frame
    mock_tk_instance.Label.return_value = mock_label
    mock_tk_instance.Button.return_value = mock_button

    return mock_tk_instance

@pytest.fixture
def calculator(mock_tkinter):
    calc = Calculator()
    return calc

def test_calculator_initialization(calculator):
    assert calculator.total_expression == ""
    assert calculator.current_expression == ""
    assert calculator.window is not None
    assert calculator.display_frame is not None
    assert calculator.total_label is not None
    assert calculator.label is not None
    assert calculator.buttons_frame is not None

def test_add_to_expression(calculator):
    calculator.add_to_expression("5")
    assert calculator.current_expression == "5"
    calculator.add_to_expression("+")
    assert calculator.current_expression == "5+"

def test_append_operator(calculator):
    calculator.current_expression = "12"
    calculator.append_operator("+")
    assert calculator.total_expression == "12+"
    assert calculator.current_expression == ""

def test_clear(calculator):
    calculator.current_expression = "12+3"
    calculator.total_expression = "15"
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
    calculator.total_expression = "10+"
    calculator.evaluate()
    assert calculator.current_expression == "15"
    assert calculator.total_expression == ""

def test_evaluate_division_by_zero(calculator):
    calculator.current_expression = "0"
    calculator.total_expression = "10/"
    calculator.evaluate()
    assert calculator.current_expression == "Error"
    assert calculator.total_expression == "10/0"

def test_update_label(calculator):
    calculator.current_expression = "1234567890123"
    calculator.update_label()
    assert calculator.label.config.call_args[1]['text'] == "12345678901"

def test_update_total_label(calculator):
    calculator.total_expression = "10*5"
    calculator.update_total_label()
    assert calculator.total_label.config.call_args[1]['text'] == "10 × 5"

def test_bind_keys_return(calculator):
    calculator.window.bind.assert_any_call("<Return>", pytest.raises(Exception))

def test_bind_keys_digits(calculator):
    for digit in calculator.digits:
        calculator.window.bind.assert_any_call(str(digit), pytest.raises(Exception))

def test_bind_keys_operators(calculator):
    for operator in calculator.operations:
        calculator.window.bind.assert_any_call(operator, pytest.raises(Exception))

def test_create_digit_buttons(calculator):
    calculator.create_digit_buttons()
    assert calculator.buttons_frame.grid.call_count >= len(calculator.digits)

def test_create_operator_buttons(calculator):
    calculator.create_operator_buttons()
    assert calculator.buttons_frame.grid.call_count >= len(calculator.operations)

def test_create_special_buttons(calculator):
    calculator.create_special_buttons()
    assert calculator.buttons_frame.grid.call_count >= 4

if __name__ == "__main__":
    import pytest, sys
    sys.exit(pytest.main([__file__, "-v"]))