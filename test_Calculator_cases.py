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

    def configure(self, **kwargs):
        pass

    def pack(self, **kwargs):
        pass

    def grid(self, **kwargs):
        pass

    def bind(self, key, func):
        pass

    def config(self, **kwargs):
        pass

    def mainloop(self):
        pass

    def destroy(self):
        pass

def test_calculator_initialization():
    mock_tk = MagicMock(spec=tk)
    mock_tk.Tk.return_value = _WidgetMock()
    mock_tk.Frame.return_value = _WidgetMock()
    mock_tk.Label.return_value = _WidgetMock()
    mock_tk.Button.return_value = _WidgetMock()

    with unittest.mock.patch('tkinter.Tk', mock_tk.Tk):
        calc = Calculator()

    assert calc.window is not None
    assert calc.total_expression == ""
    assert calc.current_expression == ""
    assert calc.display_frame is not None
    assert calc.total_label is not None
    assert calc.label is not None
    assert calc.buttons_frame is not None

def test_add_to_expression():
    mock_tk = MagicMock(spec=tk)
    mock_tk.Tk.return_value = _WidgetMock()
    mock_tk.Frame.return_value = _WidgetMock()
    mock_tk.Label.return_value = _WidgetMock()
    mock_tk.Button.return_value = _WidgetMock()

    with unittest.mock.patch('tkinter.Tk', mock_tk.Tk):
        calc = Calculator()

    calc.add_to_expression(5)
    assert calc.current_expression == "5"
    calc.add_to_expression("+")
    assert calc.current_expression == "5+"

def test_append_operator():
    mock_tk = MagicMock(spec=tk)
    mock_tk.Tk.return_value = _WidgetMock()
    mock_tk.Frame.return_value = _WidgetMock()
    mock_tk.Label.return_value = _WidgetMock()
    mock_tk.Button.return_value = _WidgetMock()

    with unittest.mock.patch('tkinter.Tk', mock_tk.Tk):
        calc = Calculator()

    calc.current_expression = "123"
    calc.append_operator("+")
    assert calc.total_expression == "123+"
    assert calc.current_expression == ""

def test_clear():
    mock_tk = MagicMock(spec=tk)
    mock_tk.Tk.return_value = _WidgetMock()
    mock_tk.Frame.return_value = _WidgetMock()
    mock_tk.Label.return_value = _WidgetMock()
    mock_tk.Button.return_value = _WidgetMock()

    with unittest.mock.patch('tkinter.Tk', mock_tk.Tk):
        calc = Calculator()

    calc.total_expression = "1+2"
    calc.current_expression = "3"
    calc.clear()
    assert calc.total_expression == ""
    assert calc.current_expression == ""

def test_square():
    mock_tk = MagicMock(spec=tk)
    mock_tk.Tk.return_value = _WidgetMock()
    mock_tk.Frame.return_value = _WidgetMock()
    mock_tk.Label.return_value = _WidgetMock()
    mock_tk.Button.return_value = _WidgetMock()

    with unittest.mock.patch('tkinter.Tk', mock_tk.Tk):
        calc = Calculator()

    calc.current_expression = "5"
    calc.square()
    assert calc.current_expression == "25"

def test_sqrt():
    mock_tk = MagicMock(spec=tk)
    mock_tk.Tk.return_value = _WidgetMock()
    mock_tk.Frame.return_value = _WidgetMock()
    mock_tk.Label.return_value = _WidgetMock()
    mock_tk.Button.return_value = _WidgetMock()

    with unittest.mock.patch('tkinter.Tk', mock_tk.Tk):
        calc = Calculator()

    calc.current_expression = "25"
    calc.sqrt()
    assert calc.current_expression == "5.0"

def test_evaluate_valid_expression():
    mock_tk = MagicMock(spec=tk)
    mock_tk.Tk.return_value = _WidgetMock()
    mock_tk.Frame.return_value = _WidgetMock()
    mock_tk.Label.return_value = _WidgetMock()
    mock_tk.Button.return_value = _WidgetMock()

    with unittest.mock.patch('tkinter.Tk', mock_tk.Tk):
        calc = Calculator()

    calc.total_expression = "2+3"
    calc.current_expression = ""
    calc.evaluate()
    assert calc.current_expression == "5"
    assert calc.total_expression == ""

def test_evaluate_expression_with_current():
    mock_tk = MagicMock(spec=tk)
    mock_tk.Tk.return_value = _WidgetMock()
    mock_tk.Frame.return_value = _WidgetMock()
    mock_tk.Label.return_value = _WidgetMock()
    mock_tk.Button.return_value = _WidgetMock()

    with unittest.mock.patch('tkinter.Tk', mock_tk.Tk):
        calc = Calculator()

    calc.total_expression = "10"
    calc.current_expression = "*2"
    calc.evaluate()
    assert calc.current_expression == "20"
    assert calc.total_expression == ""

def test_evaluate_division_by_zero():
    mock_tk = MagicMock(spec=tk)
    mock_tk.Tk.return_value = _WidgetMock()
    mock_tk.Frame.return_value = _WidgetMock()
    mock_tk.Label.return_value = _WidgetMock()
    mock_tk.Button.return_value = _WidgetMock()

    with unittest.mock.patch('tkinter.Tk', mock_tk.Tk):
        calc = Calculator()

    calc.total_expression = "10/0"
    calc.current_expression = ""
    calc.evaluate()
    assert calc.current_expression == "Error"
    assert calc.total_expression == ""

def test_bind_keys_digits():
    mock_tk = MagicMock(spec=tk)
    mock_tk.Tk.return_value = _WidgetMock()
    mock_tk.Frame.return_value = _WidgetMock()
    mock_tk.Label.return_value = _WidgetMock()
    mock_tk.Button.return_value = _WidgetMock()

    with unittest.mock.patch('tkinter.Tk', mock_tk.Tk):
        calc = Calculator()

    calc.window.bind.assert_any_call("<Return>", unittest.mock.ANY)
    for digit in calc.digits:
        calc.window.bind.assert_any_call(str(digit), unittest.mock.ANY)

def test_bind_keys_operators():
    mock_tk = MagicMock(spec=tk)
    mock_tk.Tk.return_value = _WidgetMock()
    mock_tk.Frame.return_value = _WidgetMock()
    mock_tk.Label.return_value = _WidgetMock()
    mock_tk.Button.return_value = _WidgetMock()

    with unittest.mock.patch('tkinter.Tk', mock_tk.Tk):
        calc = Calculator()

    for operator in calc.operations:
        calc.window.bind.assert_any_call(operator, unittest.mock.ANY)

def test_update_label():
    mock_tk = MagicMock(spec=tk)
    mock_tk.Tk.return_value = _WidgetMock()
    mock_tk.Frame.return_value = _WidgetMock()
    mock_label = _WidgetMock()
    mock_tk.Label.return_value = mock_label