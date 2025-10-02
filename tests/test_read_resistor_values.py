from inline_snapshot import HasRepr
from inline_snapshot import snapshot
from kicad_sym_lib_access.get_lib_symbols import (
    real_resistor_value,
    read_resistor_values,
)

"""Tests for reading resistor values from KiCad symbol libraries."""


def test_real_resistor_value():
    """Test conversion of string resistor values to float, including IEC formats like '4k7' and '4R7'."""
    test_cases = {
        "1MΩ": 1e6,
        "10 ohm": 10.0,
        "10 Ohm": 10.0,
        "10 OHM": 10.0,
        "10 oHm": 10.0,
        "10 ohms": 10.0,
        "10 Ohms": 10.0,
        "10 OHMS": 10.0,
        "10 oHms": 10.0,
        "4.7kΩ": 4700.0,
        "2.2GΩ": 2.2e9,
        "100mΩ": 0.1,
        "5KΩ": 5000.0,
        "4k7Ω": 4700.0,  # IEC format
        "4R7Ω": 4.7,  # IEC format
        "4R7 Ohm": 4.7,  # IEC format
        "4R7 ohms": 4.7,  # IEC format
        "1M5Ω": 1.5e6,  # IEC format
        "1M5 Ohms": 1.5e6,  # IEC format
        "2m2Ω": 2.2e-3,  # IEC format
        "2m2 ohm": 2.2e-3,  # IEC format
    }

    for input_str, expected in test_cases.items():
        result = real_resistor_value(input_str)
        assert result == expected, f"Expected {expected} for input '{input_str}', got {result}"


def test_read_resistor_values():
    """Test reading resistor values from a KiCad symbol library."""

    # Test with a sample image path (replace 'sample_image.jpg' with an actual image path for real testing)
    library = "!Resistor-0603.kicad_sym"

    values = read_resistor_values(library)

    # pickle these values for future tests
    with open("tests/data/resistor_values.pkl", "wb") as f:
        import pickle

        pickle.dump(values, f)

    assert len(values) == snapshot(116), f"Got {len(values)}"
