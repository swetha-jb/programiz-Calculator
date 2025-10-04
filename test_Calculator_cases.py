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

    def destroy(self):
        pass

    def rowconfigure(self, index, weight):
        pass

    def columnconfigure(self, index, weight):
        pass

@pytest.fixture
def mock_tkinter(monkeypatch):
    mock_tk = MagicMock()
    mock_tk_instance = _WidgetMock()
    mock_tk.return_value = mock_tk_instance
    monkeypatch.setattr(tk, "Tk", mock_tk)

    mock_frame = _WidgetMock()
    monkeypatch.setattr(tk.Frame, "__init__", MagicMock(return_value=None))
    monkeypatch.setattr(tk.Frame, "pack", MagicMock())
    monkeypatch.setattr(tk.Frame, "grid", MagicMock())
    monkeypatch.setattr(tk.Frame, "rowconfigure", MagicMock())
    monkeypatch.setattr(tk.Frame, "columnconfigure", MagicMock())

    mock_label = _WidgetMock()
    monkeypatch.setattr(tk.Label, "__init__", MagicMock(return_value=None))
    monkeypatch.setattr(tk.Label, "pack", MagicMock())
    monkeypatch.setattr(tk.Label, "config", MagicMock())

    mock_button = _WidgetMock()
    monkeypatch.setattr(tk.Button, "__init__", MagicMock(return_value=None))
    monkeypatch.setattr(tk.Button, "grid", MagicMock())

    return mock_tk_instance

def test_calculator_initialization(mock_tkinter, monkeypatch):
    calc = Calculator()
    assert calc.window == mock_tkinter
    assert calc.total_expression == ""
    assert calc.current_expression == ""
    assert calc.display_frame is not None
    assert calc.total_label is not None
    assert calc.label is not None
    assert calc.buttons_frame is not None

def test_add_to_expression(mock_tkinter, monkeypatch):
    mock_label = _WidgetMock()
    mock_label.config = MagicMock()
    monkeypatch.setattr(tk.Label, "__init__", lambda *args, **kwargs: mock_label)

    calc = Calculator()
    calc.label = mock_label

    calc.add_to_expression(5)
    assert calc.current_expression == "5"
    mock_label.config.assert_called_once_with(text="5")

    calc.add_to_expression("+")
    assert calc.current_expression == "5+"
    mock_label.config.assert_called_with(text="5+")

def test_append_operator(mock_tkinter, monkeypatch):
    mock_total_label = _WidgetMock()
    mock_total_label.config = MagicMock()
    mock_label = _WidgetMock()
    mock_label.config = MagicMock()

    monkeypatch.setattr(tk.Label, "__init__", lambda *args, **kwargs: mock_total_label if kwargs.get('font') == SMALL_FONT_STYLE else mock_label)

    calc = Calculator()
    calc.total_label = mock_total_label
    calc.label = mock_label

    calc.current_expression = "123"
    calc.append_operator("+")

    assert calc.current_expression == ""
    assert calc.total_expression == "123"
    mock_total_label.config.assert_called_once_with(text=" 123 ")
    mock_label.config.assert_called_once_with(text="")

def test_clear(mock_tkinter, monkeypatch):
    mock_total_label = _WidgetMock()
    mock_total_label.config = MagicMock()
    mock_label = _WidgetMock()
    mock_label.config = MagicMock()

    monkeypatch.setattr(tk.Label, "__init__", lambda *args, **kwargs: mock_total_label if kwargs.get('font') == SMALL_FONT_STYLE else mock_label)

    calc = Calculator()
    calc.total_label = mock_total_label
    calc.label = mock_label

    calc.total_expression = "1+2"
    calc.current_expression = "3"
    calc.clear()

    assert calc.total_expression == ""
    assert calc.current_expression == ""
    mock_label.config.assert_called_once_with(text="")
    mock_total_label.config.assert_called_once_with(text="")

def test_square(mock_tkinter, monkeypatch):
    mock_label = _WidgetMock()
    mock_label.config = MagicMock()
    monkeypatch.setattr(tk.Label, "__init__", lambda *args, **kwargs: mock_label)

    calc = Calculator()
    calc.label = mock_label

    calc.current_expression = "5"
    calc.square()
    assert calc.current_expression == "25"
    mock_label.config.assert_called_once_with(text="25")

    calc.current_expression = "2+3"
    calc.square()
    assert calc.current_expression == "25"
    mock_label.config.assert_called_with(text="25")

def test_sqrt(mock_tkinter, monkeypatch):
    mock_label = _WidgetMock()
    mock_label.config = MagicMock()
    monkeypatch.setattr(tk.Label, "__init__", lambda *args, **kwargs: mock_label)

    calc = Calculator()
    calc.label = mock_label

    calc.current_expression = "25"
    calc.sqrt()
    assert calc.current_expression == "5.0"
    mock_label.config.assert_called_once_with(text="5.0")

    calc.current_expression = "9"
    calc.sqrt()
    assert calc.current_expression == "3.0"
    mock_label.config.assert_called_with(text="3.0")

def test_evaluate_valid_expression(mock_tkinter, monkeypatch):
    mock_total_label = _WidgetMock()
    mock_total_label.config = MagicMock()
    mock_label = _WidgetMock()
    mock_label.config = MagicMock()

    monkeypatch.setattr(tk.Label, "__init__", lambda *args, **kwargs: mock_total_label if kwargs.get('font') == SMALL_FONT_STYLE else mock_label)

    calc = Calculator()
    calc.total_label = mock_total_label
    calc.label = mock_label

    calc.current_expression = "5"
    calc.total_expression = "2+3"
    calc.evaluate()

    assert calc.current_expression == "5"
    assert calc.total_expression == ""
    mock_total_label.config.assert_called_once_with(text=" 2 + 3 ")
    mock_label.config.assert_called_once_with(text="5")

def test_evaluate_error_expression(mock_tkinter, monkeypatch):
    mock_total_label = _WidgetMock()
    mock_total_label.config = MagicMock()
    mock_label = _WidgetMock()
    mock_label.config = MagicMock()

    monkeypatch.setattr(tk.Label, "__init__", lambda *args, **kwargs: mock_total_label if kwargs.get('font') == SMALL_FONT_STYLE else mock_label)

    calc = Calculator()
    calc.total_label = mock_total_label
    calc.label = mock_label