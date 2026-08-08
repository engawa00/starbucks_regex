import pytest
import tkinter as tk
import os
import subprocess
import time
from app import StarbucksRegexApp

@pytest.fixture(scope="session", autouse=True)
def virtual_display():
    if not os.environ.get('DISPLAY'):
        try:
            # Fallback to starting our own Xvfb process if no display exists
            xvfb = subprocess.Popen(['Xvfb', ':99', '-screen', '0', '1024x768x24'])
            os.environ['DISPLAY'] = ':99'
            time.sleep(0.5)  # give it time to start
            yield
            xvfb.terminate()
            xvfb.wait()
        except FileNotFoundError:
            # If Xvfb is not installed, just yield and let the tests possibly fail or skip
            yield
    else:
        yield

@pytest.fixture
def root():
    root = tk.Tk()
    yield root
    root.destroy()

@pytest.fixture
def app(root):
    return StarbucksRegexApp(root)
