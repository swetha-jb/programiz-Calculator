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

    def rowconfigure(self, index, weight):
        pass

    def columnconfigure(self, index, weight):
        pass

def test_calculator_initialization(monkeypatch):
    mock_tk = MagicMock()
    mock_tk_instance = _WidgetMock()
    mock_tk.return_value = mock_tk_instance
    monkeypatch.setattr(tk, "Tk", mock_tk)

    mock_frame = _WidgetMock()
    monkeypatch.setattr(tk.Frame, "__init__", lambda self, *args, **kwargs: mock_frame)
    monkeypatch.setattr(tk.Frame, "pack", MagicMock())
    monkeypatch.setattr(tk.Frame, "grid", MagicMock())
    monkeypatch.setattr(tk.Frame, "rowconfigure", MagicMock())
    monkeypatch.setattr(tk.Frame, "columnconfigure", MagicMock())

    mock_label = _WidgetMock()
    monkeypatch.setattr(tk.Label, "__init__", lambda self, *args, **kwargs: mock_label)
    monkeypatch.setattr(tk.Label, "pack", MagicMock())
    monkeypatch.setattr(tk.Label, "config", MagicMock())

    mock_button = _WidgetMock()
    monkeypatch.setattr(tk.Button, "__init__", lambda self, *args, **kwargs: mock_button)
    monkeypatch.setattr(tk.Button, "grid", MagicMock())

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
    calc.label.config = MagicMock()
    calc.add_to_expression(5)
    assert calc.current_expression == "5"
    calc.add_to_expression(3)
    assert calc.current_expression == "53"
    calc.add_to_expression('.')
    assert calc.current_expression == "53."
    calc.label.config.assert_called_with(text=calc.current_expression[:11])

def test_append_operator():
    calc = Calculator()
    calc.total_label = _WidgetMock()
    calc.total_label.config = MagicMock()
    calc.label = _WidgetMock()
    calc.label.config = MagicMock()

    calc.current_expression = "12"
    calc.append_operator("+")
    assert calc.total_expression == "12+"
    assert calc.current_expression == ""
    calc.total_label.config.assert_called_with(text=' 12 + ')
    calc.label.config.assert_called_with(text="")

def test_clear():
    calc = Calculator()
    calc.total_label = _WidgetMock()
    calc.total_label.config = MagicMock()
    calc.label = _WidgetMock()
    calc.label.config = MagicMock()

    calc.total_expression = "12+3"
    calc.current_expression = "15"
    calc.clear()
    assert calc.total_expression == ""
    assert calc.current_expression == ""
    calc.label.config.assert_any_call(text="")
    calc.total_label.config.assert_any_call(text="")

def test_square():
    calc = Calculator()
    calc.current_expression = "5"
    calc.label = _WidgetMock()
    calc.label.config = MagicMock()
    calc.square()
    assert calc.current_expression == "25"
    calc.label.config.assert_called_with(text="25")

    calc.current_expression = "10"
    calc.square()
    assert calc.current_expression == "100"
    calc.label.config.assert_called_with(text="100")

def test_sqrt():
    calc = Calculator()
    calc.current_expression = "25"
    calc.label = _WidgetMock()
    calc.label.config = MagicMock()
    calc.sqrt()
    assert calc.current_expression == "5.0"
    calc.label.config.assert_called_with(text="5.0")

    calc.current_expression = "100"
    calc.sqrt()
    assert calc.current_expression == "10.0"
    calc.label.config.assert_called_with(text="10.0")

def test_evaluate_valid_expression(monkeypatch):
    calc = Calculator()
    calc.total_label = _WidgetMock()
    calc.total_label.config = MagicMock()
    calc.label = _WidgetMock()
    calc.label.config = MagicMock()

    calc.total_expression = "2+3"
    calc.current_expression = ""
    calc.evaluate()
    assert calc.current_expression == "5"
    assert calc.total_expression == ""
    calc.total_label.config.assert_called_with(text=' 2 + 3 ')
    calc.label.config.assert_called_with(text="5")

def test_evaluate_with_current_expression(monkeypatch):
    calc = Calculator()
    calc.total_label = _WidgetMock()
    calc.total_label.config = MagicMock()
    calc.label = _WidgetMock()
    calc.label.config = MagicMock()

    calc.total_expression = "10"
    calc.current_expression = "*2"
    calc.evaluate()
    assert calc.current_expression == "20"
    assert calc.total_expression == ""
    calc.total_label.config.assert_called_with(text=' 10 * 2 ')
    calc.label.config.assert_called_with(text="20")

def test_evaluate_error_expression(monkeypatch):
    calc = Calculator()
    calc.total_label = _WidgetMock()
    calc.total_label.config = MagicMock()
    calc.label = _WidgetMock()
    calc.label.config = MagicMock()

    calc.total_expression = "2+"
    calc.current_expression = ""
    calc.evaluate()
    assert calc.current_expression == "Error"
    assert calc.total_expression == "2+"
    calc.total_label.config.assert_called_with(text=' 2 + ')
    calc.label.config.assert_called_with(text="Error")

def test_update_label_truncation():
    calc = Calculator()
    calc.label = _WidgetMock()
    calc.label.config = MagicMock()
    calc.current_expression = "1234567890123"
    calc.update_label()
    calc.label.config.assert_called_with(text=calc.current_expression[:11])

def test_update_total_label_with_operators():
    calc = Calculator()
    calc.total_label = _WidgetMock()
    calc.total_label.config = MagicMock()
    calc.total_expression = "10*5-2"
    calc.update_total_label()
    calc.total_label.config.assert_called_