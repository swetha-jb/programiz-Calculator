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
from calculator import Calculator

@pytest.fixture
def mock_tkinter():
    with patch('tkinter.Tk') as MockTk, \
         patch('tkinter.Frame') as MockFrame, \
         patch('tkinter.Label') as MockLabel, \
         patch('tkinter.Button') as MockButton:

        mock_tk_instance = MockTk.return_value
        mock_tk_instance.geometry = MagicMock()
        mock_tk_instance.resizable = MagicMock()
        mock_tk_instance.title = MagicMock()
        mock_tk_instance.bind = MagicMock()
        mock_tk_instance.mainloop = MagicMock()

        mock_frame_instance = MockFrame.return_value
        mock_frame_instance.pack = MagicMock()
        mock_frame_instance.rowconfigure = MagicMock()
        mock_frame_instance.columnconfigure = MagicMock()

        mock_label_instance = MockLabel.return_value
        mock_label_instance.pack = MagicMock()
        mock_label_instance.config = MagicMock()

        mock_button_instance = MockButton.return_value
        mock_button_instance.grid = MagicMock()
        mock_button_instance.config = MagicMock()

        yield mock_tk_instance, mock_frame_instance, mock_label_instance, mock_button_instance

def test_calculator_initialization(mock_tkinter):
    mock_tk, mock_frame, mock_label, mock_button = mock_tkinter
    calc = Calculator()

    assert calc.window == mock_tk
    assert calc.total_expression == ""
    assert calc.current_expression == ""
    assert calc.display_frame == mock_frame
    assert calc.total_label == mock_label
    assert calc.label == mock_label
    assert isinstance(calc.digits, dict)
    assert isinstance(calc.operations, dict)
    assert calc.buttons_frame == mock_frame

    mock_tk.geometry.assert_called_once_with("375x667")
    mock_tk.resizable.assert_called_once_with(0, 0)
    mock_tk.title.assert_called_once_with("Calculator")

def test_add_to_expression(mock_tkinter):
    mock_tk, mock_frame, mock_label, mock_button = mock_tkinter
    calc = Calculator()
    calc.update_label = MagicMock()

    calc.add_to_expression("5")
    assert calc.current_expression == "5"
    calc.update_label.assert_called_once()

    calc.add_to_expression("+")
    assert calc.current_expression == "5+"
    calc.update_label.assert_called_once()

def test_append_operator(mock_tkinter):
    mock_tk, mock_frame, mock_label, mock_button = mock_tkinter
    calc = Calculator()
    calc.update_label = MagicMock()
    calc.update_total_label = MagicMock()

    calc.current_expression = "123"
    calc.append_operator("+")

    assert calc.total_expression == "123"
    assert calc.current_expression == ""
    calc.update_total_label.assert_called_once()
    calc.update_label.assert_called_once()

def test_clear(mock_tkinter):
    mock_tk, mock_frame, mock_label, mock_button = mock_tkinter
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

def test_square(mock_tkinter):
    mock_tk, mock_frame, mock_label, mock_button = mock_tkinter
    calc = Calculator()
    calc.update_label = MagicMock()

    calc.current_expression = "5"
    calc.square()
    assert calc.current_expression == "25"
    calc.update_label.assert_called_once()

    calc.current_expression = "2.5"
    calc.square()
    assert calc.current_expression == "6.25"
    calc.update_label.assert_called_once()

def test_sqrt(mock_tkinter):
    mock_tk, mock_frame, mock_label, mock_button = mock_tkinter
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

def test_evaluate_valid_expression(mock_tkinter):
    mock_tk, mock_frame, mock_label, mock_button = mock_tkinter
    calc = Calculator()
    calc.update_label = MagicMock()
    calc.update_total_label = MagicMock()

    calc.total_expression = "2+3"
    calc.current_expression = ""
    calc.evaluate()

    assert calc.current_expression == "5"
    assert calc.total_expression == ""
    calc.update_total_label.assert_called_once()
    calc.update_label.assert_called_once()

def test_evaluate_with_current_expression(mock_tkinter):
    mock_tk, mock_frame, mock_label, mock_button = mock_tkinter
    calc = Calculator()
    calc.update_label = MagicMock()
    calc.update_total_label = MagicMock()

    calc.total_expression = "10"
    calc.current_expression = "*2"
    calc.evaluate()

    assert calc.current_expression == "20"
    assert calc.total_expression == ""
    calc.update_total_label.assert_called_once()
    calc.update_label.assert_called_once()

def test_evaluate_error(mock_tkinter):
    mock_tk, mock_frame, mock_label, mock_button = mock_tkinter
    calc = Calculator()
    calc.update_label = MagicMock()
    calc.update_total_label = MagicMock()

    calc.total_expression = "2+"
    calc.current_expression = ""
    calc.evaluate()

    assert calc.current_expression == "Error"
    assert calc.total_expression == "2+"
    calc.update_total_label.assert_called_once()
    calc.update_label.assert_called_once()

def test_update_total_label(mock_tkinter):
    mock_tk, mock_frame, mock_label, mock_button = mock_tkinter
    calc = Calculator()
    calc.total_expression = "10*5"
    calc.update_total_label()
    calc.total_label.config.assert_called_once_with(text='10 × 5')

    calc.total_expression = "10/5"
    calc.update_total_label()
    calc.total_label.config.assert_called_with(text='10 ÷ 5')

def test_update_label(mock_tkinter):
    mock_tk, mock_frame, mock_label, mock_button = mock_tkinter
    calc = Calculator()
    calc.current_expression = "1234567890123"
    calc.update_label()
    calc.label.config.assert_called_once_with(text=calc.current_expression[:11])

    calc.current_expression = "short"
    calc.update_label()
    calc.label.config.assert_called_with(text="short")

if __name__ == "__main__":
    import pytest, sys
    sys.exit(pytest.main([__file__, "-v"]))