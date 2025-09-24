"""Tests for reading resistor values from KiCad symbol libraries."""

from kicad_sym_lib_access.get_lib_symbols import (
    real_resistor_value,
    read_resistor_values,
)


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
        assert result == expected, (
            f"Expected {expected} for input '{input_str}', got {result}"
        )


def test_read_resistor_values():
    """Test reading resistor values from a KiCad symbol library."""

    # Test with a sample image path (replace 'sample_image.jpg' with an actual image path for real testing)
    library = "!Resistor-0603.kicad_sym"

    values = dict(
        sorted(read_resistor_values(library).items(), key=lambda item: item[1])
    )

    import pickle
    from pathlib import Path
    data_dir = Path(__file__).parent / "data"

    pickle.dump(values, open(data_dir / "resistor_values.pkl", "wb"))

    assert len(values) == 116
    for k, v in values.items():
        assert isinstance(k, str)
        assert isinstance(v, float)
        t = real_resistor_value(k)
        assert v == t, f"Value mismatch for {k}: got {v}, expected {t}"
