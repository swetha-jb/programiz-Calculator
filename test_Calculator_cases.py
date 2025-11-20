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

from calculator import Calculator

class _WidgetMock(MagicMock):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.children = {}

    def __setitem__(self, key, value):
        self.children[key] = value

    def __getitem__(self, key):
        return self.children[key]

    def grid(self, **kwargs):
        pass

    def pack(self, **kwargs):
        pass

    def configure(self, **kwargs):
        pass

    def config(self, **kwargs):
        pass

    def bind(self, key, func):
        pass

    def mainloop(self):
        pass

    def rowconfigure(self, index, weight):
        pass

    def columnconfigure(self, index, weight):
        pass

def test_calculator_initialization():
    mock_tk = MagicMock()
    mock_tk.Tk.return_value = _WidgetMock()
    tk.Tk = mock_tk

    calc = Calculator()

    assert calc.window is not None
    assert calc.total_expression == ""
    assert calc.current_expression == ""
    assert calc.display_frame is not None
    assert calc.total_label is not None
    assert calc.label is not None
    assert calc.buttons_frame is not None

def test_add_to_expression():
    mock_tk = MagicMock()
    mock_tk.Tk.return_value = _WidgetMock()
    tk.Tk = mock_tk
    mock_label = _WidgetMock()
    mock_label.config = MagicMock()
    mock_tk.Tk.return_value.display_frame.label = mock_label

    calc = Calculator()
    calc.label = mock_label
    calc.add_to_expression(5)
    assert calc.current_expression == "5"
    calc.add_to_expression(3)
    assert calc.current_expression == "53"
    calc.add_to_expression('.')
    assert calc.current_expression == "53."
    calc.add_to_expression(0)
    assert calc.current_expression == "53.0"
    calc.label.config.assert_called_with(text="53.0")

def test_append_operator():
    mock_tk = MagicMock()
    mock_tk.Tk.return_value = _WidgetMock()
    tk.Tk = mock_tk
    mock_total_label = _WidgetMock()
    mock_total_label.config = MagicMock()
    mock_label = _WidgetMock()
    mock_label.config = MagicMock()
    mock_tk.Tk.return_value.display_frame.total_label = mock_total_label
    mock_tk.Tk.return_value.display_frame.label = mock_label

    calc = Calculator()
    calc.total_label = mock_total_label
    calc.label = mock_label
    calc.current_expression = "12"
    calc.append_operator("+")
    assert calc.current_expression == ""
    assert calc.total_expression == "12+"
    calc.total_label.config.assert_called_with(text=" 12 + ")
    calc.label.config.assert_called_with(text="")

def test_clear():
    mock_tk = MagicMock()
    mock_tk.Tk.return_value = _WidgetMock()
    tk.Tk = mock_tk
    mock_total_label = _WidgetMock()
    mock_total_label.config = MagicMock()
    mock_label = _WidgetMock()
    mock_label.config = MagicMock()
    mock_tk.Tk.return_value.display_frame.total_label = mock_total_label
    mock_tk.Tk.return_value.display_frame.label = mock_label

    calc = Calculator()
    calc.total_label = mock_total_label
    calc.label = mock_label
    calc.total_expression = "1+2"
    calc.current_expression = "3"
    calc.clear()
    assert calc.total_expression == ""
    assert calc.current_expression == ""
    calc.label.config.assert_called_with(text="")
    calc.total_label.config.assert_called_with(text="")

def test_square():
    mock_tk = MagicMock()
    mock_tk.Tk.return_value = _WidgetMock()
    tk.Tk = mock_tk
    mock_label = _WidgetMock()
    mock_label.config = MagicMock()
    mock_tk.Tk.return_value.display_frame.label = mock_label

    calc = Calculator()
    calc.label = mock_label
    calc.current_expression = "5"
    calc.square()
    assert calc.current_expression == "25"
    calc.label.config.assert_called_with(text="25")

    calc.current_expression = "-3"
    calc.square()
    assert calc.current_expression == "9"
    calc.label.config.assert_called_with(text="9")

def test_sqrt():
    mock_tk = MagicMock()
    mock_tk.Tk.return_value = _WidgetMock()
    tk.Tk = mock_tk
    mock_label = _WidgetMock()
    mock_label.config = MagicMock()
    mock_tk.Tk.return_value.display_frame.label = mock_label

    calc = Calculator()
    calc.label = mock_label
    calc.current_expression = "25"
    calc.sqrt()
    assert calc.current_expression == "5.0"
    calc.label.config.assert_called_with(text="5.0")

    calc.current_expression = "2"
    calc.sqrt()
    assert calc.current_expression == "1.4142135623730951"
    calc.label.config.assert_called_with(text="1.4142135623730951")

def test_evaluate_valid_expression():
    mock_tk = MagicMock()
    mock_tk.Tk.return_value = _WidgetMock()
    tk.Tk = mock_tk
    mock_total_label = _WidgetMock()
    mock_total_label.config = MagicMock()
    mock_label = _WidgetMock()
    mock_label.config = MagicMock()
    mock_tk.Tk.return_value.display_frame.total_label = mock_total_label
    mock_tk.Tk.return_value.display_frame.label = mock_label

    calc = Calculator()
    calc.total_label = mock_total_label
    calc.label = mock_label
    calc.total_expression = "2+3"
    calc.current_expression = "5"
    calc.evaluate()
    assert calc.current_expression == "5"
    assert calc.total_expression == ""
    calc.label.config.assert_called_with(text="5")
    calc.total_label.config.assert_called_with(text=" 2 + 3 ")

def test_evaluate_expression_with_operators():
    mock_tk = MagicMock()
    mock_tk.Tk.return_value = _WidgetMock()
    tk.Tk = mock_tk
    mock_total_label = _WidgetMock()
    mock_total_label.config = MagicMock()
    mock_label = _WidgetMock()
    mock_label.config = MagicMock()
    mock_tk.Tk.return_value.display_frame.total_label = mock_total_label
    mock_tk.Tk.return_value.display_frame.label = mock_label

    calc = Calculator()
    calc.total_label = mock_total_label
    calc.label = mock_label
    calc.total_expression = "10*5"
    calc.current_expression = "50"
    calc.evaluate()
    assert calc.current_expression == "50"
    assert calc.total_expression == ""
    calc.label.config.assert_called_with(text="50")
    calc.total_label.config.assert_called_with(text=" 10 × 5 ")

def test_evaluate_error_expression():
    mock_tk = MagicMock()