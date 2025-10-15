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

    def __getattr__(self, name):
        return MagicMock()

    def add_command(self, *args, **kwargs):
        pass

    def insert(self, *args, **kwargs):
        pass

    def delete(self, *args, **kwargs):
        pass

    def get(self, *args, **kwargs):
        return ""

    def configure(self, **kwargs):
        pass

    def update_idletasks(self):
        pass

    def mainloop(self):
        pass

@pytest.fixture
def mock_tkinter():
    with patch('tkinter.Tk', new=_WidgetMock) as mock_tk, \
         patch('tkinter.Frame', new=_WidgetMock) as mock_frame, \
         patch('tkinter.Label', new=_WidgetMock) as mock_label, \
         patch('tkinter.Button', new=_WidgetMock) as mock_button:
        yield mock_tk, mock_frame, mock_label, mock_button

def test_calculator_initialization(mock_tkinter):
    mock_tk, mock_frame, mock_label, mock_button = mock_tkinter
    calc = Calculator()
    assert calc.total_expression == ""
    assert calc.current_expression == ""
    assert isinstance(calc.window, _WidgetMock)
    assert isinstance(calc.display_frame, _WidgetMock)
    assert isinstance(calc.total_label, _WidgetMock)
    assert isinstance(calc.label, _WidgetMock)
    assert isinstance(calc.buttons_frame, _WidgetMock)

def test_add_to_expression(mock_tkinter):
    calc = Calculator()
    calc.add_to_expression(5)
    assert calc.current_expression == "5"
    calc.add_to_expression("+")
    assert calc.current_expression == "5+"

def test_append_operator(mock_tkinter):
    calc = Calculator()
    calc.current_expression = "123"
    calc.append_operator("+")
    assert calc.total_expression == "123+"
    assert calc.current_expression == ""

def test_clear(mock_tkinter):
    calc = Calculator()
    calc.total_expression = "1+2"
    calc.current_expression = "3"
    calc.clear()
    assert calc.total_expression == ""
    assert calc.current_expression == ""

def test_square(mock_tkinter):
    calc = Calculator()
    calc.current_expression = "5"
    calc.square()
    assert calc.current_expression == "25"

def test_sqrt(mock_tkinter):
    calc = Calculator()
    calc.current_expression = "25"
    calc.sqrt()
    assert calc.current_expression == "5.0"

def test_evaluate_valid_expression(mock_tkinter):
    calc = Calculator()
    calc.total_expression = "2+2"
    calc.current_expression = ""
    calc.evaluate()
    assert calc.current_expression == "4"
    assert calc.total_expression == ""

def test_evaluate_with_current_expression(mock_tkinter):
    calc = Calculator()
    calc.total_expression = "2+2"
    calc.current_expression = "5"
    calc.evaluate()
    assert calc.current_expression == "9"
    assert calc.total_expression == ""

def test_evaluate_error(mock_tkinter):
    calc = Calculator()
    calc.total_expression = "2+"
    calc.current_expression = ""
    calc.evaluate()
    assert calc.current_expression == "Error"
    assert calc.total_expression == "2+"

def test_update_label(mock_tkinter):
    calc = Calculator()
    calc.current_expression = "1234567890123"
    calc.update_label()
    assert calc.label.config.call_args[1]['text'] == "12345678901"

def test_update_total_label(mock_tkinter):
    calc = Calculator()
    calc.total_expression = "1+2*3"
    calc.update_total_label()
    assert calc.total_label.config.call_args[1]['text'] == "1 + 2 * 3"

def test_bind_keys_return(mock_tkinter):
    calc = Calculator()
    calc.window.bind.assert_any_call("<Return>", pytest.raises(TypeError)) # Mocking lambda

def test_bind_keys_digits(mock_tkinter):
    calc = Calculator()
    calc.window.bind.assert_any_call("7", pytest.raises(TypeError)) # Mocking lambda

def test_bind_keys_operators(mock_tkinter):
    calc = Calculator()
    calc.window.bind.assert_any_call("+", pytest.raises(TypeError)) # Mocking lambda

def test_create_digit_buttons(mock_tkinter):
    calc = Calculator()
    assert len(calc.digits) == 11
    for digit, grid_value in calc.digits.items():
        call_args = None
        for call in mock_button.call_args_list:
            if call[1]['text'] == str(digit):
                call_args = call
                break
        assert call_args is not None
        assert call_args[1]['command'].__closure__[0].cell_contents == digit

def test_create_operator_buttons(mock_tkinter):
    calc = Calculator()
    assert len(calc.operations) == 4
    for i, (operator, symbol) in enumerate(calc.operations.items()):
        call_args = None
        for call in mock_button.call_args_list:
            if call[1]['text'] == symbol:
                call_args = call
                break
        assert call_args is not None
        assert call_args[1]['command'].__closure__[0].cell_contents == operator
        assert call_args[0][0] == calc.buttons_frame
        assert call_args[1]['grid'][0] == i
        assert call_args[1]['grid'][1] == 4

def test_create_special_buttons(mock_tkinter):
    calc = Calculator()
    mock_button_calls = [call[1]['text'] for call in mock_button.call_args_list]
    assert "C" in mock_button_calls
    assert "=" in mock_button_calls
    assert "x²" in mock_button_calls
    assert "\u221ax" in mock_button_calls

if __name__ == "__main__":
    import pytest, sys
    sys.exit(pytest.main([__file__, "-v"]))