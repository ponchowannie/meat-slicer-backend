import pytest
from unittest.mock import MagicMock, patch
import os
import sys

# Add the parent directory to the Python path to access config globally
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from conveyor.conveyor import initialize_arduino, start_conveyor, stop_conveyor, send_command

@pytest.fixture
def mock_serial():
    with patch("conveyor.conveyor.serial.Serial") as mock_serial_class:
        mock_serial_instance = MagicMock()
        mock_serial_class.return_value = mock_serial_instance
        yield mock_serial_instance

def test_start_conveyor(mock_serial):
    initialize_arduino()
    start_conveyor()
    mock_serial.write.assert_called_with(b"START\n")

def test_stop_conveyor(mock_serial):
    initialize_arduino()
    stop_conveyor()
    mock_serial.write.assert_called_with(b"STOP\n")

def test_send_command(mock_serial):
    initialize_arduino()
    send_command("TEST")
    mock_serial.write.assert_called_with(b"TEST\n")
