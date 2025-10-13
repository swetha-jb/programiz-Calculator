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
sys.path.insert(0, r'/home/vvdn/projects/sfit_unitest_19_9_2025/cloned_repos/Calculator')

import tkinter as tk
from unittest.mock import MagicMock

from calculator import Calculator, LARGE_FONT_STYLE, SMALL_FONT_STYLE, DIGITS_FONT_STYLE, DEFAULT_FONT_STYLE, OFF_WHITE, WHITE, LIGHT_BLUE, LIGHT_GRAY, LABEL_COLOR

class _WidgetMock(MagicMock):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.children = {}

    def __setitem__(self, key, value):
        self.children[key] = value

    def __getitem__(self, key):
        return self.children[key]

    def configure(self, **kwargs):
        pass

    def pack(self, **kwargs):
        pass

    def grid(self, **kwargs):
        pass

    def bind(self, **kwargs):
        pass

    def config(self, **kwargs):
        pass

    def mainloop(self):
        pass

    def destroy(self):
        pass

def test_calculator_initialization(monkeypatch):
    mock_tk = MagicMock()
    mock_tk_instance = _WidgetMock()
    mock_tk.return_value = mock_tk_instance
    monkeypatch.setattr(tk, "Tk", mock_tk)

    mock_frame = _WidgetMock()
    monkeypatch.setattr(tk.Frame, "return_value", mock_frame)

    mock_label = _WidgetMock()
    monkeypatch.setattr(tk.Label, "return_value", mock_label)

    mock_button = _WidgetMock()
    monkeypatch.setattr(tk.Button, "return_value", mock_button)

    calc = Calculator()

    assert calc.window == mock_tk_instance
    assert calc.total_expression == ""
    assert calc.current_expression == ""
    assert calc.display_frame == mock_frame
    assert calc.total_label == mock_label
    assert calc.label == mock_label
    assert calc.buttons_frame == mock_frame

def test_add_to_expression():
    calc = Calculator()
    calc.label = _WidgetMock()
    calc.update_label = MagicMock()

    calc.add_to_expression(5)
    assert calc.current_expression == "5"
    calc.update_label.assert_called_once()

    calc.add_to_expression("+")
    assert calc.current_expression == "5+"
    calc.update_label.assert_called_once()

def test_append_operator():
    calc = Calculator()
    calc.total_label = _WidgetMock()
    calc.label = _WidgetMock()
    calc.update_label = MagicMock()
    calc.update_total_label = MagicMock()

    calc.current_expression = "12"
    calc.total_expression = "3"
    calc.append_operator("+")

    assert calc.total_expression == "312"
    assert calc.current_expression == ""
    calc.update_total_label.assert_called_once()
    calc.update_label.assert_called_once()

def test_clear():
    calc = Calculator()
    calc.total_label = _WidgetMock()
    calc.label = _WidgetMock()
    calc.update_label = MagicMock()
    calc.update_total_label = MagicMock()

    calc.current_expression = "123"
    calc.total_expression = "456"
    calc.clear()

    assert calc.current_expression == ""
    assert calc.total_expression == ""
    calc.update_label.assert_called_once()
    calc.update_total_label.assert_called_once()

def test_square():
    calc = Calculator()
    calc.label = _WidgetMock()
    calc.update_label = MagicMock()

    calc.current_expression = "5"
    calc.square()
    assert calc.current_expression == "25"
    calc.update_label.assert_called_once()

    calc.current_expression = "2+3"
    calc.square()
    assert calc.current_expression == "25"
    calc.update_label.assert_called_once()

def test_sqrt():
    calc = Calculator()
    calc.label = _WidgetMock()
    calc.update_label = MagicMock()

    calc.current_expression = "25"
    calc.sqrt()
    assert calc.current_expression == "5.0"
    calc.update_label.assert_called_once()

    calc.current_expression = "9"
    calc.sqrt()
    assert calc.current_expression == "3.0"
    calc.update_label.assert_called_once()

def test_evaluate_valid_expression():
    calc = Calculator()
    calc.total_label = _WidgetMock()
    calc.label = _WidgetMock()
    calc.update_label = MagicMock()
    calc.update_total_label = MagicMock()

    calc.current_expression = "5"
    calc.total_expression = "2+3"
    calc.evaluate()

    assert calc.total_expression == ""
    assert calc.current_expression == "10"
    calc.update_total_label.assert_called_once()
    calc.update_label.assert_called_once()

def test_evaluate_division_by_zero():
    calc = Calculator()
    calc.total_label = _WidgetMock()
    calc.label = _WidgetMock()
    calc.update_label = MagicMock()
    calc.update_total_label = MagicMock()

    calc.current_expression = "0"
    calc.total_expression = "5/"
    calc.evaluate()

    assert calc.total_expression == ""
    assert calc.current_expression == "Error"
    calc.update_total_label.assert_called_once()
    calc.update_label.assert_called_once()

def test_update_total_label():
    calc = Calculator()
    calc.total_label = _WidgetMock()

    calc.total_expression = "1+2*3"
    calc.update_total_label()
    calc.total_label.config.assert_called_with(text='1 + 2 * 3')

    calc.total_expression = "10/5-2"
    calc.update_total_label()
    calc.total_label.config.assert_called_with(text='10 ÷ 5 - 2')

def test_update_label():
    calc = Calculator()
    calc.label = _WidgetMock()

    calc.current_expression = "1234567890123"
    calc.update_label()
    calc.label.config.assert_called_with(text='12345678901')

    calc.current_expression = "abc"
    calc.update_label()
    calc.label.config.assert_called_with(text='abc')

def test_bind_keys_return(monkeypatch):
    mock_window = _WidgetMock()
    mock_evaluate = MagicMock()
    monkeypatch.setattr(mock_window, "bind", MagicMock())
    monkeypatch.setattr(Calculator, "evaluate", mock_evaluate)

    calc = Calculator()
    calc.window = mock_window
    calc.bind_keys()

    mock_window.bind.assert_any_call("<Return>", calc.evaluate)

def test_bind_keys_digits(monkeypatch):
    mock_window = _WidgetMock()
    mock_add_to_expression = MagicMock()
    monkeypatch.setattr(mock_window, "bind", MagicMock())
    monkeypatch.setattr(Calculator, "add_to_expression", mock_add_to_expression)

    calc = Calculator()
    calc.window = mock_window
    calc.bind_keys()

    for digit in calc.digits:
        mock_window.bind.assert_any_call(str(digit), lambda event, digit=digit: calc.add_to_expression(digit))

def test_bind_keys_operators(monkeypatch):
    mock_window = _WidgetMock()
    mock_append_operator = MagicMock()
    monkeypatch.setattr(mock_window, "bind", MagicMock())
    monkeypatch.setattr(Calculator, "append_operator", mock_append_operator)

    calc = Calculator()
    calc.window = mock_window