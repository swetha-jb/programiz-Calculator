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
from unittest.mock import MagicMock

sys.path.insert(0, r'/home/vvdn/projects/sfit_unitest_19_9_2025/cloned_repos/Calculator')

from calculator import Calculator

class MockTkinterWindow:
    def __init__(self):
        self.bind_calls = []
        self.config_calls = []
        self.geometry_calls = []
        self.resizable_calls = []
        self.title_calls = []
        self.mainloop_calls = []

    def bind(self, key, func):
        self.bind_calls.append((key, func))

    def config(self, **kwargs):
        self.config_calls.append(kwargs)

    def geometry(self, size):
        self.geometry_calls.append(size)

    def resizable(self, width, height):
        self.resizable_calls.append((width, height))

    def title(self, title):
        self.title_calls.append(title)

    def mainloop(self):
        self.mainloop_calls.append(True)

class MockTkinterWidget:
    def __init__(self):
        self.pack_calls = []
        self.grid_calls = []
        self.config_calls = []
        self.rowconfigure_calls = []
        self.columnconfigure_calls = []
        self.children = {}

    def pack(self, **kwargs):
        self.pack_calls.append(kwargs)

    def grid(self, **kwargs):
        self.grid_calls.append(kwargs)

    def config(self, **kwargs):
        self.config_calls.append(kwargs)

    def rowconfigure(self, index, weight):
        self.rowconfigure_calls.append((index, weight))

    def columnconfigure(self, index, weight):
        self.columnconfigure_calls.append((index, weight))

    def __setitem__(self, key, value):
        self.children[key] = value

    def __getitem__(self, key):
        return self.children[key]

@pytest.fixture
def mock_tkinter():
    mock_window = MockTkinterWindow()
    mock_frame = MockTkinterWidget()
    mock_label = MockTkinterWidget()
    mock_button = MockTkinterWidget()

    mock_tk = MagicMock()
    mock_tk.Tk.return_value = mock_window
    mock_tk.Frame.return_value = mock_frame
    mock_tk.Label.return_value = mock_label
    mock_tk.Button.return_value = mock_button

    tk.Tk = mock_tk
    tk.Frame = lambda master, **kwargs: mock_frame
    tk.Label = lambda master, **kwargs: mock_label
    tk.Button = lambda master, **kwargs: mock_button

    return mock_tk, mock_window, mock_frame, mock_label, mock_button

def test_calculator_initialization(mock_tkinter):
    mock_tk, mock_window, _, _, _ = mock_tkinter
    calc = Calculator()

    assert isinstance(calc.window, MockTkinterWindow)
    assert calc.total_expression == ""
    assert calc.current_expression == ""
    assert isinstance(calc.display_frame, MockTkinterWidget)
    assert isinstance(calc.total_label, MockTkinterWidget)
    assert isinstance(calc.label, MockTkinterWidget)
    assert isinstance(calc.buttons_frame, MockTkinterWidget)

    mock_window.geometry.assert_called_once_with("375x667")
    mock_window.resizable.assert_called_once_with(0, 0)
    mock_window.title.assert_called_once_with("Calculator")

def test_add_to_expression(mock_tkinter):
    mock_tk, mock_window, _, mock_label, _ = mock_tkinter
    calc = Calculator()
    calc.label.config = MagicMock()

    calc.add_to_expression(5)
    assert calc.current_expression == "5"
    calc.label.config.assert_called_once_with(text="5")

    calc.add_to_expression("+")
    assert calc.current_expression == "5+"
    calc.label.config.assert_called_with(text="5+")

def test_append_operator(mock_tkinter):
    mock_tk, mock_window, _, mock_label, _ = mock_tkinter
    calc = Calculator()
    calc.total_label.config = MagicMock()
    calc.label.config = MagicMock()

    calc.current_expression = "123"
    calc.append_operator("+")

    assert calc.total_expression == "123+"
    assert calc.current_expression == ""
    calc.total_label.config.assert_called_once_with(text=' 123 + ')
    calc.label.config.assert_called_once_with(text="")

def test_clear(mock_tkinter):
    mock_tk, mock_window, _, mock_label, _ = mock_tkinter
    calc = Calculator()
    calc.total_label.config = MagicMock()
    calc.label.config = MagicMock()

    calc.total_expression = "1+2"
    calc.current_expression = "3"
    calc.clear()

    assert calc.total_expression == ""
    assert calc.current_expression == ""
    calc.label.config.assert_called_once_with(text="")
    calc.total_label.config.assert_called_once_with(text="")

def test_square(mock_tkinter):
    mock_tk, mock_window, _, mock_label, _ = mock_tkinter
    calc = Calculator()
    calc.label.config = MagicMock()

    calc.current_expression = "5"
    calc.square()
    assert calc.current_expression == "25"
    calc.label.config.assert_called_once_with(text="25")

    calc.current_expression = "-3"
    calc.square()
    assert calc.current_expression == "9"
    calc.label.config.assert_called_with(text="9")

def test_sqrt(mock_tkinter):
    mock_tk, mock_window, _, mock_label, _ = mock_tkinter
    calc = Calculator()
    calc.label.config = MagicMock()

    calc.current_expression = "25"
    calc.sqrt()
    assert calc.current_expression == "5.0"
    calc.label.config.assert_called_once_with(text="5.0")

    calc.current_expression = "2"
    calc.sqrt()
    assert calc.current_expression == "1.4142135623730951"
    calc.label.config.assert_called_with(text="1.4142135623730951")

def test_evaluate_valid_expression(mock_tkinter):
    mock_tk, mock_window, _, mock_label, _ = mock_tkinter
    calc = Calculator()
    calc.total_label.config = MagicMock()
    calc.label.config = MagicMock()

    calc.total_expression = "2+3"
    calc.current_expression = ""
    calc.evaluate()

    assert calc.total_expression == ""
    assert calc.current_expression == "5"
    calc.total_label.config.assert_called_once_with(text=' 2 + 3 ')
    calc.label.config.assert_called_once_with(text="5")

def test_evaluate_expression_with_current(mock_tkinter):
    mock_tk, mock_window, _, mock_label, _ = mock_tkinter
    calc = Calculator()
    calc.total_label.config = MagicMock()
    calc.label.config = MagicMock()

    calc.total_expression = "10"
    calc.current_expression = "*2"
    calc.evaluate()

    assert calc.total_expression == ""
    assert calc.current_expression == "20"
    calc.total_label.config.assert_called_once_with(text=' 10 * 2 ')
    calc.label.config.assert_called_once_with(text="20")

def test_evaluate_error_expression(mock_tkinter):
    mock_tk, mock_window, _, mock_label, _ = mock_tkinter
    calc = Calculator()
    calc.total_label.config = MagicMock()
    calc.label.config = MagicMock()

    calc.total