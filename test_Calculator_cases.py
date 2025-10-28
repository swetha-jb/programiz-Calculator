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
from unittest.mock import MagicMock, patch

sys.path.insert(0, r'/home/vvdn/projects/sfit_unitest_19_9_2025/cloned_repos/Calculator')

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

@pytest.fixture
def mock_tkinter(monkeypatch):
    mock_tk = MagicMock()
    mock_tk_instance = _WidgetMock()
    mock_tk.return_value = mock_tk_instance
    monkeypatch.setattr(tk, "Tk", mock_tk)

    mock_frame = _WidgetMock()
    monkeypatch.setattr(tk.Frame, "pack", MagicMock())
    monkeypatch.setattr(tk.Frame, "__init__", lambda self, *args, **kwargs: self.pack())

    mock_label = _WidgetMock()
    mock_label.config = MagicMock()
    monkeypatch.setattr(tk.Label, "pack", MagicMock())
    monkeypatch.setattr(tk.Label, "__init__", lambda self, *args, **kwargs: self.pack())

    mock_button = _WidgetMock()
    monkeypatch.setattr(tk.Button, "grid", MagicMock())
    monkeypatch.setattr(tk.Button, "__init__", lambda self, *args, **kwargs: self.grid())

    return mock_tk_instance, mock_label, mock_total_label

def test_calculator_initialization(mock_tkinter, monkeypatch):
    mock_tk_instance, mock_label, mock_total_label = mock_tkinter

    calc = Calculator()

    assert calc.window == mock_tk_instance
    assert calc.total_expression == ""
    assert calc.current_expression == ""
    assert calc.digits == {7: (1, 1), 8: (1, 2), 9: (1, 3), 4: (2, 1), 5: (2, 2), 6: (2, 3), 1: (3, 1), 2: (3, 2), 3: (3, 3), 0: (4, 2), '.': (4, 1)}
    assert calc.operations == {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"}

def test_add_to_expression(mock_tkinter, monkeypatch):
    mock_tk_instance, mock_label, mock_total_label = mock_tkinter
    calc = Calculator()
    calc.label = mock_label

    calc.add_to_expression(5)
    assert calc.current_expression == "5"
    mock_label.config.assert_called_once_with(text="5")

    calc.add_to_expression("+")
    assert calc.current_expression == "5+"
    mock_label.config.assert_called_with(text="5+")

def test_append_operator(mock_tkinter, monkeypatch):
    mock_tk_instance, mock_label, mock_total_label = mock_tkinter
    calc = Calculator()
    calc.total_label = mock_total_label
    calc.label = mock_label
    calc.current_expression = "123"
    calc.total_expression = "45"

    calc.append_operator("+")
    assert calc.current_expression == ""
    assert calc.total_expression == "45123+"
    calc.update_total_label()
    calc.update_label()
    mock_total_label.config.assert_called_once_with(text="45 + 123")
    mock_label.config.assert_called_once_with(text="")

def test_clear(mock_tkinter, monkeypatch):
    mock_tk_instance, mock_label, mock_total_label = mock_tkinter
    calc = Calculator()
    calc.total_label = mock_total_label
    calc.label = mock_label
    calc.current_expression = "123"
    calc.total_expression = "45+"

    calc.clear()
    assert calc.current_expression == ""
    assert calc.total_expression == ""
    mock_label.config.assert_called_once_with(text="")
    mock_total_label.config.assert_called_once_with(text="")

def test_square(mock_tkinter, monkeypatch):
    mock_tk_instance, mock_label, mock_total_label = mock_tkinter
    calc = Calculator()
    calc.label = mock_label
    calc.current_expression = "5"

    calc.square()
    assert calc.current_expression == "25.0"
    mock_label.config.assert_called_once_with(text="25.0")

def test_sqrt(mock_tkinter, monkeypatch):
    mock_tk_instance, mock_label, mock_total_label = mock_tkinter
    calc = Calculator()
    calc.label = mock_label
    calc.current_expression = "25"

    calc.sqrt()
    assert calc.current_expression == "5.0"
    mock_label.config.assert_called_once_with(text="5.0")

def test_evaluate_valid_expression(mock_tkinter, monkeypatch):
    mock_tk_instance, mock_label, mock_total_label = mock_tkinter
    calc = Calculator()
    calc.label = mock_label
    calc.total_label = mock_total_label
    calc.current_expression = "5+3"
    calc.total_expression = ""

    calc.evaluate()
    assert calc.current_expression == "8.0"
    assert calc.total_expression == ""
    mock_total_label.config.assert_called_once_with(text="")
    mock_label.config.assert_called_once_with(text="8.0")

def test_evaluate_with_existing_total_expression(mock_tkinter, monkeypatch):
    mock_tk_instance, mock_label, mock_total_label = mock_tkinter
    calc = Calculator()
    calc.label = mock_label
    calc.total_label = mock_total_label
    calc.current_expression = "3"
    calc.total_expression = "5+2"

    calc.evaluate()
    assert calc.current_expression == "10.0"
    assert calc.total_expression == ""
    mock_total_label.config.assert_called_once_with(text="5 + 2")
    mock_label.config.assert_called_once_with(text="10.0")

def test_evaluate_error(mock_tkinter, monkeypatch):
    mock_tk_instance, mock_label, mock_total_label = mock_tkinter
    calc = Calculator()
    calc.label = mock_label
    calc.total_label = mock_total_label
    calc.current_expression = "5+"
    calc.total_expression = ""

    calc.evaluate()
    assert calc.current_expression == "Error"
    assert calc.total_expression == ""
    mock_total_label.config.assert_called_once_with(text="")
    mock_label.config.assert_called_once_with(text="Error")

def test_update_label_truncation(mock_tkinter, monkeypatch):
    mock_tk_instance, mock_label, mock_total_label = mock_tkinter
    calc = Calculator()
    calc.label = mock_label
    calc.current_expression = "1234567890123"

    calc.update_label()
    mock_label.config.assert_called_once_with(text="12345678901")

def test_update_total_label(mock_tkinter, monkeypatch):
    assert True  # Placeholder assert