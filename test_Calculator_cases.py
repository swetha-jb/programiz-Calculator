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
import tkinter as tk
from unittest.mock import MagicMock, patch

# Mock tkinter widgets and the Tk root window
class MockWidget:
    def __init__(self):
        self.children = {}
        self.config_calls = []
        self.pack_calls = []
        self.grid_calls = []
        self.bind_calls = []
        self.rowconfigure_calls = []
        self.columnconfigure_calls = []

    def configure(self, **kwargs):
        self.config_calls.append(kwargs)

    def config(self, **kwargs):
        self.config_calls.append(kwargs)

    def pack(self, **kwargs):
        self.pack_calls.append(kwargs)

    def grid(self, **kwargs):
        self.grid_calls.append(kwargs)

    def bind(self, event, command):
        self.bind_calls.append((event, command))

    def rowconfigure(self, index, weight):
        self.rowconfigure_calls.append((index, weight))

    def columnconfigure(self, index, weight):
        self.columnconfigure_calls.append((index, weight))

    def __setitem__(self, key, value):
        self.children[key] = value

    def __getitem__(self, key):
        return self.children.get(key)

    def mainloop(self):
        pass

    def destroy(self):
        pass

class MockTk:
    def __init__(self):
        self.root_window = MockWidget()
        self.root_window.geometry = MagicMock()
        self.root_window.resizable = MagicMock()
        self.root_window.title = MagicMock()
        self.Tk = MagicMock(return_value=self.root_window)
        self.Frame = MagicMock(return_value=MockWidget())
        self.Label = MagicMock(return_value=MockWidget())
        self.Button = MagicMock(return_value=MockWidget())

@pytest.fixture
def mock_tkinter():
    mock_tk_instance = MockTk()
    with patch('tkinter.Tk', mock_tk_instance.Tk), \
         patch('tkinter.Frame', mock_tk_instance.Frame), \
         patch('tkinter.Label', mock_tk_instance.Label), \
         patch('tkinter.Button', mock_tk_instance.Button):
        yield mock_tk_instance

@pytest.fixture
def calculator_instance(mock_tkinter):
    return Calculator()

def test_calculator_initialization(calculator_instance):
    assert calculator_instance.window is not None
    assert calculator_instance.total_expression == ""
    assert calculator_instance.current_expression == ""
    assert calculator_instance.display_frame is not None
    assert calculator_instance.total_label is not None
    assert calculator_instance.label is not None
    assert calculator_instance.buttons_frame is not None

def test_add_to_expression(calculator_instance):
    calculator_instance.add_to_expression("5")
    assert calculator_instance.current_expression == "5"
    calculator_instance.add_to_expression("+")
    assert calculator_instance.current_expression == "5+"
    calculator_instance.label.config.assert_called_with(text="5+")

def test_append_operator(calculator_instance):
    calculator_instance.current_expression = "123"
    calculator_instance.total_expression = "45"
    calculator_instance.append_operator("+")
    assert calculator_instance.total_expression == "45123"
    assert calculator_instance.current_expression == ""
    calculator_instance.total_label.config.assert_called_with(text="45 + 123")
    calculator_instance.label.config.assert_called_with(text="")

def test_clear(calculator_instance):
    calculator_instance.current_expression = "123"
    calculator_instance.total_expression = "45"
    calculator_instance.clear()
    assert calculator_instance.current_expression == ""
    assert calculator_instance.total_expression == ""
    calculator_instance.label.config.assert_called_with(text="")
    calculator_instance.total_label.config.assert_called_with(text="")

def test_square(calculator_instance):
    calculator_instance.current_expression = "5"
    calculator_instance.square()
    assert calculator_instance.current_expression == "25.0"
    calculator_instance.label.config.assert_called_with(text="25.0")

def test_sqrt(calculator_instance):
    calculator_instance.current_expression = "25"
    calculator_instance.sqrt()
    assert calculator_instance.current_expression == "5.0"
    calculator_instance.label.config.assert_called_with(text="5.0")

def test_evaluate_valid_expression(calculator_instance):
    calculator_instance.current_expression = "5"
    calculator_instance.total_expression = "2+3"
    calculator_instance.evaluate()
    assert calculator_instance.current_expression == "5"
    assert calculator_instance.total_expression == ""
    calculator_instance.total_label.config.assert_called_with(text="2 + 3")
    calculator_instance.label.config.assert_called_with(text="5")

def test_evaluate_error_expression(calculator_instance):
    calculator_instance.current_expression = "5"
    calculator_instance.total_expression = "2+"
    calculator_instance.evaluate()
    assert calculator_instance.current_expression == "Error"
    assert calculator_instance.total_expression == ""
    calculator_instance.total_label.config.assert_called_with(text="2 + ")
    calculator_instance.label.config.assert_called_with(text="Error")

def test_bind_keys_digit(calculator_instance):
    mock_event = MagicMock()
    # Find the bind call for digit '7'
    bind_call = next(call for call in calculator_instance.window.bind_calls if call[0] == '7')
    command = bind_call[1]
    command(mock_event)
    assert calculator_instance.current_expression == "7"

def test_bind_keys_operator(calculator_instance):
    mock_event = MagicMock()
    calculator_instance.current_expression = "5"
    calculator_instance.total_expression = "10"
    # Find the bind call for operator '+'
    bind_call = next(call for call in calculator_instance.window.bind_calls if call[0] == '+')
    command = bind_call[1]
    command(mock_event)
    assert calculator_instance.current_expression == ""
    assert calculator_instance.total_expression == "105"

def test_bind_keys_return(calculator_instance):
    mock_event = MagicMock()
    calculator_instance.current_expression = "5"
    calculator_instance.total_expression = "2+3"
    # Find the bind call for '<Return>'
    bind_call = next(call for call in calculator_instance.window.bind_calls if call[0] == '<Return>')
    command = bind_call[1]
    command(mock_event)
    assert calculator_instance.current_expression == "5"
    assert calculator_instance.total_expression == ""

def test_create_digit_buttons(calculator_instance):
    # Check if buttons are created and grid is called
    assert len(calculator_instance.buttons_frame.grid_calls) > 0
    # We can't directly check the command lambda's behavior without more complex mocking,
    # but we can check if the button creation and grid placement happened.

def test_create_operator_buttons(calculator_instance):
    # Check if operator buttons are created and grid is called
    assert len(calculator_instance.buttons_frame.grid_calls) > 0

def test_create_special_buttons(calculator_instance):
    # Check if special buttons are created and grid is called
    assert len(calculator_instance.buttons_frame.grid_calls) > 0

def test_update_label(calculator_instance):
    calculator_instance.current_expression = "12345678901"
    calculator_instance.update_label()
    calculator_instance.label.config.assert_called_with(text="12345678901")

def test_update_total_label(calculator_instance):
    calculator_instance.total_expression = "10+5"
    calculator_instance.update_total_label()