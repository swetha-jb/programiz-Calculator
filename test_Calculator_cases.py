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

    def pack(self, *args, **kwargs):
        pass

    def grid(self, *args, **kwargs):
        pass

    def configure(self, *args, **kwargs):
        pass

    def config(self, *args, **kwargs):
        pass

    def bind(self, *args, **kwargs):
        pass

    def mainloop(self, *args, **kwargs):
        pass

    def destroy(self, *args, **kwargs):
        pass

    def rowconfigure(self, *args, **kwargs):
        pass

    def columnconfigure(self, *args, **kwargs):
        pass

def test_calculator_initialization(monkeypatch):
    mock_tk = MagicMock()
    mock_tk.Tk.return_value = _WidgetMock()
    monkeypatch.setattr(tk, "Tk", mock_tk)

    calc = Calculator()

    assert calc.total_expression == ""
    assert calc.current_expression == ""
    assert isinstance(calc.window, _WidgetMock)
    assert calc.window.geometry.called_with("375x667")
    assert calc.window.resizable.called_with(0, 0)
    assert calc.window.title.called_with("Calculator")
    assert isinstance(calc.display_frame, _WidgetMock)
    assert isinstance(calc.total_label, _WidgetMock)
    assert isinstance(calc.label, _WidgetMock)
    assert isinstance(calc.buttons_frame, _WidgetMock)

def test_add_to_expression(monkeypatch):
    mock_tk = MagicMock()
    mock_tk.Tk.return_value = _WidgetMock()
    monkeypatch.setattr(tk, "Tk", mock_tk)

    calc = Calculator()
    calc.update_label = MagicMock()

    calc.add_to_expression(5)
    assert calc.current_expression == "5"
    calc.update_label.assert_called_once()

    calc.add_to_expression("+")
    assert calc.current_expression == "5+"
    calc.update_label.assert_called_once()

def test_append_operator(monkeypatch):
    mock_tk = MagicMock()
    mock_tk.Tk.return_value = _WidgetMock()
    monkeypatch.setattr(tk, "Tk", mock_tk)

    calc = Calculator()
    calc.update_label = MagicMock()
    calc.update_total_label = MagicMock()

    calc.current_expression = "123"
    calc.append_operator("+")

    assert calc.total_expression == "123+"
    assert calc.current_expression == ""
    calc.update_total_label.assert_called_once()
    calc.update_label.assert_called_once()

def test_clear(monkeypatch):
    mock_tk = MagicMock()
    mock_tk.Tk.return_value = _WidgetMock()
    monkeypatch.setattr(tk, "Tk", mock_tk)

    calc = Calculator()
    calc.update_label = MagicMock()
    calc.update_total_label = MagicMock()

    calc.total_expression = "1+2"
    calc.current_expression = "3"
    calc.clear()

    assert calc.total_expression == ""
    assert calc.current_expression == ""
    calc.update_label.assert_called_once()
    calc.update_total_label.assert_called_once()

def test_square(monkeypatch):
    mock_tk = MagicMock()
    mock_tk.Tk.return_value = _WidgetMock()
    monkeypatch.setattr(tk, "Tk", mock_tk)

    calc = Calculator()
    calc.update_label = MagicMock()

    calc.current_expression = "5"
    calc.square()
    assert calc.current_expression == "25"
    calc.update_label.assert_called_once()

    calc.current_expression = "-3"
    calc.square()
    assert calc.current_expression == "9"
    calc.update_label.assert_called_once()

def test_sqrt(monkeypatch):
    mock_tk = MagicMock()
    mock_tk.Tk.return_value = _WidgetMock()
    monkeypatch.setattr(tk, "Tk", mock_tk)

    calc = Calculator()
    calc.update_label = MagicMock()

    calc.current_expression = "25"
    calc.sqrt()
    assert calc.current_expression == "5.0"
    calc.update_label.assert_called_once()

    calc.current_expression = "2"
    calc.sqrt()
    assert calc.current_expression == "1.4142135623730951"
    calc.update_label.assert_called_once()

def test_evaluate_valid_expression(monkeypatch):
    mock_tk = MagicMock()
    mock_tk.Tk.return_value = _WidgetMock()
    monkeypatch.setattr(tk, "Tk", mock_tk)

    calc = Calculator()
    calc.update_label = MagicMock()
    calc.update_total_label = MagicMock()

    calc.total_expression = "2+3"
    calc.current_expression = "5"
    calc.evaluate()

    assert calc.current_expression == "10.0"
    assert calc.total_expression == ""
    calc.update_total_label.assert_called_once()
    calc.update_label.assert_called_once()

def test_evaluate_division_by_zero(monkeypatch):
    mock_tk = MagicMock()
    mock_tk.Tk.return_value = _WidgetMock()
    monkeypatch.setattr(tk, "Tk", mock_tk)

    calc = Calculator()
    calc.update_label = MagicMock()
    calc.update_total_label = MagicMock()

    calc.total_expression = "10/0"
    calc.current_expression = ""
    calc.evaluate()

    assert calc.current_expression == "Error"
    assert calc.total_expression == "10/0"
    calc.update_total_label.assert_called_once()
    calc.update_label.assert_called_once()

def test_update_label(monkeypatch):
    mock_tk = MagicMock()
    mock_tk.Tk.return_value = _WidgetMock()
    mock_label = _WidgetMock()
    mock_tk.Tk.return_value.display_frame.label = mock_label
    monkeypatch.setattr(tk, "Tk", mock_tk)

    calc = Calculator()
    calc.current_expression = "1234567890123"
    calc.update_label()

    mock_label.config.assert_called_once_with(text="12345678901")

def test_update_total_label(monkeypatch):
    mock_tk = MagicMock()
    mock_tk.Tk.return_value = _WidgetMock()
    mock_total_label = _WidgetMock()
    mock_tk.Tk.return_value.display_frame.total_label = mock_total_label
    monkeypatch.setattr(tk, "Tk", mock_tk)

    calc = Calculator()
    calc.total_expression = "2*3+4"
    calc.update_total_label()

    mock_total_label.config.assert_called_once_with(text="2  3  + 4 ")

def test_bind_keys_return(monkeypatch):
    mock_tk = MagicMock()
    mock_window = _WidgetMock()
    mock_tk.Tk.return_value = mock_window
    monkeypatch.setattr(tk, "Tk", mock_tk)