import pytest
import tkinter as tk
from app import StarbucksRegexApp

@pytest.fixture
def root():
    root = tk.Tk()
    yield root
    root.destroy()

@pytest.fixture
def app(root):
    return StarbucksRegexApp(root)
